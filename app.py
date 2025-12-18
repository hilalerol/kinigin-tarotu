import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. TASARIM (CSS BURADA OLMALI) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    /* Arka Plan */
    .stApp { 
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); 
        color: #e0e0e0; 
        font-family: 'Special Elite', cursive; 
    }
    
    /* Başlık */
    .main-title { 
        font-family: 'Cinzel', serif; 
        text-align: center; 
        color: #ffffff; 
        letter-spacing: 12px; 
        text-shadow: 0 0 15px #ff4b4b; 
        margin-top: 20px; 
    }
    
    /* Kart Butonları */
    .stButton button { 
        background: rgba(15, 15, 15, 0.9) !important; 
        border: 1px solid #333 !important; 
        color: #ff4b4b !important; 
        border-radius: 8px !important; 
        font-size: 22px !important; 
        height: 60px !important; 
        transition: all 0.4s ease-in-out !important; 
    }
    .stButton button:hover { 
        border-color: #ff4b4b !important; 
        color: white !important; 
        box-shadow: 0 0 20px #ff4b4b !important; 
        transform: scale(1.15) rotate(2deg); 
    }
    
    /* Analiz Rapor Kutusu */
    .report-box { 
        background: rgba(5, 5, 5, 0.95); 
        padding: 35px; 
        border: 1px solid #444; 
        border-left: 5px solid #ff4b4b; 
        border-radius: 20px; 
        line-height: 2; 
        color: #d1d1d1; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.8); 
        margin-top: 25px; 
    }
    
    /* Profesör Animasyonu */
    .mystic-prof { 
        text-align: center; 
        font-size: 100px; 
        animation: float 4s ease-in-out infinite; 
        filter: drop-shadow(0 0 20px #ff4b4b); 
        margin-bottom: -20px; 
    }
    @keyframes float { 
        0% { transform: translateY(0px); } 
        50% { transform: translateY(-25px); } 
        100% { transform: translateY(0px); } 
    }
    
    /* Input Alanı */
    .stTextInput input { 
        background-color: #0a0a0a !important; 
        color: #ff4b4b !important; 
        border: 1px solid #444 !important; 
        text-align: center; 
        border-radius: 10px !important; 
        padding: 15px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_best_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(models[0]) if models else None
    except: return None

# --- 4. SESSION STATE ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 5. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.secilen_indeksler else "✧"
            if st.button(label, key=f"btn_{i}"):
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

if st.session_state.analiz_edildi:
    placeholder = st.empty()
    placeholder.markdown("<h3 style='text-align:center; color:#ff4b4b;'>🔮 Profesör Minerva enerjiyi topluyor...</h3>", unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()

    TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    with st.spinner("Kehanet işleniyor..."):
        model = get_best_model()
        if model:
            try:
                prompt = f"Sen 'The Cynic's Tarot' sistemisin. Sert ve dürüst bir analiz yap. Soru: {soru}. Kartlar: {secilen_kartlar}."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.warning("🌙 Kota doldu. Lütfen 30 saniye bekleyip tekrar basın.")
                else:
                    st.error(f"Kozmik bir engel: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
