"""Test suite for VMware VCF Architecture."""

import pytest
import os
import sys
import tempfile
import yaml
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestVCFArchitecture:
    """Test cases for VCFArchitecture class."""
    
    def test_initialization_default(self):
        """Test VCFArchitecture initialization with default config."""
        app = main.VCFArchitecture()
        assert app.version == "1.0.0"
        assert isinstance(app.config, dict)
        assert 'app' in app.config
        assert 'logging' in app.config
    
    def test_initialization_with_config(self):
        """Test VCFArchitecture initialization with custom config."""
        custom_config = {
            'app': {'name': 'test-app', 'debug': True},
            'logging': {'level': 'DEBUG'}
        }
        app = main.VCFArchitecture(config=custom_config)
        assert app.config == custom_config
    
    def test_validate_config_valid(self):
        """Test configuration validation with valid config."""
        app = main.VCFArchitecture()
        assert app.validate_config() is True
    
    def test_validate_config_invalid(self):
        """Test configuration validation with invalid config."""
        invalid_config = {'invalid': 'config'}
        app = main.VCFArchitecture(config=invalid_config)
        assert app.validate_config() is False
    
    def test_health_check_healthy(self):
        """Test health check with healthy application."""
        app = main.VCFArchitecture()
        health = app.health_check()
        assert health['status'] == 'healthy'
        assert health['version'] == "1.0.0"
        assert 'checks' in health
        assert 'config' in health['checks']
        assert 'dependencies' in health['checks']
    
    def test_health_check_unhealthy(self):
        """Test health check with unhealthy application."""
        invalid_config = {'invalid': 'config'}
        app = main.VCFArchitecture(config=invalid_config)
        health = app.health_check()
        assert health['status'] == 'unhealthy'
    
    @patch('main.yaml.safe_load')
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_load_config_from_file(self, mock_exists, mock_open, mock_yaml):
        """Test loading configuration from file."""
        mock_exists.return_value = True
        mock_yaml.return_value = {'test': 'config'}
        
        app = main.VCFArchitecture()
        config = app._load_config()
        
        assert 'test' in config
        assert config['test'] == 'config'
    
    def test_check_dependencies(self):
        """Test dependency checking."""
        app = main.VCFArchitecture()
        assert app._check_dependencies() is True
    
    def test_run_success(self):
        """Test successful application run."""
        app = main.VCFArchitecture()
        result = app.run()
        assert result == 0
    
    def test_run_failure(self):
        """Test application run with configuration failure."""
        invalid_config = {'invalid': 'config'}
        app = main.VCFArchitecture(config=invalid_config)
        result = app.run()
        assert result == 1


class TestCommandLineInterface:
    """Test cases for command line interface."""
    
    def test_create_parser(self):
        """Test argument parser creation."""
        parser = main.create_parser()
        assert parser is not None
        
        # Test parsing help
        with pytest.raises(SystemExit):
            parser.parse_args(['--help'])
    
    def test_parser_version(self):
        """Test version argument."""
        parser = main.create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(['--version'])
    
    def test_parser_config(self):
        """Test config argument."""
        parser = main.create_parser()
        args = parser.parse_args(['--config', 'test.yml'])
        assert args.config == 'test.yml'
    
    def test_parser_debug(self):
        """Test debug argument."""
        parser = main.create_parser()
        args = parser.parse_args(['--debug'])
        assert args.debug is True
    
    def test_parser_health_check(self):
        """Test health check argument."""
        parser = main.create_parser()
        args = parser.parse_args(['--health-check'])
        assert args.health_check is True


class TestMainFunction:
    """Test cases for main function."""
    
    @patch('sys.argv', ['main.py'])
    def test_main_default(self):
        """Test main function with default arguments."""
        result = main.main()
        assert result == 0
    
    @patch('sys.argv', ['main.py', '--health-check'])
    def test_main_health_check(self):
        """Test main function with health check."""
        result = main.main()
        assert result == 0
    
    @patch('sys.argv', ['main.py', '--debug'])
    def test_main_debug(self):
        """Test main function with debug mode."""
        result = main.main()
        assert result == 0


class TestConfigurationLoading:
    """Test cases for configuration loading."""
    
    def test_environment_variables(self):
        """Test loading configuration from environment variables."""
        with patch.dict(os.environ, {
            'DEBUG': 'true',
            'LOG_LEVEL': 'DEBUG',
            'VCF_ENDPOINT': 'https://test.example.com'
        }):
            app = main.VCFArchitecture()
            config = app._load_config()
            
            assert config['app']['debug'] is True
            assert config['logging']['level'] == 'DEBUG'
            assert config['vcf']['endpoint'] == 'https://test.example.com'
    
    def test_config_file_not_exists(self):
        """Test behavior when config file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            app = main.VCFArchitecture()
            config = app._load_config()
            
            # Should still have default configuration
            assert 'app' in config
            assert 'logging' in config


class TestIntegration:
    """Integration test cases."""
    
    def test_full_application_lifecycle(self):
        """Test complete application lifecycle."""
        # Initialize application
        app = main.VCFArchitecture()
        
        # Validate configuration
        assert app.validate_config() is True
        
        # Perform health check
        health = app.health_check()
        assert health['status'] == 'healthy'
        
        # Run application
        result = app.run()
        assert result == 0
    
    def test_application_with_custom_config_file(self):
        """Test application with custom configuration file."""
        # Create temporary config file
        config_data = {
            'app': {'name': 'test-app', 'debug': True},
            'logging': {'level': 'DEBUG'},
            'vcf': {'endpoint': 'https://test.vcf.com'}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name
        
        try:
            # Set environment variable to use our config file
            with patch.dict(os.environ, {'CONFIG_FILE': config_file}):
                app = main.VCFArchitecture()
                
                # Verify config was loaded
                assert app.config['app']['name'] == 'test-app'
                assert app.config['app']['debug'] is True
                assert app.config['vcf']['endpoint'] == 'https://test.vcf.com'
        finally:
            # Clean up
            os.unlink(config_file)


if __name__ == '__main__':
    pytest.main([__file__])# Updated 20251109_123823
# Updated Sun Nov  9 12:49:47 CET 2025
