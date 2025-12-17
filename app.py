Kaydet (Commit).
import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮")

# API Ayarı 
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")
model = genai.GenerativeModel('gemini-pro')

st.title("🔮 Kiniğin Tarotu")
st.subheader("Ekonomi Odaklı Analitik Risk Raporu")

# Kullanıcı Girişleri
soru = st.text_input("Neyi analiz etmek istiyorsun?")
zayifliklar = st.multiselect("Zayıflıklar:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("Analiz Et"):
    if soru:
        prompt = f"Sen Kiniğin Tarotu'sun. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle yorumla."
        response = model.generate_content(prompt)
        st.markdown(response.text)
