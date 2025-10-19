"""
SendGrid API client for email delivery.

https://docs.sendgrid.com/api-reference/
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict, List, Any, Optional
import base64
import urllib.request
import urllib.error
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)


class SendGridClient:
    """Client for SendGrid/Twilio email API."""
    
    def __init__(self, api_key: str, from_email: str = "noreply@analytos.ai", api_key_secret: Optional[str] = None, account_sid: Optional[str] = None, auth_token: Optional[str] = None):
        """
        Initialize SendGrid/Twilio client.
        
        Args:
            api_key: SendGrid API key or Twilio Account SID
            from_email: Default sender email address
            api_key_secret: API Key Secret (for Twilio API Key authentication)
            account_sid: Twilio Account SID (for Twilio auth)
            auth_token: Twilio Auth Token (for Twilio auth)
        """
        self.from_email = from_email
        self.account_sid = account_sid or api_key if api_key and api_key.startswith('AC') else None
        self.auth_token = auth_token or api_key_secret
        
        # Check if we have Twilio credentials (Account SID + Auth Token)
        if self.account_sid and self.auth_token:
            # Use Twilio authentication
            self.use_twilio = True
            self.client = None
            logger.info("Initialized Twilio SendGrid client with Account SID authentication")
        elif api_key and api_key.startswith('SK') and api_key_secret:
            # Use Twilio API Key authentication
            self.use_twilio = True
            self.account_sid = api_key
            self.auth_token = api_key_secret
            self.client = None
            logger.info("Initialized Twilio SendGrid client with API Key SID authentication")
        else:
            # Standard SendGrid API key (starts with SG.)
            self.use_twilio = False
            self.api_key = api_key
            self.client = SendGridAPIClient(api_key) if api_key else None
            logger.info("Initialized SendGrid client with standard API key")
        
        if not self.client and not self.use_twilio:
            logger.warning("SendGrid client initialized without API key - will simulate sending")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email via SendGrid or Twilio.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Email body (plain text or HTML)
            from_email: Override sender email
        
        Returns:
            Status dictionary with success/failure info
        """
        sender = from_email or self.from_email
        
        logger.info(f"Sending email to {to_email}: '{subject}'")
        
        # Use Twilio API if configured
        if self.use_twilio:
            return self._send_via_twilio(to_email, subject, body, sender)
        
        if not self.client:
            return self._simulate_send(to_email, subject)
        
        try:
            message = Mail(
                from_email=Email(sender),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", body)
            )
            
            response = self.client.send(message)
            
            logger.info(f"Email sent successfully to {to_email} (Status: {response.status_code})")
            
            return {
                "status": "sent",
                "message_id": response.headers.get('X-Message-Id', 'unknown'),
                "to": to_email,
                "subject": subject,
                "status_code": response.status_code
            }
            
        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return {
                "status": "failed",
                "to": to_email,
                "error": str(e)
            }
    
    def _send_via_twilio(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: str
    ) -> Dict[str, Any]:
        """
        Send email via Twilio SendGrid API using HTTP Basic Auth.
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body: Email body
            from_email: Sender email
        
        Returns:
            Status dictionary
        """
        try:
            # Prepare the email data
            data = {
                "personalizations": [
                    {
                        "to": [{"email": to_email}],
                        "subject": subject
                    }
                ],
                "from": {"email": from_email},
                "content": [
                    {
                        "type": "text/plain",
                        "value": body
                    }
                ]
            }
            
            # Convert to JSON
            json_data = json.dumps(data).encode('utf-8')
            
            # Create request with Basic Auth
            url = "https://api.sendgrid.com/v3/mail/send"
            req = urllib.request.Request(url, data=json_data, method='POST')
            
            # Add headers
            req.add_header('Content-Type', 'application/json')
            
            # Add Basic Authentication header
            credentials = f"{self.account_sid}:{self.auth_token}"
            encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
            req.add_header('Authorization', f'Basic {encoded_credentials}')
            
            # Send request
            response = urllib.request.urlopen(req)
            
            logger.info(f"✅ Email sent successfully to {to_email} via Twilio (Status: {response.status})")
            
            return {
                "status": "sent",
                "message_id": response.headers.get('X-Message-Id', 'unknown'),
                "to": to_email,
                "subject": subject,
                "status_code": response.status
            }
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            logger.error(f"Twilio SendGrid HTTP Error {e.code}: {error_body}")
            return {
                "status": "failed",
                "to": to_email,
                "error": f"HTTP {e.code}: {error_body}"
            }
        except Exception as e:
            logger.error(f"Twilio SendGrid error: {e}")
            return {
                "status": "failed",
                "to": to_email,
                "error": str(e)
            }
    
    def send_bulk_emails(
        self,
        emails: List[Dict[str, str]],
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Send multiple emails.
        
        Args:
            emails: List of email dicts with 'to', 'subject', 'body' keys
            dry_run: If True, simulate sending without actually sending
        
        Returns:
            Summary with sent/failed counts
        """
        results = {
            "sent": [],
            "failed": [],
            "total": len(emails)
        }
        
        for email_data in emails:
            if dry_run:
                result = self._simulate_send(
                    email_data['to'],
                    email_data['subject']
                )
            else:
                result = self.send_email(
                    to_email=email_data['to'],
                    subject=email_data['subject'],
                    body=email_data['body']
                )
            
            if result['status'] == 'sent':
                results['sent'].append(result)
            else:
                results['failed'].append(result)
        
        logger.info(
            f"Bulk send complete: {len(results['sent'])} sent, "
            f"{len(results['failed'])} failed (Dry run: {dry_run})"
        )
        
        return results
    
    def _simulate_send(self, to_email: str, subject: str) -> Dict[str, Any]:
        """Simulate email sending for testing."""
        logger.info(f"[DRY RUN] Would send email to {to_email}: '{subject}'")
        
        return {
            "status": "sent",
            "message_id": f"sim_{hash(to_email + subject)}",
            "to": to_email,
            "subject": subject,
            "simulated": True
        }


if __name__ == "__main__":
    # Test SendGrid client (dry run mode)
    print("Testing SendGrid Client (Dry Run Mode)\n")
    
    client = SendGridClient(api_key=None, from_email="test@analytos.ai")
    
    # Test single email
    print("=== Sending Single Email ===")
    result = client.send_email(
        to_email="john.smith@example.com",
        subject="Test Email from Analytos.ai",
        body="This is a test email."
    )
    print(f"Status: {result['status']}")
    print(f"Message ID: {result['message_id']}")
    print(f"Simulated: {result.get('simulated', False)}\n")
    
    # Test bulk emails
    print("=== Sending Bulk Emails ===")
    test_emails = [
        {
            "to": "john@example.com",
            "subject": "Personalized email for John",
            "body": "Hi John, ..."
        },
        {
            "to": "sarah@example.com",
            "subject": "Personalized email for Sarah",
            "body": "Hi Sarah, ..."
        },
        {
            "to": "mike@example.com",
            "subject": "Personalized email for Mike",
            "body": "Hi Mike, ..."
        }
    ]
    
    results = client.send_bulk_emails(test_emails, dry_run=True)
    print(f"Total: {results['total']}")
    print(f"Sent: {len(results['sent'])}")
    print(f"Failed: {len(results['failed'])}")
    
    print("\n✅ SendGrid client test complete!")
