"""Sidebar component for KisanMitra showing SerpApi engine diagnostics and project metadata."""
import streamlit as st
import os
from utils.serpapi_client import SerpApiClient


def render_sidebar():
    """Render the sidebar with SerpApi engine status and hackathon alignment."""
    with st.sidebar:
        st.markdown("### 🌾 KisanMitra (किसानमित्र)")
        st.caption("AI-Powered Agricultural Intelligence")

        st.markdown("---")

        # Track Alignment
        with st.container(border=True):
            st.markdown("🎯 **Track**")
            st.write("**Commerce & Market Intelligence**")
            st.caption("Connecting 150M Indian farmers to real-time wholesale commerce and input markets.")

        # SerpApi Engine Diagnostics
        st.markdown("---")
        st.markdown("🔌 **SerpApi 5-Engine Status**")

        serp_key = os.getenv("SERPAPI_API_KEY")
        if serp_key:
            st.success("API Key Configured")
        else:
            st.error("API Key Missing")

        with st.container(border=True):
            st.markdown("🟢 **Google Search**  \n`Live Mandi Rates & Agromet`")
            st.markdown("🟢 **Google News**  \n`Pest, Policy & Weather Alerts`")
            st.markdown("🟢 **Google Trends**  \n`12-Month Seasonal Demand`")
            st.markdown("🟢 **Google Shopping**  \n`Fertilizer & Seed Price Deals`")
            st.markdown("🟢 **Google Maps**  \n`Nearby APMC Yards & Storages`")

        # Quota Check
        try:
            client = SerpApiClient()
            rem = client.get_remaining_searches()
            if rem is not None:
                st.metric("Searches Left", f"{rem}")
        except Exception:
            pass

        st.markdown("---")

        # Hackathon metadata
        with st.container(border=True):
            st.caption("Built for **SerpApi India Hackathon 2026**")
            st.caption("Architecture: 7 AI Agents • 5 Search Engines • Gemini LLM")

        # Reset button
        if st.button("🔄 Reset App & Cache", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
