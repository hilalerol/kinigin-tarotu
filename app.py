import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮")

# API Ayarı
MY_API_KEY = "AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4"
genai.configure(api_key=MY_API_KEY)

# --- AKILLI MODEL SEÇİCİ ---
def get_working_model():
    try:
        # Sistemdeki modelleri tara ve en güncel 'flash' modelini bul
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if '1.5-flash' in m.name:
                    return m.name
        return 'gemini-pro' # Yedek plan
    except:
        return 'gemini-pro'

working_model_name = get_working_model()
model = genai.GenerativeModel(working_model_name)

st.title("🔮 Kiniğin Tarotu")
st.write(f"Bağlanan Sistem: {working_model_name}") # Hangi modele bağlandığını görelim

# Kullanıcı Girişleri
soru = st.text_input("Neyi analiz etmek istiyorsun?")
zayifliklar = st.multiselect("Zayıflıklar:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("Analiz Et"):
    if soru:
        with st.spinner('Kınik analiz yapıyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle yorumla."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")
