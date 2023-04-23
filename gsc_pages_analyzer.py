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
    pages_df = pd.read_csv(uploaded_file)

    # Convert the "Date" column to datetime format
    pages_df["Date"] = pd.to_datetime(pages_df["Date"], format="%b %d, %Y")

    # Define the date range selector
    start_date = st.sidebar.date_input("Select a start date", default_start_date)
    end_date = st.sidebar.date_input("Select an end date", default_end_date)

    # Convert the date range to datetime format
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

    # Filter the pages data by date range
    pages_filtered = pages_df[(pages_df["Date"] >= start_date) & (pages_df["Date"] <= end_date)]

    # Select the top 5 countries by clicks
    countries_by_clicks = pages_filtered.groupby("Country")["Url Clicks"].sum().reset_index().sort_values(by="Url Clicks", ascending=False)
    top_countries = list(countries_by_clicks["Country"][:5])

    # Allow the user to select additional countries
    other_countries = list(set(countries_by_clicks["Country"]) - set(top_countries))
    selected_countries = st.sidebar.multiselect("Select countries:", top_countries + ["Other"], default=top_countries)

    if "Other" in selected_countries:
        selected_countries.remove("Other")
        selected_countries += st.sidebar.multiselect("Select additional countries:", other_countries)

    # Create a line chart of clicks by country and date for selected countries
    clicks_by_country = pages_filtered[pages_filtered["Country"].isin(selected_countries)].groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.lineplot(x="Date", y="Url Clicks", hue="Country", data=clicks_by_country, ax=ax1)
    ax1.set_title("Clicks by Country")
    st.pyplot(fig1)

    # Define the catalog selector
    catalogs = pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).unique()
    catalogs_selected = st.sidebar.multiselect("Select catalogs:", catalogs, default=catalogs)

    # Define the metric selector
    metric = st.sidebar.selectbox("Select a metric:", ["Url Clicks", "Impressions", "URL CTR"])

    # Filter the pages data by selected catalogs
    pages_catalogs = pages_filtered[pages_filtered["Landing Page"].apply(lambda x: x.split("/")[1]).isin(catalogs_selected)]

    # Pivot the pages data to create a chart of clicks by catalog and date
    pivot = pd.pivot_table(pages_catalogs, values=metric, index="Date", columns=pages_catalogs["Landing Page"].apply(lambda x: x.split("/")[1]), aggfunc=sum)
    fig2, ax2 = plt.subplots()
    pivot.plot(ax=ax2)
    ax2.set_title("Clicks by Catalog")
    st.pyplot(fig2)
