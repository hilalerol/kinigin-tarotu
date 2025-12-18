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
    .witch-img { display: block; margin: 0 auto; width: 150px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API VE MODEL TESPİTİ (KRİTİK BÖLÜM) ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets panelinden MY_API_KEY tanımlanmamış!")

def force_get_any_model():
    """Hata almamak için izin verilen İLK modeli bulur"""
    try:
        # İzin verilen tüm modelleri çek
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not models:
            return None
        # En yeni modellerden birini seçmeye çalış, yoksa ilkini al
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
            if preferred in models:
                return genai.GenerativeModel(preferred)
        return genai.GenerativeModel(models[0])
    except Exception as e:
        st.error(f"Model Listesi Alınamadı: {e}")
        return None

# --- 6. ARAYÜZ ---
st.markdown('<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZhcWp2bXB4cWN4am14am14am14am14am14am14am14am14amImZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PXM/U6X9A55X765vP3YvP3/giphy.gif" class="witch-img">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("Senaryonu fısılda...", label_visibility="collapsed")

if not st.session_state.analiz_edildi:
    st.write(f"<p style='text-align:center;'>{len(st.session_state.secilen_indeksler)} / 3</p>", unsafe_allow_html=True)
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
    
    with st.spinner("Kınik analiz ediyor..."):
        model = force_get_any_model()
        if model:
            try:
                # Modeli ve adını kontrol et
                response = model.generate_content(f"Sert bir analiz yap. Soru: {soru}. Kartlar: {secilen_kartlar}")
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analiz Hatası: {e}")
        else:
            st.error("Google hesabınızda henüz aktif bir model bulunamadı.")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
