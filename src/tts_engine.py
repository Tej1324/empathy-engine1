import pyttsx3
import os
import time

def generate_speech(text, rate, volume, pitch, emotion):
    """
    Generates a speech audio file using pyttsx3.

    I initialize the TTS engine per request to avoid
    blocking issues when used inside a Flask app
    (especially on Windows / SAPI5).
    """

    engine = pyttsx3.init()

    # Apply voice parameters derived from emotion
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Pitch support is platform-dependent (best-effort)
    try:
        engine.setProperty("pitch", pitch)
    except Exception:
        # Windows SAPI5 often ignores pitch changes
        pass

    # Audio files are stored under static/ so Flask can serve them
    os.makedirs("static/audio", exist_ok=True)

    # Timestamped filenames prevent overwriting during multiple requests
    filename = f"static/audio/output_{emotion}_{int(time.time())}.wav"

    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()

    return filename
