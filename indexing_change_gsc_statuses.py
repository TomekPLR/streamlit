import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# Read CSV
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure the necessary columns exist
    if all(col in df.columns for col in ["property", "scrap_date"]):
        # Convert 'scrap_date' to datetime and drop invalid rows
        df['scrap_date'] = pd.to_datetime(df['scrap_date'], errors='coerce')
        df.dropna(subset=['scrap_date'], inplace=True)

        # Sidebar
        st.sidebar.title("Filters")

        # Date range selector for analysis
        selected_dates = st.sidebar.multiselect('Select Two Dates for Comparison:', sorted(df['scrap_date'].dt.date.unique()), default=[])

        if len(selected_dates) == 2:
            # Filter data based on selected dates
            df_filtered = df[df['scrap_date'].dt.date.isin(selected_dates)]

            # Select only numeric columns (columns starting with "pct")
            pct_cols = [col for col in df_filtered.columns if col.startswith('pct')]

            # Group by property and calculate the median for only pct columns
            df_grouped = df_filtered.groupby(['property', 'scrap_date'])[pct_cols].median().reset_index()

            # Pivot table for easy comparison
            df_pivot = df_grouped.pivot(index='property', columns='scrap_date', values=pct_cols)
            df_pivot.columns = [f"{col[0]}_{col[1].date()}" for col in df_pivot.columns]

            summary_data = []

            for col in pct_cols:
                col_1 = f"{col}_{selected_dates[0]}"
                col_2 = f"{col}_{selected_dates[1]}"
                
                # Calculate the increase or decrease for each property for this pct column
                df_pivot[f"{col}_change"] = df_pivot[col_2] - df_pivot[col_1]
                
                # Calculate percentages of increased and decreased properties
                increased = (df_pivot[f"{col}_change"] > 0).sum()
                decreased = (df_pivot[f"{col}_change"] < 0).sum()
                total = len(df_pivot[f"{col}_change"].dropna())
                
                if total > 0:
                    increased_pct = (increased / total) * 100
                    decreased_pct = (decreased / total) * 100
                    summary_data.append({
                        'Column': col,
                        'Increased (%)': increased_pct,
                        'Decreased (%)': decreased_pct,
                        'Total Properties': total
                    })

            # Create summary DataFrame and sort by 'Decreased (%)'
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.sort_values('Decreased (%)', ascending=False)
            st.table(summary_df)

        else:
            st.write("Please select exactly two dates for comparison.")
    else:
        st.write("CSV file must have columns named 'property' and 'scrap_date'.")
else:
    st.write("Please upload a CSV file.")
