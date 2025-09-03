import streamlit as st
import requests
import json
import os

API_URL = os.getenv('API_URL', 'https://math-routing-planet-backend.onrender.com')

# --- UI Improvements: Set Page Configuration and Custom CSS ---
st.set_page_config(
    page_title="Math Agentic-RAG System", 
    page_icon="🧮", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a polished look
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6; /* Light gray background */
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #4CAF50;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: white;
        color: #4CAF50;
        border: 2px solid #4CAF50;
    }
    .stButton>button:active {
        background-color: #3e8e41;
        color: white;
    }
    .stTextarea {
        border-radius: 8px;
        padding: 10px;
    }
    .st-emotion-cache-1c7y39f {
        font-size: 32px;
        font-weight: 600;
        color: #333333;
        text-align: center;
        margin-bottom: 20px;
        padding-top: 20px;
    }
    .st-emotion-cache-1v0x7c2 {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    .success-box {
        background-color: #e6f7e9;
        color: #2e7d32;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #c8e6c9;
        margin-top: 20px;
    }
    .error-box {
        background-color: #fde8e8;
        color: #d32f2f;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #f9c0c0;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Layout: Main Content Area ---
st.title("🧮 Math Agentic-RAG System")

st.markdown("### The system is built on the architecture you outlined on [2025-07-25], which parses and structures natural language queries to retrieve relevant information from unstructured documents. This allows for a robust and explainable decision-making process.")

# Use a container to create a visually distinct section for the input
with st.container(border=True):
    query = st.text_area(
        "Enter your math question:",
        placeholder="e.g., What are the subjects of K-2?",
        height=150
    )

    # Use columns to align the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Solve", use_container_width=True):
            if not query.strip():
                st.warning("⚠️ Please enter a question")
            else:
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = requests.post(f"{API_URL}/api/query", json={"query": query}, timeout=300)
                        response.raise_for_status()
                        result = response.json()
                        st.success("✅ Answer Generated")
                        st.markdown(f"**Answer:**\n\n{result.get('answer', 'No answer found')}")
                        
                        # Add download button in a separate row for clarity
                        st.download_button("📥 Download JSON", data=json.dumps(result, indent=2), file_name="response.json")

                    except Exception as e:
                        st.error(f"❌ API Error: {str(e)}")

st.divider()

# --- UI Improvements: Result Display Area ---
st.markdown("### Decision Details")

if 'result' in locals() and result:
    with st.expander("Show Justification and Structured Data"):
        if result.get('decision'):
            st.markdown(f"**Decision:** {result['decision']}")
            if result.get('amount'):
                st.markdown(f"**Amount:** {result['amount']}")
            
            # Display justification with enhanced formatting
            st.markdown("#### Justification")
            justification = result.get('justification', {})
            for key, value in justification.items():
                st.markdown(f"**- {key}:** {value}")

            # Display the raw JSON for auditability
            st.markdown("#### Full JSON Response")
            st.json(result)
else:
    st.info("The detailed decision and justification will appear here after a query is processed.")
