# Lead Qualification — LangGraph + Swytchcode

Automates lead capture and sales pipeline creation:
1. Creates a HubSpot contact
2. Creates a HubSpot sales opportunity (deal)

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Swytchcode](https://swytchcode.com).

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your API keys
cp .env.example .env

# 3. Fetch all integrations
swytchcode bootstrap
```

## Run

```bash
python main.py
```

## Canonical IDs Used

| Service | Canonical ID              |
|---------|---------------------------|
| HubSpot | `crm.v3.contacts.create`  |
| HubSpot | `crm.v3.deals.create`     |
