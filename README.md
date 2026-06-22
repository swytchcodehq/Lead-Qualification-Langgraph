# Lead Qualification — LangGraph + Swytchcode

Automates lead capture and sales pipeline creation:
1. Creates a HubSpot contact
2. Creates a HubSpot sales opportunity (deal)

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Swytchcode](https://swytchcode.com).

---

## Prerequisites

- **Python 3.9+**
- **Swytchcode CLI.** Install with the verified script for your platform:

  Linux / macOS:
  ```bash
  curl -fsSL https://cli.swytchcode.com/install.sh | sh
  ```
  Windows (PowerShell):
  ```powershell
  irm https://cli.swytchcode.com/install.ps1 | iex
  ```


```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your API keys
cp .env.example .env


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
