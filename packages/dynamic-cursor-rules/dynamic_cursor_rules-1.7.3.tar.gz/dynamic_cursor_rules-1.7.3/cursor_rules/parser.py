"""
Parser for Cursor Rules from various formats.
"""
import json
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any

from .core import RuleSet, Rule

def parse_markdown(content: str) -> RuleSet:
    """Parse rules from a markdown file."""
    lines = content.strip().split('\n')
    
    # Default values
    ruleset_name = "Default RuleSet"
    ruleset_desc = None
    
    # Extract rule set name and description
    for i, line in enumerate(lines):
        if line.startswith("# "):
            ruleset_name = line[2:].strip()
            
            # Check for description
            desc_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                if lines[j].strip():  # Ignore empty lines
                    desc_lines.append(lines[j])
                j += 1
                
            if desc_lines:
                ruleset_desc = '\n'.join(desc_lines).strip()
            break
    
    ruleset = RuleSet(name=ruleset_name, description=ruleset_desc)
    
    # Extract rules
    rule_pattern = re.compile(r'^## (.+)$')
    current_rule = None
    current_content = []
    
    for line in lines:
        match = rule_pattern.match(line)
        if match:
            # Save previous rule if exists
            if current_rule and current_content:
                ruleset.add_rule(Rule(
                    id=current_rule,
                    content='\n'.join(current_content).strip()
                ))
            
            # Start new rule
            current_rule = match.group(1).strip()
            current_content = []
        elif current_rule is not None:
            current_content.append(line)
    
    # Add the last rule
    if current_rule and current_content:
        ruleset.add_rule(Rule(
            id=current_rule,
            content='\n'.join(current_content).strip()
        ))
    
    return ruleset

def parse_file(filepath: str) -> RuleSet:
    """Parse rules from a file based on its extension."""
    path = Path(filepath)
    content = path.read_text(encoding="utf-8")
    
    if path.suffix.lower() == '.md':
        return parse_markdown(content)
    elif path.suffix.lower() in ('.yaml', '.yml'):
        data = yaml.safe_load(content)
        return RuleSet.from_dict(data)
    elif path.suffix.lower() == '.json':
        data = json.loads(content)
        return RuleSet.from_dict(data)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

def parse_directory(dirpath: str, recursive: bool = True) -> List[RuleSet]:
    """Parse all rule files in a directory."""
    path = Path(dirpath)
    rulesets = []
    
    pattern = "**/*" if recursive else "*"
    
    for file in path.glob(pattern):
        if file.is_file() and file.suffix.lower() in ('.md', '.yaml', '.yml', '.json'):
            try:
                ruleset = parse_file(str(file))
                rulesets.append(ruleset)
            except Exception as e:
                print(f"Failed to parse {file}: {e}")
    
    return rulesets 