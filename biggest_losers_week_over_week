import streamlit as st
import pandas as pd
import datetime

def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
    return df

def filter_by_date(df, start_date, end_date):
    return df[(df['scrap_date'] >= start_date) & (df['scrap_date'] <= end_date)]

def get_weekly_clicks(df):
    df['week'] = pd.to_datetime(df['scrap_date']).dt.isocalendar().week
    weekly_clicks = df.groupby(['property', 'week'])['clicks'].sum().reset_index()
    return weekly_clicks

def find_biggest_losers(weekly_clicks):
    weekly_clicks['week_diff'] = weekly_clicks.groupby('property')['clicks'].diff()
    losers = weekly_clicks.sort_values('week_diff').head(10)
    return losers

def main():
    st.title('Biggest Losers in Clicks')

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

        filtered_df = filter_by_date(df, start_date, end_date)
        weekly_clicks = get_weekly_clicks(filtered_df)
        biggest_losers = find_biggest_losers(weekly_clicks)

        st.header('Biggest Losers in Clicks per Week')
        st.write(biggest_losers)

if __name__ == '__main__':
    main()
