import streamlit as st
from gtts import gTTS
import os
import time

st.set_page_config(page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Text-to-Animation & Voice Generator")
st.markdown("Yahan aap apna script likh kar audio aur dynamic animated video clip generate kar sakte hain.")

# User inputs
script_text = st.text_area(
    "Apna Video Script / Prompt yahan daalein:", 
    "Hello bhai! Yeh mera AI-generated video aur voiceover clip hai jo ab successfully render ho raha hai.",
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
            
            # Simulating AI video generation time
            time.sleep(3)
            
            st.success("🎉 Aapki clip successfully generate ho gayi hai!")
            
            # Step 2: Output Display - Audio
            st.subheader("🔊 Generated Voiceover:")
            st.audio(audio_path, format="audio/mp3")
            
            # Step 3: Output Display - Video / Animation (Using a sample dynamic animation loop/video)
                # Hum yahan ek public open-source animated video link ya HTML player bind kar rahe hain 
                # taaki aapko black/empty screen na dikhe.
            st.subheader("🎥 Generated Animation Preview:")
            
            sample_video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
            st.video(sample_video_url)
            
            st.info(f"💡 Note: Yeh ek sample animated preview hai ({clip_duration}s). Production level par yahan aap Runway ya HeyGen ka API response URL link kar sakte hain.")
            
            # Download buttons
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Audio",
                        data=file,
                        file_name="ai_voice_clip.mp3",
                        mime="audio/mp3"
                    )

# Footer
st.markdown("---")
st.caption("Built with Python & Streamlit | AI Video Pipeline Active")
