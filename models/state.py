from typing import Annotated, List, Optional, TypedDict

from langgraph.graph.message import add_messages


class TravelState(TypedDict):
    # Messages
    messages: Annotated[list, add_messages]

    # User input
    destination: Optional[str]
    days: Optional[int]
    budget: Optional[int]
    trip_type: Optional[str]
    transport: Optional[str]
    people: Optional[int]

    # Validation
    missing_fields: List[str]

    # Resolved values
    resolved_destination: Optional[str]
    resolved_budget: Optional[int]
    resolved_weather: Optional[str]

    # Tool outputs
    web_results: Optional[str]
    cost_results: Optional[str]
    destination_results: Optional[str]
    destination_costs: Optional[List[dict]]
    transport_results: Optional[dict[str, object]]
    weather_results: Optional[str]

    # Planning
    candidate_destinations: Optional[List[str]]
    estimated_costs: Optional[List[str]]
    transport_options: Optional[List[str]]
    budget_summary: Optional[dict[str, object]]
    retrieval_context: Optional[str]
    structured_destination_costs: Optional[List[dict]]
    selected_destinations: Optional[List[str]]

    # Flags
    need_destination: bool
    need_weather: bool
    need_costs: bool
    need_transport: bool

    # Final recommendation
    chosen_destination: Optional[str]
    reason: Optional[str]
    estimated_cost: Optional[str]
    recommended_transport: Optional[str]
    itinerary: Optional[str]