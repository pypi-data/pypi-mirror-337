"""
Command-line interface for task management.
"""
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Any

from .task_tracker import ActionPlan, Task, TaskStatus, Phase
from .task_parser import extract_tasks_from_markdown, parse_initialization_doc
from .core import RuleSet
from .utils import generate_cursorrules_file, save_cursorrules_file
from .document_generator import DocumentGenerator

DEFAULT_TASKS_FILE = "cursor-rules-tasks.json"
DEFAULT_TASKS_MD_FILE = "cursor-rules-tasks.md"

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
        print("No phases found matching the filter.")
        return
        
    # For each phase
    for phase in phases:
        print(f"\n## {phase.title}")
        
        if phase.description:
            print(f"{phase.description}\n")
            
        # Get tasks for this phase
        tasks = phase.tasks
        
        # Apply status filter if requested
        if status_filter:
            try:
                status = TaskStatus(status_filter.lower())
                tasks = [t for t in tasks if t.status == status]
            except ValueError:
                print(f"Warning: Invalid status filter '{status_filter}'. Valid values are: "
                      f"{', '.join([s.value for s in TaskStatus])}")
                
        # Apply tag filter if requested
        if tag_filter:
            tasks = [t for t in tasks if tag_filter.lower() in [tag.lower() for tag in t.tags]]
            
        if not tasks:
            print("  No tasks found matching the filters.")
            continue
            
        # Print tasks
        for task in tasks:
            status_emoji = {
                TaskStatus.NOT_STARTED: "⭕",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.BLOCKED: "🚫"
            }.get(task.status, "⭕")
            
            task_info = f"- {status_emoji} **{task.title}** (ID: `{task.id}`"
            
            if task.priority > 0:
                task_info += f", Priority: {task.priority}"
                
            if task.effort > 0:
                task_info += f", Effort: {task.effort}"
                
            task_info += ")"
            
            print(task_info)
            
            if task.description:
                print(f"  - {task.description}")
                
            if task.dependencies:
                deps = ", ".join([f"`{dep}`" for dep in task.dependencies])
                print(f"  - **Dependencies:** {deps}")
                
            if task.tags:
                tags = ", ".join([f"#{tag}" for tag in task.tags])
                print(f"  - **Tags:** {tags}")
                
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
        
        indent_str = " " * indent
        subtask_info = f"{indent_str}- {status_emoji} **{subtask.title}** (ID: `{subtask.id}`"
        
        if subtask.priority > 0:
            subtask_info += f", Priority: {subtask.priority}"
            
        if subtask.effort > 0:
            subtask_info += f", Effort: {subtask.effort}"
            
        subtask_info += ")"
        
        print(subtask_info)
        
        if subtask.description:
            print(f"{indent_str}  - {subtask.description}")
            
        if subtask.dependencies:
            deps = ", ".join([f"`{dep}`" for dep in subtask.dependencies])
            print(f"{indent_str}  - **Dependencies:** {deps}")
            
        if subtask.tags:
            tags = ", ".join([f"#{tag}" for tag in subtask.tags])
            print(f"{indent_str}  - **Tags:** {tags}")
            
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

def generate_from_doc(doc_path: str, output_dir: str = ".") -> None:
    """
    Generate an action plan from a markdown document.
    
    Args:
        doc_path: Path to the markdown document
        output_dir: Directory where the action plan will be saved
    """
    try:
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

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Cursor Rules Task Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-f", "--file", help="Path to the tasks file", default=DEFAULT_TASKS_FILE)
    list_parser.add_argument("-p", "--phase", help="Filter tasks by phase")
    list_parser.add_argument("-s", "--status", help="Filter tasks by status")
    list_parser.add_argument("-t", "--tag", help="Filter tasks by tag")
    
    # Update task status command
    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("-f", "--file", help="Path to the tasks file", default=DEFAULT_TASKS_FILE)
    update_parser.add_argument("-t", "--task-id", required=True, help="ID of the task to update")
    update_parser.add_argument("-s", "--status", required=True, 
                              help="New status (not_started, in_progress, completed, blocked)")
    
    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("-f", "--file", help="Path to the tasks file", default=DEFAULT_TASKS_FILE)
    add_parser.add_argument("-p", "--phase-id", help="ID of the phase to add the task to")
    add_parser.add_argument("-t", "--title", required=True, help="Title of the task")
    add_parser.add_argument("-d", "--description", help="Description of the task")
    add_parser.add_argument("--priority", type=int, default=0, help="Priority of the task (0-10)")
    add_parser.add_argument("--effort", type=int, default=0, help="Effort estimate for the task (0-10)")
    add_parser.add_argument("--tags", help="Comma-separated list of tags")
    
    # Add subtask command
    add_subtask_parser = subparsers.add_parser("add-subtask", help="Add a subtask to an existing task")
    add_subtask_parser.add_argument("-f", "--file", help="Path to the tasks file", default=DEFAULT_TASKS_FILE)
    add_subtask_parser.add_argument("-p", "--parent-id", required=True, help="ID of the parent task")
    add_subtask_parser.add_argument("-t", "--title", required=True, help="Title of the subtask")
    add_subtask_parser.add_argument("-d", "--description", help="Description of the subtask")
    add_subtask_parser.add_argument("--priority", type=int, default=0, help="Priority of the subtask (0-10)")
    add_subtask_parser.add_argument("--effort", type=int, default=0, help="Effort estimate for the subtask (0-10)")
    add_subtask_parser.add_argument("--tags", help="Comma-separated list of tags")
    
    # Generate tasks from initialization document command
    generate_parser = subparsers.add_parser("generate", help="Generate tasks from an initialization document")
    generate_parser.add_argument("input", help="Path to the initialization document")
    generate_parser.add_argument("-o", "--output-dir", default=".", help="Directory where to save generated files")
    
    # Generate all documents from initialization document command
    documents_parser = subparsers.add_parser("documents", help="Generate all documents from an initialization document")
    documents_parser.add_argument("input", help="Path to the initialization document")
    documents_parser.add_argument("-o", "--output-dir", default=".", help="Directory where to save generated files")
    
    # Synchronize tasks with .cursorrules command
    sync_parser = subparsers.add_parser("sync", help="Synchronize tasks with .cursorrules")
    sync_parser.add_argument("-f", "--file", help="Path to the tasks file", default=DEFAULT_TASKS_FILE)
    sync_parser.add_argument("-r", "--rules", required=True, help="Path to the .cursorrules file")
    
    args = parser.parse_args()
    
    if args.command == "list":
        action_plan = load_action_plan(args.file)
        list_tasks(action_plan, args.phase, args.status, args.tag)
    
    elif args.command == "update":
        action_plan = load_action_plan(args.file)
        if update_task_status(action_plan, args.task_id, args.status):
            save_action_plan(action_plan, args.file)
    
    elif args.command == "add":
        action_plan = load_action_plan(args.file)
        tags = args.tags.split(",") if args.tags else []
        task = add_task(action_plan, args.title, args.phase_id, args.description, 
                       args.priority, args.effort, tags)
        if task:
            save_action_plan(action_plan, args.file)
            print(f"Task added with ID: {task.id}")
    
    elif args.command == "add-subtask":
        action_plan = load_action_plan(args.file)
        tags = args.tags.split(",") if args.tags else []
        subtask = add_subtask(action_plan, args.parent_id, args.title, args.description,
                             args.priority, args.effort, tags)
        if subtask:
            save_action_plan(action_plan, args.file)
            print(f"Subtask added with ID: {subtask.id}")
    
    elif args.command == "generate":
        generate_from_doc(args.input, args.output_dir)
    
    elif args.command == "documents":
        generate_from_doc(args.input, args.output_dir)
    
    elif args.command == "sync":
        action_plan = load_action_plan(args.file)
        ruleset = RuleSet.load(args.rules)
        sync_with_cursorrules(action_plan, ruleset)
        save_action_plan(action_plan, args.file)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 