"""
Base Agent class for all LangGraph agents.

All specialized agents inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the workflow.
    
    Each agent must implement the execute() method.
    """
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """
        Initialize base agent.
        
        Args:
            agent_id: Unique identifier for this agent
            config: Configuration dictionary from workflow.json
        """
        self.agent_id = agent_id
        self.config = config
        self.instructions = config.get('instructions', '')
        self.tools = config.get('tools', [])
        self.logger = get_logger(f"agent.{agent_id}")
        
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main logic.
        
        Args:
            inputs: Input data for the agent
        
        Returns:
            Output data from the agent
        """
        pass
    
    def log_execution_start(self, inputs: Dict[str, Any]):
        """Log the start of agent execution."""
        self.logger.info(f"=" * 60)
        self.logger.info(f"STARTING: {self.__class__.__name__}")
        self.logger.info(f"Agent ID: {self.agent_id}")
        self.logger.info(f"=" * 60)
        
        # Log input summary
        if isinstance(inputs, dict):
            input_summary = {k: f"<{type(v).__name__}>" for k, v in inputs.items()}
            self.logger.debug(f"Inputs: {json.dumps(input_summary, indent=2)}")
    
    def log_execution_end(self, outputs: Dict[str, Any], success: bool = True):
        """Log the end of agent execution."""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.logger.info(f"{status}: {self.__class__.__name__}")
        
        # Log output summary
        if isinstance(outputs, dict):
            output_summary = {k: f"<{type(v).__name__}>" for k, v in outputs.items()}
            self.logger.debug(f"Outputs: {json.dumps(output_summary, indent=2)}")
        
        self.logger.info(f"=" * 60)
    
    def log_step(self, step_name: str, details: Optional[str] = None):
        """Log an intermediate step."""
        msg = f"  → {step_name}"
        if details:
            msg += f": {details}"
        self.logger.info(msg)
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle and log errors gracefully.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        
        Returns:
            Error response dictionary
        """
        error_msg = f"Error in {self.__class__.__name__}"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        
        self.logger.error(error_msg, exc_info=True)
        
        return {
            "status": "error",
            "agent": self.agent_id,
            "error": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_inputs(self, inputs: Dict[str, Any], required_keys: List[str]) -> bool:
        """
        Validate that all required input keys are present.
        
        Args:
            inputs: Input dictionary to validate
            required_keys: List of required key names
        
        Returns:
            True if all required keys present
        """
        missing = [key for key in required_keys if key not in inputs]
        
        if missing:
            self.logger.error(f"Missing required inputs: {', '.join(missing)}")
            return False
        
        return True
    
    def get_tool_config(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool
        
        Returns:
            Tool configuration dictionary or None
        """
        for tool in self.tools:
            if tool.get('name') == tool_name:
                return tool.get('config', {})
        
        self.logger.warning(f"Tool '{tool_name}' not found in agent configuration")
        return None
    
    def format_output(self, data: Any, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format output data according to schema.
        
        Args:
            data: Data to format
            schema: Output schema from workflow.json
        
        Returns:
            Formatted output dictionary
        """
        # For now, just wrap data in standard format
        return {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "status": "success"
        }
    
    def __str__(self) -> str:
        """String representation of agent."""
        return f"{self.__class__.__name__}(id='{self.agent_id}')"
    
    def __repr__(self) -> str:
        """Detailed representation of agent."""
        return f"{self.__class__.__name__}(id='{self.agent_id}', tools={len(self.tools)})"


if __name__ == "__main__":
    # Test base agent
    print("Testing BaseAgent (Abstract Class)\n")
    
    # Create a simple test agent
    class TestAgent(BaseAgent):
        def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            self.log_execution_start(inputs)
            
            self.log_step("Processing", "Test processing")
            result = {"processed": True, "input_count": len(inputs)}
            
            self.log_execution_end(result, success=True)
            return self.format_output(result)
    
    # Test the agent
    config = {
        "instructions": "Test agent",
        "tools": [{"name": "TestTool", "config": {"key": "value"}}]
    }
    
    agent = TestAgent("test_agent", config)
    print(f"Created: {agent}\n")
    
    # Execute
    result = agent.execute({"test_input": "hello"})
    print(f"\nResult: {json.dumps(result, indent=2)}")
    
    print("\n✅ BaseAgent test complete!")
