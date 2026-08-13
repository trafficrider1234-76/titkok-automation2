import os
import requests
from groq import Groq

# Naya MoviePy import tarika (Error fix karne ke liye)
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import TextClip

# Direct API keys
GROQ_KEY = os.environ.get("GROQ_API_KEY")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
TIKTOK_KEY = os.environ.get("TIKTOK_CLIENT_KEY")
TIKTOK_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")

print("1. Groq se keyword generate ho raha hai...")
groq_client = Groq(api_key=GROQ_KEY)
chat_completion = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "system",
            "content": "Provide only ONE simple English search keyword for Pexels stock videos related to classic car restoration, garage work, or metal polishing. Reply with just the keyword, nothing else."
        },
        {
            "role": "user",
            "content": "Give me a search keyword."
        }
    ]
)
search_keyword = chat_completion.choices[0].message.content.strip()
print(f"Keyword mila: {search_keyword}")

print("2. Pexels se video download ki ja rahi hai...")
pexels_url = f"https://api.pexels.com/videos/search?query={search_keyword}&per_page=1"
headers = {"Authorization": PEXELS_KEY}
response = requests.get(pexels_url, headers=headers)
data = response.json()

if "videos" in data and len(data["videos"]) > 0:
    download_url = data["videos"][0]["video_files"][0]["link"]
    video_response = requests.get(download_url)
    with open("background_video.mp4", "wb") as f:
        f.write(video_response.content)
    print("Video successfully download ho gayi.")
else:
    raise Exception("Pexels par video nahi mili.")

print("3. MoviePy se text overlay render ho raha hai...")
background = VideoFileClip("background_video.mp4").subclip(0, 10)
txt_clip = TextClip(f"Restoring {search_keyword}", fontsize=45, color='white', size=background.size, method='caption')
txt_clip = txt_clip.set_duration(10)
video = CompositeVideoClip([background, txt_clip])
video.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")
print("Video render hokar 'output.mp4' ban gayi.")

print("Automation process completed successfully.")
