"""Tab 4: Smart Farming Input Deals dashboard for KisanMitra."""
import streamlit as st
from typing import List
from models.market_data import InputDeal
from ui.components import render_deal_card


def render_deals_dashboard(deals: List[InputDeal]):
    """Render Tab 4: Google Shopping farming input deals."""
    st.subheader("🛒 Best Deals on Farming Inputs & Equipment")
    st.caption("Compare prices on fertilizers, hybrid seeds, and sprayers via SerpApi Google Shopping.")

    if not deals:
        st.info("No input deals available.")
        return

    # Filter categories
    categories = list(set([d.category for d in deals]))
    categories.insert(0, "All Categories")

    selected_cat = st.selectbox("Filter Input Category", categories)

    filtered_deals = deals if selected_cat == "All Categories" else [d for d in deals if d.category == selected_cat]

    st.markdown(f"#### Showing {len(filtered_deals)} Verified Offers")
    for deal in filtered_deals:
        render_deal_card(deal)
