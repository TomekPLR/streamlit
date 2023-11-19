import streamlit as st
import pandas as pd

def rename_columns(df, column_patterns):
    new_columns = []
    delta_counter = 1  # Counter for duplicate % Δ columns
    for col in df.columns:
        if '% Δ' in col:
            # If the column name contains '% Δ', rename it with a counter to make it unique
            new_columns.append(f'Change in {df.columns[new_columns[-1]]} {delta_counter} (%)')
            delta_counter += 1
        else:
            new_columns.append(col)
            delta_counter = 1  # Reset counter if the column doesn't contain '% Δ'
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
        column_patterns_1 = {'% Δ': ['Change in Average Position (%)', 'Change in Clicks (%)', 'Change in Site CTR (%)', 'Change in Impressions (%)']}
        df1 = rename_columns(df1, column_patterns_1)
        st.write("First Data Preview:", df1.head())

    if file2:
        df2 = pd.read_csv(file2)
        # For the second CSV, we expect the pattern '% Δ' to follow 'Url Clicks', 'Impressions', 'URL CTR'
        # Since 'Url Clicks' appears twice, we must specify the new names accordingly
        column_patterns_2 = {'% Δ': ['Change in Url Clicks 1 (%)', 'Change in Url Clicks 2 (%)', 'Change in Impressions (%)', 'Change in URL CTR (%)']}
        df2 = rename_columns(df2, column_patterns_2)
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
