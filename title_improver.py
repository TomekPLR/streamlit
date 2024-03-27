import streamlit as st
from openai import OpenAI
import os

# Initialize your OpenAI API key
os.environ['API_KEY'] = st.secrets['API_KEY']
openai = OpenAI(api_key=os.getenv('API_KEY'))

# Variables to store the query, top 10 results, user-submitted title, and article
stored_query = ""
stored_results = ""
user_title = ""
user_article = ""  # New field for storing the user's article

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
    global stored_query, stored_results, user_title, user_article  # Access the global variables

    st.title("Google Search Results and Article Analysis")

    with st.form("query_results_form"):
        stored_query = st.text_input("Query")
        stored_results = st.text_area("Top 10 Results", height=400)
        user_title = st.text_input("Your Title")
        user_article = st.text_area("Your Article", height=400)  # New field for user to type in the entire article
        submit_button = st.form_submit_button("Calculate")

    if submit_button:
        # Existing analysis...
        
        # New analysis on the article for signs of waffle content
        waffle_content_analysis = query_chatgpt(f"I have an article: {user_article}\n\nLook for signs of waffle content, for instance: Repetition, Generalization, Lack of Depth, Limited Insights, Absence of Examples or Case Studies. Then judge how useful it's for the users typing in Google: 'Challenging Long-Term Disability Claim Denials'. Give me just summary, I don't need detailed problems in each category.")
        st.subheader("Article Waffle Content Analysis")
        st.write(waffle_content_analysis)

        # Further analysis based on utility for specific audiences
        utility_for_general_guidance = query_chatgpt(f"Given the article: {user_article}, how useful is it for those looking for general guidance")
        utility_for_comprehensive_understanding = query_chatgpt(f"Given the article: {user_article}, how useful is it for those in need of a comprehensive understanding or to take effective action?")

        st.subheader("Utility for General Guidance")
        st.write(utility_for_general_guidance)

        st.subheader("Utility for Comprehensive Understanding")
        st.write(utility_for_comprehensive_understanding)

# Run the main analysis
if __name__ == "__main__":
    main_analysis()
    # Auto-save user input to cache for persistence across sessions
    st.session_state['stored_query'] = stored_query
    st.session_state['stored_results'] = stored_results
    st.session_state['user_title'] = user_title
    st.session_state['user_article'] = user_article

    # Attempt to load cached input if available
    if 'stored_query' in st.session_state:
        stored_query = st.session_state['stored_query']
    if 'stored_results' in st.session_state:
        stored_results = st.session_state['stored_results']
    if 'user_title' in st.session_state:
        user_title = st.session_state['user_title']
    if 'user_article' in st.session_state:
        user_article = st.session_state['user_article']
