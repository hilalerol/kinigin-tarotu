import streamlit as st
import google.generativeai as genai
import random
from fpdf import FPDF

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kiniğin Tarotu Pro", page_icon="🔮", layout="wide")

# --- 2. DESTE (78 KART) ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

# --- 3. DURUM YÖNETİMİ ---
if 'lang' not in st.session_state: st.session_state.lang = "Türkçe"
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

texts = {
    "Türkçe": {
        "title": "KİNİĞİN TAROTU",
        "sub": "78 Kartlık Desteden 3 Sembol Seç...",
        "placeholder": "Analiz edilecek durumu yazın...",
        "btn_reveal": "KEHANETİ AÇ",
        "btn_reset": "YENİDEN BAŞLA",
        "pdf_btn": "📄 Analizi PDF Olarak İndir",
        "prompt": "Sen sert bir ekonomi analistisin. Seçilen tarot kartlarını kullanarak dürüst ve acımasız bir risk analizi yaz."
    },
    "English": {
        "title": "THE CYNIC'S TAROT",
        "sub": "Select 3 Symbols from the 78-Card Deck...",
        "placeholder": "Enter your scenario here...",
        "btn_reveal": "REVEAL DESTINY",
        "btn_reset": "RESTART",
        "pdf_btn": "📄 Download Analysis as PDF",
        "prompt": "You are a harsh economic analyst. Provide an honest and ruthless risk analysis based on the selected cards."
    }
}

with st.sidebar:
    st.title("🌐 Language")
    st.session_state.lang = st.radio("", ["Türkçe", "English"])
    st.divider()
    st.caption("Geliştirici: Hilal Erol | v14.0")

L = texts[st.session_state.lang]

# --- 4. PDF OLUŞTURUCU ---
def create_pdf(text, lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "KINIGIN TAROTU RAPORU", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    tr_chars = {"ş":"s","Ş":"S","ı":"i","İ":"I","ğ":"g","Ğ":"G","ü":"u","Ü":"U","ö":"o","Ö":"O","ç":"c","Ç":"C"}
    for k, v in tr_chars.items(): text = text.replace(k, v)
    safe_text = text.encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 8, safe_text)
    return pdf.output(dest="S").encode('latin-1')

# --- 5. TASARIM ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #ffffff; }}
    .main-title {{ font-family: serif; text-align: center; letter-spacing: 7px; color: #ffffff; padding-top: 10px; }}
    .stButton button {{ background-color: #0e0e0e !important; border: 1px solid #333 !important; color: #666 !important; font-size: 16px !important; height: 55px; width: 100%; transition: 0.3s; }}
    .stButton button:hover {{ border-color: #ff4b4b !important; color: #fff !important; }}
    .report-box {{ background: #0a0a0a; padding: 25px; border-radius: 12px; border-left: 5px solid #ff4b4b; color: #d0d0d0; line-height: 1.7; font-family: 'Georgia', serif; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. API BAĞLANTISI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except Exception:
    st.error("Secrets panelinden MY_API_KEY tanımlanmamış!")

# --- 7. ARAYÜZ ---
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#555;'>{L['sub']}</p>", unsafe_allow_html=True)

soru = st.text_input("", placeholder=L["placeholder"], label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"### ✧ {len(st.session_state.secilen_indeksler)} / 3")
    for row in range(6):
        cols = st.columns(13)
        for col in range(13):
            idx = row * 13 + col
            if idx < 78:
                with cols[col]:
                    is_sel = idx in st.session_state.secilen_indeksler
                    label = "❂" if is_sel else "✧"
                    if st.button(label, key=f"k_{idx}"):
                        if not is_sel and len(st.session_state.secilen_indeksler) < 3:
                            st.session_state.secilen_indeksler.append(idx)
                            st.rerun()
                        elif is_sel:
                            st.session_state.secilen_indeksler.remove(idx)
                            st.rerun()

    if len(st.session_state.secilen_indeksler) == 3:
        if st.button(L["btn_reveal"], use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]: st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid #222; border-radius:10px; color:#aaa;'>{kn}</div>", unsafe_allow_html=True)
            
    with st.spinner("Kınik analiz ediyor..."):
        try:
            # DİNAMİK MODEL TESPİTİ
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            best_model = next((m for m in available_models if '1.5-flash' in m or 'gemini-pro' in m), available_models[0] if available_models else None)
            
            if best_model:
                model = genai.GenerativeModel(best_model)
                response = model.generate_content(f"{L['prompt']} Soru: {soru}. Kartlar: {secilen_kartlar}.")
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                
                pdf_val = create_pdf(response.text, st.session_state.lang)
                st.download_button(L["pdf_btn"], data=pdf_val, file_name="Tarot_Report.pdf", mime="application/pdf")
            else:
                st.error("Uygun model bulunamadı.")
        except Exception as e:
            st.error(f"Hata: {str(e)}")
            
    if st.button(L["btn_reset"]):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
