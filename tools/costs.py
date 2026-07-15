from langchain_core.tools import tool
from config import tavily

@tool
def estimate_travel_cost(query: str):
    """Find travel cost information."""
    result = tavily.search(
        query=f"travel cost {query} Pakistan budget hotels transport",
        max_results=5
    )
    return result