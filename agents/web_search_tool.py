from langchain_community.tools.tavily_search import TavilySearchResults

def get_medical_web_search_tool():
    return TavilySearchResults(max_results=3)
