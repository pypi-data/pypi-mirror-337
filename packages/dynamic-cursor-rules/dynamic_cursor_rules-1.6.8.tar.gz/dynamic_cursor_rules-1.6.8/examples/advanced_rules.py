"""
Advanced example of using Cursor Rules.
"""
import os
from cursor_rules import RuleSet, Rule, RuleExecutor, parse_markdown

# Example markdown content
MARKDOWN_RULES = """
# Advanced Rules

These rules demonstrate more complex behaviors.

## Custom Persona

You should respond as a friendly expert who is patient and thorough.

## Technical Precision

When discussing technical topics, prioritize accuracy over simplicity.

## Contextual Examples

Provide examples that are relevant to the user's domain or industry.
"""

def create_markdown_file(content, filename):
    """Create a markdown file with the given content."""
    with open(filename, "w") as f:
        f.write(content)
    return filename

def transformer_add_metadata(rule, context):
    """Example transformer that adds metadata to rules."""
    # Create a new rule to avoid modifying the original
    new_rule = Rule(
        id=rule.id,
        content=rule.content,
        priority=rule.priority,
        tags=rule.tags,
        enabled=rule.enabled,
        metadata=rule.metadata.copy()
    )
    
    # Add application metadata
    new_rule.metadata["applied_at"] = "2025-03-29"
    new_rule.metadata["context_type"] = context.get("context_type", "general")
    
    return new_rule

def transformer_personalize(rule, context):
    """Example transformer that personalizes content based on context."""
    # Create a new rule to avoid modifying the original
    new_rule = Rule(
        id=rule.id,
        content=rule.content,
        priority=rule.priority,
        tags=rule.tags,
        enabled=rule.enabled,
        metadata=rule.metadata.copy()
    )
    
    # Personalize content if user name is available
    if "user_name" in context:
        user_name = context["user_name"]
        if "Custom Persona" in rule.id:
            new_rule.content = f"Remember to address {user_name} by name. " + rule.content
    
    return new_rule

def main():
    # Create a markdown file
    md_file = create_markdown_file(MARKDOWN_RULES, "advanced_rules.md")
    
    # Parse the markdown file
    ruleset = parse_markdown(MARKDOWN_RULES)
    print(f"Parsed ruleset: {ruleset.name} with {len(ruleset.rules)} rules")
    
    # Create an executor with transformers
    executor = RuleExecutor(ruleset)
    executor.transformers.append(transformer_add_metadata)
    executor.transformers.append(transformer_personalize)
    
    # Example contexts
    contexts = [
        {
            "user_input": "How do databases work?",
            "context_type": "technical",
            "tags": ["technical"]
        },
        {
            "user_input": "Can you help me with Python?",
            "context_type": "programming",
            "user_name": "Alice",
            "tags": ["technical"]
        }
    ]
    
    # Apply rules to different contexts
    for i, context in enumerate(contexts, 1):
        result = executor.apply_rules(context)
        
        print(f"\n--- Context {i} ---")
        print(f"User input: {context['user_input']}")
        print("\nApplied instructions:")
        print(result["instructions"])
        print("\nApplied rule IDs:", result["applied_rules"])
    
    # Clean up
    if os.path.exists(md_file):
        os.remove(md_file)

if __name__ == "__main__":
    main() 