import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Kinigin Tarotu", page_icon="🔮", layout="wide")

# --- 2. DESTE ---
TAM_DESTE = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]

# --- 3. SESSION STATE ---
if 'secilen_indeksler' not in st.session_state: st.session_state.secilen_indeksler = []
if 'analiz_edildi' not in st.session_state: st.session_state.analiz_edildi = False

# --- 4. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .report-box { background: #0a0a0a; padding: 25px; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #888 !important; width: 100%; }
    .stButton button:hover { border-color: #ff4b4b !important; color: #fff !important; }
    /* Profesör Animasyonu İçin */
    .prof-container { text-align: center; font-size: 100px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. API AYARI ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("Secrets panelinden MY_API_KEY bulunamadı!")

# --- 6. ARAYÜZ ---
# Görsel gelmiyorsa, mistik bir animasyon efektiyle emoji profesör kullanalım (Bu asla bozulmaz)
st.markdown('<div class="prof-container">🧙‍♀️✨</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>KİNİĞİN TAROTU</h1>", unsafe_allow_html=True)

soru = st.text_input("", placeholder="Senaryonu buraya yaz...", label_visibility="collapsed")

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
    # Mistik Bekleme Yazısı
    msg = st.empty()
    msg.markdown("<h3 style='text-align:center; color:#ff4b4b;'>🔮 Profesör Minerva verileri büyülüyor...</h3>", unsafe_allow_html=True)
    time.sleep(2)
    msg.empty()

    secilen_kartlar = random.sample(TAM_DESTE, 3)
    st.divider()
    
    with st.spinner("Analiz hazırlanıyor..."):
        try:
            # 404 hatasını önlemek için EN GARANTİ model adını kullanıyoruz
            model = genai.GenerativeModel('gemini-pro') 
            prompt = f"Sert bir ekonomi analisti gibi dürüst bir tarot yorumu yap. Soru: {soru}. Kartlar: {secilen_kartlar}."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            # Eğer gemini-pro da hata verirse otomatik listeleme yapalım
            try:
                available_models = [m.name for m in genai.list_models()]
                model = genai.GenerativeModel(available_models[0])
                response = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except:
                st.error(f"Sistemsel bir kısıtlama var: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.secilen_indeksler = []
        st.session_state.analiz_edildi = False
        st.rerun()
