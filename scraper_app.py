import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt

def read_csv(uploaded_files):
    dfs = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
        dfs.append(df)
    return pd.concat(dfs, axis=0)

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

    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        df = read_csv(uploaded_files)

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

        st.header("Property Details")
        specific_property = st.selectbox("Select a property", [""] + list(df["property"].unique()))

        if specific_property:
            property_df = df[df["property"] == specific_property]

            st.sidebar.header("Property chart settings")
            normalize = st.sidebar.checkbox("Normalize data (0-1)")

            chart_start_date = st.sidebar.date_input("Chart initial date", property_df["scrap_date"].min(),
                                                     min_value=property_df["scrap_date"].min(),
                                                     max_value=property_df["scrap_date"].max())
            chart_end_date = st.sidebar.date_input("Chart final date", property_df["scrap_date"].max(),
                                                   min_value=property_df["scrap_date"].min(),
                                                   max_value=property_df["scrap_date"].max())

            if chart_start_date > chart_end_date:
                st.sidebar.error("Error: Chart final date must be after initial date.")
                return

            property_df = filter_data(property_df, chart_start_date, chart_end_date)

            if normalize:
                property_df["clicks"] = (property_df["clicks"] - property_df["clicks"].min()) / (
                            property_df["clicks"].max() - property_df["clicks"].min())
                property_df["response_ok"] = (property_df["response_ok"] - property_df["response_ok"].min()) / (
                            property_df["response_ok"].max() - property_df["response_ok"].min())

            line_chart = alt.Chart(property_df).mark_line().encode(
                x="scrap_date:T",
                y=alt.Y("clicks:Q", title="Clicks (Normalized)" if normalize else "Clicks"),
                color=alt.value("blue"),
            ) + alt.Chart(property_df).mark_line().encode(
                x="scrap_date:T",
                y=alt.Y("response_ok:Q", title="Response OK (Normalized)" if normalize else "Response OK"),
                color=alt.value("red"),
            )

            st.altair_chart(line_chart, use_container_width=True)

if __name__ == '__main__':
    main()

