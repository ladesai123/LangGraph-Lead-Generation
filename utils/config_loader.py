"""
Configuration loader for the LangGraph Lead Generation System.

Loads and parses workflow.json and environment variables.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from .logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """
    Loads and manages configuration from workflow.json and environment variables.
    """
    
    def __init__(self, workflow_path: str = "workflow.json", env_path: str = ".env"):
        """
        Initialize the config loader.
        
        Args:
            workflow_path: Path to workflow.json file
            env_path: Path to .env file
        """
        self.workflow_path = Path(workflow_path)
        self.env_path = Path(env_path)
        self.workflow_config = None
        self.env_vars = {}
        
        # Load configurations
        self._load_env()
        self._load_workflow()
    
    def _load_env(self):
        """Load environment variables from .env file."""
        if not self.env_path.exists():
            logger.warning(f".env file not found at {self.env_path}. Using environment variables only.")
            return
        
        # Load .env file
        load_dotenv(self.env_path)
        logger.info(f"Loaded environment variables from {self.env_path}")
        
        # Store important env vars
        self.env_vars = {
            'AI_PROVIDER': os.getenv('AI_PROVIDER', 'gemini'),
            'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'CLAY_API_KEY': os.getenv('CLAY_API_KEY'),
            'APOLLO_API_KEY': os.getenv('APOLLO_API_KEY'),
            'CLEARBIT_API_KEY': os.getenv('CLEARBIT_API_KEY'),
            'SENDGRID_ACCOUNT_SID': os.getenv('SENDGRID_ACCOUNT_SID'),
            'SENDGRID_AUTH_TOKEN': os.getenv('SENDGRID_AUTH_TOKEN'),
            'SENDGRID_API_KEY': os.getenv('SENDGRID_API_KEY'),
            'SENDGRID_API_SECRET': os.getenv('SENDGRID_API_SECRET'),
            'SENDGRID_FROM_EMAIL': os.getenv('SENDGRID_FROM_EMAIL'),
            'SENDER_NAME': os.getenv('SENDER_NAME', 'Analytos.ai'),
            'GOOGLE_SHEET_ID': os.getenv('GOOGLE_SHEET_ID'),
            'GOOGLE_CREDENTIALS_PATH': os.getenv('GOOGLE_CREDENTIALS_PATH'),
            'ENABLE_DRY_RUN': os.getenv('ENABLE_DRY_RUN', 'true').lower() == 'true',
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO')
        }
    
    def _load_workflow(self):
        """Load workflow configuration from JSON file."""
        if not self.workflow_path.exists():
            raise FileNotFoundError(f"workflow.json not found at {self.workflow_path}")
        
        try:
            with open(self.workflow_path, 'r', encoding='utf-8') as f:
                self.workflow_config = json.load(f)
            
            logger.info(f"Loaded workflow configuration: {self.workflow_config.get('workflow_name')}")
            logger.info(f"Found {len(self.workflow_config.get('steps', []))} workflow steps")
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing workflow.json: {e}")
            raise
    
    def get_workflow(self) -> Dict[str, Any]:
        """
        Get the complete workflow configuration.
        
        Returns:
            Dictionary containing workflow configuration
        """
        return self.workflow_config
    
    def get_step(self, step_id: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific workflow step.
        
        Args:
            step_id: ID of the step (e.g., 'prospect_search')
        
        Returns:
            Step configuration or None if not found
        """
        steps = self.workflow_config.get('steps', [])
        for step in steps:
            if step.get('id') == step_id:
                return step
        
        logger.warning(f"Step '{step_id}' not found in workflow")
        return None
    
    def get_env(self, key: str, default: Any = None) -> Any:
        """
        Get an environment variable.
        
        Args:
            key: Environment variable key
            default: Default value if not found
        
        Returns:
            Environment variable value or default
        """
        return self.env_vars.get(key, default)
    
    def substitute_placeholders(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace {{PLACEHOLDER}} values with actual environment variables.
        
        Args:
            config: Configuration dictionary with placeholders
        
        Returns:
            Configuration with substituted values
        """
        config_str = json.dumps(config)
        
        # Replace all {{KEY}} with actual values
        for key, value in self.env_vars.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in config_str:
                # Handle None values
                replacement = str(value) if value is not None else ""
                config_str = config_str.replace(placeholder, replacement)
        
        return json.loads(config_str)
    
    def get_icp_criteria(self) -> Dict[str, Any]:
        """
        Get the Ideal Customer Profile criteria.
        
        Returns:
            ICP configuration
        """
        return self.workflow_config.get('target_icp', {})
    
    def get_scoring_config(self) -> Dict[str, Any]:
        """
        Get the scoring configuration.
        
        Returns:
            Scoring configuration
        """
        return self.workflow_config.get('config', {}).get('scoring', {})
    
    def get_outreach_config(self) -> Dict[str, Any]:
        """
        Get the outreach configuration.
        
        Returns:
            Outreach configuration
        """
        return self.workflow_config.get('config', {}).get('outreach', {})
    
    def is_dry_run(self) -> bool:
        """
        Check if dry run mode is enabled.
        
        Returns:
            True if dry run is enabled
        """
        return self.env_vars.get('ENABLE_DRY_RUN', True)
    
    def validate_api_keys(self, required_keys: list) -> tuple[bool, list]:
        """
        Validate that required API keys are present.
        
        Args:
            required_keys: List of required environment variable names
        
        Returns:
            Tuple of (all_present: bool, missing_keys: list)
        """
        missing = []
        for key in required_keys:
            if not self.env_vars.get(key):
                missing.append(key)
        
        if missing:
            logger.warning(f"Missing API keys: {', '.join(missing)}")
            return False, missing
        
        return True, []


if __name__ == "__main__":
    # Test the config loader
    try:
        config = ConfigLoader()
        
        print("=== Workflow Configuration ===")
        print(f"Workflow Name: {config.get_workflow().get('workflow_name')}")
        print(f"Number of Steps: {len(config.get_workflow().get('steps', []))}")
        
        print("\n=== ICP Criteria ===")
        icp = config.get_icp_criteria()
        print(json.dumps(icp, indent=2))
        
        print("\n=== Environment Variables ===")
        print(f"Dry Run Mode: {config.is_dry_run()}")
        print(f"Log Level: {config.get_env('LOG_LEVEL')}")
        print(f"OpenAI API Key Present: {bool(config.get_env('OPENAI_API_KEY'))}")
        
        print("\n=== API Key Validation ===")
        valid, missing = config.validate_api_keys(['OPENAI_API_KEY', 'APOLLO_API_KEY'])
        print(f"All required keys present: {valid}")
        if missing:
            print(f"Missing keys: {', '.join(missing)}")
        
        print("\n✅ Config loader test complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
