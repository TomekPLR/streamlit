import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from datetime import datetime, timedelta

st.set_page_config(layout='wide')

@st.cache
def load_data(file):
    return pd.read_csv(file)

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)
    data['scrap_date'] = pd.to_datetime(data['scrap_date'])

    st.sidebar.write('Date range:')
    initial_date = st.sidebar.date_input("Initial date", datetime.now() - timedelta(weeks=2))
    final_date = st.sidebar.date_input("Final date", datetime.now())

    filtered_data = data[(data['scrap_date'] >= initial_date) & (data['scrap_date'] <= final_date)]

    variable1 = st.sidebar.selectbox('Select first variable', filtered_data.columns)
    variable2 = st.sidebar.selectbox('Select second variable', filtered_data.columns)

    unique_properties = filtered_data['property'].unique()
    selected_properties = st.sidebar.multiselect('Select properties (optional)', unique_properties)

    max_results = st.sidebar.number_input('Number of results', min_value=1, max_value=len(unique_properties), value=100)

    correlation_type = st.sidebar.radio('Correlation type', ('Highest', 'Lowest'))

    normalize = st.sidebar.checkbox('Normalize charts (0-1)')

    if not selected_properties:
        selected_properties = unique_properties

    corr_list = []

    for property_name in selected_properties:
        property_data = filtered_data[filtered_data['property'] == property_name]

        if len(property_data) > 1:
            corr, _ = pearsonr(property_data[variable1], property_data[variable2])
            corr_list.append((property_name, corr))

    sorted_corr = sorted(corr_list, key=lambda x: x[1], reverse=correlation_type == 'Highest')[:max_results]

    for property_name, corr in sorted_corr:
        st.write(f"Property: {property_name}, Correlation: {corr}")

        property_data = filtered_data[filtered_data['property'] == property_name]

        fig, ax = plt.subplots()

        if normalize:
            ax.plot(property_data['scrap_date'], (property_data[variable1] - property_data[variable1].min()) / (property_data[variable1].max() - property_data[variable1].min()), label=variable1)
            ax.plot(property_data['scrap_date'], (property_data[variable2] - property_data[variable2].min()) / (property_data[variable2].max() - property_data[variable2].min()), label=variable2)
        else:
            ax.plot(property_data['scrap_date'], property_data[variable1], label=variable1)
            ax.plot(property_data['scrap_date'], property_data[variable2], label=variable2)

        ax.legend()
        ax.set_title(f"{property_name} - {variable1} vs {variable2}")

        if 'number_of_clicks' in property_data.columns:
            before_clicks = property_data[property_data['scrap_date'] < initial_date]['number_of_clicks'].sum()
            after_clicks = property_data[property_data['scrap_date'] >= initial_date]['number_of_clicks'].sum()
            relative_difference = (after_clicks - before_clicks) / before_clicks * 100
