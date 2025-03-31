"""
Test the cursorrules file generation functionality.
"""
import unittest
import tempfile
from pathlib import Path

from cursor_rules import (
    RuleSet, 
    Rule, 
    generate_cursorrules_file,
    save_cursorrules_file
)

class TestCursorRulesGeneration(unittest.TestCase):
    """Tests for generating .cursorrules files."""
    
    def test_generate_cursorrules_file(self):
        """Test generating a .cursorrules file."""
        # Create a simple ruleset
        ruleset = RuleSet(
            name="Test Project",
            description="A test project for unit testing"
        )
        
        # Add some rules
        ruleset.add_rule(Rule(
            content="Use TypeScript for all frontend code",
            id="use_typescript",
            tags=["frontend"]
        ))
        
        ruleset.add_rule(Rule(
            content="Write unit tests for all components",
            id="test_components",
            priority=9,
            tags=["testing"]
        ))
        
        # Create project info
        project_info = {
            "tech_stack": {
                "Frontend": ["React", "TypeScript"],
                "Backend": ["Node.js", "Express"]
            },
            "naming_conventions": {
                "Components": "PascalCase",
                "Functions": "camelCase"
            }
        }
        
        # Generate the .cursorrules file content
        content = generate_cursorrules_file(ruleset, project_info)
        
        # Check if the content contains all the necessary sections
        self.assertIn("# .cursorrules for Test Project", content)
        self.assertIn("# A test project for unit testing", content)
        self.assertIn("# Tech Stack:", content)
        self.assertIn("# Frontend: React, TypeScript", content)
        self.assertIn("# Backend: Node.js, Express", content)
        self.assertIn("# Naming Conventions:", content)
        self.assertIn("# - Components: PascalCase", content)
        self.assertIn("# - Functions: camelCase", content)
        self.assertIn("# Rules:", content)
        self.assertIn("## frontend Rules:", content)
        self.assertIn("# use_typescript: Use TypeScript for all frontend code", content)
        self.assertIn("## testing Rules:", content)
        self.assertIn("# test_components: Write unit tests for all components", content)
    
    def test_save_cursorrules_file(self):
        """Test saving a .cursorrules file."""
        # Create a simple ruleset
        ruleset = RuleSet(
            name="Test Project",
            description="A test project for unit testing"
        )
        
        # Add some rules
        ruleset.add_rule(Rule(
            content="Use TypeScript for all frontend code",
            id="use_typescript",
            tags=["frontend"]
        ))
        
        # Create project info
        project_info = {
            "tech_stack": {
                "Frontend": ["React", "TypeScript"]
            }
        }
        
        # Create a temporary file to save to
        with tempfile.NamedTemporaryFile(suffix=".cursorrules", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save the .cursorrules file
            save_cursorrules_file(ruleset, tmp_path, project_info)
            
            # Check if the file exists
            self.assertTrue(Path(tmp_path).exists())
            
            # Read the file and check its contents
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.assertIn("# .cursorrules for Test Project", content)
            self.assertIn("# A test project for unit testing", content)
            self.assertIn("# Tech Stack:", content)
            self.assertIn("# Frontend: React, TypeScript", content)
            self.assertIn("# Rules:", content)
            self.assertIn("## frontend Rules:", content)
            self.assertIn("# use_typescript: Use TypeScript for all frontend code", content)
        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)

if __name__ == "__main__":
    unittest.main() 