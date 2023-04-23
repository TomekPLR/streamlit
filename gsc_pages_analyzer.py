import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    pages_df = pd.read_csv(uploaded_file)

    # Convert the "Date" column to datetime format
    pages_df["Date"] = pd.to_datetime(pages_df["Date"], format="%b %d, %Y")

    # Define the date range selector
    date_range = st.sidebar.date_input("Select a date range:", [pages_df["Date"].min(), pages_df["Date"].max()])

    # Filter the pages data by date range
    pages_filtered = pages_df[(pages_df["Date"] >= date_range[0]) & (pages_df["Date"] <= date_range[1])]

    # Define the country selector
    countries = st.sidebar.multiselect("Select countries:", pages_filtered["Country"].unique())

    # Filter the pages data by selected countries
    if countries:
        pages_filtered = pages_filtered[pages_filtered["Country"].isin(countries)]

    # Create a bar chart of clicks by country and date
    clicks_by_country = pages_filtered.groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.barplot(x="Date", y="Url Clicks", hue="Country", data=clicks_by_country, ax=ax1)
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
