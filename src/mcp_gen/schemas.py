"""JSON Schema definitions for MCP configuration validation."""

# MCP Server Schema - validates individual server configurations
MCP_SERVER_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["command"],
    "properties": {
        "command": {
            "type": "string",
            "description": "Command to execute the MCP server"
        },
        "args": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Command line arguments"
        },
        "env": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "description": "Environment variables"
        }
    },
    "additionalProperties": False
}

# Full MCP Configuration Schema
MCP_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["mcpServers"],
    "properties": {
        "mcpServers": {
            "type": "object",
            "patternProperties": {
                "^[a-zA-Z0-9_-]+$": MCP_SERVER_SCHEMA
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}

# Input YAML Configuration Schema
YAML_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["servers"],
    "properties": {
        "version": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"}
            }
        },
        "variables": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        },
        "servers": {
            "type": "object",
            "patternProperties": {
                "^[a-zA-Z0-9_-]+$": {
                    "type": "object",
                    "required": ["command"],
                    "properties": {
                        "command": {"type": "string"},
                        "args": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "env": {
                            "type": "object",
                            "additionalProperties": {"type": "string"}
                        }
                    }
                }
            }
        }
    },
    "additionalProperties": False
}
