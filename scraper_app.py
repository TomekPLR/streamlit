import streamlit as st
import pandas as pd
import numpy as np
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

def join_dataframes(df_list):
    df = pd.concat(df_list, axis=0).reset_index(drop=True)
    return df

@st.cache
def get_unique_dates(df):
    return df['scrap_date'].min(), df['scrap_date'].max()

def main():
    st.title('CSV Analysis Tool')

    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        dfs = [read_csv(f) for f in uploaded_files]
        df = join_dataframes(dfs)

        min_date, max_date = get_unique_dates(df)

        st.sidebar.header('Filter data')
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

        # Chart section
        st.header("Property-specific chart")
                specific_property = st.selectbox("Select a property", [""] + list(df["property"].unique()))
        if specific_property:
            property_data = df[df["property"] == specific_property]

            st.subheader(f"Chart for property: {specific_property}")

            chart_columns = st.multiselect("Select columns to plot", options=df.columns, default=["clicks"])

            min_chart_date, max_chart_date = get_unique_dates(property_data)
            chart_start_date = st.date_input("Chart start date", min_chart_date, min_value=min_chart_date, max_value=max_chart_date)
            chart_end_date = st.date_input("Chart end date", max_chart_date, min_value=min_chart_date, max_value=max_chart_date)

            if chart_start_date > chart_end_date:
                st.error("Error: Chart end date must be after chart start date.")
            else:
                property_chart_data = filter_data(property_data, chart_start_date, chart_end_date)

                normalize = st.checkbox("Normalize values")

                if normalize:
                    property_chart_data[chart_columns] = (property_chart_data[chart_columns] - property_chart_data[chart_columns].min()) / (property_chart_data[chart_columns].max() - property_chart_data[chart_columns].min())

                chart = alt.Chart(property_chart_data).mark_line().encode(
                    x="scrap_date:T",
                    y=alt.Y(alt.repeat("row"), type="quantitative"),
                    color="property:N"
                ).properties(
                    width=600,
                    height=200
                ).repeat(
                    row=chart_columns
                ).interactive()

                st.altair_chart(chart)

if __name__ == "__main__":
    main()

