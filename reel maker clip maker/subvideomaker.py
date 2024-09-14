import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from fer import FER

# Load emotion detection model
emotion_detector = FER()


def detect_emotions(video_path):
    video = cv2.VideoCapture(video_path)
    emotions = []
    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        result = emotion_detector.detect_emotions(frame)
        if result:
            emotions.append(np.mean([emotion for emotion in result[0]['emotions'].values()]))
        frame_count += 1
    video.release()
    return emotions, frame_scount


def get_high_emotion_segments(emotions, frame_count, threshold=0.5):
    segment_length = 30  # Length of each segment in frames
    high_emotion_segments = []
    num_segments = frame_count // segment_length + (1 if frame_count % segment_length != 0 else 0)
    for i in range(num_segments):
        start = i * segment_length
        end = min(start + segment_length, frame_count)
        if len(emotions[start:end]) > 0:  # Check if the segment is not empty
            if np.max(emotions[start:end]) > threshold:
                high_emotion_segments.append((start / frame_count, end / frame_count))
    return high_emotion_segments


def process_video(video_path):
    video = VideoFileClip(video_path)

    # Detect high-impact segments based on emotions
    emotions, frame_count = detect_emotions(video_path)

    if frame_count == 0:
        print("No frames detected in video.")
        return

    if not emotions:
        print("No emotions detected.")
        return

    high_emotion_segments = get_high_emotion_segments(emotions, frame_count)

    if not high_emotion_segments:
        print("No high emotion segments detected.")
        return

    # Extract and concatenate high-impact segments
    subclips = [video.subclip(start, end) for start, end in high_emotion_segments]
    if subclips:
        final_subvideo = concatenate_videoclips(subclips)
        final_subvideo.write_videofile("high_impact_subvideo.mp4", codec='libx264')
    else:
        print("No subclips to concatenate.")


# Path to your video file
video_path = "s.mp4"

# Process the video to create a high-impact subvideo
process_video(video_path)
