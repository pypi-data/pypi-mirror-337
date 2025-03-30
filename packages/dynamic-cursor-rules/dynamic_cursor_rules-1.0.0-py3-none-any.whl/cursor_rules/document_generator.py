"""
Document generator for Cursor Rules.

This module handles the generation of all required documents from an initialization file,
including the Product Requirements Document, Technical Stack Document, and others.
"""
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .task_parser import extract_metadata_from_markdown, parse_initialization_doc
from .task_tracker import ActionPlan
from .utils import generate_cursorrules_file, save_cursorrules_file
from .core import RuleSet, Rule

class DocumentGenerator:
    """Generator for creating all required documents from an initialization file."""
    
    def __init__(self, init_doc_path: str, output_dir: str = None):
        """
        Initialize the document generator.
        
        Args:
            init_doc_path: Path to the initialization document
            output_dir: Directory where generated documents will be saved
        """
        self.init_doc_path = init_doc_path
        self.output_dir = output_dir or os.path.dirname(os.path.abspath(init_doc_path))
        
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Read the initialization document
        with open(init_doc_path, 'r', encoding='utf-8') as f:
            self.init_content = f.read()
        
        # Extract metadata and action plan
        self.action_plan, self.metadata = parse_initialization_doc(self.init_doc_path)
        
        # Extract title and description
        title_match = re.search(r'^#\s+(.*?)$', self.init_content, re.MULTILINE)
        self.title = title_match.group(1).strip() if title_match else "Project Documentation"
        
        # Extract project description
        description_sections = re.findall(r'(?:^|\n)##\s+Project Overview\s*\n(.*?)(?=\n##|\Z)', 
                                          self.init_content, re.DOTALL)
        self.description = description_sections[0].strip() if description_sections else ""
    
    def generate_all_documents(self) -> Dict[str, str]:
        """
        Generate all required documents based on the initialization file.
        
        Returns:
            Dictionary mapping document names to file paths
        """
        generated_files = {}
        
        # Generate the PRD
        prd_path = self._generate_prd()
        generated_files["Product Requirements Document"] = prd_path
        
        # Generate the Technical Stack document
        tech_stack_path = self._generate_tech_stack_doc()
        generated_files["Technical Stack Document"] = tech_stack_path
        
        # Generate the .cursorrules file
        cursorrules_path = self._generate_cursorrules()
        generated_files[".cursorrules"] = cursorrules_path
        
        # Generate the Action Items document
        tasks_json_path, tasks_md_path = self._generate_action_items()
        generated_files["Action Items JSON"] = tasks_json_path
        generated_files["Action Items Markdown"] = tasks_md_path
        
        return generated_files
    
    def _generate_prd(self) -> str:
        """
        Generate the Product Requirements Document.
        
        Returns:
            Path to the generated PRD
        """
        # Extract relevant sections from the initialization document
        overview_section = self._extract_section("Project Overview")
        core_functionality = self._extract_section("Core Functionality")
        
        # Generate the PRD content
        prd_content = [
            f"# Product Requirements Document: {self.title}",
            "",
            "## 1. Product Vision",
            "",
            self.description,
            "",
            "## 2. Target Users",
            "",
        ]
        
        # Check if there's a user section
        users_section = self._extract_section("Target Users") or self._extract_section("User Experience")
        if users_section:
            prd_content.append(users_section)
        else:
            prd_content.append("- Software developers and teams working on this project")
            prd_content.append("- End users of the application")
        
        prd_content.extend([
            "",
            "## 3. User Stories",
            "",
        ])
        
        # Check if there's a user stories section
        stories_section = self._extract_section("User Stories") or self._extract_section("User Experience")
        if stories_section:
            prd_content.append(stories_section)
        else:
            prd_content.append("1. As a user, I want to be able to use the application effectively.")
        
        prd_content.extend([
            "",
            "## 4. Functional Requirements",
            "",
        ])
        
        # Add core functionality as functional requirements
        if core_functionality:
            prd_content.append(core_functionality)
        else:
            prd_content.append("- Basic application functionality")
        
        prd_content.extend([
            "",
            "## 5. Non-Functional Requirements",
            "",
            "1. Performance",
            "   - The application should respond quickly to user interactions",
            "",
            "2. Security",
            "   - User data should be properly secured",
            "",
            "3. Usability",
            "   - The application should be intuitive and easy to use",
            "",
            "## 6. Acceptance Criteria",
            "",
            "1. The application meets all functional requirements",
            "2. The application is properly tested",
            "3. The application is documented",
            "4. The application is deployed and accessible to users"
        ])
        
        # Write the PRD to a file
        prd_path = os.path.join(self.output_dir, "product_requirements.md")
        with open(prd_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(prd_content))
        
        return prd_path
    
    def _generate_tech_stack_doc(self) -> str:
        """
        Generate the Technical Stack Document.
        
        Returns:
            Path to the generated Technical Stack Document
        """
        # Extract relevant sections
        tech_requirements = self._extract_section("Technical Requirements")
        architecture = self._extract_section("Architecture")
        
        # Generate the Technical Stack content
        tech_content = [
            f"# {self.title} Technical Stack",
            "",
            "## Technology Overview",
            "",
            f"{self.title} is built using modern technologies to ensure reliability, maintainability, and performance.",
            "",
        ]
        
        # Add technical requirements
        tech_content.extend([
            "## Backend Technologies",
            "",
        ])
        
        if tech_requirements:
            tech_content.append(tech_requirements)
        else:
            tech_content.extend([
                "### Programming Language",
                "",
                "- Python 3.9+: Primary development language",
                "",
                "### Key Libraries",
                "",
                "- Standard libraries as required by the project",
            ])
        
        # Add architecture information
        tech_content.extend([
            "",
            "## Architecture Design",
            "",
        ])
        
        if architecture:
            tech_content.append(architecture)
        else:
            tech_content.extend([
                "The system follows a modular architecture designed for maintainability and scalability.",
            ])
        
        # Add dependency management and setup information
        tech_content.extend([
            "",
            "## Dependency Management",
            "",
            "The project uses standard dependency management tools appropriate for the chosen technology stack.",
            "",
            "## Development Environment Setup",
            "",
            "To set up the development environment for this project, follow these steps:",
            "",
            "1. Clone the repository",
            "2. Install required dependencies",
            "3. Configure the environment",
            "4. Run the application locally for testing",
        ])
        
        # Write the Technical Stack document to a file
        tech_stack_path = os.path.join(self.output_dir, "technical_stack.md")
        with open(tech_stack_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(tech_content))
        
        return tech_stack_path
    
    def _generate_cursorrules(self) -> str:
        """
        Generate the .cursorrules file.
        
        Returns:
            Path to the generated .cursorrules file
        """
        # Create cursor directory if it doesn't exist
        cursor_dir = os.path.join(self.output_dir, ".cursor")
        os.makedirs(cursor_dir, exist_ok=True)
        
        # Extract rules from the initialization document
        rules_section = self._extract_section("Core Functionality")
        
        # Create a RuleSet
        ruleset = RuleSet(name=self.title, description=self.description)
        
        # Add rules based on sections in the initialization document
        # Extract coding standards, best practices, etc.
        for section_name in ["Coding Standards", "Best Practices", "Architecture", "Technical Requirements"]:
            section = self._extract_section(section_name)
            if section:
                # Split by lines and extract bullet points as rules
                lines = section.split("\n")
                for line in lines:
                    if line.strip().startswith(("-", "*", "•")):
                        rule_content = line.strip()[1:].strip()
                        if rule_content:
                            ruleset.add_rule(rule_content, tags=[section_name.lower()])
        
        # If no rules were extracted, add some default rules
        if not ruleset.rules:
            ruleset.add_rule("Use consistent code formatting", tags=["style"])
            ruleset.add_rule("Write clear and concise comments", tags=["documentation"])
            ruleset.add_rule("Follow best practices for the technology stack", tags=["best_practices"])
            ruleset.add_rule("Write testable code", tags=["testing"])
        
        # Prepare project info
        project_info = {
            "name": self.title,
            "description": self.description,
            "tech_stack": self._extract_tech_stack(),
            "naming_conventions": {
                "files": "Use descriptive names with appropriate extensions",
                "variables": "Use camelCase for variables, PascalCase for classes",
                "functions": "Use descriptive verb-noun combinations"
            },
            "directory_structure": self._extract_directory_structure()
        }
        
        # Generate and save the .cursorrules file
        cursorrules_path = os.path.join(cursor_dir, "cursor_rules.mdc")
        save_cursorrules_file(ruleset, cursorrules_path, project_info)
        
        return cursorrules_path
    
    def _generate_action_items(self) -> Tuple[str, str]:
        """
        Generate the Action Items documents (JSON and Markdown).
        
        Returns:
            Tuple containing paths to the JSON and Markdown task files
        """
        # Save the action plan as JSON
        tasks_json_path = os.path.join(self.output_dir, "cursor-rules-tasks.json")
        self.action_plan.save_to_file(tasks_json_path)
        
        # Save the action plan as Markdown
        tasks_md_path = os.path.join(self.output_dir, "cursor-rules-tasks.md")
        self._save_action_plan_as_markdown(tasks_md_path)
        
        return tasks_json_path, tasks_md_path
    
    def _save_action_plan_as_markdown(self, path: str) -> None:
        """
        Save the action plan as a Markdown file.
        
        Args:
            path: Path where to save the Markdown file
        """
        md_content = ["# Project Action Items", ""]
        
        for phase in self.action_plan.phases:
            md_content.append(f"## {phase.title}")
            md_content.append("")
            
            for task in phase.tasks:
                status_emoji = "✅" if task.status.name == "COMPLETED" else "⭕"
                priority = f"Priority: {task.priority}" if task.priority else ""
                effort = f"Effort: {task.effort}" if task.effort else ""
                tags = f"Tags: {', '.join(task.tags)}" if task.tags else ""
                
                details = ", ".join(filter(None, [priority, effort, tags]))
                task_line = f"- {status_emoji} **{task.title}** (ID: `{task.id}`"
                if details:
                    task_line += f", {details}"
                task_line += ")"
                
                md_content.append(task_line)
                
                # Add subtasks
                for subtask in task.subtasks:
                    sub_status_emoji = "✅" if subtask.status.name == "COMPLETED" else "⭕"
                    md_content.append(f"  - {sub_status_emoji} {subtask.title}")
            
            md_content.append("")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
    
    def _extract_section(self, section_name: str) -> str:
        """
        Extract a section from the initialization document.
        
        Args:
            section_name: Name of the section to extract
            
        Returns:
            Content of the section, or empty string if not found
        """
        pattern = rf'(?:^|\n)##\s+{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)'
        matches = re.findall(pattern, self.init_content, re.DOTALL)
        return matches[0].strip() if matches else ""
    
    def _extract_tech_stack(self) -> Dict[str, List[str]]:
        """
        Extract the tech stack from the initialization document.
        
        Returns:
            Dictionary mapping tech stack categories to lists of technologies
        """
        tech_stack = {}
        
        # Try to extract from Technical Requirements section
        tech_section = self._extract_section("Technical Requirements")
        if tech_section:
            # Look for language specifications
            backend_match = re.search(r'(?:Backend|Language).*?:\s*(.*?)(?:\n|$)', tech_section, re.IGNORECASE)
            if backend_match:
                tech_stack["backend"] = [tech.strip() for tech in backend_match.group(1).split(',')]
            
            # Look for libraries
            libraries_match = re.search(r'Key Libraries.*?:(.*?)(?=\n\w|\Z)', tech_section, re.DOTALL | re.IGNORECASE)
            if libraries_match:
                libs = []
                for line in libraries_match.group(1).split('\n'):
                    if line.strip().startswith(('-', '*', '•')):
                        lib = line.strip()[1:].strip()
                        if "`" in lib:
                            lib = re.search(r'`(.*?)`', lib).group(1)
                        libs.append(lib)
                if libs:
                    tech_stack["libraries"] = libs
        
        # Default tech stack if nothing was found
        if not tech_stack:
            tech_stack = {
                "backend": ["Python 3.9+"],
                "libraries": ["Standard libraries"]
            }
        
        return tech_stack
    
    def _extract_directory_structure(self) -> Dict[str, str]:
        """
        Extract the directory structure from the initialization document.
        
        Returns:
            Dictionary mapping directory names to descriptions
        """
        directory_structure = {}
        
        # Try to extract from document
        structure_section = self._extract_section("Directory Structure") or self._extract_section("Architecture")
        if structure_section:
            for line in structure_section.split('\n'):
                if line.strip().startswith(('-', '*', '•')):
                    parts = line.strip()[1:].strip().split(':', 1)
                    if len(parts) == 2:
                        dir_name = parts[0].strip()
                        description = parts[1].strip()
                        directory_structure[dir_name] = description
        
        # Default structure if nothing was found
        if not directory_structure:
            directory_structure = {
                "src/": "Source code",
                "docs/": "Documentation",
                "tests/": "Tests"
            }
        
        return directory_structure 