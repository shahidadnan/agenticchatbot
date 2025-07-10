from langgraph.graph import StateGraph,END, START
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.node.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphagenticai.node.chatbot_with_tool_node import chatbotWithToolNode



class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):

        self.basic_chatbot_node=BasicChatbotNode(self.llm)

        #node
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tool_graph(self):
        """This method builds a advance chatbot graph with tool integration"""
        ## define tool and tool node
        tools=get_tools()
        tool_node=create_tool_node(tools)

        ## Define the llm
        llm= self.llm

        ## Define the chatbot node
        obj_chatbot_with_tool_node = chatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_tool_node.chatbot_with_tool(tools=tools)

        #node
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition )
        self.graph_builder.add_edge("tools","chatbot")


    
    def setup_graph(self, usecase:str):

        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Tool":
            self.chatbot_with_tool_graph()

        return self.graph_builder.compile()

