import sys
import os
import streamlit as st
import pandas as pd
from io import StringIO


from CART import cart_intersect_class  # Import the CART class
from logger import Logger



# Configure the page
st.set_page_config(
    page_title="CART 2.0 - Complaint Review Tool",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for artistic styling
st.markdown(
            """
            <style>
                .stApp {
                    background: linear-gradient(to right, #2b5876, #4e4376);
                    color: white;
                }
                .css-1d391kg {
                    background: #1f1f1f !important;
                    color: white !important;
                }
                .main-header {
                    font-size: 40px !important;
                    font-weight: bold;
                    text-align: center;
                    color: #ffffff;
                    padding: 20px;
                }
                .stButton>button {
                    background-color: #ff9800 !important;
                    color: white !important;
                    font-size: 18px !important;
                    border-radius: 8px !important;
                }
                .dataframe {
                    background-color: white !important;
                    border-radius: 10px !important;
                    padding: 10px !important;
                    color: black !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

# App Header
st.markdown('<h1 class="main-header">CART 2.0 - Complaint Review Tool ⚖️</h1>', unsafe_allow_html=True)

# **🔄 Capture Print Statements in Streamlit UI**
class StreamlitStdout:
    def __init__(self, text_area):
        self.text_area = text_area
        self.buffer = StringIO()

    def write(self, message):
        """Redirect print() output to Streamlit UI"""
        if message.strip():
            self.buffer.write(message + "\n")
            self.text_area.text(self.buffer.getvalue())

    def flush(self):
        pass  # Required for sys.stdout override

# **Streamlit App Class**
class CartApp:
    def __init__(self):
        """Initialize the Streamlit App"""
        self.company            = "NAVY FEDERAL CREDIT UNION"
        self.total_records      = 5
        self.date_received_min  = pd.to_datetime("2024-03-01")
        self.date_received_max  = pd.to_datetime("2024-03-31")
        self.groq_models        = [    
                                        "llama3-70b-8192",
                                        "llama-3.3-70b-versatile",
                                        "qwen-2.5-32b"
                                  ]
        self.llm_model          = self.groq_models[0]  # Default Model
        self.logger_obj         = Logger()

        # **📌 Create a UI Text Area for Print Outputs**
        self.output_area        = st.empty()
        sys.stdout              = StreamlitStdout(self.output_area)  # Redirect print() output

    def sidebar_inputs(self):
        """Sidebar inputs for user interaction"""
        with st.sidebar:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/CFPB_logo.svg/1200px-CFPB_logo.svg.png", width=120)
            st.sidebar.header("🔹 Input Parameters")

            self.company           = st.text_input("🏢 Enter Company Name", self.company)
            self.total_records     = st.number_input("📊 Enter Number of Complaints", min_value=1, max_value=1000, value=self.total_records, step=1)
            self.date_received_min = st.date_input("📅 Start Date", self.date_received_min)
            self.date_received_max = st.date_input("📅 End Date", self.date_received_max)
            self.llm_model         = st.selectbox("🤖 Choose LLM Model", self.groq_models, index=0)

            # Stylized Run Button
            if st.button("🚀 Run CART "):
                self.run_cart()

    def run_cart(self):
        """Run the CART model"""
        st.subheader("🔍 Processing Complaints")
        print(f"Processing `{self.total_records}` complaints for **{self.company}** from `{self.date_received_min}` to `{self.date_received_max}` using `{self.llm_model}`")

        cart_intersect_class_obj = cart_intersect_class()

        with st.spinner("⏳ Running CART 2.0... Please wait "):
            print("Running CART 2.0 Model...")
            reviewed_complaint_df_final = cart_intersect_class_obj.run_cart(self.company, self.total_records, str(self.date_received_min), str(self.date_received_max), self.llm_model)

        if reviewed_complaint_df_final is not None and not reviewed_complaint_df_final.empty:
            print("✅ CART 2.0 Processing Completed!")
            st.write("### 📝 Reviewed Complaints")
            st.dataframe(reviewed_complaint_df_final.style.set_properties(**{"background-color": "white", "color": "white"}))
        else:
            print("⚠️ No complaints processed.")

    def show_footer(self):
        """Show the app footer"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("⚖️ **CART 2.0 - Powered by LangChain & Streamlit**")

    def run(self):
        """Run the Streamlit App"""
        self.sidebar_inputs()
        self.show_footer()

# Run the App
if __name__ == "__main__":
    app = CartApp()
    app.run()
