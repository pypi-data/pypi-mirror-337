"""
Generate an example .cursorrules file.
"""
from cursor_rules import RuleSet, Rule, generate_cursorrules_file

def main():
    # Create a ruleset
    ruleset = RuleSet(
        name="Cursor Rules Example",
        description="An example project for demonstrating .cursorrules file generation"
    )
    
    # Add rules
    ruleset.add_rule(Rule(
        content="Use functional components with hooks instead of class components",
        id="react_functional",
        tags=["frontend", "react"]
    ))
    
    ruleset.add_rule(Rule(
        content="Follow REST API design principles for all endpoints",
        id="rest_api",
        tags=["backend", "api"]
    ))
    
    ruleset.add_rule(Rule(
        content="Write unit tests for all business logic",
        id="unit_tests",
        priority=10,
        tags=["testing"]
    ))
    
    # Create project info
    project_info = {
        "tech_stack": {
            "Frontend": ["React", "TypeScript", "Tailwind CSS"],
            "Backend": ["Node.js", "Express", "MongoDB"],
            "Testing": ["Jest", "React Testing Library"]
        },
        "naming_conventions": {
            "React components": "PascalCase (e.g., TaskList)",
            "React hooks": "useCamelCase (e.g., useAuth)",
            "API routes": "kebab-case (e.g., /users/user-id)"
        },
        "directory_structure": {
            "src/components": "Reusable UI components",
            "src/pages": "Page-level components",
            "src/api": "API client code",
            "server": "Backend code"
        }
    }
    
    # Generate the .cursorrules file content
    content = generate_cursorrules_file(ruleset, project_info)
    
    # Print the content
    print(content)
    
    # Save to a file
    with open('.cursorrules_example', 'w') as f:
        f.write(content)
    
    print("\nSaved to .cursorrules_example")

if __name__ == "__main__":
    main() 