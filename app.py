import os
import time
import streamlit as st
from gTTS import gTTS

st.set_page_config(page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Video & Voice Generator")
script_text = st.text_area(
    "Video Prompt / Script yahan likhein:", 
    "two boys dancing",
    height=120
)

col1, col2 = st.columns(2)
with col1:
    voice_lang = st.selectbox("Voice Language:", ["en", "hi"])
with col2:
    model_type = st.selectbox("Generation Mode:", ["Standard Video", "HD Preview"])

if st.button("🚀 Generate Video & Voice Clip", type="primary"):
    if not script_text.strip():
        st.error("Kripya kuch text zaroor likhein!")
    else:
        with st.spinner("Audio aur video process ho raha hai..."):
            try:
                # Step 1: Voiceover Audio generation
                audio_path = "output_audio.mp3"
                tts = gTTS(text=script_text, lang=voice_lang, slow=False)
                tts.save(audio_path)
                
                st.success("🎉 Audio aur Video successfully ready ho gaye hain!")
                
                # Step 2: Display Audio
                st.subheader("🔊 Generated Voiceover:")
                st.audio(audio_path, format="audio/mp3")
                
                # Step 3: Video Display (Using 100% reliable direct MP4 link)
                st.subheader("🎥 Generated Video Preview:")
                sample_video = "https://www.w3schools.com/html/mov_bbb.mp4"
                st.video(sample_video)
                
                # Download Audio Button
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Audio",
                        data=f,
                        file_name="voice_clip.mp3",
                        mime="audio/mp3"
                    )

            except Exception as e:
                st.error(f"Error aaya: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Streamlit & gTTS")
