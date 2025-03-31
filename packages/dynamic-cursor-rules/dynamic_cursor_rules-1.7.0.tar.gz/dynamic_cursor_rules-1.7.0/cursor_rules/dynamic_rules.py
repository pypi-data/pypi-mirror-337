"""
Dynamic rule management for Cursor Rules.

This module provides functionality to generate and update dynamic rules
based on the current project state and code analysis.
"""

import os
import json
import time
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .core import Rule, RuleSet, ProjectState, Component, ComponentStatus, ProjectPhase
from .versioning import VersionManager
from .utils import save_modern_cursor_rules
from .llm_connector import LLMProvider, LLMConnector, LLMRequest
from .code_monitor import CodeMonitor

# Set up logger
logger = logging.getLogger(__name__)

class DynamicRuleManager:
    """
    Manages the generation and updating of dynamic Cursor Rules.
    """
    
    def __init__(self, project_dir: str, project_state: Optional[ProjectState] = None):
        """
        Initialize the dynamic rule manager.
        
        Args:
            project_dir: The root directory of the project
            project_state: Optional ProjectState object. If not provided, one will be created.
        """
        self.project_dir = project_dir
        self.cursor_dir = os.path.join(project_dir, ".cursor")
        self.rules_dir = os.path.join(self.cursor_dir, "rules")
        self.history_dir = os.path.join(self.cursor_dir, "history")
        self.state_file = os.path.join(self.cursor_dir, "project_state.json")
        
        # Create necessary directories
        os.makedirs(self.cursor_dir, exist_ok=True)
        os.makedirs(self.rules_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Initialize project state
        self.project_state = project_state or self._load_project_state()
        
        # Initialize version manager
        self.version_manager = VersionManager(self.cursor_dir)
        
        # Initialize code change monitor
        self.code_monitor = CodeMonitor(self.project_dir)
        
        # Initialize LLM connector
        self.llm_connector = LLMConnector()
        self.llm_provider = self._determine_best_provider()
    
    def _load_project_state(self) -> ProjectState:
        """
        Load project state from file or create a new one.
        
        Returns:
            A ProjectState object
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return ProjectState.from_dict(data)
            except Exception as e:
                logger.warning(f"Failed to load project state: {e}. Creating new state.")
        
        # Create a default project state
        return ProjectState(
            name=os.path.basename(self.project_dir),
            description="Project generated with Cursor Rules",
            last_updated=datetime.now().isoformat()
        )
    
    def _save_project_state(self) -> None:
        """Save the current project state to file."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.project_state.to_dict(), f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save project state: {e}")
    
    def _determine_best_provider(self) -> LLMProvider:
        """Determine the best available LLM provider."""
        available_providers = self.llm_connector.list_available_providers()
        if available_providers:
            return available_providers[0]
        return LLMProvider.OPENAI  # Default
    
    def update_project_state(self, 
                            name: Optional[str] = None,
                            description: Optional[str] = None,
                            phase: Optional[ProjectPhase] = None,
                            components: Optional[Dict[str, Component]] = None,
                            active_features: Optional[List[str]] = None,
                            tech_stack: Optional[Dict[str, List[str]]] = None,
                            directory_structure: Optional[Dict[str, str]] = None) -> None:
        """
        Update the project state with new information.
        
        Args:
            name: New project name
            description: New project description
            phase: New project phase
            components: New components dictionary
            active_features: New active features list
            tech_stack: New tech stack dictionary
            directory_structure: New directory structure dictionary
        """
        if name is not None:
            self.project_state.name = name
        
        if description is not None:
            self.project_state.description = description
        
        if phase is not None:
            self.project_state.phase = phase
        
        if components is not None:
            self.project_state.components = components
        
        if active_features is not None:
            self.project_state.active_features = active_features
        
        if tech_stack is not None:
            self.project_state.tech_stack = tech_stack
        
        if directory_structure is not None:
            self.project_state.directory_structure = directory_structure
        
        # Update the last updated timestamp
        self.project_state.last_updated = datetime.now().isoformat()
        
        # Save the updated state
        self._save_project_state()
    
    def add_or_update_component(self, component: Component) -> None:
        """
        Add or update a component in the project state.
        
        Args:
            component: The component to add or update
        """
        self.project_state.add_component(component)
        self.project_state.last_updated = datetime.now().isoformat()
        self._save_project_state()
    
    def detect_project_changes(self) -> bool:
        """
        Detect changes in the project and update state accordingly.
        
        Returns:
            True if changes were detected, False otherwise
        """
        changes_detected = False
        
        # Get code changes since last update
        changes = self.code_monitor.get_changes_since(self.project_state.last_updated)
        
        if changes:
            changes_detected = True
            
            # Update directory structure based on changes
            dirs = set()
            for file_path in changes:
                dir_path = os.path.dirname(file_path)
                if dir_path and not dir_path.startswith('.'):
                    dirs.add(dir_path)
            
            # Update directory structure if new directories found
            for dir_path in dirs:
                rel_path = os.path.relpath(dir_path, self.project_dir)
                if rel_path not in self.project_state.directory_structure:
                    self.project_state.directory_structure[rel_path] = "Auto-detected directory"
            
            # Analyze tech stack from files if LLM is available
            if self.llm_connector.is_provider_available(self.llm_provider):
                tech_stack = self._analyze_tech_stack_from_files(changes)
                if tech_stack:
                    # Merge with existing tech stack
                    for category, techs in tech_stack.items():
                        if category in self.project_state.tech_stack:
                            # Add new technologies
                            for tech in techs:
                                if tech not in self.project_state.tech_stack[category]:
                                    self.project_state.tech_stack[category].append(tech)
                        else:
                            self.project_state.tech_stack[category] = techs
            
            # Save the updated state
            self.project_state.last_updated = datetime.now().isoformat()
            self._save_project_state()
        
        return changes_detected
    
    def _analyze_tech_stack_from_files(self, file_paths: List[str]) -> Dict[str, List[str]]:
        """
        Analyze the tech stack from the given files using an LLM.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            A dictionary mapping tech categories to lists of technologies
        """
        try:
            # Get file content to analyze
            file_content = ""
            for file_path in file_paths[:10]:  # Limit to 10 files to avoid huge prompts
                if os.path.exists(file_path) and os.path.getsize(file_path) < 100000:  # Limit to 100KB
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            file_content += f"\n\nFile: {file_path}\n```\n{content[:1000]}...\n```\n"
                    except Exception:
                        pass
            
            if not file_content:
                return {}
            
            # Create a request to analyze the tech stack
            system_message = """
            You are an expert at analyzing code to detect technologies, frameworks, and libraries.
            Given code snippets, identify the technologies being used and categorize them.
            
            Respond with a JSON object where keys are categories (frontend, backend, database, etc.)
            and values are arrays of specific technologies. For example:
            
            {
              "frontend": ["React", "Tailwind CSS"],
              "backend": ["Node.js", "Express"],
              "database": ["MongoDB"],
              "devops": ["Docker"]
            }
            
            Only include technologies that you can confidently identify from the code.
            """
            
            prompt = f"""
            Please analyze the following code snippets and identify the technologies, frameworks, and libraries being used:
            
            {file_content}
            
            Respond with a JSON object categorizing the technologies.
            """
            
            request = LLMRequest(
                prompt=prompt,
                system_message=system_message,
                provider=self.llm_provider,
                temperature=0.1,
                max_tokens=1000
            )
            
            response = self.llm_connector.request(request)
            response_text = response.text.strip()
            
            # Extract the JSON
            import re
            json_match = re.search(r'(\{[\s\S]*\})', response_text)
            if json_match:
                json_str = json_match.group(1)
                tech_stack = json.loads(json_str)
                return tech_stack
            
            return {}
            
        except Exception as e:
            logger.warning(f"Failed to analyze tech stack from files: {e}")
            return {}
    
    def generate_dynamic_rules(self, force_regenerate: bool = False) -> List[str]:
        """
        Generate dynamic cursor rules based on the current project state.
        
        Args:
            force_regenerate: If True, regenerate all rules even if no changes detected
            
        Returns:
            List of paths to the generated rule files
        """
        # First check for project changes
        changes_detected = self.detect_project_changes()
        
        if not changes_detected and not force_regenerate:
            # No changes detected and not forced to regenerate
            logger.info("No changes detected. Skipping rule generation.")
            return []
        
        # Generate the rules
        generated_files = []
        
        # Use LLM if available
        if self.llm_connector.is_provider_available(self.llm_provider):
            generated_files = self._generate_rules_with_llm()
        
        if not generated_files:
            # Fallback to template-based generation
            generated_files = self._generate_template_rules()
        
        # Archive current rules before replacing them
        self._archive_current_rules()
        
        # Save version history for each generated file
        now = datetime.now().isoformat()
        for rule_path in generated_files:
            if os.path.exists(rule_path):
                try:
                    self.version_manager.create_version(
                        file_path=rule_path,
                        description=f"Generated based on project state at {now}",
                        tags=["auto-generated"]
                    )
                except Exception as e:
                    logger.warning(f"Failed to version rule file {rule_path}: {e}")
        
        return generated_files
    
    def _archive_current_rules(self) -> None:
        """Archive the current rules to the history directory."""
        # Create a timestamp for the archive directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = os.path.join(self.history_dir, f"rules_{timestamp}")
        os.makedirs(archive_dir, exist_ok=True)
        
        # Copy all .mdc files to the archive directory
        for file_name in os.listdir(self.rules_dir):
            if file_name.endswith('.mdc'):
                src_path = os.path.join(self.rules_dir, file_name)
                dst_path = os.path.join(archive_dir, file_name)
                try:
                    if os.path.exists(src_path):
                        import shutil
                        shutil.copy2(src_path, dst_path)
                except Exception as e:
                    logger.warning(f"Failed to archive rule file {file_name}: {e}")
    
    def _generate_rules_with_llm(self) -> List[str]:
        """
        Generate dynamic rules using LLM.
        
        Returns:
            List of paths to the generated rule files
        """
        try:
            # Prepare project info for the LLM
            project_info = {
                "name": self.project_state.name,
                "description": self.project_state.description,
                "phase": self.project_state.phase.value,
                "active_features": self.project_state.active_features,
                "current_focus": self.project_state.get_current_focus(),
                "tech_stack": self.project_state.tech_stack,
                "directory_structure": self.project_state.directory_structure,
                "components": {
                    name: {
                        "name": comp.name,
                        "path_pattern": comp.path_pattern,
                        "status": comp.status.value,
                        "description": comp.description
                    }
                    for name, comp in self.project_state.components.items()
                }
            }
            
            # Create system message for the LLM
            system_message = """
            You are an expert at creating dynamically adaptive rules for Cursor IDE. These files provide guidance 
            to AI assistants when users are working on a project.
            
            Create multiple specialized rule files that follow proper .mdc format structure, adapting to the current
            project phase and development focus. Each rule file should include:
            
            1. A title that describes the rule category (clear and specific)
            2. A pattern glob that specifies which files the rule applies to (be precise with file patterns)
            3. A description that explains when the rule should be applied (include rationale and current focus)
            4. The main rule content in markdown format (without prefixing every line with #)
            5. File references using @file: syntax to provide concrete examples
            
            Core best practices to follow:
            - Make each rule atomic (focused on a single concern)
            - Provide concrete examples of both good and bad patterns
            - Use hierarchical organization with clear section headers 
            - Make rules actionable rather than theoretical
            - Include context about why the rule exists, not just what it is
            - Balance detail (enough guidance without being overwhelming)
            - Use project-specific terminology and conventions
            
            Create separate rule files relevant to the current project phase:
            
            For SETUP/FOUNDATION phase:
            - Project Philosophy & Coding Standards (all files)
            - Architecture Guidelines (critical for early development)
            - Directory Structure & File Organization
            
            For FEATURE_DEVELOPMENT phase:
            - Component Implementation Guidelines
            - Feature-specific rules for active features
            - Testing Requirements for new features
            
            For REFINEMENT/MAINTENANCE phase:
            - Performance Optimization Guidelines
            - Refactoring & Code Quality Rules
            - Documentation Requirements
            
            IMPORTANT: Adapt your response to focus heavily on the current project phase and active features.
            For early phases, emphasize architecture and patterns. For later phases, focus on consistency and quality.
            
            Format your response as a JSON array where each object has these fields:
            - title: The rule title (clear and descriptive, reflecting current focus)
            - pattern: Glob pattern for file matching (be specific with extensions and paths)
            - description: When to apply this rule (include the rationale and current project context)
            - content: The main markdown content (including good and bad examples where appropriate)
            - references: Array of example files to reference
            
            Example response format:
            [
              {
                "title": "Project Philosophy & Approach",
                "pattern": "**/*",
                "description": "Core principles for the project currently in {current_phase} phase",
                "content": "## Project Focus\\n\\nCurrently prioritizing: {current_focus}\\n\\n## Design Principles\\n\\n- Principle 1\\n- Principle 2",
                "references": []
              },
              {
                "title": "Feature-Specific Guidelines: User Authentication",
                "pattern": "src/auth/**/*.{ts,tsx}",
                "description": "Rules specific to the auth feature currently in active development",
                "content": "## Auth Implementation Guidelines\\n\\n- Guideline 1\\n- Guideline 2\\n\\n### Good Example:\\n```tsx\\n// Example code\\n```",
                "references": ["src/auth/auth.service.ts"]
              }
            ]
            """
            
            # Create the prompt
            prompt = f"""
            Generate dynamic Cursor rules adapted to the current project state:
            
            Project Name: {project_info['name']}
            Description: {project_info['description']}
            Current Phase: {project_info['phase']}
            Current Focus: {project_info['current_focus']}
            
            Active Features: {', '.join(project_info['active_features']) if project_info['active_features'] else 'None specified'}
            
            Tech Stack:
            {json.dumps(project_info['tech_stack'], indent=2)}
            
            Directory Structure:
            {json.dumps(project_info['directory_structure'], indent=2)}
            
            Components:
            {json.dumps(project_info['components'], indent=2)}
            
            Create cursor rules that are specifically adapted to this project's current phase
            and development focus. The rules should provide concrete guidance for AI assistants
            helping with this specific project state.
            """
            
            # Send the request to the LLM
            request = LLMRequest(
                prompt=prompt,
                system_message=system_message,
                provider=self.llm_provider,
                temperature=0.2,
                max_tokens=4000
            )
            
            response = self.llm_connector.request(request)
            rules_content = response.text.strip()
            
            # Extract and parse the JSON
            import re
            json_match = re.search(r'\[\s*\{.+\}\s*\]', rules_content, re.DOTALL)
            
            generated_files = []
            
            if json_match:
                rules_json = json_match.group(0)
                try:
                    rules_data = json.loads(rules_json)
                    
                    # Save each rule file
                    for rule in rules_data:
                        title = rule.get("title", "Unnamed Rule")
                        pattern = rule.get("pattern", "**/*")
                        description = rule.get("description", "")
                        content = rule.get("content", "")
                        references = rule.get("references", [])
                        
                        # Save the rule
                        rule_path = save_modern_cursor_rules(
                            self.rules_dir,
                            title,
                            pattern,
                            description,
                            content,
                            references
                        )
                        
                        generated_files.append(rule_path)
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse rules JSON: {e}")
            
            # If JSON parsing fails, try to extract sections manually
            if not generated_files:
                rule_sections = re.split(r'# ([^\n]+)', rules_content)
                if len(rule_sections) > 1:
                    for i in range(1, len(rule_sections), 2):
                        if i + 1 < len(rule_sections):
                            title = rule_sections[i].strip()
                            content = rule_sections[i + 1].strip()
                            
                            # Try to extract pattern and description
                            pattern_match = re.search(r'pattern:\s*"([^"]+)"', content)
                            pattern = pattern_match.group(1) if pattern_match else "**/*"
                            
                            desc_match = re.search(r'description:\s*"([^"]+)"', content)
                            description = desc_match.group(1) if desc_match else ""
                            
                            # Clean up content
                            clean_content = re.sub(r'pattern:\s*"[^"]+"\n', '', content)
                            clean_content = re.sub(r'description:\s*"[^"]+"\n', '', clean_content)
                            
                            # Extract references
                            references = []
                            for line in clean_content.split('\n'):
                                if line.startswith('@file:'):
                                    ref = line.replace('@file:', '').strip()
                                    references.append(ref)
                                    clean_content = clean_content.replace(line, '')
                            
                            # Save the rule
                            rule_path = save_modern_cursor_rules(
                                self.rules_dir,
                                title,
                                pattern,
                                description,
                                clean_content.strip(),
                                references
                            )
                            
                            generated_files.append(rule_path)
            
            return generated_files
            
        except Exception as e:
            logger.warning(f"Failed to generate rules with LLM: {e}")
            return []
    
    def _generate_template_rules(self) -> List[str]:
        """
        Generate template-based rules based on project state.
        
        Returns:
            List of paths to the generated rule files
        """
        generated_files = []
        
        try:
            # Get current phase and focus
            phase = self.project_state.phase.value
            current_focus = self.project_state.get_current_focus()
            
            # Generate phase-specific rule
            phase_title = f"Project Phase: {phase.title()}"
            phase_desc = f"Guidelines for the {phase} phase of development"
            phase_content = f"""## Current Focus

{current_focus}

## Phase Guidelines

"""
            if phase == ProjectPhase.SETUP.value:
                phase_content += """- Focus on establishing project structure and architecture
- Document design decisions as they are made
- Create clear interfaces between components
- Prioritize flexibility over optimization at this early stage"""
            elif phase == ProjectPhase.FOUNDATION.value:
                phase_content += """- Implement core functionality following established patterns
- Write comprehensive tests for foundational components
- Focus on API design and separation of concerns
- Document architectural decisions"""
            elif phase == ProjectPhase.FEATURE_DEVELOPMENT.value:
                phase_content += """- Build features according to established architecture
- Maintain consistent patterns across related components
- Focus on proper error handling and edge cases
- Ensure new features are well-tested"""
            elif phase == ProjectPhase.REFINEMENT.value:
                phase_content += """- Optimize performance in critical paths
- Refactor for improved readability and maintenance
- Address technical debt before it compounds
- Improve test coverage in complex areas"""
            else:
                phase_content += """- Focus on stability and reliability
- Make minimal changes to stable components
- Document thoroughly for future developers
- Ensure backward compatibility"""
            
            # Save the phase rule
            phase_path = save_modern_cursor_rules(
                self.rules_dir,
                phase_title,
                "**/*",
                phase_desc,
                phase_content
            )
            generated_files.append(phase_path)
            
            # Generate active component rules
            active_components = self.project_state.get_active_components()
            for component in active_components:
                comp_title = f"Component: {component.name}"
                comp_desc = f"Guidelines for the {component.name} component currently in {component.status.value} status"
                
                comp_content = f"""## Component Description

{component.description}

## Implementation Guidelines

- Follow established patterns for this component type
- Ensure proper error handling and validation
- Write unit tests for all functionality
- Document public APIs and complex logic"""
                
                # Save the component rule
                comp_path = save_modern_cursor_rules(
                    self.rules_dir,
                    comp_title,
                    component.path_pattern,
                    comp_desc,
                    comp_content
                )
                generated_files.append(comp_path)
            
            # Generate tech stack rules
            tech_stack = self.project_state.tech_stack
            
            for category, techs in tech_stack.items():
                if not techs:
                    continue
                    
                tech_title = f"{category.title()} Guidelines"
                tech_desc = f"Best practices for {category} development"
                
                tech_content = f"""## {category.title()} Technologies

Currently using: {', '.join(techs)}

## Best Practices

"""
                
                if category.lower() == "frontend":
                    tech_content += """- Use functional components with hooks
- Follow component composition principles
- Implement responsive designs
- Ensure accessibility compliance"""
                elif category.lower() == "backend":
                    tech_content += """- Follow RESTful API design principles
- Implement proper error handling
- Use dependency injection where appropriate
- Document all API endpoints"""
                elif category.lower() == "database":
                    tech_content += """- Use parameterized queries to prevent SQL injection
- Implement proper database migration strategy
- Use transactions for multi-step operations
- Index frequently queried fields"""
                else:
                    tech_content += """- Follow industry best practices
- Maintain consistent patterns
- Document usage examples
- Write comprehensive tests"""
                
                # Save the tech stack rule
                tech_path = save_modern_cursor_rules(
                    self.rules_dir,
                    tech_title,
                    f"**/*.{{{','.join(self._get_extensions_for_category(category))}}}",
                    tech_desc,
                    tech_content
                )
                generated_files.append(tech_path)
            
            # Generate general project rule
            general_title = "Project Guidelines"
            general_desc = f"General guidelines for all files in {self.project_state.name}"
            
            general_content = f"""## Project Overview

{self.project_state.description}

## Current Focus

{current_focus}

## General Guidelines

- Follow consistent code style and formatting
- Document public APIs and complex logic
- Write tests for new functionality
- Use meaningful variable and function names
- Keep functions small and focused on a single task"""
            
            # Save the general rule
            general_path = save_modern_cursor_rules(
                self.rules_dir,
                general_title,
                "**/*",
                general_desc,
                general_content
            )
            generated_files.append(general_path)
            
            return generated_files
            
        except Exception as e:
            logger.warning(f"Failed to generate template rules: {e}")
            return []
    
    def _get_extensions_for_category(self, category: str) -> List[str]:
        """
        Get file extensions associated with a technology category.
        
        Args:
            category: The technology category
            
        Returns:
            List of file extensions
        """
        category = category.lower()
        
        if category == "frontend":
            return ["js", "jsx", "ts", "tsx", "css", "scss", "html", "vue", "svelte"]
        elif category == "backend":
            return ["js", "ts", "py", "java", "go", "rb", "php", "cs"]
        elif category == "database":
            return ["sql", "prisma", "schema"]
        elif category == "devops":
            return ["yaml", "yml", "tf", "Dockerfile", "docker-compose.yml"]
        else:
            return ["*"]
    
    def analyze_rules_effectiveness(self) -> Dict[str, Any]:
        """
        Analyze the effectiveness of current rules.
        
        Returns:
            Dictionary with analysis results
        """
        # This would ideally involve some heuristics or possibly LLM analysis
        # of how well the rules are being followed in the codebase
        # For now, we'll return a placeholder
        return {
            "num_rules": len([f for f in os.listdir(self.rules_dir) if f.endswith('.mdc')]),
            "last_updated": self.project_state.last_updated,
            "current_phase": self.project_state.phase.value,
            "current_focus": self.project_state.get_current_focus()
        } 