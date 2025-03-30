"""
Parse tasks and action items from markdown documents.
"""
import re
from typing import Dict, List, Tuple, Optional, Any

from .task_tracker import ActionPlan, Phase, Task, TaskStatus

# Regular expressions for extracting tasks
HEADING_PATTERN = re.compile(r'^(#+)\s+(.*?)$', re.MULTILINE)
TASK_PATTERN = re.compile(r'^[ \t]*[-*]\s+(.*?)(?:\n|$)', re.MULTILINE)
SUBTASK_PATTERN = re.compile(r'^[ \t]+[-*]\s+(.*?)(?:\n|$)', re.MULTILINE)
PRIORITY_PATTERN = re.compile(r'\[Priority:?\s*([^\]]+)\]', re.IGNORECASE)
EFFORT_PATTERN = re.compile(r'\[Effort:?\s*([^\]]+)\]', re.IGNORECASE)
DEPENDENCY_PATTERN = re.compile(r'\[Depends?:?\s*([^\]]+)\]', re.IGNORECASE)
TAG_PATTERN = re.compile(r'\[Tags?:?\s*([^\]]+)\]', re.IGNORECASE)

def extract_tasks_from_markdown(content: str) -> ActionPlan:
    """
    Extract tasks from a markdown document and organize them into an action plan.
    
    Args:
        content: Markdown content to parse
        
    Returns:
        An ActionPlan object with tasks organized into phases
    """
    # Create the action plan
    action_plan = ActionPlan(title="Project Action Plan")
    
    # Find all headings which will be used as phase titles
    headings = [(len(match.group(1)), match.group(2).strip(), match.start()) 
                for match in HEADING_PATTERN.finditer(content)]
    
    current_phase = None
    
    # Process each heading as a potential phase
    for i, (level, title, start_pos) in enumerate(headings):
        # Skip top-level heading as it's likely the document title
        if level == 1:
            action_plan.title = title
            continue
            
        # Level 2 headings are phases
        if level == 2:
            # Create a new phase
            current_phase = Phase(title=title)
            action_plan.add_phase(current_phase)
        
        # Extract tasks under this heading
        if current_phase:
            # Find the end position of this section
            end_pos = len(content)
            if i < len(headings) - 1:
                # If there's another heading, use its position as the end
                end_pos = headings[i + 1][2]
                
            # Extract the section content
            section_content = content[start_pos:end_pos]
            
            # Extract tasks from this section
            tasks = extract_tasks_from_section(section_content, level)
            
            # Add tasks to the current phase
            for task in tasks:
                current_phase.add_task(task)
    
    # If no phases were found, create a default one
    if not action_plan.phases:
        default_phase = Phase(title="Tasks")
        
        # Extract tasks from the whole document
        tasks = extract_tasks_from_section(content, 0)
        
        for task in tasks:
            default_phase.add_task(task)
            
        action_plan.add_phase(default_phase)
    
    # Process dependencies
    resolve_dependencies(action_plan)
    
    return action_plan

def extract_tasks_from_section(content: str, heading_level: int) -> List[Task]:
    """
    Extract tasks from a section of markdown content.
    
    Args:
        content: The section content
        heading_level: The level of the section heading (0 for top level)
        
    Returns:
        A list of Task objects
    """
    tasks = []
    
    # Find all list items at the appropriate indentation level
    # For level 2 headings, we want top-level list items
    # For level 3+ headings, we want indented list items
    expected_indent = max(0, heading_level - 3) * "  "
    pattern = re.compile(f"^{expected_indent}[ \t]*[-*]\\s+(.*?)(?:\\n|$)", re.MULTILINE)
    
    for match in pattern.finditer(content):
        task_text = match.group(1).strip()
        
        # Skip empty tasks
        if not task_text:
            continue
            
        # Extract task metadata
        priority = 0
        effort = 0
        dependencies = []
        tags = []
        
        # Extract priority if present
        priority_match = PRIORITY_PATTERN.search(task_text)
        if priority_match:
            try:
                priority_text = priority_match.group(1).strip()
                if priority_text.lower() == "high":
                    priority = 3
                elif priority_text.lower() == "medium":
                    priority = 2
                elif priority_text.lower() == "low":
                    priority = 1
                else:
                    priority = int(priority_text)
                task_text = task_text.replace(priority_match.group(0), "").strip()
            except ValueError:
                pass
                
        # Extract effort if present
        effort_match = EFFORT_PATTERN.search(task_text)
        if effort_match:
            try:
                effort_text = effort_match.group(1).strip()
                if effort_text.lower() == "large":
                    effort = 3
                elif effort_text.lower() == "medium":
                    effort = 2
                elif effort_text.lower() == "small":
                    effort = 1
                else:
                    effort = int(effort_text)
                task_text = task_text.replace(effort_match.group(0), "").strip()
            except ValueError:
                pass
                
        # Extract dependencies if present
        dependency_match = DEPENDENCY_PATTERN.search(task_text)
        if dependency_match:
            deps_text = dependency_match.group(1).strip()
            dependencies = [dep.strip() for dep in deps_text.split(",")]
            task_text = task_text.replace(dependency_match.group(0), "").strip()
                
        # Extract tags if present
        tag_match = TAG_PATTERN.search(task_text)
        if tag_match:
            tags_text = tag_match.group(1).strip()
            tags = [tag.strip() for tag in tags_text.split(",")]
            task_text = task_text.replace(tag_match.group(0), "").strip()
            
        # Create the task
        task = Task(
            title=task_text,
            priority=priority,
            effort=effort,
            dependencies=dependencies,
            tags=tags
        )
        
        # Find the end position of this task
        task_start = match.start()
        task_end = len(content)
        
        # Find the next task at the same level
        next_match = pattern.search(content, task_start + 1)
        if next_match:
            task_end = next_match.start()
            
        # Extract the task content
        task_content = content[task_start:task_end]
        
        # Look for subtasks
        subtask_pattern = re.compile(f"^{expected_indent}[ \t]+[-*]\\s+(.*?)(?:\\n|$)", re.MULTILINE)
        for subtask_match in subtask_pattern.finditer(task_content):
            subtask_text = subtask_match.group(1).strip()
            
            # Skip empty subtasks
            if not subtask_text:
                continue
                
            # Extract subtask metadata (same as for tasks)
            sub_priority = 0
            sub_effort = 0
            sub_dependencies = []
            sub_tags = []
            
            priority_match = PRIORITY_PATTERN.search(subtask_text)
            if priority_match:
                try:
                    sub_priority_text = priority_match.group(1).strip()
                    if sub_priority_text.lower() == "high":
                        sub_priority = 3
                    elif sub_priority_text.lower() == "medium":
                        sub_priority = 2
                    elif sub_priority_text.lower() == "low":
                        sub_priority = 1
                    else:
                        sub_priority = int(sub_priority_text)
                    subtask_text = subtask_text.replace(priority_match.group(0), "").strip()
                except ValueError:
                    pass
                    
            effort_match = EFFORT_PATTERN.search(subtask_text)
            if effort_match:
                try:
                    sub_effort_text = effort_match.group(1).strip()
                    if sub_effort_text.lower() == "large":
                        sub_effort = 3
                    elif sub_effort_text.lower() == "medium":
                        sub_effort = 2
                    elif sub_effort_text.lower() == "small":
                        sub_effort = 1
                    else:
                        sub_effort = int(sub_effort_text)
                    subtask_text = subtask_text.replace(effort_match.group(0), "").strip()
                except ValueError:
                    pass
                    
            dependency_match = DEPENDENCY_PATTERN.search(subtask_text)
            if dependency_match:
                deps_text = dependency_match.group(1).strip()
                sub_dependencies = [dep.strip() for dep in deps_text.split(",")]
                subtask_text = subtask_text.replace(dependency_match.group(0), "").strip()
                    
            tag_match = TAG_PATTERN.search(subtask_text)
            if tag_match:
                tags_text = tag_match.group(1).strip()
                sub_tags = [tag.strip() for tag in tags_text.split(",")]
                subtask_text = subtask_text.replace(tag_match.group(0), "").strip()
            
            # Create the subtask
            subtask = Task(
                title=subtask_text,
                priority=sub_priority,
                effort=sub_effort,
                dependencies=sub_dependencies,
                tags=sub_tags
            )
            
            # Add the subtask to the parent task
            task.add_subtask(subtask)
        
        tasks.append(task)
    
    return tasks

def resolve_dependencies(action_plan: ActionPlan) -> None:
    """
    Resolve task dependencies based on titles (for human-readable dependencies).
    
    Args:
        action_plan: The action plan to process
    """
    all_tasks = action_plan.get_all_tasks()
    
    # Create a mapping from task titles to task IDs
    title_to_id = {task.title.lower(): task.id for task in all_tasks}
    
    # Process each task
    for task in all_tasks:
        resolved_dependencies = []
        
        for dep in task.dependencies:
            # If this is already an ID, keep it
            if dep in [t.id for t in all_tasks]:
                resolved_dependencies.append(dep)
            # Try to resolve by title
            elif dep.lower() in title_to_id:
                resolved_dependencies.append(title_to_id[dep.lower()])
        
        # Update task dependencies
        task.dependencies = resolved_dependencies


def extract_action_plan_from_doc(doc_path_or_content: str) -> ActionPlan:
    """
    Extract an action plan from a markdown document.
    
    Args:
        doc_path_or_content: Path to the document or the document content as a string
        
    Returns:
        An ActionPlan object
    """
    # Check if input is a file path or content
    if "\n" in doc_path_or_content or not doc_path_or_content.endswith((".md", ".txt")):
        # Input appears to be content
        return extract_tasks_from_markdown(doc_path_or_content)
    else:
        # Input appears to be a file path
        try:
            with open(doc_path_or_content, 'r', encoding='utf-8') as f:
                content = f.read()
            return extract_tasks_from_markdown(content)
        except FileNotFoundError:
            raise ValueError(f"Document not found: {doc_path_or_content}")
        except Exception as e:
            raise ValueError(f"Failed to parse document: {e}")


def parse_initialization_doc(doc_path_or_content: str) -> Tuple[ActionPlan, Dict[str, Any]]:
    """
    Parse an initialization document to extract tasks and metadata.
    
    Args:
        doc_path_or_content: Path to the document or the document content as a string
        
    Returns:
        A tuple containing:
            - An ActionPlan object
            - A dictionary of metadata
    """
    # Check if input is a file path or content
    if "\n" in doc_path_or_content or not doc_path_or_content.endswith((".md", ".txt")):
        # Input appears to be content
        action_plan = extract_tasks_from_markdown(doc_path_or_content)
        metadata = extract_metadata_from_markdown(doc_path_or_content)
        return action_plan, metadata
    else:
        # Input appears to be a file path
        try:
            with open(doc_path_or_content, 'r', encoding='utf-8') as f:
                content = f.read()
            action_plan = extract_tasks_from_markdown(content)
            metadata = extract_metadata_from_markdown(content)
            return action_plan, metadata
        except FileNotFoundError:
            raise ValueError(f"Document not found: {doc_path_or_content}")
        except Exception as e:
            raise ValueError(f"Failed to parse document: {e}")


def extract_metadata_from_markdown(content: str) -> Dict[str, Any]:
    """
    Extract metadata like project name, description, etc. from markdown content.
    
    Args:
        content: Markdown content
        
    Returns:
        Dictionary of metadata
    """
    metadata = {}
    
    # Extract title from top-level heading
    title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract project description from paragraphs after the title
    if title_match:
        title_end = title_match.end()
        next_heading = re.search(r'^#', content[title_end:], re.MULTILINE)
        if next_heading:
            description_section = content[title_end:title_end + next_heading.start()]
        else:
            description_section = content[title_end:]
            
        description = description_section.strip()
        if description:
            metadata['description'] = description
    
    # Look for specific sections
    sections = {
        'overview': re.compile(r'^#{1,3}\s+(?:Project\s+)?Overview\s*\n(.*?)(?=^#|\Z)', re.MULTILINE | re.DOTALL),
        'goals': re.compile(r'^#{1,3}\s+(?:Project\s+)?Goals\s*\n(.*?)(?=^#|\Z)', re.MULTILINE | re.DOTALL),
        'tech_stack': re.compile(r'^#{1,3}\s+Tech(?:nology)?\s+Stack\s*\n(.*?)(?=^#|\Z)', re.MULTILINE | re.DOTALL),
        'team': re.compile(r'^#{1,3}\s+Team\s*\n(.*?)(?=^#|\Z)', re.MULTILINE | re.DOTALL),
        'timeline': re.compile(r'^#{1,3}\s+Timeline\s*\n(.*?)(?=^#|\Z)', re.MULTILINE | re.DOTALL)
    }
    
    for key, pattern in sections.items():
        match = pattern.search(content)
        if match:
            section_content = match.group(1).strip()
            if section_content:
                metadata[key] = section_content
    
    return metadata 