import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

st.set_page_config(layout="wide")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file:", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file.")
    st.stop()

data = pd.read_csv(uploaded_file)

data['scrap_date'] = pd.to_datetime(data['scrap_date'])

st.sidebar.title("Input Parameters")
initial_date = st.sidebar.date_input("Initial date", value=pd.to_datetime("2023-04-08") - pd.DateOffset(weeks=2))
final_date = st.sidebar.date_input("Final date", value=pd.to_datetime("2023-04-08"))

initial_date = pd.to_datetime(initial_date)
final_date = pd.to_datetime(final_date)

filtered_data = data[(data['scrap_date'] >= initial_date) & (data['scrap_date'] <= final_date)]

variable1 = st.sidebar.selectbox("Select variable 1:", data.columns)
variable2 = st.sidebar.selectbox("Select variable 2:", data.columns)
property_filter = st.sidebar.text_input("Filter properties (comma-separated):", value="")
normalize = st.sidebar.checkbox("Normalize charts (0-1)")

if property_filter:
    properties = [p.strip() for p in property_filter.split(",")]
    filtered_data = filtered_data[filtered_data['property'].isin(properties)]

top_n = st.sidebar.slider("Number of results:", min_value=1, max_value=100, value=100)

correlation_type = st.sidebar.radio("Select correlation type:", options=["Highest", "Lowest"])

numeric_data = filtered_data[[variable1, variable2]].apply(pd.to_numeric, errors='coerce').dropna()

if correlation_type == "Highest":
    sorted_data = numeric_data.sort_values(by=[variable1, variable2], ascending=[False, False])
else:
    sorted_data = numeric_data.sort_values(by=[variable1, variable2], ascending=[True, True])

sorted_data = sorted_data.head(top_n)

correlations = []

for index, row in sorted_data.iterrows():
    x = filtered_data.loc[index, variable1]
    y = filtered_data.loc[index, variable2]

    if len(x) > 1 and len(y) > 1:
        corr, _ = pearsonr(x, y)
        correlations.append((index, corr))

sorted_data["correlation"] = correlations

for idx, row in sorted_data.iterrows():
    st.write(f"Property: {data.loc[idx, 'property']}")
    st.write(f"Correlation: {row['correlation']}")

    fig, ax = plt.subplots()

    if normalize:
        ax.plot((filtered_data.loc[idx, 'scrap_date'] - initial_date) / (final_date - initial_date), filtered_data.loc[idx, variable1] / np.max(filtered_data.loc[idx, variable1]), label=variable1)
        ax.plot((filtered_data.loc[idx, 'scrap_date'] - initial_date) / (final_date - initial_date), filtered_data.loc[idx, variable2] / np.max(filtered_data.loc[idx, variable2]), label=variable2)
    else:
        ax.plot(filtered_data.loc[idx, 'scrap_date'], filtered_data.loc[idx, variable1], label=variable1)
        ax.plot(filtered_data.loc[idx, 'scrap_date'], filtered_data.loc[idx, variable2], label=variable2)

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    st.pyplot(fig)
