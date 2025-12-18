import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. DURUM YÖNETİMİ ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 4. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; color: #ddd; font-family: serif; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; border-radius: 8px; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    .prof-header { text-align: center; font-size: 80px; text-shadow: 0 0 20px #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API AYARI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets panelinden MY_API_KEY bulunamadı!")

# --- 6. ARAYÜZ ---
st.markdown('<div class="prof-header">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Senaryonu buraya fısılda...", label_visibility="collapsed")

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
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    
    # Kart İsimlerini Göster
    cols = st.columns(3)
    for i, card in enumerate(secilen_kartlar):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid #222;'>{card}</div>", unsafe_allow_html=True)
    
    # ANALİZ KISMI
    with st.spinner("🔮 Profesör Minerva kozmik bağ kuruyor..."):
        try:
            # Model ismini Google'ın en sevdiği formatta sabitledik
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Sen dürüst ve sert bir tarot yorumcususun. Soru: {soru}. Kartlar: {secilen_kartlar}. Bu durumu acımasızca analiz et."
            
            # API'den yanıtı iste
            response = model.generate_content(prompt)
            
            # Yanıt boş mu dolu mu kontrol et
            if response and response.text:
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.warning("🌙 Gökler şu an sessiz. Lütfen bir kez daha 'Kehaneti Aç' de.")
                
        except Exception as e:
            if "429" in str(e):
                st.error("⏳ Google kotası doldu. Lütfen 30 saniye bekleyip sayfayı yenileyin.")
            else:
                st.error(f"Bağlantı Hatası: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
