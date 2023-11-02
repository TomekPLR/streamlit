import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_most_correlated_pairs(corr_matrix):
    pairs_to_drop = set()
    cols = corr_matrix.columns
    for i in range(0, corr_matrix.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))

    corrs = corr_matrix.unstack().drop(labels=pairs_to_drop).sort_values(ascending=False, key=lambda x: abs(x))
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
    # Adjust figure size and annotation font size
    fig, ax = plt.subplots(figsize=(max(10, len(numeric_df.columns)), max(8, len(numeric_df.columns) // 2)))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax, annot_kws={'size': 8})
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    st.pyplot(fig)

    st.header("Most Correlated Pairs")
    most_correlated_pairs = get_most_correlated_pairs(corr_matrix)
    st.write(most_correlated_pairs)
