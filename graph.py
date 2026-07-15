from langgraph.graph import StateGraph, END

from models.state import TravelState

from nodes.extractor import extract_state
from nodes.planner import query_planner
from nodes.retrieval import retrieve_information
from nodes.context import context_builder
from nodes.retrieval import retrieve_destination_costs
from nodes.retrieval import extract_destination_costs
from nodes.retrieval import enrich_candidates
from nodes.selector import destination_selector
from nodes.decision import decision_engine
from nodes.itinerary import itinerary_builder

graph = StateGraph(TravelState)

graph.add_node("extract_state", extract_state)
graph.add_node("query_planner", query_planner)
graph.add_node("retrieve_information", retrieve_information)

graph.set_entry_point("extract_state")

graph.add_edge("extract_state", "query_planner")
graph.add_edge("query_planner", "retrieve_information")

graph.add_node("context_builder", context_builder)
graph.add_edge("retrieve_information", "context_builder")

graph.add_node("retrieve_destination_costs", retrieve_destination_costs)

graph.add_edge("context_builder", "retrieve_destination_costs")
graph.add_node("destination_selector", destination_selector)

graph.add_node("extract_destination_costs", extract_destination_costs)
graph.add_node("enrich_candidates", enrich_candidates)

graph.add_edge("retrieve_destination_costs", "extract_destination_costs")
graph.add_edge("extract_destination_costs", "enrich_candidates")
graph.add_edge("enrich_candidates", "destination_selector")

graph.add_node("decision_engine", decision_engine)
graph.add_edge("destination_selector", "decision_engine")

graph.add_node("itinerary_builder", itinerary_builder)
graph.add_edge("decision_engine", "itinerary_builder")
graph.add_edge("itinerary_builder", END)

app = graph.compile()