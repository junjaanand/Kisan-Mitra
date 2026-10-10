"""SerpApi client supporting 5 engines for KisanMitra: Search, News, Trends, Shopping, Maps."""
import os
import time
from typing import Dict, Any, Optional, List
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


class SerpApiClient:
    """Multi-Engine SerpApi client wrapper with rate limiting and robust error handling."""

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not found in environment variables")
        self._last_call_time = 0.0
        self._min_interval = 0.8  # seconds between calls to prevent rate limits

    def _rate_limit(self):
        """Simple rate limiter to respect API thresholds."""
        elapsed = time.time() - self._last_call_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call_time = time.time()

    def search_google(self, query: str, num: int = 10, location: str = "India") -> Dict[str, Any]:
        """Engine 1: Google Search — for APMC Mandi prices, crop arrivals, and weather."""
        self._rate_limit()
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
                "gl": "in",
                "hl": "en",
                "location": location,
                "num": num,
            }
            search = GoogleSearch(params)
            return search.get_dict() or {}
        except Exception as e:
            print(f"SerpApi Google Search error for '{query}': {e}")
            return {}

    def search_news(self, query: str) -> Dict[str, Any]:
        """Engine 2: Google News — for agricultural alerts, pest warnings, and policy shifts."""
        self._rate_limit()
        try:
            params = {
                "engine": "google_news",
                "q": query,
                "api_key": self.api_key,
                "gl": "in",
                "hl": "en",
            }
            search = GoogleSearch(params)
            return search.get_dict() or {}
        except Exception as e:
            print(f"SerpApi Google News error for '{query}': {e}")
            return {}

    def search_trends(self, query: str, geo: str = "IN", date: str = "today 12-m") -> Dict[str, Any]:
        """Engine 3: Google Trends — for crop search interest and seasonal demand cycles."""
        self._rate_limit()
        try:
            params = {
                "engine": "google_trends",
                "q": query,
                "api_key": self.api_key,
                "geo": geo,
                "date": date,
                "data_type": "TIMESERIES",
            }
            search = GoogleSearch(params)
            return search.get_dict() or {}
        except Exception as e:
            print(f"SerpApi Google Trends error for '{query}': {e}")
            return {}

    def search_shopping(self, query: str, num: int = 8) -> Dict[str, Any]:
        """Engine 4: Google Shopping — for real-time rates on seeds, fertilizers, and tools."""
        self._rate_limit()
        try:
            params = {
                "engine": "google_shopping",
                "q": query,
                "api_key": self.api_key,
                "gl": "in",
                "hl": "en",
                "location": "India",
                "num": num,
            }
            search = GoogleSearch(params)
            return search.get_dict() or {}
        except Exception as e:
            print(f"SerpApi Google Shopping error for '{query}': {e}")
            return {}

    def search_maps(self, query: str) -> Dict[str, Any]:
        """Engine 5: Google Maps — for discovering nearest APMC mandis and warehouses."""
        self._rate_limit()
        try:
            params = {
                "engine": "google_maps",
                "q": query,
                "api_key": self.api_key,
                "gl": "in",
                "hl": "en",
                "type": "search",
            }
            search = GoogleSearch(params)
            return search.get_dict() or {}
        except Exception as e:
            print(f"SerpApi Google Maps error for '{query}': {e}")
            return {}

    def get_remaining_searches(self) -> Optional[int]:
        """Check remaining SerpApi searches for the account."""
        try:
            from serpapi import AccountApi
            account = AccountApi(api_key=self.api_key)
            info = account.get_dict()
            return info.get("total_searches_left")
        except Exception:
            return None
