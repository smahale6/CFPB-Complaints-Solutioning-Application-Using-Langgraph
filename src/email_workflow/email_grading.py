import logging
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from logger import Logger

import warnings
warnings.filterwarnings('ignore')


class email_grading_class:
    def __init__(self):
        self.logger_obj = Logger()
        
    def regulation_email_grading_chain(self, llm, Complaint_ID):
        logging.info(f"Generating email grading for Complaint ID: {Complaint_ID}.")
        print(f"Generating email grading for Complaint ID: {Complaint_ID}.")

        class GradeEmail(BaseModel):
            """Binary score for hallucination present in generation answer."""
            binary_score: str = Field(description="To check if email addresses all the aspects of customers complaint, 'yes' or 'no'")
            Feedback:     str = Field(description="Feedback against the email if the email does not address all the concerns ")

        llm_email_grader = llm.with_structured_output(GradeEmail)
        
        system = """
                        You are a **supervisor of CFPB regulation experts** with deep expertise in CFPB regulations and their legal applications.
                        Your role is to **verify** whether the provided email response appropriately addresses the customer's complaint **without being overly strict in grading**.
            
                        ### **Customer Complaint:**  
                        "{complaint}"  
            
                        ### **Regulation Details:**  
                        - **Total Regulations:** {Total_Regulations}
                        - **Regulation Names:** {Regulation_Names}
            
                        ### **Email Response:** 
                        {email_response} 
                        
                        ## **Grading Task:**
                        Your job is to **evaluate** whether the email response sufficiently addresses all **key concerns** in the **customer complaint** 
                        based on the relevant CFPB regulations.
            
                        ## **Evaluation Criteria:**
                        1️ **Coverage:** Does the email adequately address the major concerns raised in the complaint? Minor omissions are acceptable.  
                        2️ **Regulatory Accuracy:** Does the email correctly **reference and interpret** the relevant CFPB regulations?  
                        3️ **Clarity & Completeness:** Is the response clear, well-structured, and easy for the customer to understand?  
                        4️ **No Hallucination:** Does the email avoid adding unrelated or incorrect information?  
            
                        ## **Grading Rules:**
                        - **"Yes"** → The email sufficiently meets the above criteria. **Minor gaps are acceptable** as long as they don’t change the meaning or regulatory guidance.  
                        - **"No"** → Mark as "No" **only** if the email has **major errors** (e.g., missing core concerns, misrepresenting regulations, or providing incorrect information).  
            
                        ## **Feedback Guidelines:**
                        - If **Grade = Yes**, no feedback is needed.
                        - If **Grade = No**, provide **constructive feedback** on what the email **must improve or include**.
            
                        ## **Final Decision (Yes/No):**
                        **Feedback (if applicable):**
            """


        Email_grade_prompt = ChatPromptTemplate.from_messages(
                                                                    [
                                                                        ("system", system),
                                                                        ("human", "Review the solution in email response,regulation names, complaint carefully. Provide a strict 'Yes' or 'No' grading and a feedback."),
                                                                    ]
                                                                )
        email_grader_chain = Email_grade_prompt | llm_email_grader
        logging.info(f"Completed generating email grading for Complaint ID: {Complaint_ID}.")
        print(f"Completed generating email grading for Complaint ID: {Complaint_ID}.")
        return email_grader_chain

    def non_regulation_email_grading_chain(self, llm, Complaint_ID):
        logging.info(f"Generating email grading for Complaint ID: {Complaint_ID}.")
        print(f"Generating email grading for Complaint ID: {Complaint_ID}.")
        
        class GradeEmailNoReg(BaseModel):
            """Binary score for checking if the email appropriately addresses a no-regulation complaint."""
            binary_score: str = Field(description="Does the email provide a friendly and helpful response? Answer 'yes' or 'no'")
            Feedback: str = Field(description="Provide feedback if the email does not address the complaint appropriately.")

        # LLM with structured output
        llm_email_grader = llm.with_structured_output(GradeEmailNoReg)
        
        system_prompt = """
                                You are a **supervisor of CFPB regulation experts** leading a team of **customer support specialists** handling customer concerns.  
                                Some customers express **dissatisfaction**, but their complaints do not necessarily fall under CFPB regulations.  
                                In such cases, the goal is to **acknowledge their concerns with empathy and provide helpful guidance**.  
                    
                                ### **Customer Complaint:**  
                                "{complaint}"  
                    
                                ### **Email Response:**  
                                {email_response}  
                    
                                ## **Evaluation Criteria:**  
                                1️**Empathy & Understanding:** The response should make the customer feel heard and valued.  
                                2️**Professionalism & Clarity:** It should maintain a respectful, clear, and approachable tone.  
                                3️**Helpfulness of Recommendations:** If suggestions are provided, they should be **practical, encouraging, and within CFPB guidelines**.  
                    
                                ## **Grading Guidelines:**  
                                - **"Yes"** → The email is **warm, professional, and offers reasonable guidance**. Small improvements are okay as long as they don’t affect clarity or accuracy.  
                                - **"No"** → The email is **unclear, dismissive, or provides misleading suggestions** that might confuse the customer.  
                    
                                ## **Feedback Approach:**  
                                - If **Grade = Yes**, no feedback is needed.  
                                - If **Grade = No**, provide **gentle, constructive feedback** suggesting improvements to tone, clarity, or guidance.  
                    
                                ## **Final Decision (Yes/No):**  
                                **Feedback (if applicable):**
                    """
        
        
        # Create prompt template
        no_reg_email_grade_prompt = ChatPromptTemplate.from_messages(
                                                                        [
                                                                            ("system", system_prompt),
                                                                            ("human", "Review the email response carefully. Ensure it is friendly and provides correct recommendations. Then, provide a strict 'Yes' or 'No' grading along with feedback if necessary."),
                                                                        ]
                                                                    )
        
        # Create the grading pipeline
        no_reg_email_grader_chain = no_reg_email_grade_prompt | llm_email_grader
        logging.info(f"Generating email grading for Complaint ID: {Complaint_ID}.")
        print(f"Generating email grading for Complaint ID: {Complaint_ID}.")
        
        return no_reg_email_grader_chain
        
        
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from document_grading import document_grading_class
#     from email_formation import email_formation_class
    
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

#     Complaint_ID      = '6781175'
#     Complaint_Text    = "I was scammed by someone who used this 3 companies names in 2 different banks : ( XXXX XXXX XXXX AND XXXX XXXX ) at XXXX XXXX XXXX ) based in California under XXXX clients. And the other company is XXXX XXXX XXXX. WITH JPMORGAN BANK. also under XXXX clients ) I tried to get my money through my bank but these banks are refusing giving me my XXXX $ back. ( I got pictures, bank accounts, dates, names, ) all I want is my money back."
#     Company           = "JPMORGAN CHASE & CO."
#     State             = "LA"
#     Zip_Code          = "70056"
#     Total_Regulations = 4
#     Regulation_Names  = "Reg_D, Reg_E, Reg_V, Reg_AA"
#     Feedback          = ""
#     Solutions         = """ 
#                                ____________________Reg_D_______________
#     **Expert Legal Resolution:**
    
#     **Summary of Regulatory Protections:**
    
#     The complaint involves fraudulent activity/scam involving unauthorized use of company names and bank accounts, resulting in a loss of money ($XXXX) and lack of assistance from banks in resolving the issue. The relevant regulatory protections that apply to this case are:
    
#     1. Regulation E (Electronic Fund Transfers) - 12 CFR Part 1005, which governs electronic fund transfers, including unauthorized transactions and error resolution procedures.
#     2. Regulation AA (Unfair or Deceptive Acts or Practices - UDAP) - 12 CFR Part 227, which prohibits unfair or deceptive acts or practices by banks and other financial institutions.
    
#     **Specific Regulation D Clauses:**
    
#     Although the complaint does not directly involve Regulation D (Alternative Mortgage Transaction Parity Act), it is essential to note that Regulation D does not apply to this case, as it primarily deals with alternative mortgage transactions and parity between state and federal laws.
    
#     **Clear Resolution Path:**
    
#     Based on Regulation E and Regulation AA, the complainant has the right to dispute the unauthorized transactions and request a refund of the stolen money. The banks involved, including JPMorgan Bank, are required to investigate and resolve the dispute in a timely and fair manner.
    
#     **Steps for the Complainant:**
    
#     1. **File a dispute:** The complainant should file a dispute with both banks, XXXX XXXX XXXX (based in California) and JPMorgan Bank, regarding the unauthorized transactions and request a refund of the stolen money.
#     2. **Provide documentation:** The complainant should provide any relevant documentation, such as transaction records, account statements, and police reports, to support their claim.
#     3. **Contact regulatory agencies:** If the banks fail to assist in resolving the issue, the complainant can contact regulatory agencies, such as the Consumer Financial Protection Bureau (CFPB) or the Office of the Comptroller of the Currency (OCC), to file a complaint and seek assistance.
#     4. **Seek legal counsel:** If the issue is not resolved, the complainant may want to consider seeking legal counsel to explore further legal options.
    
#     **Relevant Regulation E Clauses:**
    
#     * 12 CFR 1005.11(a) - Error resolution procedures: The bank must investigate and resolve the dispute within a reasonable time, not exceeding 10 business days.
#     * 12 CFR 1005.11(b) - Provisional credit: The bank must provisionally credit the complainant's account for the disputed amount while investigating the dispute.
    
#     **Relevant Regulation AA Clauses:**
    
#     * 12 CFR 227.3 - Unfair or deceptive acts or practices: Banks are prohibited from engaging in unfair or deceptive acts or practices, including failing to assist in resolving fraudulent activity.
    
#     By following these steps and referencing the relevant regulatory clauses, the complainant should be able to resolve the issue and obtain a refund of the stolen money.
    
#     ____________________Reg_E_______________
#     **Expert Legal Resolution:**
    
#     **Summary of Regulatory Protections:**
    
#     The complaint involves fraudulent activity/scam involving unauthorized use of company names and bank accounts, resulting in a loss of money. The customer is seeking a refund and alleges that the banks, including JPMorgan Chase & Co., failed to assist in resolving the issue. This case falls under the purview of Regulation E (Electronic Fund Transfer Act - EFTA), which protects consumers from unauthorized electronic fund transfers.
    
#     **Relevant Regulation E Clauses:**
    
#     1. **12 CFR 1005.6(b)(1) and (2)**: These clauses limit the consumer's liability for unauthorized electronic fund transfers (EFTs) to $50 or the amount of unauthorized EFTs that occurred within two business days, whichever is less, if the consumer notifies the financial institution within two business days after learning of the loss or theft of an access device.
#     2. **12 CFR 1005.6(b)(3)**: This clause states that if a consumer notifies the financial institution of an unauthorized EFT within 60 calendar days of transmittal of the periodic statement upon which the unauthorized EFT appears, the financial institution shall not hold the consumer liable for amounts as set forth in 12 CFR 1005.6(b)(1) or (2).
#     3. **12 CFR 1005.11**: This section outlines the error resolution procedures that financial institutions must follow when a consumer alleges an error, including unauthorized EFTs.
    
#     **Clear Resolution Path:**
    
#     Based on the complaint, the customer should:
    
#     1. **Notify JPMorgan Chase & Co. and the other involved bank**: The customer should notify both banks of the unauthorized EFTs and request a refund of the stolen money. The customer should provide any necessary documentation to support their claim.
#     2. **File a dispute**: The customer should file a dispute with the banks, citing the unauthorized EFTs and requesting a refund. The banks are required to investigate the dispute and respond to the customer within a reasonable time frame.
#     3. **Request provisional re-credit**: If the banks determine that the EFTs were unauthorized, they should provisionally re-credit the customer's account pending the outcome of the investigation.
    
#     **Steps the Complainant Can Take:**
    
#     1. **Contact the Consumer Financial Protection Bureau (CFPB)**: If the banks fail to assist in resolving the issue or do not comply with Regulation E, the customer can file a complaint with the CFPB.
#     2. **Contact the Louisiana Office of Financial Institutions**: As the customer is located in Louisiana, they can also contact the Louisiana Office of Financial Institutions to report the issue and seek assistance.
    
#     By following these steps, the customer should be able to resolve the issue and obtain a refund of the stolen money. The banks are required to comply with Regulation E and investigate the dispute in a timely and fair manner.
    
#     ____________________Reg_V_______________
#     **Expert Legal Resolution:**
    
#     **Summary of Regulatory Protections:**
    
#     The complaint involves fraudulent activity/scam involving unauthorized use of company names and bank accounts, resulting in a loss of money. The customer is seeking a refund and assistance from the banks in resolving the issue. The relevant regulatory protections that apply to this case include:
    
#     1. Regulation E (Electronic Fund Transfers): This regulation governs electronic fund transfers, including unauthorized transactions.
#     2. Regulation AA (Unfair or Deceptive Acts or Practices - UDAP): This regulation prohibits unfair or deceptive acts or practices by banks.
#     3. Regulation V (Fair Credit Reporting - FCRA): This regulation governs the reporting of credit information and the duties of furnishers of information.
    
#     **Specific Regulation V (Fair Credit Reporting - FCRA) Clauses:**
    
#     The following Regulation V clauses are relevant to this complaint:
    
#     1. 12 CFR § 1022.43(a)(1)(i): This clause requires furnishers of information to investigate disputes from consumers and correct inaccurate information.
#     2. 12 CFR § 1022.43(a)(1)(ii): This clause requires furnishers of information to provide a written response to the consumer within 30 days of receiving a dispute, stating the results of the investigation.
#     3. 12 CFR § 1022.43(a)(1)(iii): This clause requires furnishers of information to provide a written notice to the consumer of the results of the investigation, including any corrections made to the consumer's file.
    
#     **Clear Resolution Path:**
    
#     Based on the regulatory protections and Regulation V clauses mentioned above, the following resolution path is recommended:
    
#     1. The customer should file a dispute with JPMorgan Chase & Co. and the other bank involved, citing the fraudulent activity and unauthorized use of their account.
#     2. The customer should provide any relevant documentation, such as a police report or identity theft report, to support their claim.
#     3. The banks must investigate the dispute and correct any inaccurate information within 30 days of receiving the dispute.
#     4. The banks must provide a written response to the customer, stating the results of the investigation and any corrections made to the customer's file.
#     5. If the banks fail to resolve the issue, the customer may file a complaint with the Consumer Financial Protection Bureau (CFPB) or the Federal Trade Commission (FTC).
    
#     **Steps the Complainant Can Take:**
    
#     1. File a dispute with JPMorgan Chase & Co. and the other bank involved, citing the fraudulent activity and unauthorized use of their account.
#     2. Provide any relevant documentation, such as a police report or identity theft report, to support their claim.
#     3. Follow up with the banks to ensure they are investigating the dispute and correcting any inaccurate information.
#     4. If the banks fail to resolve the issue, file a complaint with the CFPB or FTC.
    
#     By following this resolution path, the customer should be able to resolve the issue and obtain a refund for the stolen money.
    
#     ____________________Reg_AA_______________
#     **Expert Legal Resolution:**
    
#     **Summary of Regulatory Protections:**
    
#     The complaint involves fraudulent activity/scam involving unauthorized use of company names and bank accounts, resulting in a loss of money ($XXXX) and lack of assistance from banks in resolving the issue. The relevant regulatory protections that apply to this case are:
    
#     1. Regulation E (Electronic Fund Transfers): This regulation protects consumers from unauthorized electronic fund transfers and requires financial institutions to investigate and resolve disputes in a timely manner.
#     2. Regulation AA (Unfair or Deceptive Acts or Practices - UDAP): This regulation prohibits unfair, deceptive, or abusive acts or practices by financial institutions, including failing to assist consumers in resolving fraudulent activities.
    
#     **Specific Regulation AA Clauses:**
    
#     The complaint raises concerns under Regulation AA, specifically:
    
#     * 12 CFR 1022.2(a) - Unfair Acts or Practices: The bank's failure to establish appropriate policies and procedures to prevent, detect, or remedy fraudulent activities may be considered an unfair act or practice.
#     * 12 CFR 1022.2(b) - Deceptive Acts or Practices: The bank's refusal to assist the consumer in resolving the fraudulent activity may be considered a deceptive act or practice.
#     * 12 CFR 1022.3 - Substantial Injury: The consumer has suffered a substantial injury due to the fraudulent activity, and the bank's failure to assist in resolving the issue has exacerbated the injury.
    
#     **Clear Resolution Path:**
    
#     Based on the regulatory protections and specific Regulation AA clauses, the following resolution path is recommended:
    
#     1. **File a Dispute:** The complainant should file a dispute with JPMorgan Chase & Co. and the other involved bank, XXXX XXXX XXXX, under Regulation E, citing unauthorized electronic fund transfers and requesting a refund of the stolen money ($XXXX).
#     2. **Contact Regulatory Agencies:** The complainant should contact the Consumer Financial Protection Bureau (CFPB) and the Office of the Comptroller of the Currency (OCC) to report the fraudulent activity and the banks' failure to assist in resolving the issue. The CFPB and OCC can investigate and take enforcement action against the banks if necessary.
#     3. **Request Investigation:** The complainant should request that the banks investigate the fraudulent activity and take corrective action to prevent future occurrences.
#     4. **Seek Refund and Compensation:** The complainant should seek a refund of the stolen money ($XXXX) and compensation for any additional losses or damages incurred due to the banks' failure to assist in resolving the issue.
    
#     **Steps for the Complainant:**
    
#     1. File a dispute with JPMorgan Chase & Co. and XXXX XXXX XXXX under Regulation E.
#     2. Contact the CFPB and OCC to report the fraudulent activity and the banks' failure to assist in resolving the issue.
#     3. Request an investigation into the fraudulent activity and corrective action to prevent future occurrences.
#     4. Seek a refund of the stolen money ($XXXX) and compensation for any additional losses or damages incurred.
    
#     By following this resolution path, the complainant can seek redress for the fraudulent activity and the banks' failure to assist in resolving the issue, while also ensuring that the banks take corrective action to prevent future occurrences.
#     """
#     email_formation_class_obj = email_formation_class()
#     email_grading_class_obj   = email_grading_class()
    
#     regulation_email_chain    = email_formation_class_obj.formulate_reg_email_chain(  Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Solutions,Feedback, llm)
#     reg_email_response        = regulation_email_chain.invoke(Complaint_Text)
#     email_grader_chain        = email_grading_class_obj.regulation_email_grading_chain(llm, Complaint_ID)
#     reg_email_grade           = email_grader_chain.invoke(
#                                                             {
#                                                                 "complaint": Complaint_Text,  
#                                                                 "Total_Regulations": Total_Regulations,  
#                                                                 "Regulation_Names": Regulation_Names ,
#                                                                 "email_response": reg_email_response
#                                                             }
#                                                          )
        
#     Complaint_ID      = '6781176'
#     Complaint_Text    = "I am not happy paying flood fees. I know it is mandatory but it is too much."
#     Company           = "JPMORGAN CHASE & CO."
#     State             = "TX"
#     Zip_Code          = "75080"
#     Total_Regulations = 0
#     Feedback          = "" 
#     no_regulation_email_chain     = email_formation_class_obj.formulate_noreg_email_chain(  Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Feedback, llm)
#     no_reg_email_response         = no_regulation_email_chain.invoke(Complaint_Text)
#     no_reg_email_grader_chain     = email_grading_class_obj.non_regulation_email_grading_chain(llm, Complaint_ID)
#     no_reg_email_grade            = no_reg_email_grader_chain.invoke(
#                                                                       {
#                                                                         "complaint": Complaint_Text,  
#                                                                         "Total_Regulations": Total_Regulations,  
#                                                                         "Regulation_Names": Regulation_Names ,
#                                                                         "email_response": no_reg_email_response
#                                                                       }
#                                                                      )