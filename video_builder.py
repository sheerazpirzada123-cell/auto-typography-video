import os
import random
import requests
import numpy as np
from PIL import Image, ImageDraw
from scipy.io import wavfile
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.all import audio_loop

def create_pop_sound(filename="pop.wav"):
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.04
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(1200, 300, len(t))
        waveform = np.sin(2 * np.pi * freq * t) * np.exp(-t * 80)
        audio_data = (waveform * 32767).astype(np.int16)
        wavfile.write(filename, sample_rate, audio_data)

def fetch_bg_music():
    if not os.path.exists("bg_music.mp3"):
        print("Downloading Continuous Background Track...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

def create_fallback_image(filename, category):
    img = Image.new('RGB', (500, 500), color=(30, 30, 40))
    d = ImageDraw.Draw(img)
    color = (220, 50, 50) if category == "MARVEL" else (240, 160, 40)
    d.rectangle([50, 50, 450, 450], outline=color, width=10)
    img.save(filename)

def fetch_hd_images(category):
    images = []
    urls = {
        "MARVEL": [
            "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f9b8.png",
            "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/26a1.png"
        ],
        "ANIME": [
            "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f30f.png",
            "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f525.png"
        ]
    }
    selected_urls = urls.get(category, urls["MARVEL"])
    for idx, url in enumerate(selected_urls):
        filename = f"hd_asset_{idx}.png"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(r.content)
                images.append(filename)
            else:
                create_fallback_image(filename, category)
                images.append(filename)
        except Exception:
            create_fallback_image(filename, category)
            images.append(filename)
            
    return images

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    fetch_bg_music()
    create_pop_sound("pop.wav")

    category = "MARVEL"
    if os.path.exists("category.txt"):
        with open("category.txt", "r", encoding="utf-8") as f:
            category = f.read().strip()

    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    # CONTINUOUS BACKGROUND MUSIC FIX (Loops seamlessly for entire duration)
    raw_bg = AudioFileClip("bg_music.mp3")
    bg_music = audio_loop(raw_bg, duration=duration).volumex(0.12)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [(240, 243, 246), (245, 235, 238), (236, 233, 245)]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    # Pop Animation for Images
    hd_images = fetch_hd_images(category)
    if len(hd_images) >= 1 and os.path.exists(hd_images[0]):
        img1 = (
            ImageClip(hd_images[0])
            .set_start(1.5)
            .set_duration(min(5.0, duration - 1.5))
            .resize(width=380)
            .crossfadein(0.3)
            .set_position(('center', 380))
        )
        video_clips.append(img1)

    if len(hd_images) >= 2 and os.path.exists(hd_images[1]) and duration > 8:
        img2 = (
            ImageClip(hd_images[1])
            .set_start(7.5)
            .set_duration(min(5.0, duration - 7.5))
            .resize(width=380)
            .crossfadein(0.3)
            .set_position(('center', 380))
        )
        video_clips.append(img2)

    print("Transcribing audio with Whisper...")
    script_words = []
    if os.path.exists("script.txt"):
        with open("script.txt", "r", encoding="utf-8") as f:
            script_words = f.read().strip().split()

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True, language="hi", task="transcribe")

    pop_audio = AudioFileClip("pop.wav").volumex(0.22)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']
    font_sizes = [95, 115, 130]

    word_idx = 0
    for segment in segments:
        for word_item in segment.words:
            start = max(0, word_item.start)
            end = min(duration, word_item.end)

            if script_words and word_idx < len(script_words):
                txt = script_words[word_idx].upper()
                word_idx += 1
            else:
                txt = word_item.word.strip().upper()

            if end > start and txt:
                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=random.choice(font_sizes),
                        color=random.choice(color_palette),
                        font='DejaVu-Sans-Bold',
                        method='caption',
                        size=(950, None)
                    )
                    .set_position(('center', 1050))
                    .set_start(start)
                    .set_end(end)
                )
                video_clips.append(txt_clip)

                if word_idx % 2 == 0 and (start + pop_audio.duration <= duration):
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Rendering video with Bunty Voice & Continuous Music...")
    final_video = CompositeVideoClip(video_clips).set_audio(full_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("Video rendered successfully!")

if __name__ == "__main__":
    create_video()
