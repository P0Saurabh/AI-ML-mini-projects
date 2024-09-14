import speech_recognition as sr
from moviepy.editor import VideoFileClip
import time


def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def transcribe_audio(recognizer, audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


def process_audio(audio_path, chunk_duration):
    r = sr.Recognizer()
    transcription = []

    with sr.AudioFile(audio_path) as source:
        audio_length = source.DURATION
        for i in range(0, int(audio_length / chunk_duration)):
            audio = r.record(source, duration=chunk_duration)
            text = transcribe_audio(r, audio)
            if text:
                start_time = i * chunk_duration
                end_time = (i + 1) * chunk_duration
                transcription.append(f"{start_time:.2f} - {end_time:.2f}: {text}")

    return transcription


def save_transcription(transcription, output_file):
    with open(output_file, 'w') as f:
        for line in transcription:
            f.write(line + '\n')


def main(video_path):
    audio_path = "temp_audio.wav"
    output_file = "transcription.txt"
    chunk_duration = 3  # Process audio in 3-second chunks

    print("Extracting audio from video...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    transcription = process_audio(audio_path, chunk_duration)

    print("Saving transcription...")
    save_transcription(transcription, output_file)

    print(f"Transcription saved to {output_file}")


if __name__ == "__main__":
    video_path = "a.mp4"  # Replace with your video file path
    main(video_path)