import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="📖 Qur’anic Themes Explorer",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Qur’anic Themes Explorer")
st.markdown("Explore the Qur'an by **themes**, **topics**, and **categories** with sample verses and notes.")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("themes_quran.csv")
    df.columns = df.columns.str.strip()  # Remove trailing whitespaces from column names
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Category filter (Single select)
categories = ["All"] + sorted(df['Category'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select a Category", categories)

# Theme filter (Multi-tag dropdown)
all_themes = sorted(df['Theme'].dropna().unique().tolist())
selected_themes = st.sidebar.multiselect("Select Theme(s)", all_themes)

# Filter logic
filtered_df = df.copy()

# Filter by Category
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# Filter by selected Themes (tag-style multi-select)
if selected_themes:
    filtered_df = filtered_df[filtered_df['Theme'].isin(selected_themes)]

# Result count
st.markdown(f"📚 **{len(filtered_df)} result(s)** found")

# Display results
for idx, row in filtered_df.iterrows():
    st.markdown(f"### 🟢 {row['Theme']}")
    st.markdown(f"**Category**: `{row['Category']}`")
    st.markdown(f"**Arabic Term**: `{row['Arabic Term']}`")
    st.markdown(f"**Sample Verses**: {row['Sample Verses']}")
    
    # if pd.notna(row['Notes]()


# Footer
st.markdown("---")
st.markdown("📘 Built with ❤️ for knowledge seekers | © 2025 Saiful Islam")