import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# --- MODERN & KLAS CSS (Yazı Alanı Düzeltilmiş) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* YAZI YAZILAN ALAN (INPUT BOX) AYARLARI */
    /* Burası beyaz zemin sorununu çözer */
    .stTextInput div[data-baseweb="input"] {
        background-color: #1a1c23 !important; /* Koyu Gri/Siyah zemin */
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .stTextInput input {
        color: #ffffff !important; /* Yazı rengi bembeyaz */
        background-color: transparent !important;
    }

    /* Çoklu Seçim (Multiselect) Alanı */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #1a1c23 !important;
    }
    
    /* Buton Tasarımı */
    .stButton button {
        width: 100%;
        background: linear-gradient(45deg, #333, #000) !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        height: 3.5em !important;
    }
    
    /* Başlıklar */
    .main-title {
        color: #ffffff;
        text-align: center;
        letter-spacing: 8px;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL YÖNETİMİ ---
# BURAYA KENDİ ANAHTARINI YAPIŞTIR
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

@st.cache_resource
def load_dynamic_model():
    try:
        # Çalışan modelleri listele
        working_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Varsa 1.5-flash, yoksa listedeki ilk modeli seç
        target = next((m for m in working_models if '1.5-flash' in m), working_models[0])
        return genai.GenerativeModel(target), target
    except Exception:
        # Hata durumunda güvenli liman
        return genai.GenerativeModel('gemini-pro'), "gemini-pro"

model, model_name = load_dynamic_model()

# --- 3. ARAYÜZ ---
st.markdown('<h1 class="main-title">KİNİĞİN TAROTU</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">FINANCIAL RISK & ARCHETYPAL ANALYSIS</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    soru = st.text_input("", placeholder="Analiz edilecek senaryoyu girin...")
    zayifliklar = st.multiselect("Sistem Zafiyetleri:", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])
    
    st.write("")
    if st.button("ANALİZİ BAŞLAT"):
        if soru:
            with st.spinner('Kınik zekâ verileri işliyor...'):
                try:
                    prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kart seç ve ekonomi diliyle dürüstçe yorumla."
                    response = model.generate_content(prompt)
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Sistem hatası: {e}")
        else:
            st.warning("Lütfen bir soru girin.")

st.sidebar.caption(f"⚙️ Kernel: {model_name}")
st.sidebar.caption("📊 Dev: Hilal Erol | v3.1 Executive")
