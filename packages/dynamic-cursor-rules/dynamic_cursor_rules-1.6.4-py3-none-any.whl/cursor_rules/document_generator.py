"""
Document generator for Cursor Rules.

This module handles the generation of all required documents from an initialization file,
including the Product Requirements Document, Technical Stack Document, and others.
"""
import os
import re
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from tqdm import tqdm
from colorama import Fore, Style

from .task_parser import extract_metadata_from_markdown, parse_initialization_doc
from .task_tracker import ActionPlan
from .utils import generate_cursorrules_file, save_cursorrules_file, save_modern_cursor_rules
from .core import RuleSet, Rule
from .llm_connector import LLMProvider, LLMConnector, LLMRequest
from .terminal_utils import print_header, print_success, print_step, print_info, print_warning

# Set up logger
logger = logging.getLogger(__name__)

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
        
        # Check if the file exists
        if not os.path.exists(init_doc_path):
            raise FileNotFoundError(f"Initialization file not found: {init_doc_path}")
        
        # Read the initialization document
        try:
            with open(init_doc_path, 'r', encoding='utf-8') as f:
                self.init_content = f.read()
        except Exception as e:
            raise IOError(f"Failed to read initialization file: {e}")
        
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
                print_info(f"Using {self.llm_provider.value} to enhance document generation")
            else:
                print_info("No LLM providers available - using template-based generation")
        except Exception as e:
            logger.warning(f"Failed to set up LLM provider: {e}")
        
        # Display generation plan
        print_header("Document Generation Plan")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Product Requirements Document")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Technical Stack Document")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Cursor Rules Configuration")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Action Items & Task List")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Development Log")
        print()
        
        # Generate the PRD with LLM enhancement first - all other documents will use this as source
        print_step("Generating Product Requirements Document...")
        start_time = time.time()
        prd_path = self._generate_prd(docs_dir)
        elapsed = time.time() - start_time
        generated_files["Product Requirements Document"] = prd_path
        print_success(f"Created Product Requirements Document ({elapsed:.1f}s)")
        
        # Read the generated PRD to use as input for all other document generation
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                self.generated_prd_content = f.read()
        except Exception as e:
            logger.warning(f"Failed to read generated PRD: {e}")
            self.generated_prd_content = None
        
        # Generate the Technical Stack document with LLM enhancement based on the PRD
        print_step("Generating Technical Stack Document...")
        start_time = time.time()
        tech_stack_path = self._generate_tech_stack_doc(docs_dir)
        elapsed = time.time() - start_time
        generated_files["Technical Stack Document"] = tech_stack_path
        print_success(f"Created Technical Stack Document ({elapsed:.1f}s)")
        
        # Generate the .cursorrules file with LLM enhancement based on the PRD
        print_step("Generating Cursor Rules Configuration...")
        start_time = time.time()
        cursorrules_paths = self._generate_cursorrules(cursor_dir)
        elapsed = time.time() - start_time
        if cursorrules_paths:
            if len(cursorrules_paths) == 1:
                generated_files["Cursor Rules"] = cursorrules_paths[0]
        print_success(f"Created Cursor Rules Configuration ({elapsed:.1f}s)")
            else:
                for i, path in enumerate(cursorrules_paths):
                    rule_name = os.path.basename(path).replace('.mdc', '').replace('_', ' ').title()
                    generated_files[f"Cursor Rule: {rule_name}"] = path
                print_success(f"Created {len(cursorrules_paths)} Cursor Rules files ({elapsed:.1f}s)")
        
        # Generate the Action Items document based on the PRD
        print_step("Generating Action Items & Task List...")
        start_time = time.time()
        tasks_json_path, tasks_md_path = self._generate_action_items(docs_dir)
        elapsed = time.time() - start_time
        generated_files["Action Items JSON"] = tasks_json_path
        generated_files["Action Items Markdown"] = tasks_md_path
        print_success(f"Created Action Items and Task List ({elapsed:.1f}s)")
        
        # Determine which optional documents to generate based on PRD content analysis
        optional_docs = self._determine_optional_documents()
        
        # Generate any optional documents based on the PRD
        if optional_docs:
            print_step(f"Generating {len(optional_docs)} additional documents based on project needs...")
            
            for doc_type in optional_docs:
                if doc_type == "app_flow":
                    start_time = time.time()
                    doc_path = self._generate_app_flow_doc(docs_dir)
                    elapsed = time.time() - start_time
                    generated_files["App Flow Document"] = doc_path
                    print_info(f"Created App Flow Document ({elapsed:.1f}s)")
                elif doc_type == "frontend_guidelines":
                    start_time = time.time()
                    doc_path = self._generate_frontend_guidelines(docs_dir)
                    elapsed = time.time() - start_time
                    generated_files["Frontend Guidelines"] = doc_path
                    print_info(f"Created Frontend Guidelines ({elapsed:.1f}s)")
                elif doc_type == "backend_structure":
                    start_time = time.time()
                    doc_path = self._generate_backend_structure(docs_dir)
                    elapsed = time.time() - start_time
                    generated_files["Backend Structure Document"] = doc_path
                    print_info(f"Created Backend Structure Document ({elapsed:.1f}s)")
                elif doc_type == "api_documentation":
                    start_time = time.time()
                    doc_path = self._generate_api_documentation(docs_dir)
                    elapsed = time.time() - start_time
                    generated_files["API Documentation"] = doc_path
                    print_info(f"Created API Documentation ({elapsed:.1f}s)")
                elif doc_type == "testing_guidelines":
                    start_time = time.time()
                    doc_path = self._generate_testing_guidelines(docs_dir)
                    elapsed = time.time() - start_time
                    generated_files["Testing Guidelines"] = doc_path
                    print_info(f"Created Testing Guidelines ({elapsed:.1f}s)")
        
        # Create development log file
        print_step("Generating Development Log...")
        start_time = time.time()
        dev_log_path = self._create_development_log(docs_dir, generated_files)
        elapsed = time.time() - start_time
        generated_files["Development Log"] = dev_log_path
        print_success(f"Created Development Log ({elapsed:.1f}s)")
        
        return generated_files
    
    def _get_content_for_generation(self) -> str:
        """
        Get the content to use for document generation.
        
        Returns:
            The PRD content if available, otherwise falls back to initialization document
        """
        if hasattr(self, 'generated_prd_content') and self.generated_prd_content:
            return self.generated_prd_content
        return self.init_content
    
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
                # Extract tech stack information to provide to the LLM
                tech_stack = self._extract_tech_stack()
                tech_info = ""
                for category, technologies in tech_stack.items():
                    if technologies:
                        tech_info += f"{category.capitalize()}: {', '.join(technologies)}\n"
                
                # Create a request to generate a comprehensive PRD from the initialization doc
                system_message = """
                You are an expert at creating Product Requirements Documents (PRDs) for software projects.
                Your task is to analyze the provided initialization document and create a comprehensive PRD with the following sections:
                1. Product Vision - What problem does this solve and for whom?
                2. Target Users - Who will use this product?
                3. User Stories - What will users be able to do with the product?
                4. Functional Requirements - What features and functionality should the product include?
                5. Technical Architecture - What technologies will be used and how they fit together
                6. Non-Functional Requirements - Performance, security, usability, etc.
                7. Acceptance Criteria - How will we know the product meets the requirements?
                
                For the Technical Architecture section, incorporate the technologies mentioned in the initialization document
                and explain how they will be used together in the system architecture.
                
                The output should be a well-formatted markdown document with thoughtful, detailed content derived from the initialization document.
                """
                
                # Format the prompt to include the initialization document and tech stack info
                prompt = f"""
                Below is the initialization document for a software project. Please analyze it and create a comprehensive PRD.
                
                The following technologies were detected from the initialization document and should be incorporated into the Technical Architecture section:
                {tech_info}
                
                Initialization Document:
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate PRD with LLM: {e}")
        
        # Fallback: Generate a template-based PRD
        # Extract relevant sections from the initialization document
        overview_section = self._extract_section("Project Overview")
        core_functionality = self._extract_section("Core Functionality")
        tech_section = self._extract_section("Technical Stack") or self._extract_section("Tech Stack") or self._extract_section("Technical Requirements")
        
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
        
        # Add Technical Architecture section
        prd_content.extend([
            "",
            "## 5. Technical Architecture",
            "",
        ])
        
        # Extract tech stack information
        tech_stack = self._extract_tech_stack()
        
        # Add tech section if available from the document
        if tech_section:
            prd_content.append(tech_section)
        else:
            # Generate from extracted tech stack
            for category, technologies in tech_stack.items():
                if technologies:
                    prd_content.append(f"### {category.capitalize()}")
                    for tech in technologies:
                        prd_content.append(f"- {tech}")
                    prd_content.append("")
        
        prd_content.extend([
            "",
            "## 6. Non-Functional Requirements",
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
            "## 7. Acceptance Criteria",
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate Technical Stack Document with LLM: {e}")
        
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
    
    def _generate_cursorrules(self, cursor_dir: str) -> List[str]:
        """
        Generate cursor rules files using LLM if available.
        
        Args:
            cursor_dir: Directory where to save cursor rules
            
        Returns:
            List of paths to the generated rule files
        """
        # Import required modules within the function to ensure they're available
        import os
        import re
        import json
        import logging
        from pathlib import Path
        from .utils import save_modern_cursor_rules
        from .core import ProjectState, Component, ComponentStatus, ProjectPhase
        from .dynamic_rules import DynamicRuleManager
        
        # Create rules directory
        rules_dir = os.path.join(cursor_dir, "rules")
        os.makedirs(rules_dir, exist_ok=True)
        
        # Define a function to sanitize rule titles for filenames
        def sanitize_filename(title):
            # Replace spaces with underscores and remove invalid filename characters
            sanitized = re.sub(r'[\\/*?:"<>|]', '', title)
            # Limit length to avoid path length issues (max 50 chars)
            return sanitized[:50]
        
        # Extract project information for rule generation
        project_name = self.title
        project_description = self.description
        tech_stack = self._extract_tech_stack()
        directory_structure = self._extract_directory_structure()
        
        # Use the DynamicRuleManager for rule generation if available
        try:
            # Set up a project state
            project_state = ProjectState(
                name=project_name,
                description=project_description,
                tech_stack=tech_stack,
                directory_structure=directory_structure,
                # Default to setup phase for new projects
                phase=ProjectPhase.SETUP
            )
            
            # If tech stack suggests a frontend framework, add a UI component
            if tech_stack.get("frontend"):
                ui_component = Component(
                    name="UI Components",
                    path_pattern="src/components/**/*.{js,jsx,ts,tsx,vue,svelte}",
                    status=ComponentStatus.PLANNED,
                    description="User interface components"
                )
                project_state.add_component(ui_component)
            
            # If backend technologies, add API component
            if tech_stack.get("backend"):
                api_component = Component(
                    name="API Layer",
                    path_pattern="src/api/**/*.{js,ts,py,rb,php}",
                    status=ComponentStatus.PLANNED,
                    description="API endpoints and services"
                )
                project_state.add_component(api_component)
            
            # Detect project root (where to save the rules)
            project_dir = os.getcwd()
            
            # Initialize the dynamic rule manager
            rule_manager = DynamicRuleManager(project_dir, project_state)
            
            # Set some initial active features based on the PRD
            active_features = []
            for section in ["Core Functionality", "Key Features", "MVP Features"]:
                section_content = self._extract_section(section)
                if section_content:
                    # Extract bullet points as features
                    features = re.findall(r'[-*]\s+([^\n]+)', section_content)
                    active_features.extend([f.strip() for f in features[:3]])  # Limit to first 3
            
            if active_features:
                rule_manager.update_project_state(active_features=active_features)
                
            # Generate the rules
            generated_files = rule_manager.generate_dynamic_rules(force_regenerate=True)
            
            if generated_files:
                return generated_files
                
        except Exception as e:
            logger.warning(f"Failed to generate dynamic cursor rules: {e}")
            # Fall back to the original method if dynamic generation fails
        
        # Original generation method as fallback
        
        # Collect rule sources from initialization document
        rule_sources = {}
        for section_name in ["Coding Standards", "Best Practices", "Architecture", "Technical Requirements", "Core Functionality"]:
            section = self._extract_section(section_name)
            if section:
                rule_sources[section_name.lower()] = section
        
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
        generated_files = []
        
        if use_llm:
            try:
                # Create a request to generate comprehensive cursor rules
                system_message = """
                You are an expert at creating rules for Cursor IDE. These files provide guidance 
                to AI assistants when users are working on a project.
                
                Create multiple specialized rule files that follow proper .mdc format structure. Each rule file should include:
                
                1. A title that describes the rule category (clear and specific)
                2. A pattern glob that specifies which files the rule applies to (be precise with file patterns)
                3. A description that explains when the rule should be applied (include rationale)
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
                
                Create separate rule files for:
                1. General project guidelines (applicable to all files)
                2. Frontend development (if applicable)
                3. Backend development
                4. Testing practices
                5. Architecture guidelines
                6. Code style and formatting
                7. Documentation standards
                
                For example, a frontend rule file would look like:
                
                ```
                # Frontend Component Rules
                
                pattern: "src/components/**/*.{tsx,jsx}"
                description: "Rules for React component development that ensure maintainability and consistency across UI components"
                
                ## Component Structure
                
                - Use functional components with hooks instead of class components
                - Follow the single responsibility principle - one component should do one thing well
                - Extract reusable logic into custom hooks with clear naming
                
                ### Good Example:
                ```jsx
                // UserProfile.jsx - A focused component that only handles user profile display
                function UserProfile({ user }) {
                  return (
                    <div className="profile">
                      <ProfileHeader user={user} />
                      <ProfileDetails user={user} />
                    </div>
                  );
                }
                ```
                
                ### Bad Example:
                ```jsx
                // Avoid components that do too many things
                function UserDashboard({ user }) {
                  // This component handles profile, settings, notifications, and more
                  // Better to split these into separate components
                  // ...complex implementation...
                }
                ```
                
                ## Styling Guidelines
                
                - Use CSS modules or styled-components for component-specific styling
                - Follow design system specifications for consistency
                - Implement responsive designs using the project's breakpoint system
                
                @file: src/components/example/Button.tsx
                @file: src/components/common/Card.tsx
                ```
                
                Format your response as a JSON array where each object has these fields:
                - title: The rule title (clear and descriptive)
                - pattern: Glob pattern for file matching (be specific with extensions and paths)
                - description: When to apply this rule (include the rationale)
                - content: The main markdown content (including good and bad examples where appropriate)
                - references: Array of example files to reference (at least 2-3 per rule file if possible)
                
                Example response format:
                [
                  {
                    "title": "Frontend Component Rules",
                    "pattern": "src/components/**/*.{tsx,jsx}",
                    "description": "Rules for React component development that ensure consistent, maintainable UI code",
                    "content": "## Component Structure\\n\\n- Use functional components with hooks\\n- Follow single responsibility principle\\n\\n## Styling Guidelines\\n\\n- Use CSS modules\\n\\n### Good Example:\\n```jsx\\nfunction Button({ label, onClick }) {\\n  return <button onClick={onClick}>{label}</button>;\\n}\\n```",
                    "references": ["src/components/example/Button.tsx", "src/components/common/Card.tsx"]
                  },
                  {
                    "title": "Backend API Rules",
                    "pattern": "src/api/**/*.{ts,js}",
                    "description": "Guidelines for API implementation to ensure security, performance and maintainability",
                    "content": "## Endpoint Design\\n\\n- Follow RESTful principles\\n- Include proper error handling with standardized response formats\\n\\n## Security\\n\\n- Validate all inputs\\n- Use parameterized queries",
                    "references": ["src/api/users.ts", "src/api/auth.ts"]
                  }
                ]
                """
                
                # Format the prompt to include the PRD
                prompt = f"""
                Below is the Product Requirements Document (PRD) for a software project. Please analyze it and create comprehensive Cursor rules:
                
                {self._get_content_for_generation()}
                
                Create specialized rules for different aspects of the project based on the PRD.
                Focus on the specific technologies, architecture, and practices mentioned.
                
                Tech Stack:
                {json.dumps(self._extract_tech_stack(), indent=2)}
                
                Directory Structure:
                {json.dumps(self._extract_directory_structure(), indent=2)}
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=4000
                )
                
                response = self.llm_connector.request(request)
                rules_content = response.text.strip()
                
                # Extract JSON content
                # Find and parse the JSON array
                json_match = re.search(r'\[\s*\{.+\}\s*\]', rules_content, re.DOTALL)
                if json_match:
                    rules_json = json_match.group(0)
                    try:
                        rules_data = json.loads(rules_json)
                        
                        # Save each rule file
                        for rule in rules_data:
                            title = rule.get("title", "Unnamed Rule")
                            # Sanitize the title for filename use
                            sanitized_title = sanitize_filename(title)
                            pattern = rule.get("pattern", "**/*")
                            description = rule.get("description", "")
                            content = rule.get("content", "")
                            references = rule.get("references", [])
                            
                            rule_path = save_modern_cursor_rules(
                                rules_dir, 
                                sanitized_title, 
                                pattern, 
                                description, 
                                content, 
                                references
                            )
                            generated_files.append(rule_path)
                        
                        # If successful, return the generated files
                        if generated_files:
                            return generated_files
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse rules JSON: {e}")
                
                # If JSON parsing fails, try to extract rule sections manually
                if not generated_files:
                    logger.warning("JSON parsing failed, attempting manual extraction of rule sections")
                    # Extract rule sections by looking for markdown headings
                    rule_sections = re.split(r'# ([^\n]+)', rules_content)
                    if len(rule_sections) > 1:
                        # First element is usually empty, skip it
                        for i in range(1, len(rule_sections), 2):
                            if i + 1 < len(rule_sections):
                                title = rule_sections[i].strip()
                                # Sanitize the title for filename use
                                sanitized_title = sanitize_filename(title)
                                content = rule_sections[i + 1].strip()
                                
                                # Try to extract pattern and description
                                pattern_match = re.search(r'pattern:\s*"([^"]+)"', content)
                                pattern = pattern_match.group(1) if pattern_match else "**/*"
                                
                                desc_match = re.search(r'description:\s*"([^"]+)"', content)
                                description = desc_match.group(1) if desc_match else ""
                                
                                # Clean up content by removing pattern and description lines
                                clean_content = re.sub(r'pattern:\s*"[^"]+"\n', '', content)
                                clean_content = re.sub(r'description:\s*"[^"]+"\n', '', clean_content)
                                
                                # Extract file references
                                references = []
                                for line in clean_content.split('\n'):
                                    if line.startswith('@file:'):
                                        ref = line.replace('@file:', '').strip()
                                        references.append(ref)
                                        clean_content = clean_content.replace(line, '')
                                
                                # Save the rule file
                                rule_path = save_modern_cursor_rules(
                                    rules_dir,
                                    sanitized_title,
                                    pattern,
                                    description,
                                    clean_content.strip(),
                                    references
                                )
                                generated_files.append(rule_path)
                    
                    if generated_files:
                        return generated_files
                
            except Exception as e:
                logger.warning(f"Failed to generate cursor rules with LLM: {e}")
        
        # Fallback: Generate rules based on tech stack analysis
        try:
            # Extract tech stack information
            tech_stack = self._extract_tech_stack()
            backend_techs = tech_stack.get("backend", [])
            frontend_techs = tech_stack.get("frontend", [])
            libraries = tech_stack.get("libraries", [])
            
            # Generate general project rules
            general_content = """## Project Guidelines

- Use consistent code formatting throughout the project
- Follow the established directory structure
- Document all public APIs and interfaces
- Implement proper error handling
- Use descriptive variable and function names"""
            
            general_path = save_modern_cursor_rules(
                rules_dir,
                "General_Project_Rules",  # Sanitized title
                "**/*",
                "Rules applicable to all project files",
                general_content
            )
            generated_files.append(general_path)
            
            # Generate backend rules if applicable
            if backend_techs:
                backend_pattern = "src/backend/**/*.{js,ts,py,java,go,rb}"
                backend_desc = "Rules for backend development"
                
            if any("python" in tech.lower() for tech in backend_techs):
                    backend_pattern = "**/*.py"
                    backend_content = """## Python Guidelines

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all modules, classes, and functions
- Use virtual environments for dependency management
- Write unit tests for all non-trivial functions"""
                elif any(tech.lower() in ["javascript", "typescript", "node"] for tech in backend_techs):
                    backend_pattern = "**/*.{js,ts}"
                    backend_content = """## JavaScript/TypeScript Guidelines

- Use ESLint for code quality and style enforcement
- Prefer TypeScript over JavaScript for type safety
- Use async/await for asynchronous operations
- Document functions with JSDoc comments
- Write unit tests with Jest"""
                else:
                    # Generic backend rules
                    backend_content = """## Backend Guidelines

- Follow the repository pattern for data access
- Implement proper error handling and logging
- Use dependency injection where appropriate
- Document all API endpoints
- Write comprehensive tests"""
                
                backend_path = save_modern_cursor_rules(
                    rules_dir,
                    "Backend_Development_Rules",  # Sanitized title
                    backend_pattern,
                    backend_desc,
                    backend_content
                )
                generated_files.append(backend_path)
            
            # Generate frontend rules if applicable
            if frontend_techs:
                frontend_pattern = "src/frontend/**/*.{js,jsx,ts,tsx,vue,svelte}"
                frontend_desc = "Rules for frontend development"
                
                # React-specific rules
                if any("react" in tech.lower() for tech in frontend_techs + libraries):
                    frontend_pattern = "**/*.{jsx,tsx}"
                    frontend_content = """## React Guidelines

- Use functional components with hooks instead of class components
- Implement proper prop validation
- Follow the React component file structure convention
- Extract reusable logic into custom hooks
- Write tests for all components"""
            else:
                    # Generic frontend rules
                    frontend_content = """## Frontend Guidelines

- Follow component-based architecture
- Use CSS modules or styled components for styling
- Implement responsive design principles
- Ensure accessibility compliance
- Optimize for performance"""
                
                frontend_path = save_modern_cursor_rules(
                    rules_dir,
                    "Frontend_Development_Rules",  # Sanitized title
                    frontend_pattern,
                    frontend_desc,
                    frontend_content
                )
                generated_files.append(frontend_path)
            
            # Generate database rules if applicable
            db_keywords = ["sql", "database", "postgres", "mysql", "mongodb", "nosql"]
            if any(keyword in tech.lower() for tech in backend_techs + libraries for keyword in db_keywords):
                db_content = """## Database Guidelines

- Use parameterized queries to prevent SQL injection
- Implement proper database migration strategy
- Use an ORM for database operations when appropriate
- Include database schema documentation
- Implement proper error handling for database operations"""
                
                db_path = save_modern_cursor_rules(
                    rules_dir,
                    "Database_Rules",  # Sanitized title
                    "**/*.{sql,py,js,ts}",
                    "Guidelines for database operations",
                    db_content
                )
                generated_files.append(db_path)
            
            # Generate testing rules
            testing_content = """## Testing Guidelines

- Write unit tests for all business logic
- Use integration tests for component interactions
- Implement end-to-end tests for critical user flows
- Mock external dependencies in tests
- Aim for high test coverage of critical code paths"""
            
            testing_path = save_modern_cursor_rules(
                rules_dir,
                "Testing_Rules",  # Sanitized title
                "**/*.{test,spec}.{js,jsx,ts,tsx,py}",
                "Guidelines for testing practices",
                testing_content
            )
            generated_files.append(testing_path)
            
            except Exception as e:
            logger.warning(f"Could not generate rule files: {e}")
            # Create a single basic rule file as absolute fallback
            try:
                basic_content = """## Basic Guidelines

- Write clean, readable code
- Include appropriate documentation
- Follow consistent formatting
- Write tests for your code"""
                
                basic_path = save_modern_cursor_rules(
                    rules_dir,
                    "Basic_Project_Rules",  # Sanitized title
                    "**/*",
                    "General guidelines for this project",
                    basic_content
                )
                generated_files.append(basic_path)
            except Exception:
                logger.error("Failed to create even basic rule files")
        
        return generated_files
    
    def _generate_action_items_with_llm(self) -> ActionPlan:
        """
        Generate an action plan using an LLM based on the PRD content.
        
        Returns:
            ActionPlan object containing phases, tasks, and subtasks
        """
        # Verify we have a valid LLM provider
        if not self.llm_connector.is_provider_available(self.llm_provider):
            raise RuntimeError(f"No LLM provider available. Required for action item generation.")
        
        # Prepare a message for the LLM that explains what we want
        system_message = """
        You are an expert software project planner. Based on the provided Product Requirements Document (PRD), 
        create a comprehensive development action plan with tasks and subtasks.
        
        Instead of copying the PRD structure, create actual development tasks that would be needed to implement the project.
        Organize tasks by development phases, not by feature categories.
        
        Structure your response as a JSON object with the following format:
        
        [
          {
            "id": "phase-1",
            "title": "Phase 1: Project Setup & Architecture",
            "description": "Initial setup and architectural foundation",
            "tasks": [
              {
                "id": "p1t1",
                "title": "Set up development environment",
                "description": "Configure all necessary tools and environments for development",
                "status": "not_started",
                "priority": 3,
                "effort": 2,
                "subtasks": [
                  {
                    "id": "p1t1s1",
                    "title": "Install required SDKs and frameworks",
                    "status": "not_started"
                  },
                  {
                    "id": "p1t1s2",
                    "title": "Configure version control system",
                    "status": "not_started"
                  }
                ]
              }
            ]
          }
        ]
        
        Guidelines:
        1. Organize tasks into 3-5 logical development phases (e.g., "Project Setup", "Core Features Development", "User Interface", "Testing & Refinement", "Deployment")
        2. Each task should represent actual development work, not just features from the PRD
        3. Break down larger tasks into specific, actionable subtasks
        4. Set appropriate priority (1=low, 2=medium, 3=high) and effort (1=small, 2=medium, 3=large)
        5. Create meaningful task IDs that reflect the phase (e.g., "p1t1" for Phase 1, Task 1)
        6. Include 3-8 subtasks for any complex development task
        7. Ensure all tasks start with status "not_started"
        8. Consider all aspects including development, testing, documentation, and deployment
        9. Focus on development steps, not just listing features
        
        Examples of good tasks:
        - "Implement user authentication system" (not just "Authentication")
        - "Create database schema for time tracking" (not just "Database")
        - "Develop category management UI components" (not just "Categories")
        
        Your response MUST be valid JSON. Do not include any explanatory text, markdown formatting, or code blocks.
        The response should start with '[' and end with ']' with no additional characters.
        """
        
        # Get an LLM response
        response = self.llm_connector.generate(
            provider=self.llm_provider,
            system_prompt=system_message,
            user_prompt=f"Here's the Product Requirements Document:\n\n{self.generated_prd_content}\n\nGenerate an action plan in the specified JSON format.",
            max_tokens=4000,
            temperature=0.2  # Lower temperature for more consistent JSON
        )
        
        # Extract JSON from the response
        json_str = self._extract_json_from_response(response)
        
        # Parse the JSON into an ActionPlan object
        try:
            import json
            from .task_tracker import ActionPlan, Phase, Task, TaskStatus
            
            phases_data = json.loads(json_str)
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
            
            # Ensure we have a valid action plan
            if not action_plan.phases:
                raise ValueError("Generated action plan has no phases")
                
            return action_plan
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response as action plan: {e}")
            logger.debug(f"Raw JSON: {json_str}")
            raise ValueError(f"Invalid action plan format: {e}")
    
    def _retry_action_item_generation(self) -> ActionPlan:
        """
        Retry action item generation with more explicit formatting instructions.
        Uses a simpler prompt but still relies on the PRD content.
        """
        system_message = """
        You are tasked with creating a JSON array of development phases, tasks, and subtasks.
        Your response MUST be valid JSON that starts with '[' and ends with ']'.
        
        DO NOT include any explanatory text, markdown formatting, or code blocks.
        DO NOT use backticks (```) anywhere in your response.
        
        Follow this exact template with no deviations:
        
        [
          {
            "id": "phase-1",
            "title": "Phase 1: Project Setup",
            "description": "Project setup description",
            "tasks": [
              {
                "id": "p1t1",
                "title": "Task 1 Title",
                "description": "Task 1 description",
                "status": "not_started",
                "priority": 3,
                "effort": 2,
                "subtasks": [
                  {
                    "id": "p1t1s1",
                    "title": "Subtask 1 Title",
                    "status": "not_started"
                  }
                ]
              }
            ]
          }
        ]
        """
        
        # Create a more specific prompt using the PRD
        prompt = f"""
        Based on this Product Requirements Document:
        
        {self.generated_prd_content}
        
        Create a development action plan with 3-5 phases, where each phase has 3-6 tasks, and each task has 2-5 subtasks.
        
        Your response MUST be valid JSON with no trailing commas or syntax errors.
        
        Organize development into logical phases (setup, core features, etc.)
        and provide specific, actionable tasks and subtasks.
        """
        
        # Get an LLM response
        response = self.llm_connector.generate(
            provider=self.llm_provider,
            system_prompt=system_message,
            user_prompt=prompt,
            max_tokens=4000,
            temperature=0.1  # Very low temperature for deterministic output
        )
        
        # Extract JSON from the response
        json_str = self._extract_json_from_response(response)
        
        # Parse the JSON into an ActionPlan object
        try:
            import json
            from .task_tracker import ActionPlan, Phase, Task, TaskStatus
            
            phases_data = json.loads(json_str)
            action_plan = ActionPlan(title="Project Action Plan")
            
            for phase_data in phases_data:
                phase = Phase(
                    title=phase_data.get("title", "Unnamed Phase"),
                    description=phase_data.get("description", "")
                )
                
                for task_data in phase_data.get("tasks", []):
                    task = Task(
                        title=task_data.get("title", "Unnamed Task"),
                        description=task_data.get("description", ""),
                        task_id=task_data.get("id"),
                        priority=task_data.get("priority", 0),
                        effort=task_data.get("effort", 0)
                    )
                    
                    status_str = task_data.get("status", "not_started").upper()
                    if hasattr(TaskStatus, status_str):
                        task.status = getattr(TaskStatus, status_str)
                    
                    for subtask_data in task_data.get("subtasks", []):
                        subtask = Task(
                            title=subtask_data.get("title", "Unnamed Subtask"),
                            description=subtask_data.get("description", ""),
                            task_id=subtask_data.get("id")
                        )
                        
                        subtask_status_str = subtask_data.get("status", "not_started").upper()
                        if hasattr(TaskStatus, subtask_status_str):
                            subtask.status = getattr(TaskStatus, subtask_status_str)
                        
                        task.add_subtask(subtask)
                    
                    phase.add_task(task)
                
                action_plan.add_phase(phase)
            
            if not action_plan.phases:
                raise ValueError("Generated action plan has no phases")
                
            return action_plan
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response from retry as action plan: {e}")
            logger.debug(f"Raw JSON: {json_str}")
            raise ValueError(f"Invalid action plan format from retry: {e}")
    
    def _save_action_plan_as_markdown(self, output_path: str, action_plan: ActionPlan) -> None:
        """
        Save an action plan as a Markdown document.
        
        Args:
            output_path: Path where to save the Markdown document
            action_plan: ActionPlan object to save
        """
        from .task_tracker import TaskStatus
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write the title
            f.write(f"# {action_plan.title}\n\n")
            
            # Write an overview section
            f.write("## Project Overview\n\n")
            if hasattr(self, 'description') and self.description:
                f.write(f"{self.description}\n\n")
            else:
                f.write("This document outlines the development action plan for the project.\n\n")
            
            # Write core philosophy if available
            if 'goals' in self.metadata:
                f.write("## Core Philosophy\n\n")
                f.write(f"{self.metadata['goals']}\n\n")
            
            # Add platform information if available
            tech_stack = self._extract_tech_stack()
            platforms = tech_stack.get('platforms', [])
            if platforms:
                f.write("## Platforms\n\n")
                for platform in platforms:
                    f.write(f"- {platform}\n")
                f.write("\n")
            
            # Add tech stack information
            if tech_stack:
                f.write("## Tech Stack\n\n")
                for category, techs in tech_stack.items():
                    if techs and category != 'platforms':
                        f.write(f"### {category.capitalize()}\n\n")
                        for tech in techs:
                            f.write(f"- {tech}\n")
                        f.write("\n")
            
            # Add key features if available
            if 'overview' in self.metadata:
                f.write("## Key Features\n\n")
                f.write(f"{self.metadata['overview']}\n\n")
            
            # Write the development phases and tasks
            f.write("## Development Phases\n\n")
            
            for i, phase in enumerate(action_plan.phases):
                # Write the phase title
                f.write(f"### {phase.title}\n\n")
                
                # Write the phase description if available
            if phase.description:
                    f.write(f"{phase.description}\n\n")
                
                # Write each task in the phase
                for j, task in enumerate(phase.tasks):
                    # Generate a unique ID for the task if not already present
                    task_id = task.id or f"p{i+1}t{j+1}"
                    
                    # Write the task with its ID, priority, and effort
                    priority_str = ["", "🔽 Low", "➡️ Medium", "🔼 High"][min(3, max(0, task.priority))]
                    effort_str = ["", "⚪ Small", "🟡 Medium", "🔴 Large"][min(3, max(0, task.effort))]
                    
                    status_emoji = {
                        TaskStatus.NOT_STARTED: "⬜",
                        TaskStatus.IN_PROGRESS: "🟨",
                        TaskStatus.COMPLETED: "✅",
                        TaskStatus.BLOCKED: "🚫",
                    }.get(task.status, "⬜")
                    
                    task_header = f"{status_emoji} **[{task_id}]** {task.title}"
                    if priority_str:
                        task_header += f" ({priority_str}"
                        if effort_str:
                            task_header += f", {effort_str}"
                        task_header += ")"
                    elif effort_str:
                        task_header += f" ({effort_str})"
                    
                    f.write(f"#### {task_header}\n\n")
                    
                    # Write the task description if available
                if task.description:
                        f.write(f"{task.description}\n\n")
                    
                    # Write the subtasks if any
                    if task.subtasks:
                        f.write("**Subtasks:**\n\n")
                        for k, subtask in enumerate(task.subtasks):
                            # Generate a unique ID for the subtask if not already present
                            subtask_id = subtask.id or f"{task_id}s{k+1}"
                            
                            # Get subtask status emoji
                            subtask_status_emoji = {
                                TaskStatus.NOT_STARTED: "⬜",
                                TaskStatus.IN_PROGRESS: "🟨",
                                TaskStatus.COMPLETED: "✅",
                                TaskStatus.BLOCKED: "🚫",
                            }.get(subtask.status, "⬜")
                            
                            # Write the subtask
                            f.write(f"- {subtask_status_emoji} **[{subtask_id}]** {subtask.title}\n")
                        
                        f.write("\n")
                    
                    # Add tags if available
                    if task.tags:
                        f.write(f"**Tags:** {', '.join(task.tags)}\n\n")
            
            # Add a footer with the generation date
            from datetime import datetime
            generation_date = datetime.now().strftime("%Y-%m-%d")
            f.write(f"\n\n---\n*Generated on {generation_date} using Cursor Rules*\n")
    
    def _extract_section(self, section_name: str) -> str:
        """
        Extract a section from the initialization document.
        
        Args:
            section_name: Name of the section to extract
            
        Returns:
            Content of the section, or empty string if not found
        """
        pattern = rf'(?:^|\n)##\s+{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)'
        matches = re.findall(pattern, self._get_content_for_generation(), re.DOTALL)
        return matches[0].strip() if matches else ""
    
    def _extract_tech_stack(self) -> Dict[str, List[str]]:
        """
        Extract tech stack information from the document.
        
        Returns:
            Dictionary mapping stack categories to technologies
        """
        content = self._get_content_for_generation()
        
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "libraries": [],
            "devops": [],
            "other": []
        }
        
        # Check for tech stack section
        tech_section = self._extract_section("Technical Stack") or self._extract_section("Tech Stack")
        
        if tech_section:
            # Parse the tech stack section
            for line in tech_section.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    item = line[1:].strip()
                    if ':' in item:
                        # Format: "- category: tech1, tech2"
                        category, techs = item.split(':', 1)
                        category = category.strip().lower()
                        tech_list = [t.strip() for t in techs.split(',')]
                        
                        if category in tech_stack:
                            tech_stack[category].extend(tech_list)
                        else:
                            tech_stack["other"].extend(tech_list)
                    else:
                        # Guess the category based on keywords
                        if any(kw in item.lower() for kw in ["react", "vue", "angular", "html", "css", "js", "javascript", "typescript"]):
                            tech_stack["frontend"].append(item)
                        elif any(kw in item.lower() for kw in ["node", "python", "java", "c#", ".net", "php", "go", "ruby", "flask", "django", "express"]):
                            tech_stack["backend"].append(item)
                        elif any(kw in item.lower() for kw in ["sql", "mongo", "postgres", "mysql", "database", "redis", "nosql"]):
                            tech_stack["database"].append(item)
                        elif any(kw in item.lower() for kw in ["docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins", "git"]):
                            tech_stack["devops"].append(item)
                        else:
                            tech_stack["libraries"].append(item)
        else:
            # Attempt to extract tech information from the entire document
            # Frontend technologies
            frontend_techs = ["react", "vue", "angular", "svelte", "html", "css", "javascript", "typescript", 
                             "nextjs", "nuxt", "gatsby", "bootstrap", "tailwind"]
            # Backend technologies
            backend_techs = ["node", "express", "python", "django", "flask", "fastapi", "java", "spring", "c#", 
                            ".net", "php", "laravel", "go", "ruby", "rails"]
            # Database technologies
            db_techs = ["sql", "mysql", "postgresql", "mongodb", "sqlite", "redis", "cassandra", "dynamodb"]
            # DevOps technologies
            devops_techs = ["docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "github actions"]
            
            # Scan content for mentions of techs
            for tech in frontend_techs:
                if re.search(fr'\b{re.escape(tech)}\b', content.lower()):
                    tech_stack["frontend"].append(tech)
                    
            for tech in backend_techs:
                if re.search(fr'\b{re.escape(tech)}\b', content.lower()):
                    tech_stack["backend"].append(tech)
                    
            for tech in db_techs:
                if re.search(fr'\b{re.escape(tech)}\b', content.lower()):
                    tech_stack["database"].append(tech)
                    
            for tech in devops_techs:
                if re.search(fr'\b{re.escape(tech)}\b', content.lower()):
                    tech_stack["devops"].append(tech)
        
        # Ensure we have at least some backend technologies
        if not tech_stack["backend"]:
            tech_stack["backend"] = ["Python 3.9+"]
            
        # Ensure we have at least some libraries
        if not tech_stack["libraries"]:
            tech_stack["libraries"] = ["Standard libraries"]
        
        return tech_stack
    
    def _extract_directory_structure(self) -> Dict[str, str]:
        """
        Extract directory structure information from the document.
        
        Returns:
            Dictionary mapping directory names to descriptions
        """
        content = self._get_content_for_generation()
        
        structure = {}
        
        # Check for directory structure section
        structure_section = self._extract_section("Directory Structure") or self._extract_section("Project Structure")
        
        if structure_section:
            # Parse the structure section
            for line in structure_section.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    item = line[1:].strip()
                    if ':' in item:
                        # Format: "- dir/: description"
                        dir_name, desc = item.split(':', 1)
                        dir_name = dir_name.strip()
                        structure[dir_name] = desc.strip()
                    elif '/' in item or '\\' in item:
                        # Format: "- dir/" or "- dir/subdir/"
                        dir_name = item
                        structure[dir_name] = ""
        
        # If no structure found, use common defaults
        if not structure:
            structure = {
                "src/": "Source code",
                "docs/": "Documentation",
                "tests/": "Tests"
            }
        
        return structure
    
    def _determine_optional_documents(self) -> List[str]:
        """
        Analyze the initialization document to determine which optional documents to generate.
        
        Returns:
            List of document types to generate
        """
        optional_docs = []
        
        # Check for frontend-related terms
        frontend_indicators = ["frontend", "UI", "user interface", "react", "vue", "angular", "css", "html", "javascript", "typescript"]
        if any(indicator.lower() in self._get_content_for_generation().lower() for indicator in frontend_indicators):
            optional_docs.append("frontend_guidelines")
            
            # If there's significant UI emphasis, generate app flow
            ui_indicators = ["user flow", "app flow", "interface", "interaction", "user experience", "UX"]
            if sum(self._get_content_for_generation().lower().count(indicator.lower()) for indicator in ui_indicators) >= 2:
                optional_docs.append("app_flow")
        
        # Check for backend-related terms
        backend_indicators = ["backend", "server", "database", "api", "microservice", "service", "architecture"]
        if any(indicator.lower() in self._get_content_for_generation().lower() for indicator in backend_indicators):
            optional_docs.append("backend_structure")
            
            # If there's API emphasis, generate API docs
            api_indicators = ["api", "rest", "graphql", "endpoint", "http", "request", "response"]
            if sum(self._get_content_for_generation().lower().count(indicator.lower()) for indicator in api_indicators) >= 2:
                optional_docs.append("api_documentation")
        
        # Check for testing emphasis
        test_indicators = ["test", "quality assurance", "qa", "unit test", "integration test", "e2e", "end-to-end"]
        if sum(self._get_content_for_generation().lower().count(indicator.lower()) for indicator in test_indicators) >= 2:
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
                
                {self._get_content_for_generation()}
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
                    logger.warning(f"Failed to parse LLM document suggestions: {e}")
                
            except Exception as e:
                logger.warning(f"Failed to get document suggestions from LLM: {e}")
        
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate App Flow document with LLM: {e}")
        
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate Frontend Guidelines with LLM: {e}")
        
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate Backend Structure document with LLM: {e}")
        
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate API Documentation with LLM: {e}")
        
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
                
                {self._get_content_for_generation()}
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
                logger.warning(f"Failed to generate Testing Guidelines with LLM: {e}")
        
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
    
    def _create_development_log(self, output_dir: str, generated_files: Dict[str, str]) -> str:
        """
        Create a development log file to track project changes.
        
        Args:
            output_dir: Directory where to save the log
            generated_files: Dictionary of generated files
            
        Returns:
            Path to the generated development log
        """
        import datetime
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create content for development log
        log_content = [
            "# Development Log",
            "",
            "This file tracks all significant changes made to the project.",
            "",
            f"## {today} - Initial Project Setup",
            "",
            "### Generated Initial Documentation",
            "",
            "Created the following project documentation files:",
            ""
        ]
        
        # Add list of generated files
        for doc_name, file_path in generated_files.items():
            relative_path = os.path.relpath(file_path, os.getcwd())
            log_content.append(f"- **{doc_name}**: `{relative_path}`")
        
        log_content.extend([
            "",
            "### Next Steps",
            "",
            "- Review and refine generated documentation",
            "- Begin implementation of core features",
            "- Set up development environment",
            ""
        ])
        
        # Write the development log to a file
        dev_log_path = os.path.join(output_dir, "development-log.md")
        with open(dev_log_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(log_content))
        
        return dev_log_path 
    
    def _generate_action_items(self, output_dir: str = None) -> Tuple[str, str]:
        """
        Generate the Action Items documents (JSON and Markdown) from the PRD.
        
        Args:
            output_dir: Directory where to save the Action Items documents
            
        Returns:
            Tuple containing paths to the JSON and Markdown task files
        """
        # Use provided output directory or default
        output_dir = output_dir or self.output_dir
        
        # Ensure we have the PRD content
        if not self.generated_prd_content:
            raise ValueError("PRD content not available. PRD must be generated before action items.")
        
        # Initialize action plan
        action_plan = None
        
        # Try to generate action items using LLM with the PRD
        try:
            print_info("Generating action items from PRD...")
            action_plan = self._generate_action_items_with_llm()
        except Exception as e:
            logger.error(f"Failed to generate action items with primary method: {e}")
            
            # Try once more with a simpler approach
            try:
                print_info("Retrying with alternative prompt...")
                action_plan = self._retry_action_item_generation()
            except Exception as retry_e:
                # If all LLM methods fail, raise an error - we don't fall back to init doc
                error_msg = f"All attempts to generate action items from PRD failed: {retry_e}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
        
        # Save the action plan as JSON
        tasks_json_path = os.path.join(output_dir, "cursor-rules-tasks.json")
        action_plan.save_to_file(tasks_json_path)
        
        # Save the action plan as Markdown
        tasks_md_path = os.path.join(output_dir, "cursor-rules-tasks.md")
        self._save_action_plan_as_markdown(tasks_md_path, action_plan)
        
        return tasks_json_path, tasks_md_path
    
    def _extract_json_from_response(self, response: str) -> str:
        """
        Extract valid JSON from an LLM response, handling various formatting issues.
        
        Args:
            response: Raw LLM response text
            
        Returns:
            Cleaned JSON string
        """
        # Try to extract JSON using regex patterns (looking for square brackets or curly braces)
        json_match = re.search(r'(\[[\s\S]*\]|\{[\s\S]*\})', response)
        
        if not json_match:
            logger.error(f"No JSON found in response: {response[:100]}...")
            raise ValueError("LLM response did not contain valid JSON")
        
        # Extract the JSON string
        json_str = json_match.group(1).strip()
        
        # Try to parse it to validate
        try:
            parsed = json.loads(json_str)
            return json.dumps(parsed, indent=2)  # Return properly formatted JSON
        except json.JSONDecodeError as e:
            # Try to repair common JSON issues
            logger.warning(f"Initial JSON parsing failed: {e}")
            
            # Fix unquoted keys
            fixed_json = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', json_str)
            # Fix single quotes
            fixed_json = fixed_json.replace("'", '"')
            # Fix trailing commas
            fixed_json = re.sub(r',\s*([\]}])', r'\1', fixed_json)
            
            try:
                parsed = json.loads(fixed_json)
                logger.info("Successfully repaired JSON")
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                logger.error("Could not repair JSON")
                raise ValueError(f"LLM generated invalid JSON that could not be repaired")