import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip
from moviepy.audio.fx.all import audio_loop

def create_pop_sound(filename="pop.wav"):
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.03
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(1400, 400, len(t))
        waveform = np.sin(2 * np.pi * freq * t) * np.exp(-t * 90)
        audio_data = (waveform * 32767).astype(np.int16)
        wavfile.write(filename, sample_rate, audio_data)

def ensure_bg_music():
    if not os.path.exists("bg_music.mp3"):
        print("bg_music.mp3 not found. Downloading default music...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")
        
    ensure_bg_music()
    create_pop_sound("pop.wav")

    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    # Music drop segment (starts 10s into the audio file for the best section)
    raw_bg = AudioFileClip("bg_music.mp3")
    start_time = 10 if raw_bg.duration > 15 else 0
    bg_cut = raw_bg.subclip(start_time, min(start_time + duration, raw_bg.duration))
    bg_music = audio_loop(bg_cut, duration=duration).volumex(0.12)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [(240, 243, 246), (245, 235, 238), (236, 233, 245), (230, 240, 235)]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    # Script words reading
    if os.path.exists("script.txt"):
        with open("script.txt", "r", encoding="utf-8") as f:
            raw_text = f.read().strip()
            clean_text = ''.join([c for c in raw_text if ord(c) < 128])
            words = [w.strip().upper() for w in clean_text.split() if w.strip()]
    else:
        words = ["MARVEL", "COMICS", "FACTS", "ARE", "CRAZY"]

    total_words = len(words)
    if total_words > 0:
        time_per_word = duration / total_words
        pop_audio = AudioFileClip("pop.wav").volumex(0.20)
        color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']

        words_per_page = 4  # Each page holds up to 4 stacked words
        
        for i in range(total_words):
            page_index = i // words_per_page
            word_in_page = i % words_per_page
            
            page_end_word = min((page_index + 1) * words_per_page, total_words)
            page_end_time = page_end_word * time_per_word

            start = i * time_per_word
            
            page_words_so_far = words[page_index * words_per_page : i + 1]
            display_text = "\n".join(page_words_so_far)

            segment_end = (i + 1) * time_per_word if word_in_page < (words_per_page - 1) and (i + 1) < total_words else page_end_time

            if segment_end > start:
                txt_clip = (
                    TextClip(
                        display_text,
                        fontsize=105,
                        color=random.choice(color_palette),
                        font='DejaVu-Sans-Bold',
                        align='center',
                        method='caption',
                        size=(900, None)
                    )
                    .set_position(('center', 'center'))
                    .set_start(start)
                    .set_end(segment_end)
                )
                video_clips.append(txt_clip)

                if start + pop_audio.duration <= duration:
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
    print("final_output.mp4 successfully created!")

if __name__ == "__main__":
    create_video()
