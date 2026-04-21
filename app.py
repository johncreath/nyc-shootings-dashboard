import streamlit as st

from src.load_data import load_data
from src.prepare_data import (
    prepare_base_data,
    build_borough_norm_df,
    build_day_norm_df,
    build_time_norm_df,
)
from src.charts import make_dashboard_chart

st.set_page_config(page_title="New York City Shootings Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

raw_df = load_data()
base_df = prepare_base_data(raw_df)

years = base_df["OCCUR_DATE"].dropna().dt.year
min_year = years.min()
max_year = years.max()

borough_norm_df = build_borough_norm_df(base_df)
day_norm_df = build_day_norm_df(base_df)
time_norm_df = build_time_norm_df(base_df)

st.markdown("## New York City Shootings Time of Day Analysis")
st.markdown(
    f"Explore patterns in NYC shooting incidents from **{min_year} to {max_year}** "
    f"across hour of day, borough, weekday versus weekend, and broader time-of-day groupings. "
    f"The dashboard combines total incident counts with normalized metrics to support "
    f"fairer comparisons across geographies and time segments.\n\n"
    f"Click on segmentation visuals to cross-filter other visuals for deeper analysis."
)

st.altair_chart(
    make_dashboard_chart(
        base_df,
        borough_norm_df,
        day_norm_df,
        time_norm_df,
    ),
    use_container_width=False,
)
