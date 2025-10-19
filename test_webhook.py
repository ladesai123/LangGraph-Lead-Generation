"""
Test webhook events locally - Simulate SendGrid events
"""

import requests
import json
from datetime import datetime
import time

# Your local webhook URL
WEBHOOK_URL = "http://localhost:5000/webhook/sendgrid"

# Your 10 friends' emails
friends = [
    "126156075@sastra.ac.in",  # Lade Sai Teja - OpenAI
    "126005041@sastra.ac.in",  # Shanmuga Priya - Google
    "125004343@sastra.ac.in",  # Venkateshwarlu - Meta
    "126156074@sastra.ac.in",  # Kumar - AWS
    "126015065@sastra.ac.in",  # Narsi - NVIDIA
    "ladesaiteja24@gmail.com",  # SaiTejaInc - Adobe
    "shanmugapriyapalanivel2005@gmail.com",  # Shanmuga - Anthropic
    "ladechandarrao35@gmail.com",  # Lade Chandar Rao - Tesla
    "126156007@sastra.ac.in",  # Rishi - IBM
    "126156101@sastra.ac.in",  # Lohit - Hugging Face
]

def send_event(event_type, email, extra_data=None):
    """Send a simulated SendGrid event."""
    event = {
        "email": email,
        "timestamp": int(datetime.now().timestamp()),
        "event": event_type,
        "sg_event_id": f"sim_{event_type}_{hash(email)}",
        "sg_message_id": f"msg_{hash(email)}"
    }
    
    if extra_data:
        event.update(extra_data)
    
    try:
        response = requests.post(WEBHOOK_URL, json=[event])
        if response.status_code == 200:
            print(f"✅ Sent {event_type} event for {email}")
        else:
            print(f"❌ Failed to send event: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def simulate_campaign():
    """Simulate a realistic email campaign."""
    print("🚀 Simulating Email Campaign Events...\n")
    
    # 1. All emails delivered
    print("📬 Phase 1: Emails Delivered")
    for email in friends:
        send_event("delivered", email)
        time.sleep(0.2)
    
    time.sleep(1)
    
    # 2. Some friends open emails (70%)
    print("\n👀 Phase 2: Email Opens")
    openers = friends[:7]  # First 7 friends open
    for email in openers:
        send_event("open", email, {
            "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        time.sleep(0.3)
    
    time.sleep(1)
    
    # 3. Some click links (40%)
    print("\n🖱️ Phase 3: Link Clicks")
    clickers = friends[:4]  # First 4 friends click
    for email in clickers:
        send_event("click", email, {
            "url": "https://analytos.ai",
            "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        time.sleep(0.3)
    
    time.sleep(1)
    
    # 4. One email bounces
    print("\n⚠️ Phase 4: One Bounce")
    send_event("bounce", friends[-1], {
        "reason": "550 5.1.1 The email account does not exist",
        "type": "bounce",
        "status": "5.1.1"
    })
    
    print("\n✅ Simulation Complete!")
    print("\n📊 Check your dashboard at http://localhost:5000/")
    print("🔄 Or get stats at http://localhost:5000/stats")

if __name__ == "__main__":
    print("=" * 60)
    print("  SendGrid Event Simulation")
    print("=" * 60)
    print("\nThis will simulate real SendGrid events for testing.")
    print("Make sure your webhook server is running!\n")
    
    input("Press Enter to start simulation...")
    
    simulate_campaign()
