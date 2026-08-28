import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
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
        print("bg_music.mp3 not found in repo. Downloading default music...")
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

    raw_bg = AudioFileClip("bg_music.mp3")
    bg_music = audio_loop(raw_bg, duration=duration).volumex(0.10)

    audio_stack = [voice_audio, bg_music]

    bg_colors = [(240, 243, 246), (245, 235, 238), (236, 233, 245), (230, 240, 235)]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    print("Extracting exact word timestamps with Whisper...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        "voice.mp3",
        word_timestamps=True,
        language="hi",
        task="transcribe"
    )

    pop_audio = AudioFileClip("pop.wav").volumex(0.20)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']
    font_sizes = [110, 125, 140]

    word_count = 0
    for segment in segments:
        for word_info in segment.words:
            word_text = word_info.word.strip().strip(".,!?").upper()
            start = max(0, word_info.start)
            end = min(duration, word_info.end)

            if word_text and (end > start):
                word_count += 1
                txt_clip = (
                    TextClip(
                        word_text,
                        fontsize=random.choice(font_sizes),
                        color=random.choice(color_palette),
                        font='DejaVu-Sans-Bold',
                        method='caption',
                        size=(950, None)
                    )
                    .set_position(('center', 'center'))
                    .set_start(start)
                    .set_end(end)
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
