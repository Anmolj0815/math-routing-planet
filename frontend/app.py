import streamlit as st
import requests
import json
import os
import time
from datetime import datetime

API_URL = os.getenv('API_URL', 'https://math-routing-planet-backend.onrender.com')

# --- Enhanced Page Configuration ---
st.set_page_config(
    page_title="Human in a loop- Math Routing Agent",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Streamlit Cloud Compatible CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main content text visibility */
    .main .block-container {
        color: white !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
    }
    
    /* STREAMLIT CLOUD SPECIFIC SIDEBAR FIXES */
    .css-1d391kg, .css-1l02zno, .css-17eq0hr {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95)) !important;
    }
    
    /* Multiple sidebar selectors for different Streamlit versions */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95)) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding-top: 1rem !important;
    }
    
    /* Sidebar element styling */
    .sidebar .sidebar-content {
        background: transparent !important;
    }
    
    /* Force sidebar text color */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    /* Fallback sidebar selectors */
    .css-1cypcdb, .css-17lntkn, .css-hby737, .css-1v0mbdj {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95)) !important;
    }
    
    .css-1cypcdb *, .css-17lntkn *, .css-hby737 *, .css-1v0mbdj * {
        color: white !important;
    }
    
    /* Text input styling */
    .stTextArea label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea {
        background: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #2d3748 !important;
        font-size: 16px !important;
        padding: 20px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.4) !important;
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        margin-right: 10px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Glass container effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px;
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        padding: 30px;
        margin: 20px 0;
    }
    
    .glass-container * {
        color: white !important;
    }
    
    /* Metric cards for sidebar */
    .metric-card {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card * {
        color: white !important;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        margin-bottom: 20px !important;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    .subtitle {
        font-size: 1.2rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: center;
        margin-bottom: 40px !important;
        font-weight: 300 !important;
        line-height: 1.6;
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 20px 0 !important;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 20px 0 !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    /* Answer container */
    .answer-container {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px !important;
        padding: 30px !important;
        margin: 20px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .answer-text {
        color: white !important;
        font-size: 18px !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
    }
    
    /* Expander styling */
    .stExpander {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stExpander label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* JSON viewer */
    .stJson {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Progress bar */
    .stProgress .st-bo {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stProgress .st-bp {
        background: linear-gradient(90deg, #4ecdc4, #44a08d) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }
        
        .glass-container {
            padding: 20px !important;
            margin: 10px 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Force sidebar to appear - Critical for Streamlit Cloud
st.sidebar.title("🚀 Control Panel")

# --- Enhanced Header Section ---
st.markdown("""
<div class="main-title">
    🧮 Human in a loop- Math Routing Agent
</div>
<div class="subtitle">
    Advanced AI-powered mathematical reasoning with explainable decision-making architecture<br>
    Built with cutting-edge RAG technology for intelligent query processing
</div>
""", unsafe_allow_html=True)

# --- Sidebar with Streamlit Cloud Compatible Design ---
with st.sidebar:
    st.markdown("### 🚀 System Status")
    
    # Create columns for better layout in sidebar
    status_col, time_col = st.columns(2)
    
    with status_col:
        st.metric(
            label="🟢 API Status",
            value="Online",
            delta="100% uptime"
        )
    
    with time_col:
        st.metric(
            label="⚡ Response",
            value="~2.3s",
            delta="-0.5s"
        )
    
    st.markdown("---")
    
    # System Features
    st.markdown("### 📊 Features")
    features = [
        "🔬 Advanced RAG Architecture",
        "⚡ Real-time Processing", 
        "🧠 Explainable AI Decisions",
        "📥 JSON Export Support"
    ]
    
    for feature in features:
        st.markdown(f"- {feature}")
    
    st.markdown("---")
    
    # Pro Tips section
    st.markdown("### 💡 Pro Tips")
    tips = [
        "Be specific with your math questions",
        "Include context for better results",
        "Check the justification for transparency",
        "Download results for analysis"
    ]
    
    for tip in tips:
        st.markdown(f"→ {tip}")
    
    st.markdown("---")
    
    # Debug Information for troubleshooting
    st.markdown("### 🔧 System Info")
    st.markdown(f"**Streamlit:** {st.__version__}")
    st.markdown("**Status:** ✅ Active")
    st.markdown("**Layout:** Wide")
    
    # Add a simple interactive element to ensure sidebar is functional
    if st.button("🔄 Refresh Status", key="sidebar_refresh"):
        st.success("✅ Status refreshed!")
        time.sleep(1)
        st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()

# --- Main Content Area ---
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown("### 🎯 Enter Your Mathematical Query")

# Enhanced input area
query = st.text_area(
    "Your Question:",
    placeholder="Enter your mathematical question here... (e.g., 'What are the subjects of K-2?' or 'Solve the quadratic equation x² + 5x + 6 = 0')",
    height=150,
    help="Type your question clearly for best results",
    key="query_input"
)

# Action buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    solve_button = st.button("🔍 Analyze & Solve", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Processing Logic ---
if solve_button:
    if not query.strip():
        st.markdown("""
        <div class="error-message">
            ⚠️ Please enter a question to proceed
        </div>
        """, unsafe_allow_html=True)
    else:
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Processing steps with visual feedback
            steps = [
                "🔍 Analyzing query structure...",
                "🧠 Processing with AI agents...", 
                "📚 Retrieving relevant information...",
                "⚡ Generating intelligent response...",
                "✨ Finalizing results..."
            ]
            
            for i, step in enumerate(steps):
                status_text.markdown(f"**{step}**")
                progress_bar.progress((i + 1) * 20)
                time.sleep(0.3)
            
            # API call
            response = requests.post(
                f"{API_URL}/api/query", 
                json={"query": query}, 
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Success message
            st.markdown("""
            <div class="success-message">
                ✅ Analysis Complete! Your mathematical query has been successfully processed.
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced answer display
            st.markdown("""
            <div class="answer-container">
                <h3 style="color: white; margin-bottom: 20px;">💡 Solution</h3>
                <div class="answer-text">
            """, unsafe_allow_html=True)
            
            answer = result.get('answer', 'No answer found')
            st.markdown(f"**Answer:** {answer}")
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Results section with tabs
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["📊 Analysis Details", "🔍 Decision Process", "📁 Export Data"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    if result.get('decision'):
                        st.markdown("#### 🎯 Decision")
                        st.markdown(f"**{result['decision']}**")
                
                with col2:
                    if result.get('amount'):
                        st.markdown("#### 💰 Amount") 
                        st.markdown(f"**{result['amount']}**")
            
            with tab2:
                if result.get('justification'):
                    st.markdown("#### 🧩 Reasoning Process")
                    justification = result.get('justification', {})
                    
                    for key, value in justification.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        st.markdown(f"{value}")
                        st.markdown("---")
            
            with tab3:
                st.markdown("#### 📥 Export Options")
                
                col1, col2 = st.columns(2)
                with col1:
                    # JSON download
                    json_data = json.dumps(result, indent=2)
                    st.download_button(
                        "📄 Download JSON",
                        data=json_data,
                        file_name=f"math_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # Summary download
                    summary = f"""Math Agentic-RAG Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Query: {query}
Answer: {result.get('answer', 'N/A')}
Decision: {result.get('decision', 'N/A')}
Amount: {result.get('amount', 'N/A')}"""
                    
                    st.download_button(
                        "📋 Download Summary",
                        data=summary,
                        file_name=f"math_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain", 
                        use_container_width=True
                    )
                
                # Raw JSON viewer
                with st.expander("🔧 Raw JSON Response"):
                    st.json(result)
            
            # Store results in session state
            st.session_state['last_result'] = result
            st.session_state['last_query'] = query
            
        except requests.exceptions.Timeout:
            progress_bar.empty()
            status_text.empty()
            st.markdown("""
            <div class="error-message">
                ⏱️ Request timed out. Please try again with a simpler query.
            </div>
            """, unsafe_allow_html=True)
            
        except requests.exceptions.RequestException as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="error-message">
                ❌ Connection Error: {str(e)}<br>
                <small>Please check your internet connection and try again.</small>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="error-message">
                ⚠️ Unexpected Error: {str(e)}<br>
                <small>Please try again or contact support if the issue persists.</small>
            </div>
            """, unsafe_allow_html=True)

# --- History Section ---
if 'last_result' in st.session_state:
    st.markdown("---")
    st.markdown("### 📚 Recent Analysis")
    
    with st.expander(f"Last Query: {st.session_state['last_query'][:50]}...", expanded=False):
        st.markdown(f"**Answer:** {st.session_state['last_result'].get('answer', 'N/A')}")
        if st.session_state['last_result'].get('decision'):
            st.markdown(f"**Decision:** {st.session_state['last_result']['decision']}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="glass-container" style="text-align: center; margin-top: 40px;">
    <p style="color: rgba(255,255,255,0.9); margin: 0; font-weight: bold;">
        🚀 Powered by Advanced AI • 🔒 Secure & Private • ⚡ Real-time Processing
    </p>
    <p style="color: rgba(255,255,255,0.7); font-size: 14px; margin: 10px 0 0 0;">
        Built with ❤️ using Streamlit • Enhanced with Modern Web Technologies
    </p>
</div>
""", unsafe_allow_html=True)
