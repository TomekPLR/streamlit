import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('CSV Analysis - Property Click Losses')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
    data['date'] = data['scrap_date'].dt.date

    initial_date = st.date_input('Initial Date', data['date'].min())
    final_date = st.date_input('Final Date', data['date'].max())

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        filtered_data = data[(data['date'] >= initial_date) & (data['date'] <= final_date)]

        property_filter = st.text_input('Filter properties by name (contains):', '')
        if property_filter:
            filtered_data = filtered_data[filtered_data['property'].str.contains(property_filter)]

        grouped_data = filtered_data.groupby('property')['clicks'].agg(['first', 'last', 'count'])
        grouped_data['absolute_loss'] = grouped_data['first'] - grouped_data['last']
        grouped_data['relative_loss'] = (grouped_data['absolute_loss'] / grouped_data['first']) * 100
        grouped_data = grouped_data.reset_index()

        st.write('Biggest loses in terms of clicks between selected dates:')
        st.write(grouped_data.sort_values(by='absolute_loss', ascending=False).head(10))

        property_chart = st.selectbox('Select a property to see the chart:', grouped_data['property'].unique())
        selected_property = filtered_data[filtered_data['property'] == property_chart]

        fig, ax = plt.subplots()
        ax.plot(selected_property['scrap_date'], selected_property['clicks'])
        ax.set_xlabel('Scrap Date')
        ax.set_ylabel('Clicks')
        ax.set_title(f'{property_chart} Clicks over Time')
        st.pyplot(fig)
