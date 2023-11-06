import streamlit as st

# Define median values and custom messages
medians = {
    'Good URLs': 100,
    'Average response time': 300,
    'OK (200) + 304': 20,
    '404': 55,
    '301': 20,
    'Server errors': 24,
    'Discovery': 10,
    'Resource requests': 25,
    'Not indexed': 100,
    'Discovered not indexed': 200,
    'Indexed': 272,
}

# Define whether a higher or lower value is better for each field
better_higher = {
    'Good URLs': True,
    'Average response time': False,
    'OK (200) + 304': True,
    '404': False,
    '301': False,
    'Server errors': False,
    'Discovery': True,
    'Resource requests': False,
    'Not indexed': False,
    'Discovered not indexed': False,
    'Indexed': True,
}

# Custom messages for each field
success_messages = {
    'Good URLs': "Excellent! Your Good URLs percentage is outstanding.",
    'Average response time': "Fantastic! Your response time is faster than average.",
    'OK (200) + 304': "Great! You're getting a high number of OK responses.",
    '404': "Good work! You have fewer 404 errors than the median.",
    '301': "Nicely done! Your redirects are fewer than the median, which could mean a more straightforward site structure.",
    'Server errors': "You're doing well! Your server errors are less than the median.",
    'Discovery': "Superb! Your pages with discovery purpose are well above the median.",
    'Resource requests': "Well managed! Your requests for page resources are lower than the median.",
    'Not indexed': "That's good! You have fewer not indexed pages than the median.",
    'Discovered not indexed': "You're on track! You have fewer discovered but not indexed pages than the median.",
    'Indexed': "Outstanding! You have more indexed pages than the median, which is great for SEO."
}

improvement_messages = {
    'Good URLs': "There's room for improvement. Aim to increase your Good URLs percentage.",
    'Average response time': "Looks like your response time could be faster. It's an important factor for both users and SEO.",
    'OK (200) + 304': "It's good to aim for more OK responses to improve user experience.",
    '404': "You might want to check on those 404 errors. They're above the median and can negatively affect the user experience.",
    '301': "There's potential to streamline your redirects. Too many can impact load times and user navigation.",
    'Server errors': "Server errors are higher than the median. It's crucial to investigate and resolve these.",
    'Discovery': "You're below the median in pages with discovery purpose. Enhancing content discoverability is key.",
    'Resource requests': "Your page resource requests are above the median, which could slow down your site.",
    'Not indexed': "You have more not indexed pages than the median. It's important to have these pages crawled and indexed.",
    'Discovered not indexed': "There are more discovered but not indexed pages than the median. Ensure they get indexed for better visibility.",
    'Indexed': "The number of indexed pages is below the median. You'll want to work on improving this for better search presence."
}

# Default image for groups and fields
default_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"

# Custom images for each field and group (if needed, otherwise use default)
custom_images = {
    'Core Web Vitals report': "https://gscmastery.com/wp-content/uploads/2023/11/Monosnap-Core-Web-Vitals-🔊-2023-11-06-18-30-30.png",
    'Crawl stats report': "https://gscmastery.com/wp-content/uploads/2023/11/crawl_stats.png",
    'Indexing report': "https://gscmastery.com/wp-content/uploads/2023/11/page_indexed.png",
    # ... (add custom URLs for groups or fields as necessary)
}

# Define the groups of fields and descriptions
field_groups = {
    'Core Web Vitals report': ['Good URLs'],
    'Crawl stats report': ['Average response time', 'OK (200) + 304', '404', '301', 'Server errors'],
    'Indexing report': ['Discovery', 'Resource requests', 'Not indexed', 'Discovered not indexed', 'Indexed']
}

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs.',
    'Crawl stats report': 'This report shows crawl statistics.',
    'Indexing report': 'This report shows indexing status.',
}

# App layout styling
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("SEO Checker 🕵️‍♀️")

# Input form
st.text_input("Type your domain (without www) 🔗")

user_values = {}

for group, fields in field_groups.items():
    with st.expander(group):
        st.markdown(f"<h2 style='text-align: center;'>{group}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{group_descriptions[group]}</p>", unsafe_allow_html=True)
        st.image(custom_images.get(group, default_image), use_column_width='always')
        for field in fields:
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(custom_images.get(field, default_image), use_column_width='always')
            user_values[field] = st.number_input(f"Enter value for {field}", min_value=0)

# Compare to median and display result
if st.button("Compare 🔄"):
    with st.expander("Results"):
        for field, value in user_values.items():
            median_value = medians[field]
            better = better_higher[field]
            message = success_messages[field] if (value > median_value and better) or (value < median_value and not better) else improvement_messages[field]
            result_message = "✅" if (value > median_value and better) or (value < median_value and not better) else "❌"
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(custom_images.get(field, default_image), use_column_width='always')
            st.markdown(f"<h4 style='text-align: center;'>{result_message} {field}: **{value}** {'worse' if better else 'Lower'} than median ({median_value})</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{message}</p>", unsafe_allow_html=True)
            st.markdown("---")  # Visual divider
