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
from .terminal_utils import print_header, print_success, print_step, print_info, print_warning, print_error

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
        prd_path = None # Initialize prd_path
        try:
            prd_path = self._generate_prd(docs_dir)
            elapsed = time.time() - start_time
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Error during PRD generation ({elapsed:.1f}s): {e}")
            print_error(f"Fatal: Product Requirements Document generation failed. Cannot proceed. Error: {e}")
            return {} # Stop execution

        # Check if PRD generation was successful (prd_path should not be None or empty and file must exist)
        if not prd_path or not os.path.exists(prd_path):
            # Even if no exception occurred, if path is invalid, stop.
            print_error(f"Fatal: Product Requirements Document generation failed (path: {prd_path}). Cannot proceed.")
            return {} # Stop execution
            
        generated_files["Product Requirements Document"] = prd_path
        print_success(f"Created Product Requirements Document ({elapsed:.1f}s)")
        
        # Read the generated PRD to use as input for all other document generation
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                self.generated_prd_content = f.read()
            # Add an explicit check for empty content after reading
            if not self.generated_prd_content:
                 raise ValueError("Generated PRD file is empty.")
        except Exception as e:
            logger.error(f"Failed to read generated PRD: {e}")
            print_error(f"Fatal: Failed to read generated PRD '{prd_path}'. Cannot proceed. Error: {e}")
            # Stop execution if PRD cannot be read
            return {} # Stop execution

        # --- Generation of other documents proceeds only if PRD is available ---
        
        # Generate the Technical Stack document with LLM enhancement based on the PRD
        print_step("Generating Technical Stack Document...")
        start_time = time.time()
        try:
            tech_stack_path = self._generate_tech_stack_doc(docs_dir)
            elapsed = time.time() - start_time
            generated_files["Technical Stack Document"] = tech_stack_path
            print_success(f"Created Technical Stack Document ({elapsed:.1f}s)")
        except Exception as e:
            elapsed = time.time() - start_time
            print_warning(f"Skipped Technical Stack Document generation due to error ({elapsed:.1f}s): {e}")
        
        # Generate the .cursorrules file with LLM enhancement based on the PRD
        print_step("Generating Cursor Rules Configuration...")
        start_time = time.time()
        try:
            cursorrules_paths = self._generate_cursorrules(cursor_dir)
            elapsed = time.time() - start_time
            if cursorrules_paths: # Check if list is not empty
                if len(cursorrules_paths) == 1:
                    generated_files["Cursor Rules"] = cursorrules_paths[0]
            else:
                for i, path in enumerate(cursorrules_paths):
                    rule_name = os.path.basename(path).replace('.mdc', '').replace('_', ' ').title()
                    generated_files[f"Cursor Rule: {rule_name}"] = path
                print_success(f"Created {len(cursorrules_paths)} Cursor Rules files ({elapsed:.1f}s)")
        except Exception as e:
            elapsed = time.time() - start_time
            print_warning(f"Skipped Cursor Rules generation due to error ({elapsed:.1f}s): {e}")
        
        # Generate the Action Items document based on the PRD
        print_step("Generating Action Items & Task List...")
        start_time = time.time()
        try:
            tasks_md_path, tasks_json_path = self._generate_action_items(docs_dir)
            elapsed = time.time() - start_time
            # Save paths if they are not None
            if tasks_md_path:
                generated_files["Action Items Markdown"] = tasks_md_path
            if tasks_json_path: # Check if JSON path was returned (might be None)
                generated_files["Action Items JSON"] = tasks_json_path
            
            # Only print success if at least the markdown was created
            if tasks_md_path:
                print_success(f"Created Action Items and Task List ({elapsed:.1f}s)")
            else: # Should not happen if exception handling is correct, but good safeguard
                print_warning(f"Action Items generation finished but no markdown file was created ({elapsed:.1f}s).")
        except Exception as e:
            elapsed = time.time() - start_time
            print_warning(f"Skipped Action Items generation due to error ({elapsed:.1f}s): {e}")
        
        # Determine which optional documents to generate based on PRD content analysis
        # Ensure this is called *after* attempting action item generation
        optional_docs = self._determine_optional_documents()
        
        # Generate any optional documents based on the PRD
        if optional_docs:
            print_step(f"Generating {len(optional_docs)} additional documents based on project needs...")
            for doc_type in optional_docs:
                doc_name = "Unknown Document"
                gen_func = None
                if doc_type == "app_flow":
                    doc_name = "App Flow Document"
                    # Check if method exists before assigning
                    if hasattr(self, '_generate_app_flow_doc'):
                        gen_func = self._generate_app_flow_doc
                elif doc_type == "frontend_guidelines":
                    doc_name = "Frontend Guidelines"
                    if hasattr(self, '_generate_frontend_guidelines'):
                        gen_func = self._generate_frontend_guidelines
                elif doc_type == "backend_structure":
                    doc_name = "Backend Structure Document"
                    if hasattr(self, '_generate_backend_structure'):
                        gen_func = self._generate_backend_structure
                elif doc_type == "api_documentation":
                    doc_name = "API Documentation"
                    if hasattr(self, '_generate_api_documentation'):
                        gen_func = self._generate_api_documentation
                elif doc_type == "testing_guidelines":
                    doc_name = "Testing Guidelines"
                    if hasattr(self, '_generate_testing_guidelines'):
                        gen_func = self._generate_testing_guidelines

                if gen_func and doc_name != "Unknown Document":
                    start_time = time.time()
                    try:
                        doc_path = gen_func(docs_dir)
                        elapsed = time.time() - start_time
                        generated_files[doc_name] = doc_path
                        print_info(f"Created {doc_name} ({elapsed:.1f}s)")
                    except Exception as e:
                        elapsed = time.time() - start_time
                        print_warning(f"Skipped {doc_name} generation due to error ({elapsed:.1f}s): {e}")
                elif doc_type:
                    print_warning(f"Generation function for optional document type '{doc_type}' not found or not implemented.")

        # Create development log file (assuming this is essential and doesn't have fallback)
        print_step("Generating Development Log...")
        try:
            start_time = time.time()
            dev_log_path = self._create_development_log(docs_dir, generated_files)
            elapsed = time.time() - start_time
            # Check if dev_log_path is valid before adding
            if dev_log_path:
                generated_files["Development Log"] = dev_log_path
                print_success(f"Created Development Log ({elapsed:.1f}s)")
            else:
                print_warning(f"Development log creation failed or returned no path ({elapsed:.1f}s).")
        except Exception as e:
            elapsed = time.time() - start_time
            print_error(f"Failed to create Development Log ({elapsed:.1f}s): {e}")
        
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

                # Add check for empty response from LLM
                if not tech_content:
                    raise ValueError("LLM returned an empty response for Technical Stack Document.")
                
                # Write the Technical Stack document to a file
                tech_stack_path = os.path.join(output_dir, "technical_stack.md")
                with open(tech_stack_path, 'w', encoding='utf-8') as f:
                    f.write(tech_content)
                
                return tech_stack_path
                
            except Exception as e:
                # Log the error and re-raise to indicate failure
                logger.error(f"Failed to generate Technical Stack Document with LLM: {e}")
                raise RuntimeError(f"LLM failed to generate Technical Stack Document: {e}") from e

        # If no LLM is available, raise an error as we removed the fallback
        else:
            logger.warning("LLM provider not available, and fallback generation is disabled for Technical Stack Document.")
            raise RuntimeError("LLM provider not available, fallback disabled for Technical Stack Document.")
    
    def _generate_cursorrules(self, cursor_dir: str) -> List[str]:
        """
        Generate cursor rules files using multiple targeted LLM calls, 
        one for each determined rule category.
        
        Args:
            cursor_dir: Directory where to save cursor rules
            
        Returns:
            List of paths to the generated rule files, if successful.
        """
        import os
        import re
        import json
        import logging
        from pathlib import Path
        from .utils import save_modern_cursor_rules
        from .core import ProjectState, Component, ComponentStatus, ProjectPhase # Keep core imports if needed by other parts not shown
        
        rules_dir = os.path.join(cursor_dir, "rules")
        os.makedirs(rules_dir, exist_ok=True)
        generated_files = []
        
        # --- Helper to sanitize filenames (moved inside for encapsulation) --- 
        def sanitize_filename(title):
            # Replace spaces with underscores, remove invalid chars, limit length
            sanitized = title.replace(' ', '_')
            sanitized = re.sub(r'[^\w\-_.]', '', sanitized)
            return sanitized[:50] # Limit length

        # --- Determine Categories --- 
        categories_to_generate = [
            "General_Project_Guidelines",
            "Testing_Guidelines",
            "Security_Best_Practices",
            "Documentation_Standards"
        ]
        
        try:
            tech_stack = self._extract_tech_stack()
            if not tech_stack:
                 logger.warning("Could not extract tech stack. Tech-specific rules may be limited.")
                 tech_stack = {} # Ensure it's a dict

            # Add categories based on tech stack
            if tech_stack.get("language"):
                for lang in tech_stack["language"]:
                    lang_norm = lang.lower().replace('#', 'sharp').replace('+', 'plus')
                    categories_to_generate.append(f"{lang_norm.capitalize()}_Language_Rules")
            if tech_stack.get("backend"):
                 # Prioritize specific frameworks if mentioned
                 specific_backend = False
                 for framework in ["django", "flask", "node.js", "spring", "rails", "laravel", ".net"]:
                     if any(framework in tech.lower() for tech in tech_stack["backend"]):
                          categories_to_generate.append(f"{framework.capitalize()}_Backend_Rules")
                          specific_backend = True
                 if not specific_backend:
                      categories_to_generate.append("Generic_Backend_Rules")
            if tech_stack.get("frontend"):
                 specific_frontend = False
                 for framework in ["react", "angular", "vue", "svelte"]:
                     if any(framework in tech.lower() for tech in tech_stack["frontend"]):
                         categories_to_generate.append(f"{framework.capitalize()}_Frontend_Rules")
                         specific_frontend = True
                 if not specific_frontend:
                    categories_to_generate.append("Generic_Frontend_Rules")
            if tech_stack.get("database"):
                 # Could add DB-specific rules here if needed
                 categories_to_generate.append("Database_Guidelines")
            if tech_stack.get("tools"):
                 if any("docker" in tool.lower() for tool in tech_stack["tools"]):
                      categories_to_generate.append("DevOps_Docker_Rules")
                 # Could add other tool-specific rules
            
            # Remove duplicates just in case
            categories_to_generate = sorted(list(set(categories_to_generate)))
            logger.info(f"Determined rule categories to generate: {categories_to_generate}")
                
        except Exception as e:
             logger.error(f"Error determining rule categories: {e}. Proceeding with core categories only.")
             categories_to_generate = [
                 "General_Project_Guidelines", 
                 "Testing_Guidelines", 
                 "Security_Best_Practices", 
                 "Documentation_Standards"
             ]

        # --- Check if LLM is available before looping --- 
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        if not use_llm:
             logger.error("LLM provider not available. Cannot generate cursor rules.")
             raise RuntimeError("LLM provider not available, rule generation requires it.")

        # --- Get context needed for all prompts --- 
        prd_content = self._get_content_for_generation()
        extracted_tech_stack_str = json.dumps(tech_stack, indent=2)
        extracted_dir_structure_str = json.dumps(self._extract_directory_structure(), indent=2)
        
        # --- Loop Through Categories and Generate Rules --- 
        for category in categories_to_generate:
            logger.info(f"Generating rule for category: {category}")
            try:
                # --- Determine Rule Settings --- 
                always_apply_bool = (category == "General_Project_Guidelines")
                # Convert boolean to lowercase string for YAML
                always_apply_str = str(always_apply_bool).lower()
                
                # Suggest default globs based on category (LLM should refine)
                default_glob = "**/*"
                if "_Backend_Rules" in category: default_glob = "src/backend/**/*.py" # Adjust per actual lang
                if "_Frontend_Rules" in category: default_glob = "src/frontend/**/*.{js,jsx,ts,tsx}"
                if "Testing_" in category: default_glob = "tests/**/*.py" # Adjust per lang
                if "Database_" in category: default_glob = "src/db/**/*.py" # Adjust
                # More specific tech globs needed here based on category parsing
                
                # --- Craft Targeted Prompt --- 
                # Updated system prompt demanding YAML front matter
                system_message_template = f"""
                You are an expert at creating rules for Cursor IDE. Your task is to generate ONE SINGLE rule file (.mdc format) for the specified category: '{category}'.
                
                The project is currently in its FOUNDATION phase, focusing on setting up core structures and standards.
                
                The rule file MUST start with YAML front matter enclosed in --- markers, followed by the rule content starting with a # Title.
                The YAML front matter MUST contain 'description', 'globs', and 'alwaysApply'.
                
                YAML Front Matter Structure Example (NO quotes around description text, comma-separated globs, lowercase boolean):
                ---
                description: Semantic description text goes here, potentially multiple lines, mentioning FOUNDATION phase.
                globs: **/*.py, tests/**/*.py # Example comma-separated glob string
                alwaysApply: false # Use lowercase true or false
                ---
                
                Rule Content Structure (AFTER the closing ---):
                # <Rule Title matching the category '{category}'>
                
                ## <Section Heading 1>
                - Bullet point guidance...
                - More guidance...
                
                ### Good Example:
                ```<lang>
                // Good code snippet
                ```
                
                ### Bad Example:
                ```<lang>
                // Bad code snippet
                ```
                
                ## <Section Heading 2>
                - ...
                
                @file: <path/to/relevant/example/file2.ext>
                
                Focus on providing actionable, project-specific guidance for '{category}' during the FOUNDATION phase. Use the provided project context.
                Output ONLY the complete content of the .mdc file, starting with the opening --- and ending after the rule content.
                """ 
                
                # Updated user prompt reinforcing the new format
                user_prompt = f"""
                Generate the complete .mdc rule file content (including YAML front matter) for the category: {category}
                
                Project Context:
                Phase: FOUNDATION
                Always Apply Setting for this rule: {always_apply_str} # Use lowercase 'true' or 'false'
                Suggested Globs (refine based on context): ["{default_glob}"]
                
                PRD/Initialization Document Content:
                --- PRD START ---
                {prd_content[:3000]}...
                --- PRD END ---
                
                Detected Tech Stack:
                {extracted_tech_stack_str}
                
                Detected Directory Structure:
                {extracted_dir_structure_str}
                
                Remember to output ONLY the raw .mdc file content, starting with --- and including the YAML front matter (with alwaysApply as lowercase true/false), followed by the # Title and rule content.
                """

                # --- Execute Single LLM Call --- 
                request = LLMRequest(
                    prompt=user_prompt,
                    system_message=system_message_template, # No .format needed now
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=2000 # Adjust token limit as needed per rule
                )
                
                response = self.llm_connector.request(request)
                rule_content = response.text.strip()

                # --- Process & Validate Response --- 
                if not rule_content or not rule_content.startswith('---'):
                    raise ValueError("LLM response is empty or doesn't start with YAML front matter (---).")
                
                # Basic validation for YAML structure
                if not re.search(r"^---\s*\ndescription:.*?\nglobs:.*?\nalwaysApply:.*?\n---", rule_content, re.DOTALL | re.IGNORECASE):
                    logger.warning(f"LLM response for '{category}' might be missing required YAML fields or correct format.")
                    # Consider raising ValueError here if strict validation is needed

                # Check for title after YAML
                if '\n---\n#' not in rule_content:
                     logger.warning(f"LLM response for '{category}' might be missing the # Title after the YAML block.")
                     # Consider raising ValueError

                # --- Save Rule File --- 
                filename_base = sanitize_filename(category)
                rule_path = os.path.join(rules_dir, f"{filename_base}.mdc")
                
                write_successful = False
                try:
                    with open(rule_path, 'w', encoding='utf-8') as f:
                        f.write(rule_content) 
                    write_successful = True 
                    logger.info(f"Successfully wrote rule file content to: {rule_path}")
                except IOError as e:
                     logger.error(f"Failed to save rule file {rule_path}: {e}")
                
                if write_successful:
                    generated_files.append(rule_path)
                
            except Exception as e:
                # --- Handle Errors Gracefully (for this category) --- 
                logger.error(f"Failed to generate rule for category '{category}': {e}")
                # Continue to the next category

        if not generated_files:
             logger.warning("Rule generation completed, but no rule files were successfully created.")
        
        return generated_files
    
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

                if not content:
                    raise ValueError("LLM returned empty response for Frontend Guidelines.")
                
                # Write the document to a file
                file_path = os.path.join(output_dir, "frontend_guidelines.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return file_path
            
            except Exception as e:
                logger.error(f"Failed to generate Frontend Guidelines with LLM: {e}")
                raise RuntimeError(f"LLM failed to generate Frontend Guidelines: {e}") from e
        else:
            # No LLM available, and fallback is removed.
            logger.warning("LLM provider not available, and fallback generation is disabled for Frontend Guidelines.")
            raise RuntimeError("LLM provider not available, fallback disabled for Frontend Guidelines.")

    def _extract_section(self, section_title: str) -> Optional[str]:
        """Extract a specific section from the initialization content using regex."""
        # Use a case-insensitive search
        pattern = re.compile(r'^#{1,3}\s+' + re.escape(section_title) + r'\s*\n(.*?)(?=^#|\Z)', 
                             re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = pattern.search(self.init_content)
        if match:
            # Strip leading/trailing whitespace and return
            return match.group(1).strip()
        return None
    
    def _extract_tech_stack(self) -> Dict[str, List[str]]:
        """Extract technology stack details from the initialization content."""
        tech_stack = {
            "language": [],
            "backend": [],
            "frontend": [],
            "database": [],
            "libraries": [],
            "tools": []
        }
        
        # Try extracting from a dedicated tech stack section
        tech_section_content = self._extract_section("Technical Stack") or \
                               self._extract_section("Tech Stack") or \
                               self._extract_section("Technical Requirements")
        
        if tech_section_content:
            # Basic keyword matching within the section
            lines = tech_section_content.split('\n')
            current_category = None
            for line in lines:
                line_lower = line.lower()
                # Basic category detection
                if "language" in line_lower: current_category = "language"
                elif "backend" in line_lower: current_category = "backend"
                elif "frontend" in line_lower: current_category = "frontend"
                elif "database" in line_lower or "db" in line_lower: current_category = "database"
                elif "libraries" in line_lower or "frameworks" in line_lower: current_category = "libraries"
                elif "tools" in line_lower or "devops" in line_lower: current_category = "tools"
                
                # Extract items (assuming bullet points or simple lists)
                if line.strip().startswith( ('-', '*', '+') ):
                    item = line.strip()[1:].strip()
                    # Remove potential markdown formatting like `code`
                    item = re.sub(r'`([^`]+)`', r'\1', item).strip()
                    if item and current_category and item not in tech_stack[current_category]:
                         tech_stack[current_category].append(item)
                else:
                    # Fallback: Basic keyword search across the whole document (less reliable)
                    content_lower = self.init_content.lower()
                    common_tech = {
                        "language": ["python", "javascript", "typescript", "java", "go", "ruby", "php", "c#", "swift"],
                        "backend": ["node.js", "django", "flask", "spring", "rails", "laravel", ".net"],
                        "frontend": ["react", "angular", "vue", "svelte", "jquery", "html", "css", "tailwind"],
                        "database": ["postgresql", "mysql", "sqlite", "mongodb", "redis", "sql server"],
                        "tools": ["docker", "kubernetes", "git", "aws", "azure", "gcp", "jenkins"]
                    }
                    for category, keywords in common_tech.items():
                        for keyword in keywords:
                            if keyword in content_lower:
                                tech_stack[category].append(keyword.capitalize())
        
        # Clean up empty categories
        return {k: v for k, v in tech_stack.items() if v}
    
    def _extract_directory_structure(self) -> Dict[str, str]:
        """Extract or infer directory structure from the initialization content."""
        structure = {}
        dir_section = self._extract_section("Directory Structure") or \
                      self._extract_section("Project Structure")
        
        if dir_section:
            # Simple extraction from markdown lists or code blocks
            lines = dir_section.split('\n')
            for line in lines:
                 # Match lines like '- src/: Source code' or '`src/` - Source code'
                 match = re.match(r'^[\s\-*`]*([\w\./\-_]+)[`:]*\s*[-:]?\s*(.*)', line.strip())
                 if match:
                     dir_name, description = match.groups()
                     # Basic cleanup
                     dir_name = dir_name.strip('/')
                     if dir_name and dir_name != '.':
                        structure[dir_name] = description.strip() or "No description"
        
        # If no structure found, provide a basic default
        if not structure:
            structure = {
                "src": "Source code directory",
                "tests": "Tests directory",
                "docs": "Documentation directory"
            }
        return structure
    
    def _generate_action_items(self, output_dir: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate action items (tasks, phases) by sending the PRD and Tech Stack
        to an LLM and asking it to create a plan in Markdown format.
        
        Args:
            output_dir: Directory where to save the action items files.
        
        Returns:
            A tuple containing:
                - Path to the generated Markdown file (or None if failed)
                - Path to the generated JSON file (currently None, potentially future enhancement)
        """
        tasks_md_path = os.path.join(output_dir, "action_items.md")
        tasks_json_path = None # Not generating JSON directly from LLM in this version

        logger.info("Generating Action Items using LLM...")

        # --- Check LLM Availability ---
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        if not use_llm:
            logger.error("LLM provider not available. Cannot generate Action Items.")
            raise RuntimeError("LLM provider not available, Action Item generation requires it.")

        # --- Prepare Context for LLM ---
        try:
            # Get PRD Content (mandatory)
            prd_content = self._get_content_for_generation()
            if not prd_content:
                raise ValueError("Cannot generate Action Items: PRD content is missing or empty.")

            # Get Tech Stack Content (optional, try to read if generated)
            tech_stack_content = "Not available."
            # Determine the expected path based on how _generate_tech_stack_doc saves it
            tech_stack_doc_name = "technical_stack.md"
            # Use self.output_dir or the passed output_dir consistently
            # Assuming documents are saved in a sub-directory like 'documentation'
            docs_dir = os.path.dirname(tasks_md_path) # Infer docs dir from output path
            tech_stack_path = os.path.join(docs_dir, tech_stack_doc_name) 
            
            if os.path.exists(tech_stack_path):
                try:
                    with open(tech_stack_path, 'r', encoding='utf-8') as f:
                        tech_stack_content = f.read()
                    logger.info(f"Successfully read tech stack document: {tech_stack_path}")
                except Exception as e:
                    logger.warning(f"Could not read generated tech stack doc '{tech_stack_path}': {e}")
            else:
                 logger.warning(f"Tech stack document not found at {tech_stack_path}")
                
        except Exception as e:
            logger.error(f"Error preparing context for Action Items generation: {e}")
            raise RuntimeError(f"Failed to prepare context for Action Items: {e}") from e

        # --- Craft LLM Prompt ---
        system_message = """
        You are an expert project manager and technical lead. Your task is to analyze the provided Product Requirements Document (PRD) and Technical Stack document for a software project currently in its FOUNDATION phase.

        Based on these documents, create a structured action plan in Markdown format. The plan should include:
        1.  Logical phases (e.g., Setup, Backend Core, Frontend Basics, Testing Setup) appropriate for the FOUNDATION stage. Use level 2 Markdown headings PRECEEDED by a checkbox (`## [ ] Phase Title`) for phases.
        2.  Specific, actionable tasks within each phase. Use Markdown checkbox syntax (`- [ ] Task Title`) for tasks.
        3.  Break down complex tasks into smaller sub-tasks where appropriate. Use indented Markdown checkbox syntax (`  - [ ] Sub-task Title`) for sub-tasks.
        4.  Order the phases and tasks logically for building the project foundation.
        5.  Focus ONLY on tasks relevant to the FOUNDATION phase described in the context.

        Output ONLY the Markdown action plan, starting directly with the first `## [ ] Phase Title`. Do not include any preamble, introduction, or concluding remarks.
        """

        user_prompt = f"""
        Analyze the following documents and generate the Markdown action plan (using checkbox syntax `## [ ]` for phases and `- [ ]` for tasks) for the FOUNDATION phase.

        --- PRD START ---
        {prd_content}
        --- PRD END ---

        --- TECHNICAL STACK START ---
        {tech_stack_content}
        --- TECHNICAL STACK END ---

        Remember to output ONLY the structured Markdown action plan using checkbox syntax for phases and tasks.
        """

        # --- Execute LLM Call ---
        try:
            request = LLMRequest(
                prompt=user_prompt,
                system_message=system_message,
                provider=self.llm_provider,
                temperature=0.2, # Lower temp for more deterministic planning
                max_tokens=3000 # Allow for a detailed plan
            )
            
            response = self.llm_connector.request(request)
            markdown_plan = response.text.strip()

            if not markdown_plan or not markdown_plan.startswith("##"):
                logger.error(f"LLM response for action plan is empty or improperly formatted. Response: {markdown_plan[:200]}...")
                raise ValueError("LLM failed to return a valid Markdown action plan.")

            # --- Save Markdown File --- 
            with open(tasks_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_plan)
            logger.info(f"Successfully generated Action Items Markdown: {tasks_md_path}")

            # --- Attempt to Parse MD and Save JSON --- 
            tasks_json_path = None # Initialize as None
            try:
                # Dynamically import parser to avoid circular dependencies at top level
                from .task_parser import extract_tasks_from_markdown 
                parsed_action_plan = extract_tasks_from_markdown(markdown_plan)
                
                if parsed_action_plan and parsed_action_plan.phases:
                     # Construct JSON path
                     json_filename = os.path.splitext(os.path.basename(tasks_md_path))[0] + '.json'
                     tasks_json_path = os.path.join(output_dir, json_filename) 
                     
                     # Ensure ActionPlan has save_to_json method (should exist from previous step)
                     if hasattr(parsed_action_plan, 'save_to_json'):
                         parsed_action_plan.save_to_json(tasks_json_path)
                         logger.info(f"Successfully generated Action Items JSON: {tasks_json_path}")
                     else:
                         logger.error("Parsed ActionPlan object lacks save_to_json method.")
                         tasks_json_path = None # Reset path if save failed
                else:
                     logger.warning("Could not parse generated Markdown back into ActionPlan object for JSON saving.")
            except ImportError:
                 logger.warning("Could not import task_parser to save JSON action plan.")
            except Exception as parse_e:
                 logger.warning(f"Error parsing generated Markdown or saving JSON: {parse_e}")
                 tasks_json_path = None # Ensure path is None if parsing/saving fails

            # Return paths 
            return tasks_md_path, tasks_json_path # tasks_json_path might be None

        except Exception as e:
            logger.error(f"Failed during LLM call or saving for Action Items: {e}")
            raise RuntimeError(f"Failed to generate Action Items: {e}") from e

    # --- Add placeholder for determining optional docs ---
    def _determine_optional_documents(self) -> List[str]:
        """
        Analyze PRD content to determine which optional documents are needed.
        Placeholder implementation - checks for basic keywords.
        """
        optional_docs = []
        # Ensure content is available before checking
        prd_content = ""
        try:
            prd_content = self._get_content_for_generation().lower() # Use generated PRD
        except Exception as e:
             logger.warning(f"Could not get PRD content for optional doc check: {e}")
             return [] # Return empty list if content cannot be retrieved

        # Simple keyword checks (refine these based on expected PRD content)
        if "frontend" in prd_content or " ui " in prd_content or "user interface" in prd_content or " react " in prd_content or " vue " in prd_content:
            optional_docs.append("frontend_guidelines")
        if "backend" in prd_content or " api " in prd_content or " server " in prd_content or " database " in prd_content:
            optional_docs.append("backend_structure")
        if " api " in prd_content or "restful" in prd_content or "graphql" in prd_content:
            optional_docs.append("api_documentation")
        if " test " in prd_content or " testing " in prd_content or " quality " in prd_content:
            optional_docs.append("testing_guidelines")
        if " user flow" in prd_content or " application flow" in prd_content:
             optional_docs.append("app_flow")

        # Remove duplicates and return
        logger.info(f"Determined optional documents to generate: {optional_docs}")
        return sorted(list(set(optional_docs)))

    def _create_development_log(self, output_dir: str, generated_docs: Dict[str, str]) -> str:
        """
        Create a development log summarizing generated documents.
        """
        log_path = os.path.join(output_dir, "development_log.md")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        log_content = [
            f"# Development Log - {timestamp}",
            "",
            f"Project: {self.title}",
            f"Initialization Document: {os.path.basename(self.init_doc_path)}",
            "",
            "## Document Generation Summary",
            ""
        ]
        
        if generated_docs:
            log_content.append("The following documents were generated:")
            for name, path in sorted(generated_docs.items()):
                 # Make path relative to project root if possible for cleaner logs
                 try:
                     relative_path = os.path.relpath(path, os.path.dirname(output_dir))
                 except ValueError:
                     relative_path = path # Keep absolute if not relative to output base
                 log_content.append(f"- **{name}**: `{relative_path}`")
            log_content.append("")
        else:
            log_content.append("No documents were successfully generated in this run.")
            log_content.append("")

        log_content.append("## Next Steps")
        log_content.append("- Review the generated documents, particularly the Action Items and PRD.")
        log_content.append("- Begin setting up the project structure based on the guidelines.")
        log_content.append("- Start working on tasks outlined in `action_items.md`.")
        log_content.append("")
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(log_content))
            logger.info(f"Created Development Log: {log_path}")
            return log_path
        except IOError as e:
             logger.error(f"Failed to write development log to {log_path}: {e}")
             # Return None or raise error if log is critical
             return None 

    # --- Add implementation for API Documentation ---
    def _generate_api_documentation(self, output_dir: str) -> str:
        """Generate API Documentation using LLM if available."""
        logger.info("Attempting to generate API Documentation...")
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = f"""
                You are a technical writer specializing in API documentation.
                Analyze the provided project documentation (PRD) for the '{self.title}' project (currently in FOUNDATION phase).
                Identify potential API endpoints or core data structures mentioned or implied.
                Generate a *basic* API documentation structure in Markdown format, outlining potential resources, endpoints (with HTTP methods like GET, POST), and expected request/response structures (even if high-level).
                Focus on the foundational elements suitable for the initial phase.
                Output ONLY the markdown content for the API documentation.
                """
                
                prompt = f"""
                Based on the PRD below, generate a foundational API documentation structure in Markdown:
                
                --- PRD START ---
                {self._get_content_for_generation()}
                --- PRD END ---
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=3000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                if not content:
                    raise ValueError("LLM returned empty response for API Documentation.")
                
                file_path = os.path.join(output_dir, "api_documentation.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Generated API Documentation: {file_path}")
                return file_path
                
            except Exception as e:
                logger.error(f"Failed to generate API Documentation with LLM: {e}")
                raise RuntimeError(f"LLM failed to generate API Documentation: {e}") from e
        else:
            logger.warning("LLM provider not available, cannot generate API Documentation.")
            raise RuntimeError("LLM provider not available, fallback disabled for API Documentation.")

    # --- Add implementation for Backend Structure ---
    def _generate_backend_structure(self, output_dir: str) -> str:
        """Generate Backend Structure document using LLM if available."""
        logger.info("Attempting to generate Backend Structure document...")
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                # Add tech stack context if available
                tech_stack_content = "Tech stack info not readily available."
                tech_stack_path = os.path.join(output_dir, "technical_stack.md")
                if os.path.exists(tech_stack_path):
                    try:
                        with open(tech_stack_path, 'r', encoding='utf-8') as f:
                            tech_stack_content = f.read()
                    except Exception as e:
                        logger.warning(f"Could not read tech stack for backend structure doc: {e}")
                
                system_message = f"""
                You are a backend architect. Analyze the provided project documentation (PRD) and tech stack info for '{self.title}' (FOUNDATION phase).
                Generate a Markdown document outlining a recommended backend structure. Include:
                1.  Core modules/directories (e.g., models, controllers/views, services, database access).
                2.  Brief description of each module's responsibility.
                3.  How the detected backend technologies might fit into this structure.
                Focus on a clean, scalable foundation.
                Output ONLY the markdown content for the Backend Structure document.
                """
                
                prompt = f"""
                PRD:
                --- PRD START ---
                {self._get_content_for_generation()}
                --- PRD END ---
                
                Tech Stack:
                --- TECH STACK START ---
                {tech_stack_content}
                --- TECH STACK END ---
                
                Generate the Backend Structure document based on the above.
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=3000
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                if not content:
                    raise ValueError("LLM returned empty response for Backend Structure.")
                
                file_path = os.path.join(output_dir, "backend_structure.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Generated Backend Structure: {file_path}")
                return file_path
                
            except Exception as e:
                logger.error(f"Failed to generate Backend Structure with LLM: {e}")
                raise RuntimeError(f"LLM failed to generate Backend Structure: {e}") from e
        else:
            logger.warning("LLM provider not available, cannot generate Backend Structure.")
            raise RuntimeError("LLM provider not available, fallback disabled for Backend Structure.")

    # --- Add implementation for Testing Guidelines ---
    def _generate_testing_guidelines(self, output_dir: str) -> str:
        """Generate Testing Guidelines document using LLM if available."""
        logger.info("Attempting to generate Testing Guidelines document...")
        use_llm = self.llm_connector.is_provider_available(self.llm_provider)
        
        if use_llm:
            try:
                system_message = f"""
                You are a QA engineer and testing expert. Analyze the provided project documentation (PRD) for '{self.title}' (FOUNDATION phase).
                Generate a foundational Testing Guidelines document in Markdown. Include sections for:
                1.  Testing Philosophy (e.g., testing pyramid, priorities).
                2.  Types of Tests Planned (Unit, Integration, E2E - focus on initial setup).
                3.  Recommended Tools/Frameworks (based on tech stack if possible, otherwise suggest common ones).
                4.  Basic conventions for writing tests.
                Output ONLY the markdown content for the Testing Guidelines document.
                """
                
                prompt = f"""
                Based on the PRD below, generate foundational Testing Guidelines in Markdown:
                
                --- PRD START ---
                {self._get_content_for_generation()}
                --- PRD END ---
                """
                
                request = LLMRequest(
                    prompt=prompt,
                    system_message=system_message,
                    provider=self.llm_provider,
                    temperature=0.2,
                    max_tokens=2500
                )
                
                response = self.llm_connector.request(request)
                content = response.text.strip()
                
                if not content:
                    raise ValueError("LLM returned empty response for Testing Guidelines.")
                
                file_path = os.path.join(output_dir, "testing_guidelines.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Generated Testing Guidelines: {file_path}")
                return file_path
                
            except Exception as e:
                logger.error(f"Failed to generate Testing Guidelines with LLM: {e}")
                raise RuntimeError(f"LLM failed to generate Testing Guidelines: {e}") from e
        else:
            logger.warning("LLM provider not available, cannot generate Testing Guidelines.")
            raise RuntimeError("LLM provider not available, fallback disabled for Testing Guidelines.")