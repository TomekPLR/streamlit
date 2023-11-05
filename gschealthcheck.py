import streamlit as st

# Define median values and custom messages
medians = {
    '% of Good URLs': 100,
    'Average response time': 300,
    'OK (200) + 304': 20,
    '404': 55,
    '301': 20,
    '% of requests with server errors': 24,
    '% of pages with discovery purpose': 10,
    '% of requests for page resources': 25,
    '% of pages classified as Crawled currently not indexed': 100,
    '% of URLs classified as discovered currently not indexed': 200,
    '% of indexed pages': 272,
}

custom_messages = {
    '% of Good URLs': "<b>Good job</b> on having a high percentage of quality URLs!",
    'Average response time': "Your <i>average response time</i> can be improved.",
    'OK (200) + 304': "Ensure your server returns more <b>OK statuses</b>.",
    '404': "Too many <i>404 errors</i>, check your broken links.",
    '301': "Review your <b>redirects</b> to optimize load time.",
    '% of requests with server errors': "Investigate the <b>server errors</b>.",
    '% of pages with discovery purpose': "Enhance your <b>content discoverability</b>.",
    '% of requests for page resources': "Optimize your <b>page resources</b>.",
    '% of pages classified as Crawled currently not indexed': "Ensure <b>crawled pages</b> are indexed.",
    '% of URLs classified as discovered currently not indexed': "Ensure <b>discovered pages</b> are indexed.",
    '% of indexed pages': "Increase your <b>indexed pages</b>.",
}

custom_images = {
    '% of Good URLs': "https://example.com/good-urls-image.png",
    'Average response time': "https://example.com/average-response-time-image.png",
    # Add more images here
}

lower_is_better = [
    'Average response time', '301', '404', 
    '% of requests with server errors', '% of requests for page resources',
    '% of pages classified as Crawled currently not indexed',
    '% of URLs classified as discovered currently not indexed',
]

field_groups = {
    'Core Web Vitals report': ['% of Good URLs'],
    'Crawl stats report': [
        'Average response time',
        'OK (200) + 304',
        '404',
        '301',
        '% of requests with server errors',
        '% of pages with discovery purpose',
        '% of requests for page resources',
    ],
    'Indexing report': [
        '% of pages classified as Crawled currently not indexed',
        '% of URLs classified as discovered currently not indexed',
        '% of indexed pages',
    ]
}

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs.',
    'Crawl stats report': 'This report shows crawl statistics.',
    'Indexing report': 'This report shows indexing status.',
}

default_item_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"
default_group_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"

# Input form
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}
for group, fields in field_groups.items():
    with st.expander(group):
        st.markdown(f"<p style='text-align: center;'>{group_descriptions[group]}</p>", unsafe_allow_html=True)
        st.image(default_group_image, width=300, use_column_width=False, output_format='PNG')
        for field in fields:
            if '%' in field:
                user_values[field] = st.slider(f"{field} (%) 📊", 0, 100)
            else:
                user_values[field] = st.number_input(f"{field} 🧮", 0)

# Compare to median and display result
if st.button("Compare 🔄"):
    with st.expander("Results"):
        st.subheader("Comparison Results:")
        for group, fields in field_groups.items():
            st.subheader(group)
            for field in fields:
                median_value = medians[field]
                
                st.image(custom_images.get(field, default_item_image), width=100, use_column_width=False, output_format='PNG')
                
                if field in lower_is_better:
                    if user_values[field] < median_value:
                        st.write(f"{field}: **Better** than median ({median_value}) 😃\n")
                    elif user_values[field] > median_value:
                        st.write(f"{field}: **Worse** than median ({median_value}) 😟")
                        st.markdown(f"👉 {custom_messages[field]}", unsafe_allow_html=True)
                    else:
                        st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")
                else:
                    if user_values[field] < median_value:
                        st.write(f"{field}: **Lower** than median ({median_value}) 😟")
                        st.markdown(f"👉 {custom_messages[field]}", unsafe_allow_html=True)
                    elif user_values[field] > median_value:
                        st.write(f"{field}: **Higher** than median ({median_value}) 😃\n")
                    else:
                        st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")
                
                st.markdown("---")  # Visual divider
