"""
Versioning system for .cursorrules files.

This module provides functionality to version .cursorrules files,
maintain a history of changes, and perform rollbacks when needed.
"""

import os
import json
import time
import shutil
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import hashlib

from .core import RuleSet
from .utils import generate_cursorrules_file, save_cursorrules_file

@dataclass
class Version:
    """A version of a .cursorrules file."""
    version_id: str
    timestamp: float
    description: str = ""
    author: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def formatted_date(self) -> str:
        """Get the timestamp formatted as a human-readable date."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))

@dataclass
class VersionedFile:
    """A file with version history."""
    path: str
    current_version: str
    versions: Dict[str, Version] = field(default_factory=dict)
    
    def version_count(self) -> int:
        """Get the number of versions."""
        return len(self.versions)
    
    def get_version_path(self, version_id: str) -> str:
        """Get the path to a specific version."""
        if version_id not in self.versions:
            raise ValueError(f"Version {version_id} does not exist")
        
        version_dir = self._get_version_dir()
        return os.path.join(version_dir, version_id)
    
    def _get_version_dir(self) -> str:
        """Get the directory where versions are stored."""
        base_dir = os.path.dirname(self.path)
        basename = os.path.basename(self.path)
        version_dir = os.path.join(base_dir, f".{basename}_versions")
        return version_dir
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "path": self.path,
            "current_version": self.current_version,
            "versions": {
                version_id: {
                    "version_id": version.version_id,
                    "timestamp": version.timestamp,
                    "description": version.description,
                    "author": version.author,
                    "tags": version.tags,
                    "metadata": version.metadata
                }
                for version_id, version in self.versions.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionedFile':
        """Create from dictionary representation."""
        versioned_file = cls(
            path=data["path"],
            current_version=data["current_version"],
        )
        
        for version_id, version_data in data["versions"].items():
            versioned_file.versions[version_id] = Version(
                version_id=version_data["version_id"],
                timestamp=version_data["timestamp"],
                description=version_data.get("description", ""),
                author=version_data.get("author", ""),
                tags=version_data.get("tags", []),
                metadata=version_data.get("metadata", {})
            )
        
        return versioned_file

class VersionManager:
    """Manages versioning for .cursorrules files."""
    
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()
        self.index_path = os.path.join(self.base_dir, ".cursorrules_versions_index")
        self.versioned_files: Dict[str, VersionedFile] = {}
        self._load_index()
    
    def _load_index(self) -> None:
        """Load the version index if it exists."""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'r') as f:
                    data = json.load(f)
                
                for file_path, file_data in data.items():
                    self.versioned_files[file_path] = VersionedFile.from_dict(file_data)
            except Exception as e:
                print(f"Warning: Failed to load version index: {e}")
                self.versioned_files = {}
    
    def _save_index(self) -> None:
        """Save the version index."""
        try:
            with open(self.index_path, 'w') as f:
                json.dump({
                    file_path: file.to_dict()
                    for file_path, file in self.versioned_files.items()
                }, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save version index: {e}")
    
    def is_file_versioned(self, file_path: str) -> bool:
        """Check if a file is versioned."""
        return file_path in self.versioned_files
    
    def get_versioned_file(self, file_path: str) -> Optional[VersionedFile]:
        """Get a versioned file if it exists."""
        return self.versioned_files.get(file_path)
    
    def create_version(self, file_path: str, description: str = "", 
                       author: str = "", tags: List[str] = None) -> str:
        """
        Create a new version of a file.
        
        Args:
            file_path: Path to the file to version
            description: Description of the version
            author: Author of the version
            tags: Tags for the version
            
        Returns:
            The version ID
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        
        # Generate a hash of the file content to use as version ID
        with open(file_path, 'rb') as f:
            content = f.read()
            version_id = hashlib.sha1(content).hexdigest()[:10]
        
        # Create the version directory if it doesn't exist
        if file_path not in self.versioned_files:
            # This is a new file to version
            versioned_file = VersionedFile(path=file_path, current_version=version_id)
            self.versioned_files[file_path] = versioned_file
        else:
            # This file is already versioned
            versioned_file = self.versioned_files[file_path]
            
            # Check if this exact content is already versioned
            if version_id in versioned_file.versions:
                # Update the current version and return
                versioned_file.current_version = version_id
                self._save_index()
                return version_id
        
        # Create the version directory
        version_dir = versioned_file._get_version_dir()
        os.makedirs(version_dir, exist_ok=True)
        
        # Copy the file to the version directory
        version_path = os.path.join(version_dir, version_id)
        shutil.copy2(file_path, version_path)
        
        # Create the version
        version = Version(
            version_id=version_id,
            timestamp=time.time(),
            description=description,
            author=author,
            tags=tags or []
        )
        
        # Add the version to the versioned file
        versioned_file.versions[version_id] = version
        versioned_file.current_version = version_id
        
        # Save the index
        self._save_index()
        
        return version_id
    
    def list_versions(self, file_path: str) -> List[Version]:
        """
        List all versions of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of versions, sorted by timestamp (newest first)
        """
        if file_path not in self.versioned_files:
            return []
        
        versioned_file = self.versioned_files[file_path]
        versions = list(versioned_file.versions.values())
        versions.sort(key=lambda v: v.timestamp, reverse=True)
        
        return versions
    
    def get_current_version(self, file_path: str) -> Optional[Version]:
        """
        Get the current version of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            The current version, or None if the file is not versioned
        """
        if file_path not in self.versioned_files:
            return None
        
        versioned_file = self.versioned_files[file_path]
        return versioned_file.versions.get(versioned_file.current_version)
    
    def get_version(self, file_path: str, version_id: str) -> Optional[Version]:
        """
        Get a specific version of a file.
        
        Args:
            file_path: Path to the file
            version_id: Version ID
            
        Returns:
            The version, or None if not found
        """
        if file_path not in self.versioned_files:
            return None
        
        versioned_file = self.versioned_files[file_path]
        return versioned_file.versions.get(version_id)
    
    def get_version_content(self, file_path: str, version_id: str) -> str:
        """
        Get the content of a specific version of a file.
        
        Args:
            file_path: Path to the file
            version_id: Version ID
            
        Returns:
            The content of the version
        """
        if file_path not in self.versioned_files:
            raise ValueError(f"File {file_path} is not versioned")
        
        versioned_file = self.versioned_files[file_path]
        if version_id not in versioned_file.versions:
            raise ValueError(f"Version {version_id} of file {file_path} does not exist")
        
        version_path = versioned_file.get_version_path(version_id)
        with open(version_path, 'r') as f:
            return f.read()
    
    def rollback(self, file_path: str, version_id: str) -> None:
        """
        Roll back a file to a specific version.
        
        Args:
            file_path: Path to the file
            version_id: Version ID to roll back to
        """
        if file_path not in self.versioned_files:
            raise ValueError(f"File {file_path} is not versioned")
        
        versioned_file = self.versioned_files[file_path]
        if version_id not in versioned_file.versions:
            raise ValueError(f"Version {version_id} of file {file_path} does not exist")
        
        # Get the version content
        version_path = versioned_file.get_version_path(version_id)
        
        # Copy the version back to the original file
        shutil.copy2(version_path, file_path)
        
        # Update the current version
        versioned_file.current_version = version_id
        
        # Save the index
        self._save_index()
    
    def get_diff(self, file_path: str, version_id1: str, version_id2: str) -> str:
        """
        Get a diff between two versions of a file.
        
        Args:
            file_path: Path to the file
            version_id1: First version ID
            version_id2: Second version ID
            
        Returns:
            A unified diff
        """
        content1 = self.get_version_content(file_path, version_id1).splitlines()
        content2 = self.get_version_content(file_path, version_id2).splitlines()
        
        diff = difflib.unified_diff(
            content1, 
            content2,
            f"{file_path} (version {version_id1})",
            f"{file_path} (version {version_id2})",
            lineterm=""
        )
        
        return "\n".join(diff)
    
    def delete_version(self, file_path: str, version_id: str) -> None:
        """
        Delete a version of a file.
        
        Args:
            file_path: Path to the file
            version_id: Version ID to delete
        """
        if file_path not in self.versioned_files:
            raise ValueError(f"File {file_path} is not versioned")
        
        versioned_file = self.versioned_files[file_path]
        if version_id not in versioned_file.versions:
            raise ValueError(f"Version {version_id} of file {file_path} does not exist")
        
        # Check if trying to delete the current version
        if version_id == versioned_file.current_version:
            raise ValueError(f"Cannot delete the current version ({version_id}) of file {file_path}")
        
        # Delete the version file
        version_path = versioned_file.get_version_path(version_id)
        if os.path.exists(version_path):
            os.remove(version_path)
        
        # Remove the version from the versioned file
        del versioned_file.versions[version_id]
        
        # Save the index
        self._save_index()
    
    def create_versioned_cursorrules(self, ruleset: RuleSet, output_path: str,
                                    project_info: Optional[Dict[str, Any]] = None,
                                    description: str = "", author: str = "",
                                    tags: List[str] = None) -> str:
        """
        Create a versioned .cursorrules file.
        
        Args:
            ruleset: The ruleset to generate the .cursorrules file from
            output_path: Path to save the .cursorrules file
            project_info: Optional project information
            description: Description of the version
            author: Author of the version
            tags: Tags for the version
            
        Returns:
            The version ID
        """
        # Generate the .cursorrules file content
        content = generate_cursorrules_file(ruleset, project_info)
        
        # Save the content to the output path
        save_cursorrules_file(content, output_path)
        
        # Create a version
        version_id = self.create_version(output_path, description, author, tags)
        
        return version_id 