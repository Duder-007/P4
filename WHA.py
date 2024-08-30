import streamlit as st
import pandas as pd
import altair as alt

# Step 1: Load the data and clean it
@st.cache_data
def load_data():
    df = pd.read_csv("gdp_year_with_more.csv")  # Adjust the path as needed

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Replace NaN values with 0
    df = df.fillna(0)

    # Remove commas and dollar signs, then convert to numeric
    df['gdp'] = df['gdp'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['growth'] = df['growth'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['inflation_rate'] = df['inflation_rate'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['debt'] = df['debt'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['increase'] = df['increase'].replace({'\$': '', ',': ''}, regex=True).astype(float)

    return df

df = load_data()

# Step 2: Streamlit App Setup
st.title("Presidential Economic Performance Comparison")
st.write("""
    Select multiple U.S. Presidents to compare their economic performance based on:
    - GDP Growth
    - Growth
    - Inflation Rate
    - Debt
    - Increase
""")

# Step 3: President and Metric Selection
presidents = df['president'].unique()
selected_presidents = st.multiselect("Select Presidents to compare", options=presidents, default=[presidents[0], presidents[1]])
selected_metrics = ["gdp", "growth", "inflation_rate", "debt", "increase"]

# Step 4: Prepare Comparison Data
comparison_data = {"Metric": selected_metrics}

for president in selected_presidents:
    pres_data = []
    df_pres = df[df['president'] == president]

    for metric in selected_metrics:
        if metric in df_pres.columns:
            pres_data.append(df_pres[metric].mean())
        else:
            st.error(f"Column '{metric}' not found for President '{president}'.")
            pres_data.append(None)
    comparison_data[president] = pres_data

comparison_df = pd.DataFrame(comparison_data)

# Step 5: Display comparison graph
if not comparison_df.empty:
    st.header(f"Comparison between Selected Presidents")
    comparison_chart = alt.Chart(comparison_df).transform_fold(
        selected_presidents,
        as_=['President', 'Value']
    ).mark_bar().encode(
        x=alt.X('Metric:N', axis=alt.Axis(title='Metric')),
        y=alt.Y('Value:Q', axis=alt.Axis(title='Value')),
        color='President:N',
        column='Metric:N'
    ).properties(
        width=200,
        height=400
    )

    st.altair_chart(comparison_chart, use_container_width=True)

# Step 6: Show raw data if needed
st.subheader("Raw Data")
st.write("Data for comparison:", comparison_df)
