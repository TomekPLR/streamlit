import pandas as pd
import streamlit as st
import numpy as np
import datetime

# Load the CSV file
df = pd.read_csv("scraper_data_all_properties.csv")
df["scrap_date"] = pd.to_datetime(df["scrap_date"])

# Get list of all properties
all_properties = df["property"].unique()

# Define function to calculate change percentage
def change_pct(initial, final):
    if initial == 0:
        return np.nan
    else:
        return (final - initial) / initial * 100

# Define function to filter data by date and property, and sort by column
def filter_and_sort(df, start_date, end_date, property_name, sort_col):
    # Filter by date and property
    filtered_df = df[(df["scrap_date"] >= start_date) & (df["scrap_date"] <= end_date)]
    if property_name != "All":
        filtered_df = filtered_df[filtered_df["property"] == property_name]

    # Calculate initial and final values
    initial_values = filtered_df.groupby("property")[sort_col].first().rename("initial")
    final_values = filtered_df.groupby("property")[sort_col].last().rename("final")
    change_values = final_values - initial_values
    pct_change_values = change_pct(initial_values, final_values)

    # Combine into a new DataFrame and sort by pct_change
    result_df = pd.concat([initial_values, final_values, change_values, pct_change_values], axis=1)
    result_df = result_df.sort_values("pct_change", ascending=False)

    return result_df


# Create Streamlit app
st.title("Scraper Data Analysis")
st.sidebar.title("Filters")

# Date range filter
min_date = df["scrap_date"].min().date()
max_date = df["scrap_date"].max().date()
start_date = st.sidebar.date_input("Start date", min_date)
end_date = st.sidebar.date_input("End date", max_date)

# Property filter
property_name = st.sidebar.selectbox("Property", ["All"] + list(all_properties))

# Column to sort by filter
sort_col = st.sidebar.selectbox("Sort by", df.columns)

# Filter and sort data
result_df = filter_and_sort(df, start_date, end_date, property_name, sort_col)

# Show the results in a table
st.write(result_df.head(10))
st.write(result_df.tail(10))
