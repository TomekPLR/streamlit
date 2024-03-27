import streamlit as st
from openai import OpenAI
import os

# Initialize your OpenAI API key
os.environ['API_KEY'] = st.secrets['API_KEY']
openai = OpenAI(api_key=os.getenv('API_KEY'))

# Initialize Streamlit session state for storing user inputs
if 'stored_query' not in st.session_state:
    st.session_state['stored_query'] = ""
if 'stored_results' not in st.session_state:
    st.session_state['stored_results'] = ""
if 'user_title' not in st.session_state:
    st.session_state['user_title'] = ""
if 'user_article' not in st.session_state:
    st.session_state['user_article'] = ""

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
    st.title("🔍 Google Search Results and Article Analysis")

    with st.form("query_results_form"):
        st.session_state['stored_query'] = st.text_input("Query", st.session_state['stored_query'])
        st.session_state['stored_results'] = st.text_area("Top 10 Results", value=st.session_state['stored_results'], height=400)
        st.session_state['user_title'] = st.text_input("Your Title", st.session_state['user_title'])
        st.session_state['user_article'] = st.text_area("Your Article", value=st.session_state['user_article'], height=400)  # Field for user to type in the entire article
        submit_button = st.form_submit_button("🔎 Calculate")

    if submit_button:
        # Analysis on Google search results
        st.markdown("### 📊 Google Search Results Analysis")
        differences_summary = query_chatgpt(f"Here's the Google search results: {st.session_state['stored_results']}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the places 7-10.")
        st.subheader("✏️ Differences Summary")
        st.write(differences_summary)

        differences_with_user_title_summary = query_chatgpt(f"Here's the Google search results: {st.session_state['stored_results']}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the title proposed by the user: '{st.session_state['user_title']}'.")
        st.subheader("📝 Differences Summary with User Title")
        st.write(differences_with_user_title_summary)

        relevancy_score = query_chatgpt(f"How well is the '{st.session_state['user_title']}' proposed by the user relevant to the '{st.session_state['stored_query']}'?")
        st.subheader("🎯 Relevancy Score")
        st.write(relevancy_score)

        # New analysis on the article for signs of waffle content
        waffle_content_analysis = query_chatgpt(f"I have an article: {st.session_state['user_article']}\n\nLook for signs of waffle content, for instance: Repetition, Generalization, Lack of Depth, Limited Insights, Absence of Examples or Case Studies. Then judge how useful it's for the users typing in Google: 'Challenging Long-Term Disability Claim Denials'. Give me just summary, I don't need detailed problems in each category.  Give the general score at the end. Then give the score for those looking for general guidance followed by the score for those how useful is it for those in need of a comprehensive understanding or to take effective action?")
        st.markdown("### 📝 Article Waffle Content Analysis")
        st.write(waffle_content_analysis)

# Run the main analysis
if __name__ == "__main__":
    main_analysis()
