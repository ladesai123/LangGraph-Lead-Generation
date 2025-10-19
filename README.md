# 🚀 LangGraph Autonomous Prospect-to-Lead Workflow

An end-to-end AI agent system that autonomously discovers, enriches, scores, and contacts B2B prospects using LangGraph orchestration.

## 📋 Overview

This system uses **LangGraph** to coordinate 7 specialized AI agents that work together to automate outbound lead generation for B2B companies targeting the USA market ($20M-$200M revenue).

### 🎯 Key Features

- **Dynamic Workflow**: Entire pipeline configured via `workflow.json`
- **7 Specialized Agents**: Each handles one step of the lead generation process
- **Self-Improving**: Feedback loop analyzes performance and suggests optimizations
- **API Integrations**: Clay, Apollo, Clearbit, OpenAI, SendGrid, Google Sheets
- **Production-Ready**: Logging, error handling, dry-run mode

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     workflow.json                           │
│              (Configuration & Orchestration)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌───────────────────────────┐
        │  LangGraph Builder        │
        │  (langgraph_builder.py)   │
        └─────────────┬─────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐          ┌───────────────┐
│  Agent Nodes  │          │  Tool Layer   │
├───────────────┤          ├───────────────┤
│ 1. Prospect   │◄────────►│ Clay API      │
│ 2. Enrichment │          │ Apollo API    │
│ 3. Scoring    │          │ Clearbit API  │
│ 4. Content    │          │ OpenAI API    │
│ 5. Executor   │          │ SendGrid API  │
│ 6. Tracker    │          │ Google Sheets │
│ 7. Feedback   │          └───────────────┘
└───────────────┘
```

### 🤖 The 7 Agents

1. **ProspectSearchAgent**: Finds companies matching ICP using Clay/Apollo
2. **DataEnrichmentAgent**: Enriches leads with additional data (Clearbit)
3. **ScoringAgent**: Scores and ranks leads based on fit
4. **OutreachContentAgent**: Generates personalized emails (OpenAI GPT-4)
5. **OutreachExecutorAgent**: Sends emails via SendGrid/Apollo
6. **ResponseTrackerAgent**: Monitors replies and engagement
7. **FeedbackTrainerAgent**: Analyzes results and suggests improvements

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- API Keys (see Setup section)
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd LeadGenerator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env and add your API keys
notepad .env
```

### 🔑 API Keys Setup

You'll need accounts and API keys for:

1. **OpenAI** (Required): https://platform.openai.com/api-keys
2. **Apollo.io** (Freemium): https://apollo.io - 50 free credits/month
3. **Clay** (Optional): https://clay.com
4. **Clearbit** (Trial): https://clearbit.com
5. **SendGrid** (Free): https://sendgrid.com - 100 emails/day free
6. **Google Sheets**: Enable Google Sheets API in Google Cloud Console

---

## 📖 Usage

### Running the Complete Workflow

```bash
python langgraph_builder.py
```

This will:
1. Load `workflow.json`
2. Build the LangGraph with all 7 agents
3. Execute the workflow end-to-end
4. Save results to `logs/` and output files

### Dry Run Mode (Testing Without Sending Emails)

```bash
# In .env, set:
ENABLE_DRY_RUN=true
```

This simulates email sending without actually contacting prospects.

---

## 🔧 Configuration

### Modifying the Workflow

Edit `workflow.json` to customize:

- **ICP Criteria**: Industry, location, revenue, employee count
- **Scoring Rules**: Weights for different signals
- **Outreach Tone**: Friendly, formal, casual
- **Agent Instructions**: Custom prompts for each agent

Example:

```json
{
  "id": "prospect_search",
  "inputs": {
    "icp": {
      "industry": "FinTech",
      "location": "USA",
      "employee_count": { "min": 50, "max": 500 }
    }
  }
}
```

---

## 📁 Project Structure

```
LeadGenerator/
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base class for all agents
│   ├── prospect_search.py      # Agent 1
│   ├── data_enrichment.py      # Agent 2
│   ├── scoring.py              # Agent 3
│   ├── outreach_content.py     # Agent 4
│   ├── outreach_executor.py    # Agent 5
│   ├── response_tracker.py     # Agent 6
│   └── feedback_trainer.py     # Agent 7
├── tools/                       # API integrations
│   ├── __init__.py
│   ├── clay_api.py
│   ├── apollo_api.py
│   ├── clearbit_api.py
│   ├── openai_client.py
│   ├── sendgrid_client.py
│   └── google_sheets.py
├── utils/                       # Utilities
│   ├── __init__.py
│   ├── config_loader.py        # Load workflow.json
│   ├── logger.py               # Logging setup
│   └── validators.py           # JSON schema validation
├── workflow.json                # Workflow configuration
├── langgraph_builder.py        # Main orchestrator
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_agents.py

# With coverage
pytest --cov=agents --cov-report=html
```

---

## 🎥 Demo Video

[Link to demo video]

The demo covers:
- Project setup and configuration
- Running the workflow end-to-end
- Explanation of each agent's role
- Results and output files

---

## 🛠️ Development

### Adding a New Agent

1. Create new file in `agents/` inheriting from `BaseAgent`
2. Implement `execute()` method
3. Add to `workflow.json`
4. Register in `langgraph_builder.py`

### Extending Tools

1. Create new tool in `tools/`
2. Add configuration to `workflow.json`
3. Import in relevant agent

---

## 🐛 Troubleshooting

### Common Issues

**Error: API Key not found**
- Check `.env` file exists and has correct keys
- Ensure no extra spaces in API keys

**Error: Module not found**
- Run `pip install -r requirements.txt`
- Check virtual environment is activated

**Email not sending**
- Verify SendGrid API key
- Check `ENABLE_DRY_RUN` setting
- Review logs in `logs/` directory

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👤 Author

[Your Name]

**Submission for**: Analytos.ai - LangGraph Prospect-to-Lead Workflow Assessment

---

## 🙏 Acknowledgments

- LangGraph/LangChain for agent orchestration
- OpenAI for GPT-4 reasoning
- Apollo, Clay, Clearbit for data APIs

---

**Built with ❤️ using AI-assisted development (vibe coding)**
