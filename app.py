import streamlit as st
import google.generativeai as genai
import random
import time

# --- 1. SAYFA VE KOZMIK AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

KOZMIK_UYARILAR = [
    "Bugün aynalara fazla bakma, gördüğün kişi sen olmayabilirsin.",
    "Merkür fısıldıyor: O eski sevgiliye sakın yazma, sadece canı sıkılmış.",
    "Yıldızlar bugün cüzdanını sıkı tutmanı öneriyor, o indirim bir tuzak.",
    "Kozmik enerji: Kahveni sert, kararlarını daha sert al.",
    "Bugün sessizlik en büyük silahın. Konuşursan kaybedeceksin.",
    "Kaderin bugün bir pamuk ipliğine bağlı, sakın o ipliği çekme."
]

# --- 2. MISTIK TASARIM (CSS) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: #e0e0e0; font-family: 'Special Elite', cursive; }
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: #ffffff; letter-spacing: 10px; text-shadow: 0 0 15px #ff4b4b; margin-top: 10px; }
    .cosmic-alert { text-align: center; font-style: italic; color: #ff4b4b; font-size: 0.9rem; margin-bottom: 25px; text-shadow: 0 0 5px #000; }
    
    /* Butonlar */
    .stButton button { 
        background: rgba(15, 15, 15, 0.9) !important; border: 1px solid #333 !important; 
        color: #ff4b4b !important; border-radius: 8px !important; font-size: 20px !important; 
        transition: 0.4s ease; width: 100%;
    }
    .stButton button:hover { border-color: #ff4b4b !important; color: white !important; box-shadow: 0 0 20px #ff4b4b; transform: scale(1.1); }
    
    /* Analiz Kutusu */
    .report-box { background: rgba(5, 5, 5, 0.95); padding: 30px; border: 1px solid #444; border-left: 5px solid #ff4b4b; border-radius: 15px; line-height: 1.8; color: #d1d1d1; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
    
    /* Profesör Animasyonu */
    .mystic-prof { text-align: center; font-size: 80px; animation: float 4s infinite ease-in-out; filter: drop-shadow(0 0 15px #ff4b4b); }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    
    /* Form Alanları */
    div[data-testid="stExpander"] { background: rgba(10, 10, 10, 0.8); border: 1px solid #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = False
if 'gunun_uyarisi' not in st.session_state: st.session_state.gunun_uyarisi = random.choice(KOZMIK_UYARILAR)

# --- 4. API BAĞLANTISI ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in available_models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except: return None

# --- 5. ANA EKRAN ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="cosmic-alert">✨ {st.session_state.gunun_uyarisi}</p>', unsafe_allow_html=True)

# PROFİL VE SORU ALANI
with st.expander("🔮 RUHUNU VE DURUMUNU AÇIKLA", expanded=True):
    soru = st.text_input("Neyi bilmek istiyorsun fani?", placeholder="Örn: Bu yıl zengin olacak mıyım?")
    c1, c2, c3 = st.columns(3)
    with c1:
        konu = st.selectbox("Konu", ["Genel", "Aşk ve İlişkiler", "Para ve Kariyer", "Sağlık"])
        yas = st.number_input("Yaşın", 15, 99, 25)
    with c2:
        calisma = st.selectbox("İş Durumu", ["Çalışıyorum", "Öğrenciyim", "İş Arıyorum", "Çalışmıyorum"])
        medeni = st.selectbox("Medeni Hal", ["Bekar", "Nişanlı", "Evli", "Boşanmış"])
    with c3:
        iliski = st.selectbox("İlişki Durumu", ["İlişkim var", "İlişkim yok", "Karmaşık", "Platonik"])

# KART SEÇİM SİSTEMİ
if not st.session_state.analiz_durumu:
    st.write(f"<p style='text-align:center; letter-spacing:2px;'>Kader Seçiliyor: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
    
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            label = "❂" if i in st.session_state.kart_sepeti else "✧"
            if st.button(label, key=f"btn_{i}"):
                if i not in st.session_state.kart_sepeti and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                elif i in st.session_state.kart_sepeti:
                    st.session_state.kart_sepeti.remove(i)
                st.rerun()

    if len(st.session_state.kart_sepeti) == 3:
        if st.button("KADERİMİ MÜHÜRLE VE OKU", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

# ANALİZ VE SONUÇ EKRANI
else:
    try:
        # TERS KART HESAPLAMA
        secilen_kartlar_ve_yonler = []
        for idx in st.session_state.kart_sepeti:
            yon = " (TERS)" if random.random() < 0.3 else " (DÜZ)"
            secilen_kartlar_ve_yonler.append(TAM_DESTE[idx] + yon)
        
        st.markdown(f"<p style='text-align:center; color:#ff4b4b; font-size:1.2rem;'>{ ' • '.join(secilen_kartlar_ve_yonler) }</p>", unsafe_allow_html=True)
        
        with st.spinner("Profesör Minerva enerjiyi kelimelere döküyor..."):
            model = get_working_model()
            if model:
                prompt = f"""
                Sen 'The Cynic's Tarot' isimli, çok dürüst, sert, alaycı ve gerçekçi bir tarot yorumcususun.
                Kullanıcı: {yas} yaşında, {calisma} durumunda, medeni hali {medeni}, ilişkisi {iliski}.
                Soru: {soru} (Konu: {konu})
                Kartlar: {secilen_kartlar_ve_yonler}
                
                TALİMATLAR:
                1. Kartların düz veya TERS gelme durumlarını dikkate alarak sert bir analiz yap.
                2. Analiz bittiğinde '---' ayıracı koy ve altına '🧪 ACI REÇETE' başlığıyla kullanıcıya yapması gereken 3 somut, dürüst ve sert tavsiye ver.
                """
                response = model.generate_content(prompt, generation_config={"max_output_tokens": 650})
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.error("Kozmik hatlar şu an çok yoğun, lütfen bir dakika sonra tekrar dene.")
                
    except Exception as e:
        if "429" in str(e):
            st.warning("🌙 Kota doldu. Profesör Minerva şu an dinleniyor. Lütfen 1 dakika bekleyip butona tekrar basın.")
        else:
            st.error(f"Hata: {e}")

    if st.button("KEHANETİ SIFIRLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
