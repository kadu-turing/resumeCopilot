from langchain import LLMChain
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate

recruiter_prompt = """
You are a recruiter to evaluate candidate's resume and question the candidates, 
for the optionally provided job.
"""

summary_prompt = """
Summarize, in a few concise bullet points, why this resume is a good or bad match for the above job description
"""

# gpt-4
# gpt-3.5-turbo

class Chatbot:
    def __init__(self, model_name="gpt-4", temperature=0, verbose=False):
        llm = ChatOpenAI(model_name=model_name, temperature=temperature, verbose=verbose)
        # initial message or instruction given to the model to set the context, role, or goal for the conversation
        system_message = SystemMessage(content=recruiter_prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{human_jd_input}: {jd_data} \n======\n {human_resume_input}: {resume_data}")
        self.chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message_prompt])
        self.chatgpt_chain = LLMChain(llm=llm, verbose=verbose, prompt=self.chat_prompt)
        self.resume_data = None
        self.jd_data = None


    def summarize_resume(self, resume_path, jd_path = None):
        resume_loader = UnstructuredPDFLoader(resume_path)
        self.resume_data = resume_loader.load()[0].page_content
        print("Completed reading resume.")

        if jd_path:
            jd_loader = UnstructuredPDFLoader(jd_path)
            self.jd_data = jd_loader.load()[0].page_content
        else:
            self.jd_data = "no job description provided, please ignore the job description and focus on the below resume."

        resume_summary = self.chatgpt_chain.predict(
            human_resume_input = summary_prompt, 
            resume_data = self.resume_data,
            human_jd_input= "Here is a job description",
            jd_data = self.jd_data)
        print("Completed reading job description.")
        return resume_summary
    
    
    def answer(self, question):
        result = self.chatgpt_chain.predict(
            human_resume_input = question, 
            resume_data = self.resume_data,
            human_jd_input= "Here is a job description",
            jd_data = self.jd_data)

        return result
