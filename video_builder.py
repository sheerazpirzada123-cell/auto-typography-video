import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip, ImageClip

def create_pop_sound(filename="pop.wav"):
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.03
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(1000, 250, len(t))
        waveform = np.sin(2 * np.pi * freq * t) * np.exp(-t * 100)
        audio_data = (waveform * 32767).astype(np.int16)
        wavfile.write(filename, sample_rate, audio_data)

def fetch_bg_music():
    if not os.path.exists("bg_music.mp3"):
        print("Downloading Background Music...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

def fetch_hd_images(category):
    images = []
    urls = {
        "MARVEL": [
            "https://upload.wikimedia.org/wikipedia/commons/0/04/Iron_Man_cosplay.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/a/a2/Thor_Cosplay.jpg"
        ],
        "ANIME": [
            "https://upload.wikimedia.org/wikipedia/commons/3/36/Goku_cosplay.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/e/e0/Anime_convention.jpg"
        ]
    }
    selected_urls = urls.get(category, urls["MARVEL"])
    for idx, url in enumerate(selected_urls):
        filename = f"hd_asset_{idx}.jpg"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(r.content)
                images.append(filename)
        except Exception as e:
            print(f"Download Error: {e}")
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

    bg_music = AudioFileClip("bg_music.mp3").volumex(0.10)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [(240, 243, 246), (245, 235, 238), (236, 233, 245)]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    # Dynamic Images at strategic timelines
    hd_images = fetch_hd_images(category)
    if len(hd_images) >= 1 and os.path.exists(hd_images[0]):
        img1 = (
            ImageClip(hd_images[0])
            .set_start(2.5)
            .set_duration(min(6.0, duration - 2.5))
            .resize(width=480)
            .set_position(('center', 320))
        )
        video_clips.append(img1)

    if len(hd_images) >= 2 and os.path.exists(hd_images[1]) and duration > 10:
        img2 = (
            ImageClip(hd_images[1])
            .set_start(10.0)
            .set_duration(min(6.0, duration - 10.0))
            .resize(width=480)
            .set_position(('center', 320))
        )
        video_clips.append(img2)

    print("Transcribing audio with Whisper (No Translation Fix)...")
    script_words = []
    if os.path.exists("script.txt"):
        with open("script.txt", "r", encoding="utf-8") as f:
            script_words = f.read().strip().split()

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True, language="hi", task="transcribe")

    pop_audio = AudioFileClip("pop.wav").volumex(0.18)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']
    font_sizes = [95, 115, 130]

    word_idx = 0
    for segment in segments:
        for word_item in segment.words:
            start = word_item.start
            end = word_item.end

            # Map exact Hinglish script word to eliminate English translation output
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
                    .set_position(('center', 1100))
                    .set_start(start)
                    .set_end(end)
                )
                video_clips.append(txt_clip)

                if word_idx % 2 == 0 and (start + pop_audio.duration <= duration):
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Rendering final video...")
    final_video = CompositeVideoClip(video_clips).set_audio(full_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 created successfully!")

if __name__ == "__main__":
    create_video()
