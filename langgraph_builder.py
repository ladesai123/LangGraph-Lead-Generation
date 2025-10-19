"""
LangGraph Builder - Dynamic workflow orchestration from workflow.json

This is the main entry point that reads workflow.json and executes
all agents in sequence using LangGraph.
"""

import sys
import json
import os
from typing import Dict, Any, List
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import get_logger, setup_logger
from utils.config_loader import ConfigLoader
from utils.validators import validate_workflow

# Import all agents
from agents.prospect_search import ProspectSearchAgent
from agents.data_enrichment import DataEnrichmentAgent
from agents.scoring import ScoringAgent
from agents.outreach_content import OutreachContentAgent
from agents.outreach_executor import OutreachExecutorAgent
from agents.response_tracker import ResponseTrackerAgent
from agents.feedback_trainer import FeedbackTrainerAgent

logger = get_logger(__name__)


class LangGraphWorkflowBuilder:
    """
    Builds and executes a LangGraph workflow from workflow.json configuration.
    """
    
    # Map agent names to classes
    AGENT_REGISTRY = {
        "ProspectSearchAgent": ProspectSearchAgent,
        "DataEnrichmentAgent": DataEnrichmentAgent,
        "ScoringAgent": ScoringAgent,
        "OutreachContentAgent": OutreachContentAgent,
        "OutreachExecutorAgent": OutreachExecutorAgent,
        "ResponseTrackerAgent": ResponseTrackerAgent,
        "FeedbackTrainerAgent": FeedbackTrainerAgent
    }
    
    def __init__(self, config_path: str = "workflow.json"):
        """
        Initialize workflow builder.
        
        Args:
            config_path: Path to workflow.json file
        """
        self.config_loader = ConfigLoader(workflow_path=config_path)
        self.workflow_config = self.config_loader.get_workflow()
        self.agents = {}
        self.state = {}  # Workflow state shared between agents
        
        logger.info(f"Initialized LangGraph Builder for: {self.workflow_config.get('workflow_name')}")
    
    def build_workflow(self):
        """Build all agents from workflow configuration."""
        logger.info("=" * 70)
        logger.info("BUILDING WORKFLOW")
        logger.info("=" * 70)
        
        # Validate workflow
        is_valid, error_msg = validate_workflow(self.workflow_config)
        if not is_valid:
            raise ValueError(f"Invalid workflow configuration: {error_msg}")
        
        steps = self.workflow_config.get('steps', [])
        logger.info(f"Building {len(steps)} agents...")
        
        for step in steps:
            agent_id = step['id']
            agent_class_name = step['agent']
            
            # Get agent class from registry
            agent_class = self.AGENT_REGISTRY.get(agent_class_name)
            if not agent_class:
                raise ValueError(f"Unknown agent type: {agent_class_name}")
            
            # Substitute placeholders in step config
            step_with_env = self.config_loader.substitute_placeholders(step)
            
            # Create agent instance
            agent = agent_class(agent_id, step_with_env)
            self.agents[agent_id] = agent
            
            logger.info(f"  ✓ Built {agent_class_name} (id: {agent_id})")
        
        logger.info(f"✅ Successfully built {len(self.agents)} agents")
        logger.info("=" * 70)
    
    def execute_workflow(self) -> Dict[str, Any]:
        """
        Execute the complete workflow by running agents in sequence.
        
        Returns:
            Final workflow state with all outputs
        """
        logger.info("=" * 70)
        logger.info("EXECUTING WORKFLOW")
        logger.info("=" * 70)
        
        steps = self.workflow_config.get('steps', [])
        
        for i, step in enumerate(steps, 1):
            agent_id = step['id']
            agent = self.agents[agent_id]
            
            logger.info(f"\n[Step {i}/{len(steps)}] Executing: {agent_id}")
            logger.info("-" * 70)
            
            # Prepare inputs for this agent
            inputs = self._prepare_agent_inputs(step)
            
            # Execute agent
            try:
                result = agent.execute(inputs)
                
                # Store output in state (agents return data directly, not wrapped in 'data')
                self.state[agent_id] = result if result else {}
                
                # Log summary
                if result and not result.get('error'):
                    logger.info(f"✅ {agent_id} completed successfully")
                else:
                    logger.warning(f"⚠️ {agent_id} completed with warnings")
                
            except Exception as e:
                logger.error(f"❌ {agent_id} failed: {e}")
                self.state[agent_id] = {
                    "error": str(e),
                    "status": "failed"
                }
                # Continue with workflow (or optionally stop)
        
        logger.info("\n" + "=" * 70)
        logger.info("WORKFLOW EXECUTION COMPLETE")
        logger.info("=" * 70)
        
        # Save final state
        self._save_results()
        
        return self.state
    
    def _prepare_agent_inputs(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare inputs for an agent by resolving references to previous outputs.
        
        Args:
            step: Step configuration from workflow.json
        
        Returns:
            Resolved input dictionary
        """
        inputs = step.get('inputs', {})
        resolved_inputs = {}
        
        for key, value in inputs.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                # This is a reference to previous step output, workflow config, or environment variable
                # Format: {{step_id.output.field_name}} or {{config.section_name}} or {{ENV_VAR}}
                reference = value[2:-2].strip()  # Remove {{ and }}
                
                # Parse reference
                parts = reference.split('.')
                
                # Check if it's a single-part reference (could be environment variable)
                if len(parts) == 1:
                    # Try to get from environment
                    env_value = os.getenv(reference)
                    if env_value is not None:
                        # Convert string boolean to actual boolean
                        if env_value.lower() == 'true':
                            resolved_inputs[key] = True
                        elif env_value.lower() == 'false':
                            resolved_inputs[key] = False
                        else:
                            resolved_inputs[key] = env_value
                        continue
                    else:
                        logger.warning(f"Could not resolve reference: {reference}")
                        resolved_inputs[key] = None
                        continue
                
                if len(parts) >= 2:
                    step_id = parts[0]
                    
                    # Special case: config references
                    if step_id == 'config':
                        # Get from workflow config
                        data = self.workflow_config.get('config', {})
                        # Navigate through nested fields
                        for part in parts[1:]:
                            if isinstance(data, dict) and part in data:
                                data = data[part]
                            else:
                                logger.warning(f"Could not resolve config reference: {reference}")
                                data = None
                                break
                        resolved_inputs[key] = data
                        continue
                    
                    # Get data from state
                    if step_id in self.state:
                        data = self.state[step_id]
                        
                        # Navigate through nested fields
                        for part in parts[1:]:
                            if part == 'output':
                                # When we see 'output', go into 'data' key
                                if isinstance(data, dict) and 'data' in data:
                                    data = data['data']
                                continue
                            if isinstance(data, dict) and part in data:
                                data = data[part]
                            else:
                                logger.warning(f"Could not resolve reference: {reference}")
                                data = None
                                break
                        
                        resolved_inputs[key] = data
                    else:
                        logger.warning(f"Step '{step_id}' output not found in state")
                        resolved_inputs[key] = None
                else:
                    # It's a config reference like {{config.scoring}}
                    if parts[0] == 'config' and len(parts) > 1:
                        config_section = parts[1]
                        resolved_inputs[key] = self.workflow_config.get('config', {}).get(config_section, {})
                    else:
                        resolved_inputs[key] = value
            else:
                # Not a reference, use as-is
                resolved_inputs[key] = value
        
        # Add dry_run flag from environment
        if 'dry_run' not in resolved_inputs:
            resolved_inputs['dry_run'] = self.config_loader.is_dry_run()
        
        return resolved_inputs
    
    def _save_results(self):
        """Save workflow results to file."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"workflow_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, default=str)
        
        logger.info(f"📄 Results saved to: {output_file}")
    
    def print_summary(self):
        """Print a summary of workflow results."""
        print("\n" + "=" * 70)
        print("WORKFLOW SUMMARY")
        print("=" * 70)
        
        # Prospect Search Summary
        if 'prospect_search' in self.state:
            leads = self.state['prospect_search'].get('leads', [])
            print(f"\n1. Prospect Search: Found {len(leads)} leads")
        
        # Enrichment Summary
        if 'enrichment' in self.state:
            enriched = self.state['enrichment'].get('enriched_leads', [])
            print(f"2. Data Enrichment: Enriched {len(enriched)} leads")
        
        # Scoring Summary
        if 'scoring' in self.state:
            ranked = self.state['scoring'].get('ranked_leads', [])
            print(f"3. Scoring: Ranked {len(ranked)} leads")
            if ranked:
                top_lead = ranked[0]['lead']
                print(f"   Top Lead: {top_lead.get('contact')} at {top_lead.get('company')} (Score: {ranked[0]['score']})")
        
        # Outreach Content Summary
        if 'outreach_content' in self.state:
            messages = self.state['outreach_content'].get('messages', [])
            print(f"4. Outreach Content: Generated {len(messages)} emails")
        
        # Outreach Executor Summary
        if 'send' in self.state:
            summary = self.state['send'].get('summary', {})
            print(f"5. Outreach Executor: Sent {summary.get('sent', 0)}/{summary.get('total', 0)} emails")
            campaign_id = self.state['send'].get('campaign_id', 'N/A')
            print(f"   Campaign ID: {campaign_id}")
        
        # Response Tracking Summary
        if 'response_tracking' in self.state:
            metrics = self.state['response_tracking'].get('metrics', {})
            print(f"6. Response Tracking:")
            print(f"   Open Rate: {metrics.get('open_rate', 0):.1%}")
            print(f"   Reply Rate: {metrics.get('reply_rate', 0):.1%}")
            print(f"   Meeting Rate: {metrics.get('meeting_rate', 0):.1%}")
        
        # Feedback Trainer Summary
        if 'feedback_trainer' in self.state:
            recommendations = self.state['feedback_trainer'].get('recommendations', [])
            print(f"7. Feedback Trainer: Generated {len(recommendations)} recommendations")
            if recommendations:
                print(f"   Top Recommendation: {recommendations[0].get('category')}")
        
        print("\n" + "=" * 70)
        print(f"✅ Workflow Complete!")
        print("=" * 70)


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print(" 🚀 LANGGRAPH AUTONOMOUS PROSPECT-TO-LEAD WORKFLOW")
    print("=" * 70)
    
    try:
        # Initialize builder
        builder = LangGraphWorkflowBuilder()
        
        # Build workflow
        builder.build_workflow()
        
        # Execute workflow
        builder.execute_workflow()
        
        # Print summary
        builder.print_summary()
        
        print("\n✅ All done! Check the output/ folder for detailed results.")
        print("📊 Check logs/ folder for detailed execution logs.")
        
    except Exception as e:
        logger.error(f"Fatal error in workflow execution: {e}", exc_info=True)
        print(f"\n❌ Workflow failed: {e}")
        print("Check logs/ folder for details.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
