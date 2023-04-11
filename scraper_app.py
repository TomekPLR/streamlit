import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
    return df

def filter_data(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def calculate_changes(df, column):
    if not np.issubdtype(df[column].dtype, np.number):
        raise ValueError("Selected column must be of numeric data type")

    initial_values = df.groupby('property')[column].first()
    final_values = df.groupby('property')[column].last()
    abs_changes = final_values - initial_values
    rel_changes = (final_values - initial_values) / initial_values * 100

    results = pd.concat([initial_values, final_values, abs_changes, rel_changes], axis=1)
    results.columns = ['initial_value', 'final_value', 'abs_change', 'rel_change']
    results = results.reset_index()
    return results

def filter_properties(df, property_filter, selected_property):
    if property_filter:
        df = df[df['property'].str.contains(property_filter)]
    if selected_property:
        df = df[df['property'] == selected_property]
    return df

def main():
    st.title('CSV Analysis Tool')

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = read_csv(uploaded_file)

        st.sidebar.header('Filter data')
        min_date, max_date = df['scrap_date'].min(), df['scrap_date'].max()
        start_date = st.sidebar.date_input('Initial date', min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input('Final date', max_date, min_value=min_date, max_value=max_date)
        if start_date > end_date:
            st.sidebar.error('Error: Final date must be after initial date.')
            return

        filtered_df = filter_data(df, start_date, end_date)

        st.sidebar.header('Select a column')
        column = st.sidebar.selectbox('Choose a column', df.columns)

        try:
            results = calculate_changes(filtered_df, column)
        except ValueError as e:
            st.sidebar.error(str(e))
            return

        st.sidebar.header('Property filter')
        property_filter = st.sidebar.text_input('Property contains', '')
        selected_property = st.sidebar.selectbox('Select a property', [''] + list(df['property'].unique()))
        results = filter_properties(results, property_filter, selected_property)

        st.sidebar.header('Report settings')
        num_properties = st.sidebar.number_input('Number of reported properties', min_value=1, value=10, step=1)

        st.header(f'Top {num_properties} properties with increased {column} values')
        top_winners = results.nlargest(num_properties, 'abs_change')
        st.dataframe(top_winners)

        st.header(f'Top {num_properties} properties with decreased {column} values')
        top_losers = results.nsmallest(num_properties, 'abs_change')
        st.dataframe(top_losers)

        st.header('Property-specific chart')
        property_to_plot = st.selectbox('Select a property to plot', [''] + list(df['property'].unique()))
        normalize = st.checkbox('Normalize data')
         start_date_chart = st.date_input('Initial date for chart', min_date, min_value=min_date, max_value=max_date)
        end_date_chart = st.date_input('Final date for chart', max_date, min_value=min_date, max_value=max_date)

        if property_to_plot:
            property_df = filter_data(df[df['property'] == property_to_plot], start_date_chart, end_date_chart)

            if 'clicks' in property_df.columns:
                fig, ax = plt.subplots()

                # Plot clicks data
                ax.plot(property_df['scrap_date'], property_df['clicks'], label='Clicks')

                # Choose another column to plot
                other_column = 'avg_response_time'  # Change this to the column you want to plot
                if other_column in property_df.columns:
                    ax.plot(property_df['scrap_date'], property_df[other_column], label=other_column)

                if normalize:
                    ax.set_yscale('log')

                ax.legend()
                ax.set_xlabel('Date')
                ax.set_ylabel('Value')
                ax.set_title(f'Property: {property_to_plot}')

                st.pyplot(fig)
            else:
                st.write(f"No 'clicks' data available for property {property_to_plot}.")

if __name__ == '__main__':
    main()
