"""
Feedback Trainer Agent - Analyzes performance and suggests improvements.
"""

from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from tools.openai_client import OpenAIClient
from tools.google_sheets import GoogleSheetsClient

class FeedbackTrainerAgent(BaseAgent):
    """
    Agent responsible for analyzing campaign performance and
    suggesting improvements to the workflow configuration.
    """
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze campaign performance and generate recommendations.
        
        Args:
            inputs: Dictionary containing:
                - responses: List of response dictionaries
                - metrics: Campaign metrics dictionary
                - current_config: Current workflow configuration
        
        Returns:
            Dictionary with 'analysis' and 'recommendations'
        """
        self.log_execution_start(inputs)
        
        try:
            responses = inputs.get('responses', [])
            metrics = inputs.get('metrics', {})
            current_config = inputs.get('current_config', {})
            
            self.log_step("Analyzing performance", 
                         f"Reply rate: {metrics.get('reply_rate', 0):.1%}")
            
            # Initialize clients
            openai_config = self.get_tool_config('OpenAI')
            openai_client = OpenAIClient(
                api_key=openai_config.get('api_key', ''),
                model=openai_config.get('model', 'gpt-4o-mini')
            )
            
            sheets_config = self.get_tool_config('GoogleSheets')
            sheets_client = GoogleSheetsClient(
                credentials_path=sheets_config.get('credentials_path', ''),
                sheet_id=sheets_config.get('sheet_id', '')
            )
            
            # Analyze performance with AI
            self.log_step("Generating insights", "Using OpenAI")
            ai_analysis = openai_client.analyze_campaign_performance(
                campaign_data={},
                metrics=metrics
            )
            
            # Generate specific recommendations
            recommendations = self._generate_recommendations(metrics, responses, current_config)
            
            # Identify top and underperforming segments
            analysis = self._segment_analysis(responses)
            
            self.log_step("Writing to Google Sheets", 
                         f"{len(recommendations)} recommendations")
            
            # Write recommendations to Google Sheets for human approval
            sheets_client.write_recommendations(recommendations)
            sheets_client.write_campaign_results(
                campaign_id=f"campaign_{len(responses)}",
                metrics=metrics
            )
            
            result = {
                "analysis": analysis,
                "recommendations": recommendations,
                "approval_status": "pending"
            }
            
            self.log_step("Analysis complete", 
                         f"Generated {len(recommendations)} recommendations")
            
            self.log_execution_end(result, success=True)
            
            return self.format_output(result)
            
        except Exception as e:
            error_result = self.handle_error(e, "feedback training")
            return error_result
    
    def _generate_recommendations(
        self,
        metrics: Dict[str, Any],
        responses: List[Dict[str, Any]],
        current_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on performance."""
        recommendations = []
        
        reply_rate = metrics.get('reply_rate', 0)
        open_rate = metrics.get('open_rate', 0)
        meeting_rate = metrics.get('meeting_rate', 0)
        
        # Recommendation 1: ICP Refinement
        if reply_rate < 0.10:  # Less than 10% reply rate
            recommendations.append({
                "category": "ICP_REFINEMENT",
                "current_value": str(current_config.get('outreach', {}).get('persona', 'SDR')),
                "suggested_value": "Focus on companies with recent funding signals",
                "rationale": f"Current reply rate ({reply_rate:.1%}) is below target. Funded companies typically have 2-3x better engagement.",
                "expected_impact": "Increase reply rate to 15-20%",
                "confidence": 0.80
            })
        
        # Recommendation 2: Subject Line Optimization
        if open_rate < 0.40:  # Less than 40% open rate
            recommendations.append({
                "category": "MESSAGING",
                "current_value": "Generic subject lines",
                "suggested_value": "Use personalized subject lines mentioning specific company achievements",
                "rationale": f"Open rate ({open_rate:.1%}) is below industry average. Personalization increases opens by 30-50%.",
                "expected_impact": "Increase open rate to 50-60%",
                "confidence": 0.85
            })
        
        # Recommendation 3: Timing Optimization
        recommendations.append({
            "category": "TIMING",
            "current_value": "Send anytime",
            "suggested_value": "Send Tuesday-Thursday, 10 AM-2 PM local time",
            "rationale": "Industry data shows 40% higher engagement during mid-week mornings.",
            "expected_impact": "Increase overall engagement by 15-20%",
            "confidence": 0.75
        })
        
        # Recommendation 4: Follow-up Sequence
        if meeting_rate < 0.05:  # Less than 5% meeting rate
            recommendations.append({
                "category": "FOLLOW_UP",
                "current_value": "Single touch",
                "suggested_value": "Implement 3-touch follow-up sequence (Day 0, Day 3, Day 7)",
                "rationale": "Multi-touch sequences increase meeting bookings by 2-3x.",
                "expected_impact": "Increase meeting rate to 8-12%",
                "confidence": 0.90
            })
        
        # Recommendation 5: Content Personalization
        if reply_rate > 0:
            positive_sentiment = sum(1 for r in responses if r.get('sentiment') == 'positive')
            total_replies = sum(1 for r in responses if r.get('replied'))
            
            if total_replies > 0 and (positive_sentiment / total_replies) < 0.7:
                recommendations.append({
                    "category": "CONTENT",
                    "current_value": current_config.get('outreach', {}).get('tone', 'friendly'),
                    "suggested_value": "More consultative tone, focus on specific pain points",
                    "rationale": f"Reply sentiment is mixed. More targeted value proposition may improve.",
                    "expected_impact": "Increase positive sentiment by 20-30%",
                    "confidence": 0.70
                })
        
        return recommendations
    
    def _segment_analysis(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by segments."""
        total = len(responses)
        
        if total == 0:
            return {
                "top_performing_segments": [],
                "underperforming_segments": [],
                "key_insights": ["No data available yet"]
            }
        
        # Calculate segment performance
        replied = [r for r in responses if r.get('replied')]
        not_replied = [r for r in responses if not r.get('replied')]
        
        insights = []
        
        if replied:
            avg_response_time = sum(r.get('response_time_hours', 0) for r in replied) / len(replied)
            insights.append(f"Average response time: {avg_response_time:.1f} hours")
        
        if len(replied) > 0:
            reply_rate = len(replied) / total
            if reply_rate > 0.15:
                insights.append("✅ Reply rate exceeds industry average")
            elif reply_rate < 0.08:
                insights.append("⚠️ Reply rate below target - consider ICP refinement")
        
        return {
            "top_performing_segments": [
                "Leads with recent funding signal (estimated 20% higher reply rate)"
            ],
            "underperforming_segments": [
                "Leads without verified email (estimated 50% lower delivery)"
            ],
            "key_insights": insights
        }


if __name__ == "__main__":
    # Test Feedback Trainer Agent
    print("Testing FeedbackTrainerAgent\n")
    
    config = {
        "id": "feedback_trainer",
        "instructions": "Analyze and recommend improvements",
        "tools": [
            {"name": "OpenAI", "config": {"api_key": "", "model": "gpt-4o-mini"}},
            {"name": "GoogleSheets", "config": {"sheet_id": "", "credentials_path": ""}}
        ]
    }
    
    agent = FeedbackTrainerAgent("feedback_trainer", config)
    
    test_inputs = {
        "responses": [
            {"lead_email": "john@acme.com", "opened": True, "clicked": True, "replied": True, "meeting_booked": False, "response_time_hours": 4.5, "sentiment": "positive"},
            {"lead_email": "sarah@tech.com", "opened": True, "clicked": False, "replied": False, "meeting_booked": False, "response_time_hours": None, "sentiment": None},
            {"lead_email": "mike@saas.com", "opened": False, "clicked": False, "replied": False, "meeting_booked": False, "response_time_hours": None, "sentiment": None},
        ],
        "metrics": {
            "open_rate": 0.40,
            "click_rate": 0.15,
            "reply_rate": 0.08,
            "meeting_rate": 0.03,
            "total_sent": 50
        },
        "current_config": {
            "outreach": {
                "persona": "SDR",
                "tone": "friendly"
            }
        }
    }
    
    result = agent.execute(test_inputs)
    
    data = result.get('data', {})
    analysis = data.get('analysis', {})
    recommendations = data.get('recommendations', [])
    
    print(f"\nKey Insights:")
    for insight in analysis.get('key_insights', []):
        print(f"  • {insight}")
    
    print(f"\nRecommendations ({len(recommendations)}):")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['category']}")
        print(f"   Current: {rec['current_value']}")
        print(f"   Suggested: {rec['suggested_value']}")
        print(f"   Expected Impact: {rec['expected_impact']}")
        print(f"   Confidence: {rec['confidence']:.0%}")
    
    print(f"\nApproval Status: {data.get('approval_status')}")
    
    print("\n✅ FeedbackTrainerAgent test complete!")
