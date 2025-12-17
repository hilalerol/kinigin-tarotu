import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮")

# API Ayarı - Kendi anahtarını tırnak işaretleri arasına yaz
MY_API_KEY = "AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4" 

genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.title("🔮 Kiniğin Tarotu")
st.subheader("Ekonomi Odaklı Analitik Risk Raporu")

# Kullanıcı Girişleri
soru = st.text_input("Neyi analiz etmek istiyorsun?", placeholder="Örn: Kariyer risklerim...")
zayifliklar = st.multiselect("Sistem Arızalarını Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("Analiz Et"):
    if soru:
        with st.spinner('Kınik zekâ verileri işliyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla dürüstçe ve ekonomi diliyle yorumla."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 📋 Kınik Analiz Raporu")
                st.write(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir soru sor.")
