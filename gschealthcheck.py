import streamlit as st

exclude_from_input = ['Number of Discovered not indexed pages', 'Number of Crawled not indexed pages', 'Percentage of Indexed pages', 'Percentage of Crawled Currently Not Indexed', 'Percentage of Discovered Currently Not Indexed', 'Percentage of Good URLs (Mobile)']  # Add field names you want to exclude from input
exclude_from_output = [ 'Number of Good URLs (Mobile)','Number of Need Improvement URLs (Mobile)','Number of Poor URLs (Mobile)','Number of pages not indexed',  ]  # Add field names you want to exclude from output


def calculate_indexed_percentage(total_pages, indexed_pages):
    """
    Calculate the percentage of indexed pages.

    :param total_pages: Total number of pages on the website.
    :param indexed_pages: Number of pages indexed by search engines.
    :return: Percentage of pages that are indexed.
    """
    if total_pages == 0:
        return 0  # Avoid division by zero

    percentage_indexed = (indexed_pages / total_pages) * 100
    return round(percentage_indexed, 2)  # Rounds to 2 decimal places

# Example usage
total = 1000  # Example: 1000 pages on your website
indexed = 800  # Example: 800 of those pages are indexed
print(f"Percentage of Indexed Pages: {calculate_indexed_percentage(total, indexed)}%")

# Define median values and custom messages
medians = {
    'Number of Good URLs (Mobile)': 100,
    'Number of Need Improvement URLs (Mobile)': 100,
    'Number of Poor URLs (Mobile)': 100,
    'Average response time': 300,
    'Percentage of OK (200) + Not Modified (304) requests': 20,
    'Percentage of 404s': 55,
    'Percentage of 301s': 20,
    'Percentage of server errors': 24,
    'Percentage of requests for Discovery purpose': 10,
    'Percentage of page resource load': 25,
    'Number of pages not indexed': 100,
    'Number of Discovered not indexed pages': 200,
    'Number of Crawled not indexed pages': 200,
    'Number of Indexed pages': 272,
    'Percentage of Indexed pages': 40,
    'Percentage of Crawled Currently Not Indexed': 272,
    'Percentage of Discovered Currently Not Indexed': 272,
    'Percentage of Good URLs (Mobile)': 100
    
}

# Define whether a higher or lower value is better for each field
better_higher = {
    'Percentage of Good URLs (Mobile)': True,
    'Average response time': False,
    'Percentage of OK (200) + Not Modified (304) requests': True,
    'Percentage of 404s': False,
    'Percentage of 301s': False,
    'Percentage of server errors': False,
    'Percentage of requests for Discovery purpose': True,
    'Percentage of page resource load': False,
    'Number of pages not indexed': False,
    'Number of Discovered not indexed pages': False,
    'Number of Crawled not indexed pages': False,
    'Percentage of Indexed Pages': True,

    

    'Number of Indexed pages': True,
}

# Custom messages for each field
success_messages = {
    'Percentage of Good URLs (Mobile)': "Excellent! Your Percentage of Good URLs (Mobile) percentage is outstanding.",
    'Average response time': "Fantastic! Your response time is faster than average.",
    'Percentage of OK (200) + Not Modified (304) requests': "Great! You're getting a high number of OK responses.",
    'Percentage of 404s': "Good work! You have fewer 404 errors than the median.",
    'Percentage of 301s': "Nicely done! Your redirects are fewer than the median, which could mean a more straightforward site structure.",
    'Percentage of server errors': "You're doing well! Your server errors are less than the median.",
    'Percentage of requests for Discovery purpose': "Superb! Your pages with discovery purpose are well above the median.",
    'Percentage of page resource load': "Well managed! Your requests for page resources are lower than the median.",
    'Number of pages not indexed': "That's good! You have fewer not indexed pages than the median.",
    'Number of Discovered not indexed pages': "You're on track! You have fewer discovered but not indexed pages than the median.",
        'Number of Crawled not indexed pages': "You're on track! You have fewer discovered but not indexed pages than the median.",

    'Number of Indexed pages': "Outstanding! You have more indexed pages than the median, which is great for SEO."
}

improvement_messages = {
    'Percentage of Good URLs (Mobile)': "Your website is slow on mobile devices. It negatively affects users visiting your website, rankings in Google, and crawl budget.<br> Pro Tip: Check out Google PageSpeed Insights. It's an excellent tool that diagnoses your site's issues and offers solutions to enhance its performance.",
    'Average response time': "A slow average response time can make Google less likely to discover your entire website. This means not all your important pages might be discovered or indexed.<br><b>Pro Tip:</b> you should talk to your developers about how you can fix average response time. One of the ways to do it is to invest in servers with better performance. ",
    'Percentage of OK (200) + Not Modified (304) requests': "It appears that Google is spending time on pages that aren't meant to be indexed.  This can distract it from focusing on your valuable content. As a result, many of your pages may encounter indexing issues.",
    'Percentage of 404s': "Google spends its budget on pages that don’t exist. <br><b>Pro tip:</b> I recommend using SEO crawlers (such as Screamingfrog) to ensure that there are no internal links pointing to 404 pages. Also, I recommend checking a sample of pages classified as 404 to ensure valid pages aren't erroneously showing 404s.",
    'Percentage of 301s': "Google spends its budget on pages that are redirected <br><b>Pro tip:</b> If you didn’t do any migration recently and still see a lot of requests coming to redirected pages, something is off. In such a caseI recommend using SEO crawlers (such as Screamingfrog) to ensure that there are no internal links pointing to redirected pages. <br>Also, I recommend checking a sample of pages classified as 301 to ensure valid pages aren't erroneously showing 301s for Googlebot. ",
    'Percentage of server errors': "Server errors send a clear signal to Google that your site can't handle Googlebot visits, which may discourage it from crawling your new pages.<br> <b>Pro tip:</b> you should talk to your developers about the possible causes of server errors. One of the solutions is investing in servers with better performance.  ",
    'Percentage of requests for Discovery purpose': "You're below the median in pages with discovery purpose. Enhancing content discoverability is key.",
    'Percentage of page resource load': "High page resource load is one of the biggest crawl budget killers. If Google is using too much of its crawl budget on rendering, it could neglect to visit and index some of your pages, categorizing them as Discovered - Currently not indexed. <br><b>Pro Tip: </b>talk to your developers about the issue. Consider upgrading to more powerful servers and implementing caching strategies to improve this metric.",
    'Number of pages not indexed': "You have more not indexed pages than the median. It's important to have these pages crawled and indexed.",
    'Number of Crawled not indexed pages': "Google decided that many of your pages shouldn't be indexed. <br><b>Pro tip:</b> to solve the issue review my video on how to fix Crawled - currently not indexed.",
    'Number of Indexed pages': "It seems that too many of your pages aren’t indexed in Google. As a result, they don’t get any traffic from the search engine. <br><b>Pro tip:</b> Visit the lesson: The High Five system to solve indexing issues."
}

# Default image for groups and fields
default_image = "https://gscmastery.com/wp-content/uploads/2023/09/cropped-gsc_mastery_logo-1.png"

# Custom images for each field and group (if needed, otherwise use default)
custom_images = {
    'Core Web Vitals report': "https://gscmastery.com/wp-content/uploads/2023/11/Monosnap-Core-Web-Vitals-🔊-2023-11-06-18-30-30.png",
    'Crawl stats report': "https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_statuses.png",
    'Indexing report': "https://gscmastery.com/wp-content/uploads/2023/gsc/page_indexed.png",
    'Average response time': "https://gscmastery.com/wp-content/uploads/2023/gsc/average_resp_time.png",     
    'Percentage of Good URLs (Mobile)': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_good.png',
    'Need improvement URLs': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_need_improvement.png',
    'Bad URLs': 'https://gscmastery.com/wp-content/uploads/2023/gsc/mobile_bad.png',
    'Percentage of OK (200) + Not Modified (304) requests': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stat_ok.png',
    'Percentage of 404s': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stats_404.png',
    'Percentage of 301s': 'https://gscmastery.com/wp-content/uploads/2023/gsc/crawl_stats_301.png',
    'Percentage of server errors': 'https://gscmastery.com/wp-content/uploads/2023/gsc/server_errors.png',
    'Percentage of requests for Discovery purpose': 'https://gscmastery.com/wp-content/uploads/2023/gsc/discovery.png',
    'Percentage of page resource load': 'https://gscmastery.com/wp-content/uploads/2023/gsc/page_resource.png',
    'Number of Indexed pages': 'https://gscmastery.com/wp-content/uploads/2023/gsc/indexed.png',
    'Number of pages not indexed': 'https://gscmastery.com/wp-content/uploads/2023/gsc/not_indexed.png',
    'Number of Discovered not indexed pages': 'https://gscmastery.com/wp-content/uploads/2023/gsc/discovered_not_indexed.png',
    'Number of Crawled not indexed pages': "https://gscmastery.com/wp-content/uploads/2023/gsc/crawled_not_indexed.png"


}

# Define the groups of fields and descriptions
field_groups = {
    'Core Web Vitals report': ['Percentage of Good URLs (Mobile)'],
    'Crawl stats report': ['Average response time', 'Percentage of OK (200) + Not Modified (304) requests', 'Percentage of 404s', 'Percentage of 301s', 'Percentage of server errors'],
    'Indexing report': ['Percentage of requests for Discovery purpose', 'Percentage of page resource load', 'Number of pages not indexed', 'Number of Discovered not indexed pages', 'Number of Indexed pages']
}

group_descriptions = { 
    'Core Web Vitals report': 'To access the report scroll down and click on Core Web Vitals. Alternatively, type this URL: https://search.google.com/search-console/core-web-vitals?resource_id=sc-domain%3A{your_domain}',
    'Crawl stats report': 'To access this report, you need to scroll down, click on "Settings" then "Crawl Stats". Alternatively, you can type this URL: https://search.google.com/u/0/search-console/settings/crawl-stats?resource_id=sc-domain%3A{your_domain}',
    'Indexing report': 'To enter data about indexing, go to Indexing -> Pages. Alternatively, click visit this URL: https://search.google.com/search-console/index?resource_id=sc-domain%3A{your_domain}',
}

# App layout styling
st.markdown("<style>body {font-size: 18px;}</style>", unsafe_allow_html=True)
st.title("GSC Health checker 🕵️‍♀️")

st.markdown("This is a quick, 3-5 minute check that will let you quickly diagnose your website based on some vital metrics from GSC. Your data is compared to median value from 200+ domains collected by Tomek Rudzki.")

user_values = {}


for group, fields in field_groups.items():
    with st.expander("Enter data from " + group + " report"):
        st.markdown(f"<h2 style='text-align: center;'>Enter data from your {group}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{group_descriptions[group]}</p>", unsafe_allow_html=True)
        st.image(custom_images.get(group, default_image), use_column_width='always')
        for field in fields:
            if field not in exclude_from_input:  # Check if field is not in exclude list
                st.markdown(f"<h3 style='text-align: center;'>Metric: {field}</h3>", unsafe_allow_html=True)
                st.image(custom_images.get(field, default_image), use_column_width='always')
                user_values[field] = st.number_input(f"Enter value for your {field}", min_value=0)
        if 'Number of Indexed pages' in fields and 'Number of pages not indexed' in fields:
            # Calculate percentage of indexed pages if both required fields are present
            indexed = user_values.get('Number of Indexed pages', 0)
            not_indexed = user_values.get('Number of pages not indexed', 0)
            total = indexed + not_indexed
            user_values['Percentage of Indexed pages'] = calculate_indexed_percentage(total, indexed)



# Compare to median and display result
if st.button("Do a Health check! 🔄"):
    # Compare to median and display result
    passed_checks = []
    failed_checks = []
    
    # Determine passed and failed checks
    for field, value in user_values.items():
        if field not in exclude_from_output:  # Exclude fields from output
            median_value = medians[field]
            better = better_higher[field]
            if (value > median_value and better) or (value < median_value and not better):
                passed_checks.append(field)
            else:
                failed_checks.append(field)
            
    total_checks = len(passed_checks)+len(failed_checks)
    passed_count = len(passed_checks)
    
    # Display summary results
    st.markdown(f"<h2 style='text-align: center;'>You passed {passed_count}/{total_checks} checks</h2>", unsafe_allow_html=True)
    st.markdown("---")  # Visual divider
    
    # List passed elements
    if passed_checks:
        st.markdown("### ✅ Passed Checks:")
        for check in passed_checks:
            if check not in exclude_from_output:  # Exclude fields from output
                st.markdown(f"- {check}")
    
    # List failed elements
    if failed_checks:
        st.markdown("### ❌ Checks to Improve:")
        if check not in exclude_from_output: 
            for check in failed_checks:
                st.markdown(f"- {check}")
    
    st.markdown("For detailed insights, see below.")
    st.markdown("---")  # Visual divider
    
    # Detailed results
    with st.expander("Detailed Results"):
        for field, value in user_values.items():
            if field not in exclude_from_output:  # Exclude fields from detailed results
                median_value = medians[field]
                better = better_higher[field]
                message = success_messages[field] if (value > median_value and better) or (value < median_value and not better) else improvement_messages[field]
                result_message = "✅" if (value > median_value and better) or (value < median_value and not better) else "❌"
                st.markdown(f"<h3 style='text-align: center;'>{field}</h3>", unsafe_allow_html=True)
                st.image(custom_images.get(field, default_image), use_column_width='always')
                st.markdown(f"<h4 style='text-align: center;'>{result_message} {field}: **{value}** {'higher' if better else 'lower'} than median ({median_value})</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{message}</p>", unsafe_allow_html=True)
                st.markdown("---")  # Visual divider
