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
    st.session_state['custom_prompt'] = "Here is my custom prompt. Query: {query}, Top10: {top10}, Title: {title}, Article: {article}"

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
    st.title("🔍 Tomek's article scorer")

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
    # Existing analysis code here

def custom_prompt_ui():
    st.session_state['custom_prompt'] = st.text_area("Custom Prompt", value=st.session_state['custom_prompt'], height=200)
    variables = {
        "query": st.session_state['stored_query'],
        "top10": st.session_state['stored_results'],
        "title": st.session_state['user_title'],
        "article": st.session_state['user_article']
    }
    custom_prompt = replace_variables(st.session_state['custom_prompt'], variables)
    if st.button("Run Custom Prompt"):
        custom_result = query_chatgpt(custom_prompt)
        st.write(custom_result)

if __name__ == "__main__":
    main_analysis()
