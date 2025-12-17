import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# Klas & Modern CSS (Glassmorphism ve Executive Dark)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(row, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
    }
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: 8px;
        text-align: center;
        color: #ffffff;
        text-transform: uppercase;
        padding-top: 20px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 0.8em;
        letter-spacing: 3px;
        margin-bottom: 50px;
    }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    .stButton button {
        width: 100%;
        background: linear-gradient(45deg, #333, #000) !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        height: 3.5em !important;
        transition: 0.4s;
    }
    .stButton button:hover {
        background: #ffffff !important;
        color: #000000 !important;
    }
    .report-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        line-height: 1.8;
        font-family: 'Georgia', serif;
    }
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

@st.cache_resource
def load_dynamic_model():
    # 404 hatalarını önlemek için çalışan modelleri tara
    try:
        working_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
