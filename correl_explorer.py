import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to find most correlated pairs from a correlation matrix
def get_most_correlated_pairs(corr_matrix):
    pairs_to_drop = set()
    cols = corr_matrix.columns
    for i in range(0, corr_matrix.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))

    corrs = corr_matrix.unstack().drop(labels=pairs_to_drop).sort_values(ascending=False, key=lambda x: abs(x))
    return corrs

# Streamlit app
st.title("CSV Correlation Explorer")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])

    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()

    # Display correlation matrix
    st.header("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Display most correlated pairs
    st.header("Most Correlated Pairs")
    most_correlated_pairs = get_most_correlated_pairs(corr_matrix)
    st.write(most_correlated_pairs)
