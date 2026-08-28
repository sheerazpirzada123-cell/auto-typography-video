import os
import random
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    
    # Aesthetic Solid Color Choices (Non-Black)
    bg_colors = [
        (225, 238, 244),  # Soft Ice Blue
        (245, 222, 228),  # Pastel Pink
        (230, 225, 238),  # Lilac / Light Purple
        (238, 238, 235),  # Soft Beige/Cream
        (220, 230, 225)   # Light Sage
    ]
    chosen_bg = random.choice(bg_colors)
    
    # 9:16 Vertical background
    bg = ColorClip(size=(1080, 1920), color=chosen_bg, duration=duration)
    clips = [bg]

    print("Transcribing audio with faster-whisper...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    text_colors = ['#C0392B', '#1F618D', '#117A65', '#D35400', '#2E4053', '#8E44AD']

    for segment in segments:
        for word in segment.words:
            txt = word.word.strip().upper()
            start = word.start
            end = word.end

            if end > start:
                color = random.choice(text_colors)
                # Dynamic positioning for aesthetic typography layout
                pos_y = random.choice(['center', 700, 900, 1100])
                
                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=90,
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

    print("Rendering video...")
    final_video = CompositeVideoClip(clips).set_audio(audio)
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
