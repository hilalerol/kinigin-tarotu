import streamlit as st
import google.generativeai as genai
import random

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. 78 KARTLIK DESTE TANIMI ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. SESSION STATE ---
if 'secilen_indeksler' not in st.session_state:
    st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state:
    st.session_state.analiz_edildi = False

# --- 4. CSS (Executive Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { font-family: serif; text-align: center; letter-spacing: 8px; color: #ffffff; padding-top: 20px; }
    .stButton button { 
        background-color: #0a0a0a !important; 
        border: 1px solid #333 !important; 
        color: #444 !important; 
        font-size: 16px !important; 
        height: 50px !important;
        width: 100% !important; 
        transition: 0.3s;
    }
    .stButton button:hover { border-color: #ff4b4b !important; color: white !important; }
    .report-box { background: #0a0a0a; padding: 30px; border-radius: 15px; border: 1px solid #222; border-left: 5px solid #ff4b4b; line-height: 1.8; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE AKILLI MODEL SEÇİCİ ---
genai.configure(api_key="AIzaSyDmD1S5e1WmtiiKR63MRNM6Flbe1MER5i4")

def get_response_safely(prompt_text):
    """NotFound hatasını önlemek için farklı model varyasyonlarını dener"""
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt_text)
            return response.text
        except Exception:
            continue
    return "Şu an bağlantı kurulamıyor. Lütfen API anahtarınızı ve internetinizi kontrol edin."

# --- 6. ARAYÜZ ---
st.markdown('<h1 class="main-title">KİNİĞİN TAROTU</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#555;'>Desteden 3 sembol seçerek kaderini fısılda...</p>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Senaryonu buraya yaz...", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"### ✧ Seçilen: {len(st.session_state.secilen_indeksler)} / 3")
    
    # 78 Kart Matrisi (13 sütun x 6 satır)
    for row in range(6):
        cols = st.columns(13)
        for col in range(13):
            idx = row * 13 + col
            if idx < 78:
                with cols[col]:
                    # Seçilen kartı görsel olarak işaretle
                    is_selected = idx in st.session_state.secilen_indeksler
                    label = "❂" if is_selected else "✧"
                    if st.button(label, key=f"k_{idx}"):
                        if not is_selected and len(st.session_state.secilen_indeksler) < 3:
                            st.session_state.secilen_indeksler.append(idx)
                            st.rerun()
                        elif is_selected:
                            st.session_state.secilen_indeksler.remove(idx)
                            st.rerun()

# ANALİZ BUTONU
if len(st.session_state.secilen_indeksler) == 3 and not st.session_state.analiz_edildi:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("KEHANETİ AÇ", use_container_width=True):
        st.session_state.analiz_edildi = True
        st.rerun()

# SONUÇ EKRANI
if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    
    st.divider()
    st.write("### 🃏 Kaderin Şifreleri")
    cols = st.columns(3)
    for i, k_name in enumerate(secilen_kartlar):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; padding:20px; border:1px solid #333; border-radius:10px;'>{k_name}</div>", unsafe_allow_html=True)
            
    with st.spinner("Kınik analiz ediyor..."):
        prompt = f"Sen sert bir ekonomi analistisin. Soru: {soru}. Kartlar: {secilen_kartlar}. Bu kartları ve soruyu birleştirerek dürüst, sert ve stratejik bir rapor yaz."
        result = get_response_safely(prompt)
        st.markdown(f'<div class="report-box">{result}</div>', unsafe_allow_html=True)
    
    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
