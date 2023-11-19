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
    file1 = st.file_uploader("Upload your CSV file for General Info", type=['csv'], key='file1')
    file2 = st.file_uploader("Upload your CSV file for Winners and Losers", type=['csv'], key='file2')

    # Variables to hold dataframes
    df_general_info = None
    df_winners_losers = None

    # Read files
    if file1:
        df_general_info = pd.read_csv(file1)
        df_general_info = rename_delta_columns(df_general_info)

    if file2:
        df_winners_losers = pd.read_csv(file2)
        df_winners_losers = rename_delta_columns(df_winners_losers)

    if df_general_info is not None:
        st.header("General Info")
        top_3, top_5, top_10 = analyze_query_positions(df_general_info)
        st.metric("Queries in Top 3", top_3)
        st.metric("Queries in Top 5", top_5)
        st.metric("Queries in Top 10", top_10)

    if df_winners_losers is not None:
        st.header("Winners")
        winners = find_winners_losers(df_winners_losers)[0]
        st.dataframe(winners)

        st.header("Losers")
        losers = find_winners_losers(df_winners_losers)[1]
        st.dataframe(losers)

# Run the Streamlit app
if __name__ == "__main__":
    main()
