import streamlit as st
from PIL import Image

# Define median values and custom messages
medians = {
    'Poor URLs for mobile': 100,
    'URLs need improvement': 200,
    'Good URLs': 100,
    'Average response time': 300,
    'OK (200) + 304': 20,
    '404': 55,
    '301': 20,
    '% of requests with server errors': 24,
    'purpose_discovery': 10,
    'page_resource': 25,
    'Number of indexed pages': 272,
    'number of unindexed pages': 935,
    'number of pages classified as Crawled currently not indexed': 100,
    'number of pages classfied as discovered currently not indexed': 200
}

custom_messages = {
    'Poor URLs for mobile': "Optimize your mobile URLs for better performance.",
    'URLs need improvement': "Consider improving your URLs for better SEO.",
    'Good URLs': "Good job on having quality URLs!",
    'Average response time': "Your average response time can be improved.",
    'OK (200) + 304': "Ensure your server returns OK statuses.",
    '404': "Too many 404 errors, check your broken links.",
    '301': "Review your redirects to optimize load time.",
    '% of requests with server errors': "Investigate the server errors.",
    'purpose_discovery': "Enhance your content discoverability.",
    'page_resource': "Optimize your page resources.",
    'Number of indexed pages': "Increase your indexed pages.",
    'number of unindexed pages': "Decrease the number of unindexed pages.",
    'number of pages classified as Crawled currently not indexed': "Ensure crawled pages are indexed.",
    'number of pages classfied as discovered currently not indexed': "Ensure discovered pages are indexed.",
}

# Define field groups
field_groups = {
    'Core Web Vitals report': [
        'Poor URLs for mobile',
        'URLs need improvement',
        'Good URLs'
    ],
    'Crawl stats report': [
        'Average response time',
        'OK (200) + 304',
        '404',
        '301',
        '% of requests with server errors',
        'purpose_discovery',
        'page_resource'
    ],
    'Indexing report': [
        'Number of indexed pages',
        'number of unindexed pages',
        'number of pages classified as Crawled currently not indexed',
        'number of pages classfied as discovered currently not indexed'
    ]
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
            if user_values[field] < median_value:
                st.write(f"{field}: **Lower** than median ({median_value}) 😟")
                st.write(f"👉 {custom_messages[field]}")
            elif user_values[field] > median_value:
                st.write(f"{field}: **Higher** than median ({median_value}) 😃")
            else:
                st.write(f"{field}: **Equal** to median ({median_value}) 😐")
