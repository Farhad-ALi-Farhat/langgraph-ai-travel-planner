import json

from config import llm
from models.state import TravelState
from utils.json_utils import safe_json

def decision_engine(state: TravelState):
    selected = state.get("selected_destinations", [])
    print("Decision Engine Input")
    print(json.dumps(selected, indent=2))

    selected_text = ""

    for i, d in enumerate(selected, start=1):
        selected_text += f"""
    Option {i}
    Destination: {d['name']}
    Reason: {d['reason']}
    Estimated Budget:
    {d.get("estimated_budget", "Not Available")}

    """

    prompt = f"""
You are an expert travel planner.

Your ONLY job is to choose the best destination from the shortlisted destinations.

DO NOT invent new destinations.

If none of the shortlisted destinations satisfy the user's requirements,
choose the closest match.

Never create a new destination.

--------------------------------------------------
USER REQUIREMENTS
--------------------------------------------------

Budget:
{state.get("budget")}

Trip Type:
{state.get("trip_type")}

Days:
{state.get("days")}

Transport Preference:
{state.get("transport_preference")}

--------------------------------------------------
SHORTLISTED DESTINATIONS
--------------------------------------------------

{selected_text}

--------------------------------------------------
AVAILABLE TRANSPORT
--------------------------------------------------

{chr(10).join(state.get("transport_options", []))}

--------------------------------------------------
BUDGET INFORMATION
--------------------------------------------------

{json.dumps(state.get("budget_summary", {}), indent=2)}

--------------------------------------------------

Tasks

1. Choose ONE destination ONLY from the shortlisted destinations.
2. Explain why it best satisfies the user's requirements.
3. If the user supplied a budget:

- estimate a trip cost that fits inside that budget.

Otherwise:

- use estimated_budget of the selected destination if available.

- If estimated_budget is unavailable,
  use budget_summary.

- If budget_summary contains only daily costs,
  estimate the total cost using the trip duration.
  If the duration is unknown, assume 4 days.

Never return:

- Unknown
- Not Available
- N/A

Always return an estimated PKR value.
4. Recommend the most suitable transport.
5. Do NOT invent destinations.
6. Return ONLY JSON.

{{
    "chosen_destination": "...",
    "reason": "...",
    "estimated_cost": "...",
    "recommended_transport": "..."
}}
"""
    response = llm.invoke(prompt)

    data = safe_json(response.content)

    return data
