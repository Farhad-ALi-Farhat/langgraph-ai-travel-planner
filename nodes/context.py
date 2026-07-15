import json

from langchain_core.messages import HumanMessage

from config import llm
from models.state import TravelState
from utils.json_utils import safe_json

def context_builder(state: TravelState):

    destination_results = state.get("destination_results", "{}")

    cost_results =  state.get("cost_results", "{}")

    transport_results = state.get("transport_results", "{}")

    prompt = f"""
You are building context for a travel planning AI.

The user requested:

Destination:
{state.get("destination")}

Budget:
{state.get("budget")}

Days:
{state.get("days")}

Trip Type:
{state.get("trip_type")}

People:
{state.get("num_people")}

--------------------------------------------------

Retrieved Destination Information

{destination_results}

--------------------------------------------------

Retrieved Transport Information

{transport_results}

--------------------------------------------------

Your task:

Analyze the retrieved information.

Return ONLY valid JSON.

{{
    "candidate_destinations":[
        {{
            "name":"",
            "why_recommended":"",
            "best_for":""
        }}
    ],

    "transport_options":[
    ],

    "retrieval_context":""
}}

Rules:

- Extract ONLY destinations that actually appear in the retrieved information.
- Do NOT invent new destinations.
- Return at least 3 destinations whenever possible.
- For each destination include:
    - name
    - why_recommended
    - best_for
- Summarize available transport options.
- Do NOT estimate prices.
- Do NOT include:
    - estimated_budget
    - budget_category
    - budget_fit
    - budget_summary
- Do NOT create an itinerary.
- Return ONLY JSON.
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    context = safe_json(response.content)
    return context
