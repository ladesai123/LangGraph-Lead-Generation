"""
Response Tracker Agent - Monitors email responses and engagement.
"""

from typing import Dict, Any, List
import random
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from tools.apollo_api import ApolloClient

class ResponseTrackerAgent(BaseAgent):
    """
    Agent responsible for tracking email responses and engagement metrics.
    """
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track email responses and calculate engagement metrics.
        
        Args:
            inputs: Dictionary containing:
                - campaign_id: Campaign identifier
                - tracking_period_hours: Hours to track (default: 72)
        
        Returns:
            Dictionary with 'responses' list and 'metrics'
        """
        self.log_execution_start(inputs)
        
        try:
            campaign_id = inputs.get('campaign_id', 'unknown')
            tracking_period = inputs.get('tracking_period_hours', 72)
            
            self.log_step("Tracking responses", 
                         f"Campaign: {campaign_id}, Period: {tracking_period}h")
            
            # In a real implementation, this would query Apollo API or
            # email service provider for actual engagement data
            # For now, we'll simulate realistic engagement metrics
            
            apollo_config = self.get_tool_config('ApolloAPI')
            apollo_client = ApolloClient(api_key=apollo_config.get('api_key', ''))
            
            # Simulate response tracking
            # In production, you'd query actual email tracking systems
            responses = self._simulate_responses()
            
            # Calculate metrics
            metrics = self._calculate_metrics(responses)
            
            self.log_step("Tracking complete", 
                         f"Open rate: {metrics['open_rate']:.1%}, Reply rate: {metrics['reply_rate']:.1%}")
            
            result = {
                "campaign_id": campaign_id,
                "responses": responses,
                "metrics": metrics
            }
            
            self.log_execution_end(result, success=True)
            
            return self.format_output(result)
            
        except Exception as e:
            error_result = self.handle_error(e, "response tracking")
            return error_result
    
    def _simulate_responses(self) -> List[Dict[str, Any]]:
        """
        Simulate email engagement data.
        
        In production, this would query actual tracking systems.
        """
        # Simulate 20 email responses
        responses = []
        
        emails = [
            "john@acme.com", "sarah@techflow.com", "mike@cloudco.com",
            "lisa@datasoft.com", "tom@salestech.com", "anna@growthco.com",
            "david@innovate.com", "emma@scaleco.com", "chris@b2bsaas.com",
            "rachel@leadgen.com"
        ]
        
        for email in emails:
            # Realistic engagement rates
            opened = random.random() < 0.5  # 50% open rate
            clicked = opened and random.random() < 0.25  # 25% of opens click
            replied = clicked and random.random() < 0.4  # 40% of clicks reply
            meeting_booked = replied and random.random() < 0.3  # 30% of replies book
            
            response_time = random.uniform(1, 72) if replied else None
            
            sentiment = "positive" if replied and random.random() < 0.7 else "neutral"
            if replied and random.random() < 0.1:
                sentiment = "negative"
            
            responses.append({
                "lead_email": email,
                "opened": opened,
                "clicked": clicked,
                "replied": replied,
                "meeting_booked": meeting_booked,
                "response_time_hours": round(response_time, 1) if response_time else None,
                "sentiment": sentiment if replied else None
            })
        
        return responses
    
    def _calculate_metrics(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate engagement metrics from responses."""
        total = len(responses)
        
        if total == 0:
            return {
                "open_rate": 0.0,
                "click_rate": 0.0,
                "reply_rate": 0.0,
                "meeting_rate": 0.0,
                "total_sent": 0
            }
        
        opened = sum(1 for r in responses if r['opened'])
        clicked = sum(1 for r in responses if r['clicked'])
        replied = sum(1 for r in responses if r['replied'])
        meetings = sum(1 for r in responses if r['meeting_booked'])
        
        return {
            "open_rate": opened / total,
            "click_rate": clicked / total,
            "reply_rate": replied / total,
            "meeting_rate": meetings / total,
            "total_sent": total
        }


if __name__ == "__main__":
    # Test Response Tracker Agent
    print("Testing ResponseTrackerAgent\n")
    
    config = {
        "id": "response_tracking",
        "instructions": "Track email responses",
        "tools": [
            {"name": "ApolloAPI", "config": {"api_key": ""}}
        ]
    }
    
    agent = ResponseTrackerAgent("response_tracking", config)
    
    test_inputs = {
        "campaign_id": "campaign_20251019_001",
        "tracking_period_hours": 72
    }
    
    result = agent.execute(test_inputs)
    
    data = result.get('data', {})
    metrics = data.get('metrics', {})
    
    print(f"\nCampaign: {data.get('campaign_id')}")
    print(f"\nMetrics:")
    print(f"  Open Rate: {metrics.get('open_rate', 0):.1%}")
    print(f"  Click Rate: {metrics.get('click_rate', 0):.1%}")
    print(f"  Reply Rate: {metrics.get('reply_rate', 0):.1%}")
    print(f"  Meeting Rate: {metrics.get('meeting_rate', 0):.1%}")
    print(f"  Total Sent: {metrics.get('total_sent', 0)}")
    
    print(f"\nSample Responses:")
    for resp in data.get('responses', [])[:5]:
        status = []
        if resp['opened']:
            status.append("Opened")
        if resp['clicked']:
            status.append("Clicked")
        if resp['replied']:
            status.append("Replied")
        print(f"  {resp['lead_email']}: {', '.join(status) if status else 'No engagement'}")
    
    print("\n✅ ResponseTrackerAgent test complete!")
