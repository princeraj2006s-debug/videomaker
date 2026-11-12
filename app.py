import streamlit as st
from gtts import gTTS
import os
import time

st.set_page_config(page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Text-to-Animation & Voice Generator (MVP)")
st.markdown("Yahan aap apna script likh kar audio aur animation clip generate kar sakte hain.")

# User inputs
script_text = st.text_area(
    "Apna Video Script / Prompt yahan daalein:", 
    "Hello bhai! Yeh mera AI-generated video aur voiceover clip hai jo Streamlit par chal raha hai.",
    height=150
)

col1, col2 = st.columns(2)
with col1:
    voice_lang = st.selectbox("Language select karein:", ["hi", "en"])
with col2:
    clip_duration = st.slider("Clip Duration (Seconds):", min_value=5, max_value=60, value=10)

if st.button("🚀 Generate Video & Voice Clip", type="primary"):
    if not script_text.strip():
        st.error("Kripya kuch text zaroor likhein!")
    else:
        with st.spinner("AI script process ho rahi hai... Audio aur Animation ban raha hai..."):
            
            # Step 1: Text-to-Speech Audio Generation (gTTS use kiya hai jo free aur fast hai)
            tts = gTTS(text=script_text, lang=voice_lang, slow=False)
            audio_path = "output_audio.mp3"
            tts.save(audio_path)
            
            # Simulating processing time for animation generation
            time.sleep(2)
            
            st.success("🎉 Aapki clip successfully generate ho gayi hai!")
            
            # Step 2: Output Display
            st.subheader("🔊 Generated Voiceover:")
            st.audio(audio_path, format="audio/mp3")
            
            st.subheader("🎥 Generated Animation Preview:")
            # Yahan aap apni custom animated GIF ya placeholder video dikha sakte hain
            st.info(f"Duration: {clip_duration}s | Is section mein aap Runway, HeyGen ya Pika API ka output video URL bind kar sakte hain.")
            
            # Download button for audio
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="📥 Download Audio Clip",
                    data=file,
                    file_name="ai_voice_clip.mp3",
                    mime="audio/mp3"
                )

# Footer notes
st.markdown("---")
st.caption("Built with Python & Streamlit | Powered by AI APIs")
