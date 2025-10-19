"""
AI API client for content generation and reasoning.

Supports both OpenAI and Google Gemini APIs.
"""

from openai import OpenAI
from typing import Dict, List, Any, Optional
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Gemini SDK not installed. Install with: pip install google-generativeai")


class OpenAIClient:
    """Client for AI APIs (OpenAI or Gemini)."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini", provider: str = "openai"):
        """
        Initialize AI client.
        
        Args:
            api_key: API key (OpenAI or Gemini)
            model: Model to use (default: gpt-4o-mini for OpenAI, gemini-1.5-flash for Gemini)
            provider: 'openai' or 'gemini'
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.client = None
        
        # Auto-detect provider from environment if not specified
        if not api_key:
            gemini_key = os.getenv('GEMINI_API_KEY')
            openai_key = os.getenv('OPENAI_API_KEY')
            provider_env = os.getenv('AI_PROVIDER', 'gemini').lower()
            
            if provider_env == 'gemini' and gemini_key:
                self.provider = 'gemini'
                self.api_key = gemini_key
            elif openai_key:
                self.provider = 'openai'
                self.api_key = openai_key
        
        # Initialize appropriate client
        if self.provider == 'gemini':
            if GEMINI_AVAILABLE and self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = "gemini-2.5-flash"  # Latest free model!
                self.client = genai.GenerativeModel(self.model)
                logger.info(f"✅ Initialized Gemini client with model: {self.model}")
            else:
                logger.warning("Gemini selected but SDK not available - will use mock responses")
        else:
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
                self.model = model
                logger.info(f"✅ Initialized OpenAI client with model: {self.model}")
            else:
                logger.warning("OpenAI client initialized without API key - will use mock responses")
        
        if not self.client:
            logger.warning(f"AI client initialized without valid credentials - will use mock responses")
    
    def generate_email(
        self,
        lead_data: Dict[str, Any],
        persona: str = "SDR",
        tone: str = "friendly",
        company_value_prop: str = "Analytos.ai helps B2B companies optimize their sales process with AI"
    ) -> Dict[str, str]:
        """
        Generate personalized email content for a lead.
        
        Args:
            lead_data: Dictionary with lead information (name, company, role, etc.)
            persona: Persona to write as (SDR, CEO, etc.)
            tone: Tone of email (friendly, formal, casual)
            company_value_prop: Value proposition of your company
        
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        if not self.client:
            return self._generate_mock_email(lead_data)
        
        # Build prompt
        prompt = f"""You are a {persona} writing a personalized outreach email.

Lead Information:
- Name: {lead_data.get('contact', 'there')}
- Company: {lead_data.get('company', 'their company')}
- Role: {lead_data.get('role', 'their role')}
- Technologies: {', '.join(lead_data.get('technologies', [])) if lead_data.get('technologies') else 'N/A'}
- Recent News: {lead_data.get('recent_news', 'N/A')}

Your Company: {company_value_prop}

Write a {tone} outreach email that:
1. Has a compelling subject line (max 60 characters)
2. Personalizes based on their company/role/news
3. Clearly states the value proposition
4. Includes a clear call-to-action
5. Keeps the email under 150 words

Format your response as:
SUBJECT: [subject line]
BODY: [email body]
"""
        
        try:
            logger.info(f"Generating email for {lead_data.get('contact')} at {lead_data.get('company')}")
            
            # Use Gemini or OpenAI
            if self.provider == 'gemini':
                response = self.client.generate_content(prompt)
                content = response.text
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert sales copywriter."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                content = response.choices[0].message.content
            
            # Parse response
            subject = ""
            body = ""
            
            lines = content.strip().split('\n')
            for i, line in enumerate(lines):
                if line.startswith('SUBJECT:'):
                    subject = line.replace('SUBJECT:', '').strip()
                elif line.startswith('BODY:'):
                    body = '\n'.join(lines[i:]).replace('BODY:', '').strip()
                    break
            
            if not subject or not body:
                # Fallback parsing
                parts = content.split('\n\n', 1)
                subject = parts[0].replace('SUBJECT:', '').strip()
                body = parts[1].replace('BODY:', '').strip() if len(parts) > 1 else content
            
            logger.info(f"✅ Generated email with subject: {subject[:50]}...")
            
            return {
                "subject": subject,
                "body": body
            }
            
        except Exception as e:
            logger.error(f"AI API error: {e}")
            return self._generate_mock_email(lead_data)
    
    def analyze_campaign_performance(
        self,
        campaign_data: Dict[str, Any],
        metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyze campaign performance and generate recommendations.
        
        Args:
            campaign_data: Data about the campaign
            metrics: Performance metrics (open_rate, reply_rate, etc.)
        
        Returns:
            Analysis and recommendations
        """
        if not self.client:
            return self._generate_mock_analysis(metrics)
        
        prompt = f"""Analyze this email campaign performance and provide recommendations.

Campaign Metrics:
- Open Rate: {metrics.get('open_rate', 0) * 100:.1f}%
- Click Rate: {metrics.get('click_rate', 0) * 100:.1f}%
- Reply Rate: {metrics.get('reply_rate', 0) * 100:.1f}%
- Meeting Rate: {metrics.get('meeting_rate', 0) * 100:.1f}%
- Total Sent: {metrics.get('total_sent', 0)}

Provide:
1. Key insights (what worked, what didn't)
2. 3-5 specific, actionable recommendations
3. Expected impact of each recommendation
4. Confidence level (0-1) for each

Format as JSON.
"""
        
        try:
            logger.info("Analyzing campaign performance with AI")
            
            # Use Gemini or OpenAI
            if self.provider == 'gemini':
                response = self.client.generate_content(prompt)
                content = response.text
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a sales analytics expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=800
                )
                content = response.choices[0].message.content
            
            logger.info("✅ Generated campaign analysis")
            
            return {
                "analysis": content,
                "recommendations_generated": True
            }
            
        except Exception as e:
            logger.error(f"AI API error: {e}")
            return self._generate_mock_analysis(metrics)
    
    def _generate_mock_email(self, lead_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate mock email for testing."""
        logger.warning("Using mock email generation")
        
        name = lead_data.get('contact', 'there')
        company = lead_data.get('company', 'your company')
        
        return {
            "subject": f"Quick question about {company}'s sales process",
            "body": f"""Hi {name},

I noticed {company} is growing rapidly and wanted to reach out.

At Analytos.ai, we help B2B companies like yours optimize their sales process with AI-powered insights. Many of our clients see a 30% increase in conversion rates within the first quarter.

Would you be open to a quick 15-minute call next week to explore how we might help {company}?

Best regards,
Sales Team @ Analytos.ai

P.S. I saw your recent news and was impressed!"""
        }
    
    def _generate_mock_analysis(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Generate mock analysis for testing."""
        logger.warning("Using mock campaign analysis")
        
        reply_rate = metrics.get('reply_rate', 0)
        
        if reply_rate < 0.1:
            insight = "Reply rate is below industry average. Consider improving personalization."
        else:
            insight = "Reply rate is above average. Current approach is working well."
        
        return {
            "analysis": insight,
            "recommendations": [
                {
                    "category": "MESSAGING",
                    "suggestion": "Test shorter email copy (under 100 words)",
                    "expected_impact": "15% improvement in reply rate",
                    "confidence": 0.75
                }
            ],
            "recommendations_generated": True
        }


if __name__ == "__main__":
    # Test OpenAI client (mock mode)
    print("Testing OpenAI Client (Mock Mode)\n")
    
    client = OpenAIClient(api_key=None, model="gpt-4o-mini")
    
    # Test email generation
    print("=== Generating Email ===")
    test_lead = {
        "contact": "John Smith",
        "company": "Acme SaaS Inc",
        "role": "VP of Sales",
        "technologies": ["Salesforce", "HubSpot"],
        "recent_news": "Raised $10M Series A"
    }
    
    email = client.generate_email(test_lead, persona="SDR", tone="friendly")
    print(f"Subject: {email['subject']}")
    print(f"\n{email['body']}\n")
    
    # Test campaign analysis
    print("=== Analyzing Campaign ===")
    test_metrics = {
        "open_rate": 0.45,
        "click_rate": 0.12,
        "reply_rate": 0.08,
        "meeting_rate": 0.03,
        "total_sent": 50
    }
    
    analysis = client.analyze_campaign_performance({}, test_metrics)
    print(f"Analysis: {analysis['analysis']}")
    
    print("\n✅ OpenAI client test complete!")
