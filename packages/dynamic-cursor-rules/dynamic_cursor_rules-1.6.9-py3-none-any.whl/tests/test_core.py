"""
Tests for the core module.
"""
import json
import unittest
from pathlib import Path
import tempfile

from cursor_rules import Rule, RuleSet

class TestRule(unittest.TestCase):
    """Tests for the Rule class."""
    
    def test_create_rule(self):
        """Test creating a Rule."""
        rule = Rule(content="Test rule content", id="test_rule")
        self.assertEqual(rule.content, "Test rule content")
        self.assertEqual(rule.id, "test_rule")
        self.assertEqual(rule.priority, 0)
        self.assertEqual(rule.tags, [])
        self.assertTrue(rule.enabled)
        
    def test_rule_validation(self):
        """Test rule validation."""
        # Valid rule
        rule = Rule(content="Test rule content", id="test_rule")
        errors = rule.validate()
        self.assertEqual(errors, [])
        
        # Invalid rule - empty content
        rule = Rule(content="", id="test_rule")
        errors = rule.validate()
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Content cannot be empty" in error for error in errors))

class TestRuleSet(unittest.TestCase):
    """Tests for the RuleSet class."""
    
    def test_create_ruleset(self):
        """Test creating a RuleSet."""
        ruleset = RuleSet(name="Test Rules")
        self.assertEqual(ruleset.name, "Test Rules")
        self.assertIsNone(ruleset.description)
        self.assertEqual(ruleset.rules, [])
        
    def test_add_rule(self):
        """Test adding a rule to a ruleset."""
        ruleset = RuleSet(name="Test Rules")
        rule = Rule(content="Test rule content", id="test_rule")
        ruleset.add_rule(rule)
        self.assertEqual(len(ruleset.rules), 1)
        self.assertEqual(ruleset.rules[0].id, "test_rule")
        
    def test_remove_rule(self):
        """Test removing a rule from a ruleset."""
        ruleset = RuleSet(name="Test Rules")
        rule = Rule(content="Test rule content", id="test_rule")
        ruleset.add_rule(rule)
        
        # Remove existing rule
        result = ruleset.remove_rule("test_rule")
        self.assertTrue(result)
        self.assertEqual(len(ruleset.rules), 0)
        
        # Remove non-existent rule
        result = ruleset.remove_rule("nonexistent")
        self.assertFalse(result)
        
    def test_ruleset_validation(self):
        """Test ruleset validation."""
        # Valid ruleset
        ruleset = RuleSet(name="Test Rules")
        rule = Rule(content="Test rule content", id="test_rule")
        ruleset.add_rule(rule)
        errors = ruleset.validate()
        self.assertEqual(errors, [])
        
        # Invalid ruleset - duplicate rule IDs
        ruleset = RuleSet(name="Test Rules")
        rule1 = Rule(content="Rule 1", id="duplicate_id")
        rule2 = Rule(content="Rule 2", id="duplicate_id")
        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)
        errors = ruleset.validate()
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Duplicate rule ID" in error for error in errors))
        
    def test_serialize_deserialize(self):
        """Test serializing and deserializing a ruleset."""
        # Create a ruleset
        ruleset = RuleSet(
            name="Test Rules", 
            description="Test description"
        )
        rule = Rule(
            content="Test rule content", 
            id="test_rule",
            priority=5,
            tags=["test", "example"]
        )
        ruleset.add_rule(rule)
        
        # Serialize to file
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            ruleset.save(tmp_path)
            
            # Deserialize from file
            loaded_ruleset = RuleSet.load(tmp_path)
            
            # Check values
            self.assertEqual(loaded_ruleset.name, "Test Rules")
            self.assertEqual(loaded_ruleset.description, "Test description")
            self.assertEqual(len(loaded_ruleset.rules), 1)
            
            loaded_rule = loaded_ruleset.rules[0]
            self.assertEqual(loaded_rule.id, "test_rule")
            self.assertEqual(loaded_rule.content, "Test rule content")
            self.assertEqual(loaded_rule.priority, 5)
            self.assertEqual(loaded_rule.tags, ["test", "example"])
            self.assertTrue(loaded_rule.enabled)
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)

if __name__ == "__main__":
    unittest.main() 