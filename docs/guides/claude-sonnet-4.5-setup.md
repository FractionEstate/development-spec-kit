# Claude Sonnet 4.5 Setup Guide

## Overview

Claude Sonnet 4.5 is now fully supported in the Specify CLI and GitHub Copilot integration. This guide explains how to enable and use Claude Sonnet 4.5 with your Specify projects.

## Availability

Claude Sonnet 4.5 is available in **GitHub Copilot** for:

- **Copilot Pro** subscribers
- **Copilot Pro+** subscribers
- **Copilot Business** plans
- **Copilot Enterprise** plans

## Enabling Access

### For Business & Enterprise Organizations

Your organization administrator must enable Claude Sonnet 4.5:

1. Navigate to your organization's **Copilot settings**
2. Enable the **Claude Sonnet 4.5 policy**
3. Once enabled, all users in the organization will see Claude Sonnet 4.5 in the model picker

### For Individual Users (Free, Pro, Pro+)

You have two options:

#### Option 1: Native Copilot Access

If Claude Sonnet 4.5 is enabled in your Copilot plan, it will appear automatically in the model picker.

#### Option 2: BYOK (Bring Your Own Key)

If you have an Anthropic API key, you can add it to VS Code:

1. Open **GitHub Copilot Chat** in VS Code
2. Click the model picker dropdown
3. Select **"Manage Models..."**
4. Choose **Anthropic** as the provider
5. Enter your Anthropic API key when prompted
6. Select the Claude models you want to use

## Using Claude Sonnet 4.5 with Specify

### Initialize a New Project

```bash
specify init my-project --model claude-sonnet-4.5

```text

This will:

- Create a new Specify project with Claude Sonnet 4.5 as the default model
- Configure all GitHub Copilot prompts to reference Claude Sonnet 4.5
- Set up the `.github/` directory with appropriate configuration

### Check Available Models

```bash
specify list-models

```text

This will show all 60+ available models, including:

- `claude-sonnet-4.5` - Claude Sonnet 4.5 (latest, best for agents and coding)
- `claude-sonnet-4` - Claude Sonnet 4
- `claude-3.7-sonnet` - Claude 3.7 Sonnet
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-opus` - Claude 3 Opus
- `claude-3-sonnet` - Claude 3 Sonnet
- `claude-3-haiku` - Claude 3 Haiku

### Select Model in VS Code

Once your project is initialized, you can select Claude Sonnet 4.5 in VS Code:

1. Open **GitHub Copilot Chat** (`Ctrl+Alt+I` or `Cmd+Option+I`)
2. Click the **model picker** dropdown (top of chat panel)
3. Select **claude-sonnet-4.5**

The model will now be used for:

- Chat conversations
- Ask mode (`@workspace`)
- Edit mode (inline edits)
- Agent mode (autonomous coding)

## Claude Sonnet 4.5 Capabilities

Claude Sonnet 4.5 is particularly well-suited for:

### Coding & Development

- Superior code generation and refactoring
- Enhanced debugging and error correction
- Multi-step coding projects
- Advanced tool use and function calling

### Agentic Workflows

- Best-in-class for autonomous agents
- Excellent instruction following
- Superior tool selection and error correction
- Long-running task management

### Extended Reasoning

- Step-by-step thinking with visible reasoning summaries
- Complex problem-solving
- Deep research and analysis
- Multi-step planning

### Domain Expertise

- Enhanced knowledge in coding, finance, and cybersecurity
- 200K context window for large codebases
- Accurate and detailed responses for long-running tasks

## Troubleshooting

### Claude Sonnet 4.5 Not Showing in Model Picker

**For Business/Enterprise users:**

- Contact your organization administrator
- Ask them to enable the "Claude Sonnet 4.5" policy in Copilot settings
- Wait for gradual rollout (may take a few hours)

**For Pro/Pro+ users:**

- Check if your plan includes Claude Sonnet 4.5 access
- Try using BYOK with your own Anthropic API key
- Ensure VS Code is updated to the latest version

### Model Selection Not Persisting

- Verify `.specify/config/models.json` exists in your project
- Check that the model ID is spelled correctly: `claude-sonnet-4.5`
- Run `specify status` to confirm configuration

### API Key Issues (BYOK)

- Ensure your Anthropic API key is valid and has credits
- Check that the key has access to Claude Sonnet 4.5
- Verify the key was entered correctly in VS Code settings

## Model Comparison

| Model | Best For | Context | Speed |
|-------|----------|---------|-------|
| **claude-sonnet-4.5** | Agents, coding, extended reasoning | 200K | Fast with optional extended thinking |
| claude-sonnet-4 | General AI tasks, high-volume use | 200K | Fast |
| claude-3.7-sonnet | Hybrid reasoning, content generation | 200K | Fast with thinking mode |
| claude-3-5-sonnet-20241022 | Balanced performance | 200K | Fast |
| claude-3-opus | Highest intelligence (legacy) | 200K | Slower |
| claude-3-haiku | Speed and cost efficiency | 200K | Very fast |

## Resources

- [Anthropic Claude Documentation](https://www.anthropic.com/claude/sonnet)
- [GitHub Copilot Models Documentation](https://docs.github.com/copilot/using-github-copilot/using-github-copilot-chat)
- [Specify CLI Documentation](../README.md)
- [GitHub Models Catalog](https://github.com/marketplace/models)

## Pricing

**GitHub Copilot subscription** includes access to Claude Sonnet 4.5 (subject to organizational policies).

**BYOK pricing** (if using your own Anthropic API key):

- **Input**: $3 per million tokens
- **Output**: $15 per million tokens
- **Prompt caching**: Up to 90% cost savings
- **Batch processing**: 50% cost savings

See [Anthropic's pricing page](https://www.anthropic.com/pricing) for current rates.

## Next Steps

1. **Initialize a project**: `specify init my-project --model claude-sonnet-4.5`
2. **Open VS Code**: Navigate to your project directory
3. **Select Claude Sonnet 4.5**: Use the Copilot Chat model picker
4. **Start coding**: Use `/plan`, `/specify`, `/implement` slash commands

For more information on Spec-Driven Development with Copilot, see the [Quickstart Guide](../getting-started/quickstart.md).
