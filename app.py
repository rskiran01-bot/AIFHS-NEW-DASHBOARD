import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Single-Use Plastics Dashboard",
    layout="wide"
)

st.title("🌍 Elimination of Single-Use Plastics (SUP)")
st.subheader("Global | India | Telangana – Best Practices & Interventions")

# Upload data
uploaded_file = st.file_uploader(
    "Upload SUP Best Practices Data (Excel or CSV)",
    type=["xlsx", "csv"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data loaded successfully!")

    # Sidebar filters
    st.sidebar.header("🔎 Filters")
    level = st.sidebar.multiselect(
        "Select Level",
        options=df["Level"].unique(),
        default=df["Level"].unique()
    )

    practice = st.sidebar.multiselect(
        "Select Practice Type",
        options=df["Practice_Type"].unique(),
        default=df["Practice_Type"].unique()
    )

    filtered_df = df[
        (df["Level"].isin(level)) &
        (df["Practice_Type"].isin(practice))
    ]

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Practices", len(filtered_df))
    col2.metric("Countries / States", filtered_df["Country/State"].nunique())
    col3.metric("Practice Types", filtered_df["Practice_Type"].nunique())

    st.divider()

    # Bar chart – Practices by Level
    fig1 = px.bar(
        filtered_df,
        x="Level",
        color="Practice_Type",
        title="Practices by Governance Level",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bar chart – Practices by Region/State
    fig2 = px.bar(
        filtered_df,
        x="Country/State",
        color="Practice_Type",
        title="Practices by Country / State",
        text_auto=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Table view
    st.subheader("📋 Detailed Best Practices")
    st.dataframe(filtered_df, use_container_width=True)

    # Telangana Focus Section
    st.divider()
    st.subheader("📍 Telangana – Actionable Insights")

    telangana_df = filtered_df[
        filtered_df["Country/State"].str.contains("Telangana", case=False, na=False)
    ]

    if not telangana_df.empty:
        st.dataframe(telangana_df, use_container_width=True)
    else:
        st.info("No Telangana-specific records in current filter.")

else:
    st.info("👈 Upload a SUP best practices dataset to begin.")
