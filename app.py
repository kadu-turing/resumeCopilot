import os

import streamlit as st
from streamlit_chat import message
import test_app

from profile_bot import Chatbot

# Initialize the Chatbot
chat_bot = Chatbot()

# Auth
st.sidebar.image("Img/robot_reading_resume.png")
api_key = st.sidebar.text_input("`Please provide an OpenAI API Key if you have a large PDF file:`", type="password")
st.sidebar.write("`By:` [Kai](mailto:{})".format("kai.du@turing.com"))

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# App  
st.header("`Resume Copilot`")
st.info("`Hey there! I'm an assistant for recruiter.`")

uploaded_jd = st.file_uploader("`(Optional) Upload job description PDF file:` ", type = ['pdf'] , accept_multiple_files=False)
uploaded_resume = st.file_uploader("`Upload resume PDF file:` ", type = ['pdf'] , accept_multiple_files=False)

if uploaded_resume and os.environ.get("OPENAI_API_KEY"):
    # Summarize the resume and print the result
    if uploaded_jd:
        resume_summary = chat_bot.summarize_resume(uploaded_resume, uploaded_jd)
        question_prompt = "Ask several interview questions based on the given resume and job description"
    else: 
        resume_summary = chat_bot.summarize_resume(uploaded_resume)
        question_prompt = "Ask several interview questions based on the given resume"
    st.info(resume_summary)


    # Prompt the user for a question
    query = st.text_input("`Create some interview questions:` ", question_prompt)
    answer = chat_bot.answer(query)
    st.info(answer)

else:
    st.info("`Please upload a resume PDF file.`")
