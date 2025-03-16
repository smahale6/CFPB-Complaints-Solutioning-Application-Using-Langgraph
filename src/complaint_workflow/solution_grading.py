import logging
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from logger import Logger

import warnings
warnings.filterwarnings('ignore')


class solution_grading_class:
    def __init__(self):
        self.logger_obj = Logger()

    def get_doc_hallucination_grading_chain(self, reg_name, llm):
        logging.info(f"Generating hallucination grading chain for {reg_name}.")
        print(f"Generating hallucination grading chain for {reg_name}.")

        class GradeDocHallucinations(BaseModel):
            """Binary score for hallucination detection in the generated solution."""
            binary_score: str = Field(description="To check if the solution addresses all aspects of the customer's complaint, 'yes' or 'no'")

        # LLM with structured function call
        doc_hal_structured_llm_grader = llm.with_structured_output(GradeDocHallucinations)

        system_prompt = """
                            You are a **strict grader** responsible for **verifying the accuracy and completeness** of the provided solution 
                            for a **summarized customer complaint** under **{regulation_name}**. 

                            ---

                            ## ** Grading Task:**
                            Your job is to **strictly evaluate** whether the solution correctly and **completely** addresses all concerns raised in the **customer complaint** 
                            based on the **retrieved {regulation_name} document**. 

                            ---

                            ## ** Evaluation Criteria (Must meet all):**
                            1️ **Coverage:** The solution must **fully** address all **specific issues** raised in the complaint.  
                            2️ **Regulatory Accuracy:** The solution must **correctly reference and interpret** {regulation_name} clauses.  
                            3️ **Clarity & Completeness:** The response must be **clear, well-structured, and legally sound**.  
                            4️ **Relevance:** The response must be **strictly aligned** with the retrieved {regulation_name} document.  
                            5️ **No Hallucination:** The solution must not **introduce new, unrelated, or incorrect information**.  

                            ---

                            ## **Strict Grading Rules:**
                            - **"Yes"** → The solution **fully meets** all five evaluation criteria.  
                            - **"No"** → If the solution **fails** in even one criterion, **strictly mark it as "No"**.  

                            ---

                            ## **Retrieved {regulation_name} Document:**  
                            {{documents}}  

                            ---

                            ## **Customer Complaint:**  
                            "{{complaint}}"  

                            ---

                            ## **Solution Provided:**  
                            "{{solution}}"  

                            ---

                            ## **Final Decision (Yes/No):**
                        """

        # Regulation Mapping
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
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate hallucination grading chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate hallucination grading chain.")
            return None

        # Format system prompt with the correct regulation name
        system = system_prompt.format(regulation_name=regulation_mapping[reg_name])

        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")

        # Create hallucination grading prompt
        doc_hallucinations_prompt = ChatPromptTemplate.from_messages([
                                                                        ("system", system),
                                                                        ("human", "Review the retrieved document, complaint, and solution carefully. Provide a strict 'Yes' or 'No' grading."),
                                                                     ])

        # Build the full hallucination grading chain
        doc_hallucinations_grader = (
            {
                "documents": RunnablePassthrough(),
                "complaint": RunnablePassthrough(),
                "solution": RunnablePassthrough(),
            }
            | doc_hallucinations_prompt
            | doc_hal_structured_llm_grader
        )

        logging.info(f"Hallucination grading chain successfully generated for {reg_name}.")
        print(f"Hallucination grading chain successfully generated for {reg_name}.")

        return doc_hallucinations_grader

    def get_web_hallucination_grading_chain(self, reg_name, llm):
        logging.info(f"Generating web-based hallucination grading chain for {reg_name}.")
        print(f"Generating web-based hallucination grading chain for {reg_name}.")

        class GradeWebHallucinations(BaseModel):
            """Binary score for hallucination detection in the web-based solution."""
            binary_score: str = Field(description="To check if the web-based solution fully addresses the customer's complaint, 'yes' or 'no'.")

        # LLM with structured function call
        web_hal_structured_llm_grader = llm.with_structured_output(GradeWebHallucinations)

        system_prompt = """
                            You are a **strict grader** responsible for **verifying the accuracy and completeness** of the provided solution 
                            for a **summarized customer complaint** under **{regulation_name}** using **web search results**.

                            ---

                            ## **Grading Task:**
                            Your job is to **strictly evaluate** whether the web-based solution **correctly and completely** addresses 
                            all concerns raised in the **customer complaint** based on the **retrieved web search results**.

                            ---

                            ## **Evaluation Criteria (Must meet all):**
                            1️ **Coverage:** The solution must **fully** address all **specific issues** raised in the complaint.  
                            2️ **Regulatory Accuracy:** The solution must **correctly reference and interpret** {regulation_name} guidelines.  
                            3️ **Clarity & Completeness:** The response must be **clear, well-structured, and legally sound**.  
                            4️ **Relevance:** The response must be **strictly aligned** with the retrieved web context.  
                            5️ **No Hallucination:** The solution must not **introduce new, unrelated, or incorrect information**.  

                            ---

                            ## **Strict Grading Rules:**
                            - **"Yes"** → The solution **fully meets** all five evaluation criteria.  
                            - **"No"** → If the solution **fails** in even one criterion, **strictly mark it as "No"**.  

                            ---

                            ## **Retrieved Web Context:**  
                            {{context}}  

                            ---

                            ## **Customer Complaint:**  
                            "{{complaint}}"  

                            ---

                            ## **Solution Provided:**  
                            "{{solution}}"  

                            ---

                            ## **Final Decision (Yes/No):**
                        """

        # Regulation Mapping
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
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate web solution grading chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate web solution grading chain.")
            return None

        # Format system prompt with the correct regulation name
        system = system_prompt.format(regulation_name=regulation_mapping[reg_name])

        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")

        # Create web hallucination grading prompt
        web_hallucinations_prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", "Review the retrieved web context, complaint, and solution carefully. Provide a strict 'Yes' or 'No' grading."),
        ])

        # Build the full hallucination grading chain
        web_hallucinations_grader = (
            {
                "context": RunnablePassthrough(),
                "complaint": RunnablePassthrough(),
                "solution": RunnablePassthrough(),
            }
            | web_hallucinations_prompt
            | web_hal_structured_llm_grader
        )

        logging.info(f"Web solution grading chain successfully generated for {reg_name}.")
        print(f"Web solution grading chain successfully generated for {reg_name}.")

        return web_hallucinations_grader


# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from complaint_summarization import complaint_summarization_chain_class
#     from document_grading import document_grading_class
#     from complaint_classification import complaint_clasification_class
#     from complaint_solution import solution_extraction_class
    
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
#     company   = 'JPMORGAN CHASE & CO.'
#     state     = 'NJ'
#     zip_code  = '08701'

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
    
#     print("################## Doc Classification ####################")
#     print("Classification: " + doc_response.Answer)
#     print(f"Explanation: " + doc_response.Explanation)
    
#     print("################## Web Classification ####################")
#     tavily_search_tool                      = complaint_clasification_class_obj.get_tavily_search_tool(TAVILY_API_KEY, total_tavily_searches = 3)
#     web_classification_chain                = complaint_clasification_class_obj.get_web_classification_chain(reg_name, tavily_search_tool, llm)
#     web_response                            = web_classification_chain.invoke(summarized_complaint)
#     print("Classification: " + web_response.Answer)
#     print("Explanation: " + web_response.Explanation)
    
#     print("################## Doc Solution ####################")
#     solution_extraction_class_obj           = solution_extraction_class()
#     doc_solution_chain                      = solution_extraction_class_obj.get_doc_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company)
#     doc_solution_response                   = doc_solution_chain.invoke(summarized_complaint).content
#     print(doc_solution_response)
    
#     print("################## Web Solution ####################")
#     web_solution_chain                      = solution_extraction_class_obj.get_web_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company)
#     web_solution_response                   = web_solution_chain.invoke(summarized_complaint).content
#     print(web_solution_response)
    
#     print("################## Doc Grading ####################")
#     solution_grading_class_obj              = solution_grading_class()
#     doc_hallucinations_grader               = solution_grading_class_obj.get_doc_hallucination_grading_chain(reg_name, llm)
#     doc_grading_response                    = doc_hallucinations_grader.invoke({"documents": doc_txt,"complaint": summarized_complaint,"solution": doc_solution_response})
#     print(doc_grading_response.binary_score)

#     print("################## Web Grading ####################")
#     web_hallucinations_grader               = solution_grading_class_obj.get_web_hallucination_grading_chain(reg_name, llm)
#     web_grading_response                    = web_hallucinations_grader.invoke({"documents": web_txt,"complaint": summarized_complaint,"solution": doc_solution_response})
#     print(web_grading_response.binary_score)