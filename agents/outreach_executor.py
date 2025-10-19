"""
Outreach Executor Agent - Sends emails to prospects.
"""

from typing import Dict, Any, List
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from tools.sendgrid_client import SendGridClient

class OutreachExecutorAgent(BaseAgent):
    """
    Agent responsible for sending outreach emails to prospects.
    """
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send emails to prospects.
        
        Args:
            inputs: Dictionary containing:
                - messages: List of email message dictionaries
                - dry_run: If True, simulate sending (default: True)
        
        Returns:
            Dictionary with 'sent_status' list and 'campaign_id'
        """
        self.log_execution_start(inputs)
        
        try:
            messages = inputs.get('messages', [])
            dry_run = inputs.get('dry_run', True)
            
            # Generate campaign ID
            campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            mode = "DRY RUN" if dry_run else "LIVE"
            self.log_step(f"Sending emails ({mode})", 
                         f"Processing {len(messages)} messages")
            
            # Initialize SendGrid client
            sendgrid_config = self.get_tool_config('SendGrid') or {}
            from_email = sendgrid_config.get('from_email', 'outreach@analytos.ai')
            
            sendgrid_client = SendGridClient(
                api_key=sendgrid_config.get('api_key', ''),
                from_email=from_email
            )
            
            # Prepare emails for sending
            emails_to_send = []
            for msg in messages:
                emails_to_send.append({
                    'to': msg['lead_email'],
                    'subject': msg['subject'],
                    'body': msg['email_body']
                })
            
            # Send emails (or simulate)
            results = sendgrid_client.send_bulk_emails(emails_to_send, dry_run=dry_run)
            
            # Format sent status
            sent_status = []
            for sent in results['sent']:
                sent_status.append({
                    "lead_email": sent['to'],
                    "status": "sent",
                    "message_id": sent['message_id'],
                    "sent_at": datetime.now().isoformat(),
                    "error": None
                })
            
            for failed in results['failed']:
                sent_status.append({
                    "lead_email": failed['to'],
                    "status": "failed",
                    "message_id": None,
                    "sent_at": datetime.now().isoformat(),
                    "error": failed.get('error', 'Unknown error')
                })
            
            summary = {
                "total": len(messages),
                "sent": len(results['sent']),
                "failed": len(results['failed']),
                "skipped": 0
            }
            
            self.log_step("Email sending complete", 
                         f"Sent: {summary['sent']}, Failed: {summary['failed']}")
            
            result = {
                "campaign_id": campaign_id,
                "sent_status": sent_status,
                "summary": summary
            }
            
            self.log_execution_end(result, success=True)
            
            return self.format_output(result)
            
        except Exception as e:
            error_result = self.handle_error(e, "outreach execution")
            return error_result


if __name__ == "__main__":
    # Test Outreach Executor Agent
    print("Testing OutreachExecutorAgent\n")
    
    config = {
        "id": "send",
        "instructions": "Send outreach emails",
        "tools": [
            {"name": "SendGrid", "config": {"api_key": ""}}
        ]
    }
    
    agent = OutreachExecutorAgent("send", config)
    
    test_inputs = {
        "messages": [
            {
                "lead_email": "john@acme.com",
                "subject": "Quick question about Acme's sales process",
                "email_body": "Hi John,\n\nI noticed Acme is growing..."
            },
            {
                "lead_email": "sarah@techflow.com",
                "subject": "TechFlow + Analytos.ai",
                "email_body": "Hi Sarah,\n\nCongratulations on your growth..."
            }
        ],
        "dry_run": True
    }
    
    result = agent.execute(test_inputs)
    
    data = result.get('data', {})
    print(f"\nCampaign ID: {data.get('campaign_id')}")
    print(f"\nSummary:")
    summary = data.get('summary', {})
    print(f"  Total: {summary.get('total')}")
    print(f"  Sent: {summary.get('sent')}")
    print(f"  Failed: {summary.get('failed')}")
    
    print(f"\nSent Status:")
    for status in data.get('sent_status', [])[:3]:
        print(f"  {status['lead_email']}: {status['status']}")
    
    print("\n✅ OutreachExecutorAgent test complete!")
