"""
Manages the starting and completing of development phases, 
including generating phase-specific plans and AI focus rules.
"""

import os
import re
import json
import time
import logging
from typing import Optional, Tuple, Dict, Any, List

# Assuming these modules exist and provide necessary functionality
from .llm_connector import LLMConnector, LLMRequest, LLMProvider 
from .terminal_utils import print_error, print_warning, print_info, print_success
# We might need to import ActionPlan/parsing logic if we manipulate the structure deeply
# from .task_parser import extract_tasks_from_markdown
# from .task_tracker import ActionPlan

logger = logging.getLogger(__name__)

# Default paths (consider making these configurable or passed in)
DEFAULT_DOCS_DIR = "documentation"
DEFAULT_RULES_DIR = ".cursor/rules"
DEFAULT_STATE_FILE = ".cursor/phase_state.json"
DEFAULT_ACTION_ITEMS_MD = os.path.join(DEFAULT_DOCS_DIR, "action_items.md")
DEFAULT_PRD = os.path.join(DEFAULT_DOCS_DIR, "product_requirements.md")
DEFAULT_DEV_LOG = os.path.join(DEFAULT_DOCS_DIR, "development_log.md")
CURRENT_PHASE_RULE = os.path.join(DEFAULT_RULES_DIR, "Current_Phase_Focus.mdc")


class PhaseManager:
    """Handles logic for starting and completing development phases."""

    def __init__(self, project_dir: str = "."):
        self.project_dir = os.path.abspath(project_dir)
        self.docs_dir = os.path.join(self.project_dir, DEFAULT_DOCS_DIR)
        self.rules_dir = os.path.join(self.project_dir, DEFAULT_RULES_DIR)
        self.state_file = os.path.join(self.project_dir, DEFAULT_STATE_FILE)
        self.action_items_path = os.path.join(self.project_dir, DEFAULT_ACTION_ITEMS_MD)
        self.prd_path = os.path.join(self.project_dir, DEFAULT_PRD)
        self.dev_log_path = os.path.join(self.project_dir, DEFAULT_DEV_LOG)
        self.current_phase_rule_path = os.path.join(self.project_dir, CURRENT_PHASE_RULE)
        
        self.state = self._load_state()
        self.llm_connector = LLMConnector()
        # Determine best available provider (could be passed in or configured)
        self.llm_provider = self._determine_best_provider()

        # Ensure directories exist
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.rules_dir, exist_ok=True)

    def _determine_best_provider(self) -> Optional[LLMProvider]:
        """Determine the best available LLM provider."""
        available = self.llm_connector.list_available_providers()
        if available:
            # Simple heuristic: prefer OpenAI > Anthropic > Others if available
            if LLMProvider.OPENAI in available: return LLMProvider.OPENAI
            if LLMProvider.ANTHROPIC in available: return LLMProvider.ANTHROPIC
            return available[0]
        return None

    def _load_state(self) -> Dict[str, Any]:
        """Load the current phase state from JSON file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                logger.warning(f"Could not load phase state from {self.state_file}: {e}")
        return {"current_phase": None} # Default state

    def _save_state(self) -> None:
        """Save the current phase state to JSON file."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except IOError as e:
            logger.error(f"Could not save phase state to {self.state_file}: {e}")

    def get_safe_phasename(self, phase_title: str) -> str:
         """Create a filesystem-safe name from a phase title."""
         # Remove the checkbox marker if present
         name = phase_title.replace('[ ]', '').replace('[x]', '').strip()
         # Attempt to remove common prefixes like "Phase X - " using regex
         name = re.sub(r"^[Pp]hase\s+\d+\s*[:\-]?\s*", "", name).strip()
         # Replace spaces and invalid chars with underscore
         name = re.sub(r'[^\w-]+', '_', name) 
         # Limit length
         return name[:50] 

    def _find_phase_in_markdown(self, phase_identifier: str) -> Optional[Tuple[str, str]]:
        """
        Finds a phase section in action_items.md based on the identifier (exact title text)
        and extracts its full title line and content block.

        Args:
            phase_identifier: The exact title text of the phase (e.g., "Project Setup and Environment Configuration").

        Returns:
            A tuple (full_title_line, phase_content) if found, otherwise None.
        """
        logger.debug(f"Attempting to find phase '{phase_identifier}' in {self.action_items_path}")
        if not os.path.exists(self.action_items_path):
            logger.error(f"Action items file not found: {self.action_items_path}")
            return None

        try:
            with open(self.action_items_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Regex Explanation:
            # (^##\s*\[ ?x? \]\s*   # Start of line (^) followed by '##', whitespace, '[ ]' or '[x]', whitespace
            #  {phase_title_escaped} # The phase title provided (escaped for regex safety)
            #  \s*$)               # Optional whitespace until the end of the line ($)
            # Capture this whole title line in group 1.
            # (\n.*?)             # Capture the content (group 2) - non-greedily match any char including newlines...
            # (?=\n##\s*\[ ?x? \]|\Z) # ...until it sees the start of the next phase heading OR the end of the string (\Z).
            phase_title_escaped = re.escape(phase_identifier)
            pattern = re.compile(
                r"(^##\s*\[ ?x? \]\s*" + phase_title_escaped + r"\s*$)(\n.*?)", 
                re.MULTILINE | re.DOTALL
            )

            match = pattern.search(content)

            if not match:
                logger.warning(f"Could not find phase section matching title '{phase_identifier}' in {self.action_items_path}.")
                return None

            full_title_line = match.group(1).strip()
            
            # To get content *only* for this phase, search from end of title line
            content_start_pos = match.end(1) 
            # Find the start of the *next* phase heading AFTER the current one
            next_phase_heading_match = re.search(r"^##\s*\[ ?x? \]", content[content_start_pos:], re.MULTILINE)

            if next_phase_heading_match:
                # If another phase heading is found, capture content up to it
                content_end_pos = content_start_pos + next_phase_heading_match.start()
                phase_content = content[content_start_pos:content_end_pos]
            else:
                # If no next phase heading, capture content to the end of the file
                phase_content = content[content_start_pos:]

            phase_content = phase_content.strip() # Clean up whitespace

            logger.info(f"Successfully found phase section for '{phase_identifier}'")
            return full_title_line, phase_content

        except IOError as e:
            logger.error(f"Error reading action items file {self.action_items_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error finding phase in markdown: {e}")
            logger.exception(e) # Log stack trace for unexpected errors
            return None

    def start_phase(self, phase_identifier: str) -> None:
        """Initiates a development phase."""
        if self.state.get("current_phase"):
            raise ValueError(f"Phase '{self.state['current_phase']}' is already active. Complete it first.")

        if not self.llm_provider:
            raise RuntimeError("No suitable LLM provider configured or available.")
        
        # 1. Find Phase Content in action_items.md
        phase_info = self._find_phase_in_markdown(phase_identifier)
        if not phase_info:
            raise ValueError(f"Phase '{phase_identifier}' not found in {self.action_items_path}.")
        full_phase_title, phase_tasks_content = phase_info
        
        # Extract clean title for state etc.
        clean_phase_title = phase_identifier # Assume identifier is the clean title for now

        # 2. LLM Call 1: Generate Implementation Plan
        print_info("Generating detailed implementation plan using LLM...")
        plan_filename = f"Phase_{self.get_safe_phasename(clean_phase_title)}_Implementation_Plan.md"
        plan_path = os.path.join(self.docs_dir, plan_filename)
        
        try:
            # Read PRD content
            with open(self.prd_path, 'r', encoding='utf-8') as f:
                prd_content = f.read()
        except IOError as e:
            raise FileNotFoundError(f"Could not read PRD file at {self.prd_path}: {e}") from e

        plan_system_prompt = """
        You are a senior software engineer creating a detailed implementation plan.
        Based on the provided phase tasks and the overall project PRD, break down the work into concrete steps.
        Consider potential challenges, testing needs, and documentation required for *this specific phase*.
        Output the plan in detailed Markdown format.
        """
        plan_user_prompt = f"""
        Project Phase: {clean_phase_title}

        Tasks for this Phase (from action_items.md):
        --- TASKS START ---
        {phase_tasks_content}
        --- TASKS END ---

        Overall Project PRD:
        --- PRD START ---
        {prd_content[:5000]}... 
        --- PRD END ---

        Generate the detailed implementation plan for completing ONLY this phase.
        """

        try:
            request = LLMRequest(
                prompt=plan_user_prompt,
                system_message=plan_system_prompt,
                provider=self.llm_provider,
                max_tokens=4000 # Allow longer plan
            )
            response = self.llm_connector.request(request)
            implementation_plan_content = response.text.strip()
            
            if not implementation_plan_content:
                raise ValueError("LLM returned empty implementation plan.")

            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(implementation_plan_content)
            print_success(f"Saved implementation plan to: {plan_path}")

        except Exception as e:
            print_error(f"LLM failed to generate implementation plan: {e}")
            raise # Stop if plan generation fails

        # 3. LLM Call 2: Generate current_phase.mdc
        print_info("Generating AI focus rule (current_phase.mdc)...")
        
        rule_system_prompt = f"""
        You are creating a Cursor IDE rule file (.mdc) to guide an AI assistant.
        The project is now focused *exclusively* on the '{clean_phase_title}' phase.
        Generate the content for '.cursor/rules/Current_Phase_Focus.mdc'.
        It MUST use the YAML front matter format with 'description', 'globs', and 'alwaysApply: true'.
        
        --- YAML Front Matter Requirements ---
        description: Provide a concise, single-line description stating the current phase and referencing the implementation plan. DO NOT use multi-line indicators like '|' or '>'.
        globs: ["**/*"] # Use this specific glob list.
        alwaysApply: true # Must be lowercase true.
        ---
        
        The markdown content after the closing '---' should provide STRATEGIC guidance to the AI on HOW to approach work during this phase (e.g., focus, priorities, what to avoid).
        Reference the implementation plan using '@file:{plan_filename}'.
        
        **IMPORTANT**: Your response MUST start *exactly* with the opening --- line of the YAML front matter and contain ONLY the valid .mdc content. Do NOT include any introduction, explanation, or conversational text before or after the .mdc content.
        """
        rule_user_prompt = f"""
        Current Phase: {clean_phase_title}
        Implementation Plan Filename: {plan_filename} 

        Project PRD Summary (for context):
        {prd_content[:1000]}...

        Implementation Plan Content (for context):
        {implementation_plan_content[:2000]}...

        Generate the '.cursor/rules/Current_Phase_Focus.mdc' file content now. Ensure the response starts *exactly* with --- and contains ONLY the file content.
        """

        try:
            request = LLMRequest(
                prompt=rule_user_prompt,
                system_message=rule_system_prompt,
                provider=self.llm_provider,
                max_tokens=1500 
            )
            response = self.llm_connector.request(request)
            rule_content = response.text.strip()

            # --- Add Cleanup Step ---
            # Try to find the start of the YAML block if there's leading text
            yaml_start_index = rule_content.find("---")
            if yaml_start_index > 0: # If --- is not at the very beginning
                logger.warning("LLM response had leading text before YAML front matter. Attempting cleanup.")
                rule_content = rule_content[yaml_start_index:]
            # --- End Cleanup Step ---

            if not rule_content or not rule_content.startswith('---'):
                 raise ValueError("LLM returned invalid content for current_phase rule (after cleanup).")

            # Basic validation
            if not re.search(r"^---\s*\ndescription:.*?\nglobs:.*?\nalwaysApply:\s*true\s*\n---\s*\n#", rule_content, re.DOTALL | re.IGNORECASE):
                 print_warning("Generated current_phase.mdc content may have formatting issues.")

            with open(self.current_phase_rule_path, 'w', encoding='utf-8') as f:
                f.write(rule_content)
            print_success(f"Saved AI focus rule to: {self.current_phase_rule_path}")

        except Exception as e:
            print_error(f"LLM failed to generate current_phase rule: {e}")
            # Proceeding without the rule might be acceptable, log warning
            print_warning("Could not create phase-specific AI focus rule.")


        # 4. Update State
        self.state["current_phase"] = clean_phase_title
        self.state["current_phase_start_time"] = time.time()
        self._save_state()
        logger.info(f"Updated state: current phase is now '{clean_phase_title}'")


    def _update_checkboxes_in_markdown(self, phase_identifier: str) -> bool:
        """
        Finds a phase section in action_items.md and marks all its tasks/subtasks
        checkboxes (`- [ ]`, `- [~]`) as complete (`- [x]`).

        Args:
            phase_identifier: The exact title text of the phase.

        Returns:
            True if the file was successfully read and modified, False otherwise.
        """
        logger.debug(f"Attempting to mark checkboxes complete for phase '{phase_identifier}' in {self.action_items_path}")
        if not os.path.exists(self.action_items_path):
            logger.error(f"Action items file not found: {self.action_items_path}")
            return False

        try:
            with open(self.action_items_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Regex to find the specific phase block (similar to _find_phase_in_markdown)
            phase_title_escaped = re.escape(phase_identifier)
            pattern = re.compile(
                r"(^##\\s*\\[ ?x? \\]\\s*" + phase_title_escaped + r"\\s*$)(\\n.*?)(?=\\n##\\s*\\[ ?x? \\]|\Z)",
                re.MULTILINE | re.DOTALL
            )
            match = pattern.search(content)

            if not match:
                logger.warning(f"Could not find phase section '{phase_identifier}' to update checkboxes.")
                return False # Indicate failure to find section
            
            # Extract the start and end positions of the phase content (excluding the title line)
            content_start_pos = match.end(1)
            content_end_pos = match.end(0) # End of the entire matched block
            phase_block_content = content[content_start_pos:content_end_pos]

            # Use re.sub to replace incomplete checkboxes within this block only
            # Pattern: Start of line (^), optional whitespace (\s*), hyphen (-), whitespace (\s*), 
            #          literal '[ ]', whitespace (\s*)
            # Replacement: Group 1 (indentation + hyphen + space) + '[x]' + group 2 (rest of line)
            checkbox_pattern = re.compile(r"(^\s*-\s*)\[ \](\s*.*)", re.MULTILINE)
            updated_phase_block = checkbox_pattern.sub(r"\1[x]\2", phase_block_content)

            # Construct the new full content
            new_content = content[:content_start_pos] + updated_phase_block + content[content_end_pos:]

            # Write the modified content back to the file
            with open(self.action_items_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.info(f"Updated checkboxes to complete for phase '{phase_identifier}'.")
            return True # Indicate success

        except IOError as e:
            logger.error(f"Error reading/writing action items file {self.action_items_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating checkboxes: {e}")
            logger.exception(e)
            return False

    def _append_dev_log(self, phase_identifier: str, completed_tasks_titles: List[str], implementation_plan_summary: str) -> bool:
        """Appends a phase completion entry to the development log."""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"\n## Phase Completed: {phase_identifier} - {timestamp}\n"
            
            # Add summary of completed tasks
            if completed_tasks_titles:
                 log_entry += "\n**Summary of Completed Tasks (from action_items.md):**\n"
                 for title in completed_tasks_titles:
                      log_entry += f"- {title}\n"
            else:
                 log_entry += "\n(Could not extract completed task titles from action_items.md)\n"
            
            # Add reference to implementation plan
            log_entry += f"\n**Implementation Plan Reference:**\n{implementation_plan_summary}\n"
            
            with open(self.dev_log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            logger.info("Appended phase completion details to development log.")
            return True
        except IOError as e:
            logger.error(f"Failed to append to development log {self.dev_log_path}: {e}")
            return False
        except Exception as e: # Catch other potential errors
             logger.error(f"Unexpected error appending to dev log: {e}")
             return False

    def complete_phase(self, phase_identifier: str) -> None:
        """Finalizes a development phase."""
        current_phase = self.state.get("current_phase")
        if not current_phase:
             print_warning("No phase is currently active according to state.")
             # Allow completion anyway? Or raise error? Let's allow for now.
             # raise ValueError("No active phase to complete.")
        elif current_phase != phase_identifier:
             print_warning(f"Warning: Completing phase '{phase_identifier}' but active phase in state is '{current_phase}'.")
             # Proceed with completing the specified phase anyway

        # 1. Update action_items.md checkboxes
        update_success = self._update_checkboxes_in_markdown(phase_identifier)
        if not update_success:
             print_warning("Could not automatically update checkboxes in action_items.md. Please check manually.")
             
        # 2. Extract completed task titles for logging
        completed_tasks_titles = []
        implementation_plan_summary = "(Implementation plan not found or unreadable)"
        plan_filename = f"Phase_{self.get_safe_phasename(phase_identifier)}_Implementation_Plan.md"
        plan_path = os.path.join(self.docs_dir, plan_filename)

        try:
            # Re-read action items to get titles of now-checked items
            phase_title_line, phase_content_block = self._find_phase_in_markdown(phase_identifier) or (None, None)
            if phase_content_block:
                # Regex to find lines starting with '- [x]' and extract the title part (between **)
                task_title_pattern = re.compile(r"^\s*-\s*\[x\]\s*\*\*(.*?)\*\*.*", re.MULTILINE)
                matches = task_title_pattern.finditer(phase_content_block)
                completed_tasks_titles = [match.group(1).strip() for match in matches]
            
            # Read a summary from the implementation plan
            if os.path.exists(plan_path):
                with open(plan_path, 'r', encoding='utf-8') as f:
                    # Take first few lines as a summary hint
                    plan_lines = [f.readline() for _ in range(5)] 
                    implementation_plan_summary = "".join(plan_lines).strip() + "..."
        except Exception as e:
            logger.warning(f"Could not extract completed tasks or plan summary for logging: {e}")

        # 3. Update development_log.md (passing extracted info)
        self._append_dev_log(phase_identifier, completed_tasks_titles, implementation_plan_summary)

        # 4. Delete current_phase.mdc rule
        try:
            if os.path.exists(self.current_phase_rule_path):
                os.remove(self.current_phase_rule_path)
                print_info(f"Removed phase focus rule: {self.current_phase_rule_path}")
        except OSError as e:
            print_error(f"Could not remove phase focus rule {self.current_phase_rule_path}: {e}")

        # 5. Update State
        if self.state.get("current_phase") == phase_identifier:
            self.state["current_phase"] = None
            self.state["last_completed_phase"] = phase_identifier
            self.state.pop("current_phase_start_time", None) # Remove start time
            self._save_state()
            logger.info(f"Updated state: Phase '{phase_identifier}' completed.")
        else:
             logger.info(f"State not updated as completed phase '{phase_identifier}' did not match active phase '{current_phase}'.") 