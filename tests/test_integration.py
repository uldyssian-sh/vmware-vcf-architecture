"""Basic integration tests for repository structure and functionality."""

import os
import pytest
import subprocess
import yaml
import json


class TestRepositoryStructure:
    """Test repository structure and required files."""
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            'README.md',
            'LICENSE',
            'requirements.txt',
            'main.py',
            'config.yml',
            '.gitignore',
            'Dockerfile',
            'docker-compose.yml',
            'Makefile',
            'pyproject.toml'
        ]
        
        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} is missing"
    
    def test_github_workflows_exist(self):
        """Test that GitHub workflows exist."""
        workflow_files = [
            '.github/workflows/ci.yml',
            '.github/workflows/deploy.yml'
        ]
        
        for workflow in workflow_files:
            assert os.path.exists(workflow), f"Workflow {workflow} is missing"
    
    def test_github_config_files_exist(self):
        """Test that GitHub configuration files exist."""
        github_files = [
            '.github/dependabot.yml',
            '.github/CODEOWNERS'
        ]
        
        for github_file in github_files:
            assert os.path.exists(github_file), f"GitHub config {github_file} is missing"


class TestConfigurationFiles:
    """Test configuration file validity."""
    
    def test_yaml_files_valid(self):
        """Test that YAML files are valid."""
        yaml_files = [
            'config.yml',
            '.github/workflows/ci.yml',
            '.github/workflows/deploy.yml',
            '.github/dependabot.yml'
        ]
        
        for yaml_file in yaml_files:
            if os.path.exists(yaml_file):
                with open(yaml_file, 'r') as f:
                    try:
                        yaml.safe_load(f)
                    except yaml.YAMLError as e:
                        pytest.fail(f"Invalid YAML in {yaml_file}: {e}")
    
    def test_json_files_valid(self):
        """Test that JSON files are valid."""
        json_files = [
            'package.json'
        ]
        
        for json_file in json_files:
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"Invalid JSON in {json_file}: {e}")
    
    def test_requirements_txt_valid(self):
        """Test that requirements.txt is valid."""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        # Check for required dependencies
        required_deps = ['requests', 'pyyaml', 'click', 'python-dotenv']
        for dep in required_deps:
            assert dep in content, f"Required dependency {dep} not found in requirements.txt"


class TestDockerConfiguration:
    """Test Docker configuration."""
    
    def test_dockerfile_exists_and_valid(self):
        """Test Dockerfile exists and has basic structure."""
        assert os.path.exists('Dockerfile')
        
        with open('Dockerfile', 'r') as f:
            content = f.read()
        
        # Check for basic Dockerfile instructions
        assert 'FROM' in content
        assert 'WORKDIR' in content
        assert 'COPY' in content
        assert 'RUN' in content
    
    def test_docker_compose_valid(self):
        """Test docker-compose.yml is valid."""
        with open('docker-compose.yml', 'r') as f:
            compose_config = yaml.safe_load(f)
        
        assert 'version' in compose_config
        assert 'services' in compose_config
        assert 'vmware-vcf-architecture' in compose_config['services']


class TestApplicationFunctionality:
    """Test basic application functionality."""
    
    def test_main_module_imports(self):
        """Test that main module can be imported."""
        try:
            import main
            assert hasattr(main, 'VCFArchitecture')
            assert hasattr(main, 'main')
        except ImportError as e:
            pytest.fail(f"Failed to import main module: {e}")
    
    def test_main_application_instantiation(self):
        """Test that main application can be instantiated."""
        import main
        
        app = main.VCFArchitecture()
        assert app is not None
        assert hasattr(app, 'config')
        assert hasattr(app, 'version')
    
    def test_health_check_functionality(self):
        """Test health check functionality."""
        import main
        
        app = main.VCFArchitecture()
        health = app.health_check()
        
        assert isinstance(health, dict)
        assert 'status' in health
        assert 'version' in health
        assert 'checks' in health
    
    def test_command_line_interface(self):
        """Test command line interface."""
        # Test help command
        result = subprocess.run(['python', 'main.py', '--help'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        
        # Test health check command
        result = subprocess.run(['python', 'main.py', '--health-check'], 
                              capture_output=True, text=True)
        assert result.returncode == 0


class TestSecurityConfiguration:
    """Test security-related configuration."""
    
    def test_gitignore_has_security_entries(self):
        """Test that .gitignore includes security-sensitive files."""
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        security_patterns = ['.env', '*.key', '*.pem', '__pycache__']
        for pattern in security_patterns:
            assert pattern in gitignore_content, f"Security pattern {pattern} not in .gitignore"
    
    def test_env_template_exists(self):
        """Test that environment template exists."""
        assert os.path.exists('.env.template')
        
        with open('.env.template', 'r') as f:
            content = f.read()
        
        # Check for placeholder values
        assert '<' in content and '>' in content, "Template should contain placeholder values"


class TestCIConfiguration:
    """Test CI/CD configuration."""
    
    def test_github_actions_syntax(self):
        """Test GitHub Actions workflow syntax."""
        workflows = ['.github/workflows/ci.yml', '.github/workflows/deploy.yml']
        
        for workflow in workflows:
            with open(workflow, 'r') as f:
                workflow_config = yaml.safe_load(f)
            
            assert 'name' in workflow_config
            assert 'on' in workflow_config
            assert 'jobs' in workflow_config
    
    def test_dependabot_configuration(self):
        """Test Dependabot configuration."""
        with open('.github/dependabot.yml', 'r') as f:
            dependabot_config = yaml.safe_load(f)
        
        assert 'version' in dependabot_config
        assert 'updates' in dependabot_config
        assert len(dependabot_config['updates']) > 0# Updated 20251109_123823
# Updated Sun Nov  9 12:49:47 CET 2025
# Updated Sun Nov  9 12:52:31 CET 2025
