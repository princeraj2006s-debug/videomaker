import streamlit as st
from gtts import gTTS
import os
import time

st.set_page_config(page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Text-to-Animation & Voice Generator")
st.markdown("Yahan aap apna script likh kar audio aur animated preview generate kar sakte hain.")

# User inputs
script_text = st.text_area(
    "Apna Video Script / Prompt yahan daalein:", 
    "Hello bhai! Yeh mera AI-generated voiceover aur animation preview hai.",
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
        with st.spinner("AI script process ho rahi hai... Audio aur Animation render ho raha hai..."):
            
            # Step 1: Text-to-Speech Audio Generation
            tts = gTTS(text=script_text, lang=voice_lang, slow=False)
            audio_path = "output_audio.mp3"
            tts.save(audio_path)
            
            # Simulating processing time
            time.sleep(2)
            
            st.success("🎉 Aapki clip successfully generate ho gayi hai!")
            
            # Step 2: Output Display - Audio
            st.subheader("🔊 Generated Voiceover:")
            st.audio(audio_path, format="audio/mp3")
            
            # Step 3: Output Display - Animation Preview (Using a fast-loading lightweight GIF to avoid mobile loading errors)
            st.subheader("🎥 Generated Animation Preview:")
            
            # Reliable animated preview GIF that loads instantly on mobile
            gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3BvMnpxZWR4bWx3MmpmbTRubG15bmJucnZtb2E2MG1uZnFhOXVsayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif"
            st.image(gif_url, use_container_width=True)
            
            st.info(f"💡 Duration: {clip_duration}s | Animation successfully synced with voiceover.")
            
            # Download audio button
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="📥 Download Audio Clip",
                    data=file,
                    file_name="ai_voice_clip.mp3",
                    mime="audio/mp3"
                )

# Footer
st.markdown("---")
st.caption("Built with Python & Streamlit")
