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
    'Crawled not indexed': 200,
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
        'Crawled not indexed': False,

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
        'Crawled not indexed': "You're on track! You have fewer discovered but not indexed pages than the median.",

    'Indexed': "Outstanding! You have more indexed pages than the median, which is great for SEO."
}

improvement_messages = {
    'Good URLs': "Your website is slow on mobile devices. It negatively affects users visiting your website, rankings in Google, and crawl budget.<br> Pro Tip: Check out Google PageSpeed Insights. It's an excellent tool that diagnoses your site's issues and offers solutions to enhance its performance.",
    'Average response time': "A slow average response time can make Google less likely to discover your entire website. This means not all your important pages might be discovered or indexed.<br><b>Pro Tip:</b> you should talk to your developers about how you can fix average response time. One of the ways to do it is to invest in servers with better performance. ",
    'OK (200) + 304': "It appears that Google is spending time on pages that aren't meant to be indexed.  This can distract it from focusing on your valuable content. As a result, many of your pages may encounter indexing issues.",
    '404': "Google spends its budget on pages that don’t exist. <br><b>Pro tip:</b> I recommend using SEO crawlers (such as Screamingfrog) to ensure that there are no internal links pointing to 404 pages. Also, I recommend checking a sample of pages classified as 404 to ensure valid pages aren't erroneously showing 404s.",
    '301': "Google spends its budget on pages that are redirected <br><b>Pro tip:</b> If you didn’t do any migration recently and still see a lot of requests coming to redirected pages, something is off. In such a caseI recommend using SEO crawlers (such as Screamingfrog) to ensure that there are no internal links pointing to redirected pages. <br>Also, I recommend checking a sample of pages classified as 301 to ensure valid pages aren't erroneously showing 301s for Googlebot. ",
    'Server errors': "Server errors send a clear signal to Google that your site can't handle Googlebot visits, which may discourage it from crawling your new pages.<br> <b>Pro tip:</b> you should talk to your developers about the possible causes of server errors. One of the solutions is investing in servers with better performance.  ",
    'Discovery': "You're below the median in pages with discovery purpose. Enhancing content discoverability is key.",
    'Resource requests': "High page resource load is one of the biggest crawl budget killers. If Google is using too much of its crawl budget on rendering, it could neglect to visit and index some of your pages, categorizing them as Discovered - Currently not indexed. <br><b>Pro Tip: </b>talk to your developers about the issue. Consider upgrading to more powerful servers and implementing caching strategies to improve this metric.",
    'Not indexed': "You have more not indexed pages than the median. It's important to have these pages crawled and indexed.",
    'Crawled not indexed': "Google decided that many of your pages shouldn't be indexed. <br><b>Pro tip:</b> to solve the issue review my video on how to fix Crawled - currently not indexed.",
    'Indexed': "It seems that too many of your pages aren’t indexed in Google. As a result, they don’t get any traffic from the search engine. <br><b>Pro tip:</b> Visit the lesson: The High Five system to solve indexing issues."
}

# Default image for groups and fields
default_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"

# Custom images for each field and group (if needed, otherwise use default)
custom_images = {
    'Core Web Vitals report': "https://gscmastery.com/wp-content/uploads/2023/11/Monosnap-Core-Web-Vitals-🔊-2023-11-06-18-30-30.png",
    'Crawl stats report': "https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_statuses.png",
    'Indexing report': "https://gscmastery.com/wp-content/uploads/2023/gsc/page_indexed.png",
    'Average response time': "https://gscmastery.com/wp-content/uploads/2023/gsc/average_resp_time.png",     
    'Good URLs': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_good.png',
    'Need improvement URLs': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_need_improvement.png',
    'Bad URLs': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_bad.png',
    'OK (200) + 304': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stat_ok.png',
    '404': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stats_404.png',
    '301': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stats_301.png',
    'Server errors': 'https://gscmastery.com/wp-content/uploads/2023/gsc/server_errors.png',
    'Discovery': 'https://gscmastery.com/wp-content/uploads/2023/gsc/discovery.png',
    'Resource requests': 'https://gscmastery.com/wp-content/uploads/2023/gsc/page_resource.png',
    'Indexed': 'https://gscmastery.com/wp-content/uploads/2023/gsc/indexed.png',
    'Not indexed': 'https://gscmastery.com/wp-content/uploads/2023/gsc/not_indexed.png',
    'Discovered not indexed': 'https://gscmastery.com/wp-content/uploads/2023/gsc/discovered_not_indexed.png',
    'Crawled not indexed': "https://gscmastery.com/wp-content/uploads/2023/gsc/crawled_not_indexed.png"


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
st.title("GSC Health checker 🕵️‍♀️")

# Input form
st.text_input("Type your domain (without www) - OPTIONAL🔗")

user_values = {}

for group, fields in field_groups.items():
    with st.expander("Enter data from " +  group + " report"):
        st.markdown(f"<h2 style='text-align: center;'>Enter your {group}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{group_descriptions[group]}</p>", unsafe_allow_html=True)
        st.image(custom_images.get(group, default_image), use_column_width='always')
        for field in fields:
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(custom_images.get(field, default_image), use_column_width='always')
            user_values[field] = st.number_input(f"Enter value for your {field}", min_value=0)

# Compare to median and display result
if st.button("Do a Health check! 🔄"):
    # Compare to median and display result
    passed_checks = []
    failed_checks = []
    
    # Determine passed and failed checks
    for field, value in user_values.items():
        median_value = medians[field]
        better = better_higher[field]
        if (value > median_value and better) or (value < median_value and not better):
            passed_checks.append(field)
        else:
            failed_checks.append(field)
            
    total_checks = len(user_values)
    passed_count = len(passed_checks)
    
    # Display summary results
    st.markdown(f"<h2 style='text-align: center;'>You passed {passed_count}/{total_checks} checks</h2>", unsafe_allow_html=True)
    st.markdown("---")  # Visual divider
    
    # List passed elements
    if passed_checks:
        st.markdown("### ✅ Passed Checks:")
        for check in passed_checks:
            st.markdown(f"- {check}")
    
    # List failed elements
    if failed_checks:
        st.markdown("### ❌ Checks to Improve:")
        for check in failed_checks:
            st.markdown(f"- {check}")
    
    st.markdown("For detailed insights, see below.")
    st.markdown("---")  # Visual divider
    
    # Detailed results
    with st.expander("Detailed Results"):
        for field, value in user_values.items():
            median_value = medians[field]
            better = better_higher[field]
            message = success_messages[field] if (value > median_value and better) or (value < median_value and not better) else improvement_messages[field]
            result_message = "✅" if (value > median_value and better) or (value < median_value and not better) else "❌"
            st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
            st.image(custom_images.get(field, default_image), use_column_width='always')
            st.markdown(f"<h4 style='text-align: center;'>{result_message} {field}: **{value}** {'higher' if better else 'lower'} than median ({median_value})</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{message}</p>", unsafe_allow_html=True)
            st.markdown("---")  # Visual divider

