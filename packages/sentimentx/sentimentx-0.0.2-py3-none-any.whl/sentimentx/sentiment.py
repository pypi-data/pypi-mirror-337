from sentimentx.lexicon import lexicon_sentiment
from sentimentx.emotions import detect_emotion
from sentimentx.deep_learning import deep_learning_sentiment

def analyze_sentiment(text):
    """Combines lexicon, emotion, and deep learning methods"""
    lexicon_result = lexicon_sentiment(text)
    emotion_result = detect_emotion(text)
    deep_learning_result = deep_learning_sentiment(text)
    
    return {
        "lexicon": lexicon_result,
        "emotion": emotion_result,
        "deep_learning": deep_learning_result
    }
