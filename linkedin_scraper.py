import requests
from bs4 import BeautifulSoup
import time
import random

class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.min_delay = 2
        self.max_delay = 5

    def _add_delay(self):
        """Add random delay between requests"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

    def scrape_post(self, url: str) -> dict:
        """Scrape a LinkedIn post URL"""
        try:
            self._add_delay()
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract post text
            post_text = soup.find('div', {'class': 'feed-shared-update-v2__description'})
            if post_text:
                post_text = post_text.get_text(strip=True)
            else:
                return None
            
            return {
                'text': post_text,
                'url': url
            }
            
        except Exception as e:
            return None 