"""
Code monitoring module for detecting changes in the codebase.

This module provides functionality to monitor the codebase for significant changes
and trigger updates to .cursorrules files when necessary.
"""

import os
import re
import time
import json
import hashlib
import logging
from typing import Dict, List, Set, Optional, Any, Tuple, Callable
from pathlib import Path
import fnmatch
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading

from .core import RuleSet
from .llm_connector import MultiLLMProcessor, LLMRequest, LLMProvider
from .versioning import VersionManager
from .utils import generate_cursorrules_file, save_cursorrules_file

# Set up logging
logger = logging.getLogger("cursor_rules.code_monitor")

@dataclass
class FileSnapshot:
    """A snapshot of a file's state."""
    path: str
    hash: str
    last_modified: float
    size: int
    ignored: bool = False

@dataclass
class DirectorySnapshot:
    """A snapshot of a directory's state."""
    path: str
    files: Dict[str, FileSnapshot] = field(default_factory=dict)
    subdirectories: Dict[str, 'DirectorySnapshot'] = field(default_factory=dict)
    
    def get_all_files(self) -> Dict[str, FileSnapshot]:
        """Get all files in this directory and subdirectories."""
        all_files = {}
        all_files.update(self.files)
        
        for subdir in self.subdirectories.values():
            all_files.update(subdir.get_all_files())
        
        return all_files

@dataclass
class CodebaseChange:
    """A change in the codebase."""
    timestamp: float
    changed_files: List[str]
    added_files: List[str]
    deleted_files: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def formatted_date(self) -> str:
        """Get the timestamp formatted as a human-readable date."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
    
    @property
    def total_changes(self) -> int:
        """Get the total number of changes."""
        return len(self.changed_files) + len(self.added_files) + len(self.deleted_files)
    
    def is_significant(self, threshold: int = 5) -> bool:
        """Check if this change is significant based on the number of files changed."""
        return self.total_changes >= threshold

class CodeMonitor:
    """Monitors the codebase for changes."""
    
    def __init__(self, base_dir: str, cursorrules_path: str,
                 ignore_patterns: List[str] = None,
                 poll_interval: int = 300,
                 change_threshold: int = 5):
        """
        Initialize the code monitor.
        
        Args:
            base_dir: Base directory to monitor
            cursorrules_path: Path to the .cursorrules file
            ignore_patterns: Patterns to ignore (glob syntax)
            poll_interval: How often to check for changes (in seconds)
            change_threshold: How many files need to change to trigger an update
        """
        self.base_dir = os.path.abspath(base_dir)
        self.cursorrules_path = cursorrules_path
        self.ignore_patterns = ignore_patterns or []
        self.poll_interval = poll_interval
        self.change_threshold = change_threshold
        
        # Add common ignore patterns
        self.ignore_patterns.extend([
            "**/.git/**",
            "**/.svn/**",
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            "**/node_modules/**",
            "**/venv/**",
            "**/.env/**",
            "**/.venv/**",
            "**/.idea/**",
            "**/.vs/**",
            "**/.vscode/**",
            "**/dist/**",
            "**/build/**"
        ])
        
        # Latest snapshot of the codebase
        self.current_snapshot = None
        
        # History of changes
        self.changes: List[CodebaseChange] = []
        
        # Flag to control monitoring thread
        self.monitoring = False
        self.monitor_thread = None
        
        # Version manager for the .cursorrules file
        self.version_manager = VersionManager(base_dir)
        
        # LLM processor for updating rules
        self.llm_processor = MultiLLMProcessor()
        
        # Take an initial snapshot
        self.current_snapshot = self._take_snapshot()
    
    def _is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored."""
        rel_path = os.path.relpath(path, self.base_dir)
        
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        
        return False
    
    def _get_file_hash(self, path: str) -> str:
        """Get a hash of a file's content."""
        try:
            with open(path, 'rb') as f:
                return hashlib.sha1(f.read()).hexdigest()
        except (IOError, OSError):
            # If we can't read the file, use a hash of the path and modification time
            stat = os.stat(path)
            return hashlib.sha1(f"{path}:{stat.st_mtime}".encode()).hexdigest()
    
    def _take_snapshot(self) -> DirectorySnapshot:
        """Take a snapshot of the codebase."""
        def scan_directory(dir_path: str) -> DirectorySnapshot:
            snapshot = DirectorySnapshot(path=dir_path)
            
            try:
                with os.scandir(dir_path) as entries:
                    for entry in entries:
                        if self._is_ignored(entry.path):
                            continue
                            
                        if entry.is_file():
                            try:
                                stat = entry.stat()
                                snapshot.files[entry.path] = FileSnapshot(
                                    path=entry.path,
                                    hash=self._get_file_hash(entry.path),
                                    last_modified=stat.st_mtime,
                                    size=stat.st_size
                                )
                            except (IOError, OSError):
                                # Skip files we can't access
                                pass
                        elif entry.is_dir():
                            try:
                                subdir_snapshot = scan_directory(entry.path)
                                snapshot.subdirectories[entry.path] = subdir_snapshot
                            except (IOError, OSError):
                                # Skip directories we can't access
                                pass
            except (IOError, OSError):
                # Skip directories we can't access
                pass
                
            return snapshot
        
        return scan_directory(self.base_dir)
    
    def _detect_changes(self) -> Optional[CodebaseChange]:
        """
        Detect changes since the last snapshot.
        
        Returns:
            A CodebaseChange object if changes were detected, None otherwise
        """
        if not self.current_snapshot:
            return None
            
        old_snapshot = self.current_snapshot
        new_snapshot = self._take_snapshot()
        
        old_files = old_snapshot.get_all_files()
        new_files = new_snapshot.get_all_files()
        
        changed_files = []
        added_files = []
        deleted_files = []
        
        # Find changed and deleted files
        for path, old_file in old_files.items():
            if path not in new_files:
                deleted_files.append(path)
            elif new_files[path].hash != old_file.hash:
                changed_files.append(path)
        
        # Find added files
        for path in new_files:
            if path not in old_files:
                added_files.append(path)
        
        # Update the current snapshot
        self.current_snapshot = new_snapshot
        
        if changed_files or added_files or deleted_files:
            return CodebaseChange(
                timestamp=time.time(),
                changed_files=changed_files,
                added_files=added_files,
                deleted_files=deleted_files
            )
        
        return None
    
    def _get_file_content_summary(self, paths: List[str], max_files: int = 10) -> Dict[str, str]:
        """
        Get a summary of file contents for the most relevant files.
        
        Args:
            paths: List of file paths
            max_files: Maximum number of files to include
            
        Returns:
            Dictionary mapping file paths to content
        """
        # Sort paths by modification time (newest first)
        sorted_paths = sorted(
            paths,
            key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0,
            reverse=True
        )
        
        # Only include text files and limit to max_files
        text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss',
            '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.sh', '.bash',
            '.c', '.cpp', '.h', '.hpp', '.java', '.kt', '.swift', '.go', '.rs',
            '.rb', '.php'
        }
        
        result = {}
        count = 0
        
        for path in sorted_paths:
            if count >= max_files:
                break
                
            # Skip files we can't access or that are too large
            try:
                if not os.path.exists(path) or not os.path.isfile(path):
                    continue
                    
                # Only include files with text extensions
                ext = os.path.splitext(path)[1].lower()
                if ext not in text_extensions:
                    continue
                    
                # Skip files that are too large
                if os.path.getsize(path) > 1_000_000:  # 1MB
                    continue
                    
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Skip binary files (heuristic)
                if '\0' in content:
                    continue
                    
                result[path] = content
                count += 1
                
            except Exception:
                # Skip any files we can't read
                continue
        
        return result
    
    def _generate_change_summary(self, change: CodebaseChange) -> str:
        """
        Generate a human-readable summary of changes.
        
        Args:
            change: The change to summarize
            
        Returns:
            A string summarizing the changes
        """
        lines = [f"Changes detected at {change.formatted_date}:"]
        
        if change.added_files:
            lines.append(f"\nAdded files ({len(change.added_files)}):")
            for path in sorted(change.added_files)[:10]:  # Limit to 10 files
                rel_path = os.path.relpath(path, self.base_dir)
                lines.append(f"  + {rel_path}")
            if len(change.added_files) > 10:
                lines.append(f"  ... and {len(change.added_files) - 10} more")
        
        if change.changed_files:
            lines.append(f"\nModified files ({len(change.changed_files)}):")
            for path in sorted(change.changed_files)[:10]:  # Limit to 10 files
                rel_path = os.path.relpath(path, self.base_dir)
                lines.append(f"  * {rel_path}")
            if len(change.changed_files) > 10:
                lines.append(f"  ... and {len(change.changed_files) - 10} more")
        
        if change.deleted_files:
            lines.append(f"\nDeleted files ({len(change.deleted_files)}):")
            for path in sorted(change.deleted_files)[:10]:  # Limit to 10 files
                rel_path = os.path.relpath(path, self.base_dir)
                lines.append(f"  - {rel_path}")
            if len(change.deleted_files) > 10:
                lines.append(f"  ... and {len(change.deleted_files) - 10} more")
        
        return "\n".join(lines)
    
    def _generate_updated_rules(self, change: CodebaseChange) -> Optional[RuleSet]:
        """
        Generate updated rules based on codebase changes.
        
        Args:
            change: The changes that triggered the update
            
        Returns:
            A new RuleSet, or None if the update failed
        """
        # Get a summary of the changed files
        all_changed = change.changed_files + change.added_files
        file_contents = self._get_file_content_summary(all_changed)
        
        # Prepare a summary for the LLM
        change_summary = self._generate_change_summary(change)
        
        # Include a sample of file contents
        file_samples = []
        for path, content in file_contents.items():
            rel_path = os.path.relpath(path, self.base_dir)
            # Limit content to ~2000 chars for each file
            if len(content) > 2000:
                content = content[:2000] + "...[truncated]"
            file_samples.append(f"File: {rel_path}\n\n{content}\n\n")
        
        # Get the current ruleset content
        current_ruleset_content = ""
        try:
            with open(self.cursorrules_path, 'r', encoding='utf-8') as f:
                current_ruleset_content = f.read()
        except Exception as e:
            logger.warning(f"Failed to read current ruleset: {e}")
        
        # Create prompt for the LLM
        prompt = f"""
        I need to update the .cursorrules file for a project based on recent code changes.
        
        Current .cursorrules file content:
        {current_ruleset_content}
        
        Summary of changes:
        {change_summary}
        
        Here are samples of the changed/added files:
        
        {"".join(file_samples[:5])}
        
        Based on these changes, please update the ruleset to better reflect the current state of the project.
        Think about the following:
        - Do we need new rules based on new patterns or technologies introduced?
        - Should any existing rules be modified or removed?
        - Are there any new best practices that should be enforced?
        
        Please generate a complete JSON representation of the updated ruleset, maintaining the same structure.
        """
        
        try:
            # Use the LLM processor to generate a new ruleset
            ruleset, _ = self.llm_processor.generate_rules_with_multiple_llms(prompt)
            return ruleset
        except Exception as e:
            logger.error(f"Failed to generate updated rules: {e}")
            return None
    
    def _update_rules(self, change: CodebaseChange) -> Optional[str]:
        """
        Update the .cursorrules file based on codebase changes.
        
        Args:
            change: The changes that triggered the update
            
        Returns:
            The new version ID, or None if the update failed
        """
        try:
            # Generate updated rules
            new_ruleset = self._generate_updated_rules(change)
            
            if not new_ruleset:
                logger.warning("Failed to generate updated rules")
                return None
            
            # Create a description for the new version
            description = f"Auto-update triggered by {change.total_changes} changes"
            
            # Create a new version of the .cursorrules file
            version_id = self.version_manager.create_versioned_cursorrules(
                ruleset=new_ruleset,
                output_path=self.cursorrules_path,
                description=description,
                tags=["auto-update"]
            )
            
            logger.info(f"Created new version {version_id} of .cursorrules file")
            return version_id
            
        except Exception as e:
            logger.error(f"Failed to update rules: {e}")
            return None
    
    def check_for_changes(self) -> Optional[CodebaseChange]:
        """
        Check for changes in the codebase and update rules if necessary.
        
        Returns:
            A CodebaseChange object if changes were detected, None otherwise
        """
        # Detect changes
        change = self._detect_changes()
        
        if not change:
            logger.debug("No changes detected")
            return None
        
        logger.info(f"Detected {change.total_changes} changes")
        
        # Add to history
        self.changes.append(change)
        
        # If the change is significant, update the rules
        if change.is_significant(self.change_threshold):
            logger.info(f"Change is significant ({change.total_changes} files), updating rules")
            version_id = self._update_rules(change)
            if version_id:
                change.metadata["version_id"] = version_id
        else:
            logger.info(f"Change is not significant ({change.total_changes} files), not updating rules")
        
        return change
    
    def start_monitoring(self) -> None:
        """Start monitoring the codebase in a background thread."""
        if self.monitoring:
            logger.warning("Already monitoring")
            return
        
        self.monitoring = True
        
        def monitor_loop():
            logger.info(f"Starting to monitor {self.base_dir}")
            
            while self.monitoring:
                try:
                    self.check_for_changes()
                except Exception as e:
                    logger.error(f"Error in monitor loop: {e}")
                
                # Wait for the next check
                time.sleep(self.poll_interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Monitoring thread started, checking every {self.poll_interval} seconds")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring the codebase."""
        if not self.monitoring:
            logger.warning("Not monitoring")
            return
        
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None
        
        logger.info("Monitoring stopped")

class GitChangesDetector:
    """Detects changes in a Git repository."""
    
    def __init__(self, repo_path: str):
        """
        Initialize the Git changes detector.
        
        Args:
            repo_path: Path to the Git repository
        """
        self.repo_path = os.path.abspath(repo_path)
        
        # Check if this is a Git repository
        if not os.path.isdir(os.path.join(self.repo_path, '.git')):
            raise ValueError(f"{self.repo_path} is not a Git repository")
    
    def _run_git_command(self, command: List[str]) -> str:
        """
        Run a Git command and return the output.
        
        Args:
            command: Git command to run (excluding 'git')
            
        Returns:
            Command output
        """
        full_command = ['git'] + command
        
        try:
            result = subprocess.run(
                full_command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            raise
    
    def get_changes_since_commit(self, commit: str) -> CodebaseChange:
        """
        Get changes since a specific commit.
        
        Args:
            commit: Commit hash or reference (e.g., 'HEAD~5')
            
        Returns:
            A CodebaseChange object
        """
        # Get the list of changed files
        changed_output = self._run_git_command(['diff', '--name-status', commit])
        
        changed_files = []
        added_files = []
        deleted_files = []
        
        for line in changed_output.splitlines():
            if not line.strip():
                continue
                
            status, file_path = line.split('\t', 1)
            abs_path = os.path.abspath(os.path.join(self.repo_path, file_path))
            
            if status == 'A':
                added_files.append(abs_path)
            elif status == 'D':
                deleted_files.append(abs_path)
            else:  # M, R, C, etc.
                changed_files.append(abs_path)
        
        # Get the commit timestamp
        timestamp_output = self._run_git_command(['show', '-s', '--format=%ct', commit])
        timestamp = float(timestamp_output.strip())
        
        return CodebaseChange(
            timestamp=timestamp,
            changed_files=changed_files,
            added_files=added_files,
            deleted_files=deleted_files,
            metadata={"commit": commit}
        )
    
    def get_changes_since_date(self, date: datetime) -> CodebaseChange:
        """
        Get changes since a specific date.
        
        Args:
            date: Date to get changes since
            
        Returns:
            A CodebaseChange object
        """
        # Format the date as ISO 8601
        date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Find the most recent commit before this date
        commit_output = self._run_git_command(['rev-list', '--max-count=1', '--before', date_str, 'HEAD'])
        
        if not commit_output:
            # No commits before this date, use the first commit
            commit_output = self._run_git_command(['rev-list', '--max-parents=0', 'HEAD'])
        
        return self.get_changes_since_commit(commit_output.strip())
    
    def get_latest_changes(self, count: int = 1) -> CodebaseChange:
        """
        Get the latest changes.
        
        Args:
            count: Number of commits to include
            
        Returns:
            A CodebaseChange object
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
            
        return self.get_changes_since_commit(f"HEAD~{count}")

def create_monitor_for_project(project_dir: str, cursorrules_path: str = None) -> CodeMonitor:
    """
    Create a code monitor for a project.
    
    Args:
        project_dir: Path to the project directory
        cursorrules_path: Path to the .cursorrules file, or None to use the default
        
    Returns:
        A CodeMonitor instance
    """
    if not os.path.isdir(project_dir):
        raise ValueError(f"{project_dir} is not a directory")
    
    # If no cursorrules_path is provided, use the default
    if not cursorrules_path:
        cursorrules_path = os.path.join(project_dir, '.cursorrules')
    
    # Determine if this is a Git repository
    is_git_repo = os.path.isdir(os.path.join(project_dir, '.git'))
    
    # Create the monitor
    monitor = CodeMonitor(
        base_dir=project_dir,
        cursorrules_path=cursorrules_path
    )
    
    # If this is a Git repository, try to seed the changes from recent commits
    if is_git_repo:
        try:
            git_detector = GitChangesDetector(project_dir)
            # Get changes from the last 10 commits
            changes = git_detector.get_latest_changes(10)
            monitor.changes.append(changes)
            logger.info(f"Seeded changes from Git: {changes.total_changes} files")
        except Exception as e:
            logger.warning(f"Failed to seed changes from Git: {e}")
    
    return monitor 