# Define the default number of countries and catalogs to show
default_num_countries = 5
default_num_catalogs = 5

# Define the file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    pages_df = pd.read_csv(uploaded_file)

    # Convert the "Date" column to datetime format
    pages_df["Date"] = pd.to_datetime(pages_df["Date"], format="%b %d, %Y")

    # Define the date range selector
    start_date = st.sidebar.date_input("Select a start date", default_start_date)
    end_date = st.sidebar.date_input("Select an end date", default_end_date)
    
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')

    # Filter the pages data by date range
    pages_filtered = pages_df[(pages_df["Date"] >= start_date) & (pages_df["Date"] <= end_date)]

    # Create a chart of clicks by country and date
    clicks_by_country = pages_filtered.groupby(["Country", "Date"])["Url Clicks"].sum().reset_index()

    # Get the top countries by clicks
    top_countries = clicks_by_country.groupby("Country")["Url Clicks"].sum().sort_values(ascending=False)

    # Define the country selector
    countries_selected = st.sidebar.multiselect("Select countries:", top_countries.index, default=top_countries.index[:default_num_countries])

    # Filter the pages data by selected countries
    pages_countries = pages_filtered[pages_filtered["Country"].isin(countries_selected)]

    # Create a chart of clicks by catalog and date
    catalogs = pages_countries["Landing Page"].apply(lambda x: x.split("/")[1]).unique()
    catalogs_selected = st.sidebar.multiselect("Select catalogs:", catalogs, default=catalogs[:default_num_catalogs])

    # Define the metric selector
    metric = st.sidebar.selectbox("Select a metric:", ["Url Clicks", "Impressions", "URL CTR"])

    # Filter the pages data by selected catalogs
    pages_catalogs = pages_countries[pages_countries["Landing Page"].apply(lambda x: x.split("/")[1]).isin(catalogs_selected)]

    # Pivot the pages data to create a chart of clicks by catalog and date
    pivot = pd.pivot_table(pages_catalogs, values=metric, index="Date", columns=pages_catalogs["Landing Page"].apply(lambda x: x.split("/")[1]), aggfunc=sum)

    # Plot the chart
    fig2, ax2 = plt.subplots()
    pivot.plot(ax=ax2)
    ax2.set_title("Clicks by Catalog")
    st.pyplot(fig2)
