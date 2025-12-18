import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. TASARIM (CSS) ---
# Tasarımı Python'un anlayacağı şekilde bir kutuya hapsettik
st.markdown("""
    <style>
    .stApp { background: #000; color: #e0e0e0; }
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; }
    .report-box { background: #111; padding: 20px; border-left: 5px solid #ff4b4b; border-radius: 10px; }
    .mystic-prof { text-align: center; font-size: 80px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel('models/gemini-1.5-flash')
    except: return None

# --- 4. DURUM YÖNETİMİ ---
if 'sec' not in st.session_state: st.session_state.sec = []
if 'analiz' not in st.session_state: st.session_state.analiz = False

# --- 5. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

if not st.session_state.analiz:
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.sec else "✧"
            if st.button(label, key=f"k{i}"):
                if i not in st.session_state.sec and len(st.session_state.sec) < 3:
                    st.session_state.sec.append(i)
                    st.rerun()
    
    if len(st.session_state.sec) == 3:
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz = True
            st.rerun()

if st.session_state.analiz:
    TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    with st.spinner("Kehanet fısıldanıyor..."):
        model = get_model()
        if model:
            try:
                res = model.generate_content(f"Sert bir analiz yap. Soru: {soru}. Kartlar: {secilen_kartlar}")
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Biraz bekleyip tekrar deneyin.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.sec = []
        st.session_state.analiz = False
        st.rerun()
