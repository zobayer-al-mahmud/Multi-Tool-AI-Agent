from langchain_community.tools.tavily_search import TavilySearchResults


def get_medical_web_search_tool():
    return TavilySearchResults(max_results=3)


def run_medical_web_search(question: str) -> str:
    """Thin wrapper so OpenAI Assistant can call Tavily via a tool."""
    tool = get_medical_web_search_tool()
    return tool.run(question)
