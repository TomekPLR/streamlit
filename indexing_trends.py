import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot trend
def plot_trend(df, title):
    plt.figure(figsize=(12, 6))
    plt.title(title)
    plt.plot(df['scrap_date'], df['median_value'])
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Median Value')
    st.pyplot()

# Main App
st.title("CSV Trendline Analysis")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.dtypes)  # Debug line to write the data types

    # Check if the required columns are present
    if 'property' not in df.columns or 'scrap_date' not in df.columns:
        st.error('CSV file must have columns named "property" and "scrap_date".')
    else:
        # Sidebar for date range selection
        min_date = df['scrap_date'].min()
        max_date = df['scrap_date'].max()
        selected_date_range = st.sidebar.date_input('Select Date Range:', [min_date, max_date])
        
        df['scrap_date'] = pd.to_datetime(df['scrap_date'])
        df_filtered_date = df[(df['scrap_date'] >= pd.Timestamp(selected_date_range[0])) & 
                               (df['scrap_date'] <= pd.Timestamp(selected_date_range[1]))]
        
        # Find columns that start with "pct"
        pct_columns = [col for col in df.columns if col.startswith("pct")]

        # Sidebar for property selection
        selected_pct_columns = st.sidebar.multiselect("Choose Columns:", pct_columns, default=pct_columns)
        
        # Filter DataFrame
        df_filtered = df_filtered_date[selected_pct_columns + ['scrap_date']]
        
        # Calculate the median value and add it to the dataframe
        df_filtered['median_value'] = df_filtered[selected_pct_columns].median(axis=1)

        # Group by date and find median
        df_grouped = df_filtered.groupby('scrap_date')['median_value'].median().reset_index()

        # Plotting
        plot_trend(df_grouped, 'Trendline for Selected Properties and Date Range')
