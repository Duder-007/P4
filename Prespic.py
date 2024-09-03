import streamlit as st
import pandas as pd
import altair as alt

# Step 1: Load and clean the data
@st.cache_data
def load_data():
    df = pd.read_csv("gdp_year_with_more.csv")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Replace NaN values with 0
    df = df.fillna(0)

    # Function to clean and convert columns to float
    def clean_column(column):
        # Remove any non-numeric characters and convert to float
        df[column] = df[column].replace({'\$': '', ',': ''}, regex=True)
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert non-numeric to NaN
        df[column] = df[column].fillna(0)  # Replace NaN with 0
        df[column] = df[column].astype(float)
    
    # Clean specific columns
    clean_column('gdp')
    clean_column('growth')
    clean_column('inflation_rate')
    clean_column('debt')
    clean_column('increase')

    return df

df = load_data()

# President Image URLs (these URLs are from the official White House website)
president_images = {
  # President Image URLs (these URLs are from the official White House website)
    "George Washington": "https://www.whitehouse.gov/wp-content/uploads/2021/01/01_georgewashington.jpg",
    "John Adams": "https://www.whitehouse.gov/wp-content/uploads/2021/01/02_johnadams.jpg",
    "Thomas Jefferson": "https://www.whitehouse.gov/wp-content/uploads/2021/01/03_thomasjefferson.jpg",
    "James Madison": "https://www.whitehouse.gov/wp-content/uploads/2021/01/04_jamesmadison.jpg",
    "James Monroe": "https://www.whitehouse.gov/wp-content/uploads/2021/01/05_jamesmonroe.jpg",
    "John Quincy Adams": "https://www.whitehouse.gov/wp-content/uploads/2021/01/06_johnquincyadams.jpg",
    "Andrew Jackson": "https://www.whitehouse.gov/wp-content/uploads/2021/01/07_andrewjackson.jpg",
    "Martin Van Buren": "https://www.whitehouse.gov/wp-content/uploads/2021/01/08_martinvanburen.jpg",
    "William Henry Harrison": "https://www.whitehouse.gov/wp-content/uploads/2021/01/09_williamhenryharrison.jpg",
    "John Tyler": "https://www.whitehouse.gov/wp-content/uploads/2021/01/10_johntyler.jpg",
    "James K. Polk": "https://www.whitehouse.gov/wp-content/uploads/2021/01/11_jameskpolk.jpg",
    "Zachary Taylor": "https://www.whitehouse.gov/wp-content/uploads/2021/01/12_zacharytaylor.jpg",
    "Millard Fillmore": "https://www.whitehouse.gov/wp-content/uploads/2021/01/13_millardfillmore.jpg",
    "Franklin Pierce": "https://www.whitehouse.gov/wp-content/uploads/2021/01/14_franklinpierce.jpg",
    "James Buchanan": "https://www.whitehouse.gov/wp-content/uploads/2021/01/15_jamesbuchanan.jpg",
    "Abraham Lincoln": "https://www.whitehouse.gov/wp-content/uploads/2021/01/16_abrahamlincoln.jpg",
    "Andrew Johnson": "https://www.whitehouse.gov/wp-content/uploads/2021/01/17_andrewjohnson.jpg",
    "Ulysses S. Grant": "https://www.whitehouse.gov/wp-content/uploads/2021/01/18_ulyssessgrant.jpg",
    "Rutherford B. Hayes": "https://www.whitehouse.gov/wp-content/uploads/2021/01/19_rutherfordbhayes.jpg",
    "James A. Garfield": "https://www.whitehouse.gov/wp-content/uploads/2021/01/20_jamesagarfield.jpg",
    "Chester A. Arthur": "https://www.whitehouse.gov/wp-content/uploads/2021/01/21_chesteraarthur.jpg",
    "Grover Cleveland": "https://www.whitehouse.gov/wp-content/uploads/2021/01/22_grovercleveland.jpg",
    "Benjamin Harrison": "https://www.whitehouse.gov/wp-content/uploads/2021/01/23_benjaminharrison.jpg",
    "William McKinley": "https://www.whitehouse.gov/wp-content/uploads/2021/01/25_williammckinley.jpg",
    "Theodore Roosevelt": "https://www.whitehouse.gov/wp-content/uploads/2021/01/26_theodoreroosevelt.jpg",
    "William Howard Taft": "https://www.whitehouse.gov/wp-content/uploads/2021/01/27_williamhowardtaft.jpg",
    "Woodrow Wilson": "https://www.whitehouse.gov/wp-content/uploads/2021/01/28_woodrowwilson.jpg",
    "Warren G. Harding": "https://www.whitehouse.gov/wp-content/uploads/2021/01/29_warrengharding.jpg",
    "Calvin Coolidge": "https://www.whitehouse.gov/wp-content/uploads/2021/01/30_calvincoolidge.jpg",
    "Herbert Hoover": "https://www.whitehouse.gov/wp-content/uploads/2021/01/31_herberthoover.jpg",
    "Franklin D. Roosevelt": "https://www.whitehouse.gov/wp-content/uploads/2021/01/32_franklindroosevelt.jpg",
    "Harry S. Truman": "https://www.whitehouse.gov/wp-content/uploads/2021/01/33_harrystruman.jpg",
    "Dwight D. Eisenhower": "https://www.whitehouse.gov/wp-content/uploads/2021/01/34_dwightdeisenhower.jpg",
    "John F. Kennedy": "https://www.whitehouse.gov/wp-content/uploads/2021/01/35_johnfkennedy.jpg",
    "Lyndon B. Johnson": "https://www.whitehouse.gov/wp-content/uploads/2021/01/36_lyndonbjohnson.jpg",
    "Richard Nixon": "https://www.whitehouse.gov/wp-content/uploads/2021/01/37_richardnixon.jpg",
    "Gerald Ford": "https://www.whitehouse.gov/wp-content/uploads/2021/01/38_geraldford.jpg",
    "Jimmy Carter": "https://www.whitehouse.gov/wp-content/uploads/2021/01/39_jimmycarter.jpg",
    "Ronald Reagan": "https://www.whitehouse.gov/wp-content/uploads/2021/01/40_ronaldreagan.jpg",
    "George H. W. Bush": "https://www.whitehouse.gov/wp-content/uploads/2021/01/41_georgehwbush.jpg",
    "Bill Clinton": "https://www.whitehouse.gov/wp-content/uploads/2021/01/42_billclinton.jpg",
    "George W. Bush": "https://www.whitehouse.gov/wp-content/uploads/2021/01/43_georgewbush.jpg",
    "Barack Obama": "https://www.whitehouse.gov/wp-content/uploads/2021/01/44_barackobama.jpg",
    "Donald J. Trump": "https://www.whitehouse.gov/wp-content/uploads/2021/01/45_donaldjtrump.jpg",
    "Joseph R. Biden": "https://www.whitehouse.gov/wp-content/uploads/2021/01/46_josephrjbiden.jpg"
}


# Step 2: Streamlit App Setup
st.title("Presidential Economic Performance Comparison")

st.write("""
    Select U.S. Presidents and metrics to compare their economic performance:
    - GDP
    - Growth
    - Inflation Rate
    - Debt
    - Increase
""")

# Step 3: President and Metric Selection
presidents = df['president'].unique()
selected_presidents = st.multiselect("Select Presidents to compare", options=presidents, default=[presidents[0]])
selected_metrics = st.multiselect("Select Metrics to compare", options=["gdp", "growth", "inflation_rate", "debt", "increase"], default=["gdp", "growth"])

# Step 4: Prepare Comparison Data
comparison_data = {"Metric": selected_metrics}

# Initialize an empty string to hold the HTML for president images
president_images_html = ""

for president in selected_presidents:
    pres_data = []
    df_pres = df[df['president'] == president]

    for metric in selected_metrics:
        pres_data.append(df_pres[metric].mean())

    comparison_data[president] = pres_data

    # Add the president's image and name to the HTML string
    image_url = president_images.get(president, "")
    if image_url:
        president_images_html += f"""
        <div style="display: inline-block; margin: 10px;">
            <img src="{image_url}" alt="{president}" style="width:100px; height:auto; border-radius:50%;">
            <p style="text-align:center;">{president}</p>
        </div>
        """

comparison_df = pd.DataFrame(comparison_data)

# Step 5: Display president images
st.markdown(president_images_html, unsafe_allow_html=True)

# Step 6: Display comparison graph
if not comparison_df.empty:
    st.header(f"Comparison of Selected Presidents")
    comparison_chart = alt.Chart(comparison_df).transform_fold(
        selected_presidents,
        as_=['President', 'Value']
    ).mark_bar().encode(
        x=alt.X('Metric:N', axis=alt.Axis(title='Metric')),
        y=alt.Y('Value:Q', axis=alt.Axis(title='Value')),
        color='President:N',
        column='Metric:N'
    ).properties(
        width=150,
        height=300
    )

    st.altair_chart(comparison_chart, use_container_width=True)

# Step 7: Show raw data if needed
st.subheader("Raw Data")
st.write("Data for comparison:", comparison_df)
