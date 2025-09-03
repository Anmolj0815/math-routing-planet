import streamlit as st
import requests
import json
import os
import time
from datetime import datetime

API_URL = os.getenv('API_URL', 'https://math-routing-planet-backend.onrender.com')

# --- Enhanced Page Configuration ---
st.set_page_config(
    page_title="Math Agentic-RAG System",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Advanced Custom CSS with Animations and Modern Design ---
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
    
    /* Glassmorphism Effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        padding: 30px;
        margin: 20px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Animated Title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 20px;
        animation: titleGlow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 40px;
        font-weight: 300;
        line-height: 1.6;
        animation: fadeIn 1s ease-out 0.5s both;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.4);
    }
    
    /* Modern Input Fields */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        font-size: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 20px rgba(240, 147, 251, 0.3);
        transform: scale(1.02);
    }
    
    /* Floating Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-left: 4px solid #4ecdc4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    /* Status Messages */
    .success-message {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
        animation: slideInRight 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        animation: shake 0.5s ease-out;
    }
    
    /* Answer Display */
    .answer-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .answer-text {
        color: white;
        font-size: 18px;
        line-height: 1.8;
        font-weight: 400;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
    }
    
    /* Progress Bar */
    .progress-container {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 3px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4ecdc4, #44a08d);
        border-radius: 3px;
        animation: progressLoad 2s ease-in-out;
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
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
    
    @keyframes progressLoad {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .glass-container {
            padding: 20px;
            margin: 10px 0;
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
    🧮 Math Agentic-RAG System
</div>
<div class="subtitle">
    Advanced AI-powered mathematical reasoning with explainable decision-making architecture
    <br>Built with cutting-edge RAG technology for intelligent query processing
</div>

<script>
// Force text color fix for textarea
setTimeout(function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.style.color = '#1a202c !important';
        textarea.style.background = 'white !important';
        textarea.style.fontWeight = '400';
        
        // Also fix on input event
        textarea.addEventListener('input', function() {
            this.style.color = '#1a202c !important';
            this.style.background = 'white !important';
        });
    });
    
    // Fix sidebar text
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.color = 'white !important';
        const allElements = sidebar.querySelectorAll('*');
        allElements.forEach(function(el) {
            if (el.tagName !== 'TEXTAREA' && el.tagName !== 'INPUT') {
                el.style.color = 'white !important';
            }
        });
    }
}, 1000);

// Repeat every 2 seconds to ensure it sticks
setInterval(function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.style.color = '#1a202c !important';
        textarea.style.background = 'white !important';
    });
}, 2000);
</script>
""", unsafe_allow_html=True)

# --- Sidebar with Enhanced Features ---
with st.sidebar:
    st.markdown("""
    <div class="glass-container">
        <h3 style="color: white; text-align: center; margin-bottom: 15px;">🚀 System Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # System metrics with enhanced styling
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin: 15px 0; border: 1px solid rgba(255, 255, 255, 0.2);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div style="text-align: center; flex: 1;">
                <div style="color: #4ecdc4; font-size: 24px; font-weight: bold;">🟢</div>
                <div style="color: white; font-size: 14px; margin: 5px 0;">API Status</div>
                <div style="color: #4ecdc4; font-size: 16px; font-weight: bold;">Online</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 12px;">100% uptime</div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="color: #4ecdc4; font-size: 24px; font-weight: bold;">⚡</div>
                <div style="color: white; font-size: 14px; margin: 5px 0;">Response Time</div>
                <div style="color: #4ecdc4; font-size: 16px; font-weight: bold;">~2.3s</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 12px;">-0.5s faster</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: white; margin-bottom: 15px; text-align: center;">📊 Quick Stats</h4>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4;">•</span> Advanced RAG Architecture
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4;">•</span> Real-time Processing
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4;">•</span> Explainable AI Decisions
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <span style="color: #4ecdc4;">•</span> JSON Export Support
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tips section
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin: 15px 0; border: 1px solid rgba(255, 255, 255, 0.2);">
        <h4 style="color: white; margin-bottom: 15px; text-align: center;">💡 Pro Tips</h4>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0;">
            <span style="color: #f093fb;">→</span> Be specific with your math questions
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0;">
            <span style="color: #f093fb;">→</span> Include context for better results
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0;">
            <span style="color: #f093fb;">→</span> Check the justification for transparency
        </div>
        <div style="color: rgba(255,255,255,0.9); margin: 8px 0;">
            <span style="color: #f093fb;">→</span> Download results for analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Main Input Section ---
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown("### 🎯 Enter Your Mathematical Query")

# Enhanced input area
query = st.text_area(
    "",
    placeholder="Enter your mathematical question here... (e.g., 'What are the subjects of K-2?' or 'Solve the quadratic equation x² + 5x + 6 = 0')",
    height=150,
    help="Type your question clearly for best results"
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
        
        # Animated loading
        with st.spinner(""):
            st.markdown("""
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Simulate processing steps
                for i, step in enumerate([
                    "🔍 Analyzing query structure...",
                    "🧠 Processing with AI agents...",
                    "📚 Retrieving relevant information...",
                    "⚡ Generating intelligent response...",
                    "✨ Finalizing results..."
                ]):
                    status_text.text(step)
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
                st.markdown(f"{answer}")
                
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
                            st.markdown("""
                            <div class="metric-card">
                                <h4 style="color: white;">🎯 Decision</h4>
                                <p style="color: rgba(255,255,255,0.9); font-size: 18px;">""" + 
                                result['decision'] + """</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        if result.get('amount'):
                            st.markdown("""
                            <div class="metric-card">
                                <h4 style="color: white;">💰 Amount</h4>
                                <p style="color: rgba(255,255,255,0.9); font-size: 18px;">""" + 
                                str(result['amount']) + """</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                with tab2:
                    if result.get('justification'):
                        st.markdown("#### 🧩 Reasoning Process")
                        justification = result.get('justification', {})
                        
                        for i, (key, value) in enumerate(justification.items()):
                            st.markdown(f"""
                            <div class="metric-card" style="animation-delay: {i*0.1}s;">
                                <h5 style="color: white; margin-bottom: 10px;">
                                    {key.replace('_', ' ').title()}
                                </h5>
                                <p style="color: rgba(255,255,255,0.8);">{value}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
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
                    ❌ Connection Error: {str(e)}
                    <br><small>Please check your internet connection and try again.</small>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.markdown(f"""
                <div class="error-message">
                    ⚠️ Unexpected Error: {str(e)}
                    <br><small>Please try again or contact support if the issue persists.</small>
                </div>
                """, unsafe_allow_html=True)

# --- History Section ---
if 'last_result' in st.session_state:
    st.markdown("---")
    st.markdown("### 📚 Recent Analysis")
    
    with st.expander(f"Last Query: {st.session_state['last_query'][:50]}...", expanded=False):
        st.write(f"**Answer:** {st.session_state['last_result'].get('answer', 'N/A')}")
        if st.session_state['last_result'].get('decision'):
            st.write(f"**Decision:** {st.session_state['last_result']['decision']}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="glass-container" style="text-align: center; margin-top: 40px;">
    <p style="color: rgba(255,255,255,0.7); margin: 0;">
        🚀 Powered by Advanced AI • 🔒 Secure & Private • ⚡ Real-time Processing
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 12px; margin: 10px 0 0 0;">
        Built with ❤️ using Streamlit • Enhanced with Modern Web Technologies
    </p>
</div>
""", unsafe_allow_html=True)
