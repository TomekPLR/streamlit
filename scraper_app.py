import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

def read_csv(uploaded_files):
    df_list = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
        df_list.append(df)
    
    df = pd.concat(df_list, ignore_index=True)
    return df

def filter_data(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def get_unique_dates(df):
    return df['scrap_date'].min(), df['scrap_date'].max()

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

def main():
    st.title('CSV Analysis Tool')

    uploaded_files = st.file_uploader("Upload CSV file(s)", type="csv", accept_multiple_files=True)
    if uploaded_files:
        df = read_csv(uploaded_files)

        st.sidebar.header('Filter data')
        min_date, max_date = get_unique_dates(df)
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

        st.sidebar.header('Report settings')
        num_properties = st.sidebar.number_input('Number of reported properties', min_value=1, value=10, step=1)

        st.header(f'Top {num_properties} properties with increased {column} values')
        top_winners = results.nlargest(num_properties, 'abs_change')
        st.dataframe(top_winners)

        st.header(f'Top {num_properties} properties with decreased {column} values')
        top_losers = results.nsmallest(num_properties, 'abs_change')
        st.dataframe(top_losers)

        specific_property = st.selectbox("Select a property", [""] + list(df["property"].unique()))
        if specific_property:
            property_data = df[df["property"] == specific_property]

            st.subheader(f"Chart for property: {specific_property}")

            chart_columns = st.multiselect("Select columns to plot", options=df.columns, default=["clicks"])

            min_chart_date, max_chart_date = get_unique_dates(property_data)
                        chart_start_date = st.date_input('Chart start date', min_chart_date, min_value=min_chart_date, max_value=max_chart_date)
            chart_end_date = st.date_input('Chart end date', max_chart_date, min_value=min_chart_date, max_value=max_chart_date)
            if chart_start_date > chart_end_date:
                st.error('Error: Chart end date must be after chart start date.')
            else:
                chart_data = filter_data(property_data, chart_start_date, chart_end_date)

                if st.checkbox("Normalize data"):
                    for col in chart_columns:
                        if np.issubdtype(chart_data[col].dtype, np.number):
                            chart_data[col] = (chart_data[col] - chart_data[col].min()) / (chart_data[col].max() - chart_data[col].min())

                chart_data = chart_data.melt(id_vars=['scrap_date'], value_vars=chart_columns, var_name='column', value_name='value')

                line_chart = alt.Chart(chart_data).mark_line().encode(
                    alt.X('scrap_date:T', title='Scrap Date'),
                    alt.Y('value:Q', title='Value'),
                    alt.Color('column:N', title='Column'),
                    tooltip=['scrap_date', 'column', 'value']
                ).interactive()

                st.altair_chart(line_chart, use_container_width=True)

if __name__ == '__main__':
    main()

