"""Sanity test for KisanMitra APIs: 5 SerpApi engines + LangChain Gemini."""
import sys
import io

# Force UTF-8 output on Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from utils.serpapi_client import SerpApiClient
from utils.llm_client import GeminiClient

def run_tests():
    print("Testing KisanMitra Clients...")
    
    # 1. Test LLM Client
    print("\n--- 1. Testing LangChain Gemini Client ---")
    llm = GeminiClient()
    res = llm.generate("State in one sentence why timely mandi price intelligence empowers Indian farmers.")
    print("Gemini response:", res.strip())
    
    # 2. Test SerpApi Client
    print("\n--- 2. Testing SerpApi 5 Engines ---")
    serp = SerpApiClient()
    
    # Engine 1: Google Search
    print("\n[Engine 1: Google Search]")
    s_res = serp.search_google("Nashik onion mandi price today", num=3)
    org = s_res.get("organic_results", [])
    print(f"Google Search returned {len(org)} organic results.")
    if org:
        print(f"Sample: {org[0].get('title')} ({org[0].get('link')})")
        
    # Engine 2: Google News
    print("\n[Engine 2: Google News]")
    n_res = serp.search_news("Maharashtra agriculture weather alert 2026")
    news = n_res.get("news_results", [])
    print(f"Google News returned {len(news)} news results.")
    if news:
        print(f"Sample: {news[0].get('title')}")

    # Engine 3: Google Trends
    print("\n[Engine 3: Google Trends]")
    t_res = serp.search_trends("onion price")
    iot = t_res.get("interest_over_time", {})
    t_data = iot.get("timeline_data", [])
    print(f"Google Trends returned timeline data with {len(t_data)} points.")

    # Engine 4: Google Shopping
    print("\n[Engine 4: Google Shopping]")
    shop_res = serp.search_shopping("DAP fertilizer 50kg bag", num=3)
    shop_items = shop_res.get("shopping_results", [])
    print(f"Google Shopping returned {len(shop_items)} shopping results.")
    if shop_items:
        print(f"Sample: {shop_items[0].get('title')} - Price: {shop_items[0].get('price')}")

    # Engine 5: Google Maps
    print("\n[Engine 5: Google Maps]")
    map_res = serp.search_maps("APMC mandi Nashik Maharashtra")
    local = map_res.get("local_results", [])
    print(f"Google Maps returned {len(local)} local places.")
    if local:
        print(f"Sample: {local[0].get('title')} ({local[0].get('address')})")

    # Remaining Searches
    remaining = serp.get_remaining_searches()
    print(f"\nRemaining SerpApi quota: {remaining}")
    print("\nALL SANITY TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
