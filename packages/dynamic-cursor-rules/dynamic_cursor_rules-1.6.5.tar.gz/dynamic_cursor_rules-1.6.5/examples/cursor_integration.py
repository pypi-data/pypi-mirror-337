"""
Example showing how to integrate with Cursor IDE.
"""
import os
from pathlib import Path
from cursor_rules import (
    RuleSet, 
    Rule, 
    generate_cursorrules_file, 
    save_cursorrules_file,
    create_demo_ruleset
)

def main():
    # Create a ruleset for a web application project
    ruleset = RuleSet(
        name="Web App Rules",
        description="Rules for a React web application project with Node.js backend"
    )
    
    # Add frontend rules
    ruleset.add_rule(Rule(
        content="Use functional components with hooks instead of class components.",
        id="react_functional_components",
        priority=10,
        tags=["frontend", "react"]
    ))
    
    ruleset.add_rule(Rule(
        content="Follow the container/component pattern for separation of concerns.",
        id="component_pattern",
        priority=8,
        tags=["frontend", "architecture"]
    ))
    
    ruleset.add_rule(Rule(
        content="Use Tailwind CSS for styling components.",
        id="use_tailwind",
        priority=7,
        tags=["frontend", "styling"]
    ))
    
    # Add backend rules
    ruleset.add_rule(Rule(
        content="Use Express.js middleware for authentication and validation.",
        id="express_middleware",
        priority=9,
        tags=["backend", "express"]
    ))
    
    ruleset.add_rule(Rule(
        content="Follow REST API design principles for all endpoints.",
        id="rest_api_design",
        priority=8,
        tags=["backend", "api"]
    ))
    
    # Add general coding rules
    ruleset.add_rule(Rule(
        content="Write unit tests for all business logic.",
        id="unit_testing",
        priority=9,
        tags=["testing", "quality"]
    ))
    
    ruleset.add_rule(Rule(
        content="Use descriptive variable and function names following camelCase convention.",
        id="naming_convention",
        priority=7,
        tags=["style", "readability"]
    ))
    
    # Create project info with metadata
    project_info = {
        "name": "Task Management Application",
        "description": "A modern task management web application with user authentication and real-time updates",
        "tech_stack": {
            "Frontend": ["React", "TypeScript", "Tailwind CSS", "React Query"],
            "Backend": ["Node.js", "Express", "MongoDB", "Mongoose"],
            "Testing": ["Jest", "React Testing Library"]
        },
        "naming_conventions": {
            "React components": "PascalCase (e.g., TaskList, UserProfile)",
            "React hooks": "usePascalCase (e.g., useTasks, useAuth)",
            "API routes": "kebab-case (e.g., /api/auth/sign-in)",
            "Database models": "PascalCase, singular (e.g., User, Task)"
        },
        "directory_structure": {
            "src/components": "Reusable UI components",
            "src/containers": "Stateful components that connect to data sources",
            "src/hooks": "Custom React hooks",
            "src/api": "API service functions",
            "server/routes": "Express route handlers",
            "server/models": "Mongoose database models",
            "server/controllers": "Business logic for API endpoints"
        },
        "additional_sections": {
            "Error Handling": "Use try/catch blocks with proper error logging. Return consistent error response objects.",
            "Performance Considerations": "Memoize expensive calculations. Use pagination for large data sets."
        }
    }
    
    # Generate the .cursorrules file content
    cursorrules_content = generate_cursorrules_file(ruleset, project_info)
    print("Generated .cursorrules file content:")
    print("-" * 80)
    print(cursorrules_content)
    print("-" * 80)
    
    # Save to the recommended location for Cursor IDE
    home_dir = Path.home()
    cursor_dir = home_dir / ".cursor"
    
    # Ensure cursor directory exists
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the .cursorrules file
    cursorrules_path = cursor_dir / ".cursorrules"
    save_cursorrules_file(ruleset, str(cursorrules_path), project_info)
    
    print(f"\nSaved .cursorrules file to: {cursorrules_path}")
    print("\nIntegration with Cursor IDE:")
    print("1. The .cursorrules file has been saved to the recommended location.")
    print("2. Cursor IDE will automatically load these rules when you start it.")
    print("3. AI assistants in Cursor will use these rules to guide their responses.")
    print("4. You may need to restart Cursor IDE for the changes to take effect.")
    
    # Show how to create and save project-specific rules
    print("\nFor project-specific rules:")
    print("1. You can also save a .cursorrules file at the root of your project.")
    print("2. Project-specific rules will override global rules when working in that project.")
    
    project_path = input("\nEnter your project path to save project-specific rules (or press Enter to skip): ")
    if project_path and os.path.isdir(project_path):
        project_cursorrules_path = Path(project_path) / ".cursorrules"
        save_cursorrules_file(ruleset, str(project_cursorrules_path), project_info)
        print(f"Saved project-specific .cursorrules file to: {project_cursorrules_path}")

if __name__ == "__main__":
    main() 