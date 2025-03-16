from datetime import datetime
import json
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import logging

from logger import Logger


class complaint_summarization_chain_class:
    def __init__(self):
        self.logger_obj                                  = Logger() 
        
    def get_summarization_chain(self,llm):
        logging.info("Generating the complaint summarization chain.")
        print("Generating the complaint summarization chain.")
        
        system = """
                        You are an expert in **Consumer Financial Protection Bureau (CFPB) complaints**. Your task is to analyze the consumer complaint and extract a **clear, structured summary** for regulatory classification.
                        
                        ### **Instructions:**
                        1️   **Understand the core issue** the customer is facing.  
                        2️   **Identify key financial institutions, dates, and any regulatory violations** mentioned.  
                        3️   **Break down the complaint into a structured summary** including:
                           - **Nature of the issue** (e.g., account closure, loan denial, discrimination, etc.).
                           - **Customer's key concerns** (e.g., lack of transparency, unfair treatment, hidden fees).
                           - **Relevant financial institution** (e.g., bank name, lender).
                           - **Any regulatory implications** (mentioning discrimination, unfair practices, etc.).
                        4️   **Ensure that the summary is concise yet captures the essence of the complaint**.
                        5    ** Do not miss any numerical or money related detail in the summary**
                        
                        ### **Example Output:**
                        **Complaint Summary:**
                        - Customer alleges **account closure without explanation**.
                        - Bank: **JPMorgan Chase**.
                        - Issue: **Discrimination suspected based on past history**.
                        - Customer seeks **clarification and reinstatement of account**.
                        - Possible Regulation: **Regulation AA (Unfair or Deceptive Acts or Practices - UDAP)**.
                """
       
        complaint_summary_prompt = ChatPromptTemplate.from_messages(
                                                                        [
                                                                            ("system", system),
                                                                            (
                                                                                "human",
                                                                                "Here is the complaint:\n\n{complaint}\n\nSummarize the complaint while following the structured format.",
                                                                            ),
                                                                        ]
                                                                    )

        complaint_rewriter = complaint_summary_prompt | llm | StrOutputParser()
        logging.info("Completed generating the complaint summarization chain.")
        print("Completed generating the complaint summarization chain.")
        return complaint_rewriter
    
# if __name__ == "__main__":
#     llm_model         = 'llama3-70b-8192'
    
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     load_dotenv() 
#     TAVILY_API_KEY                          = os.getenv("TAVILY_API_KEY")
#     GROQ_API_KEY                            = os.getenv("GROQ_API_KEY")
#     HUGGINGFACE_API_KEY                     = os.getenv("HUGGINGFACE_API_KEY")
#     llm = ChatGroq(model_name = llm_model, temperature = 0.0, api_key = GROQ_API_KEY)
    
#     complaint = "I am an XXXX XXXXXXXX XXXX XXXX I have {$520000.00} in my Chase checking account. I was the victim of an XXXX XXXX scam which was detected on XX/XX/XXXX. The scam was reported to XXXX XXXXXXXX XXXX XXXX XXXX  Police and is being actively investigated by the FBI ( contact details can be provided upon request ). Since XX/XX/XXXX I have been trying to have the Chase checking funds returned to me. I have on numerous occasions visited the branch, phoned, etc ( details can be provided upon request ). I need these funds for living expenses and investment purposes. I am extremely distraught by Chase 's horrible treatment. Not only were they negligent in not noting the obvious signs of the scam, but they are adding insult to injury by not returning the money I have with them."
    
#     complaint_summarization_chain_class_obj = complaint_summarization_chain_class()
#     complaint_rewriter = complaint_summarization_chain_class_obj.get_summarization_chain(llm)
#     summarized_complaint = complaint_rewriter.invoke({"complaint": complaint})
#     print(summarized_complaint)

    
    
    
    