import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. KART DESTE SİSTEMİ (EN GÜVENLİ YER) ---
# Listeyi burada bir kez tanımlıyoruz ki IndexError riski kalmasın
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA # Toplam tam 78 kart

# --- 3. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #000; color: #e0e0e0; }
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; font-family: serif; letter-spacing: 5px; }
    .report-box { background: #111; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; }
    .mystic-prof { text-align: center; font-size: 80px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: 
    st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: 
    st.session_state.analiz_durumu = False

# --- 5. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def kehanet_al(soru, kartlar):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Sen dürüst ve sert bir tarot yorumcususun. Soru: {soru}. Kartlar: {kartlar}. Acımasızca analiz et."
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Kozmik bir hata: {e}"

# --- 6. ARAYÜZ ---
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
            
            if st.button(dugme_etiketi, key=f"k_{i}"):
                if not secildi_mi and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                elif secildi_mi:
                    st.session_state.kart_sepeti.remove(i)
                st.rerun()

    if len(st.session_state.kart_sepeti) == 3:
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

# ANALİZ EKRANI
else:
    # Hata veren satırı korumaya aldık:
    try:
        secilen_kart_isimleri = [TAM_DESTE[idx] for idx in st.session_state.kart_sepeti if idx < len(TAM_DESTE)]
        
        st.markdown(f"<p style='text-align:center; color:#ff4b4b; font-size: 1.2rem;'>Kartların: {' | '.join(secilen_kart_isimleri)}</p>", unsafe_allow_html=True)
        
        with st.spinner("Kehanet işleniyor..."):
            cevap = kehanet_al(soru_girdisi, secilen_kart_isimleri)
            st.markdown(f"<div class='report-box'>{cevap}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Kartlar çekilirken bir sorun oldu: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
