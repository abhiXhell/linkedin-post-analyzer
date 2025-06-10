import requests
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
from textblob import TextBlob
import tldextract
from typing import Dict, Tuple, Optional
import re

class PostEnricher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_website(self, text: str) -> Optional[str]:
        """Extract website URL from text."""
        # Look for common URL patterns
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        urls = re.findall(url_pattern, text)
        
        if urls:
            return urls[0]
        return None

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        
        if emails:
            try:
                validated_email = validate_email(emails[0])
                return validated_email.email
            except EmailNotValidError:
                return None
        return None

    def analyze_sentiment(self, text: str) -> Tuple[float, str]:
        """Analyze sentiment of text using TextBlob."""
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        
        if score > 0.3:
            sentiment = "Positive"
        elif score < -0.3:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return score, sentiment

    def analyze_traction(self, text: str) -> Dict:
        """Analyze post traction based on engagement indicators."""
        traction = {
            "engagement_score": 0,
            "engagement_indicators": []
        }
        
        # Check for engagement indicators
        indicators = {
            "feedback": ["feedback", "comments", "thoughts", "suggestions"],
            "collaboration": ["collaborate", "partner", "join", "team up"],
            "launch": ["launched", "live", "released", "published"],
            "growth": ["growing", "users", "customers", "revenue"]
        }
        
        text_lower = text.lower()
        for category, words in indicators.items():
            if any(word in text_lower for word in words):
                traction["engagement_score"] += 1
                traction["engagement_indicators"].append(category)
        
        return traction

    def enrich_post(self, post_data: Dict) -> Dict:
        """Enrich post data with email, sentiment, and traction analysis."""
        enriched_data = post_data.copy()
        
        # Extract website and email
        website = self.extract_website(post_data["Post Text"])
        email = self.extract_email(post_data["Post Text"])
        
        # Analyze sentiment
        sentiment_score, sentiment = self.analyze_sentiment(post_data["Post Text"])
        
        # Analyze traction
        traction = self.analyze_traction(post_data["Post Text"])
        
        # Add enriched data
        enriched_data.update({
            "Website": website,
            "Email": email,
            "Sentiment Score": round(sentiment_score, 2),
            "Sentiment": sentiment,
            "Engagement Score": traction["engagement_score"],
            "Engagement Indicators": ", ".join(traction["engagement_indicators"])
        })
        
        return enriched_data 