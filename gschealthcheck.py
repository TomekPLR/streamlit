import streamlit as st
from PIL import Image

# Define median values and custom messages
medians = {
    #... (same as above)
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

# Input form
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}
for field in medians.keys():
    custom_image = Image.open("path_to_your_image.jpg")  # replace with your image path
    st.image(custom_image, caption=f"{field}", use_column_width=True)
    if '%' in field:
        user_values[field] = st.slider(f"{field} (%) 📊", 0, 100)
    else:
        user_values[field] = st.number_input(f"{field} 🧮", 0)

# Compare to median and display result
if st.button("Compare 🔄"):
    st.subheader("Comparison Results:")
    for field, median_value in medians.items():
        if user_values[field] < median_value:
            st.write(f"{field}: **Lower** than median ({median_value}) 😟")
            st.write(f"👉 {custom_messages[field]}")
        elif user_values[field] > median_value:
            st.write(f"{field}: **Higher** than median ({median_value}) 😃")
        else:
            st.write(f"{field}: **Equal** to median ({median_value}) 😐")
