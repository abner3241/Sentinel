
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str):
        return self.analyzer.polarity_scores(text)
