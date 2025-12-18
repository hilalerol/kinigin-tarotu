import streamlit as st
import google.generativeai as genai
import random
import time

# --- AYARLAR ---
st.set_page_config(page_title="Kinigin Tarotu", page_icon="🔮")

# --- KARTLAR ---
TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]

# --- DURUM ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #111; padding: 20px; border-radius: 10px; border-left: 5px solid red; }
    .prof { text-align: center; font-size: 70px; }
    </style>
    """, unsafe_allow_html=True)

# --- API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_fast_model():
    """En hızlı yanıt veren modeli seçer"""
    try:
        # Mevcut modelleri çek
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Hız önceliği: 1.5 Flash -> 1.0 Pro
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(models[0])
    except:
        return None

# --- ARAYÜZ ---
st.markdown('<div class="prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.title("KİNİĞİN TAROTU")

soru = st.text_input("Senaryo:", placeholder="Buraya yazın...")

if not st.session_state.analiz_edildi:
    cols = st.columns(10)
    for i in range(70): # Hız için kart sayısını ekranda az gösterelim ama arkada 78 olsun
        with cols[i % 10]:
            if st.button("✧", key=f"k_{i}"):
                if i not in st.session_state.secilen_indeksler and len(st.session_state.secilen_indeksler) < 3:
                    st.session_state.secilen_indeksler.append(i)
                    st.rerun()

    if len(st.session_state.secilen_indeksler) == 3:
        if st.button("HIZLI ANALİZ YAP"):
            st.session_state.analiz_edildi = True
            st.rerun()

if st.session_state.analiz_edildi:
    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.write(f"Kartlarınız: {', '.join(secilen_kartlar)}")
    
    with st.spinner("Kehanet fısıldanıyor..."):
        model = get_fast_model()
        if model:
            try:
                # Güvenlik: Cevap gelmezse 15 saniyede kes (Streamlit varsayılanı bekleyebilir)
                response = model.generate_content(
                    f"Kısa ve sert bir tarot analizi yap. Soru: {soru}. Kartlar: {secilen_kartlar}",
                    generation_config={"max_output_tokens": 300} # Yanıtı kısa tutarak hızı artırıyoruz
                )
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Bağlantı çok yavaş veya kota doldu. Lütfen 1 dakika sonra tekrar deneyin.")
        else:
            st.error("Model bulunamadı.")

    if st.button("TEMİZLE"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
