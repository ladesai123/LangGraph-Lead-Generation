"""
SendGrid Event Webhook Server - Real-time email tracking
Receives events from SendGrid: opens, clicks, bounces, spam reports, etc.
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)

# Store events in a JSON file
EVENTS_FILE = Path("tracking_events.json")

def load_events():
    """Load existing events from file."""
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE, 'r') as f:
            return json.load(f)
    return {"events": []}

def save_event(event_data):
    """Save a new event to the tracking file."""
    events = load_events()
    
    # Add timestamp
    event_data['received_at'] = datetime.now().isoformat()
    
    # Append event
    events['events'].append(event_data)
    
    # Save to file
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=2)
    
    logger.info(f"📊 Tracked event: {event_data.get('event')} for {event_data.get('email')}")

@app.route('/webhook/sendgrid', methods=['POST'])
def sendgrid_webhook():
    """
    Receive SendGrid event webhook.
    
    SendGrid Event Types:
    - processed: Message has been received and is ready to be delivered
    - dropped: Message could not be delivered
    - delivered: Message has been successfully delivered
    - deferred: Receiving server temporarily rejected message
    - bounce: Receiving server permanently rejected message
    - open: Recipient has opened the HTML message
    - click: Recipient clicked on a link in the message
    - spam_report: Recipient marked message as spam
    - unsubscribe: Recipient clicked unsubscribe link
    - group_unsubscribe: Recipient unsubscribed from group
    - group_resubscribe: Recipient resubscribed to group
    """
    try:
        # Get events from SendGrid (they send as array)
        events = request.json
        
        if not events:
            return jsonify({"status": "error", "message": "No events received"}), 400
        
        # Process each event
        for event in events:
            event_type = event.get('event')
            email = event.get('email')
            timestamp = event.get('timestamp')
            
            logger.info(f"📬 Received {event_type} event for {email}")
            
            # Save event
            save_event(event)
            
            # Log important events
            if event_type == 'open':
                logger.info(f"👀 EMAIL OPENED by {email}!")
            elif event_type == 'click':
                url = event.get('url', 'unknown')
                logger.info(f"🖱️ LINK CLICKED by {email}: {url}")
            elif event_type == 'bounce':
                reason = event.get('reason', 'unknown')
                logger.warning(f"⚠️ EMAIL BOUNCED for {email}: {reason}")
            elif event_type == 'spam_report':
                logger.warning(f"🚫 SPAM REPORT from {email}")
        
        return jsonify({
            "status": "success",
            "message": f"Processed {len(events)} events"
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get current tracking statistics."""
    try:
        events = load_events()
        event_list = events.get('events', [])
        
        # Calculate stats
        stats = {
            "total_events": len(event_list),
            "opens": len([e for e in event_list if e.get('event') == 'open']),
            "clicks": len([e for e in event_list if e.get('event') == 'click']),
            "bounces": len([e for e in event_list if e.get('event') == 'bounce']),
            "spam_reports": len([e for e in event_list if e.get('event') == 'spam_report']),
            "delivered": len([e for e in event_list if e.get('event') == 'delivered']),
            "unique_opens": len(set([e.get('email') for e in event_list if e.get('event') == 'open'])),
            "unique_clicks": len(set([e.get('email') for e in event_list if e.get('event') == 'click'])),
        }
        
        # Get per-email stats
        email_stats = {}
        for event in event_list:
            email = event.get('email')
            event_type = event.get('event')
            
            if email not in email_stats:
                email_stats[email] = {
                    "email": email,
                    "opens": 0,
                    "clicks": 0,
                    "delivered": False,
                    "bounced": False,
                    "last_activity": None
                }
            
            if event_type == 'open':
                email_stats[email]['opens'] += 1
            elif event_type == 'click':
                email_stats[email]['clicks'] += 1
            elif event_type == 'delivered':
                email_stats[email]['delivered'] = True
            elif event_type == 'bounce':
                email_stats[email]['bounced'] = True
            
            # Update last activity
            timestamp = event.get('timestamp') or event.get('received_at')
            if timestamp:
                email_stats[email]['last_activity'] = timestamp
        
        return jsonify({
            "stats": stats,
            "by_email": list(email_stats.values()),
            "recent_events": event_list[-10:]  # Last 10 events
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "SendGrid Webhook Server",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Simple dashboard."""
    events = load_events()
    event_list = events.get('events', [])
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Tracking Dashboard</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
            .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
            .stat-card h3 { margin: 0; font-size: 32px; }
            .stat-card p { margin: 10px 0 0 0; opacity: 0.9; }
            .events { margin-top: 30px; }
            .event { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #667eea; }
            .event-open { border-left-color: #48bb78; }
            .event-click { border-left-color: #4299e1; }
            .event-bounce { border-left-color: #f56565; }
            button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            button:hover { background: #5568d3; }
        </style>
        <script>
            function refreshStats() {
                fetch('/stats')
                    .then(response => response.json())
                    .then(data => {
                        location.reload();
                    });
            }
            
            // Auto-refresh every 10 seconds
            setInterval(refreshStats, 10000);
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📧 Real-Time Email Tracking Dashboard</h1>
            <p>Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>""" + str(len([e for e in event_list if e.get('event') == 'delivered'])) + """</h3>
                    <p>📬 Delivered</p>
                </div>
                <div class="stat-card">
                    <h3>""" + str(len(set([e.get('email') for e in event_list if e.get('event') == 'open']))) + """</h3>
                    <p>👀 Unique Opens</p>
                </div>
                <div class="stat-card">
                    <h3>""" + str(len([e for e in event_list if e.get('event') == 'click'])) + """</h3>
                    <p>🖱️ Total Clicks</p>
                </div>
                <div class="stat-card">
                    <h3>""" + str(len([e for e in event_list if e.get('event') == 'bounce'])) + """</h3>
                    <p>⚠️ Bounces</p>
                </div>
            </div>
            
            <button onclick="location.reload()">🔄 Refresh</button>
            <button onclick="fetch('/stats').then(r => r.json()).then(d => console.log(d))">📊 View JSON Stats</button>
            
            <div class="events">
                <h2>Recent Events (Last 20)</h2>
    """
    
    # Show last 20 events
    for event in reversed(event_list[-20:]):
        event_type = event.get('event', 'unknown')
        email = event.get('email', 'unknown')
        timestamp = event.get('received_at', 'unknown')
        
        event_class = f"event-{event_type}" if event_type in ['open', 'click', 'bounce'] else ""
        
        html += f"""
                <div class="event {event_class}">
                    <strong>{event_type.upper()}</strong> - {email}<br>
                    <small>{timestamp}</small>
                </div>
        """
    
    html += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == '__main__':
    logger.info("🚀 Starting SendGrid Event Webhook Server...")
    logger.info("📍 Webhook endpoint: http://localhost:5000/webhook/sendgrid")
    logger.info("📊 Dashboard: http://localhost:5000/")
    logger.info("📈 Stats API: http://localhost:5000/stats")
    
    # Run server
    app.run(host='0.0.0.0', port=5000, debug=True)
