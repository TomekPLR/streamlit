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

    # Get the top 5 countries with the most clicks
    top_countries = pages_filtered.groupby("Country")["Url Clicks"].sum().sort_values(ascending=False).head(5).index

    # Create a chart of clicks by country and date
    clicks_by_country = pages_filtered.groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()
    top_clicks_by_country = clicks_by_country[clicks_by_country["Country"].isin(top_countries)]

    if not top_clicks_by_country.empty:
        fig1, ax1 = plt.subplots()
        sns.lineplot(x="Date", y="Url Clicks", hue="Country", data=top_clicks_by_country, ax=ax1)
        ax1.set_title("Clicks by Country")
        st.pyplot(fig1)
    else:
        st.warning("No data found for selected date range.")

    # Define the country selector
    countries = pages_filtered["Country"].unique()
    countries_selected = st.sidebar.multiselect("Select countries:", sorted(countries), default=sorted(top_countries))
    
    # Define the catalog selector
    catalogs = pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).unique()
    top_catalogs = pages_filtered.groupby("Landing Page")["Url Clicks"].sum().sort_values(ascending=False).head(5).index
    catalogs_selected = st.sidebar.multiselect("Select catalogs:", sorted(catalogs), default=sorted(top_catalogs))
    
    # Define the metric selector
    metric = st.sidebar.selectbox("Select a metric:", ["Url Clicks", "Impressions", "URL CTR"])

    # Filter the pages data by selected countries and catalogs
    pages_countries_catalogs = pages_filtered[pages_filtered["Country"].isin(countries_selected) &
                                             pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).isin(catalogs_selected)]

    # Pivot the pages data to create a chart of clicks by catalog and date
    pivot = pd.pivot_table(pages_countries_catalogs, values=metric, index="Date ", columns=pages_countries_catalogs["Landing Page"].apply(lambda x: x.split("/")[1]), aggfunc=sum)
    if not pivot.empty:
        fig2, ax2 = plt.subplots()
        pivot.plot(ax=ax2)
        ax2.set_title(f"{metric} by Catalog")
        st.pyplot(fig2)
    else:
        st.warning("No data found for selected catalogs and date range.")

