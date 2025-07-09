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


        with st.sidebar:
            llm_options=self.config.get_llm_options()
            use_cases=self.config.get_usecase_options()
            

            self.user_control["selected_llm"]=st.selectbox("Select LLM", llm_options)
            
            if self.user_control["selected_llm"]=="Groq":
                model_options=self.config.get_groq_model_options()
                self.user_control["selected_groq_model"]=st.selectbox("Select model",model_options )
                self.user_control["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API key", type="password")

                if not self.user_control["GROQ_API_KEY"]:
                    st.warning("Please Enter you groq api key to proceed")

            self.user_control["usecase_options"]=st.selectbox("Select Usecases",use_cases)

        return self.user_control


