import streamlit as st
import google.generativeai as genai

# --- TASARIM: Karanlık ve Profesyonel Arayüz ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #ff4b4b; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; font-weight: bold; border-radius: 10px; height: 3em; }
    .stMultiSelect div div div div { background-color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DOĞRUDAN API AYARI (Hızlı Çözüm) ---
MY_API_KEY = "AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4"
genai.configure(api_key=MY_API_KEY)

# Akıllı Model Seçici
@st.cache_resource
def load_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in models if '1.5-flash' in m), models[0])
        return genai.GenerativeModel(target), target
    except:
        return None, "Bağlantı Hatası"

model, model_name = load_model()

# --- GÖRSELLER ---
TAROT_IMAGES = {
    "Magician": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Moon": "https://upload.wikimedia.org/wikipedia/commons/f/f0/RWS_Tarot_18_Moon.jpg",
    "Tower": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg"
}

st.title("🔮 Kiniğin Tarotu")
st.write("### *Ekonomi, Risk ve Kaos Analiz Laboratuvarı*")

col1, col2 = st.columns([2, 1])

with col1:
    soru = st.text_input("Gerçeği duymaya hazır mısın?", placeholder="Örn: Bu disiplinsizlikle nasıl kariyer yaparım?")
    zayifliklar = st.multiselect("Sistem Arızalarını Seç:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme", "Yüksek Risk İştahı"])

with col2:
    st.info("Kınik Analiz: Zayıflıklarınızı veriye dönüştüren, duygu barındırmayan sert bir risk raporudur.")

if st.button("ANALİZİ BAŞLAT"):
    if soru and model:
        with st.spinner('Kınik zekâ verileri işliyor...'):
            try:
                prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle dürüstçe yorumla."
                response = model.generate_content(prompt)
                
                # Kart Görselleri
                c1, c2, c3 = st.columns(3)
                with c1: st.image(TAROT_IMAGES["Magician"], caption="Büyücü", width=150)
                with c2: st.image(TAROT_IMAGES["Moon"], caption="Ay", width=150)
                with c3: st.image(TAROT_IMAGES["Tower"], caption="Kule", width=150)
                
                st.divider()
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")
    else:
        st.warning("Lütfen bir soru sor.")

st.sidebar.caption(f"⚙️ Sistem: {model_name}")
st.sidebar.caption("📊 Hilal Erol | v2.0")
