"""Test fixtures for MCP-Gen testing."""

import pytest
import tempfile
import yaml
import json
from pathlib import Path
from click.testing import CliRunner


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_config():
    """Sample MCP configuration."""
    return {
        'version': '1.0',
        'metadata': {
            'name': 'Test MCP Config',
            'description': 'Test configuration'
        },
        'variables': {
            'project_root': '~/dev/test-project',
            'data_path': '{{ variables.project_root }}/data'
        },
        'servers': {
            'filesystem': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-filesystem', '{{ variables.project_root }}']
            },
            'github': {
                'command': 'docker',
                'args': ['run', '-i', '--rm', '-e', 'GITHUB_PERSONAL_ACCESS_TOKEN={{ secrets.GITHUB_TOKEN }}', 'ghcr.io/github/github-mcp-server'],
                'env': {
                    'DEBUG': '{{ env.DEBUG }}'
                }
            }
        }
    }


@pytest.fixture
def sample_secrets():
    """Sample secrets configuration."""
    return {
        'secrets': {
            'GITHUB_TOKEN': 'ghp_test_token_123',
            'API_KEY': 'test_api_key_456'
        }
    }


@pytest.fixture
def invalid_config():
    """Invalid configuration for testing validation."""
    return {
        'version': '1.0',
        'servers': {
            'bad_server': {
                # Missing required 'command' field
                'args': ['some', 'args']
            }
        }
    }


@pytest.fixture
def valid_mcp_output():
    """Valid MCP JSON output."""
    return {
        'mcpServers': {
            'filesystem': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-filesystem', '~/dev/test-project']
            },
            'github': {
                'command': 'docker',
                'args': ['run', '-i', '--rm', '-e', 'GITHUB_PERSONAL_ACCESS_TOKEN=ghp_test_token_123', 'ghcr.io/github/github-mcp-server'],
                'env': {
                    'DEBUG': 'false'
                }
            }
        }
    }


@pytest.fixture
def invalid_mcp_output():
    """Invalid MCP JSON output for schema testing."""
    return {
        'mcpServers': {
            'bad_server': {
                # Missing required 'command' field
                'args': ['some', 'args']
            }
        }
    }


@pytest.fixture
def config_files(temp_dir, sample_config, sample_secrets):
    """Create temporary config and secrets files."""
    config_file = temp_dir / 'mcp.config.yaml'
    secrets_file = temp_dir / 'mcp.secrets.yaml'
    
    with config_file.open('w') as f:
        yaml.dump(sample_config, f)
    
    with secrets_file.open('w') as f:
        yaml.dump(sample_secrets, f)
    
    return {
        'config': config_file,
        'secrets': secrets_file,
        'config_data': sample_config,
        'secrets_data': sample_secrets
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv('DEBUG', 'false')
    monkeypatch.setenv('TEST_VAR', 'test_value')
