import altair as alt

def make_hour_chart(df):
    hour_df = (
        df.groupby("hour")
        .agg(shootings=("INCIDENT_KEY", "count"))
        .reset_index()
    )

    return alt.Chart(hour_df).mark_bar().encode(
        x=alt.X("hour:O", title=None),
        y=alt.Y("shootings:Q", title="Shootings"),
        tooltip=["hour:O", "shootings:Q"]
    ).properties(
        title="Shootings by Hour",
        width=700,
        height=300
    )