import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Kinigin Tarotu Pro", page_icon="🔮", layout="wide")

# --- 2. 78 KARTLIK TAM DESTE ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. SESSION STATE (DURUM YÖNETİMİ) ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 4. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; font-family: 'Georgia', serif; margin-top: 20px; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; border-radius: 8px; transition: 0.3s; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; box-shadow: 0 0 10px #ff4b4b; }
    .mystic-prof { text-align: center; font-size: 85px; text-shadow: 0 0 20px #ff4b4b; margin-bottom: -10px; }
    .card-display { text-align: center; padding: 15px; border: 1px solid #222; border-radius: 10px; background: #050505; color: #aaa; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE MODEL YÖNETİMİ ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets panelinde MY_API_KEY tanımlanmamış!")

def get_best_model():
    """Google'ın o an kabul ettiği aktif modeli dinamik olarak bulur."""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Tercih sırası: En güncelden en kararlıya
        for target in ['models/gemini-1.5-flash', 'models/gemini-2.0-flash-exp', 'models/gemini-pro']:
            if target in available_models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except:
        return None

# --- 6. ANA ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; letter-spacing: 8px; font-family: serif;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Kaderini merak ettiğin o soruyu buraya yaz...", label_visibility="collapsed")

# KART SEÇİM EKRANI
if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#555;'>Üç sembol seçerek enerjiyi mühürle: {len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
    
    # 78 Kartlık Matris (6 Satır x 13 Sütun)
    for row in range(6):
        cols = st.columns(13)
        for col in range(13):
            idx = row * 13 + col
            if idx < 78:
                with cols[col]:
                    is_selected = idx in st.session_state.secilen_indeksler
                    label = "❂" if is_selected else "✧"
                    if st.button(label, key=f"k_{idx}"):
                        if not is_selected and len(st.session_state.secilen_indeksler) < 3:
                            st.session_state.secilen_indeksler.append(idx)
                            st.rerun()
                        elif is_selected:
                            st.session_state.secilen_indeksler.remove(idx)
                            st.rerun()

    if len(st.session_state.secilen_indeksler) == 3:
        st.write("")
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

# ANALİZ EKRANI
if st.session_state.analiz_edildi:
    # Mistik Bekleme Efekti
    placeholder = st.empty()
    placeholder.markdown("<h3 style='text-align:center; color:#ff4b4b; animation: pulse 2s infinite;'>🔮 Profesör Minerva enerjiyi topluyor...</h3>", unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()

    # Kartları Karıştır ve Seçilenleri Göster
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    c1, c2, c3 = st.columns(3)
    cards = [c1, c2, c3]
    for i, name in enumerate(secilen_kartlar):
        with cards[i]:
            st.markdown(f"<div class='card-display'>{name}</div>", unsafe_allow_html=True)
    
    # Analizi Başlat
    with st.spinner("Kozmik veriler işleniyor..."):
        model = get_best_model()
        if model:
            try:
                prompt = f"Sen sert, dürüst ve stratejik bir ekonomi analistisin. Soru: {soru}. Seçilen Tarot Kartları: {secilen_kartlar}. Bu durumu acımasız ama gerçekçi bir dille analiz et."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.warning("🌙 Yıldızlar şu an çok yoğun. Profesör dinleniyor...")
                    timer = st.empty()
                    for i in range(45, 0, -1):
                        timer.metric("Bekleme Süresi", f"{i} Saniye")
                        time.sleep(1)
                    timer.empty()
                    st.info("🔄 Süre doldu. Lütfen sayfayı yenileyip tekrar deneyin.")
                else:
                    st.error(f"Kozmik bir hata oluştu: {e}")
        else:
            st.error("Sistemsel bir bağlantı sorunu var.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
