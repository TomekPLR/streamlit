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
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
    st.pyplot(f)

def plot_column(df, column):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='scrap_date', y=column, ax=ax)
    plt.title(f'Trend of {column} over time')
    st.pyplot(fig)

def plot_compare_columns(df, col1, col2):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df['scrap_date'], df[col1], label=col1, color='blue')
    ax1.set_ylabel(col1, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(df['scrap_date'], df[col2], label=col2, color='red')
    ax2.set_ylabel(col2, color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.tight_layout()
    plt.title(f'Comparison of {col1} and {col2} over time')
    st.pyplot(fig)

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

        numerical_columns = [col for col in property_df.columns if np.issubdtype(property_df[col].dtype, np.number) and col != 'scrap_date']
        chart_selection = st.sidebar.selectbox('Select a chart', [''] + numerical_columns)

        st.sidebar.header('Compare two variables')
        col1 = st.sidebar.selectbox('Select first variable', [''] + numerical_columns)
        col2 = st.sidebar.selectbox('Select second variable', [''] + numerical_columns)

        if chart_selection:
            plot_column(property_df, chart_selection)
        else:
            for col in numerical_columns:
                plot_column(property_df, col)

        if col1 and col2 and col1 != col2:
            st.header(f'Comparison of {col1} and {col2}')
            plot_compare_columns(property_df, col1, col2)
  if __name__ == '__main__':
    main()
