import streamlit as st
from Modules.map import get_map
from Modules.landuse import get_land_use_map
from Modules.solar import get_radiation_map
from Modules.wind import get_wind_map
from Modules.final_map import create_ml_renewable_energy_map
import streamlit.components.v1 as components

def main():

    st.set_page_config(
        page_title="SustainaSite",
        page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMyYTlkOGYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1sZWFmeS1ncmVlbiI+PHBhdGggZD0iTTIgMjJjMS4yNS0uOTg3IDIuMjctMS45NzUgMy45LTIuMmE1LjU2IDUuNTYgMCAwIDEgMy44IDEuNSA0IDQgMCAwIDAgNi4xODctMi4zNTMgMy41IDMuNSAwIDAgMCAzLjY5LTUuMTE2QTMuNSAzLjUgMCAwIDAgMjAuOTUgOCAzLjUgMy41IDAgMSAwIDE2IDMuMDVhMy41IDMuNSAwIDAgMC01LjgzMSAxLjM3MyAzLjUgMy41IDAgMCAwLTUuMTE2IDMuNjkgNCA0IDAgMCAwLTIuMzQ4IDYuMTU1QzMuNDk5IDE1LjQyIDQuNDA5IDE2LjcxMiA0LjIgMTguMSAzLjkyNiAxOS43NDMgMy4wMTQgMjAuNzMyIDIgMjIiLz48cGF0aCBkPSJNMiAyMiAxNyA3Ii8+PC9zdmc+",
        layout="wide",
        initial_sidebar_state="expanded"
        
    )

    st.html("<img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMyYTlkOGYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1sZWFmeS1ncmVlbiI+PHBhdGggZD0iTTIgMjJjMS4yNS0uOTg3IDIuMjctMS45NzUgMy45LTIuMmE1LjU2IDUuNTYgMCAwIDEgMy44IDEuNSA0IDQgMCAwIDAgNi4xODctMi4zNTMgMy41IDMuNSAwIDAgMCAzLjY5LTUuMTE2QTMuNSAzLjUgMCAwIDAgMjAuOTUgOCAzLjUgMy41IDAgMSAwIDE2IDMuMDVhMy41IDMuNSAwIDAgMC01LjgzMSAxLjM3MyAzLjUgMy41IDAgMCAwLTUuMTE2IDMuNjkgNCA0IDAgMCAwLTIuMzQ4IDYuMTU1QzMuNDk5IDE1LjQyIDQuNDA5IDE2LjcxMiA0LjIgMTguMSAzLjkyNiAxOS43NDMgMy4wMTQgMjAuNzMyIDIgMjIiLz48cGF0aCBkPSJNMiAyMiAxNyA3Ii8+PC9zdmc+' style='width: 200px'><h1>Sustaina<span style='color: #2a9d8f'>Site</span></h1>")

    # Capture the form data
    form_data = det_form()

    # Proceed only if form_data is valid (i.e., form was submitted)
    if form_data:

        siteType, location, capacity, envTolerance, gridProxi, landAvail, scale = form_data

        st.markdown("## Site Details")
        st.markdown(f"Site Type: {siteType} | Location: {location} | Production Capacity: {capacity} | Environmental Tolerance: {envTolerance} | Grid Proximity: {gridProxi} | Land Availability: {landAvail}")

        # Save map image after form submission
        get_map(location, scale)
        get_land_use_map(location, scale)
        get_radiation_map(location, scale)
        get_wind_map(location, scale)

        col1, col2 = st.columns(2, gap="small")
        with col1:
            render_html(f'tmp/{location}_map.html', caption=f"Map of Site Location - {location}")
        with col2:
            render_html(f'tmp/{location}_land_use_map.html', caption=f"Land Use Map of Site Location - {location}")
      
        col3, col4 = st.columns(2, gap="small")
        with col3:
            render_html(f'tmp/{location}_radiation_map.html', caption=f"Radiation Map of Site Location - {location}")
        with col4:
            render_html(f'tmp/{location}_wind_map.html', caption=f"Wind Map of Site Location - {location}")

        st.markdown("---")

        st.markdown("## Identified Locations!")

        create_ml_renewable_energy_map(location, scale)
        render_html(f"tmp/{location}_ml_renewable_energy_map.html", caption='Potential Locations for {location}')

def det_form():

    details = st.empty()

    with details:
        with st.form("Site Details"):

            st.markdown("## Renewable Energy Site Optimization")

            siteType = st.selectbox("Select Site Type", ["Solar", "Wind", "Hybrid"])
            location = st.text_input("Enter Location", value="Mumbai")
            capacity = st.number_input("Enter Project Production Capacity (MW)", value=10)
            envTolerance = st.slider("Select Environmental Tolerance", min_value=0, max_value=100, value=0)
            gridProxi = st.slider("Select Grid Proximity Importance", min_value=0, max_value=100, value=0)
            landAvail = st.slider("Select Land Availability Importance", min_value=0, max_value=100, value=0)
            scale = st.slider("Select Map Scale", min_value=5, max_value=100, value=50)

            submitted = st.form_submit_button("Submit")

            if submitted:
                details.empty()
                return siteType, location, capacity, envTolerance, gridProxi, landAvail, scale

    return None

def render_html(path: str, caption: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:  # Ensure UTF-8 encoding is used
            html_data = f.read()
        components.html(html_data, width=800, height=800)
        st.caption(caption)
    except UnicodeDecodeError as e:
        st.error(f"Error reading the HTML file: {e}")


if __name__ == "__main__":
    main()
