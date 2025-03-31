#!/usr/bin/env python3
"""
Test script for improved action item generation and formatting.
This script demonstrates the enhanced JSON parsing and Markdown formatting
for action items in the document generator.
"""

import os
import sys
import json
import traceback
from pathlib import Path

# Add the parent directory to sys.path to ensure we can import cursor_rules
parent_dir = str(Path(__file__).resolve().parent.parent)
print(f"Adding {parent_dir} to sys.path")
sys.path.insert(0, parent_dir)

try:
    print("Importing modules...")
    from cursor_rules.document_generator import DocumentGenerator
    print("Imported DocumentGenerator")
    from cursor_rules.llm_connector import LLMProvider
    print("Imported LLMProvider")
    from cursor_rules.task_tracker import ActionPlan, Phase, Task, TaskStatus
    print("Imported task_tracker classes")
except Exception as e:
    print(f"Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

def create_sample_action_plan():
    """Create a sample action plan for testing."""
    print("Creating sample action plan...")
    # Create the action plan
    action_plan = ActionPlan(title="168 Hours App Development Plan")
    
    # Phase 1: Project Setup
    setup_phase = Phase(title="Phase 1: Project Setup", description="Initial setup and configuration")
    
    # Tasks for Phase 1
    env_task = Task(
        title="Set up development environment",
        description="Configure development environment for all team members",
        id="p1t1",
        priority=3,
        effort=2
    )
    env_task.add_subtask(Task(title="Install Node.js and npm", id="p1t1s1"))
    env_task.add_subtask(Task(title="Install React Native CLI", id="p1t1s2"))
    env_task.add_subtask(Task(title="Configure Firebase project", id="p1t1s3"))
    
    repo_task = Task(
        title="Initialize Git repository",
        description="Set up version control and CI/CD",
        id="p1t2",
        priority=3,
        effort=1
    )
    repo_task.add_subtask(Task(title="Create GitHub repository", id="p1t2s1"))
    repo_task.add_subtask(Task(title="Set up GitHub Actions", id="p1t2s2"))
    
    setup_phase.add_task(env_task)
    setup_phase.add_task(repo_task)
    
    # Phase 2: Core Features
    core_phase = Phase(title="Phase 2: Core Features", description="Implementation of the main application features")
    
    # Tasks for Phase 2
    auth_task = Task(
        title="Implement user authentication",
        description="Create user sign-up, login, and profile management",
        id="p2t1",
        priority=3,
        effort=3,
        tags=["backend", "security"]
    )
    auth_task.add_subtask(Task(title="Implement sign-up flow", id="p2t1s1"))
    auth_task.add_subtask(Task(title="Implement login flow", id="p2t1s2"))
    auth_task.add_subtask(Task(title="Implement password reset", id="p2t1s3"))
    auth_task.add_subtask(Task(title="Create user profile screens", id="p2t1s4"))
    
    time_tracking_task = Task(
        title="Create time tracking core functionality",
        description="Implement data models and logic for tracking time entries",
        id="p2t2",
        priority=3,
        effort=3,
        tags=["core", "database"]
    )
    time_tracking_task.add_subtask(Task(title="Design database schema", id="p2t2s1"))
    time_tracking_task.add_subtask(Task(title="Implement time entry creation", id="p2t2s2"))
    time_tracking_task.add_subtask(Task(title="Implement time entry editing", id="p2t2s3"))
    time_tracking_task.add_subtask(Task(title="Create category management", id="p2t2s4"))
    
    core_phase.add_task(auth_task)
    core_phase.add_task(time_tracking_task)
    
    # Phase 3: UI Implementation
    ui_phase = Phase(title="Phase 3: UI Implementation", description="Development of the user interface")
    
    # Tasks for Phase 3
    dashboard_task = Task(
        title="Implement dashboard screen",
        description="Create main dashboard with time distribution visualization",
        id="p3t1",
        priority=2,
        effort=2,
        tags=["frontend", "ux"]
    )
    dashboard_task.add_subtask(Task(title="Create time distribution charts", id="p3t1s1"))
    dashboard_task.add_subtask(Task(title="Implement quick-add shortcuts", id="p3t1s2"))
    
    ui_phase.add_task(dashboard_task)
    
    # Add phases to the action plan
    action_plan.add_phase(setup_phase)
    action_plan.add_phase(core_phase)
    action_plan.add_phase(ui_phase)
    
    print("Sample action plan created successfully")
    return action_plan

def main():
    """Main test function."""
    print("Testing enhanced action item generation and formatting\n")
    
    # Create output directory
    output_dir = "action_item_test_output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Create a sample action plan
    try:
        action_plan = create_sample_action_plan()
        
        # Initialize a DocumentGenerator with test data
        print("Initializing DocumentGenerator...")
        test_init_path = "test_init.md"
        
        # Check if the file exists
        if not os.path.exists(test_init_path):
            print(f"Warning: {test_init_path} does not exist. Using a sample content.")
            # Create a simple initialization document for testing
            with open(test_init_path, 'w', encoding='utf-8') as f:
                f.write("# Test Project\n\n## Project Overview\n\nThis is a test project.\n\n## Goals\n\nTo test the action item generation.")
            print(f"Created sample {test_init_path}")
        
        print(f"Creating DocumentGenerator with {test_init_path}")
        generator = DocumentGenerator(test_init_path)
        print("DocumentGenerator created successfully")
        
        # Save the action plan as JSON
        json_path = os.path.join(output_dir, "test_action_plan.json")
        print(f"Saving action plan as JSON to {json_path}")
        action_plan.save_to_file(json_path)
        print(f"Saved action plan as JSON to {json_path}")
        
        # Save the action plan as Markdown
        md_path = os.path.join(output_dir, "test_action_plan.md")
        print(f"Saving action plan as Markdown to {md_path}")
        generator._save_action_plan_as_markdown(md_path, action_plan)
        print(f"Saved action plan as Markdown to {md_path}")
        
        # Print content of the Markdown file
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n=== FORMATTED ACTION PLAN ===\n")
            print(content[:500] + "...\n" if len(content) > 500 else content + "\n")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()