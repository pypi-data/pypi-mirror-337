"""
Basic example of using Cursor Rules.
"""
import json
from cursor_rules import RuleSet, Rule, RuleExecutor

def main():
    # Create a rule set
    ruleset = RuleSet(
        name="Basic Rules",
        description="A basic set of rules for an AI assistant"
    )
    
    # Add some rules
    ruleset.add_rule(Rule(
        content="Always be friendly and approachable in your responses.",
        id="friendly_tone",
        priority=10,
        tags=["tone"]
    ))
    
    ruleset.add_rule(Rule(
        content="Keep responses concise and to the point.",
        id="concise",
        priority=5,
        tags=["style"]
    ))
    
    ruleset.add_rule(Rule(
        content="When explaining code, include comments explaining each step.",
        id="code_comments",
        priority=8,
        tags=["code", "programming"]
    ))
    
    # Save the rule set to a file
    ruleset.save("basic_rules.json")
    print(f"Rule set saved to basic_rules.json")
    
    # Apply the rules in different contexts
    executor = RuleExecutor(ruleset)
    
    # General context
    general_context = {
        "user_input": "Tell me about yourself"
    }
    
    # Programming context
    programming_context = {
        "user_input": "How do I write a for loop in Python?",
        "tags": ["programming"]
    }
    
    # Apply rules to contexts
    general_result = executor.apply_rules(general_context)
    programming_result = executor.apply_rules(programming_context)
    
    # Print results
    print("\nGeneral context instructions:")
    print(general_result["instructions"])
    print("\nProgramming context instructions:")
    print(programming_result["instructions"])
    print("\nApplied rules for programming context:", programming_result["applied_rules"])

if __name__ == "__main__":
    main() 