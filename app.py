import os
import math
import requests
import streamlit as st
import replicate

from gtts import gTTS
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips
)

st.set_page_config(
    page_title="AI Cartoon Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Cartoon Video Generator")

st.write("Turn your imagination into animated videos!")

# USER INPUT

video_prompt = st.text_area(
    "Describe your cartoon video:",
    "Two cute cartoon boys dancing together in a colorful park, 3D animation style."
)

voice_text = st.text_area(
    "What should the characters say?",
    "Hello everyone! Welcome to our cartoon world!"
)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Voice Language",
        ["en", "hi"]
    )

with col2:
    duration = st.selectbox(
        "Video Duration",
        [5, 10, 15]
    )

if st.button("🚀 Generate AI Video"):

    if not video_prompt.strip():
        st.error("Please enter a video prompt.")

    else:

        try:

            with st.spinner("🎨 Generating AI cartoon video..."):

                # STEP 1: GENERATE VIDEO

                token = st.secrets["REPLICATE_API_TOKEN"]

                client = replicate.Client(
                    api_token=token
                )

                output = client.run(
                    "alibaba/wan-3",
                    input={
                        "prompt": (
                            "High quality 3D cartoon animation. "
                            + video_prompt
                        ),
                        "duration": duration,
                        "resolution": "480p",
                        "aspect_ratio": "16:9"
                    }
                )

                # GET VIDEO URL

                if isinstance(output, list):
                    video_url = str(output[0])
                elif hasattr(output, "url"):
                    video_url = output.url()
                else:
                    video_url = str(output)

                # DOWNLOAD VIDEO

                response = requests.get(
                    video_url,
                    timeout=180
                )

                response.raise_for_status()

                with open("generated_video.mp4", "wb") as f:
                    f.write(response.content)

            st.success("AI Video Generated!")

            with st.spinner("🎙️ Generating voiceover..."):

                # STEP 2: GENERATE VOICE

                tts = gTTS(
                    text=voice_text,
                    lang=language
                )

                tts.save("voice.mp3")

            with st.spinner("🎬 Combining video and voice..."):

                # STEP 3: COMBINE VIDEO + AUDIO

                video = VideoFileClip(
                    "generated_video.mp4"
                )

                audio = AudioFileClip("voice.mp3")

                # Repeat video if voice is longer

                if audio.duration > video.duration:

                    count = math.ceil(
                        audio.duration / video.duration
                    )

                    video = concatenate_videoclips(
                        [video] * count
                    )

                video = video.subclip(
                    0,
                    min(video.duration, audio.duration)
                )

                final_video = video.set_audio(
                    audio.subclip(0, video.duration)
                )

                final_video.write_videofile(
                    "final_video.mp4",
                    codec="libx264",
                    audio_codec="aac"
                )

                video.close()
                audio.close()
                final_video.close()

            # STEP 4: DISPLAY VIDEO

            st.success("🎉 Your cartoon video is ready!")

            st.subheader("🎥 Generated Video")

            st.video("final_video.mp4")

            # STEP 5: DOWNLOAD

            with open("final_video.mp4", "rb") as f:

                st.download_button(
                    "📥 Download Cartoon Video",
                    data=f,
                    file_name="my_cartoon_video.mp4",
                    mime="video/mp4"
                )

        except Exception as e:

            st.error(f"Generation Error: {str(e)}")

st.markdown("---")

st.caption("Powered by Streamlit, Wan AI & gTTS")
