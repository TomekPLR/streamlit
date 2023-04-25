import streamlit as st
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Sidebar selectors
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV
    data = pd.read_csv(uploaded_file)

    # Convert scrap_date column to pandas datetime format
    data['scrap_date'] = pd.to_datetime(data['scrap_date'])

    now = datetime.date.today()
    initial_date = pd.Timestamp(st.sidebar.date_input('Initial date', now - datetime.timedelta(weeks=2)))
    final_date = pd.Timestamp(st.sidebar.date_input('Final date', now))
    property_filter = st.sidebar.multiselect("Select properties", data['property'].unique())

    # Add a slider to filter by relative click difference
    min_relative_diff, max_relative_diff = st.sidebar.slider("Relative click difference (%)", -100.0, 100.0, (-100.0, 100.0))

    # Filter the data based on the selected dates
    filtered_data = data[(data['scrap_date'] >= initial_date) & (data['scrap_date'] <= final_date)]

    # Filter the data based on the selected properties
    if property_filter:
        filtered_data = filtered_data[filtered_data['property'].isin(property_filter)]

    # Select columns
    variables1 = st.sidebar.multiselect("Select variables 1", filtered_data.columns)
    variables2 = st.sidebar.multiselect("Select variables 2", filtered_data.columns)

    # Select sorting order
    sort_order = st.sidebar.selectbox("Sort by correlation", ["Highest", "Lowest"])

    # Normalize option
    normalize = st.sidebar.checkbox("Normalize charts (0-1)")

    # Calculate correlations
    correlations = {}
    for var1 in variables1:
        for var2 in variables2:
            if var1 != var2:
                property_correlations = filtered_data.groupby("property").apply(lambda x: x[var1].corr(x[var2]))
                correlations[(var1, var2)] = property_correlations

    # Display charts
    st.title("Charts")

    for var1, var2 in correlations.keys():
        # Sort properties based on the correlation
        property_correlations = correlations[(var1, var2)]
        if sort_order == "Highest":
            sorted_properties = property_correlations.sort_values(ascending=False)
        else:
            sorted_properties = property_correlations.sort_values(ascending=True)

        for property in sorted_properties.index[:100]:
            click_diff = filtered_data.loc[filtered_data['property'] == property, 'clicks'].diff().sum()
            total_clicks = filtered_data.loc[filtered_data['property'] == property, 'clicks'].sum()
            relative_diff = (click_diff / total_clicks) * 100

            # Filter by relative click difference
            if min_relative_diff <= relative_diff <= max_relative_diff:
                st.header(f"Property: {property}")
                st.write(f"Correlation ({var1}, {var2}): {sorted_properties[property]}")
                st.write(f"Difference in number of clicks: {click_diff} ({relative_diff:.2f}%)")

                property_data = filtered_data[filtered_data['property'] == property]
                fig, ax = plt.subplots()

                if normalize:
                    ax.plot(property_data['scrap_date'], (property_data[var1] - property_data[var1].min()) / (property_data[var1].max() - property_data[var1].min()), label=var1)
                    ax.plot(property_data['scrap_date'], (property_data[var2] - property_data[var2].min()) / (property_data[var2].max() - property_data[var2].min()), label=var2)
                else:
                    ax.plot(property_data['scrap_date'], property_data[var1], label=var1)
                    ax.plot(property_data['scrap_date'], property_data[var2], label=var2)

                # Set x-axis date format
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                # Rotate date labels
                plt.xticks(rotation=45)

                ax.legend()
                st.pyplot(fig)

else:
    st.sidebar.warning("Please upload a CSV file.")  
                                                                                                              
