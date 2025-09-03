import streamlit as st
import requests
import json
import os
from typing import Optional, Dict, Any

# Configuration
API_URL = os.getenv('API_URL', 'https://math-routing-planet-backend.onrender.com')  # Replace with your backend URL

# Page config
st.set_page_config(
    page_title="Math Agentic-RAG System",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        color: #3f51b5;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #3f51b5;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #555;
        border-bottom: 2px solid #3f51b5;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .response-container {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #a5d6a7;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #3f51b5;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #303f9f;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def make_request(endpoint: str, data: Dict[Any, Any]) -> Optional[Dict]:
    """Make API request with error handling"""
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("Invalid response format from API")
        return None

def display_response(response_data: Dict):
    """Display formatted response data"""
    st.markdown('<div class="response-container">', unsafe_allow_html=True)

    # Decision
    decision_color = "#2e7d32" if response_data.get("decision") == "APPROVED" else "#d32f2f"
    st.markdown(f'<h3 style="color: {decision_color}; margin-top: 0;">Decision: {response_data.get("decision", "N/A")}</h3>', unsafe_allow_html=True)

    # Amount
    amount = response_data.get("amount")
    if amount is not None:
        st.markdown(f"**Amount:** ${amount:.2f}")
    else:
        st.markdown("**Amount:** N/A")

    # Justification
    justification = response_data.get("justification", "N/A")
    st.markdown(f"**Justification:** {justification}")

    # Clauses Used
    clauses = response_data.get("clauses_used", [])
    if clauses:
        st.markdown("**Clauses Used:**")
        for i, clause in enumerate(clauses, 1):
            st.markdown(f"{i}. {clause}")
    else:
        st.markdown("**Clauses Used:** None")

    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'response_data' not in st.session_state:
    st.session_state.response_data = None
if 'ingestion_success' not in st.session_state:
    st.session_state.ingestion_success = False

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🧮 Math Agentic-RAG System</h1>', unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        api_url_input = st.text_input(
            "Backend API URL",
            value=API_URL,
            help="Enter your backend API endpoint"
        )
        if api_url_input != API_URL:
            st.session_state.api_url = api_url_input

        st.markdown("### 📊 System Status")
        if st.session_state.ingestion_success:
            st.success("✅ Documents ingested successfully")
        else:
            st.info("ℹ️ No documents ingested yet")

    # Main content in tabs
    tab1, tab2 = st.tabs(["📄 Document Ingestion", "❓ Query System"])

    with tab1:
        st.markdown('<h2 class="section-header">📄 Ingest Documents</h2>', unsafe_allow_html=True)

        st.markdown("Upload PDF documents to the system for analysis. Enter comma-separated URLs of PDF documents.")

        # Document ingestion form
        with st.form("ingestion_form", clear_on_submit=False):
            urls_input = st.text_area(
                "PDF URLs (comma-separated)",
                placeholder="https://example.com/doc1.pdf, https://example.com/doc2.pdf",
                help="Enter one or more PDF URLs separated by commas",
                height=100
            )

            submitted = st.form_submit_button("🚀 Ingest Documents", use_container_width=True)

            if submitted:
                if not urls_input.strip():
                    st.warning("⚠️ Please enter at least one PDF URL")
                else:
                    urls = [url.strip() for url in urls_input.split(',') if url.strip()]

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    with st.spinner("🔄 Ingesting documents... This may take several minutes for large documents."):
                        status_text.text("Connecting to backend...")
                        progress_bar.progress(10)

                        response = make_request("/api/ingest", {"urls": urls})

                        progress_bar.progress(100)

                        if response:
                            st.session_state.ingestion_success = True
                            status_text.text("✅ Success!")
                            st.markdown('<div class="success-message">✅ Documents ingested successfully!</div>', unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.session_state.ingestion_success = False
                            status_text.text("❌ Failed!")
                            st.markdown('<div class="error-message">❌ Failed to ingest documents. Please check backend logs and try again.</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<h2 class="section-header">❓ Ask a Question</h2>', unsafe_allow_html=True)

        st.markdown("Ask questions about the ingested documents or general math queries.")

        # Query form
        with st.form("query_form", clear_on_submit=False):
            query_input = st.text_area(
                "Your Question",
                placeholder="e.g., What are the subjects of K-2?",
                height=120
            )

            # 🔥 New inputs for route + docs
            docs_input = st.text_area(
                "Extra Context Documents (comma separated, optional)",
                placeholder="Narendra Modi is the current Prime Minister of India., India is in Asia"
            )

            route_input = st.selectbox(
                "Choose Route",
                ["math_agent", "knowledge_base"]
            )

            submitted = st.form_submit_button("🔍 Get Decision", use_container_width=True)

            if submitted:
                if not query_input.strip():
                    st.warning("⚠️ Please enter a question")
                else:
                    with st.spinner("🤔 Analyzing your question..."):
                        payload = {
                            "query": query_input.strip(),
                            "documents": [d.strip() for d in docs_input.split(",")] if docs_input else [],
                            "route": route_input
                        }

                        response = make_request("/api/query", payload)

                        if response:
                            st.session_state.response_data = response
                        else:
                            st.session_state.response_data = None
                            st.markdown('<div class="error-message">❌ Failed to get response from the agent. Please try again.</div>', unsafe_allow_html=True)

        if st.session_state.response_data:
            st.markdown('<h2 class="section-header">🤖 Agent Response</h2>', unsafe_allow_html=True)
            display_response(st.session_state.response_data)

            st.download_button(
                label="📥 Download Response as JSON",
                data=json.dumps(st.session_state.response_data, indent=2),
                file_name="agent_response.json",
                mime="application/json",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
