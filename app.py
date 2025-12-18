import streamlit as st
import google.generativeai as genai
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. AYARLAR VE TASARIM ---
st.set_page_config(page_title="Minerva Tarot Premium", page_icon="🔮", layout="wide")

BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: #e0e0e0; font-family: 'Special Elite', cursive; }
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: white; letter-spacing: 5px; text-shadow: 0 0 15px #ff4b4b; }
    .premium-card { background: rgba(10, 10, 10, 0.9); padding: 25px; border: 1px solid #ff4b4b; border-radius: 15px; margin-bottom: 20px; }
    .payment-link { background: #ff4b4b; color: white !important; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 50px; display: inline-block; margin: 20px 0; font-size: 1.1rem; }
    .mystic-prof { text-align: center; font-size: 60px; animation: float 4s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    .stButton button { background: #111 !important; border: 1px solid #333 !important; color: #ff4b4b !important; width: 100%; }
    .stButton button:hover { border-color: #ff4b4b !important; transform: scale(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DURUM YÖNETİMİ ---
if 'step' not in st.session_state: st.session_state.step = "form"
if 'sepet' not in st.session_state: st.session_state.sepet = []

# --- 3. MAİL MOTORU ---
def mail_at(alici, soru, analiz):
    try:
        sender = st.secrets["hilalerol1041@gmail.com"]
        pwd = st.secrets["whwg alpx qxvk sztm"]
        msg = MIMEMultipart()
        msg['From'] = f"Profesör Minerva <{sender}>"
        msg['To'] = alici
        msg['Subject'] = "Kaderin Mühürlendi: Senin Özel Analizin"
        
        html = f"""
        <div style="background:#000; color:#ddd; padding:20px; border:2px solid #ff4b4b; font-family:serif;">
            <h2 style="color:#ff4b4b; text-align:center;">MINERVA'NIN KEHANETİ</h2>
            <p><b>Soru:</b> {soru}</p>
            <div style="background:#111; padding:15px; border-radius:10px; line-height:1.6;">{analiz.replace(chr(10), '<br>')}</div>
            <p style="text-align:right; color:#ff4b4b; font-weight:bold;">— Profesör Minerva</p>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pwd)
            server.send_message(msg)
        return True
    except: return False

# --- 4. AKIŞ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)

# ADIM 1: DETAYLI FORM VE KART SEÇİMİ
if st.session_state.step == "form":
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        email = st.text_input("Analizinin gönderileceği mail:")
        soru = st.text_area("Sorun nedir fani?")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            yas = st.number_input("Yaşın", 15, 99, 25)
            konu = st.selectbox("Konu", ["Genel", "Aşk", "Para", "Sağlık"])
        with c2:
            calisma = st.selectbox("İş Durumu", ["Çalışıyorum", "Öğrenci", "İş Arıyorum", "Çalışmıyorum"])
            medeni = st.selectbox("Medeni Hal", ["Bekar", "Evli", "Nişanlı", "Boşanmış"])
        with c3:
            iliski = st.selectbox("İlişki Durumu", ["Var", "Yok", "Karmaşık", "Platonik"])
        
        st.write("---")
        st.write(f"🔮 **Ruhun için 3 Kart Seç:** {len(st.session_state.sepet)}/3")
        
        cols = st.columns(13)
        for i in range(78):
            with cols[i % 13]:
                label = "❂" if i in st.session_state.sepet else "✧"
                if st.button(label, key=f"k{i}"):
                    if i not in st.session_state.sepet and len(st.session_state.sepet) < 3:
                        st.session_state.sepet.append(i)
                        st.rerun()
                    elif i in st.session_state.sepet:
                        st.session_state.sepet.remove(i)
                        st.rerun()
        
        if len(st.session_state.sepet) == 3 and email and soru:
            if st.button("KEHANETİMİ HAZIRLA", use_container_width=True):
                with st.spinner("Minerva kartları okuyor..."):
                    genai.configure(api_key=st.secrets["MY_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    secilen_kartlar = []
                    for idx in st.session_state.sepet:
                        yon = " (TERS)" if random.random() < 0.3 else " (DÜZ)"
                        secilen_kartlar.append(TAM_DESTE[idx] + yon)
                    
                    # AI Prompt
                    prompt = f"""
                    Sen 'The Cynic's Tarot'sun. Sert, alaycı ve dürüst ol.
                    Profil: {yas} yaşında, {calisma}, {medeni}, ilişkisi {iliski}.
                    Konu: {konu}. Soru: {soru}.
                    Kartlar: {secilen_kartlar}.
                    Analiz yap ve sonuna '🧪 ACI REÇETE' başlığıyla 3 sert tavsiye ekle.
                    """
                    res = model.generate_content(prompt)
                    
                    st.session_state.final_analysis = res.text
                    st.session_state.final_email = email
                    st.session_state.final_question = soru
                    st.session_state.step = "payment"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ADIM 2: ÖDEME EKRANI
elif st.session_state.step == "payment":
    st.markdown('<div class="premium-card" style="text-align:center;">', unsafe_allow_html=True)
    st.header("⏳ Analizin Mühürlendi")
    st.write("Profesör Minerva analizi tamamladı. Mailine ulaşması için son bir adım kaldı.")
    
    # Kendi Shopier linkini buraya koymalısın
    shopier_url = "https://www.shopier.com/SizinDukkanLinkiniz" 
    st.markdown(f'<a href="{https://www.shopier.com/GoldenArcanaTarot/42299924}" target="_blank" class="payment-link">💳 50 TL ÖDE VE ANALİZİ AL</a>', unsafe_allow_html=True)
    
    st.write("---")
    if st.button("ÖDEMEYİ YAPTIM, MAİLİMİ GÖNDER"):
        if mail_at(st.session_state.final_email, st.session_state.final_question, st.session_state.final_analysis):
            st.session_state.step = "done"
            st.rerun()
        else:
            st.error("Mail gönderilemedi. Lütfen Secrets ayarlarını kontrol et.")
    st.markdown('</div>', unsafe_allow_html=True)

# ADIM 3: BAŞARI EKRANI
elif st.session_state.step == "done":
    st.balloons()
    st.markdown('<div class="premium-card" style="text-align:center;">', unsafe_allow_html=True)
    st.header("✨ Mektubun Yolda!")
    st.write(f"Minerva'nın fısıltıları **{st.session_state.final_email}** adresine gönderildi.")
    st.info("Spam (Gereksiz) klasörünü kontrol etmeyi unutma fani.")
    if st.button("YENİ BİR KEHANET İÇİN SIFIRLA"):
        st.session_state.step = "form"
        st.session_state.sepet = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
