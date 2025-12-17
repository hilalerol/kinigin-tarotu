import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# --- ULTRA MODERN & KLAS CSS ---
st.markdown("""
    <style>
    /* Ana Arka Plan: Derin Uzay Siyahı */
    .stApp {
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* Başlık Alanı: Modern ve Minimal */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: 5px;
        text-align: center;
        color: #ffffff;
        text-transform: uppercase;
        margin-bottom: 0px;
    }
    
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 0.9em;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }

    /* Giriş Kutuları: Cam Efekti */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    /* Buton: Klas ve Keskin */
    .stButton button {
        width: 100%;
        background: linear-gradient(45deg, #444, #000) !important;
        color: white !important;
        border: 1px solid #555 !important;
        border-radius: 30px !important;
        letter-spacing: 2px !important;
        font-weight: bold !important;
        transition: 0.5s;
        height: 3.5em !important;
    }
    
    .stButton button:hover {
        background: white !important;
        color: black !important;
        border: 1px solid white !important;
    }

    /* Kart Alanı Tasarımı */
    .report-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        line-height: 1.8;
    }
    
    /* Kenar Çubuğu Gizleme ve Minimalizm */
    [data-testid="stSidebar"] {
        background-color: #050505;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API AYARI ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ARAYÜZ ---
st.markdown('<h1 class="main-title">KİNİĞİN TAROTU</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">FINANCIAL RISK & ARCHETYPAL ANALYSIS</p>', unsafe_allow_html=True)

container = st.container()
with container:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        soru = st.text_input("", placeholder="Sistemsel bir soru sor...")
        zayifliklar = st.multiselect("Zayıflıklar", ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme"])
        
        st.write("") # Boşluk
        if st.button("ANALİZİ BAŞLAT"):
            if soru:
                with st.spinner('Hesaplanıyor...'):
                    try:
                        prompt = f"Sen Kiniğin Tarotu'sun. Ekonomi mezunu sert bir analistsin. Soru: {soru}. Zayıflıklar: {zayifliklar}. 3 kartla ekonomi diliyle yorumla."
                        response = model.generate_content(prompt)
                        st.markdown('<div class="report-box">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Sistem Hatası: {e}")
            else:
                st.warning("Lütfen girdi sağlayın.")

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">v3.0 Executive Edition | HE</p>', unsafe_allow_html=True)
