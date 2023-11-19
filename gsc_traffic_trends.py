def main():
    st.title("SEO Analysis Tool")

    # Two file uploaders for different CSV files
    file1 = st.file_uploader("Upload first CSV file", type=['csv'], key='file1')
    file2 = st.file_uploader("Upload second CSV file", type=['csv'], key='file2')

    if file1:
        df1 = pd.read_csv(file1)
        st.write("Original column names from first CSV:", df1.columns.tolist())
        df1 = rename_columns(df1)
        st.write("Renamed column names from first CSV:", df1.columns.tolist())
        st.write("First Data Preview:", df1.head())

        # Perform the top queries analysis only if the file is uploaded and correctly processed
        st.subheader("Top Queries Analysis (First File)")
        top_3, top_5, top_10 = analyze_top_queries(df1)
        if top_3 is not None:
            st.write(f"Number of queries in top 3: {top_3}")
            st.write(f"Number of queries in top 5: {top_5}")
            st.write(f"Number of queries in top 10: {top_10}")

        # Perform the winners and losers analysis only if the file is uploaded and correctly processed
        st.subheader("Winners and Losers Analysis (First File)")
        winners, losers = analyze_winners_losers(df1)
        if winners is not None and losers is not None:
            st.write("Winners (Top 100):")
            st.dataframe(winners)
            st.write("Losers (Top 100):")
            st.dataframe(losers)

    if file2:
        df2 = pd.read_csv(file2)
        st.write("Original column names from second CSV:", df2.columns.tolist())
        df2 = rename_columns(df2)
        st.write("Renamed column names from second CSV:", df2.columns.tolist())
        st.write("Second Data Preview:", df2.head())

        # Additional analyses for the second file can be added here
        # ...

if __name__ == "__main__":
    main()
