import streamlit as st
from openai import OpenAI
import os

# Initialize your OpenAI API key

os.environ['API_KEY'] = st.secrets['API_KEY']
openai = OpenAI(api_key=os.getenv('API_KEY'))


# Variables to store the query, top 10 results, and user-submitted title
stored_query = ""
stored_results = ""
user_title = ""

def query_chatgpt(prompt):
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": ""}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main_analysis():
    global stored_query, stored_results, user_title  # Access the global variables

    st.title("Google Search Results Analysis")

    with st.form("query_results_form"):
        stored_query = st.text_input("Query")
        stored_results = st.text_area("Top 10 Results", height=400)
        user_title = st.text_input("Your Title")
        submit_button = st.form_submit_button("Calculate")

    if submit_button:
        # Calculate differences between top 3 and 7-10 results
        differences_summary = query_chatgpt(f"Here's the Google search results: {stored_results}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the places 7-10.")
        st.subheader("Differences Summary")
        st.write(differences_summary)

        # Calculate differences between top 3 and user-proposed title
        differences_with_user_title_summary = query_chatgpt(f"Here's the Google search results: {stored_results}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the title proposed by the user: '{user_title}'.")
        st.subheader("Differences Summary with User Title")
        st.write(differences_with_user_title_summary)

        # Calculate relevancy of user-proposed title to the query
        relevancy_score = query_chatgpt(f"How well is the '{user_title}' proposed by the user relevant to the '{stored_query}'?")
        st.subheader("Relevancy Score")
        st.write(relevancy_score)

# Run the main analysis
main_analysis()
