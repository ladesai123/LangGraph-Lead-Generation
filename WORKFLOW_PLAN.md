# 🔄 Workflow Execution Plan

## Visual Workflow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│  1. PROSPECT SEARCH AGENT           │
│  ─────────────────────────────────  │
│  Input: ICP criteria, signals       │
│  Tools: Clay API, Apollo API        │
│  Output: 50 raw leads               │
│  Example: Find SaaS companies       │
│           100-1000 employees        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. DATA ENRICHMENT AGENT           │
│  ─────────────────────────────────  │
│  Input: 50 raw leads                │
│  Tools: Clearbit API                │
│  Output: Enriched leads with        │
│          tech stack, news, etc      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. SCORING AGENT                   │
│  ─────────────────────────────────  │
│  Input: Enriched leads              │
│  Tools: None (pure logic)           │
│  Output: Ranked leads (top 30)      │
│          with scores 60-100         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. OUTREACH CONTENT AGENT          │
│  ─────────────────────────────────  │
│  Input: Top 30 ranked leads         │
│  Tools: OpenAI GPT-4                │
│  Output: 30 personalized emails     │
│          with subject lines         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  5. OUTREACH EXECUTOR AGENT         │
│  ─────────────────────────────────  │
│  Input: 30 email drafts             │
│  Tools: SendGrid API                │
│  Output: Delivery status            │
│          Campaign ID: ABC123        │
└──────────────┬──────────────────────┘
               │
               ▼ (Wait 24-72 hours)
┌─────────────────────────────────────┐
│  6. RESPONSE TRACKER AGENT          │
│  ─────────────────────────────────  │
│  Input: Campaign ID ABC123          │
│  Tools: Apollo API                  │
│  Output: Open/Click/Reply metrics   │
│          15 opens, 5 replies        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  7. FEEDBACK TRAINER AGENT          │
│  ─────────────────────────────────  │
│  Input: Engagement metrics          │
│  Tools: OpenAI, Google Sheets       │
│  Output: Recommendations            │
│          "Try FinTech industry"     │
│          "Change subject line"      │
└──────────────┬──────────────────────┘
               │
               ▼
             END
    (Human reviews suggestions)
```

---

## Data Flow Example

### Example Lead Journey

**Starting Point:**
```json
{
  "icp": {
    "industry": "SaaS",
    "location": "USA",
    "employee_count": {"min": 100, "max": 1000},
    "revenue": {"min": 20000000, "max": 200000000}
  }
}
```

**After Agent 1 (Prospect Search):**
```json
{
  "leads": [
    {
      "company": "Acme SaaS Inc",
      "contact_name": "John Smith",
      "email": "john.smith@acmesaas.com",
      "title": "VP of Sales",
      "linkedin": "linkedin.com/in/johnsmith",
      "signal": "recent_funding",
      "company_size": 250,
      "estimated_revenue": 50000000
    }
  ]
}
```

**After Agent 2 (Enrichment):**
```json
{
  "enriched_leads": [
    {
      "company": "Acme SaaS Inc",
      "contact": "John Smith",
      "email": "john.smith@acmesaas.com",
      "role": "VP of Sales",
      "technologies": ["Salesforce", "HubSpot", "AWS"],
      "company_description": "B2B SaaS platform for sales teams",
      "recent_news": "Raised $10M Series A",
      "email_verified": true
    }
  ]
}
```

**After Agent 3 (Scoring):**
```json
{
  "ranked_leads": [
    {
      "lead": { /* full lead data */ },
      "score": 85.5,
      "score_breakdown": {
        "revenue_fit": 25.5,   // (30% weight)
        "employee_fit": 18.0,  // (20% weight)
        "tech_stack": 17.0,    // (20% weight)
        "growth_signals": 25.0 // (30% weight)
      },
      "rank": 1
    }
  ]
}
```

**After Agent 4 (Outreach Content):**
```json
{
  "messages": [
    {
      "lead_id": "acme_john_001",
      "lead_name": "John Smith",
      "lead_email": "john.smith@acmesaas.com",
      "subject": "Congrats on your Series A! Quick question about sales analytics",
      "email_body": "Hi John,\n\nCongratulations on Acme's recent $10M Series A! ...",
      "personalization_notes": "Mentioned funding, used tech stack context"
    }
  ]
}
```

**After Agent 5 (Send):**
```json
{
  "campaign_id": "campaign_2025_10_19_001",
  "sent_status": [
    {
      "lead_email": "john.smith@acmesaas.com",
      "status": "sent",
      "message_id": "sg_msg_123456",
      "sent_at": "2025-10-19T10:30:00Z",
      "error": null
    }
  ],
  "summary": {
    "total": 30,
    "sent": 28,
    "failed": 2,
    "skipped": 0
  }
}
```

**After Agent 6 (Response Tracking):**
```json
{
  "campaign_id": "campaign_2025_10_19_001",
  "responses": [
    {
      "lead_email": "john.smith@acmesaas.com",
      "opened": true,
      "clicked": true,
      "replied": true,
      "meeting_booked": true,
      "response_time_hours": 4.5,
      "sentiment": "positive"
    }
  ],
  "metrics": {
    "open_rate": 0.53,      // 53%
    "click_rate": 0.18,     // 18%
    "reply_rate": 0.12,     // 12%
    "meeting_rate": 0.08,   // 8%
    "total_sent": 28
  }
}
```

**After Agent 7 (Feedback Trainer):**
```json
{
  "analysis": {
    "top_performing_segments": [
      "Companies with recent funding (25% reply rate)",
      "VP-level contacts (15% reply rate)"
    ],
    "underperforming_segments": [
      "Companies without tech stack data (3% reply rate)"
    ],
    "key_insights": [
      "Subject lines mentioning funding perform 2x better",
      "Emails sent Tuesday-Thursday get more responses"
    ]
  },
  "recommendations": [
    {
      "category": "ICP_REFINEMENT",
      "current_value": "industry: SaaS",
      "suggested_value": "industry: SaaS, must_have_signal: recent_funding",
      "rationale": "Funded companies have 3x better conversion",
      "expected_impact": "Increase reply rate from 12% to 18%",
      "confidence": 0.85
    },
    {
      "category": "MESSAGING",
      "current_value": "Generic greeting",
      "suggested_value": "Mention specific funding round",
      "rationale": "Personalized intros get 40% more opens",
      "expected_impact": "Increase open rate from 53% to 65%",
      "confidence": 0.78
    }
  ],
  "approval_status": "pending"
}
```

---

## Execution Timeline

### Initial Run (Day 1)
- **09:00 AM**: Start workflow
- **09:05 AM**: Agent 1 completes (50 leads found)
- **09:10 AM**: Agent 2 completes (enriched data)
- **09:12 AM**: Agent 3 completes (ranked 30 leads)
- **09:20 AM**: Agent 4 completes (30 emails generated)
- **09:25 AM**: Agent 5 completes (28 emails sent)
- **Status**: Waiting for responses

### Follow-up (Day 3)
- **09:00 AM**: Agent 6 runs (track responses)
- **09:05 AM**: Agent 7 analyzes and creates recommendations
- **09:10 AM**: Human reviews suggestions in Google Sheet
- **Status**: Approve changes or reject

### Next Campaign (Day 4)
- **09:00 AM**: Run workflow with updated config
- **Improvements**: Better ICP, improved messaging
- **Expected Results**: Higher conversion rates

---

## Configuration Changes Over Time

### Campaign 1 (Week 1)
```json
{
  "icp": {
    "industry": "SaaS",
    "employee_count": {"min": 100, "max": 1000}
  },
  "results": {
    "reply_rate": 0.12
  }
}
```

### Campaign 2 (Week 2) - After Feedback
```json
{
  "icp": {
    "industry": "SaaS",
    "employee_count": {"min": 100, "max": 500},
    "required_signals": ["recent_funding"]
  },
  "results": {
    "reply_rate": 0.18  // 50% improvement!
  }
}
```

### Campaign 3 (Week 3) - Refined Further
```json
{
  "icp": {
    "industry": "FinTech",
    "employee_count": {"min": 100, "max": 500},
    "required_signals": ["recent_funding", "hiring_for_sales"]
  },
  "results": {
    "reply_rate": 0.24  // 100% improvement from original!
  }
}
```

---

## Error Handling Examples

### What Happens If...

**API Fails?**
```
Agent 1 → Apollo API fails
↓
System retries 3 times
↓
Falls back to Clay API
↓
If both fail, use mock data (for testing)
↓
Log error, continue workflow
```

**Email Bounces?**
```
Agent 5 → Email bounces
↓
Mark lead as "invalid_email"
↓
Remove from future campaigns
↓
Log to Google Sheets for review
```

**Low Response Rate?**
```
Agent 7 → Reply rate < 5%
↓
Generate urgent recommendations
↓
Suggest major ICP changes
↓
Flag for immediate human review
```

---

## Success Metrics

### What Good Looks Like

| Metric | Bad | Okay | Good | Excellent |
|--------|-----|------|------|-----------|
| Open Rate | <20% | 20-40% | 40-60% | >60% |
| Click Rate | <5% | 5-10% | 10-20% | >20% |
| Reply Rate | <5% | 5-10% | 10-15% | >15% |
| Meeting Rate | <2% | 2-5% | 5-10% | >10% |

### Campaign Goals
- **Week 1**: Get system running, 10% reply rate
- **Week 2**: Optimize, reach 15% reply rate
- **Week 3**: Scale, 50+ leads per day
- **Week 4**: 20% reply rate, 5+ meetings booked

---

## Next Steps

Now that you understand the workflow, let's build it! Ready to create the utilities?

**Say**: "Let's build the utilities!" to continue.
