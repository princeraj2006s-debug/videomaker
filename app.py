import streamlit as st
from gtts import gTTS
from streamlit_lottie import st_lottie
import requests
import time

st.set_page_config(page_title="2D Cartoon AI Generator", page_icon="🎨", layout="centered")

# Lottie animation fetch karne ke liye function
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Kuch cool 2D cartoon / coding animations ke Lottie URLs
lottie_cartoon = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")
lottie_ai_bot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1qulft.json")

st.title("🎨 2D Cartoon & Voice Generator")
st.markdown("Yahan apna script likho aur 2D cartoon animation + voiceover turant banao!")

# User inputs
script_text = st.text_area(
    "Apna Cartoon Script / Dialog yahan likhein:", 
    "Hello bhai! Dekho yeh mera khud ka 2D cartoon animation aur voiceover app ban gaya hai!",
    height=150
)

col1, col2 = st.columns(2)
with col1:
    voice_lang = st.selectbox("Language select karein:", ["hi", "en"])
with col2:
    anim_style = st.selectbox("2D Animation Style:", ["Coding Cat / Dev", "AI Bot Talking"])

if st.button("🚀 Generate 2D Cartoon & Voice", type="primary"):
    if not script_text.strip():
        st.error("Kripya kuch text zaroor likhein!")
    else:
        with st.spinner("2D Cartoon render ho raha hai aur Voice ban rahi hai..."):
            
            # Step 1: Text-to-Speech Audio Generation
            tts = gTTS(text=script_text, lang=voice_lang, slow=False)
            audio_path = "cartoon_audio.mp3"
            tts.save(audio_path)
            
            time.sleep(1)
            st.success("🎉 Aapka 2D Cartoon aur Voice clip ready hai!")
            
            # Step 2: 2D Cartoon Animation Display
            st.subheader("🎬 2D Cartoon Animation Preview:")
            if anim_style == "Coding Cat / Dev":
                if lottie_cartoon:
                    st_lottie(lottie_cartoon, height=250, key="cat")
            else:
                if lottie_ai_bot:
                    st_lottie(lottie_ai_bot, height=250, key="bot")
            
            # Step 3: Voiceover Audio Player
            st.subheader("🔊 Cartoon Voiceover:")
            st.audio(audio_path, format="audio/mp3")
            
            # Download Button
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="📥 Download Voice Audio",
                    data=file,
                    file_name="cartoon_voice.mp3",
                    mime="audio/mp3"
                )

# Footer
st.markdown("---")
st.caption("Powered by Streamlit & Lottie 2D Animations")
