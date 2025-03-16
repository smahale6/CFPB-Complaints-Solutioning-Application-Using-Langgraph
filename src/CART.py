import os
import time
import pandas as pd
import numpy as np
import pyodbc
import logging
from dotenv                                       import load_dotenv
from datetime                                     import datetime
from langchain_huggingface                        import HuggingFaceEmbeddings
from langchain_groq                               import ChatGroq

from logger                                       import Logger
from regulation_text_ingestion                    import regulation_ingestion_class
from database_activity                            import database_activity_class

from complaint_workflow.fetch_complaints_api      import fetch_compalints_class
from complaint_workflow.complaint_summarization   import complaint_summarization_chain_class
from complaint_workflow.document_grading          import document_grading_class
from complaint_workflow.complaint_classification  import complaint_clasification_class
from complaint_workflow.complaint_solution        import solution_extraction_class
from complaint_workflow.solution_grading          import solution_grading_class
from complaint_workflow.complaint_stategraph      import complaint_stategraph_class

from email_workflow.email_formation               import email_formation_class
from email_workflow.email_grading                 import email_grading_class
from email_workflow.email_stategraph              import email_stategraph_class




import warnings
warnings.filterwarnings('ignore')


class cart_intersect_class:
    def __init__(self):
        load_dotenv() # Load environment variables from the .env file
        self.TAVILY_API_KEY                              = os.getenv("TAVILY_API_KEY")
        self.GROQ_API_KEY                                = os.getenv("GROQ_API_KEY")
        self.HUGGINGFACE_API_KEY                         = os.getenv("HUGGINGFACE_API_KEY")
        self.employee_id                                 = os.getenv("EMPLOYEE_ID")
        self.cart_path                                   = os.path.dirname(os.path.abspath("CART.py"))
        self.SQL_USER_NAME                               = os.getenv("SQL_USER_NAME")
        self.SQL_PASSWORD                                = os.getenv("SQL_PASSWORD")
        self.version                                     = 2.0
        self.regulations_path                            = self.cart_path  +'\\regulations\\'
        self.vector_db_path                              = self.cart_path + '\\vector_db\\'
        self.fetch_compalints_class_obj                  = fetch_compalints_class()
        self.regulation_ingestion_class_obj              = regulation_ingestion_class()
        self.database_activity_class_obj                 = database_activity_class()  
        self.complaint_summarization_chain_class_obj     = complaint_summarization_chain_class()
        self.document_grading_class_obj                  = document_grading_class()
        self.complaint_clasification_class_obj           = complaint_clasification_class()
        self.solution_extraction_class_obj               = solution_extraction_class()
        self.solution_grading_class_obj                  = solution_grading_class()
        self.complaint_stategraph_class_obj              = complaint_stategraph_class()
        self.email_formation_class_obj                   = email_formation_class()
        self.email_grading_class_obj                     = email_grading_class()
        self.email_stategraph_class_obj                  = email_stategraph_class()
        self.regulation_ingestion_dict                   = {'Reg_B':True,'Reg_C':True,'Reg_D':True,'Reg_E':True,'Reg_F':True,
                                                            'Reg_G':True,'Reg_H':True,'Reg_I':True,'Reg_J':True,'Reg_K':True,
                                                            'Reg_L':True,'Reg_M':True,'Reg_N':True,'Reg_O':True,'Reg_P':True,
                                                            'Reg_V':True,'Reg_X':True,'Reg_Z':True,
                                                            'Reg_CC':True,'Reg_DD':True,'Reg_AA':True}
        self.logger_obj                                  = Logger() 


    def review_single_complaint(self,complaint_id, complaint, company, state, zip_code, Product, Sub_Product , llm, embedding_function, cart_log_id, employee_id):
        reviewed_complaint_df                            = pd.DataFrame({'Complaint_ID': [complaint_id], 
                                                                       'Complaint_Text': [complaint], 
                                                                       'Company': [company], 
                                                                       'State': [state], 
                                                                       'Zip_Code': [zip_code],
                                                                       'Product': [Product],
                                                                       'Sub_Product': [Sub_Product]})
        complaint_rewriter                               = self.complaint_summarization_chain_class_obj.get_summarization_chain(llm)
        summarized_complaint                             = complaint_rewriter.invoke({"complaint": complaint})
        reviewed_complaint_df['Summarized_Complaint']    = summarized_complaint
         
        for reg_name in self.regulation_ingestion_dict.keys():
            print(f"Running the state graph for {reg_name}")
            logging.info(f"Running the state graph for {reg_name}")
            retriever_tool, retriever     = self.document_grading_class_obj.get_document_retirever(reg_name, self.vector_db_path, embedding_function)
            document_grade_chain          = self.document_grading_class_obj.get_document_grade_chain(reg_name, llm)
            doc_classification_chain      = self.complaint_clasification_class_obj.get_doc_classification_chain(reg_name, retriever_tool, llm)
            tavily_search_tool            = self.complaint_clasification_class_obj.get_tavily_search_tool(self.TAVILY_API_KEY, total_tavily_searches = 3)
            web_classification_chain      = self.complaint_clasification_class_obj.get_web_classification_chain(reg_name, tavily_search_tool, llm)
            doc_solution_chain            = self.solution_extraction_class_obj.get_doc_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company, Product, Sub_Product) 
            web_solution_chain            = self.solution_extraction_class_obj.get_web_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company, Product, Sub_Product)
            doc_hallucinations_grader     = self.solution_grading_class_obj.get_doc_hallucination_grading_chain(reg_name, llm)
            web_hallucinations_grader     = self.solution_grading_class_obj.get_web_hallucination_grading_chain(reg_name, llm)
            complaint_app                 = self.complaint_stategraph_class_obj.get_stategraph(complaint_rewriter, retriever, document_grade_chain, doc_classification_chain, web_classification_chain, doc_solution_chain, doc_hallucinations_grader, web_solution_chain, web_hallucinations_grader, tavily_search_tool)
            result                        = complaint_app.invoke({
                                                                    "summarized_complaint": summarized_complaint,
                                                                    "company": company,
                                                                    "state": state,
                                                                    "zip_code": zip_code,
                                                                    "Product": Product,
                                                                    "Sub_Product": Sub_Product
                                                                 })
            
            reviewed_complaint_df[reg_name + '_Classification']  = result['classification']
            reviewed_complaint_df[reg_name + '_Explanation']     = result['explanation']
            reviewed_complaint_df[reg_name + '_Solution']        = result['solution']
            reviewed_complaint_df[reg_name + '_Solution_Source'] = result['solution_source']
            print(f"Completed running the state graph for {reg_name}")
            logging.info(f"Completed running the state graph for {reg_name}")
        reviewed_complaint_df['Loaded_By']                       = employee_id
        reviewed_complaint_df['Cart_Log_Id']                     = cart_log_id
        return reviewed_complaint_df
    
    
    def review_bulk_complaints(self, unreviewed_complaints_df, conn, cart_log_id, llm, embedding_function):
        query = "SELECT TOP 0 * FROM [Cart2.0].[dbo].[cart_cfpb_complaints_reg_stage]"
        reviewed_complaint_df_final = pd.read_sql_query(query, conn)
    
        regulations = list(self.regulation_ingestion_dict.keys())
        # Ensure regulation columns exist in case DataFrame is empty
        for reg in regulations:
            for suffix in ["_Classification", "_Explanation", "_Solution", "_Solution_Source"]:
                col_name = reg + suffix
                if col_name not in reviewed_complaint_df_final.columns:
                    reviewed_complaint_df_final[col_name] = None  # Ensuring column presence
    
        if unreviewed_complaints_df.empty:
            print("No complaints to review.")
            logging.info("No complaints to review.")
            return reviewed_complaint_df_final  # Return empty but structured DataFrame
    
        for _, row in unreviewed_complaints_df.iterrows():
            complaint_id = row["Complaint_ID"]
            complaint    = row["Complaint_Text"]
            company      = row["Company"]
            state        = row["State"]
            zip_code     = row["ZIP_Code"]
            Product      = row["Product"]
            Sub_Product  = row["Sub_Product"]
    
            print(f"Processing Complaint_ID: {complaint_id}")
            logging.info(f"Processing Complaint_ID: {complaint_id}")
    
            if len(complaint.strip()) > 0:
                reviewed_complaint_df = self.review_single_complaint(complaint_id, complaint, company, state, zip_code, Product, Sub_Product , llm, embedding_function, cart_log_id, self.employee_id)
                #############################################################Loading Tagged Complaints################################################################################################
                tagged_complaints_stage_table = '[dbo].[cart_cfpb_complaints_reg_stage]'
                self.database_activity_class_obj.load_reviewed_complaints(conn, reviewed_complaint_df, tagged_complaints_stage_table)

            else:
                empty_data = {
                                "Complaint_ID": complaint_id,
                                "Complaint_Text": complaint,
                                "Company": company,
                                "State": state,
                                "Zip_Code": zip_code,
                                "Product": Product,
                                "Sub_Product": Sub_Product,
                                "Summarized_Complaint": None,
                                "Total_Tags": None,
                                "Tagged_Regulations": None,
                                "Loaded_By": self.employee_id,
                                "Cart_Log_Id": cart_log_id,
                            }
                
                # Fill classification columns with "no" and explanations as empty
                for reg in regulations:
                    empty_data[f"{reg}_Classification"] = "no"
                    empty_data[f"{reg}_Explanation"] = "Complaint empty."
                    empty_data[f"{reg}_Solution"] = "No solution required."
                    empty_data[f"{reg}_Solution_Source"] = None
    
                reviewed_complaint_df = pd.DataFrame([empty_data])
    
            reviewed_complaint_df_final = pd.concat([reviewed_complaint_df_final, reviewed_complaint_df], ignore_index=True)
    
        print("Completed bulk complaint review.")
        return reviewed_complaint_df_final


    def formulate_single_email(self,llm, Complaint_ID, Complaint_Text, Company, State, Zip_Code, Total_Regulations, Regulation_Names, Solutions, Feedback = ""):
        regulation_email_chain       = self.email_formation_class_obj.formulate_reg_email_chain(  Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Solutions,Feedback, llm)
        email_grader_chain           = self.email_grading_class_obj.regulation_email_grading_chain(llm, Complaint_ID)
        
        no_regulation_email_chain    = self.email_formation_class_obj.formulate_noreg_email_chain(Complaint_ID,Complaint_Text,Company,State,Zip_Code,Total_Regulations,Regulation_Names,Feedback, llm)
        no_reg_email_grader_chain    = self.email_grading_class_obj.non_regulation_email_grading_chain(llm, Complaint_ID)
        
        email_app                    = self.email_stategraph_class_obj.get_stategraph(regulation_email_chain, email_grader_chain, no_regulation_email_chain, no_reg_email_grader_chain)
        
        result                       = email_app.invoke(
                                                            {
                                                                "Complaint_ID": Complaint_ID,
                                                                "Complaint_Text": Complaint_Text,
                                                                "Company": Company,
                                                                "State": State,
                                                                "Zip_Code": Zip_Code,
                                                                "Total_Regulations": Total_Regulations,
                                                                "Regulation_Names": Regulation_Names,
                                                                "Feedback": Feedback
                                                            }, {"recursion_limit": 99999}
                                                       )  
        
        print(f"Generating the email dataframe for Complaint ID: {Complaint_ID}")
        logging.info(f"Generating the email dataframe for Complaint ID: {Complaint_ID}")
        result_dict                  = dict(result)
        result_df                    = pd.DataFrame.from_dict(result_dict, orient="index").T
        
        email_df                     = result_df.loc[:,['Complaint_ID','Feedback','Email_Response','Email_HTML']]
        print(f"Completed generating the email dataframe for Complaint ID: {Complaint_ID}")
        logging.info(f"Completed generating the email dataframe for Complaint ID: {Complaint_ID}")
        
        return email_df
        


    def formulate_bulk_email(self, conn, llm, cart_log_id):
        print(f"Fetching complaints from cart_cfpb_complaints_reg_summarized for Cart_Log_Id: {cart_log_id}")
        logging.info(f"Fetching complaints from cart_cfpb_complaints_reg_summarized for Cart_Log_Id: {cart_log_id}")
    
        # **Step 1: Fetch Data**
        query         = "SELECT * FROM [Cart2.0].[dbo].[cart_cfpb_complaints_reg_summarized] where Complaint_ID not in (Select Complaint_ID from [dbo].[cart_email])"
        summarized_df = pd.read_sql_query(query, conn)
    
        if summarized_df.empty:
            print(f"No complaints found for Cart_Log_Id: {cart_log_id}")
            logging.info(f"No complaints found for Cart_Log_Id: {cart_log_id}")
            return pd.DataFrame()  # Return an empty DataFrame if no data
    
        print(f"Processing {len(summarized_df)} complaints...")
        logging.info(f"Processing {len(summarized_df)} complaints...")
    
        # **Step 2: Process Each Complaint**
        email_df_list = []  # Store individual email DataFrames
    
        for index, row in summarized_df.iterrows():
            print(f"Processing Complaint_ID: {row['Complaint_ID']}")
            logging.info(f"Processing Complaint_ID: {row['Complaint_ID']}")
    
            # Call the `formulate_single_email` function for each complaint
            email_df = self.formulate_single_email(
                                                    llm,  # Assuming `self.llm` exists
                                                    row["Complaint_ID"],
                                                    row["Complaint_Text"],
                                                    row["Company"],
                                                    row["State"],
                                                    row["Zip_Code"],
                                                    row["Total_Regulations"],
                                                    row["Regulation_Names"],
                                                    row["Solutions"],
                                                    row.get("Feedback", "")  # Default to empty string if Feedback is missing
                                                )
            
            self.database_activity_class_obj.load_email(conn, email_df, cart_log_id, self.employee_id)
            email_df_list.append(email_df)
    
        # **Step 3: Combine Results into a Single DataFrame**
        final_email_df = pd.concat(email_df_list, ignore_index=True)
    
        print(f"Bulk email processing completed for Cart_Log_Id: {cart_log_id}")
        logging.info(f"Bulk email processing completed for Cart_Log_Id: {cart_log_id}")
    
        return final_email_df

        
        
        
    def run_cart(self,  company,  total_records, date_received_min, date_received_max, llm_model = 'Llama 3.2 3B (Preview) 8k'):
        start_time = time.time()
        
        ############################################################# Connecting to SQL Server ################################################################
        print("Connecting to SQL Server.")
        logging.info("Connecting to SQL Server.")
        server    = 'complaints-analytics.database.windows.net'  # e.g., 'localhost\SQLEXPRESS'
        database  = 'Cart2.0'  # e.g., 'CART_DB'
        driver    = '{ODBC Driver 17 for SQL Server}'  # Ensure you have the correct ODBC driver installed
        conn      = pyodbc.connect(
                                    f'DRIVER={driver};'
                                    f'SERVER={server};'
                                    f'DATABASE={database};'
                                    f'UID={self.SQL_USER_NAME};'
                                    f'PWD={self.SQL_PASSWORD};'
                                    'Encrypt=yes;'  # Ensure encryption is enabled for Azure SQL
                                    'TrustServerCertificate=no;'  # Recommended for security
                                    'Connection Timeout=60;'
                                 )
        print("Established  Connection to the CART Database in SQL Server.")
        logging.info("Established  Connection to the CART Database in SQL Server.")
        
           
        #############################################################Checking user permissions ################################################################
        user_info_df      = pd.read_sql_query(f"Select * from [dbo].[cart_user_profile] where Employee_id = '{self.employee_id }'",conn)
        if len(user_info_df) == 1:
            #user_title        = user_info_df.loc[:,'Title'][0]
            #user_first_name   = user_info_df.loc[:,'First_Name'][0]
            #user_last_name    = user_info_df.loc[:,'Last_Name'][0]
            permissions       = user_info_df.loc[:,'Permissions'][0]
        else:
            raise ValueError(("The employee id {} does not have the permissions to use the Complaints Analysis and Review Tool.".format(self.employee_id )))
       
        if permissions == 1:
            ############################################################# Connecting to LLM ################################################################
            print(f"Establishing connection with {llm_model} LLM...")
            logging.info(f"Establishing connection with {llm_model} LLM...")
    
            try:
                llm = ChatGroq(model_name = llm_model, temperature = 0.0, api_key = self.GROQ_API_KEY)
                print(f"Connected to {llm_model} LLM.")
                logging.info(f"Connected to {llm_model} LLM.")
            except Exception as e:
                logging.error(f"LLM Connection Failed: {str(e)}")
                print(f"LLM Connection Failed: {str(e)}")
                return None
            
            ############################################################# Embedding Model ################################################################################
            print("Fetching embedding model...")
            logging.info("Fetching embedding model...")
    
            try:
                embedding_function = HuggingFaceEmbeddings(
                                                                model_name="BAAI/bge-large-en-v1.5",
                                                                model_kwargs={"token": self.HUGGINGFACE_API_KEY}
                                                            )
                print("Embedding model fetched successfully.")
                logging.info("Embedding model fetched successfully.")
            except Exception as e:
                logging.error(f"Embedding Model Fetch Failed: {str(e)}")
                print(f"Embedding Model Fetch Failed: {str(e)}")
                return None
            
            ############################################################# Creating a Cart Log Entry ################################################################################################
            table_action        = "insert"
            update_column       = None
            update_column_value = None
            cart_log_id         = None
            cart_log_id         = self.database_activity_class_obj.cart_log_entry(conn,table_action,update_column,update_column_value,self.version,self.employee_id ,cart_log_id = None)
            
            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Complaint Workflow XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            
            #############################################################Fetching Complaints from CFPB###########################################################################################
            cart_cfpb_complaints_raw_df    = self.fetch_compalints_class_obj.get_cfpb_complaints(self.employee_id, cart_log_id, date_received_min, date_received_max, company, total_records)
            
            #############################################################Loading CFPB Complaints#################################################################################################
            cart_cfpb_complaints_raw_table = 'cart_cfpb_complaints_raw_stage'
            self.database_activity_class_obj.load_cfpb_raw_complaints_data(conn,cart_cfpb_complaints_raw_df,cart_cfpb_complaints_raw_table)
            
            table_action        = "update"
            update_column       = "Total_Complaints"
            update_column_value = len(cart_cfpb_complaints_raw_df)
            self.database_activity_class_obj.cart_log_entry(conn,table_action,update_column,update_column_value,self.version,self.employee_id ,cart_log_id)

            #############################################################Generating Untagged Complaints###########################################################################################
            unreviewed_complaints_stored_procedure = '[dbo].[uspload_cart_untagged_complaints]'
            self.database_activity_class_obj.generate_unreviewed_complaints(conn,unreviewed_complaints_stored_procedure)
            
            unreviewed_complaints_table  = '[dbo].[cart_untagged_complaints]'
            unreviewed_complaints_df     = self.database_activity_class_obj.import_unreviewed_complaints(conn,unreviewed_complaints_table )

            #####################################################Ingesting Regulation Data into Vector Stores##############################################################
            chunk_size    = 1000
            chunk_overlap = 200
            self.regulation_ingestion_class_obj.ingest_regulation_files(embedding_function, self.regulation_ingestion_dict, self.regulations_path, self.vector_db_path, chunk_size, chunk_overlap)
    
            ############################################################# Reviewing Complaints ############################################################################
            reviewed_complaint_df_final  = self.review_bulk_complaints( unreviewed_complaints_df, conn, cart_log_id, llm, embedding_function)
             
            self.database_activity_class_obj.generate_reviewed_complaints_summary(conn,stored_procedure = '[dbo].[uspload_cart_cfpb_complaints_reg_summary]')
            

            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Email Workflow XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            #####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#########
            final_email_df  = self.formulate_bulk_email(conn, llm, cart_log_id)
            
            self.database_activity_class_obj.refresh_complaints_solution_report(conn,stored_procedure = '[dbo].[uspload_rpt_cfpb_complaints]')
            
            #############################################################Updating CART Log Entry################################################################################################
            reviewed_complaints_table = '[dbo].[cart_cfpb_complaints_reg]'
            self.database_activity_class_obj.update_cart_log(conn,reviewed_complaints_table,cart_log_id,self.regulation_ingestion_dict,self.version,self.employee_id)
            
            
        else:
           print("You do not have the permissions to use the Complaints Analysis and Regulation Tool.")
        ############################################################### Ending the run ################################################################################
        conn.close()
        print("Connection to the CART Database in SQL Server has been closed.")
        # Total runtime calculation
        end_time = time.time()
        execution_time = round((end_time - start_time)/60, 2)
        print(f"CART Execution completed in {execution_time} minutes.")
        logging.info(f"CART Execution completed in {execution_time} minutes.")
        return reviewed_complaint_df_final
        
        
if __name__ == "__main__":
    company                        = "NAVY FEDERAL CREDIT UNION"#"BANK OF AMERICA, NATIONAL ASSOCIATION"
    total_records                  = 10
    date_received_min              = "2022-01-01"
    date_received_max              = "2022-12-31"
    cart_intersect_class_obj       = cart_intersect_class()
    reviewed_complaint_df_final    = cart_intersect_class_obj.run_cart( company, total_records, date_received_min, date_received_max, llm_model = 'llama3-70b-8192')
    
        
        
        
        
        