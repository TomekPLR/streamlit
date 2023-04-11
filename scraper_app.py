import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def read_csv(uploaded_files):
    dfs = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def filter_data(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def normalize_0_to_1(series):
    min_value = series.min()
    max_value = series.max()
    return (series - min_value) / (max_value - min_value)

# ... [the rest of the functions from previous response] ...

def main():
    st.title('CSV Analysis Tool')

    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        df = read_csv(uploaded_files)

        # Filter data
        min_date, max_date = df['scrap_date'].min(), df['scrap_date'].max()
        start_date = st.sidebar.date_input('Initial date', min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input('Final date', max_date, min_value=min_date, max_value=max_date)
        if start_date > end_date:
            st.sidebar.error('Error: Final date must be after initial date.')
            return

        filtered_df = filter_data(df, start_date, end_date)

        # Select a column
        column = st.sidebar.selectbox('Choose a column', df.columns)

        # Calculate changes
        results = calculate_changes(filtered_df, column)

        # Property filter
        property_filter = st.sidebar.text_input('Property contains', '')
        selected_property = st.sidebar.selectbox('Select a property', [''] + list(df['property'].unique()))
        results = filter_properties(results, property_filter, selected_property)

        # Report settings
        num_properties = st.sidebar.number_input('Number of reported properties', min_value=1, value=10, step=1)

        # Display top winners and losers
        top_winners = results.nlargest(num_properties, 'abs_change')
        top_losers = results.nsmallest(num_properties, 'abs_change')
        st.dataframe(top_winners)
        st.dataframe(top_losers)

        # Property-specific chart
        property_to_analyze = st.selectbox("Select property to analyze", df['property'].unique())
        if property_to_analyze:
            other_column = st.selectbox("Select another column to compare", list(df.columns[df.columns != 'clicks']))
            normalize = st.checkbox("Normalize data")
            property_df = df[df['property'] == property_to_analyze].sort_values(by='scrap_date')

            fig, ax = plt.subplots()
            if 'clicks' in property_df.columns:
                if normalize:
                    property_df['clicks_normalized'] = normalize_0_to_1(property_df['clicks'])
                    property_df[other_column + '_normalized'] = normalize_0_to_1(property_df[other_column])

                    ax.plot(property_df['scrap_date'], property_df['clicks_normalized'], label='Clicks (normalized)')
                    ax.plot(property_df['scrap_date'], property_df[other_column + '_normalized'], label=other_column + ' (normalized)')

                else:
                                        ax.plot(property_df['scrap_date'], property_df['clicks'], label='Clicks')
                    ax.plot(property_df['scrap_date'], property_df[other_column], label=other_column)

            else:
                if normalize:
                    property_df[other_column + '_normalized'] = normalize_0_to_1(property_df[other_column])
                    ax.plot(property_df['scrap_date'], property_df[other_column + '_normalized'], label=other_column + ' (normalized)')

                else:
                    ax.plot(property_df['scrap_date'], property_df[other_column], label=other_column)

            ax.set(xlabel='Date', ylabel='Values', title=f'{property_to_analyze} - Clicks and {other_column}')
            ax.legend()
            st.pyplot(fig)

if __name__ == '__main__':
    main()

