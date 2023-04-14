import streamlit as st
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Sidebar selectors
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV
    data = pd.read_csv(uploaded_file)

    # Convert scrap_date column to pandas datetime format
    data['scrap_date'] = pd.to_datetime(data['scrap_date'])

    now = datetime.date.today()
    initial_date = pd.Timestamp(st.sidebar.date_input('Initial date', now - datetime.timedelta(weeks=2)))
    final_date = pd.Timestamp(st.sidebar.date_input('Final date', now))
    property_filter = st.sidebar.multiselect("Select properties", data['property'].unique())

    # Filter the data based on the selected dates
    filtered_data = data[(data['scrap_date'] >= initial_date) & (data['scrap_date'] <= final_date)]

    # Filter the data based on the selected properties
    if property_filter:
        filtered_data = filtered_data[filtered_data['property'].isin(property_filter)]

    # Select columns
    variable1 = st.sidebar.selectbox("Select variable 1", filtered_data.columns)
    variable2 = st.sidebar.selectbox("Select variable 2", filtered_data.columns)

    # Select sorting order
    sort_order = st.sidebar.selectbox("Sort by correlation", ["Highest", "Lowest"])

    # Normalize option
    normalize = st.sidebar.checkbox("Normalize charts (0-1)")

    # Calculate correlations
    correlations = filtered_data.groupby("property").apply(lambda x: x[variable1].corr(x[variable2]))

    # Sort properties based on the correlation
    if sort_order == "Highest":
        sorted_properties = correlations.sort_values(ascending=False)
    else:
        sorted_properties = correlations.sort_values(ascending=True)

    # Display charts
    st.title("Charts")

    for property in sorted_properties.index[:100]:
        st.header(f"Property: {property}")
        st.write(f"Correlation: {sorted_properties[property]}")
        st.write(f"Difference in number of clicks: {filtered_data.loc[filtered_data['property'] == property, 'clicks'].diff().sum()}")

        property_data = filtered_data[filtered_data['property'] == property]
        fig, ax = plt.subplots()

        if normalize:
            ax.plot(property_data['scrap_date'], (property_data[variable1] - property_data[variable1].min()) / (property_data[variable1].max() - property_data[variable1].min()), label=variable1)
            ax.plot(property_data['scrap_date'], (property_data[variable2] - property_data[variable2].min()) / (property_data[variable2].max() - property_data[variable2].min()), label=variable2)
        else:
            ax.plot(property_data['scrap_date'], property_data[variable1], label=variable1)
            ax.plot(property_data['scrap_date'], property_data[variable2], label=variable2)

        ax.legend()
        st.pyplot(fig)

else:
    st.sidebar.warning("Please upload a CSV file.")
