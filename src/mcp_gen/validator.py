"""Configuration and output validation using JSON Schema."""

import json
import jsonschema
from pathlib import Path


class ConfigValidator:
    """Validates MCP configurations and outputs."""
    
    def __init__(self):
        self.output_schema = self._get_mcp_schema()
    
    def validate_config(self, config_data):
        """Validate input configuration structure."""
        required_fields = ['servers']
        
        for field in required_fields:
            if field not in config_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate servers section
        if not isinstance(config_data['servers'], dict):
            raise ValueError("'servers' must be a dictionary")
        
        for name, server in config_data['servers'].items():
            self._validate_server_config(name, server)
    
    def validate_output(self, output_data):
        """Validate generated output against MCP schema."""
        try:
            jsonschema.validate(output_data, self.output_schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Output validation failed: {e.message}")
    
    def _validate_server_config(self, name, server):
        """Validate individual server configuration."""
        if not isinstance(server, dict):
            raise ValueError(f"Server '{name}' must be a dictionary")
        
        if 'command' not in server:
            raise ValueError(f"Server '{name}' missing required 'command' field")
        
        # Optional field type checking
        if 'args' in server and not isinstance(server['args'], list):
            raise ValueError(f"Server '{name}' args must be a list")
        
        if 'env' in server and not isinstance(server['env'], dict):
            raise ValueError(f"Server '{name}' env must be a dictionary")
    
    def _get_mcp_schema(self):
        """Return JSON schema for MCP output validation."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["mcpServers"],
            "properties": {
                "mcpServers": {
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
                            },
                            "additionalProperties": False
                        }
                    },
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
