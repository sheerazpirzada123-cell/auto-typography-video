import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip

def create_pop_sound(filename="pop.wav"):
    """Generates a clean synthetic pop sound without ffmpeg decode failures."""
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.04
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(900, 200, len(t))
        waveform = np.sin(2 * np.pi * freq * t) * np.exp(-t * 90)
        audio_data = (waveform * 32767).astype(np.int16)
        wavfile.write(filename, sample_rate, audio_data)

def fetch_bg_music():
    if not os.path.exists("bg_music.mp3"):
        print("Fetching background music...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    fetch_bg_music()
    create_pop_sound("pop.wav")

    print("Loading sound components...")
    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration
    print(f"Generated Video Duration: {duration:.2f} seconds")

    # Background audio adjustments
    bg_music = AudioFileClip("bg_music.mp3").volumex(0.08)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_stack = [voice_audio, bg_music]

    # Minimal aesthetic background colors (Non-black pastels)
    bg_colors = [
        (235, 240, 245),
        (245, 230, 235),
        (235, 230, 245),
        (245, 245, 240),
        (230, 240, 235)
    ]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    print("Processing Whisper Hinglish word timing...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    pop_audio = AudioFileClip("pop.wav").volumex(0.18)
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']

    for segment in segments:
        for word in segment.words:
            txt = word.word.strip().upper()
            start = word.start
            end = word.end

            if end > start:
                color = random.choice(color_palette)
                pos_y = random.choice(['center', 750, 950, 1150])

                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=96,
                        color=color,
                        font='DejaVu-Sans-Bold',
                        method='caption',
                        size=(950, None)
                    )
                    .set_position(('center', pos_y))
                    .set_start(start)
                    .set_end(end)
                )
                video_clips.append(txt_clip)

                if start + pop_audio.duration <= duration:
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Compiling final video output...")
    final_video = CompositeVideoClip(video_clips).set_audio(full_audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 complete!")

if __name__ == "__main__":
    create_video()
