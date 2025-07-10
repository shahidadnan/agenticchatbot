from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """Return the list of the tools to be used in chatbot"""
    tools=[TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """Creates the ToolNode for the graph"""

    return ToolNode(tools=tools)

