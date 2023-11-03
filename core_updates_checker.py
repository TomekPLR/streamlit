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
    {"name": "July 2022 product reviews update", "date_start": "2022-07-27", "duration": 6},
    {"name": "May 2022 core update", "date_start": "2022-05-25", "duration": 15},
    {"name": "March 2022 product reviews update", "date_start": "2022-03-23", "duration": 14},
    {"name": "Page experience update for desktop", "date_start": "2022-02-22", "duration": 9},
]


def analyze_clicks(clicks_df, core_updates, significant_change):
    results = []

    for update in core_updates:
        start_date = datetime.strptime(update['date_start'], '%Y-%m-%d')
        after_end = start_date + timedelta(days=14)
        before_start = start_date - timedelta(days=14)

        # Filter data and calculate sum of clicks
        clicks_before = clicks_df[(clicks_df['date'] >= before_start) & (clicks_df['date'] < start_date)]['clicks'].sum()
        clicks_after = clicks_df[(clicks_df['date'] > start_date) & (clicks_df['date'] <= after_end)]['clicks'].sum()

        difference = clicks_after - clicks_before

        if abs(difference) / clicks_before * 100 >= significant_change:
            results.append({
                'Update Name': update['name'],
                'Clicks Before': clicks_before,
                'Clicks After': clicks_after,
                'Difference': difference,
                'Percentage Change': difference / clicks_before * 100
            })

    return pd.DataFrame(results)

st.title("Website Hit Analysis during Core Updates")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
significant_change = st.slider("Select the significant change percentage", 0, 100, 10)

if uploaded_file is not None:
    # Read and display the clicks data
    clicks_df = pd.read_csv(uploaded_file)
    clicks_df['date'] = pd.to_datetime(clicks_df['date'], format='%d %b %Y')
    
    # Sort data by date
    clicks_df = clicks_df.sort_values('date')
    
    st.write("### Clicks Data")
    st.write(clicks_df)

    # Perform analysis
    results_df = analyze_clicks(clicks_df, CORE_UPDATES, significant_change)

    # Display Results
    st.write("### Analysis Results")
    st.write(results_df)

    # Plot the data
    st.write("### Clicks Timeline")
    fig = px.line(clicks_df, x='date', y='clicks', title='Clicks Over Time')
    
    # Adding annotations for core updates with alternating positions
    annotations = []
    for i, update in enumerate(CORE_UPDATES):
        y_pos = 0 if i % 2 == 0 else clicks_df['clicks'].max()
        annotations.append(dict(x=update['date_start'], y=y_pos, xref='x', yref='y', 
                                showarrow=True, text=update['name'], textangle=-45))
        # Adding vertical lines
        fig.add_shape(dict(type="line", x0=update['date_start'], x1=update['date_start'], 
                           y0=0, y1=clicks_df['clicks'].max(), line=dict(color="Red", width=2)))

    fig.update_layout(annotations=annotations)
    
    st.plotly_chart(fig)
