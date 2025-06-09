import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Qur’anic Themes Explorer",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Qur’anic Themes Explorer")
st.markdown("Explore the Qur'an by **Main Category**, **Topic**, **Sub-Topic**, and view sample verses with translations.")

@st.cache_data
def load_data():
    df = pd.read_csv("quran_subjects.csv")
    df.columns = df.columns.str.strip()  # Clean whitespace in headers
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Main Category filter (single select)
main_categories = ["All"] + sorted(df['Main Category'].dropna().unique().tolist())
selected_main_cat = st.sidebar.selectbox("Select Main Category", main_categories)

# Filter dataframe by Main Category first
filtered_df = df.copy()
if selected_main_cat != "All":
    filtered_df = filtered_df[filtered_df['Main Category'] == selected_main_cat]

# Topic multi-select dropdown (tag style)
topics = sorted(filtered_df['Topic'].dropna().unique().tolist())
selected_topics = st.sidebar.multiselect("Select Topic(s)", topics)

if selected_topics:
    filtered_df = filtered_df[filtered_df['Topic'].isin(selected_topics)]


# Display result count
st.markdown(f"📚 **{len(filtered_df)} result(s)** found")

# Display each filtered record
for _, row in filtered_df.iterrows():
    st.markdown(f"### 🟢 {row['Topic']}")
    st.markdown(f"**Main Category:** {row['Main Category']}")
    # st.markdown(f"**Reference:** {row['Surah:Ayat']}")
    st.markdown(f"**Reference:** {row['SurahName:AyatNumber']}")
    st.markdown(f"**Arabic:** {row['Ayat in Arabic']}")
    st.markdown(f"**Bangla Translation:** {row['Bangla Translation']}")
    st.markdown("---")




# Footer
st.markdown("---")
st.markdown("📘 Built with ❤️ for knowledge seekers | © 2025 Saiful Islam")