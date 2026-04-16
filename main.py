from src.emotion_analyzer import detect_emotion
from src.voice_mapper import map_emotion_to_voice
from src.tts_engine import generate_speech

# CLI-based entry point for quick testing without the web UI
text = input("Enter text: ")

emotion, intensity = detect_emotion(text)

rate, volume, pitch = map_emotion_to_voice(emotion, intensity)

print(f"Detected emotion: {emotion}")
print(f"Emotion intensity: {intensity:.2f}")
print(f"Speech rate: {rate}")
print(f"Speech volume: {volume}")
print(f"Speech pitch: {pitch}")

output_file = generate_speech(
    text=text,
    rate=rate,
    volume=volume,
    pitch=pitch,
    emotion=emotion
)

print(f"Audio saved to {output_file}")
