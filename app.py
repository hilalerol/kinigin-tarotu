import streamlit as st
import google.generativeai as genai
import random
import time
from fpdf import FPDF

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = "Türkçe"
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU",
        "sub": "78 Kartlık Desteden 3 Sembol Seç...",
        "placeholder": "Analiz edilecek senaryoyu yazın...",
        "btn_reveal": "KEHANETİ AÇ",
        "btn_reset": "YENİDEN BAŞLA",
        "pdf_btn": "📄 Analizi İndir",
        "loading": "Profesör verileri büyülüyor...",
        "prompt": "Sen sert bir ekonomi analistisin. Seçilen tarot kartlarını kullanarak dürüst ve acımasız bir risk analizi yaz."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "Select 3 Symbols from the 78-Card Deck...",
        "placeholder": "Enter your scenario...",
        "btn_reveal": "REVEAL DESTINY",
        "btn_reset": "RESTART",
        "pdf_btn": "📄 Download Report",
        "loading": "Professor is enchanting the data...",
        "prompt": "You are a harsh economic analyst. Provide an honest and ruthless risk analysis based on the cards."
    }
}
L = texts[st.session_state.lang]

# --- 4. PDF FONKSİYONU ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "KINIGIN TAROTU RAPORU", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    tr_map = {"ş":"s","Ş":"S","ı":"i","İ":"I","ğ":"g","Ğ":"G","ü":"u","Ü":"U","ö":"o","Ö":"O","ç":"c","Ç":"C"}
    for k, v in tr_map.items(): text = text.replace(k, v)
    safe_text = text.encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 8, safe_text)
    return pdf.output(dest="S").encode('latin-1')

# --- 5. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .main-title { font-family: serif; text-align: center; letter-spacing: 7px; color: #fff; margin-bottom: 0; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; height: 50px; border-radius: 10px; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; font-family: serif; }
    .witch-img { display: block; margin: 0 auto; width: 180px; filter: drop-shadow(0 0 10px #ff4b4b); }
    </style>
    """, unsafe_allow_html=True)

# --- 6. API ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

# --- 7. ARAYÜZ ---
with st.sidebar:
    st.session_state.lang = st.radio("Dil / Language", ["Türkçe", "English"])
    st.divider()
    st.caption("Hilal Erol | v18.0")

# Profesör Her Zaman Üstte
st.markdown(f'<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZhcWp2bXB4cWN4am14am14am14am14am14am14am14am14amImZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PXM/U6X9A55X765vP3YvP3/giphy.gif" class="witch-img">', unsafe_allow_html=True)
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.secilen_indeksler else "✧"
            if st.button(label, key=f"k_{i}"):
                if i not in st.session_state.secilen_indeksler and len(st.session_state.secilen_indeksler) < 3:
                    st.session_state.secilen_indeksler.append(i)
                    st.rerun()
                elif i in st.session_state.secilen_indeksler:
                    st.session_state.secilen_indeksler.remove(i)
                    st.rerun()

    if len(st.session_state.secilen_indeksler) == 3:
        if st.button(L["btn_reveal"], use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    # Büyü Efekti
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"<h3 style='text-align:center; color:#ff4b4b;'>{L['loading']}</h3>", unsafe_allow_html=True)
        time.sleep(2)
    placeholder.empty()

    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]: st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid #222; border-radius:10px;'>{kn}</div>", unsafe_allow_html=True)
    
    with st.spinner("..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}.")
            st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            
            pdf_val = create_pdf(response.text)
            st.download_button(L["pdf_btn"], data=pdf_val, file_name="Kinigin_Tarotu.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Hata: {e}")

    if st.button(L["btn_reset"]):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
