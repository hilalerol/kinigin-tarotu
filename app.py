import streamlit as st
import google.generativeai as genai
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. AYARLAR ---
st.set_page_config(page_title="Minerva Tarot", page_icon="🔮")

# Kartlar
TAM_DESTE = [f"Kart {i}" for i in range(1, 79)] 

# Tasarım (En basit ve hata vermeyecek hali)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #D4AF37; }
    .premium-card { border: 2px solid #D4AF37; padding: 20px; border-radius: 10px; background-color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "form"
if 'sepet' not in st.session_state: st.session_state.sepet = []

# --- 2. FONKSİYONLAR ---
def mail_gonder(alici, mesaj):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "Minerva'nın Kehaneti"
        msg['From'] = st.secrets["MY_EMAIL"]
        msg['To'] = alici
        msg.attach(MIMEText(mesaj, 'plain'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(st.secrets["MY_EMAIL"], st.secrets["MY_EMAIL_PASSWORD"])
            server.send_message(msg)
        return True
    except: return False

# --- 3. AKIŞ ---
st.title("🔮 THE CYNIC'S TAROT")

if st.session_state.step == "form":
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    email = st.text_input("Mail Adresin")
    soru = st.text_area("Sorun Nedir?")
    
    st.write(f"Seçilen Kart Sayısı: {len(st.session_state.sepet)}/3")
    cols = st.columns(10)
    for i in range(30): # Hata olmaması için kart sayısını test amaçlı azalttım
        with cols[i % 10]:
            if st.button(f"K{i+1}", key=f"k{i}"):
                if i not in st.session_state.sepet and len(st.session_state.sepet) < 3:
                    st.session_state.sepet.append(i)
                    st.rerun()
    
    if len(st.session_state.sepet) == 3 and email and soru:
        if st.button("ANALİZİ HAZIRLA"):
            try:
                genai.configure(api_key=st.secrets["MY_API_KEY"])
                # MODEL SEÇİMİ (En garanti yöntem)
                model = genai.GenerativeModel('gemini-pro') 
                res = model.generate_content(f"Sert bir tarot yorumu yap. Soru: {soru}")
                st.session_state.final_analysis = res.text
                st.session_state.final_email = email
                st.session_state.step = "payment"
                st.rerun()
            except Exception as e:
                st.error(f"Bağlantı Hatası: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "payment":
    st.header("☕ Kahve Zamanı")
    st.write("Analizin hazır. Ödeme için BanaBiKahve linkini kullan.")
    st.write("https://buymeacoffee.com/thesynicstarot")
    if st.button("ÖDEMEYİ YAPTIM"):
        if mail_gonder(st.session_state.final_email, st.session_state.final_analysis):
            st.session_state.step = "done"
            st.rerun()
        else:
            st.error("Mail gönderilemedi, bilgileri kontrol et.")

elif st.session_state.step == "done":
    st.success("Kehanet mailine gönderildi!")
    if st.button("Başa Dön"):
        st.session_state.step = "form"
        st.session_state.sepet = []
        st.rerun()
