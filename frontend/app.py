import streamlit as st
import requests
import json
import os

API_URL = os.getenv('API_URL', 'https://math-routing-planet-backend.onrender.com')

st.set_page_config(page_title="Math Agentic-RAG System", page_icon="🧮", layout="wide")

st.title("🧮 Math Agentic-RAG System")

query = st.text_area("Enter your math question:", placeholder="e.g., What are the subjects of K-2?")

if st.button("🔍 Solve"):
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
                st.download_button("📥 Download JSON", data=json.dumps(result, indent=2), file_name="response.json")
            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")
