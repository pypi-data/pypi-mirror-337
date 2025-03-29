from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

def lexicon_sentiment(text):
    """Returns polarity score from TextBlob & VADER"""
    blob = TextBlob(text)
    vader = SentimentIntensityAnalyzer()
    scores = vader.polarity_scores(text)
    
    return {
        "textblob_polarity": blob.sentiment.polarity,
        "textblob_subjectivity": blob.sentiment.subjectivity,
        "vader": scores
    }
