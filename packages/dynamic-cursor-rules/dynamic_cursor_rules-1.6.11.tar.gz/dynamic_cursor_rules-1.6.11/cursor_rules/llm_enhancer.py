"""
LLM enhancer for cursor rules.

This module uses LLM providers to enhance cursor rules documents.
"""

import json
from typing import Dict, Any, Optional, List

from .core import RuleSet
from .llm_connector import LLMConnector, LLMProvider, LLMRequest

def enhance_cursorrules(
    ruleset: RuleSet,
    project_info: Dict[str, Any],
    provider_name: str,
    api_key: str
) -> str:
    """
    Use an LLM to enhance the rules content.
    
    Args:
        ruleset: The RuleSet object containing rules
        project_info: Dictionary with project information
        provider_name: The LLM provider name ('openai' or 'anthropic')
        api_key: API key for the LLM provider
        
    Returns:
        Enhanced .cursorrules file content as a string
    """
    # Map the provider name to enum
    try:
        provider = LLMProvider(provider_name.lower())
    except ValueError:
        raise ValueError(f"Invalid provider: {provider_name}. Must be one of: openai, anthropic")
    
    # Set up the LLM connector
    connector = LLMConnector()
    connector.set_api_key(provider, api_key)
    
    # Prepare the system message
    system_message = """
    You are an expert at creating .cursorrules files for Cursor IDE. These files provide guidance to AI assistants
    when users are working on a project. Your task is to take the provided rules and project information and create 
    a well-formatted, comprehensive .cursorrules file that includes the original content but enhances it with:
    
    1. Better organization and categorization of rules
    2. More detailed context where appropriate
    3. Consistent formatting
    4. Default best practices for the technology stack
    
    The output should be in a format that can be directly saved as a .cursorrules file.
    """
    
    # Prepare the user message with the ruleset and project info
    user_message = f"""
    Project name: {project_info.get('name', ruleset.name)}
    Project description: {project_info.get('description', ruleset.description or "")}
    
    Tech stack:
    {json.dumps(project_info.get('tech_stack', {}), indent=2)}
    
    Naming conventions:
    {json.dumps(project_info.get('naming_conventions', {}), indent=2)}
    
    Directory structure:
    {json.dumps(project_info.get('directory_structure', {}), indent=2)}
    
    Rules:
    """
    
    # Add all rules to the user message
    for rule in ruleset.rules:
        if rule.enabled:
            tags = ", ".join(rule.tags) if rule.tags else "General"
            user_message += f"- [{tags}] {rule.content}\n"
    
    # Create and send the request
    request = LLMRequest(
        system_message=system_message,
        prompt=user_message,
        provider=provider,
        temperature=0.3,  # Lower temperature for more consistent output
        max_tokens=2000   # Allow for longer responses
    )
    
    response = connector.request(request)
    
    # Return the enhanced content
    return response.text.strip() 