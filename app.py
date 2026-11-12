import os
import math
import tempfile
import streamlit as st
import numpy as np

from PIL import Image, ImageDraw
from gtts import gTTS
from moviepy.editor import (
    ImageSequenceClip,
    AudioFileClip
)

st.set_page_config(
    page_title="2D AI Cartoon Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 2D Cartoon Studio")
st.write("Create animated cartoon videos with your own voiceover!")

# -------------------------------
# USER INPUT
# -------------------------------

story = st.text_area(
    "✍️ Write your cartoon story",
    "A little boy walks into a beautiful forest. "
    "He meets a friendly elephant. They become friends.",
    height=150
)

voice_text = st.text_area(
    "🎙️ Voiceover Script",
    "Hello! Today I am going on an adventure. "
    "Look! There is a friendly elephant!",
    height=100
)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Voice Language",
        ["en", "hi"]
    )

with col2:
    duration = st.slider(
        "Video Duration (seconds)",
        5, 20, 10
    )

# -------------------------------
# CARTOON DRAWING
# -------------------------------

def draw_scene(frame, scene, t):

    width, height = 640, 360

    img = Image.new(
        "RGB",
        (width, height),
        (135, 206, 235)
    )

    draw = ImageDraw.Draw(img)

    # Sun

    draw.ellipse(
        (510, 30, 570, 90),
        fill="yellow"
    )

    # Ground

    draw.rectangle(
        (0, 270, 640, 360),
        fill=(70, 180, 90)
    )

    # Trees

    for x in [60, 560]:
        draw.rectangle(
            (x+20, 190, x+40, 280),
            fill=(110, 65, 30)
        )

        draw.ellipse(
            (x, 120, x+80, 220),
            fill=(30, 130, 55)
        )

    # Animated boy

    boy_x = int(180 + math.sin(t * 3) * 35)
    boy_y = int(205 + abs(math.sin(t * 6)) * 5)

    # Legs

    draw.line(
        (boy_x+25, boy_y+85, boy_x+10, boy_y+125),
        fill="black",
        width=8
    )

    draw.line(
        (boy_x+35, boy_y+85, boy_x+55, boy_y+125),
        fill="black",
        width=8
    )

    # Body

    draw.rounded_rectangle(
        (boy_x, boy_y+35, boy_x+60, boy_y+95),
        radius=12,
        fill=(30, 90, 230)
    )

    # Head

    draw.ellipse(
        (boy_x+5, boy_y-15, boy_x+55, boy_y+40),
        fill=(255, 205, 160),
        outline="black",
        width=2
    )

    # Eyes

    draw.ellipse(
        (boy_x+17, boy_y+5, boy_x+23, boy_y+12),
        fill="black"
    )

    draw.ellipse(
        (boy_x+38, boy_y+5, boy_x+44, boy_y+12),
        fill="black"
    )

    # Elephant

    elephant_x = int(400 + math.sin(t * 2) * 12)

    draw.ellipse(
        (elephant_x, 190, elephant_x+120, 275),
        fill=(150, 150, 165),
        outline="black",
        width=2
    )

    draw.ellipse(
        (elephant_x+10, 160, elephant_x+65, 225),
        fill=(170, 170, 185),
        outline="black"
    )

    draw.ellipse(
        (elephant_x+78, 205, elephant_x+90, 217),
        fill="black"
    )

    # Moving trunk

    draw.arc(
        (elephant_x+65, 220, elephant_x+125, 285),
        start=0,
        end=180,
        fill=(100, 100, 120),
        width=12
    )

    # Character caption

    draw.text(
        (20, 20),
        scene,
        fill="black"
    )

    return np.array(img)


# -------------------------------
# VIDEO GENERATION
# -------------------------------

if st.button(
    "🚀 Generate Cartoon Video",
    type="primary"
):

    if not story.strip():
        st.error("Please write your story.")

    elif not voice_text.strip():
        st.error("Please enter voiceover text.")

    else:

        try:

            with tempfile.TemporaryDirectory() as temp:

                # VOICE GENERATION

                st.info("🎙️ Creating voiceover...")

                audio_path = os.path.join(
                    temp,
                    "voice.mp3"
                )

                tts = gTTS(
                    text=voice_text,
                    lang=language
                )

                tts.save(audio_path)

                audio = AudioFileClip(audio_path)

                # SCENE GENERATION

                st.info("🎨 Creating 2D animation...")

                fps = 15

                video_duration = duration

                total_frames = fps * video_duration

                frames = []

                for i in range(total_frames):

                    t = i / fps

                    scene_number = min(
                        3,
                        int(t / (video_duration / 4)) + 1
                    )

                    scene_labels = [
                        "A Beautiful Cartoon World",
                        "The Boy Goes On An Adventure",
                        "Meeting A Friendly Elephant",
                        "A New Friendship Begins"
                    ]

                    frame = draw_scene(
                        i,
                        scene_labels[scene_number-1],
                        t
                    )

                    frames.append(frame)

                # CREATE MP4

                clip = ImageSequenceClip(
                    frames,
                    fps=fps
                )

                # Match video to voice duration

                final_duration = max(
                    video_duration,
                    audio.duration
                )

                clip = clip.set_duration(
                    final_duration
                )

                clip = clip.set_audio(audio)

                output_path = os.path.join(
                    temp,
                    "cartoon_video.mp4"
                )

                clip.write_videofile(
                    output_path,
                    fps=fps,
                    codec="libx264",
                    audio_codec="aac",
                    logger=None
                )

                clip.close()
                audio.close()

                # SHOW VIDEO

                st.success("🎉 Cartoon video generated!")

                st.video(output_path)

                with open(output_path, "rb") as file:

                    st.download_button(
                        "📥 Download MP4 Video",
                        data=file.read(),
                        file_name="cartoon_video.mp4",
                        mime="video/mp4"
                    )

        except Exception as e:

            st.error(f"Generation Error: {e}")

st.markdown("---")

st.caption(
    "2D Cartoon Studio | Python + Streamlit + Pillow + MoviePy"
)
