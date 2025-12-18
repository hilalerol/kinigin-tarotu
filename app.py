import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR VE TASARIM ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# CSS KODLARINI BURADA GÜVENLİ BİR ŞEKİLDE PAKETLİYORUZ
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    .stApp { background: #000; color: #e0e0e0; font-family: 'Special Elite', cursive; }
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: white; letter-spacing: 8px; text-shadow: 0 0 15px #ff4b4b; }
    
    /* Butonlar */
    .stButton button { 
        background: #111 !important; border: 1px solid #333 !important; 
        color: #ff4b4b !important; border-radius: 8px !important; 
        transition: 0.3s; width: 100%;
    }
    .stButton button:hover { border-color: #ff4b4b !important; box-shadow: 0 0 15px #ff4b4b; transform: scale(1.1); }
    
    /* Analiz Kutusu (Senin paylaştığın kodun aktif hali) */
    .report-box { 
        background: #0a0a0a; 
        padding: 25px; 
        border-left: 5px solid #ff4b4b; 
        border-radius: 15px; 
        line-height: 1.8; 
        color: #ddd; 
    }
    
    /* Profesör (Senin paylaştığın kodun aktif hali) */
    .mystic-prof { 
        text-align: center; 
        font-size: 80px; 
        animation: float 3s infinite ease-in-out; 
    } 
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if m in models: return genai.GenerativeModel(m)
        return genai.GenerativeModel(models[0])
    except: return None

# --- 3. DURUM YÖNETİMİ ---
if 'secilenler' not in st.session_state: st.session_state.secilenler = []
if 'analiz_durum' not in st.session_state: st.session_state.analiz_durum = False

# --- 4. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

# KART SEÇİMİ
if not st.session_state.analiz_durum:
    st.write(f"<p style='text-align:center;'>Seçilen: {len(st.session_state.secilenler)} / 3</p>", unsafe_allow_html=True)
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.secilenler else "✧"
            if st.button(label, key=f"b{i}"):
                if i not in st.session_state.secilenler and len(st.session_state.secilenler) < 3:
                    st.session_state.secilenler.append(i)
                    st.rerun()
                elif i in st.session_state.secilenler:
                    st.session_state.secilenler.remove(i)
                    st.rerun()

    if len(st.session_state.secilenler) == 3:
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_durum = True
            st.rerun()

# ANALİZ GÖSTERİMİ
if st.session_state.analiz_durum:
    TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    with st.spinner("Kehanet fısıldanıyor..."):
        model = get_model()
        if model:
            try:
                res = model.generate_content(f"Sert bir tarot analizi yap. Soru: {soru}. Kartlar: {secilen_kartlar}")
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.warning("🔮 Yıldızlar çok yoğun. 30 saniye sonra tekrar dene.")
                else:
                    st.error("Bağlantıda bir sorun oldu.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilenler = []
        st.session_state.analiz_durum = False
        st.rerun()
