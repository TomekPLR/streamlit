import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

st.title('CSV Analysis - Property Click Losses')

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
    data['date'] = data['scrap_date'].dt.date

    # Extract hours from last_update column
    data['hours_ago'] = data['last_update'].apply(lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

    # Update scrap_date based on last_update column
    data['scrap_date'] = data['scrap_date'] - pd.to_timedelta(data['hours_ago'], unit='h')

    initial_date = st.sidebar.date_input('Initial Date', data['date'].min())
    final_date = st.sidebar.date_input('Final Date', data['date'].max())

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        filtered_data = data[(data['date'] >= initial_date) & (data['date'] <= final_date)]

        property_filter = st.sidebar.text_input('Filter properties by name (contains):', '')
        if property_filter:
            filtered_data = filtered_data[filtered_data['property'].str.contains(property_filter)]

        min_clicks = st.sidebar.slider("Minimum clicks threshold:", 0, int(filtered_data['clicks'].max()), 0)

        # Compute the click losses based on the initial and final dates
        grouped_data = filtered_data.pivot_table(index='property', columns='date', values='clicks', aggfunc='first').reset_index()
        grouped_data.fillna(0, inplace=True)  # Replace NaNs with zeros
        grouped_data['absolute_loss'] = grouped_data[initial_date] - grouped_data[final_date]
        grouped_data['relative_loss'] = (grouped_data['absolute_loss'] / grouped_data[initial_date]) * 100

        # Clean up the DataFrame and apply the minimum clicks threshold
        grouped_data = grouped_data[['property', initial_date, final_date, 'absolute_loss', 'relative_loss']]
        grouped_data.columns.name = None
        grouped_data.rename(columns={initial_date: 'initial_clicks', final_date: 'final_clicks'}, inplace=True)
        grouped_data = grouped_data[grouped_data['initial_clicks'] >= min_clicks]

        num_properties = st.sidebar.slider("Number of properties to display in the losers table:", 1, len(grouped_data), 10)
        st.write(f'Biggest {num_properties} losers in terms of clicks between selected dates (minimum {min_clicks} clicks):')
        st.write(grouped_data.sort_values(by='absolute_loss', ascending=False).head(num_properties))

        property_chart = st.sidebar.selectbox('Select a property to see the chart:', grouped_data['property'].unique())
        selected_property = filtered_data[filtered_data['property'] == property_chart]

        fig, ax = plt.subplots()
        ax.plot(selected_property['scrap_date'], selected_property['clicks'])
        ax.set_xlabel('Scrap Date')
        ax.set_ylabel('Clicks')
        ax.set_title(f'{property_chart} Clicks over Time')
        st.pyplot(fig)
