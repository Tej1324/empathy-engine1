# Simple manual test cases to validate emotion detection
# and voice parameter mapping logic.

test_sentences = [
    "This is AMAZING news!",
    "Why is this taking so long?",
    "I am really disappointed with the service.",
    "Your request has been processed."
]

from src.emotion_analyzer import detect_emotion
from src.voice_mapper import map_emotion_to_voice

for text in test_sentences:
    emotion, intensity = detect_emotion(text)
    rate, volume, pitch = map_emotion_to_voice(emotion, intensity)

    print("-" * 50)
    print(f"Text: {text}")
    print(f"Emotion: {emotion}")
    print(f"Intensity: {intensity:.2f}")
    print(f"Rate: {rate}, Volume: {volume}, Pitch: {pitch}")
