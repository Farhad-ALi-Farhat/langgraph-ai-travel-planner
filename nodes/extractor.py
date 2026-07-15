from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from models.state import TravelState
from utils.json_utils import safe_json

def extract_state(state: TravelState):

    user_query = state["messages"][-1].content

    response = llm.invoke([
        SystemMessage(content="""
You are an information extraction system.

Your ONLY job is to extract travel information explicitly mentioned by the user.

Never infer.
Never guess.
Never assume.

If a value is not explicitly present, return null.

Return ONLY valid JSON in exactly this format:

{
  "destination": null,
  "budget": null,
  "days": null,
  "trip_type": null,
  "transport_preference": null,
  "num_people": null
}

Rules:
- Do not add explanations.
- Do not wrap JSON in markdown.
- Budget must be an integer (e.g. 100000).
- Convert "100k" to 100000.
- Days must be an integer.
- Extract only what the user explicitly states.

Examples:

User:
Suggest a mountain trip under 100k.

Output:
{
  "destination": null,
  "budget": 100000,
  "days": null,
  "trip_type": "mountain",
  "transport_preference": null,
  "num_people": null
}

User:
Plan a 5 day Hunza trip for 2 people by car.

Output:
{
  "destination": "Hunza",
  "budget": null,
  "days": 5,
  "trip_type": null,
  "transport_preference": "car",
  "num_people": 2
}
"""),

        HumanMessage(content=user_query)
    ])

    data = safe_json(response.content)

    defaults = {
        "destination": None,
        "budget": None,
        "days": None,
        "trip_type": None,
        "transport_preference": None,
        "num_people": None,
    }

    defaults.update(data)
    data = defaults

    # Ensure every expected field exists
    expected_fields = [
        "destination",
        "budget",
        "days",
        "trip_type",
        "transport_preference",
        "num_people"
    ]

    for field in expected_fields:
        data.setdefault(field, None)

    data["missing_fields"] = [
        field for field in expected_fields
        if data[field] is None
    ]

    return data