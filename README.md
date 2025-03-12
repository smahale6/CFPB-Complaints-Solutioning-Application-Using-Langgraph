# Agent based Complaints Solutioning Application using Langgraph

---
---
## 🚀 Cart 2.0 - Complete Setup & Execution Guide  

This guide provides step-by-step instructions to install, configure, and run **Cart 2.0** for first-time users.

---

## **1️⃣ Pre-requisites**  

Before running **Cart 2.0**, ensure you have the following installed:  

✅ **Python 3.9+** (Check using `python --version`)  
✅ **Git** (Required for cloning the repository)  
✅ **Groq API Key** → Required for Llama 3 processing ([Sign up here](https://groq.com/))  
✅ **Tavily API Key** → Required for web-based search ([Get API key](https://tavily.com/))  
✅ **Hugging Face API Key** → Required for embedding models ([Get API key](https://huggingface.co/settings/tokens))  
✅ **Microsoft SQL Server** → Required for complaint storage  
✅ **ODBC Driver for SQL Server** → Download **[ODBC Driver 17](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)**  


## **2️⃣ Clone the Repository**  

Open a **terminal (Mac/Linux) or command prompt (Windows)** and run:  

```bash
git clone https://github.com/your-repo/cart-2.0.git
cd cart-2.0

##  **3️⃣ Create a Virtual Environment**
For Windows
python -m venv cart_env
cart_env\Scripts\activate

For Mac/Linux
source cart_env/bin/activate

## **4️⃣ Install Dependencies**
Run the following command to install all required packages:
pip install -r requirements.txt

## **5️⃣ Set Up API Keys in .env**
1. Create a .env file in the cart-2.0 folder:
2. Open the .env file and add the following:
**   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   EMPLOYEE_ID=your_employee_id**

## **6️⃣ Configure SQL Server Connection**
Cart 2.0 uses Microsoft SQL Server to store complaints.
Ensure that:

SQL Server is running
Your connection credentials are correct

`server = 'YOUR-SQL-SERVER-NAME'  # Example: 'localhost\SQLEXPRESS'`
`database = 'Cart2.0'`
`driver = '{ODBC Driver 17 for SQL Server}'`
`conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')`

## **7️⃣ Run Cart 2.0 from CLI**
Set Argument Values Before Running
Before executing Cart 2.0, ensure you define the necessary arguments like company name, date range, and total complaints to fetch.

Open CART.py and update the following values inside the run_cart() function:

`company = 'JPMORGAN CHASE & CO.'`
`total_records = 10`
`date_received_min = "2024-01-01"`
`date_received_max = "2024-03-31"`
`llm_model = 'llama3-70b-8192'`

After setting the values, run the tool from the terminal:
`python CART.py`

## **8️⃣ Run the Streamlit Web UI**
Cart 2.0 includes a Streamlit-based UI.
To start the web interface, run:
`streamlit run Cart_App.py`

🎯 Summary
✅ **Clone the repo**
✅ **Install dependencies (pip install -r requirements.txt)**
✅ **Set up API keys in .env**
✅ **Configure SQL Server connection**
✅ **Set arguments before running CART.py**
✅ **Run python CART.py to process complaints**
✅ **Use streamlit run Cart_App.py for UI**

----
----

## Cart 2.0 - Workflows & Class Summary

### 1️⃣ Complaint Workflow Files & Class Summary

The **Complaint Workflow** inside the `src/complaint_workflow/` folder handles the full pipeline for **fetching, summarizing, classifying, solving, and grading** consumer complaints using **LangGraph-based workflows**.

### 📂 **Complaint Workflow Components**

| File Name                          | Class Name                           | Functionality |
|-------------------------------------|--------------------------------------|-------------------|
| `fetch_complaints_api.py`         | `fetch_compalints_class`            | Fetches complaints from CFPB API and loads them into SQL DB. |
| `complaint_summarization.py`      | `complaint_summarization_chain_class` | Summarizes long complaints before processing. |
| `document_grading.py`             | `document_grading_class`             | Grades retrieved regulatory documents for relevance. |
| `complaint_classification.py`     | `complaint_clasification_class`     | Classifies complaints with a CFPB regulation (Document-based & Web-based). |
| `complaint_solution.py`           | `solution_extraction_class`         | Generates structured solutions for complaints (Document-based & Web-based). |
| `solution_grading.py`             | `solution_grading_class`             | Grades the generated solutions for accuracy and completeness. |
| `complaint_stategraph.py`         | `complaint_stategraph_class`         | LangGraph-based state machine for complaint workflow execution. |


### 2️⃣ Email Workflow Files & Class Summary

The **Email Workflow** inside the `src/email_workflow/` folder is responsible for **formulating, grading, and refining email responses** to customer complaints.

### 📂 **Email Workflow Components**

| File Name            | Class Name            | Functionality |
|----------------------|----------------------|-------------------|
| `email_formation.py` | `email_formation_class` | Generates customer-facing email responses for complaints. |
| `email_grading.py`   | `email_grading_class`   | Grades generated emails for accuracy, coverage, and clarity. |
| `email_stategraph.py` | `email_stategraph_class` | LangGraph-based workflow for email formulation and validation. |


### 3️⃣ Core Components & Classes

The **Core Components** provide **database management, logging, regulation ingestion, and the main execution flow**.

### 📂 **Core Components & Classes**

| File Name                      | Class Name                      | Functionality |
|--------------------------------|--------------------------------|-------------------|
| `CART.py`                     | `cart_intersect_class`         | Main execution file integrating all workflows (complaint & email). |
| `Cart_App.py`                  | `CartApp`                      | Streamlit web UI for running CART interactively. |
| `database_activity.py`        | `database_activity_class`      | Handles SQL Server interactions: log management, data ingestion, and report updates. |
| `logger.py`                   | `Logger`                       | Centralized logging to track execution flow and errors. |
| `regulation_text_ingestion.py` | `regulation_ingestion_class`   | Loads and vectorizes regulation PDFs into ChromaDB for retrieval. |


## 🚀 Cart 2.0 - Execution Flow Summary

This section provides an overview of how **Cart 2.0** processes complaints and formulates responses using a structured workflow.


### 1️⃣ Execution Flow of the Complaint Workflow

The **Complaint Workflow** processes consumer complaints through a **step-by-step pipeline** to classify, solve, and validate responses.

### 🔹 **Complaint Workflow Steps**
1. **Fetch Complaints (`fetch_complaints_api.py`)**  
   - Retrieves **CFPB complaints** via API.  
   - Filters complaints with **valid narratives**.  
   - Loads them into **SQL Database**.

2. **Summarize Complaints (`complaint_summarization.py`)**  
   - Extracts a **structured summary** from the complaint.  
   - Identifies **key financial institutions, regulatory violations, and monetary details**.

3. **Retrieve & Grade Documents (`document_grading.py`)**  
   - Uses **Chroma Vector DB** to fetch **relevant regulation documents**.  
   - Grades retrieved documents based on **contextual relevance**.

4. **Classify Complaint (`complaint_classification.py`)**  
   - **Document-Based Classification:** Uses **retrieved regulatory documents** to classify if a complaint falls under **Reg AA**.  
   - **Web-Based Classification:** Uses **Tavily Search API** to fetch **real-time web information** and classify the complaint.

5. **Extract Solutions (`complaint_solution.py`)**  
   - **Document-Based Solution Extraction:**  
     - Generates **structured regulatory-backed solutions** using **retrieved regulation documents**.  
     - **Incorporates location-specific clauses** (Company, State, ZIP code).  
   - **Web-Based Solution Extraction:**  
     - Uses **Tavily Search API** to fetch web sources and generate solutions.

6. **Grade Solutions (`solution_grading.py`)**  
   - **Document-Based Solution Grading:**  
     - Checks **hallucinations** in **retrieved regulatory solutions**.  
   - **Web-Based Solution Grading:**  
     - Evaluates **web-based solutions** for **accuracy and relevance**.

7. **Execute LangGraph Workflow (`complaint_stategraph.py`)**  
   - **Implements a state machine** to:  
     - **Fetch & grade documents**.  
     - **Route classification to document-based or web-based**.  
     - **Extract and validate solutions**.  
     - **Retry web-based solution if necessary**.  
     - **End the process if a valid solution is found**.  


### 2️⃣ Execution Flow of the Email Workflow

The **Email Workflow** is responsible for **formulating, grading, and refining** email responses to customer complaints.

### 🔹 **Email Workflow Steps**
1. **Select Email Type (`email_formation.py`)**  
   - **If complaint is regulated**, generate a **legal response**.  
   - **If not regulated**, generate a **polite dissatisfaction acknowledgment**.

2. **Generate Email (`email_formation.py`)**  
   - **Regulated Complaint:** Generates **structured, regulation-backed email responses**.  
   - **Non-Regulated Complaint:** Generates **empathetic responses** for complaints that do not fit any regulation.

3. **Grade Email (`email_grading.py`)**  
   - Evaluates the email for:  
     - **Coverage**: Does it address **all major concerns**?  
     - **Regulatory Accuracy**: Does it **correctly reference CFPB regulations**?  
     - **Clarity & Completeness**: Is it **clear and structured**?  
     - **No Hallucination**: Does it **avoid misleading or incorrect** information?  
   - If the email **fails**, it is **refined and regenerated**.

4. **Execute LangGraph Workflow (`email_stategraph.py`)**  
   - Implements **LangGraph-based state machine** to:  
     - **Select the correct email type** (Regulated or Non-Regulated).  
     - **Generate and grade the email**.  
     - **If the email fails**, refine and regenerate **(max 2 attempts)**.  
     - **Approve and finalize** the best version of the email.


### 3️⃣ Execution Flow of Core Components

The **Core Components** handle **database management, logging, regulation ingestion, and the main execution flow**.

### 🔹 **Core Execution Steps**
1. **Start Execution (`CART.py`)**  
   - Initializes **CART 2.0** execution.  
   - Fetches **CFPB complaints** for processing.

2. **Database Setup (`database_activity.py`)**  
   - Connects to **SQL Server** and **checks user permissions**.  
   - Loads **fetched complaints into SQL**.  
   - Updates **CART log entries**.

3. **Regulation Ingestion (`regulation_text_ingestion.py`)**  
   - Reads **regulation PDFs** and **vectorizes them** using **ChromaDB**.  
   - Moves processed PDFs to **archive**.

4. **Run Complaint Workflow (`CART.py`)**  
   - Fetches, summarizes, classifies, and solves complaints.  
   - Stores results in SQL Server.

5. **Run Email Workflow (`CART.py`)**  
   - Generates **final email responses**.  
   - Stores the email responses in **SQL Database**.

6. **Complete Execution (`CART.py`)**  
   - Finalizes **reviewed complaints and solutions**.  
   - Updates logs and reports.


## 🚀 **Cart 2.0 Overview**
✅ **CART integrates complaint and email workflows**  
✅ **Streamlit UI for easy execution**  
✅ **SQL database logging and reporting**  
✅ **Regulation PDF ingestion for document retrieval**  
✅ **Centralized logging to track execution flow**  

---
---


## 🚀 Cart 2.0 - Infrastructure Overview

Cart 2.0 is built using a **modular architecture** integrating various **AI, database, and vector storage technologies** to process consumer complaints efficiently.


### **1️⃣ Core Infrastructure Components**

| **Component**            | **Technology Used**            | **Description** |
|--------------------------|--------------------------------|----------------|
| **Programming Language** | Python 3.9                    | Used for all scripting and AI processing. |
| **Frameworks**          | LangChain, LangGraph          | Used for AI workflows, complaint classification, and email automation. |
| **Database**            | SQL Server (MSSQL)            | Stores **complaints, classified results, emails, and logs**. |
| **Vector Database**      | ChromaDB                      | Stores **vectorized regulatory documents** for retrieval. |
| **Embeddings Model**     | `BAAI/bge-large-en-v1.5`      | Used for generating embeddings for regulation documents. |
| **Large Language Model** | `Llama 3` (via Groq API)      | Used for **complaint classification, solution extraction, and email formulation**. |
| **Search Engine**        | Tavily Search API             | Fetches real-time web information when **regulatory documents are not relevant**. |
| **Cloud Environment**    | Local + Cloud (Azure)         | SQL Server is **cloud-hosted**; some components run locally. |


### **2️⃣ Database & Storage Components**

| **Storage Type**           | **Technology Used** | **Description** |
|----------------------------|--------------------|----------------|
| **SQL Database**           | Microsoft SQL Server | Stores **raw and processed complaint data, logs, email responses, and regulatory mappings**. |
| **Vector Store**           | ChromaDB | Stores **embedded regulatory documents for fast retrieval**. |
| **Document Storage**       | Local/Cloud File System | Stores **PDFs of regulations before ingestion into ChromaDB**. |
| **Logs Storage**           | Local Log Files (`logs/`) | Stores **execution logs for debugging and monitoring**. |


### **3️⃣ Machine Learning & AI Components**

| **Component**                 | **Technology Used**              | **Description** |
|--------------------------------|--------------------------------|----------------|
| **Text Embeddings**            | `BAAI/bge-large-en-v1.5` (HuggingFace) | Converts text into vector embeddings for **regulatory document retrieval**. |
| **LLM for Text Processing**    | `Llama 3.2 3B (Preview) 8k` via Groq API | Processes complaints, generates responses, and classifies issues. |
| **LangChain Pipelines**        | LangChain + LangGraph          | Automates workflows for **classification, grading, and email formulation**. |


### **4️⃣ Workflow & Automation**

| **Workflow Type**              | **Technology Used**          | **Description** |
|--------------------------------|------------------------------|----------------|
| **Complaint Processing Workflow** | LangGraph (State Machines) | Automates complaint classification, retrieval, and solution extraction. |
| **Email Processing Workflow**  | LangGraph + Streamlit        | Automates **email generation, grading, and refinement**. |
| **Regulation Ingestion**       | ChromaDB + PDF Processing   | Converts **PDF regulations into embeddings** for retrieval. |
| **Web-Based Research**         | Tavily API                  | Fetches **real-time case laws and regulatory guidelines** when needed. |


### **5️⃣ User Interface & Deployment**

| **Component**                 | **Technology Used**            | **Description** |
|--------------------------------|------------------------------|----------------|
| **User Interface**            | Streamlit                    | Provides an **interactive UI** for users to trigger and monitor complaint processing. |
| **Backend Processing**        | Python + SQL Server          | Handles **data ingestion, AI processing, and workflow execution**. |
| **Deployment Type**           | Local + Cloud (Azure)        | SQL Server and some APIs are cloud-hosted, while processing runs **locally or in a VM**. |


### **6️⃣ Logging & Monitoring**

| **Component**                 | **Technology Used**           | **Description** |
|--------------------------------|------------------------------|----------------|
| **Logging**                   | Python Logging Module        | Logs **workflow execution, errors, and API calls**. |
| **Error Handling**            | Try/Except Blocks + Logs     | Ensures **graceful error handling** with log reports. |


## **🚀 Key Takeaways**
✅ **Built using Python, LangChain, LangGraph, and SQL Server**  
✅ **Uses ChromaDB for fast document retrieval**  
✅ **Leverages Llama 3 for AI-based classification & solution extraction**  
✅ **Employs Tavily API for real-time web-based regulatory lookup**  
✅ **Automates complaint & email processing using LangGraph**  
✅ **Offers an interactive UI via Streamlit**  

---
---
## 🚀 Cart 2.0 - Complete Setup & Execution Guide  

This guide provides step-by-step instructions to install, configure, and run **Cart 2.0** for first-time users.

---

## **1️⃣ Pre-requisites**  

Before running **Cart 2.0**, ensure you have the following installed:  

✅ **Python 3.9+** (Check using `python --version`)  
✅ **Git** (Required for cloning the repository)  
✅ **Groq API Key** → Required for Llama 3 processing ([Sign up here](https://groq.com/))  
✅ **Tavily API Key** → Required for web-based search ([Get API key](https://tavily.com/))  
✅ **Hugging Face API Key** → Required for embedding models ([Get API key](https://huggingface.co/settings/tokens))  
✅ **Microsoft SQL Server** → Required for complaint storage  
✅ **ODBC Driver for SQL Server** → Download **[ODBC Driver 17](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)**  


## **2️⃣ Clone the Repository**  

Open a **terminal (Mac/Linux) or command prompt (Windows)** and run:  

```bash
git clone https://github.com/your-repo/cart-2.0.git
cd cart-2.0

##  **3️⃣ Create a Virtual Environment**
For Windows
python -m venv cart_env
cart_env\Scripts\activate

For Mac/Linux
source cart_env/bin/activate

## **4️⃣ Install Dependencies**
Run the following command to install all required packages:
pip install -r requirements.txt

## **5️⃣ Set Up API Keys in .env**
1. Create a .env file in the cart-2.0 folder:
2. Open the .env file and add the following:
**   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   EMPLOYEE_ID=your_employee_id**

## **6️⃣ Configure SQL Server Connection**
Cart 2.0 uses Microsoft SQL Server to store complaints.
Ensure that:

SQL Server is running
Your connection credentials are correct

`server = 'YOUR-SQL-SERVER-NAME'  # Example: 'localhost\SQLEXPRESS'`
`database = 'Cart2.0'`
`driver = '{ODBC Driver 17 for SQL Server}'`
`conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')`

## **7️⃣ Run Cart 2.0 from CLI**
Set Argument Values Before Running
Before executing Cart 2.0, ensure you define the necessary arguments like company name, date range, and total complaints to fetch.

Open CART.py and update the following values inside the run_cart() function:

`company = 'JPMORGAN CHASE & CO.'`
`total_records = 10`
`date_received_min = "2024-01-01"`
`date_received_max = "2024-03-31"`
`llm_model = 'llama3-70b-8192'`

After setting the values, run the tool from the terminal:
`python CART.py`

## **8️⃣ Run the Streamlit Web UI**
Cart 2.0 includes a Streamlit-based UI.
To start the web interface, run:
`streamlit run Cart_App.py`

🎯 Summary
✅ **Clone the repo**
✅ **Install dependencies (pip install -r requirements.txt)**
✅ **Set up API keys in .env**
✅ **Configure SQL Server connection**
✅ **Set arguments before running CART.py**
✅ **Run python CART.py to process complaints**
✅ **Use streamlit run Cart_App.py for UI**



