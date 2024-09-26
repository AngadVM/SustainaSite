import streamlit as st
from random import choice
from time import sleep


def main():

    st.set_page_config(
        page_title="SustainaSite",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.html("<h1>Sustaina<span style='color: #2a9d8f'>Site</span></h1>")

    form()


def form():

    details = st.empty()

    with details:

        with st.form("Site Details"):

            st.markdown("## Renewable Energy Site Optimization")

            siteType = st.selectbox("Select Site Type", ["Solar", "Wind", "Hybrid"])
            location = st.text_input("Enter Location", value=choice(["Mumbai", "Paris", "New York", "Hong Kong", "Vienna"]))
            capacity = st.number_input("Enter Project Production Capacity (MW)", value=10)
            envTolerance = st.slider("Select Environmental Tolerance", min_value=0, max_value=100, value=0)
            gridProxi = st.slider("Select Grid Proximity Importance", min_value=0, max_value=100, value=0)
            landAvail = st.slider("Select Land Availability Importance", min_value=0, max_value=100, value=0)

            submitted = st.form_submit_button("Submit")

            if submitted:

                st.html(f"<h3>Site Details:</h3><div>Site Type: {siteType}</div><div>Location: {location}</div><div>Production Capacity: {capacity}</div><div>Environmental Tolerance: {envTolerance}</div><div>Grid Proximity: {gridProxi}</div><div>Land Availability: {landAvail}</div>")
                sleep(10)
                details.empty()
                return siteType, location, capacity, envTolerance, gridProxi, landAvail
            
    
if __name__ == "__main__":

    main()
            