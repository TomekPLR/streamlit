import streamlit as st

# Define median values
medians = {
    'Good URLs': 80,
    'Bad URLs': 20,
    'URLs need improvement': 10,
    'Indexed Pages': 1000,
    'Not Indexed Pages': 100,
    # Add more median values for other fields as necessary
}

# Default images for each field (can be changed individually)
field_images = {
    'Good URLs': "default_image_url.png",
    'Bad URLs': "default_image_url.png",
    'URLs need improvement': "default_image_url.png",
    'Indexed Pages': "default_image_url.png",
    'Not Indexed Pages': "default_image_url.png",
    # Add more field images as necessary
}

# Messages for success or improvement based on comparison with median values
success_messages = {
    'Good URLs': "You have a good number of quality URLs. Great job!",
    'Bad URLs': "Your number of bad URLs is within a normal range.",
    'URLs need improvement': "The number of URLs that need improvement is acceptable.",
    'Indexed Pages': "Your number of indexed pages is impressive!",
    'Not Indexed Pages': "The number of not indexed pages is within expected limits.",
    # Add more success messages for other fields as necessary
}

improvement_messages = {
    'Good URLs': "Consider improving your quality URLs.",
    'Bad URLs': "You may have too many bad URLs. Consider reviewing them.",
    'URLs need improvement': "A significant number of URLs need improvement.",
    'Indexed Pages': "Look into why more of your pages aren't being indexed.",
    'Not Indexed Pages': "There are more not indexed pages than usual. Investigate!",
    # Add more improvement messages for other fields as necessary
}

field_groups = {
    'Core Web Vitals report': ['Good URLs', 'Bad URLs', 'URLs need improvement'],
    'Indexing report': ['Indexed Pages', 'Not Indexed Pages'],
    # Add more field groups as necessary
}

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs on your website.',
    'Indexing report': 'This report displays the indexing status of your website\'s pages.',
    # Add more group descriptions as necessary
}

# App layout styling
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("SEO Checker 🕵️‍♀️")
domain = st.text_input("Type your domain (without www) 🔗")

# Collect user input
user_values = {}

for group, fields in field_groups.items():
    with st.expander(group):
        st.markdown(f"<h2 style='text-align: center;'>{group}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{group_descriptions[group]}</p>", unsafe_allow_html=True)
        st.image(field_images.get(fields[0], "default_image_url.png"), use_column_width='always')
        for field in fields:
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(field_images[field], use_column_width='always')
            user_values[field] = st.number_input(f"Enter value for {field}", min_value=0)

# Process and display the results
if st.button("Compare 🔄"):
    with st.expander("Results"):
        st.subheader("Comparison Results:")

        for field in user_values:
            value = user_values[field]
            median_value = medians[field]
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(field_images[field], use_column_width='always')
            
            if value >= median_value:
                message = success_messages[field]
                st.success(f"✅ {field}: **{value}** - Better than median ({median_value}) 😃")
            else:
                message = improvement_messages[field]
                st.error(f"❌ {field}: **{value}** - Lower than median ({median_value}) 😟")
            
            st.markdown(f"<p style='text-align: center;'>{message}</p>", unsafe_allow_html=True)
            st.markdown("---")  # Visual divider
