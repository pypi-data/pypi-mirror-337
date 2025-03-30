"""
Core functionality for the Cursor Rules system.
"""
import json
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

@dataclass
class Rule:
    """A single rule for an AI assistant to follow."""
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: int = 0
    tags: List[str] = field(default_factory=list)
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate the rule and return any error messages."""
        errors = []
        if not self.content or not self.content.strip():
            errors.append(f"Rule {self.id}: Content cannot be empty")
        if not self.id or not self.id.strip():
            errors.append("Rule ID cannot be empty")
        return errors

@dataclass
class RuleSet:
    """A collection of rules for an AI assistant to follow."""
    name: str
    description: Optional[str] = None
    rules: List[Rule] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_rule(self, rule: Union[Rule, str], **kwargs) -> None:
        """
        Add a rule to the rule set.
        
        Args:
            rule: Either a Rule object or a string with rule content
            **kwargs: If rule is a string, these parameters are passed to the Rule constructor
        """
        if isinstance(rule, str):
            rule = Rule(content=rule, **kwargs)
        self.rules.append(rule)
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID, return True if found and removed."""
        initial_len = len(self.rules)
        self.rules = [r for r in self.rules if r.id != rule_id]
        return len(self.rules) < initial_len
    
    def validate(self) -> List[str]:
        """Validate the rule set and return any error messages."""
        errors = []
        
        if not self.name or not self.name.strip():
            errors.append("Rule set name cannot be empty")
        
        # Check for duplicate rule IDs
        rule_ids = set()
        for rule in self.rules:
            if rule.id in rule_ids:
                errors.append(f"Duplicate rule ID: {rule.id}")
            else:
                rule_ids.add(rule.id)
            
            # Validate individual rule
            errors.extend(rule.validate())
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if the rule set is valid."""
        return len(self.validate()) == 0
    
    def save(self, filepath: str) -> None:
        """Save rule set to a file."""
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'RuleSet':
        """Load a rule set from a file."""
        path = Path(filepath)
        
        with open(path, 'r') as f:
            if path.suffix.lower() == '.json':
                data = json.load(f)
                return cls.from_dict(data)
            else:
                from .parser import parse_file
                return parse_file(filepath)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RuleSet':
        """Create a rule set from a dictionary."""
        rules_data = data.pop('rules', [])
        ruleset = cls(**{k: v for k, v in data.items() if k != 'rules'})
        
        for rule_data in rules_data:
            rule = Rule(**rule_data)
            ruleset.add_rule(rule)
        
        return ruleset 