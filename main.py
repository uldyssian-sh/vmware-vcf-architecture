#!/usr/bin/env python3
"""
VMware VCF Architecture - Enterprise automation and management solution.

This module provides core functionality for VMware Cloud Foundation
architecture automation, monitoring, and management.
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any, Optional
import yaml
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('vmware-vcf-architecture.log')
    ]
)

logger = logging.getLogger(__name__)


class VCFArchitecture:
    """Main application class for VMware VCF Architecture management."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the VCF Architecture application.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._load_config()
        self.version = "1.0.0"
        logger.info(f"Initializing VMware VCF Architecture v{self.version}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment and config files.
        
        Returns:
            Configuration dictionary
        """
        config = {
            'app': {
                'name': 'vmware-vcf-architecture',
                'version': self.version if hasattr(self, 'version') else '1.0.0',
                'debug': os.getenv('DEBUG', 'false').lower() == 'true'
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'format': 'json' if os.getenv('LOG_FORMAT') == 'json' else 'text'
            },
            'vcf': {
                'endpoint': os.getenv('VCF_ENDPOINT', ''),
                'username': os.getenv('VCF_USERNAME', ''),
                'password': os.getenv('VCF_PASSWORD', ''),
                'verify_ssl': os.getenv('VCF_VERIFY_SSL', 'true').lower() == 'true'
            }
        }
        
        # Load from config file if exists
        config_file = os.getenv('CONFIG_FILE', 'config.yml')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config.update(file_config)
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config file {config_file}: {e}")
        
        return config
    
    def validate_config(self) -> bool:
        """Validate the current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_keys = ['app', 'logging']
        for key in required_keys:
            if key not in self.config:
                logger.error(f"Missing required configuration key: {key}")
                return False
        
        logger.info("Configuration validation passed")
        return True
    
    def health_check(self) -> Dict[str, Any]:
        """Perform application health check.
        
        Returns:
            Health status dictionary
        """
        status = {
            'status': 'healthy',
            'version': self.version,
            'timestamp': None,
            'checks': {
                'config': self.validate_config(),
                'dependencies': self._check_dependencies()
            }
        }
        
        # Overall health based on individual checks
        if not all(status['checks'].values()):
            status['status'] = 'unhealthy'
        
        logger.info(f"Health check completed: {status['status']}")
        return status
    
    def _check_dependencies(self) -> bool:
        """Check if required dependencies are available.
        
        Returns:
            True if all dependencies are available, False otherwise
        """
        try:
            import yaml
            import requests
            logger.debug("All dependencies are available")
            return True
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            return False
    
    def run(self) -> int:
        """Run the main application.
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            logger.info("Starting VMware VCF Architecture application")
            
            if not self.validate_config():
                logger.error("Configuration validation failed")
                return 1
            
            # Perform health check
            health = self.health_check()
            if health['status'] != 'healthy':
                logger.error("Health check failed")
                return 1
            
            logger.info("Application started successfully")
            logger.info("VMware VCF Architecture is ready for enterprise automation")
            
            return 0
            
        except Exception as e:
            logger.error(f"Application failed to start: {e}")
            return 1


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='VMware VCF Architecture - Enterprise automation solution',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--health-check',
        action='store_true',
        help='Perform health check and exit'
    )
    
    return parser


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Set config file if provided
    if args.config:
        os.environ['CONFIG_FILE'] = args.config
    
    # Initialize application
    app = VCFArchitecture()
    
    # Handle health check
    if args.health_check:
        health = app.health_check()
        print(f"Health Status: {health['status']}")
        return 0 if health['status'] == 'healthy' else 1
    
    # Run application
    return app.run()


if __name__ == '__main__':
    sys.exit(main())