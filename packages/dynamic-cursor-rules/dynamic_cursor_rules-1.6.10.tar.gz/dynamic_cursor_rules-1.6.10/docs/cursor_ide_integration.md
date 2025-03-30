# Integrating with Cursor IDE

This guide provides instructions on how to use the Cursor Rules package to generate and manage `.cursorrules` files for Cursor IDE.

## What is a `.cursorrules` File?

A `.cursorrules` file is a configuration file used by Cursor IDE to provide instructions and context to the AI assistant (Claude, GPT, etc.) integrated within the IDE. This file helps the AI understand your project, follow your coding standards, and provide more relevant and helpful assistance.

According to best practices, an effective `.cursorrules` file should include:

1. **Project Overview**: Brief description of the project's purpose and goals
2. **Technical Stack**: Languages, frameworks, and libraries used in the project
3. **Coding Standards**: Naming conventions, formatting rules, and code organization
4. **Project Structure**: Directory layout and file organization
5. **Specific Rules**: Custom instructions for AI assistants

## Using Cursor Rules to Generate `.cursorrules` Files

The Cursor Rules package provides a straightforward way to create and manage `.cursorrules` files.

### Basic Example

```python
from cursor_rules import RuleSet, Rule, save_cursorrules_file

# Create a ruleset
ruleset = RuleSet(
    name="My Project",
    description="A web application for task management"
)

# Add rules
ruleset.add_rule(Rule(
    content="Use TypeScript for all frontend code",
    id="use_typescript",
    tags=["frontend"]
))

ruleset.add_rule(Rule(
    content="Follow TDD approach for all new features",
    id="follow_tdd",
    tags=["development"]
))

# Add project information
project_info = {
    "tech_stack": {
        "Frontend": ["React", "TypeScript", "Tailwind"],
        "Backend": ["Node.js", "Express", "MongoDB"]
    },
    "naming_conventions": {
        "Components": "PascalCase",
        "Functions": "camelCase"
    }
}

# Save to default location
save_cursorrules_file(ruleset, "~/.cursor/.cursorrules", project_info)
```

### Integration Locations

Cursor IDE supports two main locations for `.cursorrules` files:

1. **Global Settings**: `~/.cursor/.cursorrules`
   - Applies to all projects opened in Cursor IDE
   - Useful for personal coding preferences that apply across projects

2. **Project-Specific**: `<project_root>/.cursorrules`
   - Applies only to the specific project
   - Takes precedence over global settings
   - Useful for project-specific conventions and rules

## Best Practices for `.cursorrules` Files

Based on industry research and user experiences, here are some best practices for creating effective `.cursorrules` files:

### Keep It Concise
- Focus on the most important rules and context
- Avoid overwhelming the AI with excessive details
- Aim for clarity and specificity over verbosity

### Organize by Category
- Group related rules together (e.g., styling, architecture, testing)
- Use clear headings and structure
- Prioritize rules by importance

### Be Specific About Technologies
- Clearly state versions of languages and frameworks
- Explain any custom tools or libraries
- Provide context on why certain technologies were chosen

### Update Regularly
- Treat the `.cursorrules` file as a living document
- Update it as your project evolves and conventions change
- Consider versioning your rules

### Include Examples
- Provide concrete examples of code patterns to follow
- Illustrate both good and bad practices
- Show real use cases from your codebase

## Sample `.cursorrules` File

Here's a sample of what a well-structured `.cursorrules` file looks like:

```
# .cursorrules for Task Management App

# Overview:
# A modern web application for task management with user authentication,
# task assignment, due dates, and real-time updates.

# Tech Stack:
# Frontend: React 18, TypeScript 4.9, Tailwind CSS 3.2
# Backend: Node.js 18, Express 4.17, MongoDB 6.0
# Testing: Jest 29, React Testing Library 13

# Naming Conventions:
# - React components: PascalCase (e.g., TaskList, UserProfile)
# - React hooks: usePascalCase (e.g., useTasks, useAuth)
# - API routes: kebab-case (e.g., /api/auth/sign-in)
# - Database models: PascalCase, singular (e.g., User, Task)

# Directory Structure:
# - src/components: Reusable UI components
# - src/containers: Stateful components that connect to data sources
# - src/hooks: Custom React hooks
# - src/api: API service functions
# - server/routes: Express route handlers
# - server/models: Mongoose database models
# - server/controllers: Business logic for API endpoints

# Rules:

## Frontend Rules:
# react_functional_components: Use functional components with hooks instead of class components.
# component_patterns: Follow the container/component pattern for separation of concerns.
# use_tailwind: Use Tailwind CSS utility classes for styling rather than custom CSS.

## Backend Rules:
# express_middleware: Use Express.js middleware for authentication, validation, and error handling.
# rest_api_design: Follow REST API design principles for all endpoints.

## Testing Rules:
# unit_testing: Write unit tests for all business logic and components.
# mock_external_services: Use mocks for external services in tests.

## Code Style Rules:
# naming_convention: Use descriptive variable and function names following camelCase convention.
# typescript_typing: Use explicit TypeScript types rather than 'any'.

# Error Handling:
# Use try/catch blocks with proper error logging. Return consistent error response objects.

# Performance Considerations:
# Memoize expensive calculations. Use pagination for large data sets.
```

## Troubleshooting

If your `.cursorrules` file isn't being applied correctly:

1. **Check File Location**: Ensure it's in the correct location (global or project root)
2. **Check File Format**: Verify the content is properly formatted
3. **Restart Cursor IDE**: Changes may require an IDE restart to take effect
4. **Check for Syntax Errors**: Ensure there are no formatting or syntax issues
5. **File Permissions**: Make sure the file has appropriate read permissions 