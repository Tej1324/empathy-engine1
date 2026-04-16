from flask import Flask, render_template, request
from src.emotion_analyzer import detect_emotion
from src.voice_mapper import map_emotion_to_voice
from src.tts_engine import generate_speech

# Explicit static folder declaration for serving audio files
app = Flask(__name__, static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    emotion = None
    intensity = None
    audio_file = None

    if request.method == "POST":
        text = request.form["text"]

        # Step 1: Detect emotion and its intensity
        emotion, intensity = detect_emotion(text)

        # Step 2: Convert emotion into voice parameters
        rate, volume, pitch = map_emotion_to_voice(emotion, intensity)

        # Step 3: Generate speech audio
        audio_path = generate_speech(
            text=text,
            rate=rate,
            volume=volume,
            pitch=pitch,
            emotion=emotion
        )

        # Make audio path accessible to browser
        audio_file = "/" + audio_path

    return render_template(
        "index.html",
        emotion=emotion,
        intensity=round(intensity, 2) if intensity is not None else None,
        audio_file=audio_file
    )

if __name__ == "__main__":
    app.run(debug=False)
