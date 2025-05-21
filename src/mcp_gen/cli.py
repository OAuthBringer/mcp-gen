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
@click.option('--secrets', '-s', type=click.Path(),
              default=None, help='Secrets YAML file (optional)')
@click.option('--output', '-o', type=click.Path(),
              default=None, help='Output JSON file (overrides config outputs)')
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
    
    # Determine output paths
    if output:
        # Use CLI-specified output
        output_paths = [output]
    else:
        # Use config-specified outputs
        output_paths = engine.get_outputs()
        if not output_paths:
            # Default fallback
            output_paths = ['.amazonq/mcp.json']
    
    # Write to all specified outputs
    for output_path in output_paths:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with path.open('w') as f:
            json.dump(result, f, indent=2)
        
        click.echo(f"Generated MCP configuration: {output_path}")


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
