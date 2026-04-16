from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# I chose VADER because it is lightweight, fast, and works well
# for short conversational text without needing heavy ML models.
analyzer = SentimentIntensityAnalyzer()

def detect_emotion(text):
    """
    Analyzes the input text and returns:
    - a human-readable emotion label
    - the sentiment intensity (compound score)

    I use a mix of sentiment score + simple rules
    to keep the logic explainable and reliable.
    """

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    # Granular emotion detection using clear, rule-based logic
    # This avoids black-box behavior and makes decisions easy to explain
    if compound >= 0.7 or "!" in text:
        emotion = "enthusiastic"
    elif compound <= -0.5:
        emotion = "frustrated"
    elif "?" in text:
        emotion = "inquisitive"
    elif compound >= 0.05:
        emotion = "positive"
    elif compound <= -0.05:
        emotion = "negative"
    else:
        emotion = "neutral"

    return emotion, compound
