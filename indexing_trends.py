import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_trends(df, columns, filter_dates):
    for col in columns:
        st.write(f"### Trendline for {col}")  # Headline for the chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        filter_start = pd.Timestamp(filter_dates[0])
        filter_end = pd.Timestamp(filter_dates[1])
        
        df_filtered = df[(df['scrap_date'] >= filter_start) & (df['scrap_date'] <= filter_end)]
        
        ax.scatter(df_filtered['scrap_date'], df_filtered[col], label='Data Points')
        
        z = np.polyfit(df_filtered.index, df_filtered[col], 1)
        p = np.poly1d(z)
        ax.plot(df_filtered['scrap_date'], p(df_filtered.index), 'r--', label='Trendline')
        
        ax.set_xlabel("Scrap Date")
        ax.set_ylabel(f"{col} (%)")
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)

# Main App
st.title("CSV Trendline Analysis")

uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if 'property' not in df.columns or 'scrap_date' not in df.columns:
        st.error("The CSV file must contain 'property' and 'scrap_date' columns.")
    else:
        df['scrap_date'] = pd.to_datetime(df['scrap_date'])
        df = df.fillna(0)  # fill missing values with zero
        
        # Sidebar for property selection
        property_input = st.sidebar.text_input("Enter properties (comma-separated):", value="all")
        
        if property_input.lower() != "all":
            properties_to_show = property_input.split(',')
            df_filtered = df[df['property'].isin(properties_to_show)]
        else:
            df_filtered = df
        
        # Group by scrap_date and average across selected properties
        numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
        df_grouped = df_filtered.groupby('scrap_date')[numeric_cols].mean().reset_index()
        
        # Sidebar for date selection
        min_date = df_grouped['scrap_date'].min()
        max_date = df_grouped['scrap_date'].max()
        
        filter_dates = st.sidebar.date_input("Filter dates:", [min_date, max_date])
        
        trend_columns = [col for col in df_grouped.columns if 'pct_affected' in col]
        
        plot_trends(df_grouped, trend_columns, filter_dates)
