"""Farmer profile form component with one-click demo personas."""
import streamlit as st
from models.farmer_profile import FarmerProfile, Season, IrrigationType
from config.constants import INDIAN_STATES, STATE_DISTRICTS, MAJOR_CROPS, DEMO_PERSONAS


def render_farmer_form() -> FarmerProfile | None:
    """Render the profile input form and return a validated FarmerProfile on submit."""
    st.subheader("👨‍🌾 Farmer & Landholding Profile")

    # One-click demo personas
    st.markdown("##### ⚡ Quick Load Demo Profiles")
    cols = st.columns(len(DEMO_PERSONAS))

    for idx, (label, data) in enumerate(DEMO_PERSONAS.items()):
        with cols[idx]:
            if st.button(label, key=f"demo_{idx}", use_container_width=True):
                st.session_state["farmer_name"] = data["farmer_name"]
                st.session_state["state"] = data["state"]
                st.session_state["district"] = data["district"]
                st.session_state["crops"] = data["crops"]
                st.session_state["farm_size"] = data["farm_size_acres"]
                st.session_state["season"] = data["season"]
                st.session_state["irrigation"] = data["irrigation"]
                st.rerun()

    with st.form("farmer_profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            farmer_name = st.text_input(
                "Farmer Name",
                value=st.session_state.get("farmer_name", "Rajesh Patil"),
                help="Enter your name or farm enterprise name"
            )

            current_state = st.session_state.get("state", "Maharashtra")
            state_idx = INDIAN_STATES.index(current_state) if current_state in INDIAN_STATES else 0
            state = st.selectbox("State / Union Territory", INDIAN_STATES, index=state_idx)

            # Dynamic district list based on selected state
            districts_list = STATE_DISTRICTS.get(state, ["Main District", "Rural District", "Other"])
            curr_district = st.session_state.get("district", "Nashik")
            dist_idx = districts_list.index(curr_district) if curr_district in districts_list else 0
            district = st.selectbox("District / Agri Region", districts_list, index=dist_idx)

        with col2:
            default_crops = st.session_state.get("crops", ["Onion", "Tomato"])
            crops = st.multiselect(
                "Primary Crops Cultivated",
                MAJOR_CROPS,
                default=[c for c in default_crops if c in MAJOR_CROPS] or ["Onion", "Tomato"],
                help="Select crops from the catalog or type any additional custom crop below"
            )

            custom_crop_input = st.text_input(
                "➕ Type Any Other / Custom Crop(s)",
                placeholder="e.g. Cumin, Cardamom, Apple, Barley (comma-separated)",
                help="Type any crop name here if it's not present in the dropdown list above"
            )

            farm_size = st.number_input(
                "Landholding Size (Acres)",
                min_value=0.5,
                max_value=100.0,
                value=float(st.session_state.get("farm_size", 2.5)),
                step=0.5
            )

            season_options = [s.value for s in Season]
            curr_season = st.session_state.get("season", Season.RABI.value)
            season_idx = season_options.index(curr_season) if curr_season in season_options else 1
            season_str = st.selectbox("Current Cropping Season", season_options, index=season_idx)
            season_enum = next((s for s in Season if s.value == season_str), Season.RABI)

        irrigation_options = [i.value for i in IrrigationType]
        curr_irrigation = st.session_state.get("irrigation", IrrigationType.CANAL_TUBEWELL.value)
        irr_idx = irrigation_options.index(curr_irrigation) if curr_irrigation in irrigation_options else 0
        irrigation_str = st.radio(
            "Primary Irrigation Source",
            irrigation_options,
            index=irr_idx,
            horizontal=True
        )
        irrigation_enum = next((i for i in IrrigationType if i.value == irrigation_str), IrrigationType.CANAL_TUBEWELL)

        submitted = st.form_submit_button(
            "🌾 Generate Live Agricultural Intelligence",
            type="primary",
            use_container_width=True
        )

        if submitted:
            # Combine selected dropdown crops with custom typed crops
            final_crops = list(crops)
            if custom_crop_input:
                custom_list = [c.strip().title() for c in custom_crop_input.split(",") if c.strip()]
                for c in custom_list:
                    if c not in final_crops:
                        final_crops.append(c)

            if not final_crops:
                st.error("Please select or type at least one crop to analyze.")
                return None

            return FarmerProfile(
                farmer_name=farmer_name,
                state=state,
                district=district,
                crops=final_crops,
                farm_size_acres=farm_size,
                season=season_enum,
                irrigation=irrigation_enum
            )

    return None
