import os
import time
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip
import streamlit as st

st.set_page_config(
    page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered"
)

st.title("🎬 Real AI Video & Voice Generator")
st.markdown(
    "Yahan apna script likho, aur app aapko actual downloadable MP4 video aur"
    " voiceover bana kar dega!"
)

# User inputs
script_text = st.text_area(
    "Apna Video Script yahan likhein:",
    (
        "Hello bhai! Yeh mera khud ka AI video generator hai jo real MP4 video"
        " file bana raha hai."
    ),
    height=150,
)

col1, col2 = st.columns(2)
with col1:
  voice_lang = st.selectbox("Language select karein:", ["hi", "en"])
with col2:
  bg_color_choice = st.selectbox(
      "Background Theme:", ["Dark Blue", "Charcoal Black"]
  )

if st.button("🚀 Generate Real MP4 Video", type="primary"):
  if not script_text.strip():
    st.error("Kripya kuch text zaroor likhein!")
  else:
    with st.spinner(
        "Audio aur Real MP4 Video render ho raha hai... Kripya 5 second wait"
        " karein..."
    ):
      try:
        # Step 1: Text-to-Speech Audio Generation
        audio_path = "output_audio.mp3"
        tts = gTTS(text=script_text, lang=voice_lang, slow=False)
        tts.save(audio_path)

        # Step 2: Generate Real MP4 Video using MoviePy
        video_path = "output_video.mp4"

        # Load audio to get exact duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Select background color RGB
        bg_color = (
            (20, 24, 33) if bg_color_choice == "Charcoal Black" else (15, 32, 67)
        )

        # Create video background matching audio duration
        bg_clip = ColorClip(
            size=(1280, 720), color=bg_color, duration=duration
        )

        # Combine video and audio
        final_clip = bg_clip.set_audio(audio_clip)

        # Write output video file (Fast rendering)
        final_clip.write_videofile(
            video_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )

        st.success("🎉 Aapka real MP4 video successfully generate ho gaya hai!")

        # Step 3: Display Video Player
        st.subheader("🎥 Generated Video Preview:")
        st.video(video_path)

        # Step 4: Download Button for MP4 Video
        with open(video_path, "rb") as f:
          st.download_button(
              label="📥 Download MP4 Video Clip",
              data=f,
              file_name="ai_video_clip.mp4",
              mime="video/mp4",
          )

      except Exception as e:
        st.error(f"Kuch error aa gaya: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Python, MoviePy & Streamlit")
