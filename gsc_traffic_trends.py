import streamlit as st
import pandas as pd

def rename_columns(df):
    # Adjust this function to match your CSV file's column names
    new_columns = []
    for i, col in enumerate(df.columns):
        if '% Δ' in col:
            new_col = f'Change in {df.columns[i-1]} (%)'
            new_columns.append(new_col)
        else:
            new_columns.append(col)
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
    file1 = st.file_uploader("Upload first CSV file", type=['csv'])
    file2 = st.file_uploader("Upload second CSV file", type=['csv'])

    if file1 and file2:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        df1 = rename_columns(df1)
        df2 = rename_columns(df2)

        st.write("First Data Preview:", df1.head())
        st.write("Second Data Preview:", df2.head())

        # Analysis for the first file
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

        # Additional analyses for the second file can be added here
        # ...

if __name__ == "__main__":
    main()
