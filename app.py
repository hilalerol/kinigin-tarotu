import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot Pro", page_icon="📊", layout="wide")

# --- 2. DİL VE RİSK TANIMLARI ---
if 'lang' not in st.session_state: st.session_state.lang = "Türkçe"

with st.sidebar:
    st.title("🌐 Language")
    st.session_state.lang = st.radio("", ["Türkçe", "English"])
    st.divider()
    st.caption("Dev: Hilal Erol | v6.0 Pro")

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU PRO",
        "sub": "STRATEJİK RİSK YÖNETİMİ & ANALİZ",
        "label": "Sistem Zafiyetlerini Seçin:",
        "options": ["Disiplinsizlik", "Panik", "Kararsızlık", "Erteleme", "Duygusallık"],
        "btn": "RİSK ANALİZİNİ BAŞLAT",
        "stability": "SİSTEM KARARLILIK SKORU",
        "prompt": "Sen bir ekonomi analistisin. Seçilen zayıflıkları 'Sistemik Risk' olarak ele al. Her zayıflığı bir fırsata (arbitraj) çeviren sert bir rapor yaz."
    },
    "English": {
        "title": "THE CYNIC'S TAROT PRO",
        "sub": "STRATEGIC RISK MANAGEMENT & ANALYSIS",
        "label": "Select Systemic Weaknesses:",
        "options": ["Indiscipline", "Panic", "Indecisiveness", "Procrastination", "Emotionality"],
        "btn": "START RISK ANALYSIS",
        "stability": "SYSTEM STABILITY SCORE",
        "prompt": "You are an economic analyst. Treat the selected weaknesses as 'Systemic Risks'. Write a harsh report that turns each weakness into a strategic opportunity (arbitrage)."
    }
}
L = texts[st.session_state.lang]

# --- 3. CSS (Executive Tasarım) ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-weight: 800; letter-spacing: 5px; text-align: center; color: #ff4b4b; }
    .report-box { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. API & MODEL ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 5. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#666;'>{L['sub']}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    soru = st.text_input("Senaryo:", placeholder="Örn: Portföyümü nasıl yönetmeliyim?")
    zafiyetler = st.multiselect(L["label"], L["options"])
    
    # DİNAMİK RİSK SKORU (Farklı Bakış Açısı)
    if zafiyetler:
        skor = 100 - (len(zafiyetler) * 20)
        st.write(f"**{L['stability']}**")
        color = "green" if skor > 60 else "orange" if skor > 30 else "red"
        st.progress(skor / 100)
        st.markdown(f"<h3 style='color:{color}; text-align:right;'>%{skor}</h3>", unsafe_allow_html=True)

with col2:
    if st.button(L["btn"]):
        if soru:
            with st.spinner("Analiz ediliyor..."):
                res = model.generate_content(f"{L['prompt']} Senaryo: {soru}. Zayıflıklar: {zafiyetler}")
                st.markdown(f'<div class="report-box">{res.text}</div>', unsafe_allow_html=True)
                
                # PDF butonu da burada kalabilir (Önceki sürümden ekleyebilirsin)
        else:
            st.warning("Lütfen bir senaryo girin.")
