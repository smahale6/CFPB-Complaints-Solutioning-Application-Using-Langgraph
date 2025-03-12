# Agentic-Complaints-Solutioning-Application-Using-Langgraph


# Cart 2.0 - Workflows & Class Summary

## 1️⃣ Complaint Workflow Files & Class Summary

The **Complaint Workflow** inside the `src/complaint_workflow/` folder handles the full pipeline for **fetching, summarizing, classifying, solving, and grading** consumer complaints using **LangGraph-based workflows**.

### 📂 **Complaint Workflow Components**

\[
\begin{array}{|c|c|c|}
\hline
\textbf{File Name} & \textbf{Class Name} & \textbf{Functionality} \\
\hline
\texttt{fetch\_complaints\_api.py} & \texttt{fetch\_compalints\_class} & Fetches complaints from CFPB API and loads them into SQL DB. \\
\hline
\texttt{complaint\_summarization.py} & \texttt{complaint\_summarization\_chain\_class} & Summarizes long complaints before processing. \\
\hline
\texttt{document\_grading.py} & \texttt{document\_grading\_class} & Grades retrieved regulatory documents for relevance. \\
\hline
\texttt{complaint\_classification.py} & \texttt{complaint\_clasification\_class} & Classifies complaints as Reg AA-related or not (Document-based \& Web-based). \\
\hline
\texttt{complaint\_solution.py} & \texttt{solution\_extraction\_class} & Generates structured solutions for complaints (Document-based \& Web-based). \\
\hline
\texttt{solution\_grading.py} & \texttt{solution\_grading\_class} & Grades the generated solutions for accuracy and completeness. \\
\hline
\texttt{complaint\_stategraph.py} & \texttt{complaint\_stategraph\_class} & LangGraph-based state machine for complaint workflow execution. \\
\hline
\end{array}
\]

---

## 2️⃣ Email Workflow Files & Class Summary

The **Email Workflow** inside the `src/email_workflow/` folder is responsible for **formulating, grading, and refining email responses** to customer complaints.

### 📂 **Email Workflow Components**

\[
\begin{array}{|c|c|c|}
\hline
\textbf{File Name} & \textbf{Class Name} & \textbf{Functionality} \\
\hline
\texttt{email\_formation.py} & \texttt{email\_formation\_class} & Generates customer-facing email responses for complaints. \\
\hline
\texttt{email\_grading.py} & \texttt{email\_grading\_class} & Grades generated emails for accuracy, coverage, and clarity. \\
\hline
\texttt{email\_stategraph.py} & \texttt{email\_stategraph\_class} & LangGraph-based workflow for email formulation and validation. \\
\hline
\end{array}
\]

---

## 3️⃣ Core Components & Classes

The **Core Components** provide **database management, logging, regulation ingestion, and the main execution flow**.

### 📂 **Core Components & Classes**

\[
\begin{array}{|c|c|c|}
\hline
\textbf{File Name} & \textbf{Class Name} & \textbf{Functionality} \\
\hline
\texttt{CART.py} & \texttt{cart\_intersect\_class} & Main execution file integrating all workflows (complaint \& email). \\
\hline
\texttt{Cart\_App.py} & \texttt{CartApp} & Streamlit web UI for running CART interactively. \\
\hline
\texttt{database\_activity.py} & \texttt{database\_activity\_class} & Handles SQL Server interactions: log management, data ingestion, and report updates. \\
\hline
\texttt{logger.py} & \texttt{Logger} & Centralized logging to track execution flow and errors. \\
\hline
\texttt{regulation\_text\_ingestion.py} & \texttt{regulation\_ingestion\_class} & Loads and vectorizes regulation PDFs into ChromaDB for retrieval. \\
\hline
\end{array}
\]

---

## 🚀 **Cart 2.0 Overview**
✅ **CART integrates complaint and email workflows**  
✅ **Streamlit UI for easy execution**  
✅ **SQL database logging and reporting**  
✅ **Regulation PDF ingestion for document retrieval**  
✅ **Centralized logging to track execution flow**  

---

This documentation provides an **organized summary** of all **Cart 2.0 workflows** and **core components**. 🚀 Save it in **GitHub README.md** using LaTeX syntax for **better readability**.
