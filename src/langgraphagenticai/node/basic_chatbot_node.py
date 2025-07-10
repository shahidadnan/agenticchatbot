from src.langgraphagenticai.state.state import State


class BasicChatbotNode:

    """This is basic chatbot implementation"""

    def __init__(self,model):
        self.llm=model

    def process(self,state:State)->dict:

        return {"messages": self.llm.invoke(state["messages"])}
    

    