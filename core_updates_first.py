import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from matplotlib.dates import DateFormatter

st.title('CSV Analysis - Property Clicks Over Time')

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
    data['date'] = data['scrap_date'].dt.date

    # Extract hours from last_update column
    data['hours_ago'] = data['last_update'].apply(lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

    # Update scrap_date based on last_update column
    data['scrap_date'] = data['scrap_date'] - pd.to_timedelta(data['hours_ago'], unit='h')

    initial_date = st.sidebar.date_input('Initial Date', data['date'].min())
    final_date = st.sidebar.date_input('Final Date', data['date'].max())

    if initial_date > final_date:
        st.error("Initial date should be before final date.")
    else:
        filtered_data = data[(data['date'] >= initial_date) & (data['date'] <= final_date)]

        # Add a multiselect widget to filter properties
        property_filter = st.sidebar.multiselect('Select properties:', filtered_data['property'].unique(), default=filtered_data['property'].unique())

        filtered_data = filtered_data[filtered_data['property'].isin(property_filter)]

        # Create a list of dates and labels for the updates
        updates = [
            ('2022-12-14', 'Dec 2022 Link Spam Update'),
            ('2022-12-05', 'Dec 2022 Helpful Content Update'),
            ('2022-10-19', 'Oct 2022 Spam Update'),
            ('2022-09-20', 'Sep 2022 Product Reviews Update'),
            ('2022-09-12', 'Sep 2022 Core Update'),
            ('2022-08-25', 'Aug 2022 Helpful Content Update'),
            ('2022-07-27', 'Jul 2022 Product Reviews Update'),
            ('2022-05-25', 'May 2022 Core Update'),
            ('2022-03-23', 'Mar 2022 Product Reviews Update'),
            ('2022-02-22', 'Feb 2022 Page Experience Update'),
        ]

        for property_name, group in filtered_data.groupby('property'):
            fig, ax = plt.subplots()
            ax.plot(group['scrap_date'], group['clicks'], label=property_name)

            for date, label in updates:
                update_date = pd.to_datetime(date)
                if initial_date <= update_date.date() <= final_date:
                    ax.axvline(update_date, linestyle='--', color='gray')
                    ax.annotate(label, xy=(update_date, ax.get_ylim()[1]), xycoords='data', xytext=(0, 5), textcoords='offset points', rotation=90, va='bottom', ha='center', fontsize=8)

            ax.set_xlabel('Scrap Date')
            ax.set_ylabel('Clicks')
            ax.set_title(f'{property_name} Clicks Over Time')
            ax.legend(loc='upper left', fontsize=8)
            ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
