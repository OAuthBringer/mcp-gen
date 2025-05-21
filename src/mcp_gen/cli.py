"""CLI interface for MCP configuration generator."""

import click
from pathlib import Path
import yaml
import json
from .template_engine import TemplateEngine
from .validator import ConfigValidator


@click.group()
@click.version_option()
def main():
    """MCP Configuration Generator - Convert YAML configs to MCP JSON."""
    pass


@main.command()
@click.option('--config', '-c', type=click.Path(exists=True), 
              default='mcp.config.yaml', help='Config YAML file')
@click.option('--secrets', '-s', type=click.Path(exists=True),
              default='mcp.secrets.yaml', help='Secrets YAML file')
@click.option('--output', '-o', type=click.Path(),
              default='.amazonq/mcp.json', help='Output JSON file')
@click.option('--validate/--no-validate', default=True,
              help='Validate output against MCP schema')
def generate(config, secrets, output, validate):
    """Generate MCP JSON from YAML configuration."""
    engine = TemplateEngine()
    validator = ConfigValidator()
    
    # Load and process configuration
    result = engine.process_config(config, secrets)
    
    # Validate if requested
    if validate:
        validator.validate_output(result)
    
    # Write output
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open('w') as f:
        json.dump(result, f, indent=2)
    
    click.echo(f"Generated MCP configuration: {output}")


@main.command()
@click.option('--config', '-c', type=click.Path(exists=True),
              default='mcp.config.yaml', help='Config YAML file')
def validate(config):
    """Validate YAML configuration without generating output."""
    validator = ConfigValidator()
    
    with open(config) as f:
        config_data = yaml.safe_load(f)
    
    validator.validate_config(config_data)
    click.echo("Configuration is valid ✓")


if __name__ == '__main__':
    main()
