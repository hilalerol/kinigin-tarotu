import streamlit as st
import google.generativeai as genai
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="The Cynic's Tarot", page_icon="🔮", layout="wide")

# --- 2. DESTE VE KOZMİK SİSTEM ---
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

KOZMIK_UYARILAR = [
    "Bugün aynalara fazla bakma, gördüğün kişi sen olmayabilirsin.",
    "Merkür fısıldıyor: O eski sevgiliye sakın yazma, sadece canı sıkılmış.",
    "Yıldızlar bugün cüzdanını sıkı tutmanı öneriyor, o indirim bir tuzak.",
    "Kozmik enerji: Kahveni sert, kararlarını daha sert al.",
    "Bugün sessizlik en büyük silahın. Konuşursan kaybedeceksin."
]

# --- 3. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #000; color: #e0e0e0; font-family: serif; }
    .main-title { text-align: center; color: white; text-shadow: 0 0 15px #ff4b4b; letter-spacing: 5px; }
    .report-box { background: #0a0a0a; padding: 25px; border: 1px solid #333; border-left: 5px solid #ff4b4b; border-radius: 10px; line-height: 1.8; color: #ddd; }
    .mystic-prof { text-align: center; font-size: 70px; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    .cosmic-alert { text-align: center; font-style: italic; color: #ff4b4b; font-size: 0.9rem; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DURUM YÖNETİMİ ---
if 'kart_sepeti' not in st.session_state: st.session_state.kart_sepeti = []
if 'analiz_durumu' not in st.session_state: st.session_state.analiz_durumu = False
if 'gunun_uyarisi' not in st.session_state: st.session_state.gunun_uyarisi = random.choice(KOZMIK_UYARILAR)

# --- 5. API VE MODEL ---
genai.configure(api_key=st.secrets["MY_API_KEY"])

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in available_models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except: return None

# --- 6. ARAYÜZ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="cosmic-alert">✨ Günün Kozmik Uyarısı: {st.session_state.gunun_uyarisi}</p>', unsafe_allow_html=True)

# PROFİL VE SORU
with st.expander("Kozmik Profilini Düzenle", expanded=True):
    soru = st.text_input("Sorun nedir fani?", placeholder="Örn: Bu iş teklifini kabul etmeli miyim?")
    c1, c2 = st.columns(2)
    with c1:
        konu = st.selectbox("Konu", ["Genel", "Aşk", "Para/Kariyer", "Sağlık"])
        yas = st.number_input("Yaş", 15, 99, 25)
    with c2:
        calisma = st.selectbox("İş Durumu", ["Çalışan", "Öğrenci", "İşsiz"])
        iliski = st.selectbox("İlişki", ["Bekar", "İlişkisi Var", "Karmaşık"])

# KART SEÇİMİ (DÜZELTİLEN BÖLÜM)
if not st.session_state.analiz_durumu:
    st.write(f"<p style='text-align:center;'>Enerji Mühürlendi: {len(st.session_state.kart_sepeti)} / 3</p>", unsafe_allow_html=True)
    cols = st.columns(13)
    for i in range(78):
        with cols[i % 13]:
            # Hatalı olan satır düzeltildi
            dugme_etiketi = "❂" if i in st.session_state.kart_sepeti else "✧"
            
            if st.button(dugme_etiketi, key=f"k_{i}"):
                if i not in st.session_state.kart_sepeti and len(st.session_state.kart_sepeti) < 3:
                    st.session_state.kart_sepeti.append(i)
                elif i in st.session_state.kart_sepeti:
                    st.session_state.kart_sepeti.remove(i)
                st.rerun()

    if len(st.session_state.kart_sepeti) == 3:
        if st.button("KADERİNİ MÜHÜRLE", use_container_width=True):
            st.session_state.analiz_durumu = True
            st.rerun()

# ANALİZ EKRANI
else:
    try:
        secilen_detaylar = []
        for idx in st.session_state.kart_sepeti:
            yon = " (TERS)" if random.random() < 0.3 else " (DÜZ)"
            secilen_detaylar.append(TAM_DESTE[idx] + yon)

        st.write(f"<p style='text-align:center; color:#ff4b4b;'>{ ' | '.join(secilen_detaylar) }</p>", unsafe_allow_html=True)
        
        with st.spinner("Profesör Minerva zehrini hazırlıyor..."):
            model = get_working_model()
            if model:
                prompt = f"""
                Sen 'The Cynic's Tarot' isimli sert, alaycı ve dürüst bir tarot yorumcususun. 
                Profil: {yas} yaşında, {calisma} durumunda, ilişkisi {iliski}. 
                Konu: {konu}. Soru: {soru}.
                Kartlar: {secilen_detaylar}.
                
                GÖREVİN:
                1. Kartları ve hayat durumunu birleştirerek sert bir analiz yap.
                2. Analizin sonuna 'ACI REÇETE' başlığı aç ve kullanıcıya yapması gereken 3 tavsiye ver.
                """
                res = model.generate_content(prompt)
                st.markdown(f"<div class='report-box'>{res.text}</div>", unsafe_allow_html=True)
            else:
                st.error("Kozmik bağlantı koptu.")
    except Exception as e:
        st.error(f"Hata: {e}")

    if st.button("YENİDEN BAŞLA"):
        st.session_state.kart_sepeti = []
        st.session_state.analiz_durumu = False
        st.rerun()
