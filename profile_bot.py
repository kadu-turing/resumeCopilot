from langchain import LLMChain
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate

recruiter_prompt = "You are a chatbot helping a recruiter to evaluate candidate's resume and question the candidates."

class Chatbot:
    def __init__(self, model_name='gpt-3.5-turbo', temperature=0, verbose=False):
        llm = ChatOpenAI(model_name=model_name, temperature=temperature, verbose=verbose)
        # initial message or instruction given to the model to set the context, role, or goal for the conversation
        system_message = SystemMessage(content=recruiter_prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template('{human_input}: {resume_data}')
        self.chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message_prompt])
        self.chatgpt_chain = LLMChain(llm=llm, verbose=verbose, prompt=self.chat_prompt)
        self.resume_data = None


    def summarize_resume(self, resume_path):
        resume_loader = UnstructuredPDFLoader(resume_path)
        print("Completed reading resume.")
        self.resume_data = resume_loader.load()[0].page_content
        resume_summary = self.chatgpt_chain.predict(
            human_input='Summarize this resume in a few concise bullet points, and focus on skills and experience.', 
            resume_data=self.resume_data)
        return resume_summary
    
    
    def answer(self, question):
        return self.chatgpt_chain.predict(human_input=question, resume_data=self.resume_data)
