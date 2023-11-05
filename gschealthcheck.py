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
    '% of indexed pages': 272,
    '% of pages classified as Crawled currently not indexed': 100,
    '% of URLs classified as discovered currently not indexed': 200
}

custom_messages = {
    '% of Good URLs': "Good job on having quality URLs!",
    'Average response time': "Your average response time can be improved.",
    'OK (200) + 304': "Ensure your server returns OK statuses.",
    '404': "Too many 404 errors, check your broken links.",
    '301': "Review your redirects to optimize load time.",
    '% of requests with server errors': "Investigate the server errors.",
    '% of pages with discovery purpose': "Enhance your content discoverability.",
    '% of requests for page resources': "Optimize your page resources.",
    '% of indexed pages': "Increase your indexed pages.",
    '% of pages classified as Crawled currently not indexed': "Ensure crawled pages are indexed.",
    '% of URLs classified as discovered currently not indexed': "Ensure discovered pages are indexed.",
}

# Define field groups
field_groups = {
    'Core Web Vitals report': [
        '% of Good URLs'
    ],
    'Crawl stats report': [
        'Average response time',
        'OK (200) + 304',
        '404',
        '301',
        '% of requests with server errors',
        '% of pages with discovery purpose',
        '% of requests for page resources'
    ],
    'Indexing report': [
        '% of indexed pages',
        '% of pages classified as Crawled currently not indexed',
        '% of URLs classified as discovered currently not indexed'
    ]
}

# Specify fields where lower is better
lower_is_better = {
    'Average response time',
    '404',
    '301',
    '% of requests with server errors',
    '% of requests for page resources',
    '% of pages classified as Crawled currently not indexed',
    '% of URLs classified as discovered currently not indexed'
}

# Input form
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}
for group, fields in field_groups.items():
    st.subheader(group)
    for field in fields:
        if '%' in field:
            user_values[field] = st.slider(f"{field} (%) 📊", 0, 100)
        else:
            user_values[field] = st.number_input(f"{field} 🧮", 0)

# Compare to median and display result
if st.button("Compare 🔄"):
    st.subheader("Comparison Results:")
    for group, fields in field_groups.items():
        st.subheader(group)
        for field in fields:
            median_value = medians[field]
            if field in lower_is_better:
                if user_values[field] < median_value:
                    st.write(f"{field}: **Better** than median ({median_value}) 😃")
                elif user_values[field] > median_value:
                    st.write(f"{field}: **Worse** than median ({median_value}) 😟")
                    st.write(f"👉 {custom_messages[field]}")
                else:
                    st.write(f"{field}: **Equal** to median ({median_value}) 😐")
            else:
                if user_values[field] < median_value:
                    st.write(f"{field}: **Lower** than median ({median_value}) 😟")
                    st.write(f"👉 {custom_messages[field]}")
                elif user_values[field] > median_value:
                    st.write(f"{field}: **Higher** than median ({median_value}) 😃")
                else:
                    st.write(f"{field}: **Equal** to median ({median_value}) 😐")
