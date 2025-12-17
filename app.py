import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮")

MY_API_KEY = "AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4"
genai.configure(api_key=MY_API_KEY)

# --- MODELİ OTOMATİK BULAN AKILLI SİSTEM ---
@st.cache_resource
def load_working_model():
    try:
        # Mevcut tüm modelleri tara
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Varsa 1.5-flash'ı seç, yoksa ilk çalışan modeli al
        final_model = next((m for m in models if '1.5-flash' in m), models[0])
        return genai.GenerativeModel(final_model), final_model
    except Exception as e:
        return None, str(e)

model, model_name = load_working_model()

st.title("🔮 Kiniğin Tarotu")
if model:
    st.caption(f"✅ Sistem Aktif: {model_name} üzerinden analiz yapılıyor.")
else:
    st.error("Bağlantı kurulamadı. Lütfen API anahtarınızı kontrol edin.")

# Kullanıcı Girişleri
soru = st.text_input("Neyi analiz etmek istiyorsun?", placeholder="Örn: Kariyer yolculuğum...")
zayifliklar = st.multiselect("Zayıflıklar:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("Analiz Et"):
    if soru and model:
        with st.spinner('Kınik analiz yapıyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle dürüstçe yorumla."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 📋 Kınik Analiz Raporu")
                st.write(response.text)
            except Exception as e:
                st.error(f"Analiz sırasında bir sorun oluştu: {e}")
    elif not soru:
        st.warning("Lütfen bir soru yaz.")
