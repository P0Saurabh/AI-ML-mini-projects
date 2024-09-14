import os
import moviepy.editor as mp
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Set the path to ImageMagick (Update this path as necessary)
os.environ['IMAGEMAGICK_BINARY'] = r'C:\Program Files\ImageMagick-7.x.x-Q16\magick.exe'

def transcribe_video_audio(video_path):
    # Load the video
    video = mp.VideoFileClip(video_path)

    # Extract the audio from the video
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path)

    # Load the transcription pipeline
    transcriber = pipeline("automatic-speech-recognition")
    result = transcriber(audio_path)

    # Delete the temporary audio file
    os.remove(audio_path)

    # Return the transcript
    return result['text']

def analyze_transcript(transcript):
    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Analyze transcript and store sentiment scores
    sentiment_score = sia.polarity_scores(transcript)
    return sentiment_score

def create_subtitle_clip(subtitle_text, video_clip):
    generator = lambda txt: mp.TextClip(txt, font='Arial-Bold', fontsize=24, color='white')
    subtitle_clip = generator(subtitle_text).set_duration(video_clip.duration)
    return mp.CompositeVideoClip([video_clip, subtitle_clip])

def extract_clips(video_path, output_folder, num_clips):
    # Load the video
    video = mp.VideoFileClip(video_path)

    # Dummy clips extraction for demonstration
    clips = []
    duration = video.duration
    clip_duration = duration / num_clips

    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = start_time + clip_duration

        # Extract the clip
        clip = video.subclip(start_time, end_time)

        # Create subtitles for the clip
        subtitle_text = f"Clip {i + 1}"
        subtitle_clip = create_subtitle_clip(subtitle_text, clip)
        final_clip = mp.CompositeVideoClip([clip, subtitle_clip])

        # Save the clip
        clip_filename = os.path.join(output_folder, f"clip_{i + 1}.mp4")
        final_clip.write_videofile(clip_filename, codec="libx264")
        clips.append(clip_filename)

    return clips

def main():
    video_path = "s.mp4"  # Replace with your video file path
    output_folder = "output"
    num_clips = 5

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Transcribe video to text
    transcript = transcribe_video_audio(video_path)
    #
    # # Analyze transcript
    # sentiment_scores = analyze_transcript(transcript)
    #
    # # Print sentiment scores
    # print(f"Sentiment Scores: {sentiment_scores}")
    #
    # # Extract clips
    # clips = extract_clips(video_path, output_folder, num_clips)
    #
    # print(f"Extracted clips: {clips}")

if __name__ == "__main__":
    main()
