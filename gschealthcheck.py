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
    '% of requuests for page resources': 25,
    '% of pages classified as Crawled currently not indedex': 100,
    '% of URLs classfied as discovered currently not indexed': 200,
    '% of indexed pages': 272,
}

custom_messages = {
    '% of Good URLs': "Good job on having a high percentage of quality URLs!",
    'Average response time': "Your average response time can be improved.",
    'OK (200) + 304': "Ensure your server returns more OK statuses.",
    '404': "Too many 404 errors, check your broken links.",
    '301': "Review your redirects to optimize load time.",
    '% of requests with server errors': "Investigate the server errors.",
    '% of pages with discovery purpose': "Enhance your content discoverability.",
    '% of requuests for page resources': "Optimize your page resources.",
    '% of pages classified as Crawled currently not indedex': "Ensure crawled pages are indexed.",
    '% of URLs classfied as discovered currently not indexed': "Ensure discovered pages are indexed.",
    '% of indexed pages': "Increase your indexed pages.",
}

lower_is_better = [
    'Average response time', '301', '404', 
    '% of requests with server errors', '% of requuests for page resources',
    '% of pages classified as Crawled currently not indedex',
    '% of URLs classfied as discovered currently not indexed',
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
        '% of requuests for page resources',
    ],
    'Indexing report': [
        '% of pages classified as Crawled currently not indedex',
        '% of URLs classfied as discovered currently not indexed',
        '% of indexed pages',
    ]
}

# Input form
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}
for group, fields in field_groups.items():
    with st.expander(group):
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
                if field in lower_is_better:
                    if user_values[field] < median_value:
                        st.write(f"{field}: **Better** than median ({median_value}) 😃\n")
                    elif user_values[field] > median_value:
                        st.write(f"{field}: **Worse** than median ({median_value}) 😟")
                        st.write(f"👉 {custom_messages[field]}\n")
                    else:
                        st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")
                else:
                    if user_values[field] < median_value:
                        st.write(f"{field}: **Lower** than median ({median_value}) 😟")
                        st.write(f"👉 {custom_messages[field]}\n")
                    elif user_values[field] > median_value:
                        st.write(f"{field}: **Higher** than median ({median_value}) 😃\n")
                    else:
                        st.write(f"{field}: **Equal** to median ({median_value}) 😐\n")
                
                st.markdown("---")  # Visual divider
