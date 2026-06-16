# Lead Qualification (LangGraph + Swytchcode)

A LangGraph agent that captures an inbound lead in HubSpot and opens a sales deal for it.

> Run one command to turn an inbound lead into a HubSpot contact and an associated deal in your pipeline, without writing API glue code or managing credentials and retries.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/swytchcodehq/Lead-Qualification-Langgraph?style=flat-square)](https://github.com/swytchcodehq/Lead-Qualification-Langgraph/commits)

## What this does

This demo handles inbound lead capture in HubSpot. It creates a HubSpot contact for the lead, then opens a HubSpot deal associated with that contact so the opportunity lands in your pipeline. The steps run as a LangGraph state machine, so the contact ID flows into the deal association.

Every external call goes through [Swytchcode](https://www.swytchcode.com/), a deterministic API execution layer for AI agents. The agent code never calls HubSpot directly. It asks the Swytchcode runtime to run a named method, and the runtime validates the request against a schema registry of 2,000+ integrations, handles auth and retries, and records an audit trail of what ran.

## How it works

The graph has two nodes and runs them in order:

```
create_contact -> create_deal
```

- **create_contact** splits the lead name into first and last and creates a HubSpot contact with company, phone, and lead status NEW via `crm.v3.contacts.create`.
- **create_deal** creates a HubSpot deal via `crm.v3.deals.create` in the default pipeline at the appointment-scheduled stage, with a close date 30 days out, associated to the contact from the previous node.

## Prerequisites

- **Python 3.9+**
- **Swytchcode CLI:** install with the verified script for your platform:

  Linux / macOS:
  ```bash
  curl -fsSL https://cli.swytchcode.com/install.sh | sh
  ```
  Windows (PowerShell):
  ```powershell
  irm https://cli.swytchcode.com/install.ps1 | iex
  ```
- A **HubSpot** private app token with CRM contact and deal scopes (see the table below).

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/swytchcodehq/Lead-Qualification-Langgraph.git
   cd Lead-Qualification-Langgraph
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example env file and fill in your keys:
   ```bash
   cp .env.example .env
   ```
4. Fetch the integrations declared in `.swytchcode/tooling.json`:
   ```bash
   swytchcode bootstrap
   ```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HUBSPOT_API_KEY` | Yes | HubSpot private app token, used for both the contact and the deal. |
| `SWYTCHCODE_TOKEN` | Yes | Swytchcode auth token. Get yours from the Swytchcode dashboard under Settings, API keys. |

The lead details (name, email, company, phone, deal value) are defined as a sample in `main.py`. Edit them there to qualify a different lead.

## Run

```bash
python main.py
```

## Expected output

The script prints each node as it runs and a summary at the end:

```
[1/2] Creating HubSpot contact for alex@techcorp.io...
    HubSpot contact created: 12345
[2/2] Creating HubSpot sales opportunity for TechCorp...
    HubSpot deal created: 67890

Lead qualified!
   HubSpot Contact ID: 12345
   HubSpot Deal ID:    67890
```

After a run you should see a new contact in HubSpot and an associated deal in the default pipeline at the appointment-scheduled stage.

## Canonical IDs used

| Service | Canonical ID |
|---------|--------------|
| HubSpot | `crm.v3.contacts.create` |
| HubSpot | `crm.v3.deals.create` |

## Part of the Swytchcode demo collection

Runnable LangGraph + Swytchcode examples:

- [Weekly-Reporting-Langgraph](https://github.com/swytchcodehq/Weekly-Reporting-Langgraph)
- [Customer-Onboarding-Langgraph](https://github.com/swytchcodehq/Customer-Onboarding-Langgraph)
- [Create-And-Send-Payment-Langgraph](https://github.com/swytchcodehq/Create-And-Send-Payment-Langgraph)
- [Bug-Escalation-Langgraph](https://github.com/swytchcodehq/Bug-Escalation-Langgraph)

## License

MIT. See [LICENSE](LICENSE).
