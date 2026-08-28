import os
import random
import requests
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip

def create_pop_sound(filename="pop.wav"):
    if not os.path.exists(filename):
        sample_rate = 44100
        duration = 0.04
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(950, 180, len(t))
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

    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration
    print(f"Target Video Length: {duration:.2f}s")

    bg_music = AudioFileClip("bg_music.mp3").volumex(0.08)
    if bg_music.duration < duration:
        bg_music = bg_music.loop(duration=duration)
    else:
        bg_music = bg_music.subclip(0, duration)

    audio_stack = [voice_audio, bg_music]

    # Minimal clean aesthetic backgrounds
    bg_colors = [
        (238, 242, 245),
        (245, 235, 238),
        (235, 232, 245),
        (242, 245, 238),
        (230, 238, 235)
    ]
    bg = ColorClip(size=(1080, 1920), color=random.choice(bg_colors), duration=duration)
    video_clips = [bg]

    print("Transcribing voice audio using Whisper...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    pop_audio = AudioFileClip("pop.wav").volumex(0.18)
    
    # Aesthetic Typography Setup (Fonts, Sizes, Vivid Colors)
    available_fonts = ['DejaVu-Sans-Bold', 'DejaVu-Sans-ExtraLight', 'DejaVu-Sans']
    color_palette = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD', '#B7950B']
    font_sizes = [80, 100, 120]

    for segment in segments:
        for word in segment.words:
            # Displaying pure Hinglish word
            txt = word.word.strip()
            start = word.start
            end = word.end

            if end > start:
                chosen_color = random.choice(color_palette)
                chosen_size = random.choice(font_sizes)
                chosen_font = random.choice(available_fonts)
                pos_y = random.choice(['center', 700, 950, 1200])

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

                if start + pop_audio.duration <= duration:
                    audio_stack.append(pop_audio.set_start(start))

    full_audio = CompositeAudioClip(audio_stack)

    print("Rendering video...")
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
