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
from .llm_connector import LLMProvider, LLMConnector, LLMRequest

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
        self.llm_provider = LLMProvider.OPENAI  # Default provider
        self.llm_connector = LLMConnector()
        
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
    
    def set_llm_provider(self, provider: LLMProvider) -> None:
        """
        Set the LLM provider to use for document generation.
        
        Args:
            provider: The LLM provider to use
        """
        if not self.llm_connector.is_provider_available(provider):
            available = self.llm_connector.list_available_providers()
            available_str = ", ".join([p.value for p in available]) if available else "none"
            raise ValueError(f"Provider {provider.value} is not available. Available providers: {available_str}")
        
        self.llm_provider = provider
    
    def generate_all_documents(self) -> Dict[str, str]:
        """
        Generate all required documents based on the initialization file.
        
        Returns:
            Dictionary mapping document names to file paths
        """
        generated_files = {}
        
        # Get current working directory (project root)
        project_root = os.getcwd()
        
        # Create documentation directory at project root
        docs_dir = os.path.join(project_root, "documentation")
        os.makedirs(docs_dir, exist_ok=True)
        
        # Create .cursor directory at project root
        cursor_dir = os.path.join(project_root, ".cursor")
        os.makedirs(cursor_dir, exist_ok=True)
        
        # Setup LLM connector if API key is available
        try:
            available_providers = self.llm_connector.list_available_providers()
            if available_providers:
                self.llm_provider = available_providers[0]
                print(f"Using {self.llm_provider.value} for document generation")
            else:
                print("No LLM providers available - using template-based generation")
        except Exception as e:
            print(f"Warning: Failed to set up LLM provider: {e}")
        
        # Generate the PRD with LLM enhancement
        prd_path = self._generate_prd(docs_dir)
        generated_files["Product Requirements Document"] = prd_path
        
        # Generate the Technical Stack document with LLM enhancement
        tech_stack_path = self._generate_tech_stack_doc(docs_dir)
        generated_files["Technical Stack Document"] = tech_stack_path
        
        # Generate the .cursorrules file with LLM enhancement
        cursorrules_path = self._generate_cursorrules(cursor_dir)
        generated_files[".cursorrules"] = cursorrules_path
        
        # Generate the Action Items document
        tasks_json_path, tasks_md_path = self._generate_action_items(docs_dir)
        generated_files["Action Items JSON"] = tasks_json_path
        generated_files["Action Items Markdown"] = tasks_md_path
        
        # Determine which optional documents to generate based on content analysis
        optional_docs = self._determine_optional_documents()
        
        # Generate any optional documents
        for doc_type in optional_docs:
            if doc_type == "app_flow":
                doc_path = self._generate_app_flow_doc(docs_dir)
                generated_files["App Flow Document"] = doc_path
            elif doc_type == "frontend_guidelines":
                doc_path = self._generate_frontend_guidelines(docs_dir)
                generated_files["Frontend Guidelines"] = doc_path
            elif doc_type == "backend_structure":
                doc_path = self._generate_backend_structure(docs_dir)
                generated_files["Backend Structure Document"] = doc_path
            elif doc_type == "api_documentation":
                doc_path = self._generate_api_documentation(docs_dir)
                generated_files["API Documentation"] = doc_path
            elif doc_type == "testing_guidelines":
                doc_path = self._generate_testing_guidelines(docs_dir)
                generated_files["Testing Guidelines"] = doc_path
        
        return generated_files
    
    def _generate_prd(self, output_dir: str = None) -> str:
        """
        Generate the Product Requirements Document using LLM if available.
        
        Args:
            output_dir: Directory where to save the PRD
            
        Returns:
            Path to the generated PRD
        """
        # Use provided output directory or default
        output_dir = output_dir or self.output_dir
        
        # Check if an LLM provider is available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            # Use LLM to generate the PRD
            try:
                # Create a request to generate a comprehensive PRD from the initialization doc
                system_message = """
                You are an expert at creating Product Requirements Documents (PRDs) for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive PRD with the following sections:
                1. Product Vision - What problem does this solve and for whom?
                2. Target Users - Who will use this product?
                3. User Stories - What will users be able to do with the product?
                4. Functional Requirements - What features and functionality should the product include?
                5. Non-Functional Requirements - Performance, security, usability, etc.
                6. Acceptance Criteria - How will we know the product meets the requirements?
                
                The output should be a well-formatted markdown document with thoughtful, detailed content derived from the initialization document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive PRD:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,  # More deterministic for documentation
                    max_tokens=4000   # Allow for detailed output
                )
                
                response = self.llm_connector.request(request)
                prd_content = response.text.strip()
                
                # Write the PRD to a file
                prd_path = os.path.join(output_dir, "product_requirements.md")
                with open(prd_path, 'w', encoding='utf-8') as f:
                    f.write(prd_content)
                
                return prd_path
                
            except Exception as e:
                # Log the error and fall back to template-based generation
                print(f"Warning: Failed to generate PRD with LLM: {e}")
        
        # Fallback: Generate a template-based PRD
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
        prd_path = os.path.join(output_dir, "product_requirements.md")
        with open(prd_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(prd_content))
        
        return prd_path
    
    def _generate_tech_stack_doc(self, output_dir: str = None) -> str:
        """
        Generate the Technical Stack Document using LLM if available.
        
        Args:
            output_dir: Directory where to save the Technical Stack Document
            
        Returns:
            Path to the generated Technical Stack Document
        """
        # Use provided output directory or default
        output_dir = output_dir or self.output_dir
        
        # Check if an LLM provider is available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            # Use LLM to generate the Technical Stack Document
            try:
                # Create a request to generate a comprehensive tech stack doc
                system_message = """
                You are an expert at creating Technical Stack Documentation for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive technical stack document with the following sections:
                1. Technology Overview - What technologies will be used in the project?
                2. Backend Technologies - Programming languages, frameworks, libraries, etc.
                3. Frontend Technologies (if applicable) - Frameworks, libraries, etc.
                4. Architecture Design - System design, patterns, and principles
                5. Dependency Management - How dependencies will be managed
                6. Development Environment Setup - Steps to set up the development environment
                
                The output should be a well-formatted markdown document with specific, technical details derived from the initialization document.
                Focus on the "Technical Requirements" and "Architecture" sections of the initialization document if they exist.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive technical stack document:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                tech_content = response.text.strip()
                
                # Write the Technical Stack document to a file
                tech_stack_path = os.path.join(output_dir, "technical_stack.md")
                with open(tech_stack_path, 'w', encoding='utf-8') as f:
                    f.write(tech_content)
                
                return tech_stack_path
                
            except Exception as e:
                # Log the error and fall back to template-based generation
                print(f"Warning: Failed to generate Technical Stack Document with LLM: {e}")
        
        # Fallback: Generate a template-based Technical Stack Document
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
        tech_stack_path = os.path.join(output_dir, "technical_stack.md")
        with open(tech_stack_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(tech_content))
        
        return tech_stack_path
    
    def _generate_cursorrules(self, cursor_dir: str) -> str:
        """
        Generate the .cursorrules file using LLM if available.
        
        Args:
            cursor_dir: Directory where to save the .cursorrules file
            
        Returns:
            Path to the generated .cursorrules file
        """
        # Create a RuleSet
        ruleset = RuleSet(name=self.title, description=self.description)
        
        # First, extract rules based on the initialization document sections
        for section_name in ["Coding Standards", "Best Practices", "Architecture", "Technical Requirements", "Core Functionality"]:
            section = self._extract_section(section_name)
            if section:
                # Split by lines and extract bullet points as rules
                lines = section.split("\n")
                for line in lines:
                    if line.strip().startswith(("-", "*", "•")):
                        rule_content = line.strip()[1:].strip()
                        if rule_content:
                            ruleset.add_rule(rule_content, tags=[section_name.lower()])
        
        # If very few rules were extracted, add some default ones
        if len(ruleset.rules) < 3:
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
        
        # Check if an LLM provider is available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        cursorrules_path = os.path.join(cursor_dir, "cursor_rules.mdc")
        
        if use_llm:
            try:
                # Create a request to generate a comprehensive cursor rules file
                system_message = """
                You are an expert at creating .cursorrules files for Cursor IDE. These files provide guidance 
                to AI assistants when users are working on a project. Your task is to analyze the provided 
                initialization document and create a comprehensive .cursorrules file with the following structure:
                
                # .cursorrules for [Project Name]
                
                # Overview:
                # [Project description]
                
                # Tech Stack:
                # [Technology details]
                
                # Naming Conventions:
                # [Naming conventions]
                
                # Directory Structure:
                # [Directory structure]
                
                # Rules:
                ## [Category] Rules:
                # [Rule 1]
                # [Rule 2]
                # ...
                
                Extract detailed rules from the initialization document, focusing on coding standards, best practices,
                technical requirements, and project-specific guidelines. Create rules that will be helpful for an AI assistant
                to understand how to help with this specific project.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive .cursorrules file:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                cursorrules_content = response.text.strip()
                
                # Write the .cursorrules file
                with open(cursorrules_path, 'w', encoding='utf-8') as f:
                    f.write(cursorrules_content)
                    
                return cursorrules_path
                
            except Exception as e:
                # Log the error and fall back to template-based generation
                print(f"Warning: Failed to generate .cursorrules with LLM: {e}")
        
        # Fallback: Use the utility function to generate the file
        try:
            # Get API key for the selected provider if available
            if use_llm:
                api_key = self.llm_connector.get_api_key(self.llm_provider)
                save_cursorrules_file(ruleset, cursorrules_path, project_info, 
                                     self.llm_provider.value, api_key)
            else:
                save_cursorrules_file(ruleset, cursorrules_path, project_info)
        except Exception as e:
            # Log the error but still generate the file with default behavior
            print(f"Warning: Could not use provider: {e}")
            save_cursorrules_file(ruleset, cursorrules_path, project_info)
        
        return cursorrules_path
    
    def _generate_action_items(self, output_dir: str = None) -> Tuple[str, str]:
        """
        Generate the Action Items documents (JSON and Markdown) using LLM if available.
        
        Args:
            output_dir: Directory where to save the Action Items documents
            
        Returns:
            Tuple containing paths to the JSON and Markdown task files
        """
        # Use provided output directory or default
        output_dir = output_dir or self.output_dir
        
        # Check if an LLM provider is available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            # Try to generate action items using LLM
            try:
                action_plan = self._generate_action_items_with_llm()
            except Exception as e:
                print(f"Warning: Failed to generate action items with LLM: {e}")
                # Fallback to regex-based extraction
                action_plan = self.action_plan
        else:
            # Use regex-based extraction
            action_plan = self.action_plan
        
        # Save the action plan as JSON
        tasks_json_path = os.path.join(output_dir, "cursor-rules-tasks.json")
        action_plan.save_to_file(tasks_json_path)
        
        # Save the action plan as Markdown
        tasks_md_path = os.path.join(output_dir, "cursor-rules-tasks.md")
        self._save_action_plan_as_markdown(tasks_md_path, action_plan)
        
        return tasks_json_path, tasks_md_path
    
    def _generate_action_items_with_llm(self) -> ActionPlan:
        """
        Generate action items using LLM.
        
        Returns:
            An ActionPlan object with tasks organized into phases
        """
        system_message = """
        You are an expert project planner. Based on the provided software project initialization document, 
        create a comprehensive action plan with tasks and subtasks. The action plan should be organized into phases 
        and include specific, actionable tasks that would be required to implement the project.
        
        Structure your response as a JSON object with the following format:
        
        [
          {
            "id": "phase-1",
            "title": "Phase 1",
            "description": "Core Functionality",
            "tasks": [
              {
                "id": "p1t1",
                "title": "Task title 1",
                "description": "Task description",
                "status": "not_started",
                "priority": 2,
                "effort": 3,
                "subtasks": [
                  {
                    "id": "p1t1s1",
                    "title": "Subtask title 1",
                    "status": "not_started"
                  }
                ]
              }
            ]
          }
        ]
        
        Guidelines:
        1. Organize tasks into 2-4 logical phases (e.g., "Setup", "Core Development", "Advanced Features")
        2. For each task, include a descriptive title and optional description
        3. Set appropriate priority (1=low, 2=medium, 3=high) and effort (1=small, 2=medium, 3=large)
        4. Create task IDs that reflect the phase (e.g., "p1t1" for Phase 1, Task 1)
        5. Include subtasks where appropriate
        6. Ensure all tasks start with status "not_started"
        7. Be specific and concrete - tasks should be actionable and clear
        8. Consider all aspects of the project, including development, testing, documentation, and deployment
        
        Provide ONLY valid JSON without any explanatory text. The JSON should be valid and ready to be parsed.
        """
        
        # Format the prompt to include the initialization document
        prompt = f"""
        Below is the initialization document for a software project. Please analyze it and create a comprehensive action plan:
        
        {self.init_content}
        """
        
        request = LLMRequest(
            prompt=prompt,
            system_message=system_message,
            provider=self.llm_provider,
            temperature=0.3,
            max_tokens=4000
        )
        
        response = self.llm_connector.request(request)
        json_content = response.text.strip()
        
        # Ensure we're working with valid JSON
        import json
        from .task_tracker import ActionPlan, Phase, Task, TaskStatus
        
        try:
            # Extract the JSON array if it's embedded in other text
            start_idx = json_content.find('[')
            end_idx = json_content.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_content = json_content[start_idx:end_idx]
            
            # Parse the JSON content
            phases_data = json.loads(json_content)
            
            # Create the action plan
            action_plan = ActionPlan(title="Project Action Plan")
            
            # Process each phase
            for phase_data in phases_data:
                phase = Phase(
                    title=phase_data.get("title", "Unnamed Phase"),
                    description=phase_data.get("description", "")
                )
                
                # Process each task in the phase
                for task_data in phase_data.get("tasks", []):
                    # Create the task
                    task = Task(
                        title=task_data.get("title", "Unnamed Task"),
                        description=task_data.get("description", ""),
                        task_id=task_data.get("id"),
                        priority=task_data.get("priority", 0),
                        effort=task_data.get("effort", 0)
                    )
                    
                    # Set the status if specified
                    status_str = task_data.get("status", "not_started").upper()
                    if hasattr(TaskStatus, status_str):
                        task.status = getattr(TaskStatus, status_str)
                    
                    # Process subtasks if any
                    for subtask_data in task_data.get("subtasks", []):
                        subtask = Task(
                            title=subtask_data.get("title", "Unnamed Subtask"),
                            description=subtask_data.get("description", ""),
                            task_id=subtask_data.get("id")
                        )
                        
                        # Set the subtask status if specified
                        subtask_status_str = subtask_data.get("status", "not_started").upper()
                        if hasattr(TaskStatus, subtask_status_str):
                            subtask.status = getattr(TaskStatus, subtask_status_str)
                        
                        task.add_subtask(subtask)
                    
                    # Add the task to the phase
                    phase.add_task(task)
                
                # Add the phase to the action plan
                action_plan.add_phase(phase)
            
            return action_plan
        
        except Exception as e:
            print(f"Warning: Failed to parse LLM task output: {e}")
            print(f"Raw output: {json_content}")
            # Return the fallback action plan based on regex extraction
            return self.action_plan
    
    def _save_action_plan_as_markdown(self, path: str, action_plan: ActionPlan) -> None:
        """
        Save the action plan as a Markdown file.
        
        Args:
            path: Path where to save the Markdown file
            action_plan: The action plan to save
        """
        md_content = ["# Project Action Items", ""]
        
        for phase in action_plan.phases:
            md_content.append(f"## {phase.title}")
            if phase.description:
                md_content.append(f"{phase.description}")
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
                
                # Add task description if available
                if task.description:
                    md_content.append(f"  - *{task.description}*")
                
                # Add subtasks
                for subtask in task.subtasks:
                    sub_status_emoji = "✅" if subtask.status.name == "COMPLETED" else "⭕"
                    md_content.append(f"  - {sub_status_emoji} {subtask.title}")
                    
                    # Add subtask description if available
                    if subtask.description:
                        md_content.append(f"    - *{subtask.description}*")
        
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
    
    def _determine_optional_documents(self) -> List[str]:
        """
        Analyze the initialization document to determine which optional documents to generate.
        
        Returns:
            List of document types to generate
        """
        optional_docs = []
        
        # Check for frontend-related terms
        frontend_indicators = ["frontend", "UI", "user interface", "react", "vue", "angular", "css", "html", "javascript", "typescript"]
        if any(indicator.lower() in self.init_content.lower() for indicator in frontend_indicators):
            optional_docs.append("frontend_guidelines")
            
            # If there's significant UI emphasis, generate app flow
            ui_indicators = ["user flow", "app flow", "interface", "interaction", "user experience", "UX"]
            if sum(self.init_content.lower().count(indicator.lower()) for indicator in ui_indicators) >= 2:
                optional_docs.append("app_flow")
        
        # Check for backend-related terms
        backend_indicators = ["backend", "server", "database", "api", "microservice", "service", "architecture"]
        if any(indicator.lower() in self.init_content.lower() for indicator in backend_indicators):
            optional_docs.append("backend_structure")
            
            # If there's API emphasis, generate API docs
            api_indicators = ["api", "rest", "graphql", "endpoint", "http", "request", "response"]
            if sum(self.init_content.lower().count(indicator.lower()) for indicator in api_indicators) >= 2:
                optional_docs.append("api_documentation")
        
        # Check for testing emphasis
        test_indicators = ["test", "quality assurance", "qa", "unit test", "integration test", "e2e", "end-to-end"]
        if sum(self.init_content.lower().count(indicator.lower()) for indicator in test_indicators) >= 2:
            optional_docs.append("testing_guidelines")
        
        # If using LLM, we can also directly ask it what documents are needed
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        if use_llm:
            try:
                system_message = """
                You are an expert project analyzer. Based on the provided initialization document,
                determine which of the following optional documents should be created:
                - App Flow Document (for detailed UI flow and interactions)
                - Frontend Guidelines (for frontend developers)
                - Backend Structure Document (for backend architecture)
                - API Documentation (for API endpoints and usage)
                - Testing Guidelines (for QA and testing procedures)
                
                Respond with only a JSON array of document types to generate, using the following format:
                ["app_flow", "frontend_guidelines", "backend_structure", "api_documentation", "testing_guidelines"]
                Include only those that are relevant based on the project description.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and determine which optional documents should be created:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.1,
                    max_tokens=500
                )
                
                response = self.llm_connector.request(request)
                llm_suggestions = response.text.strip()
                
                # Try to parse as JSON
                import json
                try:
                    # Extract the JSON array if it's embedded in other text
                    start_idx = llm_suggestions.find('[')
                    end_idx = llm_suggestions.rfind(']') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        llm_docs = json.loads(llm_suggestions[start_idx:end_idx])
                        
                        # Add any suggestions not already in our list
                        for doc in llm_docs:
                            if doc not in optional_docs:
                                optional_docs.append(doc)
                except Exception as e:
                    print(f"Warning: Failed to parse LLM document suggestions: {e}")
                
            except Exception as e:
                print(f"Warning: Failed to get document suggestions from LLM: {e}")
        
        print(f"Generating {len(optional_docs)} optional documents: {', '.join(optional_docs)}")
        return optional_docs
    
    def _generate_app_flow_doc(self, output_dir: str) -> str:
        """
        Generate the App Flow Document using LLM if available.
        
        Args:
            output_dir: Directory where to save the document
            
        Returns:
            Path to the generated document
        """
        # Use LLM if available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = """
                You are an expert at creating App Flow documents for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive 
                App Flow document that describes the user interactions and UI flows for the application.
                Include the following sections:
                1. Overview - What are the main user flows in the application?
                2. User Journeys - Step-by-step flows for key user activities
                3. Screen Transitions - How screens connect and relate to each other
                4. Key Interactions - Important interactive elements and behaviors
                
                The output should be a well-formatted markdown document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive App Flow document:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "app_flow.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
                
            except Exception as e:
                print(f"Warning: Failed to generate App Flow document with LLM: {e}")
        
        # Fallback to template
        content = [
            f"# {self.title} App Flow",
            "",
            "## Overview",
            "",
            "This document outlines the main user flows in the application.",
            "",
            "## User Journeys",
            "",
            "1. User Registration/Login",
            "2. Main Application Flow",
            "3. Settings and Configuration",
            "",
            "## Screen Transitions",
            "",
            "* Login → Home Dashboard → Feature Screens",
            "",
            "## Key Interactions",
            "",
            "* User input validation",
            "* Data submission",
            "* Navigation patterns"
        ]
        
        file_path = os.path.join(output_dir, "app_flow.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return file_path
    
    def _generate_frontend_guidelines(self, output_dir: str) -> str:
        """
        Generate Frontend Guidelines document using LLM if available.
        
        Args:
            output_dir: Directory where to save the document
            
        Returns:
            Path to the generated document
        """
        # Use LLM if available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = """
                You are an expert at creating Frontend Guidelines documents for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive 
                Frontend Guidelines document with the following sections:
                1. Overview - What frontend technologies are used?
                2. Component Structure - How should components be organized?
                3. Styling Guidelines - CSS/styling best practices
                4. State Management - How to handle application state
                5. Best Practices - Performance, accessibility, etc.
                
                The output should be a well-formatted markdown document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create comprehensive Frontend Guidelines:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "frontend_guidelines.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
                
            except Exception as e:
                print(f"Warning: Failed to generate Frontend Guidelines with LLM: {e}")
        
        # Fallback to template
        content = [
            f"# {self.title} Frontend Guidelines",
            "",
            "## Overview",
            "",
            "This document outlines the frontend technologies and best practices for the project.",
            "",
            "## Component Structure",
            "",
            "* Organize components by feature",
            "* Use atomic design principles",
            "",
            "## Styling Guidelines",
            "",
            "* Use consistent naming conventions",
            "* Follow responsive design principles",
            "",
            "## State Management",
            "",
            "* Use appropriate state management patterns",
            "* Minimize prop drilling",
            "",
            "## Best Practices",
            "",
            "* Follow accessibility standards",
            "* Optimize performance",
            "* Write unit tests for components"
        ]
        
        file_path = os.path.join(output_dir, "frontend_guidelines.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return file_path
    
    def _generate_backend_structure(self, output_dir: str) -> str:
        """
        Generate Backend Structure document using LLM if available.
        
        Args:
            output_dir: Directory where to save the document
            
        Returns:
            Path to the generated document
        """
        # Use LLM if available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = """
                You are an expert at creating Backend Structure documents for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive 
                Backend Structure document with the following sections:
                1. Architecture Overview - High-level architecture of the backend
                2. Data Model - Key entities and relationships
                3. Service Layer - Core services and responsibilities
                4. API Layer - How the API is structured
                5. Dependencies - External services and integrations
                
                The output should be a well-formatted markdown document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive Backend Structure document:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "backend_structure.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
                
            except Exception as e:
                print(f"Warning: Failed to generate Backend Structure document with LLM: {e}")
        
        # Fallback to template
        content = [
            f"# {self.title} Backend Structure",
            "",
            "## Architecture Overview",
            "",
            "This document outlines the backend architecture for the project.",
            "",
            "## Data Model",
            "",
            "* Key entities and their relationships",
            "* Database schema design",
            "",
            "## Service Layer",
            "",
            "* Core business logic services",
            "* Service responsibilities and boundaries",
            "",
            "## API Layer",
            "",
            "* REST/GraphQL API structure",
            "* Authentication and authorization",
            "",
            "## Dependencies",
            "",
            "* External services",
            "* Third-party integrations"
        ]
        
        file_path = os.path.join(output_dir, "backend_structure.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return file_path
    
    def _generate_api_documentation(self, output_dir: str) -> str:
        """
        Generate API Documentation using LLM if available.
        
        Args:
            output_dir: Directory where to save the document
            
        Returns:
            Path to the generated document
        """
        # Use LLM if available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = """
                You are an expert at creating API Documentation for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive 
                API Documentation with the following sections:
                1. API Overview - General information about the API
                2. Authentication - How to authenticate with the API
                3. Endpoints - List of endpoints and their descriptions
                4. Request/Response Format - Structure of requests and responses
                5. Error Handling - How errors are reported and handled
                
                The output should be a well-formatted markdown document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create comprehensive API Documentation:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "api_documentation.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
                
            except Exception as e:
                print(f"Warning: Failed to generate API Documentation with LLM: {e}")
        
        # Fallback to template
        content = [
            f"# {self.title} API Documentation",
            "",
            "## API Overview",
            "",
            "This document provides information about the API endpoints for the project.",
            "",
            "## Authentication",
            "",
            "* Authentication method (e.g., Bearer tokens, API keys)",
            "* How to obtain credentials",
            "",
            "## Endpoints",
            "",
            "### Resource Endpoints",
            "",
            "* `GET /api/resource` - List resources",
            "* `POST /api/resource` - Create a resource",
            "",
            "## Request/Response Format",
            "",
            "* JSON structure for requests",
            "* JSON structure for responses",
            "",
            "## Error Handling",
            "",
            "* Error codes and meanings",
            "* Error response format"
        ]
        
        file_path = os.path.join(output_dir, "api_documentation.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return file_path
    
    def _generate_testing_guidelines(self, output_dir: str) -> str:
        """
        Generate Testing Guidelines document using LLM if available.
        
        Args:
            output_dir: Directory where to save the document
            
        Returns:
            Path to the generated document
        """
        # Use LLM if available
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = """
                You are an expert at creating Testing Guidelines for software projects.
                Your task is to analyze the provided initialization document and create comprehensive 
                Testing Guidelines with the following sections:
                1. Testing Strategy - Overall approach to testing
                2. Unit Testing - How to write and run unit tests
                3. Integration Testing - Testing component interactions
                4. End-to-End Testing - Full application testing
                5. Performance Testing - Testing for performance issues
                
                The output should be a well-formatted markdown document.
                """
                
                # Format the prompt to include the initialization document
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create comprehensive Testing Guidelines:
                
                {self.init_content}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "testing_guidelines.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
                
            except Exception as e:
                print(f"Warning: Failed to generate Testing Guidelines with LLM: {e}")
        
        # Fallback to template
        content = [
            f"# {self.title} Testing Guidelines",
            "",
            "## Testing Strategy",
            "",
            "This document outlines the testing approach for the project.",
            "",
            "## Unit Testing",
            "",
            "* Test individual components in isolation",
            "* Use appropriate mocking techniques",
            "",
            "## Integration Testing",
            "",
            "* Test interactions between components",
            "* Focus on API contracts and boundaries",
            "",
            "## End-to-End Testing",
            "",
            "* Test complete user flows",
            "* Simulate real user interactions",
            "",
            "## Performance Testing",
            "",
            "* Load testing methodology",
            "* Performance metrics and thresholds"
        ]
        
        file_path = os.path.join(output_dir, "testing_guidelines.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return file_path 