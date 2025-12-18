import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kiniğin Tarotu", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]

# --- 3. SESSION STATE ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 4. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; font-family: serif; }
    .witch-img { display: block; margin: 0 auto; width: 250px; border-radius: 20px; box-shadow: 0 0 20px rgba(255, 75, 75, 0.5); }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API AYARI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Lütfen Secrets panelinden MY_API_KEY tanımlayın.")

def get_working_model():
    """Hangi model aktifse onu bulur (404 hatasını önler)"""
    try:
        # Mevcut modelleri listele
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # En güvenilir olanları sırayla dene
        for m_name in ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash', 'gemini-pro']:
            if m_name in available_models:
                return genai.GenerativeModel(m_name)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except:
        return None

# --- 6. ARAYÜZ ---
# Hareketli Profesör (Görselin açılması için daha güvenli bir link)
st.markdown('<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZhcWp2bXB4cWN4am14am14am14am14am14am14am14am14amImZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PXM/U6X9A55X765vP3YvP3/giphy.gif" class="witch-img">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; letter-spacing: 5px;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Analiz edilecek senaryoyu buraya fısılda...", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#555;'>Seçilen: {len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
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
        if st.button("KEHANETİ AÇ", use_container_width=True):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    # Mistik Bekleme
    msg_box = st.empty()
    msg_box.markdown("<h3 style='text-align:center; color:#ff4b4b;'>🔮 Profesör verileri büyülüyor...</h3>", unsafe_allow_html=True)
    time.sleep(2)
    msg_box.empty()

    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    cols = st.columns(3)
    for i, kn in enumerate(secilen_kartlar):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; padding:20px; border:1px solid #222; border-radius:10px;'>{kn}</div>", unsafe_allow_html=True)
    
    with st.spinner("..."):
        model = get_working_model()
        if model:
            try:
                prompt = f"Sen sert bir ekonomi analistisin. Soru: {soru}. Kartlar: {secilen_kartlar}. Acımasızca analiz et."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Hata: {e}")
        else:
            st.error("İzin verilen model bulunamadı.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
