import streamlit as st
from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitui.display_result import DispalyResultStreamlit


def load_langgrapg_agenticai_app():
    
    ui= LoadStreamUI()
    userInput=ui.Load_streamlit_ui()

    if not userInput:
        st.error("ERROR failed to load user input from UI")
        return 
    if st.session_state.IsFetchButtonClicked:
        user_message=st.session_state.timeframe
    else:
        user_message= st.chat_input("enter your message")

    if user_message:
        try:
    
            obj_llm_config= GroqLLM(user_controls_input=userInput)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model failed to intitalized")
                return
            
            usecase=userInput.get("usecase_options")
            if not usecase:
                st.error("Error: Please select the usecase")
            
            
            graph_builder = GraphBuilder(model=model)
            try: 
                graph = graph_builder.setup_graph(usecase)
                if graph:
                    DispalyResultStreamlit(usecase=usecase, graph=graph, user_message=user_message).display_result_on_ui()
                else:
                    st.error("Error: Failed to build graph")
                    
            except Exception as e:
                st.error(f"Error:Graph setup failed - {e}")
                return

        except Exception as e:
            st.error(f"Error:Graph setup not failed - {e}")
            return