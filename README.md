# Agentic-Complaints-Solutioning-Application-Using-Langgraph

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

## 🚀 **Cart 2.0 Overview**
✅ **CART integrates complaint and email workflows**  
✅ **Streamlit UI for easy execution**  
✅ **SQL database logging and reporting**  
✅ **Regulation PDF ingestion for document retrieval**  
✅ **Centralized logging to track execution flow**  

---


