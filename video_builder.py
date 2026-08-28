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
    """Fetches 2 distinct HD images based on topic category."""
    images = []
    keywords = ["superhero", "avengers", "ironman"] if category == "MARVEL" else ["goku", "anime", "dragonball"]
    
    for i in range(2):
        filename = f"hd_asset_{i}.jpg"
        kw = random.choice(keywords)
        try:
            print(f"Fetching HD Image #{i+1} for: {kw}")
            url = f"https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80" if category == "MARVEL" else f"https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&q=80"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(r.content)
                images.append(filename)
        except Exception as e:
            print(f"Image Download Exception: {e}")
            
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

    bg_music = AudioFileClip("bg_music.mp3").volumex(0.12)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [(240, 243, 246), (245, 235, 238), (236, 233, 245)]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    # Overlay 2 Multiple HD Images throughout video timeline
    hd_images = fetch_hd_images(category)
    if len(hd_images) >= 1 and os.path.exists(hd_images[0]):
        img1 = (
            ImageClip(hd_images[0])
            .set_start(1.5)
            .set_duration(min(7.0, duration - 1.5))
            .resize(width=450)
            .set_position(('center', 320))
        )
        video_clips.append(img1)

    if len(hd_images) >= 2 and os.path.exists(hd_images[1]) and duration > 10:
        img2 = (
            ImageClip(hd_images[1])
            .set_start(9.0)
            .set_duration(min(7.0, duration - 9.0))
            .resize(width=450)
            .set_position(('center', 320))
        )
        video_clips.append(img2)

    print("Transcribing audio with Whisper for exact text sync...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    pop_audio = AudioFileClip("pop.wav").volumex(0.15)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']
    font_sizes = [95, 115, 130]

    word_count = 0
    for segment in segments:
        for word_item in segment.words:
            start = word_item.start
            end = word_item.end
            txt = word_item.word.strip().upper()

            if end > start and txt:
                word_count += 1
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

                if word_count % 2 == 0 and (start + pop_audio.duration <= duration):
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Rendering final updated video...")
    final_video = CompositeVideoClip(video_clips).set_audio(full_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 successfully created!")

if __name__ == "__main__":
    create_video()
