import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip

def generate_clean_pop_sound(filename="pop.wav"):
    """Valid WAV pop sound effect generate karta hai bina kisi corruption error ke."""
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.05  # 50 ms
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        # Sine wave frequency drop for a clean 'pop'
        freq = np.linspace(800, 150, len(t))
        waveform = np.sin(2 * np.pi * freq * t) * np.exp(-t * 80)
        audio_data = (waveform * 32767).astype(np.int16)
        wavfile.write(filename, sample_rate, audio_data)

def download_assets():
    if not os.path.exists("bg_music.mp3"):
        print("Downloading BG Music...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

    generate_clean_pop_sound("pop.wav")

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    download_assets()

    print("Loading audio elements...")
    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    # Background music handling
    bg_music = AudioFileClip("bg_music.mp3").volumex(0.08)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_layers = [voice_audio, bg_music]

    bg_colors = [
        (225, 238, 244),
        (245, 222, 228),
        (230, 225, 238),
        (238, 238, 235),
        (220, 230, 225)
    ]
    chosen_bg = random.choice(bg_colors)

    bg = ColorClip(size=(1080, 1920), color=chosen_bg, duration=duration)
    clips = [bg]

    print("Transcribing audio for Roman Hinglish typography...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    pop_sound = AudioFileClip("pop.wav").volumex(0.20)
    text_colors = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']

    for segment in segments:
        for word in segment.words:
            txt = word.word.strip().upper()
            start = word.start
            end = word.end

            if end > start:
                color = random.choice(text_colors)
                pos_y = random.choice(['center', 750, 950, 1150])

                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=95,
                        color=color,
                        font='DejaVu-Sans-Bold',
                        method='caption',
                        size=(950, None)
                    )
                    .set_position(('center', pos_y))
                    .set_start(start)
                    .set_end(end)
                )
                clips.append(txt_clip)

                if start + pop_sound.duration <= duration:
                    audio_layers.append(pop_sound.set_start(start))

    final_audio = CompositeAudioClip(audio_layers)

    print("Rendering final video...")
    final_video = CompositeVideoClip(clips).set_audio(final_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 generated successfully!")

if __name__ == "__main__":
    create_video()
