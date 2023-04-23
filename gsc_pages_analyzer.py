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
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')

    # Filter the pages data by date range
    pages_filtered = pages_df[(pages_df["Date"] >= start_date) & (pages_df["Date"] <= end_date)]

    # Create a line chart of clicks by country and date
    clicks_by_country = pages_filtered.groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()
    top_countries = clicks_by_country.groupby("Country")["Url Clicks"].sum().sort_values(ascending=False).head(10)
    countries_selected = st.sidebar.multiselect("Select countries:", top_countries.index.tolist(), default=top_countries.index.tolist()[:5])
    clicks_by_country_selected = clicks_by_country[clicks_by_country["Country"].isin(countries_selected)]
    fig1, ax1 = plt.subplots()
    sns.lineplot(x="Date", y="Url Clicks", hue="Country", data=clicks_by_country_selected, ax=ax1)
    ax1.set_title("Clicks by Country")
    st.pyplot(fig1)

    # Define the catalog selector
    pages_catalogs = pages_filtered.copy()
    pages_catalogs["Catalog"] = pages_catalogs["Landing Page"].apply(lambda x: x.split("/")[3] if len(x.split("/"))>=4 else "")
    catalogs = pages_catalogs["Catalog"].unique()
    catalogs_selected = st.sidebar.multiselect("Select catalogs:", catalogs, default=catalogs)

    # Define the metric selector
    metric = st.sidebar.selectbox("Select a metric:", ["Url Clicks", "Impressions", "URL CTR"])

    # Filter the pages data by selected catalogs
    pages_catalogs_selected = pages_catalogs[pages_catalogs["Catalog"].isin(catalogs_selected)]

    # Pivot the pages data to create a chart of clicks by catalog and date
    pivot = pd.pivot_table(pages_catalogs_selected, values=metric, index="Date", columns="Catalog", aggfunc=sum)
    fig2, ax2 = plt.subplots()
    pivot.plot(ax=ax2)
    ax2.set_title("Clicks by Catalog")
    st.pyplot(fig2)
