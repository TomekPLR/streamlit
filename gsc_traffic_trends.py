import streamlit as st
import pandas as pd

def rename_columns(df, column_patterns):
    # Assuming the column patterns are given as a dictionary:
    # column_patterns = {'% Δ': ['Change in Average Position (%)', 'Change in Clicks (%)', ...]}
    for i, col in enumerate(df.columns):
        if col.strip() in column_patterns:
            new_col = column_patterns[col.strip()][0]
            column_patterns[col.strip()].pop(0)
            df.rename(columns={col: new_col}, inplace=True)
    return df

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

    # Further analysis would go here
    # ...

if __name__ == "__main__":
    main()