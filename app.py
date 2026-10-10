"""Main Streamlit Application for KisanMitra — AI Farming Intelligence Partner."""
import streamlit as st
import textwrap
from dotenv import load_dotenv

from models.farmer_profile import FarmerProfile
from agents.orchestrator import KisanMitraOrchestrator
from ui.farmer_form import render_farmer_form
from ui.price_dashboard import render_price_dashboard
from ui.news_dashboard import render_news_dashboard
from ui.trends_dashboard import render_trends_dashboard
from ui.deals_dashboard import render_deals_dashboard
from ui.mandi_dashboard import render_mandi_dashboard
from ui.sidebar import render_sidebar

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="KisanMitra — AI Farming Intelligence Partner",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Forest Green & Agriculture Palette)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .hero-container {
        text-align: center;
        padding: 2.2rem 1.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.12) 0%, rgba(255, 143, 0, 0.08) 100%);
        border: 1px solid rgba(46, 125, 50, 0.25);
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2E7D32 0%, #388E3C 50%, #E65100 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #4A5568;
        font-weight: 500;
        max-width: 820px;
        margin: 0 auto 1.4rem auto;
        line-height: 1.6;
    }

    .stat-pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        margin: 0.25rem 0.4rem;
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(46, 125, 50, 0.3);
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #1B5E20;
    }

    .advisory-box {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.08) 0%, rgba(21, 101, 192, 0.05) 100%);
        border-left: 5px solid #2E7D32;
        padding: 1.4rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def render_hero():
    """Render the landing hero header."""
    hero_html = textwrap.dedent("""
    <div class="hero-container">
        <div style="font-size: 3.2rem; margin-bottom: 0.3rem;">🌾</div>
        <h1 class="hero-title">KISANMITRA (किसानमित्र)</h1>
        <p class="hero-subtitle">
            AI-Powered Agricultural Intelligence for India's 150 Million Farmers.<br/>
            Real-time APMC Mandi rates, weather advisories, 12-month demand trends, input deals, and nearby trading yards.
        </p>
        <div>
            <span class="stat-pill">🌱 150M+ Farmers</span>
            <span class="stat-pill">🏢 7,000+ Mandis</span>
            <span class="stat-pill">⚡ 5 SerpApi Engines</span>
            <span class="stat-pill">🧠 Gemini Multi-Agent</span>
        </div>
    </div>
    """)
    st.markdown(hero_html, unsafe_allow_html=True)


def main():
    # Render Sidebar
    render_sidebar()

    # Render Hero
    render_hero()

    # Render Profile Form
    profile = render_farmer_form()

    # Execute pipeline when form is submitted
    if profile:
        progress_placeholder = st.empty()

        def update_progress(msg: str):
            progress_placeholder.info(f"⏳ **Live Pipeline:** {msg}")

        try:
            with st.spinner("Harvesting real-time market data across 5 SerpApi search engines..."):
                orchestrator = KisanMitraOrchestrator()
                report = orchestrator.run(profile, progress_callback=update_progress)
                st.session_state["report"] = report
                progress_placeholder.success("✅ **Intelligence harvest complete!** Scroll down to explore your dashboard.")
        except Exception as e:
            progress_placeholder.error(f"❌ Error during intelligence generation: {e}")

    # Display Report if available in session
    if "report" in st.session_state:
        report = st.session_state["report"]

        st.markdown("---")
        st.markdown(f"## 📊 Comprehensive Market Intelligence Report")
        st.caption(f"👤 **Farmer:** {report.farmer_name} | 📍 **Region:** {report.location} | 🌱 **Crops:** {', '.join(report.crops)} | 🗓️ **Generated:** {report.generated_at}")

        # Top Executive Advisory Callout
        st.markdown("### 🧠 Executive Decision Advisory")
        with st.container(border=True):
            if report.weather_summary:
                st.markdown(f"**🌦️ Regional Agromet & Weather Outlook:**  \n*{report.weather_summary}*")
                st.divider()

            st.markdown("#### 🎯 Priority Recommendations:")
            for rec in report.advisory_recommendations:
                st.markdown(f"- {rec}")

        # 5 Tabbed Dashboards
        t1, t2, t3, t4, t5 = st.tabs([
            "💰 Mandi Prices",
            "📰 Agri News & Alerts",
            "📈 Seasonal Demand Trends",
            "🛒 Smart Input Deals",
            "📍 Mandi Infrastructure"
        ])

        with t1:
            render_price_dashboard(report.prices)

        with t2:
            render_news_dashboard(report.news_alerts)

        with t3:
            render_trends_dashboard(report.trends)

        with t4:
            render_deals_dashboard(report.deals)

        with t5:
            render_mandi_dashboard(report.mandis)

        # Export & Download Report
        st.markdown("---")
        st.markdown("### 📥 Export Agricultural Advisory Report")
        
        report_text = f"""=======================================================
KISANMITRA — AGRICULTURAL INTELLIGENCE REPORT
=======================================================
Farmer Name: {report.farmer_name}
Location: {report.location}
Crops: {', '.join(report.crops)}
Generated At: {report.generated_at}

WEATHER OUTLOOK:
{report.weather_summary}

STRATEGIC DECISION ADVISORY:
"""
        for r in report.advisory_recommendations:
            report_text += f"{r}\n"

        report_text += "\n-------------------------------------------------------\nLIVE CROP WHOLESALE QUOTES:\n"
        for p in report.prices:
            val = f"Rs.{p.price_per_quintal}/q" if p.price_per_quintal else "Quote Pending"
            report_text += f"- {p.crop_name}: {val} at {p.mandi_name} | Action: {p.recommendation.value} | Trend: {p.price_trend}\n"

        report_text += "\n-------------------------------------------------------\nNEARBY APMC MANDIS & WAREHOUSES:\n"
        for m in report.mandis[:4]:
            report_text += f"- {m.name} ({m.mandi_type}): {m.address} | Rating: {m.rating}*\n"

        report_text += "\n=======================================================\nPowered by SerpApi 5-Engine Intelligence (Search, News, Trends, Shopping, Maps)\n"

        st.download_button(
            label="📄 Download Farm Advisory Report (.txt)",
            data=report_text,
            file_name=f"kisanmitra_advisory_{report.farmer_name.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
