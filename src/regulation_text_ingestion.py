from langchain_chroma import Chroma
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import pathlib
import logging
from pathlib import Path
import shutil
import sys
sys.setrecursionlimit(3000)
from logger import Logger

class regulation_ingestion_class:
    def __init__(self):
        self.logger_obj = Logger() 
        
    def ingest_regulation_files(self, embedding_function, regulation_dict, regulations_path, vector_db_path, chunk_size=1000, chunk_overlap=200):
        vector_stores = {}
        logging.info("Fetching all regulation sub-folders inside the regulation folder.")
        print("Fetching all regulation sub-folders inside the regulation folder.")
        
        subfolder_list = [f for f in os.listdir(regulations_path) if os.path.isdir(os.path.join(regulations_path, f))]

        for subfolder in subfolder_list:
            subfolder_path = os.path.join(regulations_path, subfolder)
            regulation_code = subfolder.split(" ")[0]  # Extracting Reg_X format

            if regulation_dict.get(regulation_code, False):  # Proceed only if the regulation is marked True
                archive_path = os.path.join(subfolder_path, "archive")
                os.makedirs(archive_path, exist_ok=True)

                logging.info(f"Processing regulation: {regulation_code}")
                print(f"Processing regulation: {regulation_code}")

                # Finding PDF files
                pdf_files = list(pathlib.Path(subfolder_path).glob("*.pdf"))
                
                if pdf_files:
                    persist_directory = os.path.join(vector_db_path, regulation_code)
                    
                    # Delete existing vector store (if any)
                    if os.path.exists(persist_directory):
                        shutil.rmtree(persist_directory)
                        logging.info(f"Deleted existing vector store: {persist_directory}")
                    
                    logging.info(f"Creating vector store for {regulation_code}")
                    print(f"Creating vector store for {regulation_code}")
                    
                    # Load and process PDFs
                    for pdf in pdf_files:
                        pdf_path = str(pdf.absolute())
                        pdf_name = pdf.name

                        logging.info(f"Loading PDF: {pdf_name}")
                        print(f"Loading PDF: {pdf_name}")

                        loader = PyMuPDFLoader(pdf_path)
                        document = loader.load()

                        # Splitting text
                        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                        text_chunks = text_splitter.split_documents(document)

                        texts = [doc.page_content for doc in text_chunks]  # Extracting text only

                        if texts:
                            # Ingesting into Chroma
                            logging.info(f"Ingesting text chunks into vector store: {regulation_code}")
                            print(f"Ingesting text chunks into vector store: {regulation_code}")

                            if regulation_code not in vector_stores:
                                vector_stores[regulation_code] = Chroma(
                                    persist_directory=persist_directory,
                                    embedding_function=embedding_function
                                )

                            vector_stores[regulation_code].add_texts(texts)

                        # Move processed PDF to archive
                        shutil.move(pdf_path, os.path.join(archive_path, pdf_name))
                        logging.info(f"Moved {pdf_name} to archive.")
                        print(f"Moved {pdf_name} to archive.")

                else:
                    logging.info(f"No PDF files found for {regulation_code}. Skipping...")
                    print(f"No PDF files found for {regulation_code}. Skipping...")

        logging.info("Regulation ingestion completed.")
        print("Regulation ingestion completed.")
        return None  


# if __name__ == "__main__":
#     cart_path = r'C:\GitHub Collections\CART 2.0\src'
#     regulations_path = os.path.join(cart_path, 'regulations')
#     vector_db_path = os.path.join(cart_path, 'vector_db')
#     version = 2.0
#     llm_model = 'llama3-70b-8192'
    
#     from dotenv import load_dotenv 
#     load_dotenv()  # Load environment variables from the .env file
#     TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#     HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
#     from langchain_groq import ChatGroq
#     from langchain_huggingface import HuggingFaceEmbeddings
    
#     llm = ChatGroq(model_name=llm_model, temperature=0.0, api_key=GROQ_API_KEY)
#     embedding_function = HuggingFaceEmbeddings(
#         model_name="BAAI/bge-large-en-v1.5",
#         model_kwargs={"token": HUGGINGFACE_API_KEY}
#     )
    
#     regulation_ingestion_class_obj = regulation_ingestion_class()
#     regulation_ingestion_dict = {
#         'Reg_B': True, 'Reg_C': True, 'Reg_D': True, 'Reg_E': True, 'Reg_F': True,
#         'Reg_G': True, 'Reg_H': True, 'Reg_I': True, 'Reg_J': True, 'Reg_K': True,
#         'Reg_L': True, 'Reg_M': True, 'Reg_N': True, 'Reg_O': True, 'Reg_P': True,
#         'Reg_V': True, 'Reg_X': True, 'Reg_Z': True, 'Reg_CC': True, 'Reg_DD': True,
#         'Reg_AA': True
#     }
    
#     vector_stores = regulation_ingestion_class_obj.ingest_regulation_files(
#         embedding_function, regulation_ingestion_dict, regulations_path, vector_db_path, chunk_size=1000, chunk_overlap=200
#     )
