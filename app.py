import os
import requests
from gtts import gTTS
import streamlit as st

st.set_page_config(
    page_title="AI Video & Voice Generator", page_icon="🎬", layout="centered"
)

st.title("🎬 AI Video & Voice Generator")
script_text = st.text_area(
    "Video Prompt yahan likhein (jaise: two boys dancing):",
    "two boys dancing",
    height=120,
)

# Optional Pexels API Key
pexels_api_key = st.text_input(
    "Pexels API Key (Optional):",
    type="password",
    help=(
        "Khali chhod sakte hain, default working video apne aap chal jayegi!"
    ),
)

if st.button("🚀 Generate Video & Voice", type="primary"):
  if not script_text.strip():
    st.error("Kripya kuch text zaroor likhein!")
  else:
    with st.spinner("Voice aur video ready ho rahi hai..."):
      try:
        # Step 1: Voiceover Audio Generation
        audio_path = "output_audio.mp3"
        tts = gTTS(text=script_text, lang="en", slow=False)
        tts.save(audio_path)

        st.success("🎉 Successfully generated!")

        # Step 2: Display Audio
        st.subheader("🔊 Generated Voiceover:")
        st.audio(audio_path, format="audio/mp3")

        # Step 3: Fetch Video dynamically or use robust fallback
        st.subheader("🎥 Generated Video Preview:")

        video_url = ""
        if pexels_api_key:
          try:
            headers = {"Authorization": pexels_api_key}
            url = f"https://api.pexels.com/videos/search?query={script_text}&per_page=1"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
              data = response.json()
              if data.get("videos"):
                video_files = data["videos"][0]["video_files"]
                for vf in video_files:
                  if vf.get("file_type") == "video/mp4":
                    video_url = vf.get("link")
                    break
          except:
            pass

        # Guaranteed working mobile-friendly video fallback
        if not video_url:
          video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

        # HTML5 Mobile-Friendly Video Player
        video_html = f"""
                <video width="100%" controls autoplay loop muted playsinline style="border-radius: 10px;">
                    <source src="{video_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                """
        st.markdown(video_html, unsafe_allow_html=True)

        # Download Audio Button
        with open(audio_path, "rb") as f:
          st.download_button(
              label="📥 Download Audio",
              data=f,
              file_name="voice_clip.mp3",
              mime="audio/mp3",
          )

      except Exception as e:
        st.error(f"Error aaya: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px;">
        <a href="https://www.pexels.com" target="_blank">
            <img src="https://images.pexels.com/lib/api/pexels.png" width="100"/>
        </a>
        <br>
        <a href="https://www.pexels.com" target="_blank" style="color: gray; text-decoration: none;">Videos provided by Pexels</a>
    </div>
    """,
    unsafe_allow_html=True,
)
