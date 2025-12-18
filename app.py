import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kinigin Tarotu Pro", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]

# --- 3. DURUM YÖNETİMİ ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 4. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; font-family: serif; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; border-radius: 8px; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    .prof-header { text-align: center; font-size: 80px; text-shadow: 0 0 20px #ff4b4b; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE OTOMATİK MODEL BULUCU ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets panelinden MY_API_KEY tanımlanmamış!")

def get_any_working_model():
    """Hangi model ismi geçerliyse onu otomatik bulur (404 hatasını bitirir)"""
    try:
        # Google'a 'Hangi modelleri kullanabilirim?' diye soruyoruz
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Öncelik sırası: Flash -> Pro -> Herhangi biri
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
            if target in available_models:
                return genai.GenerativeModel(target)
        
        # Eğer yukarıdakiler yoksa listedeki ilk modeli ver
        if available_models:
            return genai.GenerativeModel(available_models[0])
        return None
    except Exception as e:
        st.error(f"Modellere ulaşılamıyor: {e}")
        return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="prof-header">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Senaryonu fısılda...", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center; color:#555;'>{len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
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
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    
    with st.spinner("🔮 Profesör Minerva kozmik bağ kuruyor..."):
        model = get_any_working_model()
        if model:
            try:
                prompt = f"Sen sert bir ekonomi analistisin. Soru: {soru}. Kartlar: {secilen_kartlar}. Acımasızca analiz et."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analiz sırasında hata (Kota veya Bağlantı): {e}")
        else:
            st.error("Üzgünüm, şu an hiçbir yapay zeka modeli yanıt vermiyor.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
