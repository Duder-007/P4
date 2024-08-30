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
    "Herbert Hoover": "https://www.whitehouse.gov/wp-content/uploads/2021/01/31_herberthoover.jpg",
    "Franklin D. Roosevelt": "https://www.whitehouse.gov/wp-content/uploads/2021/01/32_franklindroosevelt.jpg",
    # Add other presidents and their image URLs here
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
