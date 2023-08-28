import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_trends(df, columns, filter_dates):
    for col in columns:
        plt.figure(figsize=(12, 6))

        # Convert filter_dates to Pandas Timestamp for compatible filtering
        filter_start = pd.Timestamp(filter_dates[0])
        filter_end = pd.Timestamp(filter_dates[1])

        # Filter based on selected date range
        df_filtered = df[(df['scrap_date'] >= filter_start) & (df['scrap_date'] <= filter_end)]

        plt.scatter(df_filtered['scrap_date'], df_filtered[col], label='Data Points')

        # Adding Trendline
        z = np.polyfit(df_filtered.index, df_filtered[col], 1)
        p = np.poly1d(z)
        plt.plot(df_filtered['scrap_date'], p(df_filtered.index), 'r--', label='Trendline')

        plt.title(f"Trendline for {col}")
        plt.xlabel("Scrap Date")
        plt.ylabel(f"{col} (%)")
        plt.legend()
        plt.grid(True)

        st.pyplot()


# Main App
st.title("CSV Trendline Analysis")

uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if 'property' not in df.columns or 'scrap_date' not in df.columns:
        st.error("The CSV file must contain 'property' and 'scrap_date' columns.")
    else:
        df['scrap_date'] = pd.to_datetime(df['scrap_date'])
        
        # Sidebar for date selection
        min_date = df['scrap_date'].min()
        max_date = df['scrap_date'].max()
        
        filter_dates = st.sidebar.date_input("Filter dates:", [min_date, max_date])
        
        # Columns to consider for trendlines
        trend_columns = [col for col in df.columns if 'pct_affected' in col]
        
        # Sorting dataframe by scrap_date for plotting
        df.sort_values('scrap_date', inplace=True)
        
        # Grouping by scrap_date
        df_grouped = df.groupby('scrap_date')[trend_columns].mean().reset_index()
        
        # Plotting
        plot_trends(df_grouped, trend_columns, filter_dates)
