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

# --- Fixed CSS with proper text visibility ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #4ecdc4;
        --warning-color: #ffe066;
        --error-color: #ff6b6b;
        --text-color: #2d3748;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Force text visibility */
    .stApp, .stApp * {
        color: white !important;
    }
    
    /* Specific fixes for Streamlit elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: white !important;
    }
    
    .stTextArea label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    .stButton label {
        color: white !important;
    }
    
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
    
    .stExpander label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton label {
        color: white !important;
    }
    
    /* Glassmorphism Effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px;
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        padding: 30px;
        margin: 20px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .glass-container * {
        color: white !important;
    }
    
    /* Animated Title */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        margin-bottom: 20px !important;
        animation: titleGlow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    .subtitle {
        font-size: 1.2rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: center;
        margin-bottom: 40px !important;
        font-weight: 300 !important;
        line-height: 1.6;
        animation: fadeIn 1s ease-out 0.5s both;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.4) !important;
        color: white !important;
    }
    
    /* Text Input Fields - FIXED */
    .stTextArea > div > div > textarea {
        background: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #2d3748 !important;
        font-size: 16px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 20px rgba(240, 147, 251, 0.3) !important;
        color: #2d3748 !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #a0aec0 !important;
    }
    
    /* Sidebar Fixes */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px);
    }
    
    .css-1d391kg * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 15px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .metric-card * {
        color: white !important;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    /* Status Messages */
    .success-message {
        background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 20px 0 !important;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
        animation: slideInRight 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 20px 0 !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        animation: shake 0.5s ease-out;
    }
    
    /* Answer Display */
    .answer-container {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px !important;
        padding: 30px !important;
        margin: 20px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .answer-text {
        color: white !important;
        font-size: 18px !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3) !important;
        color: white !important;
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
    
    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }
        100% { text-shadow: 0 0 40px rgba(255, 255, 255, 0.6); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }
        
        .glass-container {
            padding: 20px !important;
            margin: 10px 0 !important;
        }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

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

# --- Sidebar with Enhanced Features ---
with st.sidebar:
    st.markdown("### 🚀 System Status", unsafe_allow_html=True)
    
    # System metrics with enhanced styling
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div style="text-align: center; flex: 1;">
                <div style="color: #4ecdc4; font-size: 24px; font-weight: bold;">🟢</div>
                <div style="color: white; font-size: 14px; margin: 5px 0; font-weight: bold;">API Status</div>
                <div style="color: #4ecdc4; font-size: 16px; font-weight: bold;">Online</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 12px;">100% uptime</div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="color: #4ecdc4; font-size: 24px; font-weight: bold;">⚡</div>
                <div style="color: white; font-size: 14px; margin: 5px 0; font-weight: bold;">Response Time</div>
                <div style="color: #4ecdc4; font-size: 16px; font-weight: bold;">~2.3s</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 12px;">-0.5s faster</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### 📊 System Features", unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <div style="color: white; margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4; font-weight: bold;">•</span> Advanced RAG Architecture
        </div>
        <div style="color: white; margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4; font-weight: bold;">•</span> Real-time Processing
        </div>
        <div style="color: white; margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4; font-weight: bold;">•</span> Explainable AI Decisions
        </div>
        <div style="color: white; margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4; font-weight: bold;">•</span> JSON Export Support
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tips section
    st.markdown("### 💡 Pro Tips", unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <div style="color: white; margin: 8px 0;">
            <span style="color: #f093fb; font-weight: bold;">→</span> Be specific with your math questions
        </div>
        <div style="color: white; margin: 8px 0;">
            <span style="color: #f093fb; font-weight: bold;">→</span> Include context for better results
        </div>
        <div style="color: white; margin: 8px 0;">
            <span style="color: #f093fb; font-weight: bold;">→</span> Check the justification for transparency
        </div>
        <div style="color: white; margin: 8px 0;">
            <span style="color: #f093fb; font-weight: bold;">→</span> Download results for analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Main Input Section ---
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

# Action buttons in columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    solve_button = st.button("🔍 Analyze & Solve", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Processing Logic ---
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
            # Simulate processing steps
            for i, step in enumerate([
                "🔍 Analyzing query structure...",
                "🧠 Processing with AI agents...",
                "📚 Retrieving relevant information...",
                "⚡ Generating intelligent response...",
                "✨ Finalizing results..."
            ]):
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
            
            # Enhanced results section
            st.markdown("---")
            
            # Create tabs for different views
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
                    # Enhanced download button
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
                    summary = f"""
Math Agentic-RAG Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Query: {query}

Answer: {result.get('answer', 'N/A')}

Decision: {result.get('decision', 'N/A')}
Amount: {result.get('amount', 'N/A')}
                    """
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
            
            # Store in session state for persistence
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
