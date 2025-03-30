SentimentX is an advanced sentiment analysis Python library that combines multiple sentiment detection techniques, including lexicon-based, emotion detection, and deep learning models, to provide a comprehensive analysis of text sentiment.

-> Features:

1. Lexicon-based Analysis: Uses predefined sentiment lexicons to determine sentiment scores.

2. Emotion Detection: Identifies emotions such as happiness, sadness, anger, etc.

3. Deep Learning Models: Leverages transformer-based models for context-aware sentiment classification.

4. Multilingual Support: Supports sentiment analysis in multiple languages.

5. Emoji & Slang Handling: Understands modern-day text including emojis and internet slang.

-> Installation:

pip install sentimentx

-> Usage:

from sentimentx.sentiment import analyze_sentiment

# Sample text
text = "I am really happy today! This is the best day of my life 🎉"

# Analyze sentiment
result = analyze_sentiment(text)

# Display results
import json
print(json.dumps(result, indent=4))

Output Example

{
    "lexicon": "Positive",
    "emotion": "Happy",
    "deep_learning": "Positive"
}

-> Modules:

1. lexicon.py

Function: lexicon_sentiment(text)

Uses sentiment dictionaries to classify text.

2. emotions.py

Function: detect_emotion(text)

Detects emotions based on predefined word mappings.

3. deep_learning.py

Function: deep_learning_sentiment(text)

Uses transformer models (e.g., BERT) to classify sentiment.

4. sentiment.py

Function: analyze_sentiment(text)

Combines lexicon, emotion, and deep learning results into a unified sentiment analysis output.

-> Contributing:

Pull requests are welcome! If you find a bug or have suggestions, feel free to open an issue.

-> License:

MIT License. See LICENSE for details.