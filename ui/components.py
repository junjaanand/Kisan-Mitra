"""Reusable UI components for KisanMitra using native Streamlit containers."""
import streamlit as st
from config.constants import CROP_ICONS, SEVERITY_COLORS, RECOMMENDATION_COLORS
from models.market_data import CropPrice, NewsAlert, InputDeal, MandiInfo, TrendData


def render_metric_pill(icon: str, label: str, value: str):
    """Render a clean metric pill in a bordered container."""
    with st.container(border=True):
        st.caption(f"{icon} {label}")
        st.subheader(value)


def render_price_card(price: CropPrice):
    """Render a crop wholesale mandi price card."""
    with st.container(border=True):
        icon = CROP_ICONS.get(price.crop_name, "🌿")
        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            st.markdown(f"### {icon} {price.crop_name}")
            st.caption(f"📍 Market: **{price.mandi_name}**")
            if price.arrival_quantity:
                st.caption(f"📦 Daily Arrivals: {price.arrival_quantity}")

        with col2:
            if price.price_per_quintal:
                st.metric(
                    label="Wholesale Rate",
                    value=f"₹{price.price_per_quintal:,.0f} / q",
                    delta=f"{price.price_trend} Trend" if price.price_trend != "Stable" else "Stable",
                    delta_color="normal" if price.price_trend == "Rising" else ("inverse" if price.price_trend == "Falling" else "off")
                )
            else:
                st.info("Live quotes updating...")

        with col3:
            # Recommendation Badge
            rec_val = price.recommendation.value
            if rec_val == "SELL NOW":
                st.success(f"🟢 **{rec_val}**")
            elif rec_val == "HOLD":
                st.warning(f"🟠 **{rec_val}**")
            else:
                st.info(f"🔵 **{rec_val}**")

            st.caption(f"Confidence: {price.confidence}")

        # Price range and notes
        if price.min_price or price.max_price or price.notes:
            st.divider()
            c_sub1, c_sub2 = st.columns([2, 3])
            with c_sub1:
                if price.min_price and price.max_price:
                    st.caption(f"📊 Range: ₹{price.min_price:,.0f} — ₹{price.max_price:,.0f} per quintal")
            with c_sub2:
                if price.notes:
                    st.caption(f"💡 {price.notes}")

        if price.source_urls:
            with st.expander("🔗 Verified Data Sources"):
                for url in price.source_urls:
                    st.markdown(f"- [{url[:60]}...]({url})")


def render_alert_card(alert: NewsAlert):
    """Render an agricultural news alert card."""
    with st.container(border=True):
        col1, col2 = st.columns([5, 2])
        with col1:
            if alert.severity.value == "URGENT":
                st.markdown(f"🚨 **{alert.headline}**")
            elif alert.severity.value == "IMPORTANT":
                st.markdown(f"⚠️ **{alert.headline}**")
            else:
                st.markdown(f"ℹ️ **{alert.headline}**")
        with col2:
            st.caption(f"🏷️ {alert.category} | {alert.severity.value}")

        st.write(alert.summary)

        c_meta1, c_meta2 = st.columns([3, 1])
        with c_meta1:
            st.caption(f"📰 Source: {alert.source or 'Agri Bulletin'} | {alert.date or 'Today'}")
        with c_meta2:
            if alert.url:
                st.link_button("Read ↗", alert.url, use_container_width=True)


def render_deal_card(deal: InputDeal):
    """Render a farm input shopping deal card."""
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 4, 2])
        with col1:
            if deal.thumbnail:
                st.image(deal.thumbnail, width=65)
            else:
                st.markdown("📦")

        with col2:
            st.markdown(f"**{deal.product_name}**")
            st.caption(f"🏷️ {deal.category} • Seller: {deal.seller or 'Authorized Vendor'}")
            if deal.savings_hint:
                st.caption(f"💡 *{deal.savings_hint}*")

        with col3:
            st.subheader(deal.price or "Check Rate")
            if deal.rating:
                st.caption(f"⭐ {deal.rating:.1f}/5.0")
            if deal.url:
                st.link_button("View Offer 🛒", deal.url, use_container_width=True)


def render_mandi_card(mandi: MandiInfo):
    """Render a physical mandi/warehouse local card."""
    with st.container(border=True):
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"### 📍 {mandi.name}")
            st.caption(f"🏢 Type: **{mandi.mandi_type}**")
            if mandi.address:
                st.write(mandi.address)
            if mandi.phone:
                st.caption(f"📞 Contact: {mandi.phone}")

        with col2:
            if mandi.rating:
                st.metric(label="Trader Rating", value=f"{mandi.rating} ⭐", delta=f"{mandi.reviews_count or 0} reviews")
            if mandi.open_status:
                st.caption(f"🕒 {mandi.open_status}")
            if mandi.link:
                st.link_button("Open Maps 🗺️", mandi.link, use_container_width=True)
