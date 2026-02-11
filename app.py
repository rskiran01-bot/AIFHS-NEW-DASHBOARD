import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="NFHS India Dashboard",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")
st.caption("India & State-level Analysis | Evidence-based Governance")

# Load data
@st.cache_data
def load_data():
    file_path = "/mnt/data/All India National Family Health Survey1.xlsx"
    df = pd.read_excel(file_path)
    return df

df = load_data()

st.success("NFHS data loaded successfully")

# Show raw data (optional)
with st.expander("🔍 View Raw Data"):
    st.dataframe(df, use_container_width=True)

# Identify columns dynamically
columns = df.columns.tolist()

# Sidebar filters
st.sidebar.header("🔎 Filters")

state_col = st.sidebar.selectbox(
    "Select State Column",
    options=columns
)

indicator_col = st.sidebar.selectbox(
    "Select Indicator Column",
    options=columns
)

value_col = st.sidebar.selectbox(
    "Select Value Column",
    options=columns
)

# Optional state filter
states = df[state_col].dropna().unique().tolist()
selected_states = st.sidebar.multiselect(
    "Select States",
    options=states,
    default=states[:5]
)

filtered_df = df[df[state_col].isin(selected_states)]

# KPIs
st.subheader("📌 Key Indicators Snapshot")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total States Selected",
    len(selected_states)
)

col2.metric(
    "Indicators Covered",
    filtered_df[indicator_col].nunique()
)

col3.metric(
    "Total Records",
    len(filtered_df)
)

st.divider()

# Indicator selection
selected_indicator = st.selectbox(
    "Select Indicator for Comparison",
    options=filtered_df[indicator_col].unique()
)

indicator_df = filtered_df[
    filtered_df[indicator_col] == selected_indicator
]

# Bar chart
fig = px.bar(
    indicator_df,
    x=state_col,
    y=value_col,
    title=f"State-wise Comparison: {selected_indicator}",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# Telangana focus
st.divider()
st.subheader("📍 Telangana Focus")

telangana_df = df[df[state_col].str.contains("Telangana", case=False, na=False)]

if not telangana_df.empty:
    st.dataframe(telangana_df, use_container_width=True)
else:
    st.info("Telangana data not found in selected column.")

# Download filtered data
st.divider()
st.download_button(
    label="⬇️ Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="nfhs_filtered_data.csv",
    mime="text/csv"
)
