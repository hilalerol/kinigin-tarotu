import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #000; color: #e0e0e0; }
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; }
    .report-box { background: #111; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; }
    .mystic-prof { text-align: center; font-size: 80px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DURUM YÖNETİMİ (KİLİT NOKTA) ---
# Uygulama yenilendiğinde seçimleri unutmaması için bu isimleri sabitledik
if 'kart_sepeti' not in st.session_state: 
    st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: 
    st.session_state.analiz_durumu = False

# --- 4. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def kehanet_al(soru, kartlar):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Sert bir analiz yap. Soru: {soru}. Kartlar: {kartlar}")
        return res.text
    except Exception as e:
        return f"Bağlantı Hatası: {e}"

# --- 5. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

soru_girdisi = st.text_input("", placeholder="Kehanetini öğrenmek için 3 kart seç", label_visibility="collapsed")

# KART SEÇİM EKRANI
if st.session_state.analiz_durumu == False:
    st.write(f"<p style='text-align:center;'>Mühürlenen Enerji: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
    
    # 78 Kart Matrisi
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            secildi_mi = i in st.session_state.kart_sepeti
            dugme_etiketi = "❂" if secildi_mi else "✧"
            
            if st.button(dugme_etiketi, key=f"kart_{i}"):
                if not secildi_mi and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                    st.rerun() # Seçimi hemen kaydetmek için sayfayı tazele
                elif secildi_mi:
                    st.session_state.kart_sepeti.remove(i)
                    st.rerun()

    if len(st.session_state.kart_sepeti) == 3:
        st.write("")
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

# ANALİZ EKRANI
else:
    TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
    secilen_kart_isimleri = [TAM_DESTE[idx % 78] for idx in st.session_state.kart_sepeti]
    
    st.markdown(f"<p style='text-align:center; color:#ff4b4b;'>Seçilen Kartlar: {', '.join(secilen_kart_isimleri)}</p>", unsafe_allow_html=True)
    
    with st.spinner("Kaderin fısıldanıyor..."):
        cevap = kehanet_al(soru_girdisi, secilen_kart_isimleri)
        st.markdown(f"<div class='report-box'>{cevap}</div>", unsafe_allow_html=True)

    if st.button("BAŞA DÖN"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
