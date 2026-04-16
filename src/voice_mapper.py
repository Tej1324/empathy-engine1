# Baseline voice configuration
BASE_RATE = 150
BASE_VOLUME = 0.9
BASE_PITCH = 50  # Engine-dependent default

# Scaling factors control how strongly emotion affects voice
POSITIVE_RATE_SCALE = 50
NEGATIVE_RATE_SCALE = 40

POSITIVE_VOLUME_SCALE = 0.15
NEGATIVE_VOLUME_SCALE = 0.15

POSITIVE_PITCH_SCALE = 15
NEGATIVE_PITCH_SCALE = 10

MIN_VOLUME = 0.6
MAX_VOLUME = 1.0

def map_emotion_to_voice(emotion, intensity):
    """
    Maps emotion + intensity into concrete voice parameters.

    I use the absolute value of intensity so that
    stronger emotions (positive or negative) result
    in stronger modulation.
    """

    intensity = abs(intensity)

    if emotion in ["positive", "enthusiastic"]:
        rate = BASE_RATE + int(intensity * POSITIVE_RATE_SCALE)
        volume = min(MAX_VOLUME, BASE_VOLUME + intensity * POSITIVE_VOLUME_SCALE)
        pitch = BASE_PITCH + int(intensity * POSITIVE_PITCH_SCALE)

    elif emotion in ["negative", "frustrated"]:
        rate = BASE_RATE - int(intensity * NEGATIVE_RATE_SCALE)
        volume = max(MIN_VOLUME, BASE_VOLUME - intensity * NEGATIVE_VOLUME_SCALE)
        pitch = BASE_PITCH - int(intensity * NEGATIVE_PITCH_SCALE)

    elif emotion == "inquisitive":
        # Slightly quicker and higher tone to sound curious
        rate = BASE_RATE + 10
        volume = BASE_VOLUME
        pitch = BASE_PITCH + 5

    else:
        # Neutral speech stays close to baseline
        rate = BASE_RATE
        volume = BASE_VOLUME
        pitch = BASE_PITCH

    return rate, volume, pitch
