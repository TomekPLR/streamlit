import streamlit as st

# Define median values
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

# Input form
st.title("SEO Checker")
domain = st.text_input("Type your domain (without www)")
user_values = {}
for field in medians.keys():
    # Determine if percentage input is needed
    if '%' in field:
        user_values[field] = st.slider(f"{field} (%)", 0, 100)
    else:
        user_values[field] = st.number_input(f"{field}", 0)

# Compare to median and display result
if st.button("Compare"):
    st.subheader("Comparison Results:")
    for field, median_value in medians.items():
        if user_values[field] < median_value:
            st.write(f"{field}: **Lower** than median ({median_value})")
        elif user_values[field] > median_value:
            st.write(f"{field}: **Higher** than median ({median_value})")
        else:
            st.write(f"{field}: **Equal** to median ({median_value})")
