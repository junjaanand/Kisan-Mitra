"""Query Strategist Agent — Converts farmer profile into multi-engine SerpApi queries."""
from typing import Dict, List
from models.farmer_profile import FarmerProfile
from utils.llm_client import GeminiClient
from config.prompts import QUERY_GENERATION_PROMPT


class QueryStrategistAgent:
    """Generates targeted search queries across 5 search engines based on farmer profile."""

    def __init__(self, llm_client: GeminiClient):
        self.llm = llm_client

    def generate_strategy(self, profile: FarmerProfile) -> Dict[str, List[str]]:
        """Generate targeted search queries grouped by engine.
        
        Returns:
            Dict with keys: 'google_search', 'google_news', 'google_trends', 
            'google_shopping', 'google_maps'
        """
        prompt = QUERY_GENERATION_PROMPT.format(
            farmer_profile=profile.to_search_context()
        )

        res = self.llm.generate_json(prompt)

        # Fallback if LLM output is invalid or missing keys
        fallback = self._build_fallback(profile)
        if not isinstance(res, dict):
            return fallback

        strategy = {}
        for key in ["google_search", "google_news", "google_trends", "google_shopping", "google_maps"]:
            val = res.get(key)
            if isinstance(val, list) and len(val) > 0:
                strategy[key] = val
            else:
                strategy[key] = fallback[key]

        return strategy

    def _build_fallback(self, profile: FarmerProfile) -> Dict[str, List[str]]:
        """Deterministic rule-based query fallback."""
        primary_crop = profile.crops[0] if profile.crops else "Onion"
        secondary_crop = profile.crops[1] if len(profile.crops) > 1 else "Tomato"
        district = profile.district
        state = profile.state

        return {
            "google_search": [
                f"{primary_crop} mandi price today {district} {state} 2026",
                f"{secondary_crop} mandi price today {district} {state} 2026",
                f"{district} agriculture weather forecast 7 days rain"
            ],
            "google_news": [
                f"{state} agriculture {primary_crop} alert 2026",
                f"{primary_crop} mandi price market news India"
            ],
            "google_trends": [
                f"{primary_crop.lower()} price"
            ],
            "google_shopping": [
                "DAP fertilizer 50kg bag price",
                f"best hybrid {primary_crop.lower()} seeds price India"
            ],
            "google_maps": [
                f"APMC mandi market {district} {state}",
                f"agricultural cold storage warehouse {district}"
            ]
        }
