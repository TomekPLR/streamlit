import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Sample core updates data
CORE_UPDATES = [
    {"name": "October 2023 core update", "date_start": "2023-10-05", "duration": 14},
    {"name": "Ranking ongoing issue", "date_start": "2023-10-05", "duration": 26},
    {"name": "October 2023 spam update", "date_start": "2023-10-04", "duration": 16},
    {"name": "September 2023 helpful content update", "date_start": "2023-09-14", "duration": 13},
    {"name": "August 2023 core update", "date_start": "2023-08-22", "duration": 17},
    {"name": "April 2023 reviews update", "date_start": "2023-04-12", "duration": 13},
    {"name": "March 2023 core update", "date_start": "2023-03-15", "duration": 13},
    {"name": "February 2023 product reviews update", "date_start": "2023-02-21", "duration": 14},
    {"name": "December 2022 link spam update", "date_start": "2022-12-14", "duration": 29},
    {"name": "December 2022 helpful content update", "date_start": "2022-12-05", "duration": 38},
    {"name": "October 2022 spam update", "date_start": "2022-10-19", "duration": 2},
    {"name": "September 2022 product reviews update", "date_start": "2022-09-20", "duration": 6},
    {"name": "September 2022 core update", "date_start": "2022-09-12", "duration": 14},
    {"name": "August 2022 helpful content update", "date_start": "2022-08-25", "duration": 15},
    {"name": "July 2022 product reviews update", "date_start": "2022-07-27", "duration": 6}
]

def analyze_clicks(clicks_df, core_updates, significant_change):
    results = []

    for update in core_updates:
        start_date = datetime.strptime(update['date_start'], '%Y-%m-%d')
        after_end = start_date + timedelta(days=update['duration'])
        before_start = start_date - timedelta(days=14)

        # Filter data and calculate sum of clicks
        clicks_before = clicks_df[(clicks_df['date'] >= before_start) & (clicks_df['date'] < start_date)]['clicks'].sum()
        clicks_after = clicks_df[(clicks_df['date'] >= start_date) & (clicks_df['date'] <= after_end)]['clicks'].sum()

        difference = clicks_after - clicks_before

        if abs(difference) / clicks_before * 100 >= significant_change:
            results.append({
                'Update Name': update['name'],
                'Clicks Before': clicks_before,
                'Clicks After': clicks_after,
                'Difference': difference,
                'Percentage Change': (difference / clicks_before * 100) if clicks_before > 0 else 0
            })

    return pd.DataFrame(results)

st.title("Website Hit Analysis during Core Updates")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
significant_change = st.slider("Select the significant change percentage", 0, 100, 10)

if uploaded_file is not None:
    # Read and display the clicks data
    clicks_df = pd.read_csv(uploaded_file)
    clicks_df['date'] = pd.to_datetime(clicks_df['date'], format='%Y-%m-%d')
    clicks_df = clicks_df.sort_values('date')

    st.write("### Clicks Data")
    st.write(clicks_df)

    # Group by week option
    group_by_week = st.checkbox("Group by week")
    plot_df = clicks_df.copy()
    if group_by_week:
        plot_df['week_start'] = plot_df['date'].dt.to_period('W').apply(lambda r: r.start_time)
        plot_df = plot_df.groupby(['week_start']).agg({'clicks': 'sum'}).reset_index()

    # Perform analysis
    results_df = analyze_clicks(clicks_df, CORE_UPDATES, significant_change)

    # Display Results
    st.write("### Analysis Results")
    st.write(results_df)

    # Let user select core updates to annotate
    update_names = [update['name'] for update in CORE_UPDATES]
    selected_updates = st.multiselect("Select core updates to annotate", options=update_names, default=update_names)

    # Checkbox to select if annotations for core update ends should be shown
    show_update_ends = st.checkbox("Show annotations for core update ends")

    # Let user choose plot type
    plot_type = st.selectbox("Select plot type", ['Line', 'Dotted'])

    # Plot the data
    st.write("### Clicks Timeline")
    x_axis = 'week_start' if group_by_week else 'date'
    chart_func = px.line if plot_type == 'Line' else px.scatter
    fig = chart_func(plot_df, x=x_axis, y='clicks', title='Clicks Over Time')

    # Adding annotations for selected core updates with alternating positions
    annotations = []
    for i, update in enumerate([upd for upd in CORE_UPDATES if upd['name'] in selected_updates]):
        update_start_date = datetime.strptime(update['date_start'], '%Y-%m-%d')
        update_end_date = update_start_date + timedelta(days=update['duration'])
        y_pos = 0 if i % 2 == 0 else plot_df['clicks'].max()

        # Annotate the start date
        annotations.append(dict(
            x=update['date_start'], y=y_pos, xref='x', yref='y',
            showarrow=True, text=update['name'], textangle=-45
        ))
        # Add vertical line for start date
        fig.add_shape(dict(
            type="line", x0=update['date_start'], x1=update['date_start'],
            y0=0, y1=plot_df['clicks'].max(), line=dict(color="Red", width=2)
        ))

        if show_update_ends:
            # Annotate the end date if checkbox is checked
            annotations.append(dict(
                x=str(update_end_date.date()), y=y_pos, xref='x', yref='y',
                showarrow=True, text=f"{update['name']} end", textangle=-45
           

