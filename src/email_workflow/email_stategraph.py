import os
import logging
import markdown
from typing import TypedDict, Optional

from langgraph.graph          import StateGraph, END, START
from langchain_core.runnables import RunnableLambda

from logger                   import Logger

import warnings
warnings.filterwarnings('ignore')

class email_stategraph_class:
    def __init__(self):
        self.logger_obj                              = Logger()
        
    def get_stategraph(self, regulation_email_chain, email_grader_chain, no_regulation_email_chain, no_reg_email_grader_chain):
        class EmailWorkflowState(TypedDict):
            Complaint_ID: str
            Complaint_Text: str
            Company: str
            State: str
            Zip_Code: str
            Total_Regulations: int
            Regulation_Names: str
            Feedback: str
            Solutions: Optional[str]
            binary_score: Optional[str]
            Email_Response: Optional[str]
            Email_HTML: Optional[str]
            Iteration_Count: int 
        
        # Function: Select Email Chain
        def choose_email_chain(state: EmailWorkflowState):
            Complaint_ID  = state["Complaint_ID"]
            print("Checking the Total Regulations for Complaint ID:", Complaint_ID)
            logging.info(f"Checking the Total Regulations for Complaint ID: {Complaint_ID}")
        
            Total_Regulations = state["Total_Regulations"]  # Fetching the regulation count
            print("Total Regulations Found:", Total_Regulations)
            logging.info(f"Total Regulations Found: {Total_Regulations}")
        
            if Total_Regulations > 0:
                print("Complaint falls under regulations. Moving to: `generate_email`")
                logging.info("Complaint falls under regulations. Moving to: `generate_email`")
                return "Total_Regulations>0"
            else:
                print("No applicable regulations found. Treating as Expression of Dissatisfaction. Moving to: `generate_noreg_email`")
                logging.info("No applicable regulations found. Treating as Expression of Dissatisfaction. Moving to: `generate_noreg_email`")
                return "Total_Regulations=0"
            
        # Function: Generate Email (Regulated)
        def generate_email(state: EmailWorkflowState):
            Complaint_Text = state["Complaint_Text"]
            logging.info(f"Generating regulated email for Complaint Text: {Complaint_Text}")
        
            # Generating email using EMAIL_CHAIN
            email_response = regulation_email_chain.invoke(Complaint_Text).content
            print("Email Generated Successfully.")
            logging.info("Email Generated Successfully.")
        
            # Converting response to HTML
            html_output = markdown.markdown(f"# **Generated Email**\n\n{email_response}")
            print("Email Converted to HTML Format.")
            logging.info("Email Converted to HTML Format.")
        
            # Returning response
            return {"Email_Response": email_response, "Email_HTML": html_output}
            
        # Function: Grade Email
        def grade_email(state: EmailWorkflowState):
            Complaint_Text    = state["Complaint_Text"]
            Total_Regulations = state["Total_Regulations"]
            Regulation_Names  = state["Regulation_Names"]
            Email_Response    = state["Email_Response"]
            Iteration_Count   = state.get("Iteration_Count", 0)
        
            print("Grading Email for Complaint ID:", state["Complaint_ID"])
            logging.info(f"Grading Email for Complaint ID: {state['Complaint_ID']}")
            
            Iteration_Count += 1
            state["Iteration_Count"] = Iteration_Count  
            
            # Invoke email grading
            email_grade = email_grader_chain.invoke(
                                                        {
                                                            "complaint": Complaint_Text,  
                                                            "Total_Regulations": Total_Regulations,  
                                                            "Regulation_Names": Regulation_Names,
                                                            "email_response": Email_Response
                                                        }
                                                    )
        
            binary_score = email_grade.binary_score.lower()
            Feedback     = email_grade.Feedback
        
            print("Grading Completed. Decision:", email_grade.binary_score.upper())
            logging.info(f"Grading Completed. Decision: {email_grade.binary_score.upper()}")
        
            if email_grade.binary_score.lower() == "yes":
                print("Email approved. Moving to END state.\n")
                logging.info("Email approved. Moving to END state.")
                return {"binary_score": binary_score, "Feedback": Feedback, "Iteration_Count":Iteration_Count}
            else:
                print("Email needs improvement. Providing feedback.")
                logging.info("Email needs improvement. Providing feedback.")
                return {"binary_score": binary_score, "Feedback": Feedback, "Iteration_Count":Iteration_Count}
            
        ## Rerouting Email
        def reroute_email(state: EmailWorkflowState):
        
            binary_score    = state["binary_score"]
            Feedback        = state["Feedback"]
            Iteration_Count = state["Iteration_Count"] 
        
            if binary_score.lower() == "yes":
                print("Email is fine. Proceeding to END.")
                return "Email_Is_Fine"
        
            if Iteration_Count > 2:
                print("Email is fine. Proceeding to END.")
                return "Email_Is_Fine"
        
            else:
                print("Email is not fine. Rewriting email.")
                return "Email_Is_Not_Fine"
            
        # Function: Generate Email (No Regulations)
        def generate_noreg_email(state: EmailWorkflowState):
            Complaint_ID   = state["Complaint_ID"]
            Complaint_Text = state["Complaint_Text"]
        
            print("\nGenerating Non-Regulated Complaint Email for Complaint ID:", Complaint_ID)
            logging.info(f"Generating Non-Regulated Complaint Email for Complaint ID: {Complaint_ID}")
        
            # Generating email using NOREG_EMAIL_CHAIN
            email_response = no_regulation_email_chain.invoke(Complaint_Text).content
        
            print("Non-Regulated Email Generated Successfully.")
            logging.info("Non-Regulated Email Generated Successfully.")
        
            # Converting response to HTML
            html_output = markdown.markdown(f"# **Generated Email**\n\n{email_response}")
        
            print("Email Converted to HTML Format.")
            logging.info("Email Converted to HTML Format.")
        
            print("Moving to: 'grade_noreg_email'")
            logging.info("Moving to: 'grade_noreg_email'")
        
            # Returning response
            return {"Email_Response": email_response, "Email_HTML": html_output}

        # Function: Grade No Regulation Email
        def grade_noreg_email(state: EmailWorkflowState):
            Complaint_ID    = state["Complaint_ID"]
            Complaint_Text  = state["Complaint_Text"]
            Email_Response  = state["Email_Response"]
            Iteration_Count = state.get("Iteration_Count", 0)
        
            print("\nGrading No-Regulation Email for Complaint ID:", Complaint_ID)
            logging.info(f"Grading No-Regulation Email for Complaint ID: {Complaint_ID}")
            
            Iteration_Count += 1
            state["Iteration_Count"] = Iteration_Count  
        
            # Invoke email grading
            email_grade     = no_reg_email_grader_chain.invoke(
                                                                {
                                                                    "complaint": Complaint_Text,  
                                                                    "email_response": Email_Response
                                                                }
                                                          )
            
            binary_score    = email_grade.binary_score.lower()
            Feedback        = email_grade.Feedback
        
            print("Grading Completed. Decision:", email_grade.binary_score.upper())
            logging.info(f"Grading Completed for Complaint ID {Complaint_ID}. Decision: {email_grade.binary_score.upper()}")
        
            if binary_score == "yes":
                print("No-Reg Email approved. Moving to END state.\n")
                logging.info(f"No-Reg Email for Complaint ID {Complaint_ID} approved. Moving to END state.")
                return {"binary_score": binary_score, "Feedback": Feedback, "Iteration_Count":Iteration_Count}
            else:
                print("No-Reg Email needs improvement. Providing feedback.")
                logging.info(f"No-Reg Email for Complaint ID {Complaint_ID} needs improvement. Providing feedback.")
                return {"binary_score": binary_score, "Feedback": Feedback, "Iteration_Count":Iteration_Count}
            

        # Function: Reroute No Regulation Email
        def reroute_noreg_email(state: EmailWorkflowState):
        
            binary_score    = state["binary_score"]
            Feedback        = state["Feedback"]
            Iteration_Count = state["Iteration_Count"] 
        
            if binary_score.lower() == "yes":
                print("Email is fine. Proceeding to END.")
                return "Email_Is_Fine"
        
            if Iteration_Count > 2:
                print("Email is fine. Proceeding to END.")
                return "Email_Is_Fine"
        
            else:
                print("Email is not fine. Rewriting email.")
                return "Email_Is_Not_Fine"
                    
            
            
        print("Compiling a workflow.")
        logging.info("Compiling a workflow.")
        workflow = StateGraph(EmailWorkflowState)
        
        workflow.add_conditional_edges(START, choose_email_chain,  
                                           {
                                               "Total_Regulations>0": "generate_email",
                                               "Total_Regulations=0": "generate_noreg_email"
                                           }
                                      )
        
        workflow.add_node("generate_email", RunnableLambda(generate_email))
        workflow.add_node("grade_email", RunnableLambda(grade_email))
        workflow.add_edge("generate_email", "grade_email")
        workflow.add_conditional_edges("grade_email", reroute_email,  
                                           {
                                               "Email_Is_Fine": END,
                                               "Email_Is_Not_Fine": "generate_email"
                                           }
                                      )
        
        workflow.add_node("generate_noreg_email", RunnableLambda(generate_noreg_email))
        workflow.add_node("grade_noreg_email", RunnableLambda(grade_noreg_email))
        workflow.add_edge("generate_noreg_email", "grade_noreg_email")
        workflow.add_conditional_edges("grade_noreg_email", reroute_noreg_email,  
                                           {
                                               "Email_Is_Fine": END,
                                               "Email_Is_Not_Fine": "generate_noreg_email"
                                           }
                                       )
        
        email_app = workflow.compile()
        print("Completed compiling a workflow.")
        logging.info("Completed compiling a workflow.")
        
        return email_app
            
# if __name__ == "__main__":
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from email_formation import email_formation_class
#     from email_grading import email_grading_class
    
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
#     email_formation_class_obj    = email_formation_class()
#     email_grading_class_obj      = email_grading_class()
#     email_stategraph_class_obj   = email_stategraph_class()
    
#     regulation_email_chain       = email_formation_class_obj.formulate_reg_email_chain(  Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Solutions,Feedback, llm)
#     reg_email_response           = regulation_email_chain.invoke(Complaint_Text)
#     email_grader_chain           = email_grading_class_obj.regulation_email_grading_chain(llm, Complaint_ID)
    
#     no_regulation_email_chain    = email_formation_class_obj.formulate_noreg_email_chain(Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Feedback, llm)
#     no_reg_email_response        = no_regulation_email_chain.invoke(Complaint_Text)
#     no_reg_email_grader_chain    = email_grading_class_obj.non_regulation_email_grading_chain(llm, Complaint_ID)
    

#     email_app                    = email_stategraph_class_obj.get_stategraph(regulation_email_chain, email_grader_chain, no_regulation_email_chain, no_reg_email_grader_chain)
       
    
#     result1                       = email_app.invoke(
#                                                         {
#                                                             "Complaint_ID": Complaint_ID,
#                                                             "Complaint_Text": Complaint_Text,
#                                                             "Company": Company,
#                                                             "State": State,
#                                                             "Zip_Code": Zip_Code,
#                                                             "Total_Regulations": Total_Regulations,
#                                                             "Regulation_Names": Regulation_Names,
#                                                             "Feedback": Feedback
#                                                         }
#                                                    )  
    
#     Complaint_ID      = '6781176'
#     Complaint_Text    = "I am not happy paying flood fees. I know it is mandatory but it is too much."
#     Company           = "JPMORGAN CHASE & CO."
#     State             = "TX"
#     Zip_Code          = "75080"
#     Total_Regulations = 0
#     Feedback          = "" 


#     result2                       = email_app.invoke(
#                                                         {
#                                                             "Complaint_ID": Complaint_ID,
#                                                             "Complaint_Text": Complaint_Text,
#                                                             "Company": Company,
#                                                             "State": State,
#                                                             "Zip_Code": Zip_Code,
#                                                             "Total_Regulations": Total_Regulations,
#                                                             "Regulation_Names": Regulation_Names,
#                                                             "Feedback": Feedback
#                                                         }
#                                                    )  

    
    
    
    
    
    
    
    
    
    