"""
Utility functions for the Cursor Rules system.
"""
import os
import json
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .core import RuleSet, Rule

def merge_rulesets(rulesets: List[RuleSet], name: str = "Merged RuleSet") -> RuleSet:
    """
    Merge multiple rulesets into one.
    
    Args:
        rulesets: List of RuleSet objects to merge
        name: Name for the merged ruleset
        
    Returns:
        A new RuleSet containing all rules from the input rulesets
    """
    merged = RuleSet(name=name)
    
    # Track rule IDs to avoid duplicates
    rule_ids = set()
    
    for ruleset in rulesets:
        # Merge metadata
        for key, value in ruleset.metadata.items():
            if key not in merged.metadata:
                merged.metadata[key] = value
        
        # Add rules, skipping duplicates
        for rule in ruleset.rules:
            if rule.id not in rule_ids:
                merged.add_rule(rule)
                rule_ids.add(rule.id)
    
    return merged

def find_rule_files(directory: str, extensions: List[str] = None) -> List[str]:
    """
    Find all potential rule files in a directory.
    
    Args:
        directory: Directory to search
        extensions: File extensions to include (defaults to ['.md', '.json', '.yaml', '.yml'])
        
    Returns:
        List of file paths
    """
    if extensions is None:
        extensions = ['.md', '.json', '.yaml', '.yml']
    
    rule_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                rule_files.append(os.path.join(root, file))
    
    return rule_files

def create_demo_ruleset() -> RuleSet:
    """
    Create a demo rule set with sample rules.
    
    Returns:
        A RuleSet with sample rules
    """
    ruleset = RuleSet(
        name="Demo Rules",
        description="A sample rule set demonstrating various rule types"
    )
    
    # Add some sample rules
    rule1 = Rule(
        content="Always respond in a friendly, conversational tone.",
        rule_id="tone_friendly",
        priority=10,
        tags=["tone", "general"]
    )
    
    rule2 = Rule(
        content="When explaining technical concepts, use analogies to make them easier to understand.",
        rule_id="explain_with_analogies",
        priority=5,
        tags=["explanations", "teaching"]
    )
    
    rule3 = Rule(
        content="If asked about code, provide working examples with comments explaining each step.",
        rule_id="code_examples",
        priority=8,
        tags=["code", "examples"]
    )
    
    ruleset.add_rule(rule1)
    ruleset.add_rule(rule2)
    ruleset.add_rule(rule3)
    
    return ruleset

def generate_cursorrules_file(
    ruleset: RuleSet,
    project_info: Optional[Dict[str, Any]] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generate a .cursorrules file from a RuleSet and project information.
    
    Args:
        ruleset: The RuleSet object containing rules
        project_info: Optional dictionary with project information
        provider: Optional LLM provider name ('openai' or 'anthropic')
        api_key: Optional API key for the LLM provider
        
    Returns:
        String content for a .cursorrules file in markdown format
    """
    if project_info is None:
        project_info = {}
    
    # Check if we should use an LLM to enhance the file
    if provider and api_key:
        try:
            from .llm_enhancer import enhance_cursorrules
            return enhance_cursorrules(ruleset, project_info, provider, api_key)
        except Exception as e:
            print(f"Warning: Failed to enhance cursorrules with {provider}: {e}")
            # Fall back to standard generation
    
    # Default values
    project_name = project_info.get('name', ruleset.name)
    project_description = project_info.get('description', ruleset.description or "")
    tech_stack = project_info.get('tech_stack', {})
    
    # Start with header - using proper markdown formatting
    content = [
        f"# .cursorrules for {project_name}",
        "",
        "## Overview",
        project_description,
        ""
    ]
    
    # Add tech stack if available
    if tech_stack:
        content.append("## Tech Stack")
        for category, technologies in tech_stack.items():
            if isinstance(technologies, list):
                tech_str = ", ".join(technologies)
            else:
                tech_str = str(technologies)
            content.append(f"**{category}**: {tech_str}")
        content.append("")
    
    # Add naming conventions if available
    if 'naming_conventions' in project_info:
        content.append("## Naming Conventions")
        for item, convention in project_info['naming_conventions'].items():
            content.append(f"- **{item}**: {convention}")
        content.append("")
    
    # Add directory structure if available
    if 'directory_structure' in project_info:
        content.append("## Directory Structure")
        for directory, description in project_info['directory_structure'].items():
            content.append(f"- **{directory}**: {description}")
        content.append("")
    
    # Add rules section
    content.append("## Rules")
    content.append("")
    
    # Group rules by tag for better organization
    rules_by_tag = {}
    for rule in ruleset.rules:
        if not rule.enabled:
            continue
            
        if not rule.tags:
            tag = "General"
        else:
            # Use the first tag as primary category
            tag = rule.tags[0]
            
        if tag not in rules_by_tag:
            rules_by_tag[tag] = []
        rules_by_tag[tag].append(rule)
    
    # Sort rules by priority within each tag
    for tag, rules in rules_by_tag.items():
        content.append(f"### {tag} Rules")
        
        # Sort by priority (higher first)
        for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
            content.append(f"- **{rule.id}**: {rule.content}")
        
        content.append("")
    
    # Add any additional sections from project_info
    for section, text in project_info.get('additional_sections', {}).items():
        content.append(f"## {section}")
        content.append(text)
        content.append("")
    
    # Join all lines into a single string
    return "\n".join(content)

def save_cursorrules_file(
    ruleset: RuleSet,
    filepath: str,
    project_info: Optional[Dict[str, Any]] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Generate and save a .cursorrules file.
    
    Args:
        ruleset: The RuleSet object containing rules
        filepath: Path where to save the .cursorrules file
        project_info: Optional dictionary with project information
        provider: Optional LLM provider name ('openai' or 'anthropic')
        api_key: Optional API key for the LLM provider
    """
    content = generate_cursorrules_file(ruleset, project_info, provider, api_key)
    
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content) 