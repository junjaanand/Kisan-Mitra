"""Tab 5: Nearby Mandis & Storage Infrastructure dashboard for KisanMitra."""
import streamlit as st
from typing import List
from models.market_data import MandiInfo
from ui.components import render_mandi_card


def render_mandi_dashboard(mandis: List[MandiInfo]):
    """Render Tab 5: Nearby APMC Mandis and Warehouses."""
    st.subheader("📍 Nearby APMC Mandis, Sub-Yards & Cold Storages")
    st.caption("Locate physical auction yards, grain warehouses, and cold storages via SerpApi Google Maps.")

    if not mandis:
        st.info("No physical mandis or storage points detected in this vicinity.")
        return

    # Counts
    apmc_cnt = sum(1 for m in mandis if "APMC" in m.mandi_type or "Yard" in m.mandi_type)
    storage_cnt = sum(1 for m in mandis if "Cold" in m.mandi_type or "Warehouse" in m.mandi_type)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("🏢 APMC Market Yards", f"{apmc_cnt} Discovered")
    with c2:
        st.metric("❄️ Storage & Warehouses", f"{storage_cnt} Discovered")

    st.markdown("#### Trading Yards Directory")
    for mandi in mandis:
        render_mandi_card(mandi)
