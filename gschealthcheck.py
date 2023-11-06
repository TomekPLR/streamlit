import streamlit as st

# Define median values and custom messages
medians = {
    'Indexed': 272,
    'Not indexed': 100,
    'Good URLs': 100,
    'Bad URLs': 55,
    'URLs Need Improvement': 20,
    'Average response time': 300,
    'OK (200) + 304': 20,
    '404': 55,
    '301': 20,
    '% of requests with server errors': 24,
    '% of requests for page resources': 25,
    '% of pages with discovery purpose': 10,
}

custom_messages = {
    'Indexed': "Increase your <b>indexed pages</b>.",
    'Not indexed': "Ensure <b>discovered pages</b> are indexed.",
    'Good URLs': "<b>Good job</b> on having a high percentage of quality URLs!",
    'Bad URLs': "Too many <i>404 errors</i>, check your broken links.",
    'URLs Need Improvement': "There's room for improvement. Optimize your URLs for better performance.",
    'Average response time': "Your <i>average response time</i> can be improved.",
    # ... other messages
}

group_descriptions = {
    'Core Web Vitals report': 'This report shows the quality of URLs in terms of their status and performance.',
    'Crawl stats report': 'This report shows crawl statistics for your site and how it can be optimized.',
    'Indexing report': 'This report details the status of your site\'s URLs whether they have been indexed or not.',
}

# Default image
default_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"

# Set up layout
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("SEO Checker 🕵️‍♀️")

# Input form
domain = st.text_input("Type your domain (without www) 🔗")

user_values = {}

# Input for Good URLs vs Bad URLs vs URLs Need Improvement
good_urls = st.number_input("Good URLs 🟢", 0)
bad_urls = st.number_input("Bad URLs 🔴", 0)
urls_need_improvement = st.number_input("URLs Need Improvement 🟡", 0)

total_urls = good_urls + bad_urls + urls_need_improvement
percent_good_urls = (good_urls / total_urls * 100) if total_urls > 0 else 0
user_values['% of Good URLs'] = percent_good_urls

# Input for Indexed vs Not indexed
indexed_pages = st.number_input("Indexed Pages 📈", 0)
not_indexed_pages = st.number_input("Not Indexed Pages 📉", 0)

indexed_ratio = (indexed_pages / (indexed_pages + not_indexed_pages) * 100) if (indexed_pages + not_indexed_pages) > 0 else 0
user_values['% of indexed pages'] = indexed_ratio

# Here you should add inputs for the other values you want to track, similarly to above.
# ...

# Compare to median and display result
if st.button("Compare 🔄"):
    with st.expander("Results"):
        st.subheader("Comparison Results:")
        
        # Check and display for Good URLs
        st.markdown(f"### % of Good URLs")
        st.markdown(f"<p style='text-align: center;'>Good URLs: {good_urls} 🔵</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Bad URLs: {bad_urls} 🔴</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>URLs Need Improvement: {urls_need_improvement} 🟡</p>", unsafe_allow_html=True)
        st.markdown(f"👉 <b>Percentage of Good URLs: {percent_good_urls:.2f}%</b>", unsafe_allow_html=True)
        st.markdown("---")  # Visual divider
        
        # Check and display for Indexed Pages
        st.markdown(f"### % of Indexed Pages")
                st.markdown(f"<p style='text-align: center;'>Indexed Pages: {indexed_pages} ✅</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Not Indexed Pages: {not_indexed_pages} ❌</p>", unsafe_allow_html=True)
        st.markdown(f"👉 <b>Percentage of Indexed Pages: {indexed_ratio:.2f}%</b>", unsafe_allow_html=True)
        st.markdown("---")  # Visual divider

        # Add more comparisons as needed for other metrics
        # For example:
        # for field in medians.keys():
        #     median_value = medians[field]
        #     st.markdown(f"<p style='text-align: center;'>{field}</p>", unsafe_allow_html=True)
        #     user_value = user_values.get(field, 0)
        #     # Comparison logic here...
        #     st.markdown("---")  # Visual divider

        # Example of detailed comparison for 'Average response time'
        median_response_time = medians['Average response time']
        user_response_time = st.number_input("Average response time (ms) 🕒", 0)
        if user_response_time > median_response_time:
            st.markdown("Your response time is **higher** than the median, which may affect user experience negatively. Consider investigating potential causes and optimizing your server's response time.")
        elif user_response_time < median_response_time:
            st.markdown("Your response time is **lower** than the median, which is great for user experience!")
        else:
            st.markdown("Your response time matches the median. It's an average performance.")

        # Continue adding comparisons for the rest of your fields

# Footer
st.markdown("---")
st.markdown("SEO Checker provided by GSC Mastery. Ensure your site is fully optimized!")

# Run the app with: streamlit run your_script.py

