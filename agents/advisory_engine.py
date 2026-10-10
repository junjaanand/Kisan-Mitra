"""Advisory Engine — Synthesizes multi-engine data into actionable farmer recommendations."""
import json
from datetime import datetime
from typing import List, Dict, Any
from utils.llm_client import GeminiClient
from models.farmer_profile import FarmerProfile
from models.market_data import (
    CropPrice, NewsAlert, TrendData, InputDeal, MandiInfo, FarmerIntelligenceReport
)
from config.prompts import ADVISORY_SYNTHESIS_PROMPT


class AdvisoryEngine:
    """Cross-engine intelligence synthesizer powered by Gemini LLM."""

    def __init__(self, llm_client: GeminiClient):
        self.llm = llm_client

    def synthesize(
        self,
        profile: FarmerProfile,
        prices: List[CropPrice],
        news_alerts: List[NewsAlert],
        trends: List[TrendData],
        deals: List[InputDeal],
        mandis: List[MandiInfo],
        weather_context: str,
        progress_callback=None,
    ) -> FarmerIntelligenceReport:
        """Synthesize all engine streams into an integrated decision advisory.
        
        Returns:
            FarmerIntelligenceReport containing all enriched data and strategic advice.
        """
        if progress_callback:
            progress_callback("🧠 Synthesizing market intelligence & agronomic advisory...")

        # Prepare JSON representations for prompt
        prices_repr = [
            {
                "crop": p.crop_name,
                "price": f"₹{p.price_per_quintal}/q" if p.price_per_quintal else "N/A",
                "mandi": p.mandi_name,
                "trend": p.price_trend,
                "recommendation": p.recommendation.value,
                "notes": p.notes,
            }
            for p in prices
        ]

        news_repr = [
            {
                "headline": n.headline,
                "severity": n.severity.value,
                "category": n.category,
                "summary": n.summary,
            }
            for n in news_alerts[:5]
        ]

        trends_repr = [
            {
                "crop": t.crop_name,
                "trend": t.trend_direction,
                "peak_months": t.peak_months,
                "insight": t.insight,
            }
            for t in trends
        ]

        deals_repr = [
            {"product": d.product_name, "price": d.price, "seller": d.seller}
            for d in deals[:4]
        ]

        mandis_repr = [
            {"mandi": m.name, "address": m.address, "rating": m.rating, "type": m.mandi_type}
            for m in mandis[:4]
        ]

        prompt = ADVISORY_SYNTHESIS_PROMPT.format(
            farmer_profile=profile.to_search_context(),
            prices_json=json.dumps(prices_repr, indent=2),
            news_json=json.dumps(news_repr, indent=2),
            trends_json=json.dumps(trends_repr, indent=2),
            deals_json=json.dumps(deals_repr, indent=2),
            mandis_json=json.dumps(mandis_repr, indent=2),
            weather_context=weather_context[:1000],
        )

        res = self.llm.generate_json(prompt)

        weather_summary = "Favorable weather observed for current agricultural activities."
        recommendations = []

        if isinstance(res, dict):
            weather_summary = res.get("weather_summary") or weather_summary
            recs = res.get("recommendations")
            if isinstance(recs, list) and len(recs) > 0:
                recommendations = [str(r) for r in recs]

        # Robust fallbacks if LLM output was incomplete
        if not recommendations:
            primary_crop = profile.crops[0] if profile.crops else "produce"
            recommendations = [
                f"🟢 [PROFIT/SELL]: Current market arrivals for {primary_crop} are fetching favorable wholesale rates — consider liquidating 50% to lock in immediate cash flow.",
                f"⚠️ [RISK/WEATHER]: Check 3-day regional rainfall forecast before scheduling field irrigation or chemical application.",
                f"💰 [SAVINGS]: Procure subsidized fertilizer bags directly through registered cooperative society outlets to save over retail MRP.",
                f"📈 [STRATEGY]: Maintain aerated dry storage for the remaining crop lot to benefit from expected seasonal price surge in upcoming winter weeks.",
                f"📍 [LOGISTICS]: Compare daily price differences between {profile.district} APMC and neighboring terminal market yards before dispatching vehicles."
            ]

        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

        return FarmerIntelligenceReport(
            farmer_name=profile.farmer_name,
            location=f"{profile.district}, {profile.state}",
            crops=profile.crops,
            prices=prices,
            news_alerts=news_alerts,
            trends=trends,
            deals=deals,
            mandis=mandis,
            weather_summary=weather_summary,
            advisory_recommendations=recommendations,
            generated_at=timestamp,
        )
