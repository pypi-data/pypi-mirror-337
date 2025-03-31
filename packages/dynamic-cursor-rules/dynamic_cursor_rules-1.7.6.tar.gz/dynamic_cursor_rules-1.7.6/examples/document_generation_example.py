#!/usr/bin/env python
"""
Example demonstrating document generation from an initialization document.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the path to allow importing cursor_rules
sys.path.insert(0, str(Path(__file__).parent.parent))

from cursor_rules import DocumentGenerator

def main():
    """Run the document generation example."""
    print("\n=== Cursor Rules Document Generation Example ===\n")
    
    # Create a temporary directory for our example
    temp_dir = tempfile.mkdtemp(prefix="cursor_rules_doc_gen_")
    print(f"Created temporary directory: {temp_dir}")
    
    # Create an initialization document
    init_doc_path = os.path.join(temp_dir, "timer_app_init.md")
    with open(init_doc_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_TIMER_APP_INIT_DOC)
    
    print(f"Created sample initialization document at: {init_doc_path}")
    
    try:
        # Generate documents from the initialization document
        print("\nGenerating documents...")
        document_generator = DocumentGenerator(init_doc_path, temp_dir)
        generated_files = document_generator.generate_all_documents()
        
        print("\nGenerated files:")
        for doc_name, file_path in generated_files.items():
            print(f"- {doc_name}: {file_path}")
            
            # Print a preview of each generated file
            print(f"\nPreview of {doc_name}:")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Just show the first few lines of each file
                preview_lines = content.split("\n")[:10]
                print("\n".join(preview_lines))
                if len(content.split("\n")) > 10:
                    print("... (more content omitted)")
                    
                print()
        
        print("\nDocument generation complete!")
        print(f"\nYou can find all the generated files in: {temp_dir}")
        print("\nThis demo showed how to:")
        print("1. Create an initialization document with project details")
        print("2. Generate a complete set of documentation files")
        print("   - Product Requirements Document")
        print("   - Technical Stack Document")
        print("   - .cursorrules file for Cursor IDE")
        print("   - Action Items (tasks) in JSON and Markdown formats")
        
    except Exception as e:
        print(f"Error generating documents: {e}")
    finally:
        # Do not delete the temp directory so user can explore the files
        print(f"\nTemporary directory will not be deleted for you to explore: {temp_dir}")


# Sample initialization document for a timer application
SAMPLE_TIMER_APP_INIT_DOC = """# Timer App: Simple Productivity Timer

## Project Overview

Timer App is a simple productivity application that helps users manage their time effectively using the Pomodoro Technique. The app allows users to set work intervals followed by short breaks, with a longer break after completing a set number of work intervals. This approach helps maintain focus and prevent burnout.

## Core Functionality

1. **Timer Features**
   - Customizable work intervals (default: 25 minutes)
   - Customizable short breaks (default: 5 minutes)
   - Customizable long breaks (default: 15 minutes)
   - Configurable number of work intervals before a long break (default: 4)
   - Visual and audio notifications when timers complete

2. **Task Management**
   - Simple task list to associate with timer sessions
   - Ability to mark tasks as complete
   - Task prioritization
   - Daily task reset option

3. **Statistics and Reports**
   - Track time spent on work sessions
   - Daily, weekly, and monthly summaries
   - Productivity trends visualization

4. **Settings**
   - Light/dark theme toggle
   - Sound on/off and volume control
   - Notification preferences
   - Auto-start next timer option

## Technical Requirements

### Language
- JavaScript/TypeScript for frontend development

### Frameworks and Libraries
- React for UI components
- Redux for state management
- Chart.js for statistics visualization
- Electron (optional) for desktop app version

### Key Libraries
- `date-fns` for date manipulation
- `react-beautiful-dnd` for drag-and-drop task reordering
- `howler` for audio notifications
- `react-testing-library` for component testing

## Architecture

The application follows a clean architecture pattern with the following components:

1. **UI Layer**: React components for user interface
2. **State Management**: Redux store with slices for different features
3. **Services Layer**: Timer service, notification service, storage service
4. **Data Layer**: Local storage for persisting user data

## Directory Structure
- `src/`: Source code
  - `components/`: React components
  - `features/`: Feature-specific code
  - `services/`: Business logic services
  - `store/`: Redux state management
  - `utils/`: Utility functions
- `public/`: Static assets
- `tests/`: Testing files

## Coding Standards
- Use functional components with hooks
- Implement proper error handling
- Write comprehensive unit tests
- Use TypeScript interfaces for type safety
- Follow airbnb eslint rules
- Use CSS modules for styling

## User Experience

1. **Initial Setup**
   - User installs the app
   - First-time tutorial explains the Pomodoro Technique
   - Default timer settings are applied

2. **Daily Usage**
   - User adds tasks for the day
   - Starts a work timer
   - Receives notification when timer completes
   - Takes a break
   - Repeats the cycle

3. **Weekly Review**
   - User checks statistics to review productivity
   - Adjusts timer settings if needed

## Phases

### 1. Setup & Planning
- Set up development environment [Priority: High] [Effort: Small]
- Create project structure [Priority: High] [Effort: Small] [Tags: setup]
- Define user stories and wireframes [Priority: High] [Effort: Medium] [Tags: planning]

### 2. Core Timer Implementation
- Implement timer functionality [Priority: High] [Effort: Medium] [Tags: core]
  - Create timer state management
  - Build timer display component
  - Add timer controls (start, pause, reset)
- Implement timer settings [Priority: Medium] [Effort: Small] [Tags: core]
- Add notifications [Priority: Medium] [Effort: Small] [Tags: ux]

### 3. Task Management
- Create task list component [Priority: Medium] [Effort: Medium] [Tags: features]
- Implement task CRUD operations [Priority: Medium] [Effort: Medium] [Tags: features]
- Add task prioritization [Priority: Low] [Effort: Small] [Tags: features]

### 4. Statistics and Settings
- Implement activity tracking [Priority: Low] [Effort: Medium] [Tags: features]
- Create statistics visualization [Priority: Low] [Effort: Large] [Tags: features]
- Add user settings [Priority: Medium] [Effort: Medium] [Tags: ux]

### 5. Testing & Deployment
- Write unit tests [Priority: Medium] [Effort: Large] [Tags: quality]
- Perform user testing [Priority: Medium] [Effort: Medium] [Tags: quality]
- Deploy to production [Priority: High] [Effort: Small] [Tags: deployment]
"""

if __name__ == "__main__":
    main() 