import streamlit as st
import google.generativeai as genai
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. 78 KARTLIK GENİŞ DESTE (Özet Listesi) ---
# Gerçek tarot destesi 78 karttır. Burada temel isimleri kullanıyoruz.
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA # Toplam 78 Kart

# --- 3. SESSION STATE ---
if 'secilen_indeksler' not in st.session_state:
    st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state:
    st.session_state.analiz_edildi = False

# --- 4. CSS (Mistik ve Karanlık) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { font-family: serif; text-align: center; letter-spacing: 10px; color: #ffffff; text-transform: uppercase; }
    .stButton button { 
        background-color: #111 !important; 
        border: 1px solid #333 !important; 
        color: #555 !important; 
        font-size: 20px !important;
        height: 60px !important;
        width: 100% !important;
        transition: 0.3s;
    }
    .stButton button:hover { border-color: #ff4b4b !important; color: #ff4b4b !important; background-color: #1a1a1a !important; }
    .selected-btn button { border-color: #ff4b4b !important; color: #ff4b4b !important; background-color: #222 !important; }
    .report-box { background: #111; padding: 30px; border-radius: 15px; border-left: 4px solid #ff4b4b; font-family: 'Georgia', serif; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 6. ARAYÜZ ---
st.markdown('<h1 class="main-title">KİNİĞİN TAROTU</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#444;'>78 Kartlık Desteden 3 Sembol Seç...</p>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Analiz edilecek senaryoyu buraya fısılda...", label_visibility="collapsed")

# KART SEÇİM ALANI
if not st.session_state.analiz_edildi:
    st.write(f"### ✧ Seçilen: {len(st.session_state.secilen_indeksler)} / 3")
    
    # 78 Kartı 6 satır x 13 sütun şeklinde dizelim
    for row in range(6):
        cols = st.columns(13)
        for col in range(13):
            idx = row * 13 + col
            if idx < 78:
                with cols[col]:
                    is_selected = idx in st.session_state.secilen_indeksler
                    # Sembol olarak ✧ kullanıyoruz
                    if st.button("✧", key=f"k_{idx}", help=f"Kart {idx+1}"):
                        if not is_selected and len(st.session_state.secilen_indeksler) < 3:
                            st.session_state.secilen_indeksler.append(idx)
                            st.rerun()
                        elif is_selected:
                            st.session_state.secilen_indeksler.remove(idx)
                            st.rerun()

# ANALİZ TETİKLEYİCİ
if len(st.session_state.secilen_indeksler) == 3 and not st.session_state.analiz_edildi:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("KADERİNİ ANALİZ ET", use_container_width=True):
        st.session_state.analiz_edildi = True
        st.rerun()

# SONUÇ EKRANI
if st.session_state.analiz_edildi:
    # Seçilen her indeks için desteden rastgele bir kart ata
    # (Kullanıcı hangi indekse bastıysa o 'enerji' ile bir kart eşleşir)
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    st.divider()
    st.write("### 🃏 Açılan Kartlar")
    c1, c2, c3 = st.columns(3)
    k_cols = [c1, c2, c3]
    for i, k_name in enumerate(secilen_kartlar):
        with k_cols[i]:
            st.info(f"**{k_name}**") # Resim yerine isimler (78 kart resmi yüklemeyi önlemek için)
            
    with st.spinner("Kınik analiz ediyor..."):
        prompt = f"Sen sert bir analistsin. Soru: {soru}. Seçilen 3 Tarot Kartı: {secilen_kartlar}. Bu kartları ve soruyu birleştirerek dürüst, sert ve stratejik bir rapor yaz."
        response = model.generate_content(prompt)
        st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
    
    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
