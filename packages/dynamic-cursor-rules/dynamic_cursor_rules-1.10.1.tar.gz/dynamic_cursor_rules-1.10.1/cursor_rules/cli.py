"""
Command-line interface for task management.
"""
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Any
import colorama
from colorama import Fore, Style, Back
import click

from .task_tracker import ActionPlan, Task, TaskStatus, Phase
from .task_parser import extract_tasks_from_markdown, parse_initialization_doc
from .core import RuleSet, ProjectPhase
from .utils import generate_cursorrules_file, save_cursorrules_file
from .llm_connector import LLMConnector, LLMProvider, LLMRequest, MultiLLMProcessor
from .terminal_utils import print_header, print_success, print_info, print_warning, print_error, print_step
from .phase_manager import PhaseManager

# Initialize colorama for cross-platform color support
colorama.init(autoreset=True)

# Define the CLI group
@click.group()
def cli():
    """Cursor Rules CLI - Tools for managing AI assistant instructions."""
    pass

DEFAULT_TASKS_FILE = "cursor-rules-tasks.json"
DEFAULT_TASKS_MD_FILE = "cursor-rules-tasks.md"
DEFAULT_CLAUDE_MODEL = "claude-3-7-sonnet-latest"  # Latest Claude model

def list_tasks(action_plan: ActionPlan, phase_filter: Optional[str] = None, 
               status_filter: Optional[str] = None, tag_filter: Optional[str] = None) -> None:
    """
    List tasks from an action plan with optional filtering.
    
    Args:
        action_plan: The action plan to list tasks from
        phase_filter: Optional phase title to filter by
        status_filter: Optional status to filter by
        tag_filter: Optional tag to filter by
    """
    # Filter phases if requested
    phases = action_plan.phases
    if phase_filter:
        phases = [p for p in phases if phase_filter.lower() in p.title.lower()]
        
    if not phases:
        print_warning("No phases found matching the filter.")
        return
    
    print_header(f"Project: {action_plan.title}")
    
    if phase_filter:
        print_info(f"Filtering by phase: {phase_filter}")
    if status_filter:
        print_info(f"Filtering by status: {status_filter}")
    if tag_filter:
        print_info(f"Filtering by tag: {tag_filter}")
    
    print()
    
    # Count tasks
    total_tasks = sum(len(p.tasks) for p in phases)
    total_completed = sum(
        sum(1 for t in p.tasks if t.status == TaskStatus.COMPLETED)
        for p in phases
    )
    
    # Display progress bar
    if total_tasks > 0:
        completion_percentage = int((total_completed / total_tasks) * 100)
        bar_length = 30
        filled_length = int(bar_length * total_completed // total_tasks)
        bar = f"{Fore.GREEN}{'█' * filled_length}{Fore.WHITE}{'░' * (bar_length - filled_length)}"
        print(f"{Style.BRIGHT}Overall Progress: {completion_percentage}% {Style.RESET_ALL}")
        print(f"{bar} {Fore.CYAN}{total_completed}/{total_tasks} tasks completed{Style.RESET_ALL}")
        print()
        
    # For each phase
    for phase in phases:
        print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} {phase.title} {Style.RESET_ALL}")
        
        if phase.description:
            print(f"{Fore.CYAN}{phase.description}{Style.RESET_ALL}\n")
            
        # Get tasks for this phase
        tasks = phase.tasks
        
        # Apply status filter if requested
        if status_filter:
            try:
                status = TaskStatus(status_filter.lower())
                tasks = [t for t in tasks if t.status == status]
            except ValueError:
                print_warning(f"Invalid status filter '{status_filter}'. Valid values are: "
                      f"{', '.join([s.value for s in TaskStatus])}")
                
        # Apply tag filter if requested
        if tag_filter:
            tasks = [t for t in tasks if tag_filter.lower() in [tag.lower() for tag in t.tags]]
            
        if not tasks:
            print_info("  No tasks found matching the filters.")
            continue
            
        # Print tasks
        for task in tasks:
            status_emoji = {
                TaskStatus.NOT_STARTED: "⭕",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.BLOCKED: "🚫"
            }.get(task.status, "⭕")
            
            status_color = {
                TaskStatus.NOT_STARTED: Fore.WHITE,
                TaskStatus.IN_PROGRESS: Fore.YELLOW,
                TaskStatus.COMPLETED: Fore.GREEN,
                TaskStatus.BLOCKED: Fore.RED
            }.get(task.status, Fore.WHITE)
            
            task_info = f"- {status_emoji} {status_color}{Style.BRIGHT}{task.title}{Style.RESET_ALL} (ID: `{Fore.CYAN}{task.id}{Style.RESET_ALL}`"
            
            if task.priority > 0:
                priority_colors = [Fore.BLUE, Fore.YELLOW, Fore.RED]
                priority_color = priority_colors[min(task.priority-1, 2)]
                task_info += f", Priority: {priority_color}{task.priority}{Style.RESET_ALL}"
                
            if task.effort > 0:
                effort_symbols = ["⚪", "⚪⚪", "⚪⚪⚪"]
                effort_display = effort_symbols[min(task.effort-1, 2)]
                task_info += f", Effort: {effort_display}"
                
            task_info += ")"
            
            print(task_info)
            
            if task.description:
                print(f"  - {Fore.CYAN}{task.description}{Style.RESET_ALL}")
                
            if task.dependencies:
                deps = ", ".join([f"`{Fore.MAGENTA}{dep}{Style.RESET_ALL}`" for dep in task.dependencies])
                print(f"  - {Fore.YELLOW}Dependencies:{Style.RESET_ALL} {deps}")
                
            if task.tags:
                tags = ", ".join([f"{Fore.BLUE}#{tag}{Style.RESET_ALL}" for tag in task.tags])
                print(f"  - {Fore.YELLOW}Tags:{Style.RESET_ALL} {tags}")
                
            # Print subtasks recursively
            if task.subtasks:
                _print_subtasks(task.subtasks, indent=2)
                
    print("\n")
    
def _print_subtasks(subtasks: List[Task], indent: int) -> None:
    """Helper function to print subtasks recursively."""
    for subtask in subtasks:
        status_emoji = {
            TaskStatus.NOT_STARTED: "⭕",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.BLOCKED: "🚫"
        }.get(subtask.status, "⭕")
        
        status_color = {
            TaskStatus.NOT_STARTED: Fore.WHITE,
            TaskStatus.IN_PROGRESS: Fore.YELLOW,
            TaskStatus.COMPLETED: Fore.GREEN,
            TaskStatus.BLOCKED: Fore.RED
        }.get(subtask.status, Fore.WHITE)
        
        indent_str = " " * indent
        subtask_info = f"{indent_str}- {status_emoji} {status_color}{subtask.title}{Style.RESET_ALL} (ID: `{Fore.CYAN}{subtask.id}{Style.RESET_ALL}`"
        
        if subtask.priority > 0:
            priority_colors = [Fore.BLUE, Fore.YELLOW, Fore.RED]
            priority_color = priority_colors[min(subtask.priority-1, 2)]
            subtask_info += f", Priority: {priority_color}{subtask.priority}{Style.RESET_ALL}"
            
        if subtask.effort > 0:
            effort_symbols = ["⚪", "⚪⚪", "⚪⚪⚪"]
            effort_display = effort_symbols[min(subtask.effort-1, 2)]
            subtask_info += f", Effort: {effort_display}"
            
        subtask_info += ")"
        
        print(subtask_info)
        
        if subtask.description:
            print(f"{indent_str}  - {Fore.CYAN}{subtask.description}{Style.RESET_ALL}")
            
        if subtask.dependencies:
            deps = ", ".join([f"`{Fore.MAGENTA}{dep}{Style.RESET_ALL}`" for dep in subtask.dependencies])
            print(f"{indent_str}  - {Fore.YELLOW}Dependencies:{Style.RESET_ALL} {deps}")
            
        if subtask.tags:
            tags = ", ".join([f"{Fore.BLUE}#{tag}{Style.RESET_ALL}" for tag in subtask.tags])
            print(f"{indent_str}  - {Fore.YELLOW}Tags:{Style.RESET_ALL} {tags}")
            
        # Recursively print nested subtasks
        if subtask.subtasks:
            _print_subtasks(subtask.subtasks, indent + 2)

def update_task_status(action_plan: ActionPlan, task_id: str, new_status: str) -> bool:
    """
    Update the status of a task in the action plan.
    
    Args:
        action_plan: The action plan containing the task
        task_id: The ID of the task to update
        new_status: The new status to set
        
    Returns:
        True if the task was found and updated, False otherwise
    """
    try:
        status = TaskStatus(new_status.lower())
    except ValueError:
        print(f"Error: Invalid status '{new_status}'. Valid values are: "
              f"{', '.join([s.value for s in TaskStatus])}")
        return False
        
    # Find the task
    task = action_plan.get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID '{task_id}' not found.")
        return False
        
    # Update the status
    task.status = status
    print(f"Task '{task.title}' status updated to {status.value}.")
    return True

def add_task(action_plan: ActionPlan, title: str, phase_id: Optional[str] = None,
             description: Optional[str] = None, priority: int = 0, 
             effort: int = 0, tags: Optional[List[str]] = None) -> Task:
    """
    Add a new task to the action plan.
    
    Args:
        action_plan: The action plan to add the task to
        title: The title of the new task
        phase_id: Optional ID of the phase to add the task to (defaults to first phase)
        description: Optional description for the task
        priority: Optional priority for the task (0-10)
        effort: Optional effort estimate for the task (0-10)
        tags: Optional list of tags for the task
        
    Returns:
        The newly created task
    """
    # Create the task
    task = Task(
        title=title,
        description=description,
        priority=priority,
        effort=effort,
        tags=tags or []
    )
    
    # Find the phase to add it to
    target_phase = None
    
    if phase_id:
        # Find phase by ID
        for phase in action_plan.phases:
            if phase.id == phase_id:
                target_phase = phase
                break
                
        if not target_phase:
            print(f"Warning: Phase with ID '{phase_id}' not found. Adding to first phase.")
    
    # Default to first phase if not specified or not found
    if not target_phase and action_plan.phases:
        target_phase = action_plan.phases[0]
    
    # Create a default phase if none exist
    if not target_phase:
        target_phase = Phase(title="Tasks")
        action_plan.add_phase(target_phase)
    
    # Add the task to the phase
    target_phase.add_task(task)
    
    print(f"Task '{task.title}' added with ID: {task.id}")
    return task

def add_subtask(action_plan: ActionPlan, parent_id: str, title: str,
                description: Optional[str] = None, priority: int = 0,
                effort: int = 0, tags: Optional[List[str]] = None) -> Optional[Task]:
    """
    Add a subtask to an existing task.
    
    Args:
        action_plan: The action plan containing the parent task
        parent_id: The ID of the parent task
        title: The title of the new subtask
        description: Optional description for the subtask
        priority: Optional priority for the subtask (0-10)
        effort: Optional effort estimate for the subtask (0-10)
        tags: Optional list of tags for the subtask
        
    Returns:
        The newly created subtask, or None if the parent task wasn't found
    """
    # Find the parent task
    parent_task = action_plan.get_task_by_id(parent_id)
    if not parent_task:
        print(f"Error: Parent task with ID '{parent_id}' not found.")
        return None
    
    # Create the subtask
    subtask = Task(
        title=title,
        description=description,
        priority=priority,
        effort=effort,
        tags=tags or []
    )
    
    # Add the subtask to the parent
    parent_task.add_subtask(subtask)
    
    print(f"Subtask '{subtask.title}' added to '{parent_task.title}' with ID: {subtask.id}")
    return subtask

def load_action_plan(file_path: str = DEFAULT_TASKS_FILE) -> ActionPlan:
    """
    Load an action plan from a file.
    
    Args:
        file_path: Path to the action plan file
        
    Returns:
        The loaded action plan, or a new one if the file wasn't found
    """
    try:
        return ActionPlan.load(file_path)
    except FileNotFoundError:
        print(f"No action plan found at {file_path}. Creating a new one.")
        return ActionPlan(title="Project Action Plan")

def save_action_plan(action_plan: ActionPlan, json_path: str = DEFAULT_TASKS_FILE,
                     md_path: str = DEFAULT_TASKS_MD_FILE) -> None:
    """
    Save an action plan to JSON and markdown files.
    
    Args:
        action_plan: The action plan to save
        json_path: Path for the JSON file
        md_path: Path for the markdown file
    """
    # Save JSON
    action_plan.save(json_path)
    print(f"Action plan saved to {json_path}")
    
    # Save markdown
    markdown = action_plan.to_markdown()
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"Action plan saved to {md_path}")

def sync_with_cursorrules(action_plan: ActionPlan, ruleset: RuleSet) -> None:
    """
    Synchronize the action plan with a ruleset.
    
    Args:
        action_plan: The action plan to synchronize
        ruleset: The ruleset to synchronize with
    """
    # Get all rule content as a single string
    rules_content = "\n".join([rule.content for rule in ruleset.rules])
    
    # Extract tasks from the rules content
    rules_plan = extract_tasks_from_markdown(rules_content)
    
    # Track new tasks
    new_tasks = []
    
    # Track existing task IDs
    existing_task_ids = [t.id for t in action_plan.get_all_tasks()]
    
    # Create a "Rules Tasks" phase if it doesn't exist
    rules_phase = None
    for phase in action_plan.phases:
        if phase.title.lower() == "rules tasks":
            rules_phase = phase
            break
            
    if not rules_phase:
        rules_phase = Phase(title="Rules Tasks", description="Tasks derived from rules")
        action_plan.add_phase(rules_phase)
    
    # Add tasks from rules to the plan
    for phase in rules_plan.phases:
        for task in phase.tasks:
            # Skip if a similar task already exists
            similar_exists = False
            for existing_task in action_plan.get_all_tasks():
                if existing_task.title.lower() == task.title.lower():
                    similar_exists = True
                    break
                    
            if not similar_exists:
                # Add the task to the rules phase
                rules_phase.add_task(task)
                new_tasks.append(task)
    
    # Report results
    if new_tasks:
        print(f"Added {len(new_tasks)} new tasks from rules:")
        for task in new_tasks:
            print(f"- {task.title} (ID: {task.id})")
    else:
        print("No new tasks added from rules.")

@cli.command('documents')
@click.argument(
    'doc_path',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True)
)
@click.option(
    '--output-dir', '-o',
    type=click.Path(file_okay=False, dir_okay=True),
    default='.',
    help='Directory to save generated documents.'
)
def generate_from_doc(doc_path: str, output_dir: str) -> None:
    """
    Generate project documents from an initialization markdown file.
    
    DOC_PATH: Path to the initialization markdown document.
    """
    try:
        # Import here to avoid circular imports
        from cursor_rules.document_generator import DocumentGenerator
        
        print(f"Generating documents from '{doc_path}'...")
        
        # Create a document generator
        generator = DocumentGenerator(doc_path, output_dir)
        
        # Generate all documents
        generated_files = generator.generate_all_documents()
        
        print("\nGenerated files:")
        for doc_name, file_path in generated_files.items():
            print(f"- {doc_name}: {file_path}")
        
        print("\nDocument generation complete!")
        
    except Exception as e:
        print(f"Error generating documents: {e}")
        sys.exit(1)

def handle_llm_list():
    """Handle the llm list command."""
    try:
        # Create an LLM connector
        llm_connector = LLMConnector()
        
        # List available providers
        providers = llm_connector.list_available_providers()
        
        if not providers:
            print("No LLM providers are available")
            print("Use 'cursor-rules llm config' to configure API keys")
            return
        
        # Print the providers
        print("Available LLM providers:")
        for provider in providers:
            print(f"  - {provider.value}")
            
    except Exception as e:
        print(f"Failed to list LLM providers: {e}")

def handle_llm_config(provider_name: str, api_key: str):
    """Handle the llm config command."""
    try:
        # Map provider name to enum
        try:
            provider = LLMProvider(provider_name.lower())
        except ValueError:
            print(f"Invalid provider: {provider_name}. Must be one of: "
                  f"{', '.join(p.value for p in LLMProvider if p != LLMProvider.MOCK)}")
            return
        
        # Create an LLM connector
        llm_connector = LLMConnector()
        
        # Set the API key
        llm_connector.set_api_key(provider, api_key)
        
        print(f"Configured API key for {provider.value}")
        
    except Exception as e:
        print(f"Failed to configure LLM provider: {e}")

def handle_llm_test(provider_name: str, query: str):
    """Handle the llm test command."""
    try:
        # Create an LLM processor
        llm_processor = MultiLLMProcessor()
        
        # Create a request
        request = LLMRequest(
            prompt=query,
            system_message="You are a helpful assistant."
        )
        
        # Set model for Claude to latest version
        if provider_name.lower() == "anthropic":
            request.model = DEFAULT_CLAUDE_MODEL
        
        # Process the request
        if provider_name.lower() == "all":
            # Use all available providers
            responses = llm_processor.process_with_all_available(request)
        else:
            # Use a specific provider
            try:
                provider = LLMProvider(provider_name.lower())
            except ValueError:
                print(f"Invalid provider: {provider_name}. Must be one of: "
                       f"{', '.join(p.value for p in LLMProvider)}")
                return
                
            responses = llm_processor.process_with_specific(request, [provider])
        
        if not responses:
            print("No responses received. Make sure your API keys are configured correctly.")
            return
        
        # Print the responses
        for response in responses:
            print(f"\n===== Response from {response.provider.value} ({response.model}) =====")
            print(f"Time: {response.elapsed_time:.2f}s")
            print(f"Tokens: {response.total_tokens} ({response.prompt_tokens} prompt, {response.completion_tokens} completion)")
            print(f"\n{response.text}")
        
    except Exception as e:
        print(f"Failed to test LLM providers: {e}")

@cli.command()
@click.option(
    '--project-dir', '-p',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default='.',
    help="Project directory to analyze"
)
@click.option(
    '--force', '-f',
    is_flag=True,
    help="Force regeneration of rules even if no changes detected"
)
@click.option(
    '--phase',
    type=click.Choice(['setup', 'foundation', 'feature_development', 'refinement', 'maintenance']),
    help="Set the current project phase for rule generation"
)
@click.option(
    '--features',
    help="Comma-separated list of active features being developed"
)
def update_rules(project_dir, force, phase, features):
    """
    Update cursor rules based on project changes.
    
    This command analyzes the current project state and generates or updates
    cursor rules to match the current development phase and focus.
    """
    try:
        from .dynamic_rules import DynamicRuleManager
        from .core import ProjectPhase
        
        click.echo(click.style("Analyzing project state...", fg="cyan"))
        
        # Initialize the rule manager
        rule_manager = DynamicRuleManager(project_dir)
        
        # Update project state if options specified
        if phase:
            click.echo(f"Setting project phase to: {phase}")
            rule_manager.update_project_state(phase=ProjectPhase(phase))
        
        if features:
            feature_list = [f.strip() for f in features.split(',')]
            click.echo(f"Setting active features to: {', '.join(feature_list)}")
            rule_manager.update_project_state(active_features=feature_list)
        
        # Check for changes
        if not force:
            click.echo("Checking for project changes...")
            changes_detected = rule_manager.detect_project_changes()
            if not changes_detected:
                click.echo(click.style("No significant changes detected. Use --force to regenerate rules anyway.", fg="yellow"))
                return
        
        # Generate rules
        click.echo(click.style("Generating dynamic cursor rules...", fg="cyan"))
        generated_files = rule_manager.generate_dynamic_rules(force_regenerate=force)
        
        if generated_files:
            click.echo(click.style(f"Successfully generated {len(generated_files)} rule files:", fg="green"))
            for file_path in generated_files:
                click.echo(f" - {os.path.basename(file_path)}")
        else:
            click.echo(click.style("No rules were generated.", fg="yellow"))
        
    except ImportError as e:
        click.echo(click.style(f"Error: Could not import required modules: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))

# --- Add this LLM group and its commands ---

@cli.group()
def llm():
    """Commands for configuring and testing LLM providers."""
    pass

@llm.command()
@click.option(
    '--provider',
    required=True,
    type=click.Choice([p.value for p in LLMProvider], case_sensitive=False),
    help="LLM provider to configure (e.g., 'openai', 'anthropic')"
)
@click.option(
    '--api-key',
    required=True,
    prompt="API Key",
    hide_input=True,
    help="API key for the selected provider"
)
def config(provider, api_key):
    """Configure API key for a specific LLM provider."""
    try:
        connector = LLMConnector()
        provider_enum = LLMProvider(provider.lower())
        connector.set_api_key(provider_enum, api_key)
        click.echo(click.style(f"API key for {provider_enum.value} configured successfully.", fg="green"))
    except ValueError as e:
        print_error(f"Invalid provider value: {e}")
    except Exception as e:
        print_error(f"Failed to configure API key: {e}")

@llm.command()
def test():
    """Test connectivity and response from configured LLM providers."""
    try:
        connector = LLMConnector()
        available_providers = connector.list_available_providers()

        if not available_providers:
            print_warning("No LLM providers seem to be configured or available. Use 'llm config' first.")
            return

        click.echo(click.style(f"Testing {len(available_providers)} available provider(s)...", fg="cyan"))

        processor = MultiLLMProcessor()
        request = LLMRequest(
            prompt="Respond with only the word 'test'.",
            max_tokens=5,
            temperature=0.1
        )

        # Create requests for all available providers
        requests = {provider: request for provider in available_providers}

        responses = processor.process_requests(requests)

        if not responses:
            print_warning("No responses received. Check API keys and network connection.")
            return

        click.echo(click.style("\n--- Test Results ---", bold=True))
        for provider, response in responses.items():
            status = click.style("SUCCESS", fg="green") if response.text.strip().lower() == "test" else click.style("FAILED", fg="red")
            click.echo(f"{provider.value}: {status} ({response.elapsed_time:.2f}s)")
            if status == click.style("FAILED", fg="red"):
                 click.echo(f"  Expected: 'test', Got: '{response.text.strip()}'")

    except Exception as e:
        print_error(f"Failed to test LLM providers: {e}")

# --- End of LLM commands ---

# --- Add new Phase Management Commands ---

@cli.command('start-phase')
@click.argument('phase_identifier', type=str)
@click.option(
    '--project-dir', '-d', 
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True), 
    default='.', 
    help="Root directory of the project."
)
def start_phase_command(phase_identifier, project_dir):
    """Starts a specific dev phase: generates plan & updates AI focus rule."""
    click.echo(f"Attempting to start phase: {phase_identifier} in project: {project_dir}")
    try:
        manager = PhaseManager(project_dir=project_dir)
        manager.start_phase(phase_identifier)
        safe_name = manager.get_safe_phasename(phase_identifier)
        click.echo(click.style(f"Successfully started phase '{phase_identifier}'.", fg="green"))
        click.echo(f"- Detailed plan: documentation/Phase_{safe_name}_Implementation_Plan.md")
        click.echo(f"- AI focus rule: .cursor/rules/Current_Phase_Focus.mdc")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print_error(f"Error starting phase '{phase_identifier}': {e}")
    except Exception as e:
        # Catch unexpected errors
        print_error(f"An unexpected error occurred during start-phase: {e}")
        logger.exception("Unexpected error in start-phase command") # Log stack trace

@cli.command('complete-phase')
@click.argument('phase_identifier', type=str)
@click.option(
    '--project-dir', '-d',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default='.',
    help="Root directory of the project."
)
def complete_phase_command(phase_identifier, project_dir):
    """Completes a specific dev phase: updates action items and logs."""
    click.echo(f"Attempting to complete phase: {phase_identifier} in project: {project_dir}")
    try:
        manager = PhaseManager(project_dir=project_dir)
        manager.complete_phase(phase_identifier)
        click.echo(click.style(f"Successfully completed phase '{phase_identifier}'.", fg="green"))
        click.echo("- Action items potentially updated (manual check recommended if parsing failed)." )
        click.echo("- Development log updated.")
        click.echo("- Phase focus rule removed.")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print_error(f"Error completing phase '{phase_identifier}': {e}")
    except Exception as e:
        # Catch unexpected errors
        print_error(f"An unexpected error occurred during complete-phase: {e}")
        logger.exception("Unexpected error in complete-phase command") # Log stack trace

# --- Existing Commands Continue Below --- 

def main():
    """Main entry point for the CLI."""
    colorama.init()
    cli()

if __name__ == "__main__":
    main() 