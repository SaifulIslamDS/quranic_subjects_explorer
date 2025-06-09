import streamlit as st
import pandas as pd

# App config
st.set_page_config(
    page_title="📖 Qur’anic Subjects Explorer",
    layout="wide",
    page_icon="🕌"
)

st.title("📖 Qur’anic Subjects Explorer")
st.markdown("Explore the Qur'an by **Subject**, with Arabic text and Bangla translation. More subjects coming as the database grows inshaAllah.")

# Load and clean the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("quran_subjects.csv")
    df.columns = df.columns.str.strip()  # Strip whitespace from headers
    df.dropna(subset=["Main Category", "Topic", "Surah:Ayat"], inplace=True)  # Ensure essential fields exist
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Main Category dropdown
main_cats = ["All"] + sorted(df['Main Category'].dropna().unique())
selected_main_cat = st.sidebar.selectbox("Select Main Category", main_cats)

# Apply Main Category filter
filtered_df = df.copy()
if selected_main_cat != "All":
    filtered_df = filtered_df[filtered_df["Main Category"] == selected_main_cat]

# Topic tag-style filter (multi-select)
topics = sorted(filtered_df['Topic'].dropna().unique())
selected_topics = st.sidebar.multiselect("Select Topic(s)", topics)

if selected_topics:
    filtered_df = filtered_df[filtered_df['Topic'].isin(selected_topics)]

# Show number of matched entries
st.markdown(f"📚 **{len(filtered_df)} result(s)** found")

# Display results
for _, row in filtered_df.iterrows():
    st.markdown(f"### 🟢 {row['Topic']}")
    st.markdown(f"**Main Category:** {row['Main Category']}")
    st.markdown(f"**Reference (Surah:Ayat):** `{row['Surah:Ayat']}`")
    # st.markdown(f"**Arabic:**\n\n📜 {row['Ayat in Arabic']}")
    st.markdown(
    f"""
    <div dir="rtl" style="text-align: right; font-size: 20px; font-family: 'Amiri', serif;">
        {row['Ayat in Arabic']}
    </div>
    """,
    unsafe_allow_html=True
    )

    # st.markdown(f"**Bangla Translation**:** `{row['Bangla Translation']}`", unsafe_allow_html=True)
    st.write("**Bangla Translation:**", row['Bangla Translation'], unsafe_allow_html=True)
    st.markdown("---")

# Footer
st.markdown("---")
st.markdown("📘 Built with ❤️ for knowledge seekers | © 2025 Saiful Islam")