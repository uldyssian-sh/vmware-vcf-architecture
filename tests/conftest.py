"""Test configuration and fixtures for VMware VCF Architecture test suite."""

import pytest
import os
import tempfile
import yaml
from unittest.mock import MagicMock


@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing."""
    return {
        'app': {
            'name': 'vmware-vcf-architecture',
            'version': '1.0.0',
            'debug': False
        },
        'logging': {
            'level': 'INFO',
            'format': 'json'
        },
        'vcf': {
            'endpoint': 'https://test.vcf.com',
            'username': 'testuser',
            'password': 'testpass',
            'verify_ssl': True
        }
    }


@pytest.fixture
def temp_config_file(sample_config):
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(sample_config, f)
        config_file = f.name
    
    yield config_file
    
    # Cleanup
    os.unlink(config_file)


@pytest.fixture
def mock_environment():
    """Provide mock environment variables."""
    return {
        'DEBUG': 'false',
        'LOG_LEVEL': 'INFO',
        'VCF_ENDPOINT': 'https://mock.vcf.com',
        'VCF_USERNAME': 'mockuser',
        'VCF_PASSWORD': 'mockpass'
    }


@pytest.fixture
def vcf_architecture_instance(sample_config):
    """Provide a VCFArchitecture instance for testing."""
    import main
    return main.VCFArchitecture(config=sample_config)


class TestHelpers:
    """Helper methods for testing."""
    
    @staticmethod
    def create_mock_response(status_code=200, json_data=None):
        """Create a mock HTTP response."""
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data or {}
        return mock_response