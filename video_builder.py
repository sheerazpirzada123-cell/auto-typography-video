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

def fetch_relevant_png(keyword, idx):
    filename = f"asset_{idx}.png"
    if os.path.exists(filename):
        return filename

    try:
        print(f"Fetching online image for topic keyword: {keyword}")
        search_url = f"https://pixabay.com/api/?key=38128328-912f2c8d28a3068e285a889b7&q={keyword}&image_type=illustration&safesearch=true"
        response = requests.get(search_url, timeout=5).json()

        if response.get("hits"):
            img_url = response["hits"][0]["webformatURL"]
            img_data = requests.get(img_url, timeout=5).content
            with open(filename, "wb") as f:
                f.write(img_data)
            return filename
    except Exception as e:
        print(f"Image Download Warning: {e}")

    fallback_url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f431.png"
    r = requests.get(fallback_url)
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    fetch_bg_music()
    create_pop_sound("pop.wav")

    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    bg_music = AudioFileClip("bg_music.mp3").volumex(0.12)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [
        (235, 240, 245),
        (245, 230, 235),
        (235, 230, 245),
        (242, 245, 238)
    ]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    print("Transcribing voice audio using Whisper...")
    script_words = []
    if os.path.exists("script.txt"):
        with open("script.txt", "r", encoding="utf-8") as f:
            script_words = f.read().strip().split()

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        "voice.mp3", 
        word_timestamps=True,
        initial_prompt=" ".join(script_words[:30]) if script_words else "Kya aapko pata hai"
    )

    context_keywords = ["anime", "marvel", "goku", "ironman", "cat", "hero"]
    for i in range(2):
        target_time = random.uniform(3.0, max(4.0, duration - 6.0))
        kw = random.choice(context_keywords)
        asset_file = fetch_relevant_png(kw, i)
        
        if os.path.exists(asset_file):
            img_clip = (
                ImageClip(asset_file)
                .set_start(target_time)
                .set_duration(3.5)
                .resize(width=320)
                .set_position((random.choice([100, 650]), random.choice([350, 1250])))
            )
            video_clips.append(img_clip)

    pop_audio = AudioFileClip("pop.wav").volumex(0.15)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']
    available_fonts = ['DejaVu-Sans-Bold', 'DejaVu-Sans-ExtraLight', 'DejaVu-Sans']
    font_sizes = [85, 105, 125]

    word_idx = 0
    for segment in segments:
        for word_item in segment.words:
            start = word_item.start
            end = word_item.end

            if script_words and word_idx < len(script_words):
                txt = script_words[word_idx].upper()
                word_idx += 1
            else:
                txt = word_item.word.strip().upper()

            if end > start:
                chosen_color = random.choice(color_palette)
                chosen_size = random.choice(font_sizes)
                chosen_font = random.choice(available_fonts)
                pos_y = random.choice(['center', 720, 960, 1180])

                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=chosen_size,
                        color=chosen_color,
                        font=chosen_font,
                        method='caption',
                        size=(950, None)
                    )
                    .set_position(('center', pos_y))
                    .set_start(start)
                    .set_end(end)
                )
                video_clips.append(txt_clip)

                if word_idx % 2 == 0 and (start + pop_audio.duration <= duration):
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Rendering final dynamic video...")
    final_video = CompositeVideoClip(video_clips).set_audio(full_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 completed successfully!")

if __name__ == "__main__":
    create_video()
