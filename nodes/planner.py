from models.state import TravelState

def query_planner(state: TravelState):

    need_destination = state.get("destination") is None
    need_transport = state.get("transport_preference") is None

    # Weather can only be fetched after a destination exists
    need_weather = not need_destination

    # If destination is unknown, we also need to research costs
    need_costs = state.get("budget") is None or need_destination

    return {
        "need_destination": need_destination,
        "need_weather": need_weather,
        "need_costs": need_costs,
        "need_transport": need_transport,
    }