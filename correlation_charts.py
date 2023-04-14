import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

# Read the CSV file
df = pd.read_csv("your_csv_file.csv")

# Set default dates
today = pd.Timestamp.today()
default_start_date = (today - pd.Timedelta(weeks=2)).strftime("%Y-%m-%d")
default_end_date = today.strftime("%Y-%m-%d")

# Sidebar inputs
start_date = st.sidebar.date_input("Start date", pd.to_datetime(default_start_date))
end_date = st.sidebar.date_input("End date", pd.to_datetime(default_end_date))
variable1 = st.sidebar.selectbox("Variable 1", df.columns)
variable2 = st.sidebar.selectbox("Variable 2", df.columns)
property = st.sidebar.selectbox("Property", df["property"].unique(), index=0)
num_results = st.sidebar.number_input("Number of results", min_value=1, max_value=len(df), value=100)

# Filter the data by date and property
mask = (df["scrap_date"] >= start_date) & (df["scrap_date"] <= end_date)
if property != "All":
    mask &= df["property"] == property
filtered_df = df.loc[mask]

# Calculate the correlation between variable1 and variable2 for each property
correlations = filtered_df.groupby("property")[variable1, variable2].corr().iloc[::2, -1]
sorted_properties = correlations.sort_values(ascending=False).index[:num_results]

# Display the plots and text information for each property
for prop in sorted_properties:
    prop_df = filtered_df[filtered_df["property"] == prop]
    x = prop_df[variable1]
    y = prop_df[variable2]
    corr = correlations[prop]
    diff_clicks = prop_df["clicks_after"].sum() - prop_df["clicks_before"].sum()
    diff_var1 = prop_df[variable1].max() - prop_df[variable1].min()
    diff_var2 = prop_df[variable2].max() - prop_df[variable2].min()

    # Normalize x and y to be between 0 and 1
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())

    # Plot the normalized data
    fig, ax = plt.subplots()
    sns.scatterplot(x=x_norm, y=y_norm, ax=ax)
    ax.set_title(f"{prop} (Corr: {corr:.2f})")
    st.pyplot(fig)

    # Display the text information
    st.write(f"Difference in clicks: {diff_clicks}")
    st.write(f"Difference in {variable1}: {diff_var1}")
    st.write(f"Difference in {variable2}: {diff_var2}")
