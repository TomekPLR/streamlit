import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Load the CSV data
@st.cache
def load_data(file):
    data = pd.read_csv(file, parse_dates=['scrap_date'])
    return data

st.title('CSV Data Analysis')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Select the initial and final dates
    now = datetime.datetime.now()
    initial_date = st.date_input('Initial date', now - datetime.timedelta(weeks=2))
    final_date = st.date_input('Final date', now)

    # Filter the data based on the selected dates
    filtered_data = data[(data['scrap_date'] >= initial_date) & (data['scrap_date'] <= final_date)]

    # Select variables and filter properties
    variable1 = st.selectbox('Select variable 1', filtered_data.columns)
    variable2 = st.selectbox('Select variable 2', filtered_data.columns)
    properties = st.multiselect('Select properties', filtered_data['property'].unique())
    num_results = st.number_input('Number of results', min_value=1, value=100, step=1)

    if properties:
        filtered_data = filtered_data[filtered_data['property'].isin(properties)]

    def calculate_correlation(data, var1, var2):
        if np.issubdtype(data[var1].dtype, np.number) and np.issubdtype(data[var2].dtype, np.number):
            return data[[var1, var2]].corr().iloc[0, 1]
        else:
            return None

    # Calculate correlations and sort properties
    correlations = filtered_data.groupby('property').apply(lambda x: calculate_correlation(x, variable1, variable2))
    correlations = correlations.nlargest(num_results)

    # Display the results
    for property_name, correlation in correlations.items():
        st.write(f'Property: {property_name}')
        st.write(f'Correlation between {variable1} and {variable2}: {correlation}')
        
        if correlation is not None:
            property_data = filtered_data[filtered_data['property'] == property_name]
            st.line_chart(property_data[[variable1, variable2]])

        before = property_data[property_data['scrap_date'] == initial_date]
        after = property_data[property_data['scrap_date'] == final_date]

        if not before.empty and not after.empty:
            st.write(f"Difference in clicks: {after['clicks'].values[0] - before['clicks'].values[0]}")
            st.write(f"Difference in {variable1}: {after[variable1].values[0] - before[variable1].values[0]}")
            st.write(f"Difference in {variable2}: {after[variable2].values[0] - before[variable2].values[0]}")
        st.write('\n\n')
