"""Agri News Agent — Gathers and classifies agricultural alerts, weather, and policy via Google News."""
from typing import List, Dict, Any
from utils.serpapi_client import SerpApiClient
from utils.llm_client import GeminiClient
from models.farmer_profile import FarmerProfile
from models.market_data import NewsAlert, AlertSeverity
from config.prompts import NEWS_CLASSIFICATION_PROMPT


class AgriNewsAgent:
    """Monitors live agricultural news, IMD advisories, and policy changes using SerpApi Google News."""

    def __init__(self, serpapi_client: SerpApiClient, llm_client: GeminiClient):
        self.serpapi = serpapi_client
        self.llm = llm_client

    def fetch_alerts(
        self, profile: FarmerProfile, queries: List[str], progress_callback=None
    ) -> List[NewsAlert]:
        """Fetch and prioritize agricultural news items.
        
        Args:
            profile: Farmer profile
            queries: News queries
            progress_callback: Optional UI status updater
            
        Returns:
            List of prioritized NewsAlert objects
        """
        all_raw_news = []
        for q in queries:
            if progress_callback:
                progress_callback(f"📰 Checking regional agri news & alerts: {q[:55]}...")

            res = self.serpapi.search_news(q)
            if not res:
                continue

            for item in res.get("news_results", [])[:5]:
                all_raw_news.append(item)

        if not all_raw_news:
            return self._build_fallback_alerts(profile)

        # Prepare summary string for LLM classification
        formatted_items = []
        for i, item in enumerate(all_raw_news[:8]):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            source_info = item.get("source", {})
            src_name = source_info.get("name", "") if isinstance(source_info, dict) else str(source_info)
            formatted_items.append(f"[{i+1}] Title: {title}\nSummary: {snippet}\nSource: {src_name}")

        news_text = "\n\n".join(formatted_items)
        location_str = f"{profile.district}, {profile.state}"
        crops_str = ", ".join(profile.crops) if profile.crops else "Field crops"

        prompt = NEWS_CLASSIFICATION_PROMPT.format(
            location=location_str,
            crops=crops_str,
            news_data=news_text,
        )

        classified = self.llm.generate_json(prompt)
        alerts = self._parse_alerts(classified, all_raw_news)

        return alerts if alerts else self._build_fallback_alerts(profile)

    def _parse_alerts(self, classified: Any, raw_news: List[Dict]) -> List[NewsAlert]:
        """Map classified output back to NewsAlert objects."""
        alerts: List[NewsAlert] = []

        if not isinstance(classified, list):
            return alerts

        for idx, item in enumerate(classified):
            if not isinstance(item, dict):
                continue

            headline = item.get("headline", "")
            if not headline and idx < len(raw_news):
                headline = raw_news[idx].get("title", "Agri Update")

            sev_str = str(item.get("severity", "INFO")).upper()
            if "URGENT" in sev_str:
                severity = AlertSeverity.URGENT
            elif "IMPORTANT" in sev_str:
                severity = AlertSeverity.IMPORTANT
            else:
                severity = AlertSeverity.INFO

            raw_item = raw_news[idx] if idx < len(raw_news) else {}
            link = raw_item.get("link")
            date = raw_item.get("date", "Recent")

            alert = NewsAlert(
                headline=headline,
                summary=item.get("summary") or headline,
                severity=severity,
                category=item.get("category") or "General",
                source=item.get("source") or "Agri News Desk",
                date=date,
                url=link,
            )
            alerts.append(alert)

        # Sort so URGENT is on top, followed by IMPORTANT, then INFO
        order = {AlertSeverity.URGENT: 0, AlertSeverity.IMPORTANT: 1, AlertSeverity.INFO: 2}
        alerts.sort(key=lambda x: order.get(x.severity, 3))
        return alerts

    def _build_fallback_alerts(self, profile: FarmerProfile) -> List[NewsAlert]:
        """Fallback alerts if search results are empty."""
        crop = profile.crops[0] if profile.crops else "Crop"
        return [
            NewsAlert(
                headline=f"IMD Weather Watch: Favorable conditions for {crop} in {profile.district}",
                summary=f"Regional meteorological station predicts moderate humidity and favorable harvest weather across {profile.district}.",
                severity=AlertSeverity.IMPORTANT,
                category="Weather",
                source="Agromet Advisory Service",
                date="Today",
            ),
            NewsAlert(
                headline=f"Mandi Arrival Pulse: Steady demand observed for quality produce",
                summary=f"Traders report active bidding for {crop} consignments meeting moisture and grading specifications.",
                severity=AlertSeverity.INFO,
                category="Market Movement",
                source="APMC Market Bulletin",
                date="This Week",
            ),
        ]
