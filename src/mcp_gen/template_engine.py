"""Template engine for processing YAML configurations with Jinja2."""

import yaml
import json
from pathlib import Path
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, UndefinedError


class TemplateEngine:
    """Processes YAML configurations with template interpolation."""
    
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
        self.outputs = []
    
    def process_config(self, config_path, secrets_path=None):
        """Process configuration with optional secrets."""
        # Load base configuration
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Load secrets if provided
        secrets = {}
        if secrets_path and Path(secrets_path).exists():
            with open(secrets_path) as f:
                secrets = yaml.safe_load(f) or {}
        
        # Extract variables and raw outputs from config
        variables = config.get('variables', {})
        raw_outputs = config.get('outputs', [])
        
        # Build template context
        context = {
            'variables': variables,
            'secrets': secrets.get('secrets', {}),
            'env': dict(__import__('os').environ)
        }
        
        # Process outputs with template interpolation
        self.outputs = [self._interpolate_string(output, context) for output in raw_outputs]
        
        # Process servers section
        if 'servers' not in config:
            raise ValueError("Configuration missing 'servers' section")
        
        processed_servers = {}
        for name, server_config in config['servers'].items():
            processed_servers[name] = self._process_server(server_config, context)
        
        return {
            'mcpServers': processed_servers
        }
    
    def get_outputs(self):
        """Get configured output paths."""
        return self.outputs
    
    def _process_server(self, server_config, context):
        """Process individual server configuration."""
        result = {}
        
        # Process each field with template interpolation
        for key, value in server_config.items():
            if isinstance(value, str):
                result[key] = self._interpolate_string(value, context)
            elif isinstance(value, list):
                result[key] = [self._interpolate_string(str(item), context) for item in value]
            elif isinstance(value, dict):
                result[key] = {k: self._interpolate_string(str(v), context) for k, v in value.items()}
            else:
                result[key] = value
        
        return result
    
    def _interpolate_string(self, template_str, context):
        """Interpolate a single string template."""
        try:
            template = self.env.from_string(template_str)
            return template.render(**context)
        except (TemplateSyntaxError, UndefinedError) as e:
            raise ValueError(f"Template error in '{template_str}': {e}")
