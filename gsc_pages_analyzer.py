import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Define the default date range
default_end_date = datetime.today() - timedelta(days=1)
default_start_date = default_end_date - timedelta(days=14)

# Define the file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    try:
        pages_df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error("Error: Could not read CSV file. Please check your file format.")

    # Convert the "Date" column to datetime format
    pages_df["Date"] = pd.to_datetime(pages_df["Date"], format="%b %d, %Y")

    # Define the date range selector
    start_date = st.sidebar.date_input("Select a start date", default_start_date)
    end_date = st.sidebar.date_input("Select an end date", default_end_date)
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')

    # Filter the pages data by date range
    pages_filtered = pages_df[(pages_df["Date"] >= start_date) & (pages_df["Date"] <= end_date)]

    # Create a chart of clicks by country and date
    clicks_by_country = pages_filtered.groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()
    if not clicks_by_country.empty:
        fig1, ax1 = plt.subplots()
        sns.lineplot(x="Date", y="Url Clicks", hue="Country", data=clicks_by_country, ax=ax1)
        ax1.set_title("Clicks by Country")
        st.pyplot(fig1)
    else:
        st.warning("No data found for selected date range.")

    # Define the catalog selector
    catalogs = pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).unique()
    default_num_catalogs = 5
    top_catalogs = pages_filtered.groupby("Landing Page")["Url Clicks"].sum().sort_values(ascending=False).head(default_num_catalogs)
    catalogs_selected = st.sidebar.multiselect("Select catalogs:", top_catalogs.index, default=top_catalogs.index)
    
    # Define the metric selector
    metric = st.sidebar.selectbox("Select a metric:", ["Url Clicks", "Impressions", "URL CTR"])

    # Filter the pages data by selected catalogs
    pages_catalogs = pages_filtered[pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).isin(catalogs_selected)]

    # Pivot the pages data to create a chart of clicks by catalog and date
    pivot = pd.pivot_table(pages_catalogs, values=metric, index="Date", columns=pages_catalogs["Landing Page"].apply(lambda x: x.split("/")[1]), aggfunc=sum)
    if not pivot.empty:
        fig2, ax2 = plt.subplots()
        pivot.plot(ax=ax2)
        ax2.set_title(f"{metric} by Catalog")
        st.pyplot(fig2)
    else:
        st.warning("No data found for selected catalogs and date range.")
