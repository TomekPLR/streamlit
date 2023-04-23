import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime

st.title('CSV Analysis - Property Click Losses')

important_dates = {
    # (same content as before)
}

# Convert the keys to datetime objects
important_dates = {pd.to_datetime(k): v for k, v in important_dates.items()}

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
    data['date'] = data['scrap_date'].dt.date

    initial_date = st.sidebar.date_input('Initial Date', data['date'].min())
    final_date = st.sidebar.date_input('Final Date', data['date'].max())

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        filtered_data = data[(data['date'] >= initial_date) & (data['date'] <= final_date)]

        property_filter = st.sidebar.text_input('Filter properties by name (contains):', '')
        if property_filter:
            filtered_data = filtered_data[filtered_data['property'].str.contains(property_filter)]

        threshold = st.sidebar.number_input('Minimum average number of clicks:', value=0)

        filtered_properties = filtered_data['property'].unique()
        st.write(f"Found {len(filtered_properties)} properties")

        for property_name in filtered_properties:
            selected_property = filtered_data[filtered_data['property'] == property_name]

            if selected_property['clicks'].mean() >= threshold:
                fig, ax = plt.subplots()

                ax.plot(selected_property['scrap_date'], selected_property['clicks'], label=property_name)
                ax.set_xlabel('Scrap Date')
                ax.set_ylabel('Clicks')
                ax.set_title(f'{property_name} Clicks over Time', pad=20)

                for event_date, event_description in important_dates.items():
                    ax.axvline(pd.Timestamp(event_date), color='red', linestyle='--', alpha=0.5)
                    ax.annotate(event_description,
                                xy=(pd.Timestamp(event_date), ax.get_ylim()[1] * 1.05),
                                xytext=(pd.Timestamp(event_date), ax.get_ylim()[1] * 1.15),
                                rotation=45,
                                ha='left', va='bottom', fontsize=8,
                                arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.5))

                ax.legend(loc='upper left', fontsize=8)
                ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)