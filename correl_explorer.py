import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_most_correlated_pairs(corr_matrix, selected_column):
    # Get the correlation pairs related to the selected column
    corrs = corr_matrix[selected_column].sort_values(ascending=False, key=lambda x: abs(x))
    return corrs

st.title("CSV Correlation Explorer")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    default_exclude_columns = [
        'status_details', 'response_301', 'response_302', 'response_moved',
        'response_not_modified', 'response_blocked_robots', 'response_404',
        'response_robots_not_available', 'response_dns_error', 'response_fetch_error',
        'response_page_not_reached', 'response_page_timeout', 'response_redirect_error',
        'response_other_error', 'purpose_refresh', 'type_mobile', 'type_desktop',
        'type_image', 'type_video', 'type_ads', 'type_store', 'type_other',
        'property.3', 'scrap_date.3', 'property.4', 'scrap_date.4', 'last_update',
        'property.5', 'scrap_date.5', 'last_update.1'
    ]

    st.header("Columns to Exclude")
    exclude_columns = st.multiselect(
        "Select additional columns to exclude from analysis:", 
        df.columns.tolist(),
        default=default_exclude_columns
    )

    filtered_df = df.drop(columns=exclude_columns)
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    st.header("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(max(10, len(numeric_df.columns)), max(8, len(numeric_df.columns) // 2)))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax, annot_kws={'size': 8})
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    st.pyplot(fig)

    # Let user select a column
    st.header("Correlation Analysis")
    selected_column = st.selectbox("Select a column to see most correlated columns:", numeric_df.columns.tolist())

    # Display most correlated pairs for the selected column
    st.header(f"Most Correlated Columns with {selected_column}")
    most_correlated_pairs = get_most_correlated_pairs(corr_matrix, selected_column)
    st.write(most_correlated_pairs.drop(selected_column, errors='ignore'))  # Exclude self-correlation
