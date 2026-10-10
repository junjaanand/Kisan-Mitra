"""End-to-end test script for KisanMitra orchestrator."""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from models.farmer_profile import FarmerProfile, Season, IrrigationType
from agents.orchestrator import KisanMitraOrchestrator

def test_full_pipeline():
    print("Testing KisanMitra Full Multi-Agent Pipeline...")

    profile = FarmerProfile(
        farmer_name="Rajesh Patil",
        state="Maharashtra",
        district="Nashik",
        crops=["Onion", "Tomato"],
        farm_size_acres=2.5,
        season=Season.RABI,
        irrigation=IrrigationType.CANAL_TUBEWELL
    )

    print(f"\nFarmer: {profile.farmer_name} ({profile.district}, {profile.state})")
    print(f"Crops: {profile.crops}")

    orchestrator = KisanMitraOrchestrator()

    report = orchestrator.run(profile, progress_callback=lambda msg: print(f"-> {msg}"))

    print("\n================== PIPELINE REPORT ==================")
    print(f"Farmer: {report.farmer_name} | Location: {report.location}")
    print(f"Weather: {report.weather_summary}\n")

    print(f"--- 1. CROP PRICES ({len(report.prices)}) ---")
    for p in report.prices:
        p_val = f"Rs.{p.price_per_quintal}/q" if p.price_per_quintal else "N/A"
        print(f"[{p.crop_name}] Price: {p_val} | Mandi: {p.mandi_name} | Rec: {p.recommendation.value}")

    print(f"\n--- 2. NEWS ALERTS ({len(report.news_alerts)}) ---")
    for n in report.news_alerts[:3]:
        print(f"[{n.severity.value}] {n.headline} ({n.category})")

    print(f"\n--- 3. TRENDS ({len(report.trends)}) ---")
    for t in report.trends:
        print(f"[{t.crop_name}] Dir: {t.trend_direction} | Peak: {t.peak_months}")

    print(f"\n--- 4. INPUT DEALS ({len(report.deals)}) ---")
    for d in report.deals[:3]:
        print(f"[{d.category}] {d.product_name} - Price: {d.price} ({d.seller})")

    print(f"\n--- 5. MANDIS & INFRASTRUCTURE ({len(report.mandis)}) ---")
    for m in report.mandis[:3]:
        print(f"[{m.mandi_type}] {m.name} - Rating: {m.rating}* ({m.address})")

    print("\n--- 6. ACTIONABLE RECOMMENDATIONS ---")
    for rec in report.advisory_recommendations:
        print(f"{rec}")

    print("\n=====================================================")
    print("PIPELINE TEST PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_pipeline()
