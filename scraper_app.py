import streamlit as st
import pandas as pd
from pandas.api.types import CategoricalDtype

# Define a custom sorting order for the "property" column
property_order = ['Property A', 'Property B', 'Property C', 'Property D', 'Property E']

# Define the columns that can be selected for analysis
analysis_columns = ['download_size', 'requests', 'avg_response_time', 'response_ok', 'response_301', 'response_302', 'response_404', 'response_server_error', 'clicks', 'impressions', 'avg_ctr', 'avg_position', 'purpose_discovery', 'purpose_refresh', 'mobile_good', 'mobile_improve', 'mobile_poor', 'desktop_good', 'desktop_improve', 'desktop_poor']

# Define the column names to use for the output table
output_columns = list(property_data.columns) + ['Absolute Change', 'Relative Change']

# Define a function to calculate the relative change
def calculate_relative_change(initial_value, final_value):
    if initial_value == 0:
        return 0
    else:
        return (final_value - initial_value) / initial_value

# Define the Streamlit app
st.title("Property Analysis")

# File upload
file = st.file_uploader("Upload a CSV file", type=["csv"])
if file is None:
    st.stop()

# Load the CSV file
data = pd.read_csv(file)

# Convert the "scrap_date" column to a categorical data type and sort it in ascending order
date_order = sorted(data["scrap_date"].unique())
date_dtype = CategoricalDtype(categories=date_order, ordered=True)
data["scrap_date"] = data["scrap_date"].astype(date_dtype)

# Sidebar controls
initial_date = st.sidebar.selectbox("Select initial date", date_order)
final_date = st.sidebar.selectbox("Select final date", date_order)
analysis_column = st.sidebar.selectbox("Select column to analyze", analysis_columns)

# Filter the data based on the selected dates
filtered_data = data[(data["scrap_date"] == initial_date) | (data["scrap_date"] == final_date)]

# Calculate the initial and final values for each property
property_data = filtered_data.pivot_table(values=analysis_column, index="property", columns="scrap_date")
property_data["Absolute Change"] = property_data[final_date] - property_data[initial_date]
property_data["Relative Change"] = property_data.apply(lambda row: calculate_relative_change(row[initial_date], row[final_date]), axis=1)

# Sort the properties by their relative change
sorted_data = property_data.sort_values("Relative Change", ascending=False)

# Display the top 10 winning properties
st.subheader("Top 10 winning properties")
winning_properties = sorted_data.head(10)[output_columns]
winning_properties.index.name = None
st.dataframe(winning_properties.style.format({'Relative Change': "{:.2%}"}))

# Display the top 10 losing properties
st.subheader("Top 10 losing properties")
losing_properties = sorted_data.tail(10)[output_columns]
losing_properties.index.name = None
st.dataframe(losing_properties.style.format({'Relative Change': "{:.2%}"}))

# Display the full table
st.subheader("Full table")
full_table = property_data[output_columns].reindex(property_order)
full_table.index.name = None
st.dataframe(full_table.style.format({'Relative Change': "{:.2%}"}))
