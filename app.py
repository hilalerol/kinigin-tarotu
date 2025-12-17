import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# Tasarım (CSS) - Her yerin karanlık ve şık olması için
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #ff4b4b; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; height: 3em; font-weight: bold; border-radius: 10px; }
    h1, h2, h3 { color: #ff4b4b !important; }
    .stMarkdown { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- API AYARI ---

genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

# Modeli Çağır
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🔮 Kiniğin Tarotu")
st.markdown("### *Ekonomi Mezunu Sert Bir Analistten Risk Raporu*")

col1, col2 = st.columns([2, 1])

with col1:
    soru = st.text_input("Gerçeği duymaya hazır mısın?", placeholder="Örn: Kariyerimdeki bu belirsizlik ne zaman biter?")
    zayifliklar = st.multiselect("Zayıflık Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])

with col2:
    st.info("Kınik Analiz: Zayıflıklarınızı veriye dönüştüren duygusuz bir risk raporudur.")

if st.button("ANALİZİ BAŞLAT"):
    if soru:
        with st.spinner('Kınik zekâ verileri işliyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle dürüstçe yorumla."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("## 📊 ANALİZ RAPORU")
                st.write(response.text)
            except Exception as e:
                st.error(f"Bir pürüz çıktı: {e}")
    else:
        st.warning("Lütfen bir soru yaz.")

st.sidebar.write("📊 Hilal Erol | Fintech Prototipi")
