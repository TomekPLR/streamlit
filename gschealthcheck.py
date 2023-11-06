import streamlit as st

# Define median values and custom messages
medians = {
    'Indexed/Not indexed': 1.2,  # Example median for the ratio of Indexed to Not indexed
    'Average response time': 300,
    'OK (200) + 304': 20,
    '404': 55,
    '301': 20,
    '% of requests with server errors': 24,
    '% of pages with discovery purpose': 10,
    '% of requests for page resources': 25,
    'Crawled/not indexed': 0.5,  # Example median for the ratio of Crawled to Not indexed
    'Discovered/not indexed': 1.0,  # Example median for the ratio of Discovered to Not indexed
    '% of Good URLs': 85,  # Example median for the percentage of Good URLs
}

custom_messages = {
    'Indexed/Not indexed': "Your indexing ratio can be improved.",
    # ... other custom messages ...
    '% of Good URLs': "Your website's URL quality can be better.",
    # ... other custom messages ...
}

# ... your other predefined data ...

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs.',
    'Crawl stats report': 'This report shows crawl statistics.',
    'Indexing report': 'This report shows indexing status.',
}

# Input form
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}
user_values['Good URLs'] = 0
user_values['Bad URLs'] = 0
user_values['URLs need improvement'] = 0
user_values['Indexed'] = 0
user_values['Not indexed'] = 0

for group, fields in field_groups.items():
    with st.expander(group):
        st.text(group_descriptions[group])
        st.image(default_image, use_column_width=True)
        for field in fields:
            st.markdown(f"<p style='font-size:18px; text-align: center;'>Enter {field}</p>", unsafe_allow_html=True)
            st.image(default_image, use_column_width=True)
            if field in ['Indexed', 'Not indexed']:
                user_values[field] = st.number_input(f"{field} 🧮", 0)
            elif field in ['Good URLs', 'Bad URLs', 'URLs need improvement']:
                user_values[field] = st.number_input(f"{field} 🧮", 0)
            else:
                if '%' in field:
                    user_values[field] = st.slider(f"{field} (%) 📊", 0, 100)
                else:
                    user_values[field] = st.number_input(f"{field} 🧮", 0)
            st.markdown("---")  # Visual divider

# Compare to median and display result
if st.button("Compare 🔄"):
    with st.expander("Results"):
        st.subheader("Comparison Results:")

        # Calculate the percentage of Good URLs
        total_urls = user_values['Good URLs'] + user_values['Bad URLs'] + user_values['URLs need improvement']
        if total_urls > 0:
            percent_good_urls = (user_values['Good URLs'] / total_urls) * 100
        else:
            percent_good_urls = 0
        user_values['% of Good URLs'] = percent_good_urls

        # Calculate the ratio of Indexed to Not indexed
        if user_values['Not indexed'] > 0:
            indexed_not_indexed_ratio = user_values['Indexed'] / user_values['Not indexed']
        else:
            indexed_not_indexed_ratio = 0
        user_values['Indexed/Not indexed'] = indexed_not_indexed_ratio

        for group, fields in field_groups.items():
            st.subheader(group)
            for field in fields:
                if field in user_values:  # Check if we have a calculated value to display
                    median_value = medians[field]
                    st.markdown(f"<p style='text-align: center;'>{field}</p>", unsafe_allow_html=True)
                    st.image(default_image, use_column_width=True)
                    value_to_compare = user_values[field]
                    # Custom comparison logic based on the type of value
                    if field in lower_is_better:
                        if value_to_compare < median_value:
                            st.write(f"{field}: **Better** than median ({median_value}) 😃\n")
                        elif value_to_compare > median_value:
                            st.write(f"{field}: **Worse** than median ({median_value}) 😟")
                            st.markdown(f"👉 {custom_messages[field]}", unsafe_allow_html=True)
                        else:
                            st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")
                    else:
                        if value_to_compare < median_value:
                            st.write(f"{field}: **Lower** than median ({median_value}) 😟")
                            st.markdown(f"👉 {custom_messages[field]}", unsafe_allow_html=True)
                        elif value_to_compare > median_value:
                            st.write(f"{field}: **Higher** than median ({median_value}) 😃\n")
                        else:
                            st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")

                    st.markdown("---")  # Visual divider
