import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE GLOBAL TEMA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. DİL SÖZLÜĞÜ (LOCALIZATION) ---
# Sol menüden seçilen dile göre tüm arayüz değişecek
if 'lang' not in st.session_state:
    st.session_state.lang = "Türkçe"

with st.sidebar:
    st.title("🌐 Language")
    selected_lang = st.radio("Select Language / Dil Seçin", ["Türkçe", "English"])
    st.session_state.lang = selected_lang
    st.divider()
    st.caption("Dev: Hilal Erol | v4.0 Multi-Lang Executive")

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU",
        "sub": "STRATEJİK RİSK VE ARKETİP ANALİZİ",
        "placeholder": "Analiz edilecek senaryoyu girin...",
        "label": "Sistem Zafiyetleri:",
        "options": ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme", "Duygusallık"],
        "button": "ANALİZİ BAŞLAT",
        "working": "Kınik zekâ verileri işliyor...",
        "prompt": "Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Lütfen Türkçe ve ekonomi diliyle, dürüst ve sert bir risk analizi yap."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "STRATEGIC RISK & ARCHETYPAL ANALYSIS",
        "placeholder": "Enter the scenario to analyze...",
        "label": "Systemic Weaknesses:",
        "options": ["Indiscipline", "Panic", "Indecisiveness", "Procrastination", "Emotionality"],
        "button": "START ANALYSIS",
        "working": "The Cynic is processing data...",
        "prompt": "You are The Cynic's Tarot. You are a sharp analyst with an economics background. Please provide an honest, harsh, and strategic risk analysis in English using economic terminology."
    }
}

L = texts[st.session_state.lang]

# --- 3. ULTRA MODERN CSS (HATA ÖNLEYİCİ) ---
st.markdown(f"""
    <style>
    /* Ana Arka Plan */
    .stApp {{
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #ffffff;
    }}
    
    /* Başlık Tasarımları */
    .main-title {{
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: 8px;
        text-align: center;
        color: #ffffff;
        text-transform: uppercase;
        padding-top: 10px;
    }}
    .sub-title {{
        text-align: center;
        color: #666;
        font-size: 0.8em;
        letter-spacing: 3px;
        margin-bottom: 40px;
    }}

    /* YAZI KUTUSU DÜZELTME (Beyaz zemin sorununu çözer) */
