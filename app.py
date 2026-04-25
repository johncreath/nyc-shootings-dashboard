import os
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
            padding-top: 3rem;
            padding-bottom: 2rem;
        }

        @media (max-width: 640px) {
            .block-container {
                padding: 1rem 0.75rem 1.5rem;
            }

            h1, h2 {
                line-height: 1.15;
            }

            h2 {
                font-size: 1.45rem;
            }

            div[data-testid="stAltairChart"] {
                overflow-x: auto;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_ENV = os.getenv("APP_ENV", "PROD")

if APP_ENV.upper() != "PROD":
    st.warning(f"{APP_ENV} VERSION - This app is for testing only.")

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
    f"across hour of day, borough, weekday versus weekend, and broader time-of-day groupings."
)

with st.expander("Questions this dashboard can answer"):
    st.markdown(
        "- Which boroughs experience the highest levels of gun violence?\n"
        "- Do shooting patterns remain consistent across different times of day?\n"
        "- When normalized, do patterns emerge that differ from raw incident counts?\n"
        "- How do temporal patterns vary across boroughs?\n\n"
        "Click on the segmentation visuals to cross-filter the dashboard for deeper analysis."
    )

compact_control = st.toggle if hasattr(st, "toggle") else st.checkbox
compact_layout = compact_control(
    "Compact mobile layout",
    value=False,
    help="Stacks charts vertically and tightens chart sizing for smaller screens.",
)

dashboard_chart = make_dashboard_chart(
    base_df,
    borough_norm_df,
    day_norm_df,
    time_norm_df,
    compact=compact_layout,
)

st.altair_chart(dashboard_chart, use_container_width=True)

st.markdown("---")
st.markdown("## Author's Analysis")

with st.expander("Where do shootings occur?", expanded=True):
    st.markdown(
        f"At the raw incident level, **Brooklyn and the Bronx** record the highest number of shootings. "
        f"However, raw totals alone can be misleading because borough populations differ substantially. "
        f"When shootings are normalized on a per-capita basis, **the Bronx emerges as the borough with the highest concentration of gun violence**.\n\n"
        f"This suggests that shootings are not simply a function of population size, but are instead "
        f"disproportionately concentrated in specific geographies."
    )

with st.expander("Do shootings differ between weekdays and weekends?"):
    st.markdown(
        f"At first glance, total shootings appear higher on weekdays. That pattern is misleading, however, "
        f"because the dataset contains more weekdays than weekend days.\n\n"
        f"After normalizing by the number of days in each category, a different pattern emerges: "
        f"**shootings occur more frequently on weekends than on weekdays on an average per-day basis**.\n\n"
        f"This reinforces the importance of normalization. Without it, the apparent pattern in the raw counts "
        f"would lead to the wrong conclusion."
    )

with st.expander("Key takeaways"):
    st.markdown(
        f"Across multiple dimensions, a consistent pattern emerges:\n\n"
        f"- **Geographic concentration:** the Bronx stands out when shootings are viewed per capita\n\n"
        f"- **Temporal concentration:** shootings cluster more heavily during nighttime hours\n\n"
        f"- **Contextual concentration:** shootings occur more frequently on weekends after normalization\n\n"
        f"Taken together, these results suggest that shootings are not randomly distributed. Instead, they cluster "
        f"in identifiable high-risk contexts, particularly **weekend nights**.\n\n"
        f"These kinds of patterns can help support more targeted prevention and intervention strategies."
    )

with st.expander("Limitations and assumptions"):
    st.markdown(
        f"- This analysis does not account for population movement, such as nightlife-related travel between boroughs\n\n"
        f"- External influences such as weather, holidays, and major events are not included\n\n"
        f"- Broad time-of-day categories may obscure more granular temporal patterns\n\n"
        f"Future iterations of this work could incorporate these factors to produce a more refined view of when and where shootings occur."
    )

st.markdown(
    "---\n\n"
    "**Author:** John Creath  \n"
    "**Project:** NYC Shootings Dashboard  \n"
    "**Data Source:** NYPD shooting incident data  \n"
    "© 2026 John Creath. All rights reserved."
)
