import numpy as np
import pandas as pd
import streamlit as st


BOROUGH_POPULATION = {
    "Bronx": 1_400_000,
    "Brooklyn": 2_700_000,
    "Manhattan": 1_600_000,
    "Queens": 2_400_000,
    "Staten Island": 500_000,
}

TIME_GROUP_SORT = ["Morning", "Afternoon", "Evening", "Night"]


def hour_order(hour):
    if pd.isna(hour):
        return None
    return (int(hour) - 7) % 24


def hour_label(hour):
    if pd.isna(hour):
        return None
    hour = int(hour)
    if hour == 0:
        return "12 AM"
    if hour < 12:
        return f"{hour} AM"
    if hour == 12:
        return "12 PM"
    return f"{hour - 12} PM"


@st.cache_data(show_spinner=False)
def prepare_base_data(df):
    df = df.copy()

    if "OCCUR_DATE" in df.columns:
        df["OCCUR_DATE"] = pd.to_datetime(df["OCCUR_DATE"], errors="coerce")

    if "OCCUR_TIME" in df.columns:
        df["OCCUR_TIME"] = pd.to_datetime(
            df["OCCUR_TIME"],
            format="%H:%M:%S",
            errors="coerce",
        )

    if "hour" not in df.columns:
        if "OCCUR_TIME" in df.columns:
            df["hour"] = df["OCCUR_TIME"].dt.hour
        else:
            raise ValueError("Missing both 'hour' and 'OCCUR_TIME' columns.")

    if "OCCUR_DATE" in df.columns:
        df["day_type_standard"] = np.where(
            df["OCCUR_DATE"].dt.dayofweek >= 5,
            "Weekend",
            "Weekday",
        )
    else:
        df["day_type_standard"] = None

    hour_series = df["hour"]
    df["time_group"] = np.select(
        [
            hour_series.between(7, 11, inclusive="both"),
            hour_series.between(12, 17, inclusive="both"),
            hour_series.between(18, 22, inclusive="both"),
        ],
        ["Morning", "Afternoon", "Evening"],
        default="Night",
    )
    df.loc[hour_series.isna(), "time_group"] = None

    df["hour_order"] = df["hour"].apply(hour_order)
    df["hour_label"] = df["hour"].apply(hour_label)

    if "BORO" in df.columns:
        df["borough"] = df["BORO"].astype(str).str.title()
    elif "borough" in df.columns:
        df["borough"] = df["borough"].astype(str).str.title()
    else:
        raise ValueError("Missing both 'BORO' and 'borough' columns.")

    df["borough_population"] = df["borough"].map(BOROUGH_POPULATION)

    base_df = (
        df[
            [
                "INCIDENT_KEY",
                "OCCUR_DATE",
                "hour",
                "hour_order",
                "hour_label",
                "borough",
                "borough_population",
                "day_type_standard",
                "time_group",
            ]
        ]
        .drop_duplicates(subset=["INCIDENT_KEY"])
        .dropna(
            subset=[
                "INCIDENT_KEY",
                "OCCUR_DATE",
                "hour",
                "borough",
                "day_type_standard",
                "time_group",
            ]
        )
        .copy()
    )

    base_df["day_type_standard"] = base_df["day_type_standard"].astype(str)
    base_df["time_group"] = base_df["time_group"].astype(str)

    return base_df


@st.cache_data(show_spinner=False)
def build_borough_norm_df(base_df):
    borough_norm_df = (
        base_df.groupby("borough")
        .agg(
            shootings=("INCIDENT_KEY", "nunique"),
            population=("borough_population", "max"),
        )
        .reset_index()
    )

    borough_norm_df["shootings_per_100k"] = (
        borough_norm_df["shootings"] / borough_norm_df["population"] * 100_000
    )

    return borough_norm_df


@st.cache_data(show_spinner=False)
def build_day_norm_df(base_df):
    day_counts = (
        base_df.dropna(subset=["OCCUR_DATE", "day_type_standard"])
        .groupby(["day_type_standard", "OCCUR_DATE"])
        .agg(shootings_on_day=("INCIDENT_KEY", "nunique"))
        .reset_index()
    )

    day_norm_df = (
        day_counts.groupby("day_type_standard")
        .agg(
            total_shootings=("shootings_on_day", "sum"),
            days=("OCCUR_DATE", "nunique"),
        )
        .reset_index()
    )

    day_norm_df["shootings_per_day"] = (
        day_norm_df["total_shootings"] / day_norm_df["days"]
    )

    return day_norm_df


@st.cache_data(show_spinner=False)
def build_time_norm_df(base_df):
    time_source = base_df.dropna(
        subset=["OCCUR_DATE", "hour", "time_group", "INCIDENT_KEY"]
    ).copy()

    shootings = (
        time_source.groupby("time_group")
        .agg(shootings=("INCIDENT_KEY", "nunique"))
        .reset_index()
    )

    exposure = (
        time_source[["OCCUR_DATE", "hour", "time_group"]]
        .drop_duplicates()
        .groupby("time_group")
        .size()
        .reset_index(name="date_hour_slots")
    )

    time_norm_df = shootings.merge(exposure, on="time_group", how="left")
    time_norm_df["shootings_per_hour"] = (
        time_norm_df["shootings"] / time_norm_df["date_hour_slots"]
    )

    return time_norm_df
