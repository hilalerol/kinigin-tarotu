import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. SAYFA VE FONT AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# Google Fonts'tan mistik fontları çekiyoruz
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    /* Genel Arka Plan ve Yazı Tipleri */
    .stApp {
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Special Elite', cursive;
    }
    
    /* Başlık Stili */
    .main-title {
        font-family: 'Cinzel', serif;
        text-align: center;
        color: #ffffff;
        letter-spacing: 10px;
        text-shadow: 0 0 20px #ff4b4b, 0 0 30px #000;
        margin-top: 20px;
        font-weight: 700;
    }

    /* Kart Butonları Efekti */
    .stButton button {
        background: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid #333 !important;
        color: #ff4b4b !important;
        border-radius: 5px !important;
        font-size: 20px !important;
        transition: all 0.4s ease-in-out !important;
    }
    
    .stButton button:hover {
        border-color: #ff4b4b !important;
        color: white !important;
        box-shadow: 0 0 15px #ff4b4b !important;
        transform: scale(1.1);
    }

    /* Analiz Rapor Kutusu */
    .report-box {
        background: rgba(10, 10, 10, 0.9);
        padding: 30px;
        border: 1px solid #444;
        border-left: 4px solid #ff4b4b;
        border-radius: 15px;
        line-height: 2;
        color: #d1d1d1;
        font-family: 'Special Elite', cursive;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
    }

    /* Profesör Emoji Animasyonu */
    .mystic-prof {
        text-align: center;
        font-size: 90px;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 15px #ff4b4b);
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    /* Input Alanı */
    .stTextInput input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
        font-family: 'Special Elite', cursive !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("API Anahtarı eksik!")

def get_actual_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(models[0]) if models else None
    except: return None

# --- 3. İÇERİK ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

# Session State
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# Kart Seçimi
if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#666;'>Kaderin mühürleniyor: {len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
    
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
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

# Analiz Sonucu
if st.session_state.analiz_edildi:
    placeholder = st.empty()
    placeholder.markdown("<h3 style='text-align:center; color:#ff4b4b; font-family:Cinzel;'>🔮 Profesör Minerva enerjiyi topluyor...</h3>", unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()

    TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    st.markdown(f"<p style='text-align:center; font-size:20px; color:#aaa;'>Seçilen Kartlar: {', '.join(secilen_kartlar)}</p>", unsafe_allow_html=True)
    
    with st.spinner("Analiz hazırlanıyor..."):
        model = get_actual_model()
        if model:
            try:
                prompt = f"Sen 'The Cynic's Tarot' isimli sert ve stratejik bir analiz sistemisin. Soru: {soru}. Kartlar: {secilen_kartlar}. Acımasızca analiz et."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Hata: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
