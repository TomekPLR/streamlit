import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load the CSV file
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to display the trendline for a specific column
def display_trendline(data, column):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="scrape_date", y=column, data=data)
    plt.title(f"Trendline for {column}")
    plt.xlabel("Scrape Date")
    plt.ylabel("Percentage Affected")
    st.pyplot()

# Main function
def main():
    st.title("CSV Data Analysis")
    st.sidebar.title("Settings")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        
        # Date filtering
        date_filter = st.sidebar.date_input("Select date range", [data['scrape_date'].min(), data['scrape_date'].max()])
        filtered_data = data[(data['scrape_date'] >= date_filter[0]) & (data['scrape_date'] <= date_filter[1])]

        columns_to_plot = [col for col in data.columns if col.startswith("pct_affected_")]
        selected_column = st.sidebar.selectbox("Select column to plot", columns_to_plot)

        display_trendline(filtered_data, selected_column)

if __name__ == "__main__":
    main()
