import streamlit as st
import google.generativeai as genai
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. AYARLAR VE GOLD-BLACK TASARIM ---
st.set_page_config(page_title="Minerva Tarot Premium", page_icon="🔮", layout="wide")

# Sabit Kart Listesi
BUYUK_ARKANA = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
KUCUK_ARKANA = [f"{n} of {s}" for s in ["Swords", "Cups", "Wands", "Pentacles"] for n in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]]
TAM_DESTE = BUYUK_ARKANA + KUCUK_ARKANA

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    /* Genel Tema */
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #050505 100%); color: #e0e0e0; font-family: 'Special Elite', cursive; }
    
    /* Başlık ve Metinler */
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: #D4AF37; letter-spacing: 5px; text-shadow: 0 0 20px rgba(212, 175, 55, 0.4); margin-bottom: 0px; }
    .gold-text { color: #D4AF37; font-family: 'Cinzel', serif; font-weight: bold; }
    
    /* Kart Şeklinde Kutular */
    .premium-card { background: rgba(15, 15, 15, 0.95); padding: 30px; border: 1px solid #D4AF37; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.8); margin-bottom: 25px; }
    
    /* Özel Butonlar */
    .stButton button { 
        background: linear-gradient(135deg, #111 0%, #222 100%) !important; 
        border: 1px solid #D4AF37 !important; 
        color: #D4AF37 !important; 
        border-radius: 5px !important; 
        height: 60px !important;
        transition: 0.4s;
    }
    .stButton button:hover { box-shadow: 0 0 15px #D4AF37; transform: translateY(-3px); color: white !important; }
    
    /* Kahve Butonu */
    .coffee-btn { 
        display: inline-block; padding: 18px 40px; background: linear-gradient(45deg, #D4AF37, #B8860B); color: black !important; 
        text-decoration: none; font-weight: bold; border-radius: 50px; font-size: 1.2rem; transition: 0.4s; border: none;
    }
    .coffee-btn:hover { transform: scale(1.05); box-shadow: 0 0 25px #D4AF37; }

    /* Animasyon */
    .mystic-prof { text-align: center; font-size: 70px; animation: float 4s infinite ease-in-out; filter: drop-shadow(0 0 10px #D4AF37); }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DURUM YÖNETİMİ ---
if 'step' not in st.session_state: st.session_state.step = "form"
if 'sepet' not in st.session_state: st.session_state.sepet = []

# --- 3. MAİL MOTORU (HTML TASARIMLI) ---
def mail_at(alici, soru, analiz):
    try:
        sender = st.secrets["MY_EMAIL"]
        pwd = st.secrets["MY_EMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['From'] = f"Profesör Minerva <{sender}>"
        msg['To'] = alici
        msg['Subject'] = "Mühürlü Kehanet: Senin Özel Analizin Hazır"
        
        html = f"""
        <div style="background-color: #050505; padding: 40px; font-family: 'Georgia', serif; color: #e0e0e0; border: 2px solid #D4AF37; border-radius: 15px;">
            <h1 style="text-align: center; color: #D4AF37; font-family: 'Cinzel', serif; letter-spacing: 3px;">MINERVA'NIN KEHANETİ</h1>
            <hr style="border: 0.5px solid #D4AF37;">
            <p style="font-size: 16px;"><b>Sorduğun Soru:</b> {soru}</p>
            <div style="background-color: #111; padding: 25px; border-radius: 10px; line-height: 1.8; border-left: 4px solid #D4AF37; font-size: 17px;">
                {analiz.replace(chr(10), '<br>')}
            </div>
            <p style="text-align: right; color: #D4AF37; font-size: 20px; font-style: italic; margin-top: 30px;">— Profesör Minerva</p>
            <p style="text-align: center; color: #444; font-size: 12px; margin-top: 40px;">Bu mesaj Profesör Minerva'nın dijital kütüphanesinden mühürlenerek gönderilmiştir.</p>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pwd)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

# --- 4. AKIŞ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Kadim Bilgelik & Acımasız Gerçekler</p>', unsafe_allow_html=True)

# ADIM 1: DETAYLI FORM VE KART SEÇİMİ
if st.session_state.step == "form":
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="gold-text">1. Ruhunu Tanımla</h3>', unsafe_allow_html=True)
        email = st.text_input("Analizinin gönderileceği mail adresi:")
        soru = st.text_area("Aklını kurcalayan o derin soru nedir?")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            yas = st.number_input("Yaşın", 15, 99, 25)
            konu = st.selectbox("Konu", ["Genel", "Aşk ve İlişkiler", "Para ve Kariyer", "Ruhsal Sağlık"])
        with c2:
            calisma = st.selectbox("İş Durumu", ["Çalışıyorum", "Öğrenci", "İş Arıyorum", "Çalışmıyorum"])
            medeni = st.selectbox("Medeni Hal", ["Bekar", "Evli", "Nişanlı", "Boşanmış", "Karmaşık"])
        with c3:
            iliski = st.selectbox("İlişki Durumu", ["İlişkim var", "İlişkim yok", "Platonik", "Yeni bitti"])
        
        st.write("---")
        st.markdown(f'<h3 class="gold-text">2. Kaderini Seç ({len(st.session_state.sepet)}/3)</h3>', unsafe_allow_html=True)
        
        cols = st.columns(13)
        for i in range(78):
            with cols[i % 13]:
                label = "❂" if i in st.session_state.sepet else "✧"
                if st.button(label, key=f"card_{i}"):
                    if i not in st.session_state.sepet and len(st.session_state.sepet) < 3:
                        st.session_state.sepet.append(i)
                        st.rerun()
                    elif i in st.session_state.sepet:
                        st.session_state.sepet.remove(i)
                        st.rerun()
        
        if len(st.session_state.sepet) == 3 and email and soru:
            if st.button("KEHANETİ HAZIRLA VE MÜHÜRLE", use_container_width=True):
                with st.spinner("Minerva zihnini kartlara odaklıyor..."):
                    try:
                        genai.configure(api_key=st.secrets["MY_API_KEY"])
                        model = genai.GenerativeModel('models/gemini-1.5-flash')
                        
                        secilen_kartlar = []
                        for idx in st.session_state.sepet:
                            yon = " (TERS)" if random.random() < 0.3 else " (DÜZ)"
                            secilen_kartlar.append(TAM_DESTE[idx] + yon)
                        
                        prompt = f"Sen 'The Cynic's Tarot'sun. Sert, alaycı ve dürüst ol. Profil: {yas} yaş, {calisma}, {medeni}, {iliski}. Konu: {konu}. Soru: {soru}. Kartlar: {secilen_kartlar}. Analiz yap ve sonuna '🧪 ACI REÇETE' ekle."
                        res = model.generate_content(prompt)
                        
                        st.session_state.final_analysis = res.text
                        st.session_state.final_email = email
                        st.session_state.final_question = soru
                        st.session_state.step = "payment"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Kozmik bir kesinti oluştu. Lütfen tekrar dene.")
        st.markdown('</div>', unsafe_allow_html=True)

# ADIM 2: BANABİKAHVE ÖDEME EKRANI
elif st.session_state.step == "payment":
    st.markdown('<div class="premium-card" style="text-align:center;">', unsafe_allow_html=True)
    st.header("⏳ Kehanet Mühürlendi")
    st.write("Minerva senin için analizi hazırladı. Mektubun mail kutuna uçmak üzere bekliyor.")
    st.markdown('<p class="gold-text">Minerva\'nın emeği için ona küçük bir kahve ısmarlayarak süreci tamamlayabilirsin.</p>', unsafe_allow_html=True)
    
    # Kendi BanaBiKahve linkini buraya yapıştır
    banabikahve_url = "https://buymeacoffee.com/thesynicstarot" 
    st.markdown(f'<a href="{banabikahve_url}" target="_blank" class="coffee-btn">☕ KAHVE ISMARLA (50 TL)</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.info("💡 Kahveyi ısmarladıktan sonra aşağıdaki mühre basarak analizi mailine ışınla.")
    if st.button("KAHVEYİ ISMARLADIM, KEHANETİ GÖNDER"):
        with st.spinner("Mektup mühürleniyor ve gönderiliyor..."):
            if mail_at(st.session_state.final_email, st.session_state.final_question, st.session_state.final_analysis):
                st.session_state.step = "done"
                st.rerun()
            else:
                st.error("Mail gönderiminde bir sorun oluştu. Lütfen sistem ayarlarını (Secrets) kontrol et.")
    st.markdown('</div>', unsafe_allow_html=True)

# ADIM 3: BAŞARI EKRANI
elif st.session_state.step == "done":
    st.balloons()
    st.markdown('<div class="premium-card" style="text-align:center;">', unsafe_allow_html=True)
    st.header("✨ Mektubun Gönderildi!")
    st.write(f"Kader fısıltıları **{st.session_state.final_email}** adresine doğru yola çıktı.")
    st.write("Spam (Gereksiz) klasörünü kontrol etmeyi unutma fani.")
    if st.button("YENİ BİR KEHANET İÇİN SIFIRLA"):
        st.session_state.step = "form"
        st.session_state.sepet = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
