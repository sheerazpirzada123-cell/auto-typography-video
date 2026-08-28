import os
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip

def create_video():
    if not os.path.exists("voice.mp3"):
        raise FileNotFoundError("voice.mp3 missing!")

    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    
    # Dark modern vertical background
    bg = ColorClip(size=(1080, 1920), color=(12, 12, 12), duration=duration)
    clips = [bg]

    print("Transcribing audio for typography timing...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("voice.mp3", word_timestamps=True)

    for segment in segments:
        for word in segment.words:
            txt = word.word.strip().upper()
            start = word.start
            end = word.end

            if end > start:
                # Dynamic Yellow Bold Typography Overlay
                txt_clip = (
                    TextClip(
                        txt,
                        fontsize=85,
                        color='#FFD700',
                        font='DejaVu-Sans-Bold',
                        stroke_color='black',
                        stroke_width=4
                    )
                    .set_position('center')
                    .set_start(start)
                    .set_end(end)
                )
                clips.append(txt_clip)

    print("Rendering long duration vertical video...")
    final_video = CompositeVideoClip(clips).set_audio(audio)
    final_video.write_videofile(
        "final_output.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        bitrate="2500k"
    )
    print("final_output.mp4 rendered successfully!")

if __name__ == "__main__":
    create_video()
