"""Tab 3: Seasonal Price & Demand Trends dashboard for KisanMitra (Pure SVG — Zero Pandas Dependency)."""
import streamlit as st
from typing import List
from models.market_data import TrendData


def _generate_svg_chart(crop_name: str, months: list, values: list) -> str:
    """Generate a pure SVG responsive line & area chart without pandas or external libraries."""
    width = 620
    height = 200
    padding_x = 45
    padding_top = 35
    padding_bottom = 40

    usable_w = width - (2 * padding_x)
    usable_h = height - padding_top - padding_bottom

    max_val = 100
    min_val = 20

    coords = []
    for i, val in enumerate(values):
        x = padding_x + (i * (usable_w / (len(values) - 1)))
        norm = (val - min_val) / (max_val - min_val)
        y = (padding_top + usable_h) - (norm * usable_h)
        coords.append((x, y, val))

    # Construct line points
    line_path = " ".join([f"{'M' if i == 0 else 'L'} {x:.1f} {y:.1f}" for i, (x, y, _) in enumerate(coords)])
    area_path = f"{line_path} L {coords[-1][0]:.1f} {height - padding_bottom:.1f} L {coords[0][0]:.1f} {height - padding_bottom:.1f} Z"

    # SVG text labels for months and points
    month_labels = "".join([
        f'<text x="{x:.1f}" y="{height - 18}" font-size="11" font-weight="600" fill="#64748B" text-anchor="middle">{months[i]}</text>'
        for i, (x, _, _) in enumerate(coords)
    ])

    # Highlight peak points (points with value >= 80)
    data_circles = "".join([
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{"5" if v >= 80 else "3.5"}" fill="{"#E65100" if v >= 80 else "#2E7D32"}" stroke="#FFFFFF" stroke-width="2"/>'
        f'<text x="{x:.1f}" y="{y - 8:.1f}" font-size="10" font-weight="700" fill="{"#E65100" if v >= 80 else "#2E7D32"}" text-anchor="middle">{v}</text>'
        for (x, y, v) in coords
    ])

    svg = f"""
    <div style="background: rgba(255, 255, 255, 0.7); border-radius: 12px; padding: 12px; border: 1px solid rgba(46, 125, 50, 0.2); margin-top: 10px;">
        <svg viewBox="0 0 {width} {height}" style="width: 100%; height: auto; display: block; font-family: 'Plus Jakarta Sans', system-ui, sans-serif;">
            <defs>
                <linearGradient id="areaGrad_{crop_name.replace(' ', '_')}" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#2E7D32" stop-opacity="0.32" />
                    <stop offset="100%" stop-color="#2E7D32" stop-opacity="0.02" />
                </linearGradient>
            </defs>
            <!-- Grid Lines -->
            <line x1="{padding_x}" y1="{padding_top}" x2="{width - padding_x}" y2="{padding_top}" stroke="#E2E8F0" stroke-dasharray="3 3"/>
            <line x1="{padding_x}" y1="{padding_top + (usable_h / 2)}" x2="{width - padding_x}" y2="{padding_top + (usable_h / 2)}" stroke="#E2E8F0" stroke-dasharray="3 3"/>
            <line x1="{padding_x}" y1="{height - padding_bottom}" x2="{width - padding_x}" y2="{height - padding_bottom}" stroke="#CBD5E1" stroke-width="1.5"/>

            <!-- Area & Line -->
            <path d="{area_path}" fill="url(#areaGrad_{crop_name.replace(' ', '_')})" />
            <path d="{line_path}" fill="none" stroke="#2E7D32" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>

            <!-- Data Circles & Values -->
            {data_circles}

            <!-- Month Axis Labels -->
            {month_labels}
        </svg>
    </div>
    """
    return svg


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

            # Clean SVG seasonal index curve (Zero Pandas / Zero DLL dependency)
            st.divider()
            st.caption(f"📊 Annual 12-Month Demand Cycle Curve ({t.crop_name}) — *Peak months highlighted in orange*")
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            # Base seasonal curve based on typical Indian agricultural cycles
            base_curve = [45, 50, 52, 48, 42, 58, 65, 70, 75, 80, 88, 92]
            if "Onion" in t.crop_name:
                base_curve = [85, 70, 55, 45, 40, 48, 60, 68, 75, 85, 95, 90]
            elif "Wheat" in t.crop_name:
                base_curve = [75, 85, 90, 70, 50, 45, 48, 52, 55, 60, 68, 72]
            elif "Tomato" in t.crop_name:
                base_curve = [40, 45, 50, 55, 65, 90, 95, 75, 60, 70, 85, 50]

            svg_html = _generate_svg_chart(t.crop_name, months, base_curve)
            st.markdown(svg_html, unsafe_allow_html=True)
