import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. TASARIM (CSS BURADA KİLİTLİDİR, DIŞARI SIZAMAZ) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: #e0e0e0; font-family: 'Special Elite', cursive; }
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: white; letter-spacing: 8px; text-shadow: 0 0 15px #ff4b4b; }
    .report-box { background: rgba(5, 5, 5, 0.95); padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 15px; line-height: 1.8; color: #ddd; box-shadow: 0 10px 30px rgba(0,0,0,0.8); margin-top: 20px; }
    .mystic-prof { text-align: center; font-size: 80px; animation: float 4s infinite ease-in-out; filter: drop-shadow(0 0 15px #ff4b4b); }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    div[data-testid="stExpander"] { background: rgba(10, 10, 10, 0.8); border: 1px solid #333; border-radius: 10px; }
    .stButton button { background: rgba(15, 15, 15, 0.9) !important; border: 1px solid #333 !important; color: #ff4b4b !important; border-radius: 8px !important; transition: 0.4s; }
    .stButton button:hover { border-color: #ff4b4b !important; box-shadow: 0 0 20px #ff4b4b; transform: scale(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SABİT VERİLER ---
TAM_DESTE = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"] + [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]

# --- 4. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = False

# --- 5. API ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if m in models: return genai.GenerativeModel(m)
        return genai.GenerativeModel(models[0])
    except: return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

with st.expander("🔮 KOZMİK PROFİLİN", expanded=True):
    soru = st.text_input("Sorun nedir?", placeholder="Geleceğimi söyle...")
    c1, c2 = st.columns(2)
    with c1:
        yas = st.number_input("Yaş", 15, 99, 25)
        medeni = st.selectbox("Medeni Hal", ["Bekar", "Evli", "Boşanmış"])
    with c2:
        calisma = st.selectbox("İş", ["Çalışan", "Öğrenci", "İşsiz"])
        iliski = st.selectbox("İlişki", ["Var", "Yok", "Karmaşık"])

if not st.session_state.analiz_durumu:
    st.write(f"<p style='text-align:center;'>Seçilen: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.kart_sepeti else "✧"
            if st.button(label, key=f"b_{i}"):
                if i not in st.session_state.kart_sepeti and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                elif i in st.session_state.kart_sepeti:
                    st.session_state.kart_sepeti.remove(i)
                st.rerun()
    if len(st.session_state.kart_sepeti) == 3:
        if st.button("KADERİNİ MÜHÜRLE", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()
else:
    try:
        secilenler = []
        for idx in st.session_state.kart_sepeti:
            yon = " (TERS)" if random.random() < 0.3 else " (DÜZ)"
            secilenler.append(TAM_DESTE[idx] + yon)
        
        st.write(f"<p style='text-align:center; color:#ff4b4b;'>{ ' | '.join(secilenler) }</p>", unsafe_allow_html=True)
        
        with st.spinner("Minerva yazıyor..."):
            model = get_model()
            if model:
                res = model.generate_content(f"Sert ol. Profil: {yas}, {calisma}, {medeni}, {iliski}. Soru: {soru}. Kartlar: {secilenler}. Sonunda 3 maddelik ACI REÇETE yaz.")
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Hata: {e}")
    if st.button("SIFIRLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
