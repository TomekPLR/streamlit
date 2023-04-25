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
    sns.set(style="white")
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    f, ax = plt.subplots(figsize=(15, 12))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
    ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
    st.pyplot(f)

def plot_column(df, column):
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='scrap_date', y=column, ax=ax, palette='husl')
    ax.set_title(f'Trend of {column} over time', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_compare_columns(df, col1, col2, normalize):
    sns.set(style="darkgrid")
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    if normalize:
        col1_data = (df[col1] - df[col1].min()) / (df[col1].max() - df[col1].min())
        col2_data = (df[col2] - df[col2].min()) / (df[col2].max() - df[col2].min())
    else:
        col1_data = df[col1]
        col2_data = df[col2]

    ax1.plot(df['scrap_date'], col1_data, label=col1, color='blue')
    ax1.set_ylabel(col1, color='blue', fontsize=14)
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(df['scrap_date'], col2_data, label=col2, color='red')
    ax2.set_ylabel(col2, color='red', fontsize=14)
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    plt.title(f'Comparison of {col1} and {col2} over time', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def main():
    st.title('GSC property explorer')

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = read_csv(uploaded_file)
        
        st.sidebar.header('Select property')
        selected_property = st.sidebar.selectbox('Choose a property', df['property'].unique())
        property_df = filter_by_property(df, selected_property)

        # Dynamically
        numerical_columns = [col for col in property_df.columns if np.issubdtype(property_df[col].dtype, np.number) and col != 'scrap_date']
        correlation_columns = st.sidebar.multiselect('Select columns for correlation analysis', numerical_columns, default=numerical_columns)
        tab = st.sidebar.radio("Select tab", ["Correlation Matrix", "All Charts", "Compare Two Variables"])

    if tab == "Correlation Matrix":
        st.header(f'Correlation matrix for {selected_property}')
        display_correlation_matrix(property_df[correlation_columns])

    elif tab == "All Charts":
        st.header(f'Trends for {selected_property}')
        chart_selection = st.sidebar.selectbox('Select a chart', [''] + numerical_columns)

        if chart_selection:
            plot_column(property_df, chart_selection)
        else:
            for col in numerical_columns:
                plot_column(property_df, col)

    elif tab == "Compare Two Variables":
        st.sidebar.header('Compare two variables')
        col1 = st.sidebar.selectbox('Select first variable', [''] + numerical_columns)
        col2 = st.sidebar.selectbox('Select second variable', [''] + numerical_columns)
        normalize = st.sidebar.checkbox("Normalize charts (0-1)")

        if col1 and col2 and col1 != col2:
            st.header(f'Comparison of {col1} and {col2}')
            plot_compare_columns(property_df, col1, col2, normalize)
if __name__ == '__main__':
    main()
