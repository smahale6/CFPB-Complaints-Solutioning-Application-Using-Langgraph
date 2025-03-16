from logger import Logger
import os
import logging
from pydantic import BaseModel, Field
import warnings
warnings.filterwarnings('ignore')

from langchain_core.tools import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


class email_formation_class:
    def __init__(self):
        self.logger_obj                 = Logger()
        
    def formulate_reg_email_chain(self, Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Solutions,Feedback, llm):
        logging.info(f"Generating a regulation email chain for the Complaint Id: {Complaint_ID}.")
        print(f"Generating a regulation email chain for the Complaint Id: {Complaint_ID}.")
        
        formulate_email_prompt_template = """
                                                  You are a  customer care representative for this company given below.
                                                  - **Company:** {Company}
                                                  You are an expert in summarizing legal texts and formulating an email in simple language which is easy for normal day to day people to understand.
                                                  Your task is to formulate an email on your company's behalf to a customer who has placed a complaint on the CFPB website.
                                                  
                                                  ## **Customer Complaint:**  
                                                  "{complaint}"
                                            
                                                  The customer is from the state and zip code given below.
                                                    - **State:** {State}
                                                    - **Zip Code:** {ZIP_code}
                                            
                                                  The complaint was reviewed by a **CFPB regulation experts** of who specialized in their respective CFPB regulations and identified
                                                  the regulations this complaint belonged to. So the complaint was classified in the regulations given below.
                                            
                                                    ## **Regulation Details:**  
                                                    - **Total Regulations:** {Total_Regulations}
                                                    - **Regulation Names:** {Regulation_Names}
                                            
                                                  The **CFPB regulation experts** later on provided the solutions for the complaint based on their respective regulations. 
                                                  The solutions are given below
                                                    ## **Complaint Solution:** 
                                                    {Solutions} 
                                            
                                                  Take the feedback given by **CFPB regulation expert supervisor's** feedback into consideration if he/she has any feedback.
                                                    ## **Feedback:** 
                                                    {Feedback} 
                                                    
                                                  Read the solutions, formulate your email by picking contents of the solution. The email should summarize the solutions provided
                                                  The email should include the following:
                                                  1. Greet the customer well and express your concerns and gratitude.
                                                  2. Start the email by mentioning which CFPB regulations this email belongs to and the clauses of the regulation which you can get from the solutions.
                                                  3. Then write the rest of the email by providing solutions that addresses all the concerns of the customer.
                                                     - Provide the list of steps, actions and investigations the company will perform. But be confident that your comapny follows all the laws.
                                                     - Provide the steps and actions expected out of the customer.
                                            
                                                  Just display the email and not the summary.
                                            
                                            """
        
        EMAIL_PROMPT = PromptTemplate(
            template=formulate_email_prompt_template,
            input_variables=["Company", "complaint", "State", "ZIP_code", "Total_Regulations", "Regulation_Names", "Solutions", "Feedback"]
        )
        
        regulation_email_chain = (
                                    {
                                        "Company": lambda _: Company,
                                        "complaint": RunnablePassthrough(),
                                        "State": lambda _: State,
                                        "ZIP_code": lambda _: Zip_Code,
                                        "Total_Regulations": lambda _: Total_Regulations,
                                        "Regulation_Names": lambda _: Regulation_Names,
                                        "Solutions": lambda _: Solutions,
                                        "Feedback": lambda _: Feedback,
                                    }
                                    | EMAIL_PROMPT
                                    | llm
                                )
        logging.info(f"Completed generating a regulation email chain for the Complaint Id: {Complaint_ID}.")
        print(f"Completed generating a regulation email chain for the Complaint Id: {Complaint_ID}.")
        
        return regulation_email_chain
        
        
        
    def formulate_noreg_email_chain(self, Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Feedback, llm):
        logging.info(f"Generating a non regulation email chain for the Complaint Id: {Complaint_ID}.")
        print(f"Generating a non regulation email chain for the Complaint Id: {Complaint_ID}.")

        formulate_email_prompt_template = """
              You are a  customer care representative for this company given below.
              - **Company:** {Company}
              You are an expert in summarizing legal texts and formulating an email in simple language which is easy for normal day to day people to understand.
              Your task is to formulate an email on your company's behalf to a customer who has placed a complaint on the CFPB website.
              
              ## **Customer Complaint:**  
              "{complaint}"
        
              The customer is from the state and zip code given below.
                - **State:** {State}
                - **Zip Code:** {ZIP_code}
        
              The complaint was reviewed by a **CFPB regulation experts** of who specialized in their respective CFPB regulations and none of the
              experts could classify this complaint under any regulations. So this complaint is not a complaint but an **Expression of Dissatisfaction**
        
              The **CFPB regulation experts** have not provided solutions for this as it does not fall under any regulations.
        
              Take the feedback given by **CFPB regulation expert supervisor's** feedback into consideration if he/she has any feedback.
                ## **Feedback:** 
                {Feedback} 
                
              Formulate your email response to the customer
              The email should include the following:
              1. Greet the customer well and express your concerns and gratitude.  
              2. Since you cannot tie this complaint to any CFPB regulations, be kind to the customer and explain why his complaint not 
                 exactly a complaint but an **Expression of Dissatisfaction**.
              3. In rest of the email, provide some firendly recommendations and suggestions to address his greviences within the CFPB framework. 
        
              Just display the email and not the summary.
        
        """
        
        NOREG_EMAIL_PROMPT = PromptTemplate(
            template=formulate_email_prompt_template,
            input_variables=["Company", "complaint", "State", "ZIP_code","Feedback"]
        )
        
        no_regulation_email_chain = (
                                        {
                                            "Company": lambda _: Company,
                                            "complaint": RunnablePassthrough(),
                                            "State": lambda _: State,
                                            "ZIP_code": lambda _: Zip_Code,
                                            "Feedback": lambda _: Feedback,
                                        }
                                        | NOREG_EMAIL_PROMPT
                                        | llm
                                    )
        return no_regulation_email_chain


        
        
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
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
#     regulation_email_chain    = email_formation_class_obj.formulate_reg_email_chain( Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Solutions,Feedback, llm)
#     reg_email_response = regulation_email_chain.invoke(Complaint_Text)
    
#     Complaint_ID      = '6781176'
#     Complaint_Text    = "I am not happy paying flood fees. I know it is mandatory but it is too much."
#     Company           = "JPMORGAN CHASE & CO."
#     State             = "TX"
#     Zip_Code          = "75080"
#     Total_Regulations = 0
#     Feedback          = "" 
#     no_regulation_email_chain     = email_formation_class_obj.formulate_noreg_email_chain(  Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Feedback, llm)
#     no_reg_email_response         = no_regulation_email_chain.invoke(Complaint_Text)