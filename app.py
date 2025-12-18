import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE GLOBAL TEMA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. DİL SÖZLÜĞÜ ---
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

# --- 3. ULTRA MODERN CSS (HATA BURADAYDI, DÜZELTİLDİ) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #ffffff;
    }}
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
    .stTextInput div[data-baseweb="input"] {{
        background-color: #1a1c23 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }}
    .stTextInput input {{
        color: #ffffff !important;
        background-color: transparent !important;
    }}
    .stMultiSelect div[data-baseweb="select"] {{
        background-color: #1a1c23 !important;
        border-radius: 12px !important;
    }}
    .stButton button {{
        width: 100%;
        background: linear-gradient(45deg, #333, #000) !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        height: 3.5em !important;
    }}
    .report-box {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        line-height: 1.8;
        font-family: 'Georgia', serif;
        color: #e0e0e0;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. API VE MODEL KURULUMU ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

@st.cache_resource
def load_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in available if '1.5-flash' in m), available[0])
        return genai.GenerativeModel(target), target
    except:
        return genai.GenerativeModel('gemini-pro'), "gemini-pro"

model, model_name = load_model()

# --- 5. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{{L["title"]}}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{{L["sub"]}}</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    soru = st.text_input("", placeholder=L["placeholder"])
    zafiyetler = st.multiselect(L["label"], L["options"])
    
    st.write("")
    if st.button(L["button"]):
        if soru:
            with st.spinner(L["working"]):
                try:
                    full_prompt = f"{{L['prompt']}} Soru: {{soru}}. Zayıflıklar: {{zafiyetler}}."
                    response = model.generate_content(full_prompt)
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {{e}}")
