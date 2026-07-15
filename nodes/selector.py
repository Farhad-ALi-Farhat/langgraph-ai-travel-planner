import json

from config import llm
from models.state import TravelState
from utils.json_utils import safe_json

def destination_selector(state: TravelState):

    candidates = state.get("candidate_destinations", [])

    prompt = f"""
You are an expert Pakistani travel planner.

The user requested:

Budget: {state.get("budget")}
Trip Type: {state.get("trip_type")}
Days: {state.get("days")}

--------------------------------------------------
CANDIDATE DESTINATIONS
--------------------------------------------------

{json.dumps(candidates, indent=2)}

--------------------------------------------------

Your job is NOT to create an itinerary.

Choose the best destination(s).

Rules:

- NEVER return an empty list.
- Always choose at least one destination.
- Use BOTH:
    • why_recommended
    • cost_info
  when making your decision.
- Compare each destination's retrieved cost against the user's budget.
- Prefer destinations that fit the budget.
- If none fit, choose the closest affordable option.
- Preserve the retrieved cost exactly as the estimated_budget.
- Do NOT invent prices.
- Return ONLY JSON.

Example:

{{
    "selected_destinations":[
        {{
            "name":"Hunza",
            "reason":"Best mountain destination within the user's budget.",
            "estimated_budget":"PKR 70,000 - 90,000"
        }},
        {{
            "name":"Skardu",
            "reason":"Excellent alternative with more adventure activities.",
            "estimated_budget":"PKR 95,000 - 120,000"
        }}
    ]
}}
"""

    response = llm.invoke(prompt)

    data = safe_json(response.content)

    print("Destination Selector Output")
    print(json.dumps(data, indent=2))

    return data
