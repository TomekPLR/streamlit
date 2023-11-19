import streamlit as st
import pandas as pd

# Function to rename % Δ columns
def rename_delta_columns(df):
    columns = df.columns.tolist()
    for i, col in enumerate(columns):
        if '% Δ' in col:
            prev_col = columns[i - 1] if i > 0 else 'Unknown'
            new_col_name = f'Change in {prev_col.strip()} (%)'
            columns[i] = new_col_name
    df.columns = columns
    return df

# Function to analyze the number of queries within the top positions
def analyze_query_positions(df):
    top_3 = df[df['Average Position'] <= 3].shape[0]
    top_5 = df[df['Average Position'] <= 5].shape[0]
    top_10 = df[df['Average Position'] <= 10].shape[0]
    return top_3, top_5, top_10

# Function to find the top winners and losers
def find_winners_losers(df, metric='Change in Clicks (%)', top_n=100):
    df_sorted = df.sort_values(by=metric, ascending=False)
    winners = df_sorted[df_sorted[metric] > 0].head(top_n)
    losers = df_sorted[df_sorted[metric] < 0].head(top_n)
    return winners, losers

# Streamlit App
def main():
    st.title("SEO Analysis Tool")

    # File uploaders
    file1 = st.file_uploader("Upload your CSV file for Query Analysis", type=['csv'], key='file1')
    file2 = st.file_uploader("Upload your CSV file for Landing Page Analysis", type=['csv'], key='file2')

    # Variables to hold dataframes
    df_queries = None
    df_landing_pages = None

    # Read files
    if file1:
        df_queries = pd.read_csv(file1)
        df_queries = rename_delta_columns(df_queries)
        st.write("Columns in Query Analysis file:", df_queries.columns.tolist())

    if file2:
        df_landing_pages = pd.read_csv(file2)
        df_landing_pages = rename_delta_columns(df_landing_pages)
        st.write("Columns in Landing Page Analysis file:", df_landing_pages.columns.tolist())

    # Analysis for the first file (Queries)
    if df_queries is not None:
        st.header("General Info - Queries")
        top_3, top_5, top_10 = analyze_query_positions(df_queries)
        st.metric("Queries in Top 3", top_3)
        st.metric("Queries in Top 5", top_5)
        st.metric("Queries in Top 10", top_10)

        st.header("Winners - Queries with Increased Clicks")
        winners_queries = find_winners_losers(df_queries)[0]
        st.dataframe(winners_queries)

        st.header("Losers - Queries with Decreased Clicks")
        losers_queries = find_winners_losers(df_queries)[1]
        st.dataframe(losers_queries)

    # Analysis for the second file (Landing Pages)
    if df_landing_pages is not None:
        st.header("Winners - Landing Pages with Increased Clicks")
        winners_landing_pages = find_winners_losers(df_landing_pages)[0]
        st.dataframe(winners_landing_pages)

        st.header("Losers - Landing Pages with Decreased Clicks")
        losers_landing_pages = find_winners_losers(df_landing_pages)[1]
        st.dataframe(losers_landing_pages)

# Run the Streamlit app
if __name__ == "__main__":
    main()
