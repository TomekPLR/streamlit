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
def find_winners_losers(df, metric='Change in clicks (%)', top_n=100):
    winners = df.sort_values(by=metric, ascending=False).head(top_n)
    losers = df.sort_values(by=metric, ascending=True).head(top_n)
    return winners, losers

# Function to analyze cannibalization
def analyze_cannibalization(df):
    cannibalization_df = df.groupby('Query').agg({
        'Landing Page': pd.Series.nunique,
        'Url Clicks': 'sum',
        'Change in Url Clicks (%)': 'mean',
        'Impressions': 'sum',
        'Change in Impressions (%)': 'mean'
    }).reset_index()
    cannibalization_df.rename(columns={'Landing Page': 'Number of Unique Landing Pages'}, inplace=True)
    return cannibalization_df

# Streamlit App
def main():
    st.title("SEO Analysis Tool")

    # File uploaders
    st.sidebar.title("Upload CSV Files")
    file1 = st.sidebar.file_uploader("Upload your first CSV file", type=['csv'], key='file1')
    file2 = st.sidebar.file_uploader("Upload your second CSV file", type=['csv'], key='file2')

    # If the first file is uploaded, perform the analysis
    if file1:
        df1 = pd.read_csv(file1)
        df1 = rename_delta_columns(df1)

        top_3, top_5, top_10 = analyze_query_positions(df1)

        winners, losers = find_winners_losers(df1, metric='Change in clicks (%)')
        
        st.subheader("Queries in Top Positions")
        st.write(f"Top 3: {top_3}")
        st.write(f"Top 5: {top_5}")
        st.write(f"Top 10: {top_10}")

        st.subheader("Winners - Top 100 Queries")
        st.dataframe(winners)

        st.subheader("Losers - Top 100 Queries")
        st.dataframe(losers)

    # If the second file is uploaded, perform the analysis
    if file2:
        df2 = pd.read_csv(file2)
        df2 = rename_delta_columns(df2)

        cannibalization_data = analyze_cannibalization(df2)

        st.subheader("Cannibalization Analysis")
        st.dataframe(cannibalization_data)

# Run the Streamlit app
if __name__ == "__main__":
    main()
