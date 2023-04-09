import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.title("Multi-column Chart Visualization")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])
        df['scrap_date'] = df['scrap_date'].dt.date

        st.subheader("Data preview")
        st.write(df.head())

        st.subheader("Select columns to visualize")
        column_options = st.multiselect("Choose columns", df.columns, default=['clicks', 'impressions'])

        if len(column_options) > 0:
            st.subheader("Chart")
            chart_data = df[['scrap_date'] + column_options]
            chart = alt.Chart(chart_data).mark_line().encode(
                x='scrap_date:T',
                y=alt.Y(alt.repeat("column"), type='quantitative'),
                color=alt.Color('variable:N', legend=alt.Legend(title="Column"))
            ).properties(
                width=800,
                height=400
            ).repeat(
                column=column_options
            ).interactive()

            st.altair_chart(chart)

if __name__ == "__main__":
    main()
