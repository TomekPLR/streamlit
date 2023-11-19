import streamlit as st
import pandas as pd

# Function to calculate top 100 winners and losers
def top_winners_losers(df, group_by_column):
    # Group by specified column and sum Url Clicks
    grouped_df = df.groupby(group_by_column)['Url Clicks'].sum().reset_index()
    
    # Sort and get top 100 winners
    top_winners = grouped_df.sort_values(by='Url Clicks', ascending=False).head(100)
    
    # Sort and get top 100 losers
    top_losers = grouped_df.sort_values(by='Url Clicks', ascending=True).head(100)
    
    return top_winners, top_losers

# Streamlit app
def main():
    st.title("Top 100 Winners and Losers Analyzer")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read CSV
        data = pd.read_csv(uploaded_file)

        # Display original data
        st.write("### Original Data")
        st.dataframe(data)

        # Calculate and Display for Landing Page
        st.write("### Top 100 Winners and Losers by Landing Page")
        winners_lp, losers_lp = top_winners_losers(data, 'Landing Page')
        st.write("#### Top Winners")
        st.dataframe(winners_lp)
        st.write("#### Top Losers")
        st.dataframe(losers_lp)

        # Calculate and Display for Query
        st.write("### Top 100 Winners and Losers by Query")
        winners_q, losers_q = top_winners_losers(data, 'Query')
        st.write("#### Top Winners")
        st.dataframe(winners_q)
        st.write("#### Top Losers")
        st.dataframe(losers_q)

if __name__ == "__main__":
    main()
