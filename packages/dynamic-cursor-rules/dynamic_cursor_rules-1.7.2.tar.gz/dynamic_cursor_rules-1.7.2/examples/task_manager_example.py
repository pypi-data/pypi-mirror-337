#!/usr/bin/env python
"""
Example script demonstrating the task tracking functionality of cursor_rules.

This script shows how to:
1. Parse an initialization document to extract tasks
2. Manage tasks and their statuses
3. Save and load action plans
4. Synchronize with .cursorrules files
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path to allow importing cursor_rules
sys.path.insert(0, str(Path(__file__).parent.parent))

from cursor_rules import (
    RuleSet,
    Rule,
    Task,
    Phase,
    ActionPlan,
    TaskStatus,
    extract_action_plan_from_doc,
    extract_tasks_from_markdown,
    synchronize_with_cursorrules,
    generate_cursorrules_file
)

def create_sample_initialization_doc():
    """Create a sample initialization document for demonstration purposes."""
    sample_doc = """# Project Initialization: Task Manager App

## Project Overview
Create a task management application with a clean UI and robust backend.

## Phases

### 1. Setup & Planning
- Set up the development environment [Priority: High] [Effort: Small]
- Create project structure [Priority: High] [Effort: Medium] [Tags: architecture, setup]
- Design database schema [Priority: Medium] [Effort: Medium] [Tags: database, architecture]

### 2. Backend Development
- Implement user authentication [Priority: High] [Effort: Large] [Tags: security]
  - Create login endpoint
  - Add JWT handling
  - Implement password hashing
- Create task CRUD endpoints [Priority: High] [Effort: Medium] [Depends: Design database schema]
  - Implement task creation
  - Add task update functionality
  - Create task deletion endpoint
- Add categorization system [Priority: Medium] [Effort: Medium]

### 3. Frontend Development
- Design UI components [Priority: High] [Effort: Medium]
- Implement dashboard view [Priority: Medium] [Effort: Large] [Depends: Design UI components]
- Create task forms [Priority: Medium] [Effort: Medium]
- Add drag and drop functionality [Priority: Low] [Effort: Large]

### 4. Testing & Deployment
- Write unit tests [Priority: High] [Effort: Large]
- Set up CI/CD pipeline [Priority: Medium] [Effort: Medium]
- Deploy to staging environment [Priority: Medium] [Effort: Small] [Depends: Set up CI/CD pipeline]
- Perform security audit [Priority: High] [Effort: Medium] [Tags: security]
"""
    return sample_doc

def print_tasks(action_plan):
    """Print all tasks from an action plan."""
    print("\nAll Tasks:")
    for phase in action_plan.phases:
        print(f"\n## {phase.title}")
        for task in phase.tasks:
            print(f"- {task.title} [Status: {task.status.name}]")
            for subtask in task.subtasks:
                print(f"  - {subtask.title} [Status: {subtask.status.name}]")

def main():
    """Run the task manager example."""
    try:
        # Create a sample document
        sample_doc = create_sample_initialization_doc()
        print("Created sample initialization document.\n")
        
        # Parse the document to extract tasks
        action_plan = extract_tasks_from_markdown(sample_doc)
        print(f"Extracted action plan with {len(action_plan.phases)} phases and {action_plan.total_task_count()} tasks.")
        
        # Display all tasks
        print_tasks(action_plan)
        
        # Update some task statuses
        setup_tasks = action_plan.get_tasks_by_phase("1. Setup & Planning")
        if setup_tasks:
            setup_tasks[0].status = TaskStatus.COMPLETED
            print(f"\nMarked '{setup_tasks[0].title}' as COMPLETED.")
        
        backend_phase = None
        for phase in action_plan.phases:
            if "Backend Development" in phase.title:
                backend_phase = phase
                break
                
        if backend_phase and backend_phase.tasks:
            auth_task = next((t for t in backend_phase.tasks if "authentication" in t.title.lower()), None)
            if auth_task and auth_task.subtasks:
                auth_task.subtasks[0].status = TaskStatus.IN_PROGRESS
                print(f"\nMarked '{auth_task.subtasks[0].title}' as IN_PROGRESS.")
        
        # Save the action plan to a file
        output_file = "sample_action_plan.json"
        action_plan.save_to_file(output_file)
        print(f"\nSaved action plan to {output_file}")
        
        # Load the action plan from the file
        loaded_plan = ActionPlan.load_from_file(output_file)
        print(f"Loaded action plan with {len(loaded_plan.phases)} phases and {loaded_plan.total_task_count()} tasks.")
        
        # Create a ruleset and synchronize with the action plan
        ruleset = RuleSet(name="Task Manager App Rules")
        ruleset.add_rule("Use TypeScript for frontend development", tags=["frontend", "typescript"])
        ruleset.add_rule("Follow REST API design principles", tags=["backend", "api"])
        ruleset.add_rule("Write unit tests for all business logic", tags=["testing"])
        
        # Sync the ruleset with the action plan
        synchronize_with_cursorrules(action_plan, ruleset)
        print("\nSynchronized action plan with ruleset.")
        
        # Display updated tasks
        print_tasks(action_plan)
        
        # Generate a markdown representation of the action plan
        markdown_output = action_plan.to_markdown()
        with open("sample_action_plan.md", "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print("\nSaved markdown representation to sample_action_plan.md")
        
        # Generate a .cursorrules file from the ruleset
        cursorrules_content = generate_cursorrules_file(
            ruleset,
            project_info={
                "name": "Task Manager App",
                "description": "A task management application with a clean UI and robust backend."
            }
        )
        with open("sample_cursorrules", "w", encoding="utf-8") as f:
            f.write(cursorrules_content)
        print("Generated sample_cursorrules file from the ruleset.")
        
        print("\nExample complete. Check the output files for details.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 