"""
Task tracker module for managing action items in projects.
"""
import json
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

class TaskStatus(str, Enum):
    """Status of a task."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """A single task or action item."""
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: int = 0  # Higher number = higher priority
    effort: int = 0  # Estimated effort (1-10)
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # IDs of tasks this depends on
    subtasks: List['Task'] = field(default_factory=list)

    def is_complete(self) -> bool:
        """Check if the task is complete."""
        return self.status == TaskStatus.COMPLETED
    
    def is_blocked(self) -> bool:
        """Check if any dependencies are not complete."""
        return self.status == TaskStatus.BLOCKED
    
    def can_start(self, completed_task_ids: List[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return all(dep_id in completed_task_ids for dep_id in self.dependencies)
    
    def add_subtask(self, task: 'Task') -> None:
        """Add a subtask."""
        self.subtasks.append(task)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "priority": self.priority,
            "effort": self.effort,
            "tags": self.tags,
            "dependencies": self.dependencies
        }
        
        if self.description:
            result["description"] = self.description
            
        if self.subtasks:
            result["subtasks"] = [subtask.to_dict() for subtask in self.subtasks]
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create from dictionary representation."""
        # Handle subtasks recursively
        subtasks = []
        if "subtasks" in data:
            subtasks = [cls.from_dict(subtask) for subtask in data.pop("subtasks")]
        
        # Convert string status to enum
        if "status" in data and isinstance(data["status"], str):
            data["status"] = TaskStatus(data["status"])
            
        # Create the task
        task = cls(**{k: v for k, v in data.items() 
                     if k not in ["subtasks"]})
        
        # Add subtasks
        task.subtasks = subtasks
        
        return task


@dataclass
class Phase:
    """A project phase containing multiple tasks."""
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to this phase."""
        self.tasks.append(task)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Find a task by ID (including in subtasks)."""
        # Check direct tasks
        for task in self.tasks:
            if task.id == task_id:
                return task
            
            # Check subtasks recursively
            stack = list(task.subtasks)
            while stack:
                subtask = stack.pop()
                if subtask.id == task_id:
                    return subtask
                stack.extend(subtask.subtasks)
        
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description if hasattr(self, 'description') else None,
            "tasks": [task.to_dict() for task in self.tasks]
        }
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Phase':
        """Create from dictionary representation."""
        tasks_data = data.pop("tasks", [])
        phase = cls(**{k: v for k, v in data.items() if k != "tasks"})
        
        for task_data in tasks_data:
            phase.add_task(Task.from_dict(task_data))
            
        return phase


@dataclass
class ActionPlan:
    """A complete action plan containing multiple phases."""
    title: str
    phases: List[Phase] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_phase(self, phase: Phase) -> None:
        """Add a phase to the action plan."""
        self.phases.append(phase)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Find a task by ID across all phases."""
        for phase in self.phases:
            task = phase.get_task_by_id(task_id)
            if task:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all phases (flattened)."""
        tasks = []
        for phase in self.phases:
            tasks.extend(phase.tasks)
            
            # Add subtasks recursively
            stack = []
            for task in phase.tasks:
                stack.extend(task.subtasks)
                
            while stack:
                subtask = stack.pop()
                tasks.append(subtask)
                stack.extend(subtask.subtasks)
                
        return tasks
    
    def get_completed_task_ids(self) -> List[str]:
        """Get IDs of all completed tasks."""
        return [task.id for task in self.get_all_tasks() if task.is_complete()]
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update the status of a task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        task.status = status
        return True
    
    def add_task_to_phase(self, phase_id: str, task: Task) -> bool:
        """Add a task to a specific phase."""
        for phase in self.phases:
            if phase.id == phase_id:
                phase.add_task(task)
                return True
        return False
    
    def save(self, filepath: str) -> None:
        """Save the action plan to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the action plan to a dictionary."""
        return {
            "title": self.title,
            "description": self.description if hasattr(self, 'description') else None,
            "phases": [phase.to_dict() for phase in self.phases],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionPlan':
        """Create from dictionary representation."""
        phases_data = data.pop("phases", [])
        action_plan = cls(**{k: v for k, v in data.items() if k != "phases"})
        
        for phase_data in phases_data:
            action_plan.add_phase(Phase.from_dict(phase_data))
            
        return action_plan
    
    @classmethod
    def load(cls, filepath: str) -> 'ActionPlan':
        """Load an action plan from a file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_markdown(self) -> str:
        """Generate a markdown representation of the action plan."""
        lines = [f"# {self.title}", ""]
        
        # Add metadata if present
        if self.metadata:
            lines.append("## Metadata")
            for key, value in self.metadata.items():
                lines.append(f"- **{key}:** {value}")
            lines.append("")
        
        # Add phases
        for phase in self.phases:
            lines.append(f"## {phase.title}")
            
            if phase.description:
                lines.append(f"{phase.description}")
                
            lines.append("")
            
            # Add tasks
            for task in phase.tasks:
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
                
                lines.append(task_info)
                
                if task.description:
                    lines.append(f"  - {task.description}")
                    
                if task.dependencies:
                    deps = ", ".join([f"`{dep}`" for dep in task.dependencies])
                    lines.append(f"  - **Dependencies:** {deps}")
                    
                # Add subtasks recursively
                if task.subtasks:
                    self._add_subtasks_to_markdown(task.subtasks, lines, indent=2)
                    
            lines.append("")
            
        return "\n".join(lines)
    
    def _add_subtasks_to_markdown(self, subtasks: List[Task], lines: List[str], indent: int) -> None:
        """Helper to recursively add subtasks to markdown."""
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
            
            lines.append(subtask_info)
            
            if subtask.description:
                lines.append(f"{indent_str}  - {subtask.description}")
                
            if subtask.dependencies:
                deps = ", ".join([f"`{dep}`" for dep in subtask.dependencies])
                lines.append(f"{indent_str}  - **Dependencies:** {deps}")
                
            # Recursively add nested subtasks
            if subtask.subtasks:
                self._add_subtasks_to_markdown(subtask.subtasks, lines, indent + 2)

    def save_to_json(self, file_path: str) -> None:
        """Save the action plan to a JSON file."""
        try:
            import json # Ensure json is imported
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2)
            print(f"Action plan saved to JSON: {file_path}") # Add confirmation
        except Exception as e:
            print(f"Error saving ActionPlan to JSON '{file_path}': {e}")
            raise

    def save_to_markdown(self, file_path: str) -> None:
        """Save the action plan to a Markdown file."""
        content = [f"# {self.title}\n"]
        if hasattr(self, 'description') and self.description:
            content.append(f"{self.description}\n")

        for phase in self.phases:
            content.append(f"## {phase.title}\n")
            if hasattr(phase, 'description') and phase.description:
                 content.append(f"{phase.description}\n")
            for task in phase.tasks:
                self._add_task_to_markdown(content, task, indent_level=0)
            content.append("") # Add newline after phase

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
            print(f"Action plan saved to Markdown: {file_path}") # Add confirmation
        except Exception as e:
             print(f"Error saving ActionPlan to Markdown '{file_path}': {e}")
             raise

    def _add_task_to_markdown(self, content: List[str], task: 'Task', indent_level: int) -> None:
        """Recursively add a task and its subtasks to markdown content using checkboxes."""
        prefix = "  " * indent_level + "- "
        
        # Use Markdown checkboxes based on status
        if task.status == TaskStatus.COMPLETED:
            status_marker = "[x]"
        else:
            # Treat IN_PROGRESS, BLOCKED, NOT_STARTED as unchecked
            status_marker = "[ ]"
            
        # Ensure title exists before using it
        task_title = task.title if hasattr(task, 'title') and task.title else "Untitled Task"
        
        # Construct the task line with checkbox
        task_line = f"{prefix}{status_marker} **{task_title}** (ID: `{task.id}`)"

        meta = []
        if hasattr(task, 'priority') and task.priority > 0: meta.append(f"P{task.priority}")
        if hasattr(task, 'effort') and task.effort > 0: meta.append(f"E{task.effort}")
        if hasattr(task, 'tags') and task.tags: meta.append(f"Tags: {','.join(task.tags)}")
        if hasattr(task, 'dependencies') and task.dependencies: meta.append(f"Deps: {','.join(task.dependencies)}")
        if meta:
             task_line += f" [{', '.join(meta)}]"

        content.append(task_line)
        if hasattr(task, 'description') and task.description:
            # Indent description slightly more than the task itself for clarity
            content.append("  " * (indent_level + 1) + f"> {task.description}") # Keep description format

        if hasattr(task, 'subtasks') and task.subtasks:
            for subtask in task.subtasks:
                # Recursive call for subtasks
                self._add_task_to_markdown(content, subtask, indent_level + 1)

    @classmethod
    def load_from_json(cls, file_path: str) -> 'ActionPlan':
        """Load an action plan from a JSON file."""
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
             print(f"Error: Action plan file not found at '{file_path}'")
             raise
        except Exception as e:
             print(f"Error loading ActionPlan from JSON '{file_path}': {e}")
             raise

    def get_tasks_by_phase(self, phase_title: str) -> List[Task]:
        """Get all tasks in a specific phase by title."""
        for phase in self.phases:
            if phase.title == phase_title:
                return phase.tasks
        return []
    
    def total_task_count(self) -> int:
        """Count the total number of tasks and subtasks."""
        count = 0
        for phase in self.phases:
            count += len(phase.tasks)
            # Count all subtasks recursively
            for task in phase.tasks:
                stack = list(task.subtasks)
                count += len(task.subtasks)
                while stack:
                    subtask = stack.pop()
                    count += len(subtask.subtasks)
                    stack.extend(subtask.subtasks)
        return count


def synchronize_with_cursorrules(action_plan: ActionPlan, ruleset: Any) -> None:
    """
    Synchronize an action plan with rules from a ruleset.
    This adds tasks for implementing rules that aren't covered yet.
    
    Args:
        action_plan: The action plan to update
        ruleset: A RuleSet object containing rules
    """
    # Ensure we have a planning phase
    planning_phase = None
    for phase in action_plan.phases:
        if "planning" in phase.title.lower():
            planning_phase = phase
            break
    
    if planning_phase is None:
        planning_phase = Phase(title="Planning & Rules")
        action_plan.add_phase(planning_phase)
    
    # Extract rules and add as tasks if they don't exist yet
    existing_task_titles = {task.title.lower() for task in action_plan.get_all_tasks()}
    
    for rule in ruleset.rules:
        task_title = f"Implement rule: {rule.content}"
        
        # Check if we already have this rule as a task
        if task_title.lower() in existing_task_titles:
            continue
            
        # Create a new task for this rule
        task = Task(
            title=task_title,
            description=f"Ensure compliance with: {rule.content}",
            priority=2,  # Medium priority by default
            tags=rule.tags
        )
        
        planning_phase.add_task(task)

def generate_action_plan_from_doc(doc_content: str, ruleset: Any = None) -> ActionPlan:
    """
    Generate an action plan from a document and optionally a ruleset.
    
    Args:
        doc_content: The document content (usually markdown)
        ruleset: Optional ruleset to integrate
        
    Returns:
        An ActionPlan with tasks from the document and rules
    """
    # This is a placeholder that would be implemented to extract
    # tasks from the document and integrate with the ruleset
    
    # In a real implementation, you'd parse the document for tasks
    from .task_parser import extract_tasks_from_markdown
    
    action_plan = extract_tasks_from_markdown(doc_content)
    
    # If we have a ruleset, synchronize with it
    if ruleset:
        synchronize_with_cursorrules(action_plan, ruleset)
        
    return action_plan 