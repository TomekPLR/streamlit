import streamlit as st
import pandas as pd
import numpy as np

st.title('CSV Analysis - Pages and Queries')

important_dates = {
    '2022-12-14': 'Dec 2022 link spam update',
    '2022-12-05': 'Dec 2022 helpful content update',
    '2022-10-19': 'Oct 2022 spam update',
    '2022-09-20': 'Sep 2022 product reviews update',
    '2022-09-12': 'Sep 2022 core update',
    '2022-08-25': 'Aug 2022 helpful content update',
    '2022-07-27': 'Jul 2022 product reviews update',
    '2022-05-25': 'May 2022 core update',
    '2022-03-23': 'Mar 2022 product reviews update',
    '2022-02-22': 'Feb 2022 page experience update for desktop',
}

uploaded_file1 = st.sidebar.file_uploader("Choose the first CSV file (Pages)", type="csv")
uploaded_file2 = st.sidebar.file_uploader("Choose the second CSV file (Queries)", type="csv")

initial_date = st.sidebar.date_input('Initial Date')
final_date = st.sidebar.date_input('Final Date')

if uploaded_file1 is not None and uploaded_file2 is not None:
    df1 = pd.read_csv(uploaded_file1, parse_dates=['Date'])
    df1['Date'] = df1['Date'].dt.date
    df2 = pd.read_csv(uploaded_file2, parse_dates=['Date'])
    df2['Date'] = df2['Date'].dt.date

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        df1_filtered = df1[(df1['Date'] >= initial_date) & (df1['Date'] <= final_date)]
        df2_filtered = df2[(df2['Date'] >= initial_date) & (df2['Date'] <= final_date)]

        # Rest of the code for analysis as previously provided
        # Perform analysis on the first CSV file
        st.header("Analysis of the First CSV file")

        # Clicks grouped by country before and after, including relative difference
        st.subheader("Clicks grouped by country before and after, including relative difference")
        clicks_by_country = df1_filtered.groupby('Country')['Url Clicks'].agg(['sum', 'count']).reset_index()
        st.write(clicks_by_country)

        # Landing pages that relatively lost the highest number of clicks (relative)
        st.subheader("Landing pages that relatively lost the highest number of clicks (relative)")
        landing_page_clicks = df1_filtered.groupby('Landing Page')['Url Clicks'].agg(['sum', 'count']).reset_index()
        st.write(landing_page_clicks)

        # Group by first catalog
        st.subheader("Group by first catalog")
        df1_filtered['First Catalog'] = df1_filtered['Landing Page'].str.extract(r'(\w+)/')
        catalog_clicks = df1_filtered.groupby('First Catalog')['Url Clicks'].agg(['sum', 'count']).reset_index()
        st.write(catalog_clicks)

        # Perform analysis on the second CSV file
        st.header("Analysis of the Second CSV file")

        # Clicks grouped by country before and after, including relative difference
        st.subheader("Clicks grouped by country before and after, including relative difference")
        clicks_by_country2 = df2_filtered.groupby('Country')['Clicks'].agg(['sum', 'count']).reset_index()
        st.write(clicks_by_country2)

        # Query that relatively lost the highest number of clicks (relative)
        st.subheader("Query that relatively lost the highest number of clicks (relative)")
        query_clicks = df2_filtered.groupby('Query')['Clicks'].agg(['sum', 'count']).reset_index()
        st.write(query_clicks)

        # Group by first catalog
        st.subheader("Group by first catalog")
        df2_filtered['First Catalog'] = df2_filtered['Query'].str.extract(r'(\w+)/')
        catalog_clicks2 = df2_filtered.groupby('First Catalog')['Clicks'].agg(['sum', 'count']).reset_index()
        st.write(catalog_clicks2)

        # Custom queries defined by the user with information if they lost clicks or won clicks, with relative difference
        st.subheader("Custom queries defined by the user")
        custom_query = df2_filtered[df2_filtered['Query'].str.contains(branding_query, na=False)]
        custom_query_clicks = custom_query.groupby('Query')['Clicks'].agg(['sum', 'count']).reset_index()
        st.write(custom_query_clicks)

        # URLs that had clicks in the past (initial date) but no longer bring clicks
        st.subheader("URLs that had clicks in the past (initial date) but no longer bring clicks")
        past_clicks = df2_filtered[df2_filtered['Date'] == initial_date]
        current_clicks = df2_filtered[df2_filtered['Date'] == final_date]
        lost_clicks = past_clicks[~past_clicks['Query'].isin(current_clicks['Query'])]
        st.write(lost_clicks)

        # Table with a list of core updates
        st.header("List of core updates")
        core_updates = pd.DataFrame(list(important_dates.items()), columns=['Date', 'Description'])
        core_updates['Date'] = pd.to_datetime(core_updates['Date'])

        # Filter core updates based on the selected date range
        core_updates = core_updates[(core_updates['Date'] >= initial_date) & (core_updates['Date'] <= final_date)]

        # Calculate clicks before and after the core update
        core_updates['Before'] = core_updates['Date'].apply(lambda x: df2_filtered[(df2_filtered['Date'] >= x - pd.Timedelta(days=14)) & (df2_filtered['Date'] < x)]['Clicks'].sum())
        core_updates['After'] = core_updates['Date'].apply(lambda x: df2_filtered[(df2_filtered['Date'] > x) & (df2_filtered['Date'] <= x + pd.Timedelta(days=14))]['Clicks'].sum())
        core_updates['Percentage Change'] = (core_updates['After'] - core_updates['Before']) / core_updates['Before'] * 100
        st.write(core_updates)

