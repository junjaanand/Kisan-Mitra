"""Tab 1: Live Mandi Wholesale Prices dashboard for KisanMitra."""
import streamlit as st
from typing import List
from models.market_data import CropPrice
from ui.components import render_price_card, render_metric_pill


def render_price_dashboard(prices: List[CropPrice]):
    """Render Tab 1: Live crop market prices."""
    st.subheader("💰 Live APMC Mandi Wholesale Rates")
    st.caption("Live auction and wholesale mandi prices retrieved via SerpApi Google Search.")

    if not prices:
        st.info("No price data found for the selected crops. Try selecting different crops.")
        return

    # Top summary metrics
    cols = st.columns(min(len(prices), 4))
    for i, p in enumerate(prices[:4]):
        with cols[i]:
            val_str = f"₹{p.price_per_quintal:,.0f}/q" if p.price_per_quintal else "Quote Pending"
            render_metric_pill(
                icon="🌾",
                label=f"{p.crop_name} ({p.recommendation.value})",
                value=val_str
            )

    st.markdown("#### Detailed Crop Quotations & Selling Recommendations")
    for price in prices:
        render_price_card(price)
