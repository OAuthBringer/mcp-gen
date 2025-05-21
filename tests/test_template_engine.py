"""Test template engine functionality."""

import pytest
import os
from pathlib import Path
from mcp_gen.template_engine import TemplateEngine


def test_basic_template_processing(config_files, mock_env_vars):
    """Test basic template interpolation."""
    engine = TemplateEngine()
    
    result = engine.process_config(
        config_files['config'], 
        config_files['secrets']
    )
    
    assert 'mcpServers' in result
    assert 'filesystem' in result['mcpServers']
    assert 'github' in result['mcpServers']


def test_variable_interpolation(config_files):
    """Test variable substitution works correctly."""
    engine = TemplateEngine()
    result = engine.process_config(config_files['config'], config_files['secrets'])
    
    filesystem_args = result['mcpServers']['filesystem']['args']
    assert '~/dev/test-project' in filesystem_args[-1]


def test_secrets_interpolation(config_files):
    """Test secrets are properly interpolated."""
    engine = TemplateEngine()
    result = engine.process_config(config_files['config'], config_files['secrets'])
    
    github_args = result['mcpServers']['github']['args']
    token_arg = next(arg for arg in github_args if 'GITHUB_PERSONAL_ACCESS_TOKEN' in arg)
    assert 'ghp_test_token_123' in token_arg


def test_env_interpolation(config_files, mock_env_vars):
    """Test environment variable interpolation."""
    engine = TemplateEngine()
    result = engine.process_config(config_files['config'], config_files['secrets'])
    
    github_env = result['mcpServers']['github']['env']
    assert github_env['DEBUG'] == 'false'


def test_missing_secrets_file(config_files):
    """Test handling when secrets file doesn't exist."""
    engine = TemplateEngine()
    
    # Process without secrets file
    result = engine.process_config(config_files['config'], None)
    
    # Should still work but with empty secrets
    assert 'mcpServers' in result


def test_missing_config_section(temp_dir):
    """Test error when servers section is missing."""
    config_file = temp_dir / 'bad_config.yaml'
    with config_file.open('w') as f:
        f.write("version: '1.0'\n")
    
    engine = TemplateEngine()
    with pytest.raises(ValueError, match="Configuration missing 'servers' section"):
        engine.process_config(config_file)


def test_template_syntax_error(temp_dir):
    """Test handling of template syntax errors."""
    bad_config = {
        'servers': {
            'bad': {
                'command': 'test',
                'args': ['{{ invalid template syntax']
            }
        }
    }
    
    config_file = temp_dir / 'bad_template.yaml'
    with config_file.open('w') as f:
        import yaml
        yaml.dump(bad_config, f)
    
    engine = TemplateEngine()
    with pytest.raises(ValueError, match="Template error"):
        engine.process_config(config_file)
