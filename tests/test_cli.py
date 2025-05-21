"""Test CLI functionality."""

import pytest
import json
from pathlib import Path
from mcp_gen.cli import main


def test_cli_generate_command(cli_runner, config_files, temp_dir):
    """Test CLI generate command."""
    output_file = temp_dir / 'output.json'
    
    result = cli_runner.invoke(main, [
        'generate',
        '--config', str(config_files['config']),
        '--secrets', str(config_files['secrets']),
        '--output', str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    
    # Verify output is valid JSON
    with output_file.open() as f:
        output_data = json.load(f)
    assert 'mcpServers' in output_data


def test_cli_generate_without_secrets(cli_runner, config_files, temp_dir):
    """Test CLI generate without secrets file."""
    output_file = temp_dir / 'output.json'
    
    result = cli_runner.invoke(main, [
        'generate',
        '--config', str(config_files['config']),
        '--output', str(output_file)
    ])
    
    # Should still succeed
    assert result.exit_code == 0


def test_cli_validate_command(cli_runner, config_files):
    """Test CLI validate command."""
    result = cli_runner.invoke(main, [
        'validate',
        '--config', str(config_files['config'])
    ])
    
    assert result.exit_code == 0
    assert 'Configuration is valid' in result.output


def test_cli_validate_invalid_config(cli_runner, temp_dir):
    """Test CLI validate with invalid config."""
    invalid_config_file = temp_dir / 'invalid.yaml'
    with invalid_config_file.open('w') as f:
        f.write("version: '1.0'\n")  # Missing servers
    
    result = cli_runner.invoke(main, [
        'validate',
        '--config', str(invalid_config_file)
    ])
    
    assert result.exit_code != 0


def test_cli_generate_with_validation_disabled(cli_runner, config_files, temp_dir):
    """Test CLI generate with validation disabled."""
    output_file = temp_dir / 'output.json'
    
    result = cli_runner.invoke(main, [
        'generate',
        '--config', str(config_files['config']),
        '--secrets', str(config_files['secrets']),
        '--output', str(output_file),
        '--no-validate'
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()


def test_cli_version(cli_runner):
    """Test CLI version option."""
    result = cli_runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


def test_cli_help(cli_runner):
    """Test CLI help output."""
    result = cli_runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'MCP Configuration Generator' in result.output


def test_cli_generate_creates_output_directory(cli_runner, config_files, temp_dir):
    """Test CLI creates output directory if it doesn't exist."""
    nested_output = temp_dir / 'nested' / 'dir' / 'output.json'
    
    result = cli_runner.invoke(main, [
        'generate',
        '--config', str(config_files['config']),
        '--secrets', str(config_files['secrets']),
        '--output', str(nested_output)
    ])
    
    assert result.exit_code == 0
    assert nested_output.exists()
    assert nested_output.parent.exists()
