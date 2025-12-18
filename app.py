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
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; border-radius: 8px; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    .mystic-prof { text-align: center; font-size: 80px; margin-bottom: 10px; text-shadow: 0 0 20px #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE DİNAMİK MODEL BULUCU ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_actual_model():
    """Google'ın o an kabul ettiği gerçek model ismini bulur"""
    try:
        # Google'dan aktif model listesini al
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Tercih sıramız
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash', 'gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target)
        # Hiçbiri yoksa listedeki ilk modeli ver
        return genai.GenerativeModel(models[0]) if models else None
    except Exception as e:
        st.error(f"Modellere ulaşılamadı: {e}")
        return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; letter-spacing: 5px;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Senaryonu buraya yaz...", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#444;'>{len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
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
    # Mistik bekleme
    placeholder = st.empty()
    placeholder.markdown("<h3 style='text-align:center; color:#ff4b4b;'>🔮 Profesör Minerva enerjiyi topluyor...</h3>", unsafe_allow_html=True)
    time.sleep(1.5)
    placeholder.empty()

    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    
    with st.spinner("Analiz hazırlanıyor..."):
        model = get_actual_model()
        if model:
            try:
                prompt = f"Sen sert bir ekonomi analistisin. Soru: {soru}. Kartlar: {secilen_kartlar}. Acımasızca analiz et."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analiz sırasında hata: {e}")
        else:
            st.error("Üzgünüm, şu an hiçbir yapay zeka modeli yanıt vermiyor.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
