import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Sample core updates data
CORE_UPDATES = [
    {"name": "October 2023 core update", "date_start": "2023-10-05", "duration": 14},
    # ... Add other updates
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
    
    # Adjusting date format to match "Sep 27, 2023"
    clicks_df['date'] = pd.to_datetime(clicks_df['date'], format='%b %d, %Y')
    
    # Sort data by date
    clicks_df = clicks_df.sort_values('date')
    
    st.write("### Clicks Data")
    st.write(clicks_df)

    # Perform analysis
    results_df = analyze_clicks(clicks_df, CORE_UPDATES, significant_change)

    # Display Results
    st.write("### Analysis Results")
    st.write(results_df)

    # Let user select core updates to annotate
    update_names = [update['name'] for update in CORE_UPDATES]
    selected_updates = st.multiselect("Select core updates to annotate", options=update_names, default=update_names)

    # Plot the data
    st.write("### Clicks Timeline")
    fig = px.line(clicks_df, x='date', y='clicks', title='Clicks Over Time')
    
    # Adding annotations for selected core updates with alternating positions
    annotations = []
    for i, update in enumerate([upd for upd in CORE_UPDATES if upd['name'] in selected_updates]):
        y_pos = 0 if i % 2 == 0 else clicks_df['clicks'].max()
        annotations.append(dict(x=update['date_start'], y=y_pos, xref='x', yref='y', 
                                showarrow=True, text=update['name'], textangle=-45))
        # Adding vertical lines
        fig.add_shape(dict(type="line", x0=update['date_start'], x1=update['date_start'], 
                           y0=0, y1=click
