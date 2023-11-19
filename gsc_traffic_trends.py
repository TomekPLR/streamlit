import streamlit as st
import pandas as pd

# Function to rename columns based on their preceding column
def rename_columns(df):
    new_columns = []
    for i, col in enumerate(df.columns):
        if col.strip() == '% Δ':
            new_col = f'Change in {df.columns[i-1]} (%)'
            new_columns.append(new_col)
        else:
            new_columns.append(col)
    df.columns = new_columns
    return df

# Function to analyze top queries
def analyze_top_queries(df):
    top_3 = df[df['Average Position'] <= 3]
    top_5 = df[df['Average Position'] <= 5]
    top_10 = df[df['Average Position'] <= 10]

    return len(top_3), len(top_5), len(top_10)

# Function to find winners and losers
def analyze_winners_losers(df, top_n=100):
    # Sort by 'Change in Clicks (%)' and select top 100
    winners = df.sort_values(by='Change in Clicks (%)', ascending=False).head(top_n)
    losers = df.sort_values(by='Change in Clicks (%)').head(top_n)

    return winners, losers

# Function to analyze cannibalization
def analyze_cannibalization(df):
    # Group by query and count unique landing pages
    cannibalization = df.groupby('Query')['Landing Page'].nunique().reset_index()
    cannibalization.columns = ['Query', 'Number of Unique Landing Pages']
    return cannibalization

# Streamlit App
def main():
    st.title("SEO Analysis Tool")

    file = st.file_uploader("Upload your CSV file", type=['csv'])

    if file:
        df = pd.read_csv(file)
        df = rename_columns(df)

        st.write("Data Preview:", df.head())

        # Analysis Section
        st.subheader("Top Queries Analysis")
        top_3, top_5, top_10 = analyze_top_queries(df)
        st.write(f"Number of queries in top 3: {top_3}")
        st.write(f"Number of queries in top 5: {top_5}")
        st.write(f"Number of queries in top 10: {top_10}")

        st.subheader("Winners and Losers Analysis")
        winners, losers = analyze_winners_losers(df)
        st.write("Winners (Top 100):")
        st.dataframe(winners)
        st.write("Losers (Top 100):")
        st.dataframe(losers)

        st.subheader("Cannibalization Analysis")
        cannibalization_data = analyze_cannibalization(df)
        st.write("Cannibalization Data:")
        st.dataframe(cannibalization_data)

if __name__ == "__main__":
    main()
