import streamlit as st
import google.generativeai as genai
import random

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
        "prompt": "Sert bir ekonomi analisti gibi dürüst ve acımasız bir tarot yorumu yap."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "Select 3 Symbols...",
        "placeholder": "Enter scenario...",
        "btn_reveal": "REVEAL",
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
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; font-family: serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE MODEL TESPİTİ ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Lütfen Secrets panelinden MY_API_KEY tanımlayın.")

def get_best_model():
    """Sistemde aktif olan en uygun modeli bulur"""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Öncelik sırası: Flash 1.5 -> Pro 1.5 -> Gemini Pro (Old)
        for target in ['models/gemini-1.5-flash', 'gemini-1.5-flash', 'models/gemini-pro', 'gemini-pro']:
            if target in available_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except:
        return None

# --- 6. ARAYÜZ ---
st.markdown(f"<h1 style='text-align:center; letter-spacing: 5px;'>{L['title']}</h1>", unsafe_allow_html=True)
soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#555;'>{len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
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

    if len(st.session_state.secilen_indeksler) == 3:
        if st.button(L["btn_reveal"], use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; padding:20px; border:1px solid #222; border-radius:10px;'>{kn}</div>", unsafe_allow_html=True)
    
    with st.spinner("Analiz ediliyor..."):
        model = get_best_model()
        if model:
            try:
                response = model.generate_content(f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}.")
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Kota doldu. Lütfen 1 dakika sonra tekrar deneyin.")
                else:
                    st.error(f"Hata: {e}")
        else:
            st.error("Kullanılabilir model bulunamadı.")

    if st.button("YENİ ANALİZ"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
