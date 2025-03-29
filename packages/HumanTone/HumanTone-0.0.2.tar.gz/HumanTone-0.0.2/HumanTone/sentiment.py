from textblob import TextBlob
import nltk
from transformers import pipeline

nltk.download('punkt')

# Load Transformer model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob, NLTK, and transformers."""
    # TextBlob Sentiment
    blob_sentiment = TextBlob(text).sentiment.polarity
    
    # Transformers Sentiment
    transformer_sentiment = sentiment_pipeline(text)[0]

    return {
        "textblob_sentiment": blob_sentiment,
        "transformer_sentiment": transformer_sentiment['label'],
        "transformer_score": transformer_sentiment['score']
    }
