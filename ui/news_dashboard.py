"""Tab 2: Agri News, Weather Advisories & Risk Alerts dashboard for KisanMitra."""
import streamlit as st
from typing import List
from models.market_data import NewsAlert
from ui.components import render_alert_card


def render_news_dashboard(news_alerts: List[NewsAlert]):
    """Render Tab 2: Agricultural news alerts and bulletins."""
    st.subheader("📰 Regional Agriculture News & Risk Bulletins")
    st.caption("Live alerts on weather changes, pest notices, and farmer welfare policies retrieved via SerpApi Google News.")

    if not news_alerts:
        st.info("No regional news alerts detected for this area.")
        return

    # Counts
    urgent_cnt = sum(1 for a in news_alerts if a.severity.value == "URGENT")
    important_cnt = sum(1 for a in news_alerts if a.severity.value == "IMPORTANT")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🚨 Urgent Advisories", f"{urgent_cnt} Active")
    with c2:
        st.metric("⚠️ Important Notices", f"{important_cnt} Active")
    with c3:
        st.metric("ℹ️ General Bulletins", f"{len(news_alerts) - urgent_cnt - important_cnt} Recorded")

    st.markdown("#### Classified Alerts Feed")
    for alert in news_alerts:
        render_alert_card(alert)
