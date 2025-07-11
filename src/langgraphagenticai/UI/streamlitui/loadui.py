import streamlit as st
import os
from src.langgraphagenticai.UI.uiconfigfile import Config


class LoadStreamUI:

    def __init__(self):
        self.config=Config()
        self.user_control={}

    def Load_streamlit_ui(self):
        st.set_page_config(page_title="X"+ self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe=''
        st.session_state.IsFetchButtonClicked = False


        with st.sidebar:
            llm_options=self.config.get_llm_options()
            use_cases=self.config.get_usecase_options()
            

            self.user_control["selected_llm"]=st.selectbox("Select LLM", llm_options)
            
            if self.user_control["selected_llm"]=="Groq":
                model_options=self.config.get_groq_model_options()
                self.user_control["selected_groq_model"]=st.selectbox("Select model",model_options )
                self.user_control["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("GROQ API key", type="password")

                if not self.user_control["GROQ_API_KEY"]:
                    st.warning("Please Enter you groq api key to proceed")

            self.user_control["usecase_options"]=st.selectbox("Select Usecases",use_cases)
            
            if  self.user_control["usecase_options"]=="Chatbot with Tool":
                os.environ["Tavily_API_Key"]=self.user_control["Tavily_API_Key"]=st.session_state["Tavily_API_KEY"]=st.text_input("TAVILY API key", type="password")
                
                if not self.user_control["Tavily_API_Key"]:
                    st.warning("Please Enter you Tavily api key to proceed")

            if self.user_control["usecase_options"]=="AI News":
                os.environ["Tavily_API_Key"]=self.user_control["Tavily_API_Key"]=st.session_state["Tavily_API_KEY"]=st.text_input("TAVILY API key", type="password")
                
                if not self.user_control["Tavily_API_Key"]:
                    st.warning("Please Enter you Tavily api key to proceed")

                st.subheader("AI News Explorer")
                time_frame=st.selectbox("Select Time Frame", ["Daily", "Weekly", "Monthly"])
                if st.button("Fetch Latest AI news", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe=time_frame

        return self.user_control


