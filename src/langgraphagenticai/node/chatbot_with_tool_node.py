from src.langgraphagenticai.state.state import State


class chatbotWithToolNode:

    def __init__(self, model):
        self.llm = model

    def chatbot_with_tool(self,tools):

        """Chatbot logic for processing the input state and return the chatbot response"""
    
        llm_with_tools=self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """Chatbot logic for processing the input state and returning a response"""

            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node