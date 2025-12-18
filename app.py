import streamlit as st
import google.generativeai as genai
import random
from fpdf import FPDF

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kiniğin Tarotu Pro", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
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
        "placeholder": "Durumu yazın...",
        "btn_reveal": "KEHANETİ AÇ",
        "pdf_btn": "📄 Analizi PDF İndir",
        "prompt": "Sert bir ekonomi analisti gibi dürüst bir tarot yorumu yap."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "Select 3 Symbols...",
        "placeholder": "Enter scenario...",
        "btn_reveal": "REVEAL",
        "pdf_btn": "📄 Download PDF",
        "prompt": "Provide a harsh and honest tarot analysis as an economic expert."
    }
}
L = texts[st.session_state.lang]

# --- 4. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; height: 50px; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    .report-box { background: #0a0a0a; padding: 20px; border-left: 5px solid #ff4b4b; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API YAPILANDIRMASI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("API Key bulunamadı!")

# --- 6. ARAYÜZ ---
st.markdown(f"<h1 style='text-align:center;'>{L['title']}</h1>", unsafe_allow_html=True)
soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.secilen_indeksler else "✧"
            if st.button(label, key=f"k_{i}"):
                if i not in st.session_state.secilen_indeksler and len(st.session_state.secilen_indeksler) < 3:
                    st.session_state.secilen_indeksler.append(i)
                    st.rerun()
                elif i in st.session_state.secilen_indeksler:
                    st.session_state.secilen_indeksler.remove(i)
                    st.rerun()

    if len(st.session_state.secilen_indeksler) == 3:
        if st.button(L["btn_reveal"]):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.write(f"### 🃏 {', '.join(secilen_kartlar)}")
    
    with st.spinner("Analiz ediliyor..."):
        try:
            # Önce FLASH modelini deniyoruz (Kota dostu!)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}.")
            st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Google kotası doldu. Lütfen 1 dakika bekleyip sayfayı yenileyin veya yeni bir API anahtarı kullanın.")
            else:
                st.error(f"Hata oluştu: {e}")

    if st.button("GERİ DÖN"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
