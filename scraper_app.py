import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def read_csv(uploaded_file):
    return pd.read_csv(uploaded_file, parse_dates=['scrap_date'])

def filter_data(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def calculate_changes(df, column):
    initial_values = df.groupby('property')[column].first()
    final_values = df.groupby('property')[column].last()
    abs_changes = final_values - initial_values
    rel_changes = (final_values - initial_values) / initial_values * 100
    
    results = pd.concat([initial_values, final_values, abs_changes, rel_changes], axis=1)
    results.columns = ['initial_value', 'final_value', 'abs_change', 'rel_change']
    results = results.reset_index()
    return results

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

        st.header(f'Top 10 properties with increased {column} values')
        results = calculate_changes(filtered_df, column)
        top_10_winners = results.nlargest(10, 'abs_change')
        st.dataframe(top_10_winners)

        st.header(f'Top 10 properties with decreased {column} values')
        top_10_losers = results.nsmallest(10, 'abs_change')
        st.dataframe(top_10_losers)

if __name__ == '__main__':
    main()
