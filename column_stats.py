import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up the main structure of the Streamlit app
st.title('Data Analysis')

# Add a file uploader and ask the user to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Once the file is uploaded, read and display the data and statistics
if uploaded_file is not None:
    # Use the 'read_csv' function to read the uploaded file object
    data = pd.read_csv(uploaded_file, parse_dates=['scrap_date'])

    # Sidebar user inputs for filtering
    st.sidebar.header('Filters')
    property_filter = st.sidebar.text_input("Property contains")
    selected_date = st.sidebar.date_input("Select date")

    # Filter data based on selections
    if property_filter:
        filtered_data = data[data['property'].str.contains(property_filter)]
    else:
        filtered_data = data

    filtered_data = filtered_data[filtered_data['scrap_date'] == pd.to_datetime(selected_date)]

    # Main window of the app to display data and stats
    st.write("Data Overview:", data)  # Show the entire data loaded for user reference

    # Iterating through each column in the dataframe
    for column in filtered_data.columns:
        if filtered_data[column].dtype in [np.float64, np.int64]:  # checking if the column is numeric
            st.header(f"Analyzing column: {column}")

            # Calculate statistics
            daily_average = filtered_data[column].mean()
            daily_median = filtered_data[column].median()
            daily_90_percentile = np.percentile(filtered_data[column].dropna(), 90)
            daily_10_percentile = np.percentile(filtered_data[column].dropna(), 10)

            # Display statistics
            st.subheader('Statistics for selected day')
            st.markdown(f"""
            - **Average**: {daily_average}
            - **Median**: {daily_median}
            - **90th Percentile**: {daily_90_percentile}
            - **10th Percentile**: {daily_10_percentile}
            """)

            # Generate a trend chart
            st.subheader('Trend chart over time')
            fig, ax = plt.subplots()
            ax.plot(data['scrap_date'], data[column], label=column)  # Plotting the trend
            ax.set_xlabel('Date')
            ax.set_ylabel(column)
            ax.legend()
            st.pyplot(fig)

            st.write("---")  # Adding a separating line for clarity

    st.sidebar.markdown('---')
    st.sidebar.markdown('End of options.')
else:
    st.info('Please upload a CSV file to proceed.')
