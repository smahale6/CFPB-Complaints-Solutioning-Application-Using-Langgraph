import streamlit as st
import pandas as pd
import pyodbc
import io
import base64  # ✅ Import base64 module
import os
from dotenv import load_dotenv

class cart_report_class:
    def __init__(self):
        load_dotenv()  # Load environment variables from the .env file
        self.server = 'complaints-analytics.database.windows.net'
        self.database = 'Cart2.0'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.SQL_USER_NAME = os.getenv("SQL_USER_NAME")
        self.SQL_PASSWORD = os.getenv("SQL_PASSWORD")

    def get_db_connection(self):
        """Establish SQL Server connection"""
        conn = pyodbc.connect(
            f'DRIVER={self.driver};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.SQL_USER_NAME};'
            f'PWD={self.SQL_PASSWORD};'
            'Encrypt=yes;'  # Ensure encryption is enabled for Azure SQL
            'TrustServerCertificate=no;'  # Recommended for security
            'Connection Timeout=60;'
        )
        return conn

    @staticmethod
    @st.cache_data
    def fetch_data():
        """Fetch complaint data from SQL Server"""
        query = """
        SELECT 
            Complaint_ID, Complaint_Text, Company, Date_Received, Product, Sub_Product, Issue, Sub_Issue,
            State, ZIP_Code, Summarized_Complaint, Total_Regulations,
            Regulation_Names, Explanations, Solutions
        FROM dbo.rpt_cfpb_complaints
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

    def apply_filters(self, df):
        """Apply sidebar filters (Complaint ID filter removed)"""
        with st.sidebar.expander("🔎 **Filter Complaints**", expanded=True):
            selected_product = st.selectbox("Product", ["All"] + sorted(df["Product"].dropna().unique().tolist()))
            selected_sub_product = st.selectbox("Sub-Product", ["All"] + sorted(df["Sub_Product"].dropna().unique().tolist()))
            selected_company = st.selectbox("Company", ["All"] + sorted(df["Company"].dropna().unique().tolist()))
            selected_state = st.selectbox("State", ["All"] + sorted(df["State"].dropna().unique().tolist()))

        if selected_product != "All":
            df = df[df["Product"] == selected_product]
        if selected_sub_product != "All":
            df = df[df["Sub_Product"] == selected_sub_product]
        if selected_company != "All":
            df = df[df["Company"] == selected_company]
        if selected_state != "All":
            df = df[df["State"] == selected_state]

        return df

    def add_email_link(self, df):
        """Add 'See Email' link column that redirects to email_page.py"""
        df["Link"] = df["Complaint_ID"].apply(lambda x: f'<a href="/email_page?complaint_id={x}" target="_self" style="color:#FF8C00;font-weight:bold;">See Email</a>')
        return df

    def export_to_excel(self, df):
        """Convert DataFrame to Excel and create a download button"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name="Complaints", index=False)
        output.seek(0)
        return output

    def generate_excel_download_link(self, df):
        """Generate a download link for the Excel file"""
        excel_file = self.export_to_excel(df)
        b64 = base64.b64encode(excel_file.read()).decode()  # ✅ Fix base64 encoding
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="complaints_report.xlsx" class="export-button">📥 Download Excel Report</a>'

    def apply_custom_css(self):
        """Apply custom CSS to bring main content very close to the sidebar"""
        st.markdown(
            """
            <style>
                .stApp {
                    background: linear-gradient(to right, #2b5876, #4e4376);
                    color: white;
                    padding: 0px !important;
                }
                /* ✅ Reduce Sidebar Width */
                .css-18e3th9 {
                    padding: 5px !important;
                    width: 12rem !important;
                }
                /* ✅ Bring main content very close to the sidebar */
                .block-container {
                    padding-top: 0rem !important;
                    padding-left: 0.5rem !important;
                    padding-right: 1rem !important;
                    margin-left: -2rem !important;
                    max-width: 1200px;
                }
                /* ✅ Adjust "Download Excel" button */
                .export-button {
                    display: inline-block;
                    background-color: #28a745;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 12px 20px;
                    border-radius: 8px;
                    text-align: center;
                    text-decoration: none;
                    margin-bottom: 15px;
                    transition: background-color 0.3s;
                }
                .export-button:hover {
                    background-color: #218838;
                    text-decoration: none;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

    def run(self):
        """Main function to run the Streamlit report"""
        self.apply_custom_css()

        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", width=100, use_container_width=False)  # Adjust width manually

        st.markdown('<h1 class="main-header">📊 Complaint Reporting Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("### Filter and explore consumer complaints with regulatory classifications and email responses.")

        # Decorative Image
        st.image("https://source.unsplash.com/1600x500/?business,technology", use_container_width=True, caption="Business and Technology Insights")

        # Load and filter data
        df = self.fetch_data()
        df = self.apply_filters(df)
        df = self.add_email_link(df)

        # Display the "Download Excel Report" Button
        st.markdown(self.generate_excel_download_link(df), unsafe_allow_html=True)

        # Convert DataFrame to HTML for proper rendering
        df_html = df.to_html(escape=False, index=False)

        # Display Table as HTML
        st.markdown("### Complaints Overview")
        st.markdown(df_html, unsafe_allow_html=True)

# Run Streamlit App
if __name__ == "__main__":
    app = cart_report_class()
    app.run()
