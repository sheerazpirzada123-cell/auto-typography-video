import os
import random
import requests
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip, CompositeAudioClip

def download_assets():
    # Download calm background music
    if not os.path.exists("bg_music.mp3"):
        print("Downloading BG Music...")
        url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
        r = requests.get(url)
        with open("bg_music.mp3", "wb") as f:
            f.write(r.content)

    # Download pop sound effect
    if not os.path.exists("pop.mp3"):
        print("Downloading Sound Effect...")
        url = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a7315b.mp3"
        r = requests.get(url)
        with open("pop.mp3", "wb") as f:
            f.write(r.content)

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    download_assets()

    print("Loading audio elements...")
    voice_audio = AudioFileClip("voice.mp3")
    duration = voice_audio.duration

    bg_music = AudioFileClip("bg_music.mp3").volumex(0.10)
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

    pop_sound = AudioFileClip("pop.mp3").volumex(0.15)
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

                # Add sound effect on word appear (limit duration)
                if start + pop_sound.duration <= duration:
                    audio_layers.append(pop_sound.set_start(start))

    final_audio = CompositeAudioClip(audio_layers)

    print("Rendering video...")
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
