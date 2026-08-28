import whisper
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip

def create_video():
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    
    model = whisper.load_model("tiny")
    result = model.transcribe("voice.mp3", word_timestamps=True)
    
    bg = ColorClip(size=(1080, 1920), color=(245, 245, 245), duration=duration)
    clips = [bg]
    
    for segment in result['segments']:
        for word in segment['words']:
            txt = word['word'].strip().upper()
            start = word['start']
            end = word['end']
            
            txt_clip = (TextClip(txt, fontsize=75, color='black', font='Arial-Bold')
                        .set_position('center')
                        .set_start(start)
                        .set_end(end))
            clips.append(txt_clip)
            
    final_video = CompositeVideoClip(clips).set_audio(audio)
    final_video.write_videofile("final_output.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    create_video()
