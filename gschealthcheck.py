import streamlit as st

# Define median values and custom messages
medians = {
    'Good URLs': 80,
    'Bad URLs': 10,
    'URLs need improvement': 10,
    'Indexed Pages': 95,
    'Not Indexed Pages': 5,
    # Add more medians for other fields if necessary
}

custom_messages = {
    '% of Good URLs': "<b>Good job</b> on having a high percentage of quality URLs!",
    'Indexed/Not indexed': "You have a healthy number of indexed pages. Keep it up!",
    # Add more custom messages for other fields if necessary
}

default_image = "https://your-default-image-url.png"

field_groups = {
    'Core Web Vitals report': ['Good URLs', 'Bad URLs', 'URLs need improvement'],
    'Indexing report': ['Indexed Pages', 'Not Indexed Pages'],
    # Add more groups and fields if necessary
}

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs on your website.',
    'Indexing report': 'This report displays the indexing status of your website\'s pages.',
    # Add more descriptions for other groups if necessary
}

# Input form
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

# Collect user values for each field
user_values = {}

for group, fields in field_groups.items():
    with st.expander(group):
        st.text(group_descriptions[group])
        st.image(default_image, use_column_width=True)
        for field in fields:
            user_values[field] = st.number_input(f"{field} 🧮", 0)

# Calculate the percentages based on the user input
if st.button("Calculate 🔄"):
    with st.expander("Results"):
        st.subheader("Comparison Results:")

        # Calculations for Core Web Vitals
        good_urls = user_values.get('Good URLs', 0)
        bad_urls = user_values.get('Bad URLs', 0)
        urls_need_improvement = user_values.get('URLs need improvement', 0)
        total_urls = good_urls + bad_urls + urls_need_improvement
        percent_good_urls = (good_urls / total_urls * 100) if total_urls else 0

        st.markdown(f"<p style='text-align: center;'>% of Good URLs: {percent_good_urls:.2f}%</p>", unsafe_allow_html=True)
        st.markdown(custom_messages['% of Good URLs'], unsafe_allow_html=True)

        # Calculations for Indexing report
        indexed_pages = user_values.get('Indexed Pages', 0)
        not_indexed_pages = user_values.get('Not Indexed Pages', 0)
        indexed_ratio = (indexed_pages / (indexed_pages + not_indexed_pages) * 100) if (indexed_pages + not_indexed_pages) else 0

        st.markdown(f"<p style='text-align: center;'>Indexed/Not indexed: {indexed_ratio:.2f}%</p>", unsafe_allow_html=True)
        st.markdown(custom_messages['Indexed/Not indexed'], unsafe_allow_html=True)

        # Add more calculations for other groups and fields if necessary

# Footer
st.markdown("---")
st.markdown("SEO Checker provided by GSC Mastery. Ensure your site is fully optimized!")

# Run the app with: streamlit run your_script.py
