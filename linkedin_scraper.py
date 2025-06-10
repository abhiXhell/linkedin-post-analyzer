from serpapi import GoogleSearch
import config
import json
from typing import List, Dict
import time

class LinkedInScraper:
    def __init__(self):
        self.api_key = config.SERPAPI_API_KEY
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not found in environment variables")

    def search_posts(self, keywords: str, tags: str = None) -> List[Dict]:
        """
        Search for LinkedIn posts using SerpAPI
        
        Args:
            keywords (str): Search keywords
            tags (str, optional): Additional tags to filter by
            
        Returns:
            List[Dict]: List of post data including title, snippet, link, etc.
        """
        query = f'site:linkedin.com/posts "{keywords}"'
        if tags:
            query += f' "{tags}"'

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": config.MAX_POSTS
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "error" in results:
                raise Exception(f"SerpAPI Error: {results['error']}")

            posts = []
            if "organic_results" in results:
                for result in results["organic_results"]:
                    post = {
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "date": result.get("date", ""),
                        "position": result.get("position", 0)
                    }
                    posts.append(post)

            return posts

        except Exception as e:
            print(f"Error searching posts: {str(e)}")
            return []

    def extract_post_data(self, post: Dict) -> Dict:
        """
        Extract relevant data from a post
        
        Args:
            post (Dict): Raw post data from SerpAPI
            
        Returns:
            Dict: Processed post data
        """
        return {
            "post_text": f"{post['title']} {post['snippet']}",
            "post_url": post["link"],
            "post_date": post["date"],
            "post_position": post["position"]
        } 