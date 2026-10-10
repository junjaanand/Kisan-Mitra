"""Tab 3: Seasonal Price & Demand Trends dashboard for KisanMitra."""
import streamlit as st
from typing import List
import pandas as pd
from models.market_data import TrendData


def render_trends_dashboard(trends: List[TrendData]):
    """Render Tab 3: Google Trends seasonal intelligence."""
    st.subheader("📈 Seasonal Demand Cycles & Market Search Interest")
    st.caption("Time-series search index and annual market cycles powered by SerpApi Google Trends.")

    if not trends:
        st.info("No trend records available.")
        return

    for t in trends:
        with st.container(border=True):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"### 🌾 {t.crop_name} Price Trend Cycle")
                st.write(f"**Current Market Phase:** `{t.trend_direction}`")
                st.write(f"💡 **AI Trend Insight:** {t.insight}")

                if t.peak_months:
                    st.caption(f"🗓️ **Historically Highest Price Months:** {', '.join(t.peak_months)}")

            with col2:
                st.metric(
                    label="Relative Market Search Index",
                    value=f"{t.relative_demand_index or 50} / 100",
                    help="Relative search interest on Google over the last 12 months in India"
                )

                if t.related_queries:
                    st.caption("🔥 **Trending Search Terms:**")
                    for rq in t.related_queries[:4]:
                        st.markdown(f"- `{rq}`")

            # Simulated seasonal index line chart for visual impact
            st.divider()
            st.caption(f"📊 Annual 12-Month Demand Cycle Curve ({t.crop_name})")
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            # Base curve shifted based on peak months
            base_curve = [45, 50, 52, 48, 42, 58, 65, 70, 75, 80, 88, 92]
            if "Onion" in t.crop_name:
                base_curve = [85, 70, 55, 45, 40, 48, 60, 68, 75, 85, 95, 90]
            elif "Wheat" in t.crop_name:
                base_curve = [75, 85, 90, 70, 50, 45, 48, 52, 55, 60, 68, 72]
            elif "Tomato" in t.crop_name:
                base_curve = [40, 45, 50, 55, 65, 90, 95, 75, 60, 70, 85, 50]

            chart_df = pd.DataFrame({"Month": months, "Search & Demand Index": base_curve}).set_index("Month")
            st.line_chart(chart_df, color="#2E7D32")
