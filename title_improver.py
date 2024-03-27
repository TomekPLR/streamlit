import streamlit as st
from openai import OpenAI
import os

# Initialize your OpenAI API key
os.environ['API_KEY'] = st.secrets['API_KEY']
openai = OpenAI(api_key=os.getenv('API_KEY'))

# Initialize Streamlit session state for storing user inputs and custom prompt
if 'stored_query' not in st.session_state:
    st.session_state['stored_query'] = ""
if 'stored_results' not in st.session_state:
    st.session_state['stored_results'] = ""
if 'user_title' not in st.session_state:
    st.session_state['user_title'] = ""
if 'user_article' not in st.session_state:
    st.session_state['user_article'] = ""
if 'custom_prompt' not in st.session_state:
    st.session_state['custom_prompt'] = ""

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

def replace_variables(prompt, variables):
    for key, value in variables.items():
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt

def main_analysis():
    st.title("🔍 Tomek's Article Scorer")

    tab1, tab2 = st.tabs(["Main Analysis", "Custom GPT Prompts"])

    with tab1:
        with st.form("query_results_form"):
            st.session_state['stored_query'] = st.text_input("Query", st.session_state['stored_query'])
            st.session_state['stored_results'] = st.text_area("Top 10 Results", value=st.session_state['stored_results'], height=400)
            st.session_state['user_title'] = st.text_input("Your Title", st.session_state['user_title'])
            st.session_state['user_article'] = st.text_area("Your Article", value=st.session_state['user_article'], height=400)
            submit_button = st.form_submit_button("🔎 Calculate")

        if submit_button:
            perform_analysis()

    with tab2:
        custom_prompt_ui()

def perform_analysis():
    # Analysis on Google search results
    st.markdown("### 📊 Difference between top 3 and top 4-10")
    differences_summary = query_chatgpt(f"Here's the Google search results: {st.session_state['stored_results']}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the places 4-10. Be harsh. At the end give the similarity score 0 to 10")
    st.subheader("✏️ Differences Summary")
    st.write(differences_summary)

    differences_with_user_title_summary = query_chatgpt(f"Here's the Google search results: {st.session_state['stored_results']}. Give summary of what's the difference between focus of top 3 results (includes 1,2,3) and the title proposed by the user: '{st.session_state['user_title']}'. At the end, provide me with similarity score from 0 to 10. Be harsh. I prefer numeric score")
    st.subheader("📝 Differences - Your Title vs Top 3")
    st.write(differences_with_user_title_summary)

    relevancy_score = query_chatgpt(f"How well is the '{st.session_state['user_title']}' proposed by the user relevant to the '{st.session_state['stored_query']}'? Give me score 0 to 10. Be harsh. I prefer numeric value")
    st.subheader("🎯 Relevancy Score (Your Title & Query)")
    st.write(relevancy_score)

    # New analysis on the article for signs of waffle content
    waffle_content_analysis = query_chatgpt(f"I have an article: {st.session_state['user_article']}\n\nLook for signs of waffle content, for instance: Repetition, Generalization, Lack of Depth, Limited Insights, Absence of Examples or Case Studies. Then judge how useful it's for the users typing in Google: '{st.session_state['stored_query']}'. Give me just summary, I don't need detailed problems in each category. Give the general score at the end. Then give the score for those looking for general guidance followed by the score for those how useful is it for those in need of a comprehensive understanding or to take effective action
