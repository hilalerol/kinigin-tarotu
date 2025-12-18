import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. TASARIM ---
st.markdown("""
    <style>
    .stApp { background: #000; color: #e0e0e0; font-family: serif; }
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; letter-spacing: 5px; }
    .report-box { background: #111; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; }
    .mystic-prof { text-align: center; font-size: 80px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = False

# --- 5. API VE DİNAMİK MODEL SEÇİCİ ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_working_model():
    """Google'ın o an sunduğu en iyi aktif modeli bulur."""
    try:
        # Google'dan aktif model listesini al
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Tercih sırasına göre kontrol et
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro', 'models/gemini-1.0-pro']:
            if target in available_models:
                return genai.GenerativeModel(target)
        
        # Hiçbiri yoksa listedeki ilkini kullan
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except Exception as e:
        return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

if not st.session_state.analiz_durumu:
    st.write(f"<p style='text-align:center;'>Mühür: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.kart_sepeti else "✧"
            if st.button(label, key=f"k_{i}"):
                if i not in st.session_state.kart_sepeti and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                elif i in st.session_state.kart_sepeti:
                    st.session_state.kart_sepeti.remove(i)
                st.rerun()

    if len(st.session_state.kart_sepeti) == 3:
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

else:
    try:
        secilen_kart_isimleri = [TAM_DESTE[idx] for idx in st.session_state.kart_sepeti]
        st.write(f"<p style='text-align:center; color:#ff4b4b;'>{ ' | '.join(secilen_kart_isimleri) }</p>", unsafe_allow_html=True)
        
        with st.spinner("Kehanet hazırlanıyor..."):
            model = get_working_model()
            if model:
                res = model.generate_content(f"Sert bir analiz yap. Soru: {soru}. Kartlar: {secilen_kart_isimleri}")
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
            else:
                st.error("Şu an hiçbir kozmik model yanıt vermiyor.")
    except Exception as e:
        st.error(f"Hata oluştu: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
