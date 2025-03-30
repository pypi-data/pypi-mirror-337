#!/usr/bin/env python
"""
Complete workflow example demonstrating all Cursor Rules features working together.

This script demonstrates:
1. Generating a .cursorrules file from a markdown document
2. Extracting tasks from the document
3. Versioning the .cursorrules file
4. Monitoring codebase changes
5. Working with LLM providers
"""

import os
import sys
import time
import shutil
from pathlib import Path
import tempfile

# Add the parent directory to the path to allow importing cursor_rules
sys.path.insert(0, str(Path(__file__).parent.parent))

from cursor_rules import (
    # Core functionality
    RuleSet, Rule,
    
    # File generation
    generate_cursorrules_file, save_cursorrules_file,
    
    # Task tracking
    extract_action_plan_from_doc, ActionPlan, TaskStatus,
    
    # Versioning
    VersionManager,
    
    # Code monitoring
    create_monitor_for_project,
    
    # LLM integration
    LLMProvider, LLMConnector, MultiLLMProcessor, LLMRequest
)

def create_demo_project():
    """Create a temporary directory with demo project files."""
    temp_dir = tempfile.mkdtemp(prefix="cursor_rules_demo_")
    print(f"Created demo project directory: {temp_dir}")
    
    # Create some initial files
    readme_content = """# Demo Project
    
This is a demo project for Cursor Rules.

## Features
- Feature 1
- Feature 2
- Feature 3
"""
    with open(os.path.join(temp_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    # Create a requirements.txt file
    requirements_content = """
flask==2.0.1
pytest==6.2.5
"""
    with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
        f.write(requirements_content)
    
    # Create a source directory
    src_dir = os.path.join(temp_dir, "src")
    os.makedirs(src_dir)
    
    # Create a main app file
    app_content = """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open(os.path.join(src_dir, "app.py"), "w") as f:
        f.write(app_content)
    
    # Create an initialization document
    init_doc_content = """# Project Initialization: Demo Web App

## Project Overview
A simple web application to demonstrate Cursor Rules features.

## Tech Stack
- Flask - Web framework
- SQLAlchemy - ORM
- Pytest - Testing framework

## Project Structure
- src/ - Source code
- tests/ - Test files
- docs/ - Documentation

## Phases

### 1. Setup & Planning
- Set up development environment [Priority: High] [Effort: Small]
- Create project structure [Priority: High] [Effort: Small] [Tags: setup]
- Initialize git repository [Priority: Medium] [Effort: Small] [Tags: setup]

### 2. Backend Development
- Create Flask app [Priority: High] [Effort: Medium] [Tags: backend]
  - Set up routes
  - Configure settings
- Create database models [Priority: High] [Effort: Medium] [Tags: backend, database]
- Implement API endpoints [Priority: High] [Effort: Large] [Tags: backend, api]

### 3. Frontend Development
- Create templates [Priority: Medium] [Effort: Medium] [Tags: frontend]
- Implement CSS styling [Priority: Low] [Effort: Medium] [Tags: frontend, ui]
- Add JavaScript functionality [Priority: Medium] [Effort: Large] [Tags: frontend, js]

### 4. Testing & Deployment
- Write unit tests [Priority: High] [Effort: Large] [Tags: testing]
- Set up CI/CD pipeline [Priority: Medium] [Effort: Medium] [Tags: devops]
- Deploy to production [Priority: Medium] [Effort: Medium] [Tags: devops, deployment]
"""
    with open(os.path.join(temp_dir, "project_init.md"), "w") as f:
        f.write(init_doc_content)
    
    return temp_dir

def cleanup_demo_project(temp_dir):
    """Clean up the temporary directory."""
    try:
        shutil.rmtree(temp_dir)
        print(f"Cleaned up demo project directory: {temp_dir}")
    except Exception as e:
        print(f"Warning: Failed to clean up directory: {e}")

def main():
    """Run the complete workflow example."""
    print("\n=== Cursor Rules Complete Workflow Example ===\n")
    
    # Create a demo project
    project_dir = create_demo_project()
    
    try:
        # Step 1: Generate .cursorrules file from the initialization document
        print("\n--- Step 1: Generate .cursorrules file ---")
        init_doc_path = os.path.join(project_dir, "project_init.md")
        cursorrules_path = os.path.join(project_dir, ".cursorrules")
        
        # Create a RuleSet directly
        ruleset = RuleSet(name="Demo Web App Rules")
        ruleset.add_rule("Use type hints for all function definitions", tags=["python", "typing"])
        ruleset.add_rule("Write docstrings for all public functions and classes", tags=["python", "documentation"])
        ruleset.add_rule("Follow PEP 8 style guide", tags=["python", "style"])
        
        # Generate the .cursorrules file
        project_info = {
            "name": "Demo Web App",
            "description": "A simple web application to demonstrate Cursor Rules features",
            "tech_stack": {
                "frontend": ["HTML", "CSS", "JavaScript"],
                "backend": ["Flask", "SQLAlchemy"]
            }
        }
        # Generate and save the .cursorrules file directly with the ruleset
        save_cursorrules_file(ruleset, cursorrules_path, project_info)
        
        print(f"Generated .cursorrules file with {len(ruleset.rules)} rules")
        print(f"File path: {cursorrules_path}")
        
        # Step 2: Extract tasks from the initialization document
        print("\n--- Step 2: Extract tasks from initialization document ---")
        action_plan = extract_action_plan_from_doc(init_doc_path)
        tasks_file = os.path.join(project_dir, "tasks.json")
        action_plan.save_to_file(tasks_file)
        
        print(f"Extracted {action_plan.total_task_count()} tasks in {len(action_plan.phases)} phases")
        print(f"Tasks saved to: {tasks_file}")
        
        # Print some sample tasks
        print("\nSample tasks:")
        for phase in action_plan.phases[:2]:  # Just the first two phases
            print(f"\nPhase: {phase.title}")
            for task in phase.tasks[:2]:  # Just the first two tasks in each phase
                print(f"  - {task.title} [Status: {task.status.name}]")
                for subtask in task.subtasks[:2]:  # Just the first two subtasks
                    print(f"    - {subtask.title} [Status: {subtask.status.name}]")
        
        # Update a task status
        if action_plan.phases and action_plan.phases[0].tasks:
            first_task = action_plan.phases[0].tasks[0]
            first_task.status = TaskStatus.COMPLETED
            print(f"\nMarked task '{first_task.title}' as COMPLETED")
            
            # Save the updated action plan
            action_plan.save_to_file(tasks_file)
        
        # Step 3: Version the .cursorrules file
        print("\n--- Step 3: Version the .cursorrules file ---")
        version_manager = VersionManager()
        
        # Create an initial version
        version_id = version_manager.create_version(
            cursorrules_path,
            description="Initial version",
            author="Cursor Rules Demo"
        )
        
        print(f"Created initial version: {version_id}")
        
        # Modify the .cursorrules file
        ruleset.add_rule("Use descriptive variable names", tags=["style", "readability"])
        ruleset.add_rule("Keep functions small and focused", tags=["style", "maintainability"])
        
        # Generate and save updated version
        save_cursorrules_file(ruleset, cursorrules_path, project_info)
        
        # Create a new version
        version_id2 = version_manager.create_version(
            cursorrules_path,
            description="Added style rules",
            author="Cursor Rules Demo"
        )
        
        print(f"Created second version: {version_id2}")
        
        # List versions
        versions = version_manager.list_versions(cursorrules_path)
        print(f"\nVersions of {cursorrules_path}:")
        for i, version in enumerate(versions):
            print(f"{i+1}. {version.version_id} - {version.description} ({version.formatted_date})")
        
        # Get diff between versions
        diff = version_manager.get_diff(cursorrules_path, version_id, version_id2)
        print(f"\nDiff between versions {version_id} and {version_id2}:")
        print(diff[:500] + "..." if len(diff) > 500 else diff)  # Truncate if too long
        
        # Step 4: Set up code monitoring (just demonstrate setup)
        print("\n--- Step 4: Set up code monitoring ---")
        monitor = create_monitor_for_project(
            project_dir=project_dir,
            cursorrules_path=cursorrules_path
        )
        
        print(f"Created code monitor for {project_dir}")
        print(f"  .cursorrules file: {cursorrules_path}")
        print(f"  Polling interval: {monitor.poll_interval} seconds")
        print(f"  Change threshold: {monitor.change_threshold} files")
        
        # Create some changes to detect
        print("\nMaking changes to the project...")
        
        # Add a new file
        new_file_path = os.path.join(project_dir, "src", "models.py")
        new_file_content = """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"
"""
        with open(new_file_path, "w") as f:
            f.write(new_file_content)
            
        # Modify an existing file
        app_file_path = os.path.join(project_dir, "src", "app.py")
        with open(app_file_path, "r") as f:
            app_content = f.read()
            
        app_content += """
# Add a new route
@app.route('/api/users')
def get_users():
    return {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}
"""
        
        with open(app_file_path, "w") as f:
            f.write(app_content)
        
        # Check for changes
        print("\nChecking for changes...")
        changes = monitor.check_for_changes()
        
        if changes:
            print(f"Detected {changes.total_changes} changes:")
            print(f"  Added files: {len(changes.added_files)}")
            print(f"  Modified files: {len(changes.changed_files)}")
            print(f"  Deleted files: {len(changes.deleted_files)}")
        else:
            print("No changes detected")
        
        # Step 5: Demonstrate LLM integration
        print("\n--- Step 5: Demonstrate LLM integration ---")
        
        # Skip this step if API keys aren't available
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not (openai_api_key or anthropic_api_key):
            print("Skipping LLM integration demo as no API keys are available.")
            print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables to enable.")
        else:
            print("LLM providers available:")
            
            llm_connector = LLMConnector()
            
            if openai_api_key:
                llm_connector.set_api_key(LLMProvider.OPENAI, openai_api_key)
                print(f"  - {LLMProvider.OPENAI.value}")
                
            if anthropic_api_key:
                llm_connector.set_api_key(LLMProvider.ANTHROPIC, anthropic_api_key)
                print(f"  - {LLMProvider.ANTHROPIC.value}")
            
            # Always available
            print(f"  - {LLMProvider.MOCK.value}")
            
            # Test with the mock provider (doesn't require API key)
            print("\nTesting with mock provider...")
            
            llm_processor = MultiLLMProcessor()
            request = LLMRequest(
                prompt="Generate 3 rules for a Python web application",
                system_message="You are a helpful coding assistant.",
                provider=LLMProvider.MOCK
            )
            
            responses = llm_processor.process_with_specific(request, [LLMProvider.MOCK])
            
            for response in responses:
                print(f"\nResponse from {response.provider.value}:")
                print(f"  Time: {response.elapsed_time:.2f}s")
                print(f"  Text: {response.text}")
        
        print("\n=== Example Complete ===")
        print("\nThis example demonstrated:")
        print("1. Generating a .cursorrules file from a markdown document")
        print("2. Extracting tasks from the document")
        print("3. Versioning the .cursorrules file")
        print("4. Monitoring codebase changes")
        print("5. Working with LLM providers")
        
    finally:
        # Clean up the temporary directory
        cleanup_demo_project(project_dir)

if __name__ == "__main__":
    main() 