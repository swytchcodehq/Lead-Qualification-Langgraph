from swytchcode_runtime import exec as swytchcode_exec
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()


class LeadQualificationState(TypedDict):
    lead_name: str
    lead_email: str
    company: str
    phone: Optional[str]
    deal_value: int
    hubspot_contact_id: Optional[str]
    hubspot_deal_id: Optional[str]


# ── Node 1: Create HubSpot contact ───────────────────────────────────────────

def create_hubspot_contact(state: LeadQualificationState) -> dict:
    print(f"[1/2] Creating HubSpot contact for {state['lead_email']}...")
    name_parts = state["lead_name"].split()
    result = swytchcode_exec("crm.v3.contacts.create", {
        "body": {
            "properties": {
                "email":          state["lead_email"],
                "firstname":      name_parts[0],
                "lastname":       name_parts[-1] if len(name_parts) > 1 else "",
                "company":        state["company"],
                "phone":          state.get("phone", ""),
                "hs_lead_status": "NEW",
            }
        },
        "Authorization": f"Bearer {os.environ['HUBSPOT_API_KEY']}",
    })
    contact_id = (result or {}).get("data", {}).get("id")
    print(f"    ✔ HubSpot contact created: {contact_id}")
    return {"hubspot_contact_id": contact_id}


# ── Node 2: Create HubSpot deal ──────────────────────────────────────────────

def create_hubspot_deal(state: LeadQualificationState) -> dict:
    print(f"[2/2] Creating HubSpot sales opportunity for {state['company']}...")
    close_date = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
    result = swytchcode_exec("crm.v3.deals.create", {
        "body": {
            "properties": {
                "dealname":  f"{state['company']} — Inbound Lead",
                "dealstage": "appointmentscheduled",
                "pipeline":  "default",
                "amount":    str(state["deal_value"]),
                "closedate": close_date,
            },
            "associations": [
                {
                    "to":    {"id": state["hubspot_contact_id"]},
                    "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}],
                }
            ],
        },
        "Authorization": f"Bearer {os.environ['HUBSPOT_API_KEY']}",
    })
    deal_id = (result or {}).get("data", {}).get("id")
    print(f"    ✔ HubSpot deal created: {deal_id}")
    return {"hubspot_deal_id": deal_id}


# ── Build graph ───────────────────────────────────────────────────────────────

workflow = StateGraph(LeadQualificationState)
workflow.add_node("create_contact", create_hubspot_contact)
workflow.add_node("create_deal",    create_hubspot_deal)

workflow.set_entry_point("create_contact")
workflow.add_edge("create_contact", "create_deal")
workflow.add_edge("create_deal",    END)

app = workflow.compile()


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = app.invoke({
        "lead_name":          "Alex Johnson",
        "lead_email":         "alex@techcorp.io",
        "company":            "TechCorp",
        "phone":              "+1-415-555-0192",
        "deal_value":         5000,
        "hubspot_contact_id": None,
        "hubspot_deal_id":    None,
    })

    print("\n✅ Lead qualified!")
    print(f"   HubSpot Contact ID: {result['hubspot_contact_id']}")
    print(f"   HubSpot Deal ID:    {result['hubspot_deal_id']}")

