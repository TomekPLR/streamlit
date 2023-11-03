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
        start_date = datetime.strptime(update['date_start'], '%d %b %Y')
        end_date = start_date + timedelta(days=update['duration'])
        before_start = start_date - timedelta(days=14)

        # Filter data and calculate average clicks
        clicks_before = clicks_df[(clicks_df['date'] >= before_start) & (clicks_df['date'] < start_date)]['clicks'].mean()
        clicks_after = clicks_df[(clicks_df['date'] >= start_date) & (clicks_df['date'] <= end_date)]['clicks'].mean()

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
    
    # Adding annotations for core updates
    annotations = [dict(x=update['date_start'], y=0, showarrow=False, text=update['name'], textangle=-45, xref='x', yref='y') for update in CORE_UPDATES]
    fig.update_layout(annotations=annotations)
    
    st.plotly_chart(fig)
