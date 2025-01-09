from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any

def analyze_sentiment_textblob(text: str) -> TextBlob:
    """Analyze the sentiment of the given text using TextBlob.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        TextBlob: The sentiment analysis result from TextBlob.
    """
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment
        return sentiment
    except Exception as e:
        print(f"Error analyzing sentiment with TextBlob: {e}")
        return None

def analyze_sentiment_vader(text: str) -> Dict[str, Any]:
    """Analyze the sentiment of the given text using VADER.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        dict: The sentiment analysis result from VADER.
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(text)
        return sentiment
    except Exception as e:
        print(f"Error analyzing sentiment with VADER: {e}")
        return {}
