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
    st.caption("Dev: Hilal Erol | v12.5 Platinum")

L = texts[st.session_state.lang]

# --- 4. PDF FONKSİYONU ---
def create_pdf(text, lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    title = "KINIGIN TAROTU - RAPOR" if lang == "Türkçe" else "THE CYNIC'S TAROT - REPORT"
    pdf.cell(190, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    tr_map = {"ş":"s","Ş":"S","ı":"i","İ":"I","ğ":"g","Ğ":"G","ü":"u","Ü":"U","ö":"o","Ö":"O","ç":"c","Ç":"C","\u2013":"-","*":"","#":""}
    clean_text = text
    for c, r in tr_map.items(): clean_text = clean_text.replace(c, r)
    safe_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    
    pdf.multi_cell(0, 10, safe_text)
    return pdf.output(dest="S").encode('latin-1')

# --- 5. CSS (TASARIM) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #ffffff; }}
    .main-title {{ font-family: serif; text-align: center; letter-spacing: 8px; color: #ffffff; padding-top: 20px; }}
    .stButton button {{ background-color: #0a0a0a !important; border: 1px solid #333 !important; color: #666 !important; font-size: 16px !important; width: 100% !important; height: 50px; }}
    .stButton button:hover {{ border-color: #ff4b4b !important; color: white !important; }}
    .report-box {{ background: #0a0a0a; padding: 25px; border-radius: 15px; border: 1px solid #222; border-left: 5px solid #ff4b4b; color: #e0e0e0; margin-top: 20px; line-height: 1.8; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. API YAPILANDIRMASI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets ayarı eksik! Lütfen MY_API_KEY tanımlayın.")

# --- 7. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#444;'>{L['sub']}</p>", unsafe_allow_html=True)

soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

# KART MATRİSİ
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

# SONUÇ EKRANI
if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]: st.markdown(f"<div style='text-align:center; padding:20px; border:1px solid #333; border-radius:10px;'>{kn}</div>", unsafe_allow_html=True)
            
    with st.spinner("..."):
        full_prompt = f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}."
        try:
            # Otomatik model seçimi (Hangi model aktifse onu kullanır)
            model_names = ['gemini-1.5-flash', 'gemini-pro']
            response = None
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(full_prompt)
                    if response: break
                except: continue
            
            if response:
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                pdf_data = create_pdf(response.text, st.session_state.lang)
                st.download_button(label=L["pdf_btn"], data=pdf_data, file_name="Cynic_Report.pdf", mime="application/pdf")
            else:
                st.error("Google API yanıt vermiyor. Lütfen yeni bir API anahtarı ile Secrets kısmını güncelleyin.")
        except Exception as e:
            st.error(f"Sistemsel Hata: {str(e)}")
    
    if st.button(L["btn_reset"]):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
