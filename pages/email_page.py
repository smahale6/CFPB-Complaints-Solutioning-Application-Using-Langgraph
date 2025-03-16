import streamlit as st
import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os

class email_viewer:
    def __init__(self):
        load_dotenv()  # Load environment variables from the .env file
        self.server = 'complaints-analytics.database.windows.net'
        self.database = 'Cart2.0'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.SQL_USER_NAME = os.getenv("SQL_USER_NAME")
        self.SQL_PASSWORD = os.getenv("SQL_PASSWORD")

    def get_db_connection(self):
        """Establish SQL Server connection"""
        conn = pyodbc.connect(f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;')
        return conn

    @staticmethod
    @st.cache_data
    def fetch_email_details(complaint_id):
        """Fetch complaint email details from SQL Server"""
        query = f"""
        SELECT Complaint_ID, Complaint_Text, Email_HTML
        FROM dbo.rpt_cfpb_complaints
        WHERE Complaint_ID = {complaint_id}
        """
        conn = pyodbc.connect(
                                f'DRIVER={"{ODBC Driver 17 for SQL Server}"};'
                                f'SERVER={"complaints-analytics.database.windows.net"};'
                                f'DATABASE={"Cart2.0"};'
                                f'UID={os.getenv("SQL_USER_NAME")};'
                                f'PWD={os.getenv("SQL_PASSWORD")};'
                                'Encrypt=yes;'
                                'TrustServerCertificate=no;'
                                'Connection Timeout=60;'
                            )
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def run(self):
        """Main function to display email details"""
        st.markdown('<h1 class="email-header">📧 Complaint Email Viewer</h1>', unsafe_allow_html=True)

        # ✅ FIX: Ensure correct query parameter handling
        query_params = st.query_params
        complaint_id = query_params.get("complaint_id", None)

        if complaint_id:
            st.write(f"Debug: Received Complaint_ID = {complaint_id}")  # Debugging Line

            df_email = self.fetch_email_details(complaint_id)
            if not df_email.empty:
                st.markdown(f"### 📝 Complaint ID: {df_email.iloc[0]['Complaint_ID']}")
                st.markdown("### 📝 Complaint Text:")
                st.write(df_email.iloc[0]["Complaint_Text"])

                st.markdown("### 📩 Email Response:")
                st.markdown(df_email.iloc[0]["Email_HTML"], unsafe_allow_html=True)

                # Back Button
                if st.button("🔙 Go Back to Dashboard"):
                    st.query_params.clear()

            else:
                st.error("⚠️ No email found for this complaint.")
        else:
            st.error("⚠️ No complaint ID provided.")

# Run Streamlit App
if __name__ == "__main__":
    app = email_viewer()
    app.run()
