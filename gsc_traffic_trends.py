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
def find_winners_losers(df, metric='Change in Clicks (%)', change_metric='Change in Impressions (%)', top_n=100):
    df_filtered = df[df[metric] > 0] if 'Winners' in st.current_tab else df[df[metric] < 0]
    sorted_df = df_filtered.sort_values(by=metric, ascending=False)
    return sorted_df.head(top_n)

# Streamlit App
def main():
    st.title("SEO Analysis Tool")

    # Tab creation
    tab1, tab2, tab3 = st.tabs(["General Info", "Winners", "Losers"])

    # File uploader
    file1 = st.file_uploader("Upload your CSV file", type=['csv'], key='file1')

    # Variables to hold dataframes
    df1 = None

    # Read file
    if file1:
        df1 = pd.read_csv(file1)
        df1 = rename_delta_columns(df1)

    with tab1:
        st.header("General Info")
        if df1 is not None:
            top_3, top_5, top_10 = analyze_query_positions(df1)
            st.metric("Queries in Top 3", top_3)
            st.metric("Queries in Top 5", top_5)
            st.metric("Queries in Top 10", top_10)

    with tab2:
        st.header("Winners - Top Queries with Increased Clicks")
        if df1 is not None:
            winners = find_winners_losers(df1)
            st.dataframe(winners)

    with tab3:
        st.header("Losers - Top Queries with Decreased Clicks")
        if df1 is not None:
            losers = find_winners_losers(df1)
            st.dataframe(losers)

# Run the Streamlit app
if __name__ == "__main__":
    main()
