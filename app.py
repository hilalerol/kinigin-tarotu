import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# RENKLERİ ZORLAYAN CSS (Bu sefer daha güçlü)
st.markdown("""
    <style>
    /* Ana arka planı siyah yap */
    .stApp {
        background-color: #0e1117;
    }
    /* Tüm yazıların rengini beyaz yap */
    h1, h2, h3, p, span, div, label {
        color: #ffffff !important;
    }
    /* Başlıkları kırmızı yap */
    h1, h2 {
        color: #ff4b4b !important;
        text-shadow: 2px 2px #000000;
    }
    /* Giriş kutusunu ve düğmeyi belirginleştir */
    .stTextInput input {
        background-color: #1a1c23 !important;
        color: white !important;
        border: 1px solid #ff4b4b !important;
    }
    .stButton button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API AYARIN ---
genai.configure(api_key="BURAYA_API_ANAHTARINI_YAZ")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🔮 Kiniğin Tarotu")
st.markdown("### *Ekonomi Mezunu Sert Bir Analistten Risk Raporu*")

# ... Kodun geri kalanı aynı kalabilir ...
soru = st.text_input("Gerçeği duymaya hazır mısın?", placeholder="Kariyerim ne olacak?")
zayifliklar = st.multiselect("Zayıflık Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("ANALİZİ BAŞLAT"):
    if soru:
        with st.spinner('Kınik verileri işliyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle yorumla."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("## 📊 ANALİZ RAPORU")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")
