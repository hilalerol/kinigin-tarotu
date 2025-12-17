import streamlit as st
import google.generativeai as genai

# 1. TASARIM: Karanlık ve Profesyonel Arayüz
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #ff4b4b; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. GÜVENLİK: API Anahtarını Kasadan (Secrets) Al
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ HATA: API Anahtarı Streamlit Secrets içine tanımlanmamış!")

# Akıllı Model Seçici
@st.cache_resource
def load_model():
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target = next((m for m in models if '1.5-flash' in m), models[0])
    return genai.GenerativeModel(target)

model = load_model()

# 3. GÖRSELLİK: Kart Arşivi
# (Bu linkler Rider-Waite destesi görselleridir)
TAROT_IMAGES = {
    "Magician": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Moon": "https://upload.wikimedia.org/wikipedia/commons/f/f0/RWS_Tarot_18_Moon.jpg",
    "Devil": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "Knight of Swords": "https://upload.wikimedia.org/wikipedia/commons/d/d4/RWS_Tarot_Knight_of_Swords.jpg",
    "Tower": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg"
}

st.title("🔮 Kiniğin Tarotu")
st.write("### *Ekonomi, Risk ve Kaos Analiz Laboratuvarı*")

col1, col2 = st.columns([2, 1])

with col1:
    soru = st.text_input("Gerçeği sormaya cesaretin var mı?", placeholder="Kariyerimdeki panik halini nasıl kâra dönüştürürüm?")
    zayifliklar = st.multiselect("Sistem Arızalarını Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme", "Duygusallık"])

with col2:
    st.info("Bu sistem, zayıflıklarınızı birer 'ekonomik girdi' olarak kabul eder ve size pazar odaklı bir risk raporu sunar.")

if st.button("ANALİZİ BAŞLAT"):
    if soru:
        with st.spinner('Kınik zekâ verileri işliyor...'):
            # Prompt Mühendisliği: Gemini'ye kart isimlerini vermesini söylüyoruz
            prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kart seç ve yorumla. Kartların İngilizce isimlerini (Magician, Moon gibi) mutlaka belirt."
            response = model.generate_content(prompt)
            
            # Kart resimlerini (temsili) gösterelim
            c1, c2, c3 = st.columns(3)
            with c1: st.image(TAROT_IMAGES["Magician"], caption="Potansiyel", width=150)
            with c2: st.image(TAROT_IMAGES["Moon"], caption="Belirsizlik", width=150)
            with c3: st.image(TAROT_IMAGES["Tower"], caption="Yıkım ve Yenilenme", width=150)
            
            st.divider()
            st.markdown(response.text)

st.sidebar.write("📊 Hilal Erol | Fintech Prototipi")
