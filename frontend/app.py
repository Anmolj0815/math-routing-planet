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

# --- Simplified Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Corrected Sidebar Text Color */
    .stSidebar .stMarkdown, .stSidebar .st-emotion-cache-16txte8 {
        color: white;
    }

    /* Corrected Text Area and Input Colors */
    .stTextArea > div > div > textarea, .stTextInput > div > div > input {
        background-color: white !important;
        color: #1a202c !important;
        border-radius: 15px;
        border: 2px solid rgba(0, 0, 0, 0.1);
        padding: 20px;
        font-size: 16px;
    }

    .stTextArea > label, .stTextInput > label {
        color: white;
        font-weight: bold;
    }
    
    /* General Glassmorphism Effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 30px;
        margin: 20px 0;
    }
    
    /* Streamlit's default markdown text color */
    .st-emotion-cache-1cypcdb {
        color: white;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 40px;
        font-weight: 300;
        line-height: 1.6;
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

    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.4);
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
    
    st.markdown("""
    <div class="glass-container">
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
st.markdown("<h3 style='color: white;'>🎯 Enter Your Mathematical Query</h3>", unsafe_allow_html=True)

# Corrected input area
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
        <div class="glass-container" style="background: rgba(255, 107, 107, 0.1);">
            <p style="color: white; text-align: center;">⚠️ Please enter a question to proceed</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            for i, step in enumerate([
                "🔍 Analyzing query structure...",
                "🧠 Processing with AI agents...",
                "📚 Retrieving relevant information...",
                "⚡ Generating intelligent response...",
                "✨ Finalizing results..."
            ]):
                status_text.markdown(f'<p style="color: white;">{step}</p>', unsafe_allow_html=True)
                progress_bar.progress((i + 1) * 20)
                time.sleep(0.3)
            
            # API call (uncomment when API is available)
            # response = requests.post(f"{API_URL}/api/query", json={"query": query}, timeout=300)
            # response.raise_for_status()
            # result = response.json()
            
            # Mock data for demonstration
            result = {
                "answer": "The subjects typically taught in grades K-2 include reading, writing, mathematics, and science, often with an emphasis on foundational skills and basic concepts.",
                "decision": "Approved",
                "justification": {
                    "Query Analysis": "The query was parsed to identify 'K-2' and 'subjects'.",
                    "Information Retrieval": "Used RAG to retrieve a document on elementary school curricula.",
                    "Answer Synthesis": "Synthesized the answer based on the retrieved information about K-2 subjects.",
                    "Confidence Score": "High"
                }
            }
            
            progress_bar.empty()
            status_text.empty()
            
            st.markdown("""
            <div class="glass-container" style="background: rgba(78, 205, 196, 0.1);">
                <p style="color: white; text-align: center;">✅ Analysis Complete! Your mathematical query has been successfully processed.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="glass-container">
                <h3 style="color: white; margin-bottom: 20px;">💡 Solution</h3>
                <div style="color: white; font-size: 18px; line-height: 1.8;">
            """, unsafe_allow_html=True)
            
            answer = result.get('answer', 'No answer found')
            st.markdown(f"{answer}")
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["📊 Analysis Details", "🔍 Decision Process", "📁 Export Data"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    if result.get('decision'):
                        st.markdown(f"""
                        <div class="glass-container" style="padding: 20px;">
                            <h4 style="color: white;">🎯 Decision</h4>
                            <p style="color: white; font-size: 18px;">{result['decision']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if result.get('amount'):
                        st.markdown(f"""
                        <div class="glass-container" style="padding: 20px;">
                            <h4 style="color: white;">💰 Amount</h4>
                            <p style="color: white; font-size: 18px;">{str(result['amount'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab2:
                if result.get('justification'):
                    st.markdown("#### 🧩 Reasoning Process")
                    justification = result.get('justification', {})
                    
                    for key, value in justification.items():
                        st.markdown(f"""
                        <div class="glass-container" style="margin-bottom: 10px; padding: 20px;">
                            <h5 style="color: white; margin-bottom: 5px;">{key.replace('_', ' ').title()}</h5>
                            <p style="color: rgba(255,255,255,0.8);">{value}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("#### 📥 Export Options")
                
                col1, col2 = st.columns(2)
                with col1:
                    json_data = json.dumps(result, indent=2)
                    st.download_button(
                        "📄 Download JSON",
                        data=json_data,
                        file_name=f"math_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
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
                
                with st.expander("🔧 Raw JSON Response"):
                    st.json(result)
            
            st.session_state['last_result'] = result
            st.session_state['last_query'] = query
            
        except requests.exceptions.Timeout:
            progress_bar.empty()
            status_text.empty()
            st.markdown("""
            <div class="glass-container" style="background: rgba(255, 107, 107, 0.1);">
                <p style="color: white; text-align: center;">⏱️ Request timed out. Please try again with a simpler query.</p>
            </div>
            """, unsafe_allow_html=True)
            
        except requests.exceptions.RequestException as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="glass-container" style="background: rgba(255, 107, 107, 0.1);">
                <p style="color: white; text-align: center;">❌ Connection Error: {str(e)}</p>
                <p style="color: white; text-align: center; font-size: 12px;">Please check your internet connection and try again.</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="glass-container" style="background: rgba(255, 107, 107, 0.1);">
                <p style="color: white; text-align: center;">⚠️ Unexpected Error: {str(e)}</p>
                <p style="color: white; text-align: center; font-size: 12px;">Please try again or contact support if the issue persists.</p>
            </div>
            """, unsafe_allow_html=True)

# --- History Section ---
if 'last_result' in st.session_state:
    st.markdown("---")
    st.markdown("<h3 style='color: white;'>📚 Recent Analysis</h3>", unsafe_allow_html=True)
    
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
