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
