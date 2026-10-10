"""KisanMitra Orchestrator — Coordinates 7 agents across 5 SerpApi engines into a unified intelligence report."""
from typing import Optional, Callable
from models.farmer_profile import FarmerProfile
from models.market_data import FarmerIntelligenceReport
from utils.serpapi_client import SerpApiClient
from utils.llm_client import GeminiClient

from agents.query_strategist import QueryStrategistAgent
from agents.market_price_agent import MarketPriceAgent
from agents.agri_news_agent import AgriNewsAgent
from agents.trend_analyst_agent import TrendAnalystAgent
from agents.smart_deals_agent import SmartDealsAgent
from agents.mandi_locator_agent import MandiLocatorAgent
from agents.advisory_engine import AdvisoryEngine


class KisanMitraOrchestrator:
    """Master orchestrator for the 5-engine agricultural intelligence pipeline."""

    def __init__(self):
        self.serpapi = SerpApiClient()
        self.llm = GeminiClient()

        # Initialize all 7 agents
        self.query_strategist = QueryStrategistAgent(self.llm)
        self.price_agent = MarketPriceAgent(self.serpapi, self.llm)
        self.news_agent = AgriNewsAgent(self.serpapi, self.llm)
        self.trends_agent = TrendAnalystAgent(self.serpapi, self.llm)
        self.deals_agent = SmartDealsAgent(self.serpapi)
        self.mandi_agent = MandiLocatorAgent(self.serpapi)
        self.advisory_engine = AdvisoryEngine(self.llm)

    def run(
        self,
        profile: FarmerProfile,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> FarmerIntelligenceReport:
        """Run the end-to-end multi-agent intelligence pipeline.
        
        Pipeline:
        1. Formulate Search Strategies for 5 engines
        2. Google Search -> Live Mandi Rates & Weather
        3. Google News -> Agricultural Risk Alerts
        4. Google Trends -> Demand Patterns & Seasonal Cycles
        5. Google Shopping -> Subsidized & Retail Input Deals
        6. Google Maps -> Physical Mandi Infrastructure
        7. Gemini LLM -> Integrated Actionable Advisory
        """
        def update(msg: str):
            if progress_callback:
                progress_callback(msg)

        # Step 1: Formulate targeted queries for 5 engines
        update("🧠 [Agent 1/7] Formulating targeted queries across 5 search engines...")
        strategy = self.query_strategist.generate_strategy(profile)
        update(f"✅ Generated queries for Search, News, Trends, Shopping & Maps")

        # Step 2: Live APMC Mandi Prices & Weather via Google Search
        update("🔍 [Agent 2/7] Fetching live mandi prices & weather via Google Search...")
        search_queries = strategy.get("google_search", [])[:3]
        prices, weather_context = self.price_agent.fetch_prices_and_weather(
            profile, search_queries, progress_callback=update
        )
        update(f"✅ Discovered live prices for {len(prices)} crop categories")

        # Step 3: Agri News & Risk Alerts via Google News
        update("📰 [Agent 3/7] Scanning breaking news, weather & pest alerts via Google News...")
        news_queries = strategy.get("google_news", [])[:2]
        news_alerts = self.news_agent.fetch_alerts(
            profile, news_queries, progress_callback=update
        )
        update(f"✅ Verified {len(news_alerts)} regional agricultural bulletins")

        # Step 4: Seasonal Demand Cycles via Google Trends
        update("📈 [Agent 4/7] Tracking seasonal search interest & cycles via Google Trends...")
        trend_queries = strategy.get("google_trends", [])[:2]
        trends = self.trends_agent.analyze_trends(
            profile, trend_queries, progress_callback=update
        )
        update(f"✅ Mapped demand cycles for {len(trends)} crops")

        # Step 5: Farm Input Deals via Google Shopping
        update("🛒 [Agent 5/7] Comparing fertilizer, seed & equipment deals via Google Shopping...")
        shop_queries = strategy.get("google_shopping", [])[:2]
        deals = self.deals_agent.fetch_deals(
            profile, shop_queries, progress_callback=update
        )
        update(f"✅ Found {len(deals)} verified farming input offers")

        # Step 6: Mandi Yards & Cold Storage via Google Maps
        update("📍 [Agent 6/7] Locating physical APMC yards & warehouses via Google Maps...")
        maps_queries = strategy.get("google_maps", [])[:2]
        mandis = self.mandi_agent.locate_mandis(
            profile, maps_queries, progress_callback=update
        )
        update(f"✅ Located {len(mandis)} regional trading yards and cold storages")

        # Step 7: Advisory Synthesis via Gemini LLM
        update("🌾 [Agent 7/7] Synthesizing comprehensive intelligence report with Gemini AI...")
        report = self.advisory_engine.synthesize(
            profile=profile,
            prices=prices,
            news_alerts=news_alerts,
            trends=trends,
            deals=deals,
            mandis=mandis,
            weather_context=weather_context,
            progress_callback=update,
        )
        update("🎉 Market intelligence report generated successfully!")

        return report
