import streamlit as st
import google.generativeai as genai
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. AYARLAR VE TASARIM ---
st.set_page_config(page_title="Minerva Tarot Premium", page_icon="🔮", layout="centered")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: #e0e0e0; font-family: 'Special Elite', cursive; }
    .main-title { font-family: 'Cinzel', serif; text-align: center; color: white; letter-spacing: 8px; text-shadow: 0 0 15px #ff4b4b; }
    .premium-card {
        background: rgba(10, 10, 10, 0.9);
        padding: 40px;
        border: 2px solid #ff4b4b;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);
    }
    .payment-link {
        background: linear-gradient(45deg, #ff4b4b, #800000);
        color: white !important;
        padding: 18px 40px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 50px;
        display: inline-block;
        margin-top: 25px;
        font-size: 1.2rem;
        transition: 0.4s;
        border: none;
    }
    .payment-link:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(255, 75, 75, 0.5); }
    .mystic-prof { text-align: center; font-size: 70px; animation: float 4s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MINERVA'NIN ÖZEL MAİL MOTORU ---
def send_mystic_mail(to_email, user_question, ai_analysis):
    sender_email = st.secrets["MY_EMAIL"]
    sender_password = st.secrets["MY_EMAIL_PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = f"Profesör Minerva <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = "Kaderin Mühürlendi: Özel Analizin Hazır"

    # HTML Mail Tasarımı (Eski bir mektup havası)
    html_content = f"""
    <html>
    <body style="background-color: #000; color: #ddd; font-family: serif; padding: 20px;">
        <div style="border: 2px solid #ff4b4b; padding: 30px; border-radius: 15px; background-color: #0a0a0a;">
            <h1 style="color: #ff4b4b; text-align: center; font-family: 'Cinzel', serif;">MINERVA'NIN KEHANETİ</h1>
            <p style="font-style: italic; color: #888; text-align: center;">"Gerçekler bazen acıtır fani, ama seni özgür kılar."</p>
            <hr style="border: 0.5px solid #333;">
            <p><strong>Senin Sorun:</strong> {user_question}</p>
            <div style="line-height: 1.8; font-size: 1.1rem; color: #eee; background: #111; padding: 20px; border-radius: 10px;">
                {ai_analysis.replace('\n', '<br>')}
            </div>
            <br>
            <p style="text-align: right; font-weight: bold; color: #ff4b4b;">— Profesör Minerva</p>
            <p style="font-size: 0.8rem; color: #444; text-align: center;">Bu analiz Profesör Minerva'nın dijital kütüphanesinde mühürlenmiştir.</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except:
        return False

# --- 3. ANA AKIŞ ---
st.markdown('<div class="mystic-prof">🧙‍♀️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE CYNIC\'S TAROT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Özel Seans ve Derin Analiz Ofisi</p>', unsafe_allow_html=True)

# Oturum Durumları
if 'order_status' not in st.session_state: st.session_state.order_status = "idle"

# ADIM 1: Veri Toplama
if st.session_state.order_status == "idle":
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        user_email = st.text_input("Analizin hangi adrese gönderilsin?", placeholder="fani@mail.com")
        user_question = st.text_area("Ruhunu sıkan o soru nedir?", placeholder="Tüm detayları yaz...")
        yas = st.number_input("Yaşın", 15, 99, 25)
        
        if st.button("KEHANETİ BAŞLAT"):
            if "@" not in user_email or len(user_question) < 10:
                st.error("Lütfen geçerli bir mail ve soru gir.")
            else:
                # Arka planda analizi hazırla ama henüz gönderme
                try:
                    genai.configure(api_key=st.secrets["MY_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Sert ol. {yas} yaşında biri şunu sordu: {user_question}. Analiz et ve ACI REÇETE ekle."
                    response = model.generate_content(prompt)
                    st.session_state.temp_analysis = response.text
                    st.session_state.temp_email = user_email
                    st.session_state.temp_question = user_question
                    st.session_state.order_status = "waiting_payment"
                    st.rerun()
                except:
                    st.error("Kozmik hatlar şu an meşgul, lütfen 1 dakika sonra tekrar dene.")
        st.markdown('</div>', unsafe_allow_html=True)

# ADIM 2: Ödeme Yönlendirme
elif st.session_state.order_status == "waiting_payment":
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.success("✅ Analizin Hazırlandı ve Mühürlendi!")
    st.write("Analizinin mail kutuna düşmesi için son bir adım kaldı.")
    st.write("Profesör Minerva'nın emeği için sembolik bedeli öde.")
    
    shopier_url = "https://www.shopier.com/SizinDukkanLinkiniz" # BURAYI GÜNCELLE
    st.markdown(f'<a href="{shopier_url}" target="_blank" class="payment-link">💳 50 TL ÖDE VE ANALİZİ AL</a>', unsafe_allow_html=True)
    
    st.info("💡 Ödeme sonrası butona basarak analizi anında mailine uçurabilirsin.")
    if st.button("ÖDEMEYİ YAPTIM, MAİLİMİ GÖNDER"):
        if send_mystic_mail(st.session_state.temp_email, st.session_state.temp_question, st.session_state.temp_analysis):
            st.session_state.order_status = "completed"
            st.rerun()
        else:
            st.error("Mail gönderilirken bir sorun oldu. Lütfen tekrar dene.")
    st.markdown('</div>', unsafe_allow_html=True)

# ADIM 3: Tamamlandı
elif st.session_state.order_status == "completed":
    st.balloons()
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("✨ Mektubun Yolda!")
    st.write(f"Analizin **{st.session_state.temp_email}** adresine gönderildi.")
    st.write("Spam (Gereksiz) klasörünü kontrol etmeyi unutma.")
    if st.button("YENİ KEHANET İÇİN BAŞA DÖN"):
        st.session_state.order_status = "idle"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
