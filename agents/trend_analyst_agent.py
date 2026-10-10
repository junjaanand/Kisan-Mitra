"""Trend Analyst Agent — Analyzes seasonal demand cycles & search interest via Google Trends."""
from typing import List, Dict, Any
from utils.serpapi_client import SerpApiClient
from utils.llm_client import GeminiClient
from models.farmer_profile import FarmerProfile
from models.market_data import TrendData


class TrendAnalystAgent:
    """Evaluates time-series search interest and seasonal price patterns using SerpApi Google Trends."""

    def __init__(self, serpapi_client: SerpApiClient, llm_client: GeminiClient):
        self.serpapi = serpapi_client
        self.llm = llm_client

    def analyze_trends(
        self, profile: FarmerProfile, queries: List[str], progress_callback=None
    ) -> List[TrendData]:
        """Fetch trends data and generate seasonal insights.
        
        Args:
            profile: Farmer profile
            queries: Trends keywords (e.g. ['onion price', 'tomato price'])
            progress_callback: Optional UI status updater
            
        Returns:
            List of TrendData models
        """
        results: List[TrendData] = []

        for q in queries[:2]:
            if progress_callback:
                progress_callback(f"📈 Analyzing seasonal demand trend: {q}...")

            clean_term = q.lower().strip()
            res = self.serpapi.search_trends(clean_term)

            iot = res.get("interest_over_time", {})
            timeline = iot.get("timeline_data", [])

            # Extract related queries if available
            related_items = []
            for rq in res.get("related_queries", {}).get("rising", [])[:4]:
                q_text = rq.get("query", "")
                if q_text:
                    related_items.append(q_text)

            # Analyze points
            recent_score = 50
            if timeline:
                try:
                    last_point = timeline[-1]
                    vals = last_point.get("values", [])
                    if vals:
                        recent_score = int(vals[0].get("extracted_value", 50))
                except Exception:
                    recent_score = 50

            crop_name = q.replace("price", "").strip().title()
            if not crop_name:
                crop_name = profile.crops[0] if profile.crops else "Crop"

            # Determine direction from scores
            if recent_score > 65:
                direction = "Rising (High Consumer & Market Interest)"
            elif recent_score < 35:
                direction = "Low Season / Stable Wholesale Flow"
            else:
                direction = "Moderate / Seasonal Average"

            # Synthesize insight using LLM
            prompt = (
                f"You are an agricultural market trends analyst. "
                f"In India, the Google search trend for '{q}' currently scores {recent_score}/100. "
                f"Related queries include: {', '.join(related_items) if related_items else 'regional mandi rates'}. "
                f"In 2 sentences, explain what this means for a farmer in {profile.state} "
                f"regarding harvest selling timing and peak price months."
            )
            insight_text = self.llm.generate(prompt)
            if not insight_text:
                insight_text = (
                    f"Consumer and wholesale interest for {crop_name} is currently at index {recent_score}/100. "
                    f"Historical patterns show seasonal price surges ahead of festive periods and monsoon shifts."
                )

            # Peak months heuristic based on crop
            peak_months = self._get_typical_peak_months(crop_name)

            results.append(
                TrendData(
                    crop_name=crop_name,
                    trend_direction=direction,
                    peak_months=peak_months,
                    insight=insight_text.strip(),
                    relative_demand_index=recent_score,
                    related_queries=related_items if related_items else [f"{crop_name.lower()} mandi rate", f"{crop_name.lower()} today wholesale"],
                )
            )

        if not results:
            primary_crop = profile.crops[0] if profile.crops else "Produce"
            results.append(
                TrendData(
                    crop_name=primary_crop,
                    trend_direction="Active Seasonal Cycle",
                    peak_months=["November", "December", "January"],
                    insight=f"Search demand for {primary_crop} typically gains momentum in winter months as market arrivals fluctuate.",
                    relative_demand_index=62,
                    related_queries=[f"{primary_crop.lower()} wholesale price", f"{primary_crop.lower()} mandi rate"],
                )
            )

        return results

    def _get_typical_peak_months(self, crop: str) -> List[str]:
        """Standard Indian agricultural peak price cycles."""
        c = crop.lower()
        if "onion" in c:
            return ["November", "December", "January"]
        elif "tomato" in c:
            return ["June", "July", "November"]
        elif "potato" in c:
            return ["September", "October", "November"]
        elif "wheat" in c:
            return ["January", "February", "March"]
        elif "soybean" in c:
            return ["July", "August", "September"]
        elif "cotton" in c:
            return ["February", "March", "April"]
        return ["Post-harvest peak months"]
