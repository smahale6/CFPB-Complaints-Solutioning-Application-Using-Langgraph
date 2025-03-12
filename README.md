# Agentic Complaints Solutioning Application using Langgraph

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

---

### 2️⃣ Email Workflow Files & Class Summary

The **Email Workflow** inside the `src/email_workflow/` folder is responsible for **formulating, grading, and refining email responses** to customer complaints.

### 📂 **Email Workflow Components**

| File Name            | Class Name            | Functionality |
|----------------------|----------------------|-------------------|
| `email_formation.py` | `email_formation_class` | Generates customer-facing email responses for complaints. |
| `email_grading.py`   | `email_grading_class`   | Grades generated emails for accuracy, coverage, and clarity. |
| `email_stategraph.py` | `email_stategraph_class` | LangGraph-based workflow for email formulation and validation. |

---

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

---

##🚀 Cart 2.0 - Execution Flow Summary

This section provides an overview of how **Cart 2.0** processes complaints and formulates responses using a structured workflow.

---

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

---

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

---

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

---

## 🚀 **Cart 2.0 Overview**
✅ **CART integrates complaint and email workflows**  
✅ **Streamlit UI for easy execution**  
✅ **SQL database logging and reporting**  
✅ **Regulation PDF ingestion for document retrieval**  
✅ **Centralized logging to track execution flow**  

---




