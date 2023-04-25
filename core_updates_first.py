import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime

st.title('CSV Analysis - Property Click Losses')

important_dates = {
    # (same content as before)
    '2022-12-14': 'Dec 2022 link spam update',
    '2022-12-05': 'Dec 2022 helpful content update',
    '2022-10-19': 'Oct 2022 spam update',
    '2022-09-20': 'Sep 2022 product reviews update',
    '2022-09-12': 'Sep 2022 core update',
    '2022-08-25': 'Aug 2022 helpful content update',
    '2022-07-27': 'Jul 2022 product reviews update',
    '2022-05-25': 'May 2022 core update',
    '2022-03-23': 'Mar 2022 product reviews update',
    '2022-02-22': 'Feb 2022 page experience update for desktop'
}

# Convert the keys to datetime objects
important_dates = {pd.to_datetime(k): v for k, v in important_dates.items()}

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
    data['date'] = data['scrap_date'].dt.date

    initial_date = st.sidebar.date_input('Initial Date', data['date'].min())
    final_date = st.sidebar.date_input('Final Date', data['date'].max())

    additional_dates = st.sidebar.text_area("Add additional important dates (YYYY-MM-DD:description, one per line):")

    if additional_dates:
        additional_dates_list = additional_dates.split('\n')
        for date_entry in additional_dates_list:
            date, description = date_entry.split(':')
            important_dates[pd.to_datetime(date)] = description

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        filtered_data = data[(data['date'] >= initial_date) & (data['date'] <= final_date)]

        property_filter = st.sidebar.text_input('Filter properties by name (contains):', '')
        if property_filter:
            filtered_data = filtered_data[filtered_data['property'].str.contains(property_filter)]

        threshold = st.sidebar.number_input('Minimum average number of clicks:', value=0)

        selected_dates = st.sidebar.multiselect('Select important dates to display:',
                                                list(important_dates.values()),
                                                default=list(important_dates.values()))

        filtered_properties = filtered_data['property'].unique()
        st.write(f"Found {len(filtered_properties)} properties")

        drop_summary = []

        for property_name in filtered_properties:
            selected_property = filtered_data[filtered_data['property'] == property_name]
            start_clicks = selected_property[selected_property['date'] == initial_date]['clicks'].mean()
            end_clicks = selected_property[selected_property['date'] == final_date]['clicks'].mean()

            if start_clicks is not None and end_clicks is not None:
                drop_percentage = ((start_clicks - end_clicks) / start_clicks) * 100
                drop_summary.append((property_name, drop_percentage))

        sorted_properties = sorted(drop_summary, key=lambda x: x[1], reverse=True)

        for property_name, drop_percentage in sorted_properties:
            selected_property = filtered_data[filtered_data['property'] == property_name]

            if selected_property['clicks'].mean() >= threshold:
                fig, ax = plt.subplots()

                ax.plot(selected_property['scrap_date'], selected_property['clicks'], label=property_name)
                ax.set_xlabel('Scrap Date')
                ax.set_ylabel('Clicks')
                ax.set_title(f'{property_name} Clicks over Time ({drop_percentage:.2f}% drop)', pad=20)

                for event_date, event_description in important_dates.items():
                    if event_description in selected_dates:
                        ax.axvline(pd.Timestamp(event_date), color='red', linestyle='--', alpha=0.5)
                        ax.annotate(event_description,
                                    xy=(pd.Timestamp(event_date), ax.get_ylim()[1]),
                                    xytext=(pd.Timestamp(event_date), ax.get_ylim()[1] * 1.1),
                                    rotation=45,
                                    ha='left', va='bottom', fontsize=8,
                                    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
                                    arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.5))

                ax.legend(loc='upper left', fontsize=8)
                ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
