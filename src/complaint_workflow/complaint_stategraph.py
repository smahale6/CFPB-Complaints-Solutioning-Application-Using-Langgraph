import os
import logging
from pydantic import BaseModel, Field
from typing   import List,  Annotated, Literal, Sequence, TypedDict

from langgraph.graph          import StateGraph, END, START
from langgraph.prebuilt       import tools_condition
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts   import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from logger                   import Logger

import warnings
warnings.filterwarnings('ignore')


class complaint_stategraph_class:
    def __init__(self):
        self.logger_obj                              = Logger()
    
    def get_stategraph(self, complaint_rewriter, retriever, document_grade_chain, doc_classification_chain, web_classification_chain, doc_solution_chain, doc_hallucinations_grader, web_solution_chain, web_hallucinations_grader, tavily_search_tool):
        class ComplaintState(TypedDict):
            summarized_complaint: str
            company: str
            state: str
            zip_code: str
            Product: str
            Sub_Product: str
            retrieved_docs: list
            doc_relevance: str
            classification: str
            explanation: str
            solution: str
            retrieved_web_context: list  
            solution_source: str
            solution_valid: str
            retry_count: int  
            web_txt: str
            
            

            
        # Step 1: Retrieve Relevant Documents (First Node)
        def retrieve_documents(state: ComplaintState):
            print("Retrieving relevant documents for the complaint...")
            logging.info("Retrieving relevant documents for the complaint...")
            summarized_complaint = state["summarized_complaint"]
            company              = state["company"]
            state_location       = state["state"]
            zip_code             = state["zip_code"]
            Product              = state["Product"]
            Sub_Product          = state["Sub_Product"]
            retrieved_docs       = retriever.get_relevant_documents(summarized_complaint)
            print(f"Retrieved {len(retrieved_docs)} documents.")
            logging.info(f"Retrieved {len(retrieved_docs)} documents.")
            logging.info("Retrieving relevant documents for the complaint...")
            return {
                        "retrieved_docs": retrieved_docs,
                        "company": company,
                        "state": state_location,
                        "zip_code": zip_code,
                        "Product": Product,
                        "Sub_Product": Sub_Product
                    } 
        
        
        # Step 2: Grade Retrieved Documents
        def grade_documents(state: ComplaintState):
            print("Grading retrieved documents for relevance...")
            logging.info("Grading retrieved documents for relevance...")
            summarized_complaint = state["summarized_complaint"]
            retrieved_docs       = state["retrieved_docs"]
            if not retrieved_docs:
                print("No documents retrieved. Skipping grading.")
                logging.info("No documents retrieved. Skipping grading.")
                return {"doc_relevance": "no"}
            doc_txt              = "\n".join([doc.page_content for doc in retrieved_docs])
            grade_response       = document_grade_chain.invoke({
                                                                "document": doc_txt, 
                                                                "complaint": summarized_complaint
                                                               }).binary_score
            print("Document grading complete. Relevance:", grade_response)
            logging.info(f"Document grading complete. Relevance: {grade_response}")
            return {"doc_relevance": grade_response.lower()}
        
        
        # Step 3: **Conditional Edge** → Classify Using Doc or Web Based on Grade
        def route_classification(state: ComplaintState):
            print("Routing to classification step...")
            logging.info("Routing to classification step...")
            doc_relevance = state["doc_relevance"]
            if doc_relevance.lower() == "yes":
                print("Documents are relevant. Proceeding with document-based classification.")
                logging.info("Documents are relevant. Proceeding with document-based classification.")
                return "Docs_are_relevant"
            else:
                print("Documents are NOT relevant. Switching to web-based classification.")
                logging.info("Documents are NOT relevant. Switching to web-based classification.")
                return "Docs_are_not_relevant"

        # Step 4: Document-Based Classification
        def classify_complaint_doc(state: ComplaintState):
            print("Classifying complaint using documents...")
            logging.info("Classifying complaint using documents...")
            summarized_complaint    = state["summarized_complaint"]
            classification_response = doc_classification_chain.invoke(summarized_complaint)
        
            classification          = classification_response.Answer.lower()
            explanation             = classification_response.Explanation
            
            print(f"Document-based classification complete.")
            logging.info(f"Document-based classification complete.")
            if classification == 'yes':
                return {"classification": classification, "explanation": explanation}
            else:
                return {
                        "classification": classification,
                        "explanation": explanation,
                        "solution": "No solution required.",
                        "solution_source": "None",
                        "solution_valid": "N/A"  
                       }

        # Step 5: Routing Classification
        def route_doc_classification(state: ComplaintState):
            classification = state["classification"].lower()
            if classification.lower() == "no":
                print("Classification is 'No'. Ending process.")
                logging.info("Classification is 'No'. Ending process.")
                return "Classification  = No"  
            else:
                print("Classification is 'Yes'. Proceeding to grade document solution.")
                logging.info("Classification is 'Yes'. Proceeding to grade document solution.")
                return "Classification  = Yes"
        
        
        # Step 6: Web-Based Classification
        def classify_complaint_web(state: ComplaintState):
            print("Classifying complaint using web search...")
            logging.info("Classifying complaint using web search...")
            summarized_complaint    = state["summarized_complaint"]
            classification_response = web_classification_chain.invoke(summarized_complaint)
            
            classification = classification_response.Answer.lower()
            explanation = classification_response.Explanation
            
            print(f"Web-based classification complete.")
            logging.info(f"Web-based classification complete.")
            print(f"Classification = {classification}.")
            logging.info(f"Classification = {classification}.")
            if classification == 'yes':
                return {"classification": classification, "explanation": explanation}
            else:
                return {
                        "classification": classification,
                        "explanation": explanation,
                        "solution": "No solution required.",
                        "solution_source": "None",
                        "solution_valid": "N/A"  
                       }

        # Step 7: Web-Based Classification
        def route_web_classification(state: ComplaintState):
            classification = state["classification"].lower()
            if classification == "no":
                print("Web Classification is 'No'. Ending process.")
                logging.info("Web Classification is 'No'. Ending process.")
                return "Classification  = No"  # Goes to END
            else:
                print("Web Classification is 'Yes'. Proceeding to generate web solution.")
                logging.info("Web Classification is 'Yes'. Proceeding to generate web solution.")
                return "Classification  = Yes"


        # Step 8: Generate Document-Based Solution
        def generate_doc_solution(state: ComplaintState):
            print("Generating document-based solution...")
            logging.info("Generating document-based solution...")
            
            summarized_complaint = state["summarized_complaint"]
            classification       = state["classification"]
            company              = state["company"]
            state_name           = state["state"]
            zip_code             = state["zip_code"]
            Product              = state["Product"]
            Sub_Product          = state["Sub_Product"]
        
            solution_response = doc_solution_chain.invoke({
                                                                "query": summarized_complaint,  
                                                                "Company": company,
                                                                "State": state_name,
                                                                "ZIP_code": zip_code
                                                          }).content
            print("Document-based solution generated.")
            logging.info("Document-based solution generated.")
            return {"solution": solution_response}


        # Step 9: Grade Document-Based Solution
        def grade_doc_solution(state: ComplaintState):
            print("Grading the document-based solution...")
            logging.info("Grading the document-based solution...")
        
            summarized_complaint = state["summarized_complaint"]
            solution             = state["solution"]
            retrieved_docs       = state["retrieved_docs"]
            classification       = state["classification"]
            explanation          = state["explanation"]
            
            
            max_doc_length       = 2000  
            doc_txt              = "\n".join([doc.page_content for doc in retrieved_docs])[:max_doc_length]
        
            grade_response = doc_hallucinations_grader.invoke({
                                                                    "documents": doc_txt,
                                                                    "complaint": summarized_complaint,
                                                                    "solution": solution
                                                                })
        
            print(f"Grading complete. Raw response: {grade_response}")
            logging.info(f"Grading complete. Raw response: {grade_response}")
        
            solution_valid = grade_response.binary_score.lower()
            print(f"Solution validity: {solution_valid}")
            logging.info(f"Solution validity: {solution_valid}")

            if solution_valid == "yes":
                return {
                            "classification": classification,
                            "explanation": explanation,
                            "solution": solution,
                            "solution_source": "doc",
                            "solution_valid": "yes"  
                        }
            else:
                print("Document-based solution did not pass grading.")
                logging.info("Document-based solution did not pass grading.")
                return {
                         "classification": classification,
                         "explanation": explanation,
                         "solution": None,
                         "solution_source": None,
                         "solution_valid": "no" 
                        }

        # Step 10: Route Solution Based on Validity
        def route_solution(state: ComplaintState):
            print("Checking if document-based solution is valid...")
            logging.info("Checking if document-based solution is valid...")
            if state["solution_valid"] == "yes":
                print("Document-based solution is valid. Ending process.")
                logging.info("Document-based solution is valid. Ending process.")
                return "Document Solution is valid"
            else:
                print("Document-based solution is invalid. Routing to web-based solution...")
                logging.info("Document-based solution is invalid. Routing to web-based solution...")
                return "Document Solution is not valid"
            
            
        # Step 11: Generate Web-Based Solution
        def generate_web_solution(state: ComplaintState):
            print("Generating web-based solution...")
            logging.info("Generating web-based solution...")
        
            summarized_complaint = state["summarized_complaint"]
            company              = state["company"]
            state_name           = state["state"]
            zip_code             = state["zip_code"]
            Product              = state["Product"]
            Sub_Product          = state["Sub_Product"]
            
            web_context_response = tavily_search_tool.invoke({"query": summarized_complaint})
        

            if isinstance(web_context_response, dict):
                web_context_list = web_context_response.get("context", ["No relevant web context found."])  
            elif isinstance(web_context_response, list):
                web_context_list = [entry.get("snippet", "") if isinstance(entry, dict) else str(entry) for entry in web_context_response]
            else:
                web_context_list = [str(web_context_response)]
        
            web_context = "\n".join(web_context_list)  
        
            web_solution_response = web_solution_chain.invoke({     "query": summarized_complaint,   
                                                                    "context": web_context,  
                                                                    "complaint": summarized_complaint,
                                                                    "Company": company,
                                                                    "State": state_name,
                                                                    "ZIP_code": zip_code
                                                                }).content
            
            logging.info("Fetching Web_Text.")
            print("Fetching Web_Text.")
            
            if isinstance(web_context_response, list):
                web_txt                             = "\n".join([entry.get("snippet", "No relevant web data found.") for entry in web_context_response])
            elif isinstance(web_context_response, dict):
                web_txt                             = web_context_response.get("snippet", "No relevant web data found.")
            else:
                web_txt                             = "No relevant web data found."
            logging.info("Completed fetching Web_Text.")
            print("Completed fetching Web_Text.")
        
            print("Web-based solution generated.")
            logging.info("Web-based solution generated.")
            
            return {
                        "solution": web_solution_response,
                        "retrieved_web_context": web_context_list,
                        "web_txt" : web_txt
                    }


        def grade_web_solution(state: ComplaintState):
            print("Grading the web-based solution...")
        
            summarized_complaint = state["summarized_complaint"]
            solution             = state["solution"]
            classification       = state["classification"]
            explanation          = state["explanation"]
            web_txt              = state["web_txt"]
            retry_count          = state.get("retry_count", 0)
            
            retry_count += 1
            state["retry_count"] = retry_count  # Ensure persistence
        
            retry_count = state["retry_count"] 
            grade_response = web_hallucinations_grader.invoke({
                                                                    "context": web_txt, 
                                                                    "complaint": summarized_complaint, 
                                                                    "solution": solution
                                                                })
        
            print("Grading complete. Raw response:", grade_response)
        
            solution_valid = grade_response.binary_score.lower()
            print("Solution validity:", solution_valid)
            if solution_valid == "yes":
                return {
                    "classification": classification,
                    "explanation": explanation,
                    "solution": solution,
                    "solution_source": "web",
                    "solution_valid": "yes",
                    "retry_count" : retry_count
                }
            else:
                print("Web-based solution did not pass grading.")
                return {
                    "classification": classification,
                    "explanation": explanation,
                    "solution": "No valid solution found from web.",
                    "solution_source": "none",
                    "solution_valid": "no",
                    "retry_count" : retry_count
                    
                }

        
        
        # Step 13: Retry Web-Based Solution 
        def retry_web_solution(state: ComplaintState):
            print("Checking if web-based solution is valid...")
            logging.info("Checking if web-based solution is valid...")
        
            solution_valid = state.get("solution_valid", "no")  
            retry_count = state.get("retry_count", 0)  
        
            if solution_valid.lower() == "yes":
                print("Web solution is valid. Proceeding to next step.")
                logging.info("Web solution is valid. Proceeding to next step.")
                return "Web solution valid" 
        
            if retry_count > 2:
                print("Web solution failed after 2 retries. Ending process.")
                logging.info("Web solution failed after 2 retries. Ending process.")
                return "Web solution failed"
        
            print(f"Retrying web solution (Attempt {retry_count + 1})...")
            logging.info(f"Retrying web solution (Attempt {retry_count + 1})...")
        
            return {"retry_count": retry_count + 1, "solution_valid": "no"}

        ###################### Compiling a workflow #####################################################
        print("Compiling a workflow.")
        logging.info("Compiling a workflow.")
        workflow = StateGraph(ComplaintState) 
        workflow.add_node("retrieve_documents", RunnableLambda(retrieve_documents))
        workflow.set_entry_point("retrieve_documents")
        
        workflow.add_node("grade_documents", RunnableLambda(grade_documents))
        workflow.add_edge("retrieve_documents", "grade_documents")
        
        workflow.add_conditional_edges("grade_documents", route_classification,  
                                       {
                                           "Docs_are_relevant": "classify_complaint_doc",
                                           "Docs_are_not_relevant": "classify_complaint_web"
                                       })
        
        workflow.add_node("classify_complaint_doc", RunnableLambda(classify_complaint_doc))
        workflow.add_node("classify_complaint_web", RunnableLambda(classify_complaint_web))
        
        workflow.add_node("generate_doc_solution", RunnableLambda(generate_doc_solution))
        workflow.add_conditional_edges(
                                            "classify_complaint_doc",
                                            route_doc_classification,
                                                                        {
                                                                            "Classification  = No": END,  
                                                                            "Classification  = Yes": "generate_doc_solution"  
                                                                        }
                                        )
        
        workflow.add_node("grade_doc_solution", RunnableLambda(grade_doc_solution))
        workflow.add_edge("generate_doc_solution", "grade_doc_solution")
        
        workflow.add_node("generate_web_solution", RunnableLambda(generate_web_solution))
        workflow.add_conditional_edges(
                                            "classify_complaint_web",
                                            route_web_classification,
                                                                        {
                                                                            "Classification  = No": END,  
                                                                            "Classification  = Yes": "generate_web_solution"  
                                                                        }
                                        )
        
        workflow.add_conditional_edges("grade_doc_solution", route_solution,  
                                       {
                                           "Document Solution is valid": END,
                                           "Document Solution is not valid": "generate_web_solution"
                                       })
        
        
        
        workflow.add_node("grade_web_solution", RunnableLambda(grade_web_solution))
        workflow.add_edge("generate_web_solution", "grade_web_solution")
        
        workflow.add_conditional_edges("grade_web_solution", retry_web_solution,  
                                       {
                                           "Web solution valid": END,  
                                           "Web solution not valid": "generate_web_solution",
                                           "Web solution failed": END  
                                       })
        complaint_app = workflow.compile()
        print("Completed compiling a workflow.")
        logging.info("Completed compiling a workflow.")
         
        return complaint_app
    
    
    
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv 
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
#     from complaint_summarization import complaint_summarization_chain_class
#     from document_grading import document_grading_class
#     from complaint_classification import complaint_clasification_class
#     from complaint_solution import solution_extraction_class
#     from solution_grading import solution_grading_class
#     from database_activity import database_activity_class
#     import pyodbc
    
#     server                                  = 'DESKTOP-VONKKUH'  # e.g., 'localhost\SQLEXPRESS'
#     database                                = 'Cart2.0'  # e.g., 'CART_DB'
#     driver                                  = '{ODBC Driver 17 for SQL Server}'  # Ensure you have the correct ODBC driver installed
#     conn                                    = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
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
#     complaint_id                            = '10000'
#     complaint                               = "I am an XXXX XXXXXXXX XXXX XXXX I have {$520000.00} in my Chase checking account. I was the victim of an XXXX XXXX scam which was detected on XX/XX/XXXX. The scam was reported to XXXX XXXXXXXX XXXX XXXX XXXX  Police and is being actively investigated by the FBI ( contact details can be provided upon request ). Since XX/XX/XXXX I have been trying to have the Chase checking funds returned to me. I have on numerous occasions visited the branch, phoned, etc ( details can be provided upon request ). I need these funds for living expenses and investment purposes. I am extremely distraught by Chase 's horrible treatment. Not only were they negligent in not noting the obvious signs of the scam, but they are adding insult to injury by not returning the money I have with them."
#     company                                 = 'JPMORGAN CHASE & CO.'
#     state                                   = 'NJ'
#     zip_code                                = '08701'
#     employee_id                             = 'c6400'
#     cart_log_id                             = 1001

#     complaint_summarization_chain_class_obj = complaint_summarization_chain_class()
#     complaint_rewriter                      = complaint_summarization_chain_class_obj.get_summarization_chain(llm)
#     summarized_complaint                    = complaint_rewriter.invoke({"complaint": complaint})

#     document_grading_class_obj              = document_grading_class()
#     retriever_tool, retriever               = document_grading_class_obj.get_document_retirever(reg_name, vector_db_path, embedding_function)
#     document_grade_chain                    = document_grading_class_obj.get_document_grade_chain(reg_name, llm)

#     complaint_clasification_class_obj       = complaint_clasification_class()
#     doc_classification_chain                = complaint_clasification_class_obj.get_doc_classification_chain(reg_name, retriever_tool, llm)

#     tavily_search_tool                      = complaint_clasification_class_obj.get_tavily_search_tool(TAVILY_API_KEY, total_tavily_searches = 3)
#     web_classification_chain                = complaint_clasification_class_obj.get_web_classification_chain(reg_name, tavily_search_tool, llm)
  
#     solution_extraction_class_obj           = solution_extraction_class()
#     doc_solution_chain                      = solution_extraction_class_obj.get_doc_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company) 
#     web_solution_chain                      = solution_extraction_class_obj.get_web_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company)

    
#     solution_grading_class_obj              = solution_grading_class()
#     doc_hallucinations_grader               = solution_grading_class_obj.get_doc_hallucination_grading_chain(reg_name, llm)
#     web_hallucinations_grader               = solution_grading_class_obj.get_web_hallucination_grading_chain(reg_name, llm)
    


            
    
#     complaint_stategraph_class_obj          = complaint_stategraph_class()
#     # complaint_app                           = complaint_stategraph_class_obj.get_stategraph(complaint_rewriter, retriever, document_grade_chain, doc_classification_chain, web_classification_chain, doc_solution_chain, doc_hallucinations_grader, web_solution_chain, web_hallucinations_grader, tavily_search_tool)
    
#     # from IPython.display import Image, display  # Type: ignore
#     # # Graph visualization
#     # display(Image(complaint_app.get_graph(xray=True).draw_mermaid_png()))
    
#     # result                                  = complaint_app.invoke({
#     #                                                                     "summarized_complaint": summarized_complaint,
#     #                                                                     "company": company,
#     #                                                                     "state": state,
#     #                                                                     "zip_code": zip_code
#     #                                                                 })
#     regulation_ingestion_dict                  = {'Reg_B':True,'Reg_C':True,'Reg_D':True,'Reg_E':True,'Reg_F':True,
#                                                   'Reg_G':True,'Reg_H':True,'Reg_I':True,'Reg_J':True,'Reg_K':True,
#                                                   'Reg_L':True,'Reg_M':True,'Reg_N':True,'Reg_O':True,'Reg_P':True,
#                                                   'Reg_V':True,'Reg_X':True,'Reg_Z':True,
#                                                   'Reg_CC':True,'Reg_DD':True,'Reg_AA':True}
#     import pandas as pd
#     def review_single_complaint(complaint_id, complaint, company, state, zip_code, llm, embedding_function, cart_log_id, employee_id):
#         reviewed_complaint_df                          = pd.DataFrame({'Complaint_ID': [complaint_id], 
#                                                                        'Complaint_Text': [complaint], 
#                                                                        'Company': [company], 
#                                                                        'State': [state], 
#                                                                        'Zip_Code': [zip_code]})
#         complaint_rewriter                             = complaint_summarization_chain_class_obj.get_summarization_chain(llm)
#         summarized_complaint                           = complaint_rewriter.invoke({"complaint": complaint})
#         reviewed_complaint_df['Summarized_Complaint']  = summarized_complaint
        
#         for reg_name in regulation_ingestion_dict.keys():
#             print(f"Running the state graph for {reg_name}")
#             logging.info(f"Running the state graph for {reg_name}")
#             retriever_tool, retriever     = document_grading_class_obj.get_document_retirever(reg_name, vector_db_path, embedding_function)
#             document_grade_chain          = document_grading_class_obj.get_document_grade_chain(reg_name, llm)
#             doc_classification_chain      = complaint_clasification_class_obj.get_doc_classification_chain(reg_name, retriever_tool, llm)
#             tavily_search_tool            = complaint_clasification_class_obj.get_tavily_search_tool(TAVILY_API_KEY, total_tavily_searches = 3)
#             web_classification_chain      = complaint_clasification_class_obj.get_web_classification_chain(reg_name, tavily_search_tool, llm)
#             doc_solution_chain            = solution_extraction_class_obj.get_doc_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company) 
#             web_solution_chain            = solution_extraction_class_obj.get_web_solution_chain(reg_name, retriever_tool, llm, state, zip_code, company)
#             doc_hallucinations_grader     = solution_grading_class_obj.get_doc_hallucination_grading_chain(reg_name, llm)
#             web_hallucinations_grader     = solution_grading_class_obj.get_web_hallucination_grading_chain(reg_name, llm)
#             complaint_app                 = complaint_stategraph_class_obj.get_stategraph(complaint_rewriter, retriever, document_grade_chain, doc_classification_chain, web_classification_chain, doc_solution_chain, doc_hallucinations_grader, web_solution_chain, web_hallucinations_grader, tavily_search_tool)
#             result                        = complaint_app.invoke({
#                                                                     "summarized_complaint": summarized_complaint,
#                                                                     "company": company,
#                                                                     "state": state,
#                                                                     "zip_code": zip_code
#                                                                  })
            
#             reviewed_complaint_df[reg_name + '_Classification']  = result['classification']
#             reviewed_complaint_df[reg_name + '_Explanation']     = result['explanation']
#             reviewed_complaint_df[reg_name + '_Solution']        = result['solution']
#             reviewed_complaint_df[reg_name + '_Solution_Source'] = result['solution_source']
#             print(f"Completed running the state graph for {reg_name}")
#             logging.info(f"Completed running the state graph for {reg_name}")
#         reviewed_complaint_df['Total_Tags']                  = None
#         reviewed_complaint_df['Tagged_Regulations']          = None
#         reviewed_complaint_df['Loaded_By']                   = employee_id
#         reviewed_complaint_df['Cart_Log_Id']                 = cart_log_id
#         return reviewed_complaint_df
    
#     database_activity_class_obj                 = database_activity_class()  
#     unreviewed_complaints_table                 = 'cart_untagged_complaints'
#     unreviewed_complaints_df                    = database_activity_class_obj.import_unreviewed_complaints(conn,unreviewed_complaints_table)

#     def review_bulk_complaints(unreviewed_complaints_df, conn, cart_log_id, llm, embedding_function):
#         query = "SELECT TOP 0 * FROM [Cart2.0].[dbo].[cart_cfpb_complaints_reg_stage]"
#         reviewed_complaint_df_final = pd.read_sql_query(query, conn)
#         reviewed_complaint_df_final = pd.DataFrame(columns=reviewed_complaint_df_final.columns)
    
#         regulations = [
#             "Reg_B", "Reg_C", "Reg_D", "Reg_E", "Reg_F", "Reg_G", "Reg_H", "Reg_I",
#             "Reg_J", "Reg_K", "Reg_L", "Reg_M", "Reg_N", "Reg_O", "Reg_P", "Reg_V",
#             "Reg_X", "Reg_Z", "Reg_CC", "Reg_DD", "Reg_AA"
#         ]
    
#         for _, row in unreviewed_complaints_df.iterrows():
#             complaint_id = row["Complaint_ID"]
#             complaint = row["Complaint_Text"]
#             company = row["Company"]
#             state = row["State"]
#             zip_code = row["ZIP_Code"]
    
#             print(f"Processing Complaint_ID: {complaint_id}")
#             logging.info(f"Processing Complaint_ID: {complaint_id}")
    
#             if len(complaint.strip()) > 0:
#                 reviewed_complaint_df = review_single_complaint(
#                     complaint_id, complaint, company, state, zip_code, llm, embedding_function, cart_log_id, employee_id
#                 )
#             else:
#                 empty_data = {
#                     "Complaint_ID": complaint_id,
#                     "Complaint_Text": complaint,
#                     "Company": company,
#                     "State": state,
#                     "Zip_Code": zip_code,
#                     "Summarized_Complaint": None,
#                     "Total_Tags": None,
#                     "Tagged_Regulations": None,
#                     "Loaded_By": employee_id,
#                     "Cart_Log_Id": cart_log_id,
#                 }
    
#                 # Fill classification columns with "no"
#                 for reg in regulations:
#                     empty_data[f"{reg}_Classification"] = "no"
#                     empty_data[f"{reg}_Explanation"] = "Complaint empty."
#                     empty_data[f"{reg}_Solution"] = "No solution required."
#                     empty_data[f"{reg}_Solution_Source"] = None
    
#                 reviewed_complaint_df = pd.DataFrame([empty_data])
    
#             # Append to final DataFrame
#             reviewed_complaint_df_final = pd.concat([reviewed_complaint_df_final, reviewed_complaint_df], ignore_index=True)
            
#             print(f"Completed processing Complaint_ID: {complaint_id}")
#             logging.info(f"Completed processing Complaint_ID: {complaint_id}")
#         return reviewed_complaint_df_final
    
#     reviewed_complaint_df_final = review_bulk_complaints(unreviewed_complaints_df, conn, cart_log_id, llm, embedding_function)

                
            
        
        
    
     