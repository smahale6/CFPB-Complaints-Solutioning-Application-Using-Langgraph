from logger import Logger
import os
import logging
from pydantic import BaseModel, Field
import warnings
warnings.filterwarnings('ignore')

from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.tools.tavily_search import TavilySearchResults



class complaint_clasification_class:
    def __init__(self):
        self.logger_obj                 = Logger()
        
    def get_doc_classification_chain(self, reg_name, retriever_tool, llm):
        logging.info(f"Generating complaint classification chain for {reg_name}.")
        print(f"Generating complaint classification chain for {reg_name}.")
    
        class Reg_Classification(BaseModel):
            """Structured output for complaint classification."""
            Answer: str      = Field(description="Answer must be 'Yes' or 'No'")
            Explanation: str = Field(description="Short explanation (max 4 sentences)")
    
        # LLM with structured function call
        structured_llm_grader = llm.with_structured_output(Reg_Classification)
    
        system_prompt = """
                            You are an expert in CFPB regulations. Given data is the context of **{regulation_name}**.
                            
                            ### **Instructions:**
                            - Analyze the complaint and determine if it falls under **{regulation_name}**. 
                            - **Answer with 'Yes' or 'No'**. Get this classification of Yes or No from the context.
                            - Provide an **explanation in 4 sentences or fewer**. The explanation should come from the context retrived.
                            
                            ### **Context (Extracted {regulation_name} Documents):**
                            {{context}}
                            
                            ### **Consumer Complaint:**
                            "{{complaint}}"
                        """



    
        # Mapping for all regulations
        regulation_mapping = {
                                "Reg_AA": "Regulation AA (Unfair or Deceptive Acts or Practices)",
                                "Reg_B" : "Regulation B (Equal Credit Opportunity Act - ECOA)",
                                "Reg_C" : "Regulation C (Home Mortgage Disclosure Act - HMDA)",
                                "Reg_D" : "Regulation D (Alternative Mortgage Transaction Parity Act)",
                                "Reg_E" : "Regulation E (Electronic Fund Transfer Act - EFTA)",
                                "Reg_F" : "Regulation F (Fair Debt Collection Practices Act - FDCPA)",
                                "Reg_G" : "Regulation G (S.A.F.E. Mortgage Licensing Act – Federal Registration)",
                                "Reg_H" : "Regulation H (S.A.F.E. Mortgage Licensing Act – State Compliance)",
                                "Reg_I" : "Regulation I (Disclosure Requirements for Depository Institutions Lacking Federal Deposit Insurance)",
                                "Reg_J" : "Regulation J (Land Sales Registration)",
                                "Reg_K" : "Regulation K (Purchasers’ Revocation Rights, Sales Practices and Standards)",
                                "Reg_L" : "Regulation L (Protection of Nonpublic Personal Information)",
                                "Reg_M" : "Regulation M (Consumer Leasing)",
                                "Reg_N" : "Regulation N (Mortgage Acts and Practices – Advertising Rule)",
                                "Reg_O" : "Regulation O (Mortgage Assistance Relief Services - MARS Rule)",
                                "Reg_P" : "Regulation P (Privacy of Consumer Financial Information)",
                                "Reg_V" : "Regulation V (Fair Credit Reporting - FCRA)",
                                "Reg_X" : "Regulation X (Real Estate Settlement Procedures Act - RESPA)",
                                "Reg_Z" : "Regulation Z (Truth in Lending Act - TILA)",
                                "Reg_CC": "Regulation CC (Availability of Funds and Collection of Checks)",
                                "Reg_DD": "Regulation DD (Truth in Savings Act - TISA)"
                            }
    
        if reg_name not in regulation_mapping:
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate classification chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate classification chain.")
            return None
    
        # Format system prompt with the correct regulation name
        system = system_prompt.format(regulation_name=regulation_mapping[reg_name])
    
        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")
    
        # Create classification prompt
        classification_prompt = ChatPromptTemplate.from_messages([
                                                                    ("system", system),
                                                                    ("human", "Analyze the complaint and return a structured response."),
                                                                ])
    
        # Build the full classification chain
        classification_chain = (
                                    {"context": retriever_tool, "complaint": RunnablePassthrough()}
                                    | classification_prompt
                                    | structured_llm_grader
                                )
    
        logging.info(f"Classification chain successfully generated for {reg_name}.")
        print(f"Classification chain successfully generated for {reg_name}.")
        
        return classification_chain

    def get_tavily_search_tool(self, TAVILY_API_KEY, total_tavily_searches = 3, ):
        logging.info("Creating Tavily Tool.")
        print("Creating Tavily Tool.")
        tavily_search_tool = Tool(
                                    name="web_search_tool",
                                    description="Searches the web for information related to a given complaint and retrieves top 3 results.",
                                    func=lambda query: TavilySearchResults(api_key=TAVILY_API_KEY).invoke(query)[:total_tavily_searches]  # Fetch top 3 search results
                                 )
        logging.info("Created Tavily Tool.")
        print("Created Tavily Tool.")
        
        return tavily_search_tool
        
    def get_web_classification_chain(self, reg_name, tavily_search_tool, llm):
        logging.info(f"Generating web-based complaint classification chain for {reg_name}.")
        print(f"Generating web-based complaint classification chain for {reg_name}.")
    
        class Web_Classification(BaseModel):
            """Structured output for web-based complaint classification."""
            Answer: str      = Field(description="Answer must be 'Yes' or 'No'")
            Explanation: str = Field(description="Short explanation (max 4 sentences)")
    
        # LLM with structured function call
        structured_web_llm = llm.with_structured_output(Web_Classification)
    
        system_prompt = """
                            You are an expert in CFPB regulations. You have access to **real-time web search results**.
                            Use the retrieved **web context** to determine if the given complaint falls under **{regulation_name}**.
    
                            ### **Instructions:**
                            - Analyze the complaint using **Web Context**.
                            - Ensure that the web context **has the latest version, draft, and rules of {regulation_name}**.
                            - **Answer with 'Yes' or 'No'**. Get the classification from the **web search results**.
                            - Provide an **explanation in 4 sentences or fewer**. The explanation should be based on the **retrieved web results**.
    
                            ### **Web Context (Search Results):**
                            {{context}}
    
                            ### **Consumer Complaint:**
                            "{{complaint}}"
                       """
    
        # Mapping for all regulations
        regulation_mapping = {
                                "Reg_AA": "Regulation AA (Unfair or Deceptive Acts or Practices)",
                                "Reg_B" : "Regulation B (Equal Credit Opportunity Act - ECOA)",
                                "Reg_C" : "Regulation C (Home Mortgage Disclosure Act - HMDA)",
                                "Reg_D" : "Regulation D (Alternative Mortgage Transaction Parity Act)",
                                "Reg_E" : "Regulation E (Electronic Fund Transfer Act - EFTA)",
                                "Reg_F" : "Regulation F (Fair Debt Collection Practices Act - FDCPA)",
                                "Reg_G" : "Regulation G (S.A.F.E. Mortgage Licensing Act – Federal Registration)",
                                "Reg_H" : "Regulation H (S.A.F.E. Mortgage Licensing Act – State Compliance)",
                                "Reg_I" : "Regulation I (Disclosure Requirements for Depository Institutions Lacking Federal Deposit Insurance)",
                                "Reg_J" : "Regulation J (Land Sales Registration)",
                                "Reg_K" : "Regulation K (Purchasers’ Revocation Rights, Sales Practices and Standards)",
                                "Reg_L" : "Regulation L (Protection of Nonpublic Personal Information)",
                                "Reg_M" : "Regulation M (Consumer Leasing)",
                                "Reg_N" : "Regulation N (Mortgage Acts and Practices – Advertising Rule)",
                                "Reg_O" : "Regulation O (Mortgage Assistance Relief Services - MARS Rule)",
                                "Reg_P" : "Regulation P (Privacy of Consumer Financial Information)",
                                "Reg_V" : "Regulation V (Fair Credit Reporting - FCRA)",
                                "Reg_X" : "Regulation X (Real Estate Settlement Procedures Act - RESPA)",
                                "Reg_Z" : "Regulation Z (Truth in Lending Act - TILA)",
                                "Reg_CC": "Regulation CC (Availability of Funds and Collection of Checks)",
                                "Reg_DD": "Regulation DD (Truth in Savings Act - TISA)"
                            }
    
        if reg_name not in regulation_mapping:
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate web classification chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate web classification chain.")
            return None
    
        # Format system prompt with the correct regulation name
        system = system_prompt.format(regulation_name=regulation_mapping[reg_name])
    
        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")
    
        # Create classification prompt
        web_classification_prompt = ChatPromptTemplate.from_messages([
                                                                        ("system", system),
                                                                        ("human", "Analyze the complaint using web context and return a structured response."),
                                                                    ])
    
        # Build the full web classification chain
        web_classification_chain = (
                                        {"context": tavily_search_tool, "complaint": RunnablePassthrough()}
                                        | web_classification_prompt
                                        | structured_web_llm
                                    )
    
        logging.info(f"Web classification chain successfully generated for {reg_name}.")
        print(f"Web classification chain successfully generated for {reg_name}.")
    
        return web_classification_chain

        


# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from complaint_summarization import complaint_summarization_chain_class
#     from document_grading import document_grading_class
    
#     llm_model                               = 'llama3-70b-8192'
#     cart_path                               = r'C:\GitHub Collections\CART 2.0\src'
#     regulations_path                        = cart_path + '\\regulations'
#     vector_db_path                          = cart_path + '\\vector_db\\'
#     reg_name                                = 'Reg_AA'

#     load_dotenv() 
#     TAVILY_API_KEY                          = os.getenv("TAVILY_API_KEY")
#     GROQ_API_KEY                            = os.getenv("GROQ_API_KEY")
#     HUGGINGFACE_API_KEY                     = os.getenv("HUGGINGFACE_API_KEY")
#     llm                                     = ChatGroq(model_name = llm_model, temperature = 0.0, api_key = GROQ_API_KEY)
#     embedding_function                      = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5",model_kwargs={"token": HUGGINGFACE_API_KEY})
#     complaint                               = "I am an XXXX XXXXXXXX XXXX XXXX I have {$520000.00} in my Chase checking account. I was the victim of an XXXX XXXX scam which was detected on XX/XX/XXXX. The scam was reported to XXXX XXXXXXXX XXXX XXXX XXXX  Police and is being actively investigated by the FBI ( contact details can be provided upon request ). Since XX/XX/XXXX I have been trying to have the Chase checking funds returned to me. I have on numerous occasions visited the branch, phoned, etc ( details can be provided upon request ). I need these funds for living expenses and investment purposes. I am extremely distraught by Chase 's horrible treatment. Not only were they negligent in not noting the obvious signs of the scam, but they are adding insult to injury by not returning the money I have with them."
    
#     complaint_summarization_chain_class_obj = complaint_summarization_chain_class()
#     complaint_rewriter                      = complaint_summarization_chain_class_obj.get_summarization_chain(llm)
#     summarized_complaint                    = complaint_rewriter.invoke({"complaint": complaint})
#     print(summarized_complaint)

#     document_grading_class_obj              = document_grading_class()
#     retriever_tool, retriever               = document_grading_class_obj.get_document_retirever(reg_name, vector_db_path, embedding_function)
#     retrieved_docs                          = retriever.get_relevant_documents(summarized_complaint) 
#     doc_txt                                 = "\n".join([doc.page_content for doc in retrieved_docs])
#     document_grade_chain                    = document_grading_class_obj.get_document_grade_chain(reg_name, llm)
#     grade_response                          = document_grade_chain.invoke({"document": doc_txt, "complaint": summarized_complaint}).binary_score
#     print(grade_response)

#     complaint_clasification_class_obj       = complaint_clasification_class()
#     doc_classification_chain                = complaint_clasification_class_obj.get_doc_classification_chain(reg_name, retriever_tool, llm)
#     doc_response                            = doc_classification_chain.invoke(summarized_complaint)
#     print("################## Doc ####################")
#     print("Classification: " + doc_response.Answer)
#     print(f"Explanation: " + doc_response.Explanation)
    
#     print("################## Web ####################")
#     tavily_search_tool                      = complaint_clasification_class_obj.get_tavily_search_tool(TAVILY_API_KEY, total_tavily_searches = 3)
#     web_classification_chain                = complaint_clasification_class_obj.get_web_classification_chain(reg_name, tavily_search_tool, llm)
#     web_response                            = web_classification_chain.invoke(summarized_complaint)
#     print("Classification: " + web_response.Answer)
#     print("Explanation: " + web_response.Explanation)