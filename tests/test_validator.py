"""Test validator functionality."""

import pytest
import json
from mcp_gen.validator import ConfigValidator


def test_validate_valid_config(sample_config):
    """Test validation of valid configuration."""
    validator = ConfigValidator()
    # Should not raise any exceptions
    validator.validate_config(sample_config)


def test_validate_invalid_config_missing_servers(temp_dir):
    """Test validation fails when servers section missing."""
    invalid_config = {'version': '1.0'}
    
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="Missing required field: servers"):
        validator.validate_config(invalid_config)


def test_validate_invalid_config_missing_command(invalid_config):
    """Test validation fails when server missing command."""
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="missing required 'command' field"):
        validator.validate_config(invalid_config)


def test_validate_invalid_server_args_type():
    """Test validation fails when args is not a list."""
    bad_config = {
        'servers': {
            'test': {
                'command': 'test',
                'args': 'not_a_list'  # Should be a list
            }
        }
    }
    
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="args must be a list"):
        validator.validate_config(bad_config)


def test_validate_invalid_server_env_type():
    """Test validation fails when env is not a dict."""
    bad_config = {
        'servers': {
            'test': {
                'command': 'test',
                'env': 'not_a_dict'  # Should be a dict
            }
        }
    }
    
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="env must be a dictionary"):
        validator.validate_config(bad_config)


def test_validate_valid_output(valid_mcp_output):
    """Test validation of valid MCP output."""
    validator = ConfigValidator()
    # Should not raise any exceptions
    validator.validate_output(valid_mcp_output)


def test_validate_invalid_output_schema(invalid_mcp_output):
    """Test validation fails for invalid MCP output."""
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="Output validation failed"):
        validator.validate_output(invalid_mcp_output)


def test_validate_output_missing_mcpservers():
    """Test validation fails when mcpServers missing."""
    invalid_output = {'not_mcpServers': {}}
    
    validator = ConfigValidator()
    with pytest.raises(ValueError, match="Output validation failed"):
        validator.validate_output(invalid_output)


def test_mcp_schema_structure():
    """Test MCP schema contains required fields."""
    validator = ConfigValidator()
    schema = validator.output_schema
    
    assert schema['type'] == 'object'
    assert 'mcpServers' in schema['required']
    assert 'mcpServers' in schema['properties']
