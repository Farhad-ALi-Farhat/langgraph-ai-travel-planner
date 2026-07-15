from langchain_core.tools import tool
from config import tavily

@tool
def search_web(query: str):
    """Search the internet for travel information."""
    result = tavily.search(
        query=query,
        max_results=5
    )

    return result
