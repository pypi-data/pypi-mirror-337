"""
Core functionality for the Cursor Rules system.
"""
import json
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import os
from enum import Enum

class RuleStatus(Enum):
    """Status enum for rules."""
    ACTIVE = "active"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"

class ProjectPhase(Enum):
    """Enum representing the current phase of the project."""
    SETUP = "setup"
    FOUNDATION = "foundation"
    FEATURE_DEVELOPMENT = "feature_development"
    REFINEMENT = "refinement"
    MAINTENANCE = "maintenance"

class ComponentStatus(Enum):
    """Status enum for components within the project."""
    PLANNED = "planned"
    IN_DEVELOPMENT = "in_development"
    STABLE = "stable"
    DEPRECATED = "deprecated"
    
@dataclass
class Component:
    """Represents a component or module in the project."""
    name: str
    path_pattern: str
    status: ComponentStatus = ComponentStatus.PLANNED
    description: str = ""
    owners: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

@dataclass
class ProjectState:
    """
    Tracks the current state of the project for dynamic rule generation.
    """
    name: str
    description: str = ""
    version: str = "0.1.0"
    phase: ProjectPhase = ProjectPhase.SETUP
    components: Dict[str, Component] = field(default_factory=dict)
    active_features: List[str] = field(default_factory=list)
    tech_stack: Dict[str, List[str]] = field(default_factory=dict)
    directory_structure: Dict[str, str] = field(default_factory=dict)
    last_updated: str = ""
    
    def add_component(self, component: Component) -> None:
        """Add or update a component in the project state."""
        self.components[component.name] = component
    
    def update_component_status(self, name: str, status: ComponentStatus) -> bool:
        """Update the status of a component."""
        if name in self.components:
            self.components[name].status = status
            return True
        return False
    
    def set_active_features(self, features: List[str]) -> None:
        """Set the list of currently active features."""
        self.active_features = features
    
    def get_active_components(self) -> List[Component]:
        """Get all components that are in active development."""
        return [comp for comp in self.components.values() 
                if comp.status == ComponentStatus.IN_DEVELOPMENT]
    
    def get_current_focus(self) -> str:
        """Get a description of the current development focus."""
        if not self.active_features:
            return f"Project is in {self.phase.value} phase" 
            
        components = self.get_active_components()
        if components:
            component_names = [c.name for c in components]
            return f"Currently developing: {', '.join(self.active_features)} in components: {', '.join(component_names)}"
        
        return f"Currently focusing on: {', '.join(self.active_features)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the project state to a dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "phase": self.phase.value,
            "components": {
                name: {
                    "name": comp.name,
                    "path_pattern": comp.path_pattern,
                    "status": comp.status.value,
                    "description": comp.description,
                    "owners": comp.owners,
                    "dependencies": comp.dependencies,
                    "created_at": comp.created_at,
                    "updated_at": comp.updated_at
                } for name, comp in self.components.items()
            },
            "active_features": self.active_features,
            "tech_stack": self.tech_stack,
            "directory_structure": self.directory_structure,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectState':
        """Create a ProjectState instance from a dictionary."""
        components = {}
        for name, comp_data in data.get("components", {}).items():
            components[name] = Component(
                name=comp_data["name"],
                path_pattern=comp_data["path_pattern"],
                status=ComponentStatus(comp_data["status"]),
                description=comp_data.get("description", ""),
                owners=comp_data.get("owners", []),
                dependencies=comp_data.get("dependencies", []),
                created_at=comp_data.get("created_at", ""),
                updated_at=comp_data.get("updated_at", "")
            )
            
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "0.1.0"),
            phase=ProjectPhase(data.get("phase", "setup")),
            components=components,
            active_features=data.get("active_features", []),
            tech_stack=data.get("tech_stack", {}),
            directory_structure=data.get("directory_structure", {}),
            last_updated=data.get("last_updated", "")
        )

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