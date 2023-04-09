import streamlit as st
import pandas as pd
import datetime

def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
    return df

def filter_by_date(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def get_weekly_data(df, column):
    df['week'] = pd.to_datetime(df['scrap_date']).dt.isocalendar().week
    weekly_data = df.groupby(['property', 'week'])[column].sum().reset_index()
    return weekly_data

def find_biggest_movers(weekly_data, num_properties, ascending):
    weekly_data['week_diff'] = weekly_data.groupby('property')[column].diff()
    weekly_data['rel_diff'] = (weekly_data['week_diff'] / (weekly_data[column] - weekly_data['week_diff'])) * 100
    movers = weekly_data.sort_values('week_diff', ascending=ascending).head(num_properties)
    return movers

def main():
    st.title('Biggest Movers in Selected Metric')

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = read_csv(uploaded_file)

        st.sidebar.header('Select Date Range')
        time_frames = ['Last week', 'Last month', 'Last year', 'Custom']
        selected_time_frame = st.sidebar.selectbox('Choose a time frame', time_frames)

        today = datetime.date.today()
        start_date = end_date = None

        if selected_time_frame == 'Last week':
            start_date = today - datetime.timedelta(weeks=1)
            end_date = today
        elif selected_time_frame == 'Last month':
            start_date = today - datetime.timedelta(weeks=4)
            end_date = today
        elif selected_time_frame == 'Last year':
            start_date = today - datetime.timedelta(weeks=52)
            end_date = today
        elif selected_time_frame == 'Custom':
            start_date = st.sidebar.date_input("Start date", value=today - datetime.timedelta(weeks=1))
            end_date = st.sidebar.date_input("End date", value=today)

        num_properties = st.sidebar.slider('Number of properties to show', min_value=1, max_value=100, value=10, step=1)

        column = st.sidebar.selectbox('Select a column to analyze', df.columns)

        if df[column].dtype not in ('int64', 'float64'):
            st.error(f"Selected column '{column}' is not numeric. Please choose a numeric column.")
            return

        filtered_df = filter_by_date(df, start_date, end_date)
        weekly_data = get_weekly_data(filtered_df, column)

        biggest_losers = find_biggest_movers(weekly_data, num_properties, ascending=True)
        biggest_winners = find_biggest_movers(weekly_data, num_properties, ascending=False)

        st.header(f'Biggest Losers in {column} per Week (Top {num_properties})')
        st.write(biggest_losers)

        st.header(f'Biggest Winners in {column} per Week (Top {num_properties})')
        st.write(biggest_winners)

if __name__ == '__main__':
    main()
