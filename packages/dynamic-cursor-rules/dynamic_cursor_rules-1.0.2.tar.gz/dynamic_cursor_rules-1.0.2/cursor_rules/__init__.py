"""
Cursor Rules - A framework for managing custom instructions for AI assistants.
"""

__version__ = "0.1.0"

from .core import Rule, RuleSet
from .parser import parse_file, parse_directory, parse_markdown
from .executor import RuleExecutor
from .utils import (
    merge_rulesets, 
    find_rule_files, 
    create_demo_ruleset,
    generate_cursorrules_file,
    save_cursorrules_file
)
from .task_tracker import (
    Task, 
    Phase, 
    ActionPlan, 
    TaskStatus,
    synchronize_with_cursorrules,
    generate_action_plan_from_doc
)
from .task_parser import (
    extract_tasks_from_markdown,
    extract_action_plan_from_doc,
    parse_initialization_doc
)
from .llm_connector import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMConnector,
    MultiLLMProcessor,
    ApiCredentialManager
)
from .versioning import (
    Version,
    VersionedFile,
    VersionManager
)
from .code_monitor import (
    CodebaseChange,
    CodeMonitor,
    GitChangesDetector,
    create_monitor_for_project
)
from .document_generator import DocumentGenerator

# Convenience function
def create_demo_ruleset() -> RuleSet:
    """Create a demo rule set with sample rules."""
    ruleset = RuleSet(
        name="Demo Rules",
        description="A sample rule set demonstrating various rule types"
    )
    
    ruleset.add_rule(Rule(
        content="Always respond in a friendly, conversational tone.",
        id="tone_friendly",
        priority=10,
        tags=["tone", "general"]
    ))
    
    ruleset.add_rule(Rule(
        content="When explaining technical concepts, use analogies to make them easier to understand.",
        id="explain_with_analogies",
        priority=5,
        tags=["explanations", "teaching"]
    ))
    
    ruleset.add_rule(Rule(
        content="If asked about code, provide working examples with comments explaining each step.",
        id="code_examples",
        priority=8,
        tags=["code", "examples"]
    ))
    
    return ruleset

__all__ = [
    # Core functionality
    "Rule",
    "RuleSet",
    "RuleExecutor",
    
    # Parser functionality
    "parse_file",
    "parse_directory",
    "parse_markdown",
    
    # Utilities
    "create_demo_ruleset",
    "merge_rulesets",
    "find_rule_files",
    
    # Cursor Rules file generation
    "generate_cursorrules_file",
    "save_cursorrules_file",
    
    # Task tracking
    "Task",
    "Phase",
    "ActionPlan",
    "TaskStatus",
    "synchronize_with_cursorrules",
    "generate_action_plan_from_doc",
    
    # Task parsing
    "extract_tasks_from_markdown",
    "extract_action_plan_from_doc",
    "parse_initialization_doc",
    
    # Document generation
    "DocumentGenerator",
    
    # LLM integration
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "LLMConnector",
    "MultiLLMProcessor",
    "ApiCredentialManager",
    
    # Versioning
    "Version",
    "VersionedFile",
    "VersionManager",
    
    # Code monitoring
    "CodebaseChange",
    "CodeMonitor",
    "GitChangesDetector",
    "create_monitor_for_project"
] 