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
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; letter-spacing: 5px; margin-bottom: 0px;}
    .report-box { background: #111; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; }
    .mystic-prof { text-align: center; font-size: 70px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    div[data-testid="stExpander"] { background: #0a0a0a; border: 1px solid #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = False

# --- 5. API VE MODEL ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in available_models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except: return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

# GİRİŞ FORMU
with st.container():
    soru = st.text_input("Kehanetini sormadan önce ruhunu aç...", placeholder="Neyi bilmek istersin?")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        konu = st.selectbox("Odak Noktan Ne?", ["Genel", "Aşk ve İlişkiler", "Para ve Kariyer", "Sağlık", "İş ve Projeler"])
        yas = st.number_input("Yaşın", min_value=15, max_value=99, value=25)
    with col_info2:
        calisma = st.selectbox("Çalışma Durumun", ["Çalışıyorum", "Öğrenciyim", "İş Arıyorum", "Çalışmıyorum"])
        medeni = st.selectbox("Medeni Halin", ["Bekar", "Sözlü/Nişanlı", "Evli", "Boşanmış/Dul"])
        iliski = st.selectbox("İlişki Durumun", ["İlişkim var", "İlişkim yok", "Karmaşık", "Platonik"])

# KART SEÇİMİ
if not st.session_state.analiz_durumu:
    st.write(f"<p style='text-align:center; color:#ff4b4b;'>Seçilen Kart: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
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
        if st.button("KADERİMİ ANALİZ ET", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

# ANALİZ EKRANI
else:
    try:
        secilen_kart_isimleri = [TAM_DESTE[idx] for idx in st.session_state.kart_sepeti]
        st.write(f"<p style='text-align:center; color:#ff4b4b;'>{ ' | '.join(secilen_kart_isimleri) }</p>", unsafe_allow_html=True)
        
        with st.spinner("Profesör Minerva kartları okuyor..."):
            model = get_working_model()
            if model:
                # Yapay zekaya gönderilen süper detaylı komut
                prompt = f"""
                Sen 'The Cynic's Tarot' isimli sert, dürüst ve alaycı bir tarot yorumcususun.
                Kullanıcı Bilgileri:
                - Soru: {soru}
                - Konu: {konu}
                - Yaş: {yas}
                - Çalışma Durumu: {calisma}
                - Medeni Hal: {medeni}
                - İlişki Durumu: {iliski}
                - Seçilen Kartlar: {', '.join(secilen_kart_isimleri)}
                
                Bu bilgilere dayanarak, kullanıcının hayat durumunu da gözeterek acımasızca dürüst bir analiz yap.
                Gereksiz kibarlıktan kaçın, gerçekleri yüzüne vur.
                """
                res = model.generate_content(prompt, generation_config={"max_output_tokens": 600})
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
            else:
                st.error("Kozmik hatlar meşgul.")
    except Exception as e:
        st.error(f"Hata: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
