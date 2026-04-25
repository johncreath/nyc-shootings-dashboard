import altair as alt

HOUR_SORT = [
    "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM",
    "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM",
    "7 PM", "8 PM", "9 PM", "10 PM", "11 PM", "12 AM",
    "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM",
]
DAY_SORT = ["Weekday", "Weekend"]
TIME_GROUP_SORT = ["Morning", "Afternoon", "Evening", "Night"]
BOROUGH_SORT = ["Brooklyn", "Bronx", "Manhattan", "Queens", "Staten Island"]

CHART_HEIGHT = 250
CHART_SPACING = 24
MAIN_CHART_HEIGHT = 320
DASHBOARD_WIDTH = 920
SMALL_CHART_WIDTH = (DASHBOARD_WIDTH - 2 * CHART_SPACING) // 3
COMPACT_CHART_WIDTH = 320
COMPACT_CHART_HEIGHT = 230
COMPACT_MAIN_CHART_HEIGHT = 260
COMPACT_CHART_SPACING = 14

BOROUGH_PALETTE = ["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#54A24B"]
DAY_PALETTE = ["#4C78A8", "#F58518"]
TIME_PALETTE = ["#D36A86", "#72B7B2", "#54A24B", "#4C78A8"]
HOUR_PALETTE = ["#31447A", "#4E6FAE", "#F2C94C", "#F39C12", "#2C345B"]


def _base_style(chart, compact=False):
    axis_label_size = 11 if compact else 12
    axis_title_size = 12 if compact else 13
    title_size = 14 if compact else 16
    spacing = COMPACT_CHART_SPACING if compact else CHART_SPACING

    return (
        chart.configure_axis(labelFontSize=axis_label_size, titleFontSize=axis_title_size)
        .configure_title(fontSize=title_size, anchor="start")
        .configure_view(stroke=None)
        .configure_concat(spacing=spacing)
    )


def make_hour_chart_filtered(base_df, borough_sel, day_sel, time_sel, compact=False):
    width = COMPACT_CHART_WIDTH if compact else DASHBOARD_WIDTH
    height = COMPACT_MAIN_CHART_HEIGHT if compact else MAIN_CHART_HEIGHT
    label_angle = 60 if compact else 45

    return (
        alt.Chart(base_df)
        .transform_filter(borough_sel)
        .transform_filter(day_sel)
        .transform_filter(time_sel)
        .mark_bar()
        .encode(
            x=alt.X(
                "hour_label:N",
                sort=HOUR_SORT,
                title=None,
                axis=alt.Axis(labelAngle=label_angle),
            ),
            y=alt.Y("count(INCIDENT_KEY):Q", title="Shootings"),
            color=alt.Color(
                "hour:Q",
                scale=alt.Scale(domain=[0, 6, 12, 18, 23], range=HOUR_PALETTE),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("hour_label:N", title="Hour"),
                alt.Tooltip("count(INCIDENT_KEY):Q", title="Shootings", format=",")
            ],
        )
        .properties(
            title=alt.TitleParams(
                text="Shootings by Hour",
                fontSize=16 if compact else 18
            ),
            width=width,
            height=height,
        )
    )


def make_interactive_segment_chart(
    base_df,
    field,
    title,
    sort_order,
    palette,
    tooltip_title,
    selection,
    filter_selections=None,
    compact=False,
):
    chart = alt.Chart(base_df)
    width = COMPACT_CHART_WIDTH if compact else SMALL_CHART_WIDTH
    height = COMPACT_CHART_HEIGHT if compact else CHART_HEIGHT
    label_angle = 35 if compact else 45

    for filter_selection in filter_selections or []:
        chart = chart.transform_filter(filter_selection)

    return (
        chart.mark_bar()
        .encode(
            x=alt.X(f"{field}:N", sort=sort_order, title=None, axis=alt.Axis(labelAngle=label_angle)),
            y=alt.Y("count(INCIDENT_KEY):Q", title=None),
            color=alt.Color(
                f"{field}:N",
                scale=alt.Scale(domain=sort_order, range=palette),
                legend=None,
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.45)),
            tooltip=[
                alt.Tooltip(f"{field}:N", title=tooltip_title),
                alt.Tooltip("count(INCIDENT_KEY):Q", title="Shootings", format=","),
            ],
        )
        .add_params(selection)
        .properties(title=title, width=width, height=height)
    )


def make_static_segment_chart(
    data,
    field,
    value_field,
    value_title,
    title,
    sort_order,
    palette,
    tooltip_title,
    tooltip_value_title,
    tooltip_format=".2f",
    compact=False,
):
    width = COMPACT_CHART_WIDTH if compact else SMALL_CHART_WIDTH
    height = COMPACT_CHART_HEIGHT if compact else CHART_HEIGHT
    label_angle = 35 if compact else 45

    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(f"{field}:N", sort=sort_order, title=None, axis=alt.Axis(labelAngle=label_angle)),
            y=alt.Y(f"{value_field}:Q", title=value_title),
            color=alt.Color(
                f"{field}:N",
                scale=alt.Scale(domain=sort_order, range=palette),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(f"{field}:N", title=tooltip_title),
                alt.Tooltip(f"{value_field}:Q", title=tooltip_value_title, format=tooltip_format),
            ],
        )
        .properties(title=title, width=width, height=height)
    )


def make_raw_row(base_df, borough_sel, day_sel, time_sel, compact=False):
    borough_chart = make_interactive_segment_chart(
        base_df=base_df,
        field="borough",
        title="By Borough",
        sort_order=BOROUGH_SORT,
        palette=BOROUGH_PALETTE,
        tooltip_title="Borough",
        selection=borough_sel,
        filter_selections=[day_sel, time_sel],
        compact=compact,
    )

    day_chart = make_interactive_segment_chart(
        base_df=base_df,
        field="day_type_standard",
        title="By Day Type",
        sort_order=DAY_SORT,
        palette=DAY_PALETTE,
        tooltip_title="Day Type",
        selection=day_sel,
        filter_selections=[borough_sel, time_sel],
        compact=compact,
    )

    time_chart = make_interactive_segment_chart(
        base_df=base_df,
        field="time_group",
        title="By Time of Day",
        sort_order=TIME_GROUP_SORT,
        palette=TIME_PALETTE,
        tooltip_title="Time Group",
        selection=time_sel,
        filter_selections=[borough_sel, day_sel],
        compact=compact,
    )

    if compact:
        return alt.vconcat(
            borough_chart,
            day_chart,
            time_chart,
            spacing=COMPACT_CHART_SPACING,
        )

    return alt.hconcat(
        borough_chart,
        day_chart,
        time_chart,
        spacing=CHART_SPACING,
        # bounds="flush",
    )


def make_norm_row(borough_norm_df, day_norm_df, time_norm_df, compact=False):
    borough_chart = make_static_segment_chart(
        data=borough_norm_df,
        field="borough",
        value_field="shootings_per_100k",
        value_title="Per 100k Residents",
        title="By Borough (Per Capita)",
        sort_order=BOROUGH_SORT,
        palette=BOROUGH_PALETTE,
        tooltip_title="Borough",
        tooltip_value_title="Shootings per 100k",
        compact=compact,
    )

    day_chart = make_static_segment_chart(
        data=day_norm_df,
        field="day_type_standard",
        value_field="shootings_per_day",
        value_title="Shootings per Day",
        title="By Day Type (Per Day)",
        sort_order=DAY_SORT,
        palette=DAY_PALETTE,
        tooltip_title="Day Type",
        tooltip_value_title="Shootings per Day",
        compact=compact,
    )

    time_chart = make_static_segment_chart(
        data=time_norm_df,
        field="time_group",
        value_field="shootings_per_hour",
        value_title="Shootings per Hour",
        title="By Time of Day (Per Hour)",
        sort_order=TIME_GROUP_SORT,
        palette=TIME_PALETTE,
        tooltip_title="Time Group",
        tooltip_value_title="Shootings per Hour",
        compact=compact,
    )

    if compact:
        return alt.vconcat(
            borough_chart,
            day_chart,
            time_chart,
            spacing=COMPACT_CHART_SPACING,
        )

    return alt.hconcat(
        borough_chart,
        day_chart,
        time_chart,
        spacing=CHART_SPACING,
        # bounds="flush",
    )


def make_dashboard_chart(base_df, borough_norm_df, day_norm_df, time_norm_df, compact=False):
    borough_sel = alt.selection_point(fields=["borough"], empty=True, name="borough_sel")
    day_sel = alt.selection_point(fields=["day_type_standard"], empty=True, name="day_sel")
    time_sel = alt.selection_point(fields=["time_group"], empty=True, name="time_sel")

    hour_chart = make_hour_chart_filtered(
        base_df,
        borough_sel,
        day_sel,
        time_sel,
        compact=compact,
    )

    if compact:
        borough_chart = make_interactive_segment_chart(
            base_df=base_df,
            field="borough",
            title="Total Shootings by Borough",
            sort_order=BOROUGH_SORT,
            palette=BOROUGH_PALETTE,
            tooltip_title="Borough",
            selection=borough_sel,
            filter_selections=[day_sel, time_sel],
            compact=True,
        )

        day_chart = make_interactive_segment_chart(
            base_df=base_df,
            field="day_type_standard",
            title="Total Shootings by Day Type",
            sort_order=DAY_SORT,
            palette=DAY_PALETTE,
            tooltip_title="Day Type",
            selection=day_sel,
            filter_selections=[borough_sel, time_sel],
            compact=True,
        )

        time_chart = make_interactive_segment_chart(
            base_df=base_df,
            field="time_group",
            title="Total Shootings by Time of Day",
            sort_order=TIME_GROUP_SORT,
            palette=TIME_PALETTE,
            tooltip_title="Time Group",
            selection=time_sel,
            filter_selections=[borough_sel, day_sel],
            compact=True,
        )

        borough_norm_chart = make_static_segment_chart(
            data=borough_norm_df,
            field="borough",
            value_field="shootings_per_100k",
            value_title="Per 100k Residents",
            title="Per Capita by Borough",
            sort_order=BOROUGH_SORT,
            palette=BOROUGH_PALETTE,
            tooltip_title="Borough",
            tooltip_value_title="Shootings per 100k",
            compact=True,
        )

        day_norm_chart = make_static_segment_chart(
            data=day_norm_df,
            field="day_type_standard",
            value_field="shootings_per_day",
            value_title="Shootings per Day",
            title="Per Day by Day Type",
            sort_order=DAY_SORT,
            palette=DAY_PALETTE,
            tooltip_title="Day Type",
            tooltip_value_title="Shootings per Day",
            compact=True,
        )

        time_norm_chart = make_static_segment_chart(
            data=time_norm_df,
            field="time_group",
            value_field="shootings_per_hour",
            value_title="Shootings per Hour",
            title="Per Hour by Time of Day",
            sort_order=TIME_GROUP_SORT,
            palette=TIME_PALETTE,
            tooltip_title="Time Group",
            tooltip_value_title="Shootings per Hour",
            compact=True,
        )

        dashboard = alt.vconcat(
            hour_chart,
            borough_chart,
            day_chart,
            time_chart,
            borough_norm_chart,
            day_norm_chart,
            time_norm_chart,
            spacing=COMPACT_CHART_SPACING,
        ).resolve_scale(color="independent")

        return _base_style(dashboard, compact=True)

    raw_row = make_raw_row(base_df, borough_sel, day_sel, time_sel, compact=compact).properties(
        title=alt.TitleParams(
            "Volume Metrics (Total Shootings) by Segmentation",
            anchor="start",
            fontSize=16 if compact else 18,
            offset=16 if compact else 20
        )
    )

    norm_row = make_norm_row(
        borough_norm_df,
        day_norm_df,
        time_norm_df,
        compact=compact,
    ).properties(
        title=alt.TitleParams(
            "Normalized Metrics (Shootings Per Capita/Day/Hour) by Segmentation",
            anchor="start",
            fontSize=16 if compact else 18,
            offset=16 if compact else 20
        )
    )

    dashboard = alt.vconcat(
        hour_chart,
        raw_row,
        norm_row,
        spacing=COMPACT_CHART_SPACING if compact else 18,
    ).resolve_scale(color="independent")

    return _base_style(dashboard, compact=compact)
