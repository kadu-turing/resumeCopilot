import os

import streamlit as st
from streamlit_chat import message

from profile_bot import Chatbot


# Auth
st.sidebar.image("Img/robot_reading_resume.png")
api_key = st.sidebar.text_input("`Please provide an OpenAI API Key if you have a large PDF file:`", type="password")
st.sidebar.write("`By:` [Kai](mailto:{})".format("kai.du@turing.com"))

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# App 
st.header("`Resume Copilot`")
st.info("`Hey there! I'm an assistant for recruiter.`")
uploaded_resume = st.file_uploader("`Upload resume PDF file:` ", type = ['pdf'] , accept_multiple_files=False)

# Initialize the Chatbot
chat_bot = Chatbot()

# keep chat history
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []

if uploaded_resume and os.environ["OPENAI_API_KEY"]:
    # Summarize the resume and print the result
    resume_summary = chat_bot.summarize_resume(uploaded_resume)
    st.info(resume_summary)

    # Print instructions for chat mode and available commands
    st.info("Entering interview mode.")
    
     # Prompt the user for a question
    query = st.text_input("`Ask interview questions about the resume:` ","Ask 10 interview questions about skills and experience based on the given resume.")
    answer = chat_bot.answer(query)
        
    st.session_state["past"].append(query)
    st.session_state["generated"].append(answer)

    if st.session_state["past"]:
        for i in range(len(st.session_state["past"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i) + "_answer")
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
else:
    st.info("`Please upload a resume PDF file.`")
