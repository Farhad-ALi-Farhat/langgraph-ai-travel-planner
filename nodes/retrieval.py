from models.state import TravelState

from tools.search import search_web
from tools.weather import get_weather
from tools.costs import estimate_travel_cost
from config import llm
from utils.json_utils import safe_json

def retrieve_information(state: TravelState):

    updates = {}

    # -------------------------
    # Destination Search
    # -------------------------

    if state.get("need_destination"):

        destination_results = search_web.invoke({
            "query": f"""
            Best {state.get('trip_type','travel')}
            destinations in Pakistan
            {'under ' + str(state.get('budget')) + ' PKR' if state.get('budget') else ''}
            """
        })

    else:

        destination_results = {
            "results": [
                {
                    "title": state["destination"],
                    "content": state["destination"]
                }
            ]
        }

    updates["destination_results"] = destination_results

    # -------------------------
    # Transport Search

    # -------------------------

    if state.get("need_transport"):

        updates["transport_results"] = search_web.invoke({
            "query": "Transportation options for northern Pakistan"
        })
    return updates

def retrieve_destination_costs(state: TravelState):

    destination_costs = []

    for destination in state.get("candidate_destinations", []):

        result = estimate_travel_cost.invoke({
            "query": f"""
            Estimated trip cost for {destination['name']} Pakistan.

            Include:

            - accommodation
            - transport
            - food
            - activities
            - total trip cost

            Assume a typical trip if the duration is unknown.
            """
        })

        destination_costs.append({
            "name": destination["name"],
            "cost_info": result
        })

    return {
        "destination_costs": destination_costs
    }

def enrich_candidates(state: TravelState):

    enriched = []

    for candidate in state.get("candidate_destinations", []):

        cost = next(
            (
                c
                for c in state.get("structured_destination_costs", [])
                if c["name"] == candidate["name"]
            ),
            {}
        )

        enriched.append({
            **candidate,
            **cost
        })

    return {
        "candidate_destinations": enriched
    }

def extract_destination_costs(state: TravelState):

    structured_costs = []

    for destination in state.get("destination_costs", []):

        prompt = f"""
You are extracting travel cost information.

Destination:
{destination["name"]}

Retrieved Cost Information:

{destination["cost_info"]}

Return ONLY valid JSON.

{{
    "name": "{destination["name"]}",
    "estimated_budget": "",
    "daily_cost": "",
    "transport_cost": "",
    "accommodation_cost": "",
    "food_cost": "",
    "activities_cost": "",
    "budget_category": ""
}}

Rules:

- Use ONLY the retrieved information.
- If a value is unavailable, return an empty string.
- Do NOT invent prices.
"""

        response = llm.invoke(prompt)

        structured_costs.append(safe_json(response.content))

    return {
        "structured_destination_costs": structured_costs
    }
