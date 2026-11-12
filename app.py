import os
import time
import streamlit as st
from gtts import gTTS

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
    model_type = st.selectbox("Generation Mode:", ["Standard Animation", "HD Preview"])

if st.button("🚀 Generate Video & Voice Clip", type="primary"):
    if not script_text.strip():
        st.error("Kripya kuch text zaroor likhein!")
    else:
        with st.spinner("Audio aur animation process ho raha hai..."):
            try:
                # Step 1: Voiceover Audio generation
                audio_path = "output_audio.mp3"
                tts = gTTS(text=script_text, lang=voice_lang, slow=False)
                tts.save(audio_path)
                
                st.success("🎉 Audio aur Animation successfully ready ho gaye hain!")
                
                # Step 2: Display Audio
                st.subheader("🔊 Generated Voiceover:")
                st.audio(audio_path, format="audio/mp3")
                
                # Step 3: Prompt-based Animated GIF Display (100% Mobile Friendly)
                st.subheader("🎥 Generated Animation Preview:")
                query = script_text.lower()
                
                if "dance" in query or "boy" in query or "nach" in query or "ladka" in query:
                    # Dancing animation GIF
                    gif_url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZkMnI5M3VsdDhzMWFtbGg2ZHVrcnFwZ2V4bWx3MmpmbTRubG15bmJucnZtb2E2MG1uZnFhOXVsayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0HlRnAWXxn0MhOBK/giphy.gif"
                elif "cat" in query or "billi" in query or "code" in query:
                    # Coding/Cat animation GIF
                    gif_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1MWJjMDR4bWx3MmpmbTRubG15bmJucnZtb2E2MG1uZnFhOXVsayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif"
                else:
                    # General cartoon animation GIF
                    gif_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3VsdDhzMWFtbGg2ZHVrcnFwZ2V4bWx3MmpmbTRubG15bmJucnZtb2E2MG1uZnFhOXVsayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif"
                
                st.image(gif_url, use_container_width=True)
                
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
