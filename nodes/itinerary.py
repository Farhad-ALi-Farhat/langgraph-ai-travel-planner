from config import llm
from models.state import TravelState

def itinerary_builder(state: TravelState):

    prompt = f"""
You are a professional travel planner.

The destination has ALREADY been selected.

Destination:
{state["chosen_destination"]}

This destination is FINAL.

You MUST generate an itinerary ONLY for this destination.

Do NOT mention any other destination.

Do NOT include attractions from any other city or valley.

If you mention another destination, your answer is incorrect.

--------------------------------------------------
FINAL TRIP DECISION
--------------------------------------------------

Destination:
{state.get("chosen_destination")}

Reason:
{state.get("reason")}

Estimated Cost:
{state.get("estimated_cost")}

Recommended Transport:
{state.get("recommended_transport")}

--------------------------------------------------
USER REQUIREMENTS
--------------------------------------------------

Budget:
{state.get("budget")}

Days:
{state.get("days") or 4}

Trip Type:
{state.get("trip_type")}

People:
{state.get("num_people") or 1}

--------------------------------------------------
OPTIONAL CONTEXT
--------------------------------------------------

Weather:
{state.get("weather")}

--------------------------------------------------

Every activity must take place in:

{state["chosen_destination"]}

Do not visit any place outside this destination.

Generate:

# Day-wise Itinerary

Day 1
...

Day 2
...

Day 3
...

Day 4
...

# Budget Breakdown

Use the estimated trip cost and divide it into:
- Transport
- Accommodation
- Food
- Activities
- Miscellaneous

# Transport Plan

If the user's starting city is unknown, provide a generic transport plan from a major Pakistani city.

# Travel Tips

Provide 3-5 useful tips relevant to the destination.

Return clean markdown only.
"""

    response = llm.invoke(prompt)

    return {
    **state,
    "messages": state["messages"] + [response],
    "itinerary": response.content
    }
