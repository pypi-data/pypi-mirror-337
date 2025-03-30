from transformers import pipeline
import stanza

stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')
classifier = pipeline("sentiment-analysis")

def deep_learning_sentiment(text):
    """Uses Stanza and Hugging Face Transformers for sentiment"""
    stanza_result = [s.sentiment for s in nlp(text).sentences]
    transformers_result = classifier(text)[0]
    
    return {
        "stanza": stanza_result,
        "transformers": transformers_result
    }
