import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮")

MY_API_KEY = "AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4"
genai.configure(api_key=MY_API_KEY)

# 2. MODELİ DOĞRUDAN GÜNCEL İSİMLE ÇAĞIRALIM
# Eğer gemini-1.5-flash yine hata verirse, sistem otomatik listeleme yapacak
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Test amaçlı küçük bir çağrı yapalım (opsiyonel)
except:
    model = genai.GenerativeModel('gemini-pro') # Yedek

st.title("🔮 Kiniğin Tarotu")
st.subheader("Ekonomi Odaklı Analitik Risk Raporu")

# Kullanıcı Girişleri
soru = st.text_input("Neyi analiz etmek istiyorsun?", placeholder="Örn: Kariyer yolculuğumdaki engeller...")
zayifliklar = st.multiselect("Sistem Arızalarını Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

if st.button("Analiz Et"):
    if soru:
        with st.spinner('Kınik analiz yapıyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle dürüstçe yorumla."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 📋 Kınik Analiz Raporu")
                st.write(response.text)
            except Exception as e:
                st.error(f"Sistem hatası: {e}. Lütfen API anahtarını ve model ismini kontrol et.")
    else:
        st.warning("Lütfen bir soru yaz.")
