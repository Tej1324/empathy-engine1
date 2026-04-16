def build_ssml(text, emotion):
    """
    This function demonstrates how emotion-aware SSML
    can be generated for advanced TTS engines.

    I intentionally keep this separate because pyttsx3
    (Windows / SAPI5) has limited SSML support.

    This design allows easy migration to cloud TTS
    engines like Google Cloud TTS or Amazon Polly.
    """

    if emotion == "enthusiastic":
        return f"""
        <speak>
            <prosody rate="fast" pitch="+10%">
                {text}
            </prosody>
        </speak>
        """

    elif emotion == "frustrated":
        return f"""
        <speak>
            <prosody rate="slow" pitch="-5%">
                {text}
            </prosody>
        </speak>
        """

    elif emotion == "inquisitive":
        return f"""
        <speak>
            <prosody rate="medium">
                {text}
            </prosody>
            <break time="300ms"/>
        </speak>
        """

    else:
        return f"<speak>{text}</speak>"
