import streamlit as st
import pandas as pd

def rename_columns(df):
    new_columns = []
    delta_counter = 1  # Counter for duplicate % Δ columns
    prev_col_name = ""  # Variable to hold the previous column's name

    for col in df.columns:
        if '% Δ' in col:
            # Ensure that there is a previous column to reference
            if prev_col_name:
                # If the column name contains '% Δ', rename it by referencing the last non-'% Δ' column
                new_col = f'Change in {prev_col_name} {delta_counter} (%)'
                delta_counter += 1  # Increment the counter for the next potential '% Δ' column
            else:
                new_col = f'Change in {col} {delta_counter} (%)'  # Fallback if no previous column is found
        else:
            new_col = col
            prev_col_name = col  # Update the previous column name
            delta_counter = 1  # Reset counter if the column doesn't contain '% Δ'

        new_columns.append(new_col)

    df.columns = new_columns
    return df



def analyze_top_queries(df):
    # Add error handling or adjust column names based on your CSV
    try:
        top_3 = df[df['Average Position'] <= 3]
        top_5 = df[df['Average Position'] <= 5]
        top_10 = df[df['Average Position'] <= 10]
    except KeyError:
        st.error("Column names do not match. Please check your CSV file.")
        return None, None, None

    return len(top_3), len(top_5), len(top_10)

def analyze_winners_losers(df, top_n=100):
    # Add error handling or adjust column names
    try:
        winners = df.sort_values(by='Change in Clicks (%)', ascending=False).head(top_n)
        losers = df.sort_values(by='Change in Clicks (%)').head(top_n)
    except KeyError:
        st.error("Column names do not match. Please check your CSV file.")
        return None, None

    return winners, losers

def main():
    st.title("SEO Analysis Tool")

    # Two file uploaders for different CSV files
    file1 = st.file_uploader("Upload first CSV file", type=['csv'], key='file1')
    file2 = st.file_uploader("Upload second CSV file", type=['csv'], key='file2')

    if file1:
        df1 = pd.read_csv(file1)
        # For the first CSV, we expect the pattern '% Δ' to follow 'Average Position', 'clicks', etc.
        df1 = rename_columns(df1)
        st.write("First Data Preview:", df1.head())

    if file2:
        df2 = pd.read_csv(file2)
        # For the second CSV, we expect the pattern '% Δ' to follow 'Url Clicks', 'Impressions', 'URL CTR'
        # Since 'Url Clicks' appears twice, we must specify the new names accordingly
        df2 = rename_columns(df2)
        st.write("Second Data Preview:", df2.head())
        
        st.subheader("Top Queries Analysis (First File)")
        top_3, top_5, top_10 = analyze_top_queries(df1)
        if top_3 is not None:
            st.write(f"Number of queries in top 3: {top_3}")
            st.write(f"Number of queries in top 5: {top_5}")
            st.write(f"Number of queries in top 10: {top_10}")

        # Winners and Losers Analysis for the first file
        st.subheader("Winners and Losers Analysis (First File)")
        winners, losers = analyze_winners_losers(df1)
        if winners is not None and losers is not None:
            st.write("Winners (Top 100):")
            st.dataframe(winners)
            st.write("Losers (Top 100):")
            st.dataframe(losers)

if __name__ == "__main__":
    main()
