pip install seaborn
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['scrap_date'] = pd.to_datetime(df['scrap_date']).dt.date
    return df

def filter_by_property(df, selected_property):
    return df[df['property'] == selected_property]

def display_correlation_matrix(df):
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    st.pyplot(f)

def plot_column(df, column):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='scrap_date', y=column)
    plt.title(f'Trend of {column} over time')
    st.pyplot()

def main():
    st.title('CSV Analysis Tool')

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = read_csv(uploaded_file)

        st.sidebar.header('Select property')
        selected_property = st.sidebar.selectbox('Choose a property', df['property'].unique())
        property_df = filter_by_property(df, selected_property)

        st.header(f'Correlation matrix for {selected_property}')
        display_correlation_matrix(property_df)

        st.header(f'Trends for {selected_property}')
        for col in property_df.columns:
            if np.issubdtype(property_df[col].dtype, np.number) and col != 'scrap_date':
                plot_column(property_df, col)

if __name__ == '__main__':
    main()
