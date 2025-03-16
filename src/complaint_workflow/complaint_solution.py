import logging
import os
from langchain_core.prompts import ChatPromptTemplate
from logger import Logger
from langchain_core.runnables import RunnablePassthrough
from logger                                       import Logger

import warnings
warnings.filterwarnings('ignore')


class solution_extraction_class:
    def __init__(self):
        self.logger_obj                 = Logger()
    
    def validate_us_state(self,state):
        """
        Validates if the given state abbreviation is a valid U.S. state.
        
        Parameters:
        state (str): Two-character state abbreviation.
    
        Returns:
        bool: True if valid, raises ValueError if invalid.
        """
        
        # List of valid two-letter U.S. state abbreviations
        us_states = {
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
        }
        
        # Ensure state is uppercase and trimmed
        state = state.strip().upper()
    
        if state not in us_states:
            logging.error(f"Invalid state abbreviation: {state}")
            raise ValueError(f"Invalid state abbreviation: {state}. Please enter a valid U.S. state.")
    
        logging.info(f"Valid state abbreviation: {state}")
        return True

    def validate_us_zipcode(self, zip_code):
        """
        Validates if the given ZIP code is a valid U.S. ZIP code.
        
        Parameters:
        zip_code (str): ZIP code to validate.
    
        Returns:
        bool: True if valid, raises ValueError if invalid.
        """
    
        # Ensure ZIP code is a string and remove extra spaces
        zip_code = str(zip_code).strip()
    
        # Check if ZIP code is 5 digits or 9 digits (ZIP+4 format)
        if not (zip_code.isdigit() and (len(zip_code) == 5 or len(zip_code) == 9)):
            logging.error(f"Invalid ZIP code: {zip_code}")
            raise ValueError(f"Invalid ZIP code: {zip_code}. Please enter a valid 5-digit or 9-digit U.S. ZIP code.")
    
        logging.info(f"Valid ZIP code: {zip_code}")
        return True
        
    def get_doc_solution_chain(self, reg_name, retriever_tool, llm, state, zip_code, company, Product, Sub_Product ):
        logging.info(f"Generating document-based solution extraction chain for {reg_name}.")
        print(f"Generating document-based solution extraction chain for {reg_name}.")

        # Validate the provided state
        #self.validate_us_state(state)  
        
        # Validate the provided zipcode
        #self.validate_us_zipcode(zip_code)

        system_prompt = """
                            You are a **CFPB regulation expert** specializing in **{regulation_name}**.  
                            Your task is to provide a **comprehensive and legally sound resolution** to a customer's complaint **based on official government regulations**.

                            ---
                            
                            ## **Customer Details:**
                            - **Company:** {company}
                            - **State:** {state}
                            - **Zip Code:** {zip_code}
                            - **Product** {Product}
                            - **SubProduct** {Sub_Product}


                            Some **{regulation_name} clauses vary based on state and location**.  
                            Ensure that your solution takes into account **both location-specific and nationwide clauses**.

                            ---

                            ## **Instructions:**
                            1. Provide a **clear, structured, and well-explained legal resolution** to the complaint.  
                            2. **Directly reference relevant clauses** of **{regulation_name}** to justify your solution.  
                            3. If multiple clauses apply, **explain how they relate** to the complaint.  
                            4. Ensure the response is **specific, legally backed, and avoids vague or generic answers**.  
                            5. If the complaint involves discrimination, **mention relevant anti-discrimination provisions**.  

                            ---

                            ## **Regulation Context (Extracted from Official Documents):**  
                            {{context}}

                            ---

                            ## **Consumer Complaint:**  
                            "{{complaint}}"

                            ---

                            ## **Expert Legal Resolution:**
                            - Summarize the key **regulatory protections** that apply to this case.  
                            - Identify **specific {regulation_name} clauses** that address the complaint.  
                            - Provide a **clear resolution path** for the complainant, based on legal guidelines.  
                            - If relevant, mention any **steps the complainant can take** (e.g., filing a dispute, contacting regulatory agencies).  
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
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate solution extraction chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate solution extraction chain.")
            return None

        # Format system prompt with the correct regulation name
        system = system_prompt.format(regulation_name=regulation_mapping[reg_name], company=company, state=state, zip_code=zip_code,Product=Product  , Sub_Product =Sub_Product)

        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")

        # Create solution extraction prompt
        solution_prompt = ChatPromptTemplate.from_messages([
                                                                ("system", system),
                                                                ("human", "Analyze the complaint and generate a legally backed solution."),
                                                           ])

        # Build the full solution extraction chain
        solution_chain = (
                            {
                                "context": retriever_tool,
                                "complaint": RunnablePassthrough(),
                                "company": lambda _: company,
                                "state": lambda _: state,
                                "zip_code": lambda _: zip_code,
                                "Product": lambda _: Product,
                                "Sub_Product": lambda _: Sub_Product
                            }
                            | solution_prompt
                            | llm
                         )

        logging.info(f"Solution extraction chain successfully generated for {reg_name}.")
        print(f"Solution extraction chain successfully generated for {reg_name}.")
        
        return solution_chain
    
    
    def get_web_solution_chain(self, reg_name, tavily_search_tool, llm, state, zip_code, company, Product, Sub_Product ):
        logging.info(f"Generating web-based solution extraction chain for {reg_name}.")
        print(f"Generating web-based solution extraction chain for {reg_name}.")
        
        # Validate State & ZIP Code
        #self.validate_us_state(state)
        #self.validate_us_zipcode(zip_code)
        
        system_prompt = """
                            You are a **CFPB regulation expert**. You have access to **real-time web search results**.
                            The complaint has been classified under **{regulation_name}**.  
                            Using the retrieved **web context**, provide a **detailed legal solution** to the customer's complaint
                            based on the **latest government guidelines** for **{regulation_name}**.

                            ---
                            
                            ## **Customer Information:**
                            - **Company:** {company}
                            - **State:** {state}
                            - **Zip Code:** {zip_code}
                            - **Product** {Product}
                            - **SubProduct** {Sub_Product}

                            Some **{regulation_name} clauses vary based on state and location**.  
                            Ensure that your solution takes into account **both location-specific and nationwide clauses**.

                            ---

                            ## **Instructions:**
                            1. Provide a **clear, structured, and well-explained solution** to the complaint.  
                            2. **Directly reference relevant CFPB regulations and government guidelines**.  
                            3. If multiple sources apply, mention them and explain how they relate to the complaint.  
                            4. Some **{regulation_name} clauses vary based on state and ZIP code**—consider this.  
                            5. Avoid generic answers—your response should be backed by **actual regulatory sources and legal reasoning**.

                            ---

                            ## **Web Context (extracted from search results):**
                            {{context}}

                            ---

                            ## **Consumer Complaint:**  
                            "{{complaint}}"

                            ---

                            ## **Expert Legal Resolution:**
                            - Explain the **regulatory protections** applicable to this complaint.  
                            - Mention the **relevant CFPB laws, regulations, or case references**.  
                            - Provide a **resolution path** based on legal guidelines.  
                            - If applicable, mention steps like **filing a dispute, contacting regulatory agencies**.
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
            logging.error(f"Unknown regulation: {reg_name}. Unable to generate web solution extraction chain.")
            print(f"Unknown regulation: {reg_name}. Unable to generate web solution extraction chain.")
            return None
        
        # Format system prompt with the correct regulation name
        system = system_prompt.format(
                                        regulation_name=regulation_mapping[reg_name],
                                        company=company,
                                        state=state,
                                        zip_code=zip_code,
                                        Product=Product  , 
                                        Sub_Product =Sub_Product
                                    )

        logging.info(f"System prompt generated for {reg_name}.")
        print(f"System prompt generated for {reg_name}.")

        # Create web solution extraction prompt
        web_solution_prompt = ChatPromptTemplate.from_messages([
                                                                    ("system", system),
                                                                    ("human", "Analyze the complaint using web context and generate a legally backed solution."),
                                                              ])
        
        # Build the full web-based solution extraction chain
        web_solution_chain = (
                                {
                                    "context": tavily_search_tool,
                                    "complaint": RunnablePassthrough(),
                                    "company": lambda _: company,
                                    "state": lambda _: state,
                                    "zip_code": lambda _: zip_code,
                                    "Product": lambda _: Product,
                                    "Sub_Product": lambda _: Sub_Product,
                                }
                                | web_solution_prompt
                                | llm
                             )

        logging.info(f"Web solution extraction chain successfully generated for {reg_name}.")
        print(f"Web solution extraction chain successfully generated for {reg_name}.")
        
        return web_solution_chain


# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from complaint_summarization import complaint_summarization_chain_class
#     from document_grading import document_grading_class
#     from complaint_classification import complaint_clasification_class
    
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
#     complaint                               = "Navy Federal Credit Union is participating in illegal collecting and reporting practices by improperly adding 3 incorrect late payments for XXXX ( XXXX, XXXX, and XXXX ) to auto loan XXXX. I am now working towards paying off my 3rd vehicle loan with Navy Federal with perfect payment history prior to this occurrence. In XX/XX/XXXX, one late payment was reported to the 3 credit bureaus for XX/XX/XXXX. This ensued my immediate contact with Navy Federal Credit Union loan servicing department. My first conversation about this matter in XX/XX/XXXX, I spoke with the Senior Manager of the department. This conversation was recorded on my personal device with the knowledge of both myself and the Navy Federal representative. During this conversation, we  discussed the late payment that was now reporting for XX/XX/XXXX, as well as the second of the two deferments done on the account within a 7 month period. She assured me, the account had not been 30 days delinquent during either deferment period nor prior to them going into affect. Incidentally, she is the sole individual that approved both deferments on my loan. With that assurance, I was confident the late payment would be removed. However, for record keeping purposes, I requested that in writing. I was then informed that she could not individually draft any letters for consumers. I then asked what could I do to fix the reported late payment. I was instructed to complete the dispute process with Navy Federal or with each individual credit bureau. At which point, I initiated the dispute process with XXXX, through my XXXX   membership. Within 10 days, the dispute was complete in opposition to the credit report. Navy Federal responded that the late payment for XX/XX/XXXX was accurate and added 2 additional late payments for XX/XX/XXXX and XX/XX/XXXX. All of these dates reported are dates within the deferments that took place almost consecutively with one month between them. After receiving such response from the dispute, I decided to make another attempt at resolving this with Navy Federal. I emailed the CEO, XXXX XXXX, three separate times with no response or effectiveness. Lastly, I called Navy Federal again, on a personal recorded line, to discuss the additional reported late payments. I questioned why two additional late payments were added after disputing one late payment, why all of them remain, and why are they reporting inaccurately. During this call, there were no attempts to rectify the errors, nor were there any suggested solutions. Prior to these reported late payments, I was in the lending process with XXXX  ( XXXX XXXX XXXX XXXX ) to purchase my first home for my XXXX  young children and myself. This has adversely affected my credit score. Due to the detrimental affects of these negative remarks, I am no longer moving forward in the lending process with XXXX. Navy Federal Credit Union is participating in illegal reporting practices. I have contacted them repeatedly to try and resolve this matter without a resolution."
#     company   = 'JPMORGAN CHASE & CO.'
#     state     = 'NJ'
#     zip_code  = '08701'
#     Product   = 'Credit reporting, credit repair services, or other personal consumer reports'
#     Sub_Product = "Credit reporting"
    

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
#     doc_solution_chain                      = solution_extraction_class_obj.get_doc_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company, Product, Sub_Product)
#     doc_solution_response                   = doc_solution_chain.invoke(summarized_complaint).content
#     print(doc_solution_response)
    
#     print("################## Web Solution ####################")
#     web_solution_chain                      = solution_extraction_class_obj.get_web_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company, Product, Sub_Product)
#     web_solution_response                   = web_solution_chain.invoke(summarized_complaint).content
#     print(web_solution_response)