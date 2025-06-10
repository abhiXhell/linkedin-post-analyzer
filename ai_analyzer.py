import time
import random
import traceback
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from config import ANALYSIS_PROMPT, DEFAULT_ANALYSIS

class AIAnalyzer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        
        # Rate limiting parameters
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum seconds between requests
        self.max_retries = 3
        self.retry_delay = 2  # Base delay in seconds

    def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def analyze_post(self, post_text: str) -> dict:
        """Analyze a LinkedIn post using AI"""
        if not post_text or not post_text.strip():
            return DEFAULT_ANALYSIS

        for attempt in range(self.max_retries):
            try:
                # Prepare the prompt
                prompt = ANALYSIS_PROMPT.format(post_text=post_text)
                
                # Wait for rate limit before making request
                self._wait_for_rate_limit()
                
                # Use a Gemini model for the chat completions call
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                if response and response.text:
                    try:
                        # Try to parse the response as JSON
                        analysis = json.loads(response.text)
                        return analysis
                    except json.JSONDecodeError:
                        # If response is not valid JSON, return default analysis
                        return DEFAULT_ANALYSIS
                else:
                    return DEFAULT_ANALYSIS

            except Exception as e:
                if attempt < self.max_retries - 1:
                    # Add exponential backoff
                    delay = self.retry_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                return DEFAULT_ANALYSIS

        return DEFAULT_ANALYSIS

    def enrich_analysis(self, analysis: dict) -> dict:
        """Add additional insights or process the analysis if needed"""
        return analysis