import text2emotion as te

def detect_emotion(text):
    """Detects emotions in text"""
    return te.get_emotion(text)
