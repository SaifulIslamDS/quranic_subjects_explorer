import streamlit as st
import pandas as pd

# ---------------------------------
# 📦 Load Data
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSteXbAdUyJFek-Uysk9Jlb4iwF6G51Yt3ThxOHQVmacBjZicJ7NDPKoMCR0uJoGJdPoe8jHvLYqwyC/pub?gid=843924243&single=true&output=csv")  # ✅ Your dataset

df = load_data()

# ---------------------------------
# 🧠 Initialize session_state safely
# ---------------------------------
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

# ---------------------------------
# 🔄 Reset Filters Callback
# ---------------------------------
def reset_filters():
    st.session_state.main_category_selectbox = "All"
    st.session_state.selected_topics_multiselect = []

# ---------------------------------
# 🧱 Layout: Header + Hamburger
# ---------------------------------
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">📖 Qur’anic Subjects Explorer</h1>
    </div>
    """,
    unsafe_allow_html=True
)
# ---------------------------------
# 🎛️ Sidebar Filters
# ---------------------------------
if st.session_state.show_sidebar:
    with st.sidebar:
        st.header("🔍 Filter Options")

        main_categories = ["All"] + sorted(df["Main Category"].dropna().unique())
        selected_main_category = st.selectbox(
            "Select Main Category",
            options=main_categories,
            key="main_category_selectbox"
        )

        if selected_main_category == "All":
            filtered_topics_df = df
        else:
            filtered_topics_df = df[df["Main Category"] == selected_main_category]

        topics = sorted(filtered_topics_df["Topic"].dropna().unique())
        selected_topics = st.multiselect(
            "Select Topic(s)",
            options=topics,
            key="selected_topics_multiselect"
        )

        st.button("🔄 Reset Filters", on_click=reset_filters)
else:
    st.sidebar.empty()

# ---------------------------------
# 📊 Filter the Data
# ---------------------------------
filtered_df = df.copy()

main_cat_val = st.session_state.get("main_category_selectbox", "All")
if main_cat_val != "All":
    filtered_df = filtered_df[filtered_df["Main Category"] == main_cat_val]

selected_topics_vals = st.session_state.get("selected_topics_multiselect", [])
if selected_topics_vals:
    filtered_df = filtered_df[filtered_df["Topic"].isin(selected_topics_vals)]

# ---------------------------------
# 🧾 Render in Article-Style View
# ---------------------------------
st.markdown(f"### Showing {len(filtered_df)} Ayah(s)\n")

for i, row in filtered_df.iterrows():
    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);">
        <h4 style="color:#1a73e8; margin-bottom: 8px;">📌 Topic: {row['Topic']}</h4>
        <span style="color: #555;><strong>📖 Ayah:</strong> {row['Surah:Ayat']}</span>
        <span style="color: #555;><strong>📖 Ayah:</strong> {row['SurahName:AyatNumber']}</span>
        <p style="font-size: 20px; color: #000; text-align: right; direction: rtl;"><strong>{row['Ayat in Arabic']}</strong></p>
        <p><em>🇧🇩 Bangla:</em> {row['Bangla Translation']}</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# 🦶 Footer
# ---------------------------------
st.markdown(
    """
    <hr style="margin-top: 60px;">
    <div style="text-align: center; font-size: 14px;">
        Developed with ❤️ by <a href="https://saifulshuvo.com" target="_blank" style="text-decoration: none;">Saiful Islam</a>
    </div>
    """,
    unsafe_allow_html=True
)
