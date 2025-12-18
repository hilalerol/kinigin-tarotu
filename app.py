import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- 1. SAYFA VE GLOBAL TEMA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. DİL AYARLARI ---
if 'lang' not in st.session_state:
    st.session_state.lang = "Türkçe"

with st.sidebar:
    st.title("🌐 Language")
    selected_lang = st.radio("Select Language / Dil Seçin", ["Türkçe", "English"])
    st.session_state.lang = selected_lang
    st.divider()
    st.caption("Dev: Hilal Erol | v5.0 Platinum Edition")

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU",
        "sub": "STRATEJİK RİSK VE ARKETİP ANALİZİ",
        "placeholder": "Analiz edilecek senaryoyu girin...",
        "label": "Sistem Zafiyetleri:",
        "options": ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme", "Duygusallık"],
        "button": "ANALİZİ BAŞLAT",
        "working": "Kınik zekâ verileri işliyor...",
        "pdf_btn": "📄 Raporu PDF Olarak İndir",
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
        "pdf_btn": "📄 Download PDF Report",
        "prompt": "You are The Cynic's Tarot. You are a sharp analyst with an economics background. Please provide an honest, harsh, and strategic risk analysis in English using economic terminology."
    }
}

L = texts[st.session_state.lang]

# --- 3. CSS (TASARIM) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: #ffffff; }
    .main-title { font-family: 'Helvetica Neue', sans-serif; font-weight: 800; letter-spacing: 8px; text-align: center; color: #ffffff; text-transform: uppercase; padding-top: 10px; }
    .sub-title { text-align: center; color: #666; font-size: 0.8em; letter-spacing: 3px; margin-bottom: 40px; }
    .stTextInput div[data-baseweb="input"] { background-color: #1a1c23 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 12px !important; }
    .stTextInput input { color: #ffffff !important; }
    .stMultiSelect div[data-baseweb="select"] { background-color: #1a1c23 !important; border-radius: 12px !important; }
    .stButton button { width: 100%; background: linear-gradient(45deg, #333, #000) !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 25px !important; font-weight: bold !important; letter-spacing: 2px !important; height: 3.5em !important; }
    .stButton button:hover { background: #ffffff !important; color: #000000 !important; }
    .report-box { background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px; border: 1px solid rgba(255, 255, 255, 0.07); line-height: 1.8; font-family: 'Georgia', serif; color: #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PDF OLUŞTURMA FONKSİYONU ---
def create_pdf(text, language):
    pdf = FPDF()
    pdf.add_page()
    # Unicode desteklemediği için standart fontu kullanıyoruz
    pdf.set_font("Arial", 'B', 16)
    
    title = "KINIGIN TAROTU - RISK RAPORU" if language == "Türkçe" else "THE CYNIC'S TAROT - RISK REPORT"
    pdf.cell(190, 10, title, ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    
    # TÜRKÇE KARAKTER DÜZELTME TABLOSU
    # Latin-1 uyumlu hale getiriyoruz
    tr_map = {
        "ş": "s", "Ş": "S", "ı": "i", "İ": "I", "ğ": "g", "Ğ": "G", 
        "ü": "u", "Ü": "U", "ö": "o", "Ö": "O", "ç": "c", "Ç": "C"
    }
    
    clean_text = text
    for tr_char, en_char in tr_map.items():
        clean_text = clean_text.replace(tr_char, en_char)
    
    # Latin-1'e güvenli çeviri
    safe_text = clean_text.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.multi_cell(0, 10, safe_text)
    return pdf.output(dest="S")

# --- 5. API VE MODEL ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

@st.cache_resource
def load_model():
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in available if '1.5-flash' in m), available[0])
        return genai.GenerativeModel(target)
    except:
        return genai.GenerativeModel('gemini-pro')

model = load_model()

# --- 6. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{L["sub"]}</p>', unsafe_allow_html=True)

c1, col_main, c3 = st.columns([1, 2, 1])
with col_main:
    soru = st.text_input("", placeholder=L["placeholder"])
    zafiyetler = st.multiselect(L["label"], L["options"])
    
    if st.button(L["button"]):
        if soru:
            with st.spinner(L["working"]):
                try:
                    full_prompt = f"{L['prompt']} Soru: {soru}. Zayıflıklar: {zafiyetler}. 3 kartla ekonomi terminolojisi kullanarak analiz et."
                    response = model.generate_content(full_prompt)
                    report_text = response.text
                    
                    # Sonucu Ekrana Bas
                    st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
                    
                    # PDF İndirme Butonu
                    pdf_output = create_pdf(report_text, st.session_state.lang)
                    st.download_button(
                        label=L["pdf_btn"],
                        data=pdf_output,
                        file_name="Cynic_Risk_Report.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Lütfen giriş yapın.")
