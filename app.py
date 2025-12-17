Kaydet (Commit).
import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# API Ayarı
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")
model = genai.GenerativeModel('gemini-pro')

# --- KART GÖRSELLERİ (ÖRNEK SİSTEM) ---
# Buraya kart isimlerini ve internetteki resim linklerini ekliyoruz
TAROT_IMAGES = {
    "Büyücü": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Ay": "https://upload.wikimedia.org/wikipedia/commons/f/f0/RWS_Tarot_18_Moon.jpg",
    "Şeytan": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "Kılıç Şövalyesi": "https://upload.wikimedia.org/wikipedia/commons/d/d4/RWS_Tarot_Knight_of_Swords.jpg"
}

st.title("🔮 Kiniğin Tarotu: Analitik Risk Raporu")
st.sidebar.header("Kişisel Parametreler")

soru = st.text_input("Gerçeği duymaya hazır mısın?", placeholder="Sorum şu...")
zayifliklar = st.sidebar.multiselect("Sistem Arızalarını Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("ANALİZİ BAŞLAT"):
    if soru:
        with st.spinner('Kınik zekâ verileri işliyor...'):
            prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Seçtiğin 3 kartın ismini metnin başında 'KARTLAR: Kart1, Kart2, Kart3' şeklinde belirt ve dürüstçe yorumla."
            response = model.generate_content(prompt)
            
            # Kart resimlerini gösterme mantığı
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            
            # Metinden kart isimlerini bulup resim basma (Basit mantık)
            for i, (name, url) in enumerate(list(TAROT_IMAGES.items())[:3]):
                with cols[i]:
                    st.image(url, caption=name, width=150)
            
            st.markdown("---")
            st.write(response.text)
