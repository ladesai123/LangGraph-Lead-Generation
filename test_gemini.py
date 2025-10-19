"""Quick test of Gemini integration."""

import os
from dotenv import load_dotenv
from tools.openai_client import OpenAIClient

# Load .env file
load_dotenv()

print("=" * 60)
print("🔥 TESTING GEMINI API")
print("=" * 60)

# Get Gemini key from env
gemini_key = os.getenv('GEMINI_API_KEY')
print(f"\n✅ Gemini Key Found: {gemini_key[:20]}..." if gemini_key else "❌ No Gemini Key")

# Initialize client with Gemini
client = OpenAIClient(api_key=gemini_key, provider="gemini")

# Test lead data
test_lead = {
    'contact': 'John Smith',
    'company': 'Acme SaaS Inc',
    'role': 'VP of Sales',
    'technologies': ['Salesforce', 'HubSpot'],
    'recent_news': 'Recently raised $5M Series A'
}

print("\n📧 Generating Email with Gemini...\n")

# Generate email
email = client.generate_email(test_lead, persona="SDR", tone="friendly")

print("✅ EMAIL GENERATED!\n")
print(f"SUBJECT: {email['subject']}")
print(f"\nBODY:\n{email['body']}")

print("\n" + "=" * 60)
print("🎉 GEMINI IS WORKING PERFECTLY!")
print("=" * 60)
