"""
Executor for applying rules to AI interactions.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional

from .core import RuleSet, Rule

@dataclass
class RuleExecutor:
    """Executor for applying rules within a production environment."""
    ruleset: Optional[RuleSet] = None
    transformers: List[Callable[[Rule, Dict[str, Any]], Rule]] = field(default_factory=list)
    
    def apply_rules(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply relevant rules to the given context."""
        if not self.ruleset:
            return context
        
        # Get applicable rules (enabled and matching tags)
        rules = self._get_applicable_rules(context)
        
        # Apply transformers to each rule
        for transformer in self.transformers:
            rules = [transformer(rule, context) for rule in rules]
        
        # Combine rule content into instructions
        instructions = "\n\n".join([rule.content for rule in rules])
        
        # Update context
        result = context.copy()
        result['instructions'] = instructions
        result['applied_rules'] = [rule.id for rule in rules]
        
        return result
    
    def _get_applicable_rules(self, context: Dict[str, Any]) -> List[Rule]:
        """Get rules that apply to the current context."""
        if not self.ruleset:
            return []
            
        # Start with enabled rules
        rules = [rule for rule in self.ruleset.rules if rule.enabled]
        
        # Filter by tags if specified
        if 'tags' in context and context['tags']:
            requested_tags = set(context['tags'])
            rules = [
                rule for rule in rules 
                if not rule.tags or any(tag in requested_tags for tag in rule.tags)
            ]
        
        # Sort by priority (higher first)
        return sorted(rules, key=lambda r: r.priority, reverse=True) 