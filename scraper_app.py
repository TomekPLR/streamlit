import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def read_csv(uploaded_files):
    dfs = []

    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
        dfs.append(df)

    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    return combined_df

def filter_data(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def calculate_changes(df, column, clicks_column='clicks'):
    if not np.issubdtype(df[column].dtype, np.number):
        raise ValueError("Selected column must be of numeric data type")

    initial_values = df.groupby('property')[column].first()
    final_values = df.groupby('property')[column].last()
    abs_changes = final_values - initial_values
    rel_changes = (final_values - initial_values) / initial_values * 100

    results = pd.concat([initial_values, final_values, abs_changes, rel_changes], axis=1)
    results.columns = ['initial_value', 'final_value', 'abs_change', 'rel_change']

    if clicks_column in df.columns:
        initial_clicks = df.groupby('property')[clicks_column].first()
        final_clicks = df.groupby('property')[clicks_column].last()
        click_changes = final_clicks - initial_clicks
        rel_click_changes = (final_clicks - initial_clicks) / initial_clicks * 100

        results = pd.concat([results, click_changes, rel_click_changes], axis=1)
        results.columns = ['initial_value', 'final_value', 'abs_change', 'rel_change', 'clicks_change', 'rel_clicks_change']

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

    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files is not None:
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

if __name__ == '__main__':
    main()
