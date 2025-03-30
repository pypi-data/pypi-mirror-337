# Setting Up API Keys

Dynamic Cursor Rules can integrate with various LLM providers to enhance document generation, suggestions, and analysis. This guide will show you how to set up and manage your API keys.

## Supported LLM Providers

Currently, the following LLM providers are supported:

- **OpenAI** (GPT-4, etc.)
- **Anthropic** (Claude, etc.)

## Setting Up API Keys

You can set up your API keys in one of two ways:

### Option 1: Using Environment Variables

Set the appropriate environment variables for your provider:

For OpenAI:
```bash
# On Linux/macOS
export OPENAI_API_KEY=your_key_here

# On Windows PowerShell
$env:OPENAI_API_KEY = "your_key_here"

# On Windows Command Prompt
set OPENAI_API_KEY=your_key_here
```

For Anthropic:
```bash
# On Linux/macOS
export ANTHROPIC_API_KEY=your_key_here

# On Windows PowerShell
$env:ANTHROPIC_API_KEY = "your_key_here"

# On Windows Command Prompt
set ANTHROPIC_API_KEY=your_key_here
```

### Option 2: Using the CLI Command (Recommended)

The `cursor-rules` CLI provides a command to configure your API keys securely:

```bash
# For OpenAI
cursor-rules llm config --provider openai --api-key your_key_here

# For Anthropic
cursor-rules llm config --provider anthropic --api-key your_key_here
```

This method securely stores your API keys in `~/.cursor-rules/credentials` with basic obfuscation.

## Verifying API Key Setup

To check if your API keys are properly configured, use the list command:

```bash
cursor-rules llm list
```

This will show you which providers are correctly configured and available for use.

## Testing Your API Keys

You can test your API keys with:

```bash
# Test all configured providers
cursor-rules llm test

# Test a specific provider
cursor-rules llm test --provider openai
cursor-rules llm test --provider anthropic

# Test with a custom query
cursor-rules llm test --query "Generate three coding standards for a Python project"
```

## Using LLMs with Other Commands

Once your API keys are configured, any command that needs LLM integration will work automatically.

For example, to generate documentation with a specific provider:

```bash
cursor-rules documents your_init_file.md -o output_dir --provider openai
```

## API Key Security

Your API keys are stored with basic obfuscation in `~/.cursor-rules/credentials`. For maximum security:

1. Never commit this file to version control
2. Use environment variables in CI/CD pipelines
3. Consider using API keys with usage limits and appropriate permissions

## Troubleshooting

If you encounter issues with your API keys:

1. Verify the key is valid and has not expired
2. Check that you're using the correct key format
3. Ensure you have sufficient credits/quota on your account
4. Try using environment variables instead of stored credentials
5. Check that the required packages are installed:
   ```bash
   pip install dynamic-cursor-rules[llm]
   ```

For further assistance, please open an issue in the project repository. 