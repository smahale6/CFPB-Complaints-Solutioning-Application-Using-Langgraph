import logging
import os
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from logger import Logger
from langchain.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import Tool

import warnings
warnings.filterwarnings('ignore')

class document_grading_class:
    def __init__(self):
        self.logger_obj = Logger()

    def get_document_retirever(self,reg_name, vector_db_path, embedding_function):
        logging.info("Retrieving the relevant documents for {} for the summarized Complaint.".format(reg_name))
        print("Retrieving the relevant documents for {} for the summarized Complaint.".format(reg_name))
        # Construct the full path to the vector store
        persist_directory = os.path.join(vector_db_path, reg_name)
        
        # Load the persisted Chroma vector store
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embedding_function) 
        
        # Convert Chroma store to retriever
        retriever      = vector_store.as_retriever()
        logging.info("Completed retrieving the relevant documents for {} for the summarized Complaint.".format(reg_name))
        print("Completed retrieving the relevant documents for {} for the summarized Complaint.".format(reg_name))
        
        # Getting retriever tool
        retriever_tool = create_retriever_tool(
                                                retriever   = vector_store.as_retriever(),
                                                name        = "{} retriever".format(reg_name),
                                                description = "Retrieve relevant {} documents for a given complaint.".format(reg_name)
                                                      )
        return retriever_tool, retriever
        

    def get_document_grade_chain(self, reg_name, llm):
        print("Document Grading Chain Initialized.")
        logging.info("Document Grading Chain Initialized.")
        print(f"Generating document grading chain for {reg_name}.")
        logging.info(f"Generating document grading chain for {reg_name}.")

        class GradeDocuments(BaseModel):
            """Binary score for relevance check on retrieved documents."""
            binary_score: str = Field(description="Documents are relevant to the complaints, 'yes' or 'no'")

        # LLM with function call
        structured_llm_grader = llm.with_structured_output(GradeDocuments)
        logging.info("Structured LLM grader initialized.")

        system_template = """You are a strict evaluator assessing whether a retrieved document is **highly relevant** to a summarized customer complaint.
                                Your goal is to **strictly validate** if the document provides information that addresses the customer's issue.
                                
                                ### **Evaluation Criteria:**
                                1 **Direct Match:** The document **must explicitly** discuss topics covered under **{regulation_name}**.
                                2 **Legal Basis:** The document should **mention key legal clauses, interpretations, or compliance guidelines** related to the complaint.
                                3 **Actionability:** The document must provide **useful insights or references** to help resolve the customer's issue.
                                4 **Avoid False Positives:** If the document contains **generic lending rules** or **irrelevant financial regulations**, it should be marked **'no'**.
                                
                                ### **Instructions:**
                                - **Answer only 'yes' or 'no'.**
                                - If the document **directly supports** the complaint under {regulation_name} → **Respond with 'yes'**.
                                - If the document is **partially relevant** or **completely unrelated** → **Respond with 'no'**.
                          """

        regulation_mapping = {
                                "Reg_AA": "Regulation AA (Unfair or Deceptive Acts or Practices)",
                                "Reg_B":  "Regulation B (Equal Credit Opportunity Act - ECOA)",
                                "Reg_C":  "Regulation C (Home Mortgage Disclosure Act - HMDA)",
                                "Reg_D":  "Regulation D (Alternative Mortgage Transaction Parity Act)",
                                "Reg_E":  "Regulation E (Electronic Fund Transfer Act - EFTA)",
                                "Reg_F":  "Regulation F (Fair Debt Collection Practices Act - FDCPA)",
                                "Reg_G":  "Regulation G (S.A.F.E. Mortgage Licensing Act – Federal Registration)",
                                "Reg_H":  "Regulation H (S.A.F.E. Mortgage Licensing Act – State Compliance)",
                                "Reg_I":  "Regulation I (Disclosure Requirements for Depository Institutions Lacking Federal Deposit Insurance)",
                                "Reg_J":  "Regulation J (Land Sales Registration)",
                                "Reg_K":  "Regulation K (Purchasers’ Revocation Rights, Sales Practices and Standards)",
                                "Reg_L":  "Regulation L (Protection of Nonpublic Personal Information)",
                                "Reg_M":  "Regulation M (Consumer Leasing)",
                                "Reg_N":  "Regulation N (Mortgage Acts and Practices – Advertising Rule)",
                                "Reg_O":  "Regulation O (Mortgage Assistance Relief Services - MARS Rule)",
                                "Reg_P":  "Regulation P (Privacy of Consumer Financial Information)",
                                "Reg_V":  "Regulation V (Fair Credit Reporting - FCRA)",
                                "Reg_X":  "Regulation X (Real Estate Settlement Procedures Act - RESPA)",
                                "Reg_Z":  "Regulation Z (Truth in Lending Act - TILA)",
                                "Reg_CC": "Regulation CC (Availability of Funds and Collection of Checks)",
                                "Reg_DD": "Regulation DD (Truth in Savings Act - TISA)"
                            }

        if reg_name not in regulation_mapping:
            print(f"Unknown regulation: {reg_name}. Unable to generate grading chain.")
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate grading chain.")
            return None

        system = system_template.format(regulation_name=regulation_mapping[reg_name])
        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")
        
        grade_prompt = ChatPromptTemplate.from_messages([
                                                            ("system", system),
                                                            ("human", "Retrieved document: \n\n {document} \n\n Summarized complaint: {complaint}")
                                                        ])
        
        logging.info(f"ChatPromptTemplate initialized for {reg_name}.")
        print(f"ChatPromptTemplate initialized for {reg_name}.")
        document_grade_chain = grade_prompt | structured_llm_grader
        logging.info(f"Document grading chain successfully generated for {reg_name}.")
        print(f"Document grading chain successfully generated for {reg_name}.")
        return document_grade_chain

# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from complaint_summarization import complaint_summarization_chain_class
    
#     llm_model                               = 'llama3-70b-8192'
#     cart_path                               = r'C:\GitHub Collections\CART 2.0\src'
#     regulations_path                        = cart_path + '\\regulations'
#     vector_db_path                          = cart_path + '\\vector_db\\'
#     reg_name                                = 'Reg_X'

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
    
    

        
    
    
    
    
    
    
    
    
    
    
    