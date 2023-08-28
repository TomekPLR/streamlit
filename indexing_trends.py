import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_trends(df, columns, filter_dates):
    for col in columns:
        plt.figure(figsize=(12, 6))
        
        # Filter based on selected date range
        if filter_dates:
            df_filtered = df[(df['scrape_date'] >= filter_dates[0]) & (df['scrape_date'] <= filter_dates[1])]
        else:
            df_filtered = df
        
        plt.scatter(df_filtered['scrape_date'], df_filtered[col], label='Data Points')
        
        # Adding Trendline
        z = np.polyfit(df_filtered.index, df_filtered[col], 1)
        p = np.poly1d(z)
        plt.plot(df_filtered['scrape_date'], p(df_filtered.index), 'r--', label='Trendline')
        
        plt.title(f"Trendline for {col}")
        plt.xlabel("Scrape Date")
        plt.ylabel(f"{col} (%)")
        plt.legend()
        plt.grid(True)
        
        st.pyplot()

# Main App
st.title("CSV Trendline Analysis")

uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if 'Property' not in df.columns or 'scrape_date' not in df.columns:
        st.error("The CSV file must contain 'Property' and 'scrape_date' columns.")
    else:
        df['scrape_date'] = pd.to_datetime(df['scrape_date'])
        
        # Sidebar for date selection
        min_date = df['scrape_date'].min()
        max_date = df['scrape_date'].max()
        
        filter_dates = st.sidebar.date_input("Filter dates:", [min_date, max_date])
        
        # Columns to consider for trendlines
        trend_columns = [col for col in df.columns if 'pct_affected' in col]
        
        # Sorting dataframe by scrape_date for plotting
        df.sort_values('scrape_date', inplace=True)
        
        # Grouping by scrape_date
        df_grouped = df.groupby('scrape_date')[trend_columns].mean().reset_index()
        
        # Plotting
        plot_trends(df_grouped, trend_columns, filter_dates)
