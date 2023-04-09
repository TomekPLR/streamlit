import streamlit as st
import pandas as pd
import altair as alt

def normalize_columns(df, columns):
    normalized_df = df.copy()
    for column in columns:
        min_value = df[column].min()
        max_value = df[column].max()
        normalized_df[column] = (df[column] - min_value) / (max_value - min_value)
    return normalized_df

def main():
    st.title("Normalized Single Chart Multi-column Visualization")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
        df['scrap_date'] = df['scrap_date'].dt.date

        st.subheader("Data preview")
        st.write(df.head())

        st.subheader("Select property")
        properties = df['property'].unique()
        selected_property = st.selectbox("Choose a property", properties)

        st.subheader("Select columns to visualize")
        column_options = st.multiselect("Choose columns", df.columns, default=['clicks', 'impressions'])

        st.subheader("Select date range")
        min_date = df['scrap_date'].min()
        max_date = df['scrap_date'].max()
        start_date = st.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("End date", max_date, min_value=min_date, max_value=max_date)

        if len(column_options) > 0:
            st.subheader("Chart")
            filtered_df = df[(df['property'] == selected_property) & (df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]
            normalized_df = normalize_columns(filtered_df, column_options)
            chart_data = normalized_df[['scrap_date'] + column_options].melt('scrap_date', var_name='variable', value_name='value')
            chart = alt.Chart(chart_data).mark_line().encode(
                x='scrap_date:T',
                y='value:Q',
                color=alt.Color('variable:N', legend=alt.Legend(title="Column"))
            ).properties(
                width=800,
                height=400
            ).interactive()

            st.altair_chart(chart)

if __name__ == "__main__":
    main()
