import streamlit as st
import google.generativeai as genai
import random
from fpdf import FPDF

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot Pro", page_icon="🔮", layout="wide")

# --- 2. 78 KARTLIK TAM DESTE ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "Türkçe"
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU",
        "sub": "78 Kartlık Desteden 3 Sembol Seç...",
        "placeholder": "Senaryonu buraya fısılda...",
        "btn_reveal": "KEHANETİ AÇ",
        "btn_reset": "YENİDEN BAŞLA",
        "pdf_btn": "📄 Analizi PDF Olarak İndir",
        "prompt": "Sen sert bir ekonomi analistisin. Soruya dürüst, stratejik ve acımasız bir analiz yap."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "Select 3 Symbols from the 78-Card Deck...",
        "placeholder": "Whisper your scenario here...",
        "btn_reveal": "REVEAL DESTINY",
        "btn_reset": "RESTART",
        "pdf_btn": "📄 Download Analysis as PDF",
        "prompt": "You are a harsh economic analyst. Provide a strategic, honest, and ruthless analysis for the question."
    }
}

with st.sidebar:
    st.title("🌐 Language")
    st.session_state.lang = st.radio("", ["Türkçe", "English"])
    st.divider()
    st.caption("Dev: Hilal Erol | v12.0 Final")

L = texts[st.session_state.lang]

# --- 4. PDF FONKSİYONU ---
def create_pdf(text, lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    title = "KİNİĞİN TAROTU - RAPOR" if lang == "Türkçe" else "THE CYNIC'S TAROT - REPORT"
    pdf.cell(190, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    tr_map = {"ş":"s","Ş":"S","ı":"i","İ":"I","ğ":"g","Ğ":"G","ü":"u","Ü":"U","ö":"o","Ö":"O","ç":"c","Ç":"C","\u2013":"-","*":"","#":""}
    clean_text = text
    for c, r in tr_map.items(): clean_text = clean_text.replace(c, r)
    safe_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    
    pdf.multi_cell(0, 10, safe_text)
    return pdf.output(dest="S").encode('latin-1')

# --- 5. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #ffffff; }}
    .main-title {{ font-family: serif; text-align: center; letter-spacing: 8px; color: #ffffff; }}
    .stButton button {{ background-color: #0a0a0a !important; border: 1px solid #333 !important; color: #555 !important; font-size: 16px !important; width: 100% !important; }}
    .stButton button:hover {{ border-color: #ff4b4b !important; color: white !important; }}
    .report-box {{ background: #0a0a0a; padding: 25px; border-radius: 15px; border: 1px solid #222; border-left: 5px solid #ff4b4b; color: #e0e0e0; margin-top: 20px; font-family: 'Georgia', serif; line-height: 1.8; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. API VE MODEL (HATA KORUMALI) ---
# SADECE BU KISMI GÜNCELLEMEN YETERLİ
genai.configure(api_key="AIzaSyC8knFCnlZI1EKpZnwmbNexMEH1fKPPMmk")
model = genai.GenerativeModel('gemini-pro') # En kararlı model budur

def generate_ai_response(prompt_text):
    # Sırasıyla çalışan modeli bulmaya çalışır
    for model_name in ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt_text)
            return response.text
        except Exception:
            continue
    return None

# --- 7. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#444;'>{L['sub']}</p>", unsafe_allow_html=True)

soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"### ✧ {len(st.session_state.secilen_indeksler)} / 3")
    for row in range(6):
        cols = st.columns(13)
        for col in range(13):
            idx = row * 13 + col
            if idx < 78:
                with cols[col]:
                    label = "❂" if idx in st.session_state.secilen_indeksler else "✧"
                    if st.button(label, key=f"k_{idx}"):
                        if idx not in st.session_state.secilen_indeksler and len(st.session_state.secilen_indeksler) < 3:
                            st.session_state.secilen_indeksler.append(idx)
                            st.rerun()
                        elif idx in st.session_state.secilen_indeksler:
                            st.session_state.secilen_indeksler.remove(idx)
                            st.rerun()

if len(st.session_state.secilen_indeksler) == 3 and not st.session_state.analiz_edildi:
    if st.button(L["btn_reveal"], use_container_width=True):
        st.session_state.analiz_edildi = True
        st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]: st.markdown(f"<div style='text-align:center; padding:20px; border:1px solid #333; border-radius:10px;'>{kn}</div>", unsafe_allow_html=True)
            
    with st.spinner("..."):
        full_prompt = f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}."
        report_text = generate_ai_response(full_prompt)
        
        if report_text:
            st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
            pdf_data = create_pdf(report_text, st.session_state.lang)
            st.download_button(label=L["pdf_btn"], data=pdf_data, file_name="Cynic_Report.pdf", mime="application/pdf")
        else:
            st.error("Google API uyarısı nedeniyle analiz yapılamadı. Lütfen API anahtarınızı AI Studio'dan kontrol edin.")
    
    if st.button(L["btn_reset"]):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
