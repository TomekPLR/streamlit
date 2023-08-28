import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# Read CSV
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Ensure the necessary columns exist
    if all(col in df.columns for col in ["property", "scrap_date"]):
        # Convert 'scrap_date' to datetime and drop invalid rows
        df['scrap_date'] = pd.to_datetime(df['scrap_date'], errors='coerce')
        df.dropna(subset=['scrap_date'], inplace=True)
        
        min_date = df['scrap_date'].min().date()
        max_date = df['scrap_date'].max().date()

        if min_date and max_date:
            # Sidebar
            st.sidebar.title("Filters")
            
            # Date range selector
            selected_date_range = st.sidebar.date_input('Select Date Range:', [min_date, max_date])
            
            # Property selector
            property_list = df['property'].unique().tolist()
            selected_properties = st.sidebar.multiselect('Select Properties:', ["All"] + property_list, default=["All"])
            
            # Filter data
            if "All" not in selected_properties:
                df_filtered = df[df['property'].isin(selected_properties)]
            else:
                df_filtered = df
            
            df_filtered = df_filtered[(df_filtered['scrap_date'].dt.date >= selected_date_range[0]) & (df_filtered['scrap_date'].dt.date <= selected_date_range[1])]
            
            # Select only numeric columns (columns starting with "pct")
            pct_cols = [col for col in df_filtered.columns if col.startswith('pct')]
            
            # Group and calculate the median for only pct columns
            df_grouped = df_filtered.groupby('scrap_date')[pct_cols].median().reset_index()
            
            # Display data
            st.write(df_grouped)
            
            # Create trend charts
            for col in pct_cols:
                st.write(f"Trend for {col}")
                st.line_chart(df_grouped[['scrap_date', col]].set_index('scrap_date'))
        else:
            st.write("Data does not contain valid min and max dates.")
    else:
        st.write("CSV file must have columns named 'property' and 'scrap_date'.")
else:
    st.write("Please upload a CSV file.")
