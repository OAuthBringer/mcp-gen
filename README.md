# MCP Configuration Generator

Standalone YAML-based MCP configuration generator with template interpolation and secret management.

## Why This Tool Exists

**Problem:** MCP configurations contain hardcoded paths and secrets, making them impossible to version control or share across teams/environments.

**Solution:** Separate configuration structure from secrets and environment-specific values:

- **Version control** YAML configs without exposing secrets
- **Team sharing** of standardized MCP server setups  
- **Environment portability** via template variables
- **Secret isolation** in git-ignored files

Transform this unmaintainable config:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/alice/dev/project"]
    },
    "github": {
      "command": "docker",
      "args": ["run", "-e", "GITHUB_TOKEN=ghp_actual_secret123", "github-server"]
    }
  }
}
```

Into maintainable, shareable YAML:
```yaml
variables:
  project_root: "/Users/alice/dev/project"

servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "{{ variables.project_root }}"]
  github:
    command: "docker" 
    args: ["run", "-e", "GITHUB_TOKEN={{ secrets.GITHUB_TOKEN }}", "github-server"]
```

## Installation

```bash
pip install -e .
```

## Quick Start

### Using the Examples

1. Navigate to project root:
```bash
cd /path/to/mcp-gen
```

2. Generate MCP JSON from example configuration:
```bash
python -m mcp_gen.cli generate \
  --config examples/mcp.config.yaml \
  --secrets examples/mcp.secrets.yaml
```

3. View the generated files (automatically written to configured outputs):
```bash
cat .amazonq/mcp.json
cat claude-desktop/mcp.json
```

### CLI Commands

**Generate configuration:**
```bash
python -m mcp_gen.cli generate --config config.yaml --secrets secrets.yaml --output mcp.json
```

**Generate to configured outputs (no --output needed):**
```bash
python -m mcp_gen.cli generate --config config.yaml --secrets secrets.yaml
```

**Validate configuration:**
```bash
python -m mcp_gen.cli validate --config config.yaml
```

## Configuration Format

**mcp.config.yaml:**
```yaml
version: "1.0"

outputs:
  - "{{ variables.project_root }}/.amazonq/mcp.json"
  - "{{ variables.project_root }}/claude-desktop/mcp.json"

variables:
  project_root: "/path/to/project"

servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "{{ variables.project_root }}"]
```

**mcp.secrets.yaml:**
```yaml
secrets:
  API_TOKEN: "your_secret_token"
```

## Features

- Template interpolation with Jinja2 (variables, secrets, environment)
- Multiple output paths with variable support
- Secret management (git-ignored files)
- JSON Schema validation
- Optional outputs configuration (CLI --output overrides)
