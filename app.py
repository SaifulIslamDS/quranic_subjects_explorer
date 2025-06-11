import pandas as pd
import streamlit as st
# ---------------------------------
# Set page config
st.set_page_config(
    page_title="Qur’anic Subjects Explorer",
    page_icon="📖",
    layout="wide"
)
# ---------------------------------
# ✅ Custom CSS + Hamburger Button + Scroll-to-Top + JS
# ---------------------------------
st.markdown("""
<style>
  /* Completely hide Streamlit's top header, including spacing */
  header[data-testid="stHeader"] {
    display: none;
  }

  /* Hide default sidebar toggle */
  [data-testid="collapsedControl"] {
    display: none;
  }

  /* Hide Streamlit's default hamburger icon (extra safety) */
  .st-emotion-cache-1eyfjps {
    display: none;
  }

  /* Custom Hamburger Button */
  .custom-hamburger {
    position: fixed;
    top: 12px;
    right: 16px;
    z-index: 9999;
    background-color: #1a73e8;
    color: white;
    border: none;
    font-size: 28px;
    border-radius: 8px;
    padding: 10px 14px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  /* Responsive tweak */
  @media (max-width: 768px) {
    .custom-hamburger {
      font-size: 32px;
      padding: 12px 16px;
    }
  }
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 📦 Load Data
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSteXbAdUyJFek-Uysk9Jlb4iwF6G51Yt3ThxOHQVmacBjZicJ7NDPKoMCR0uJoGJdPoe8jHvLYqwyC/pub?gid=843924243&single=true&output=csv")

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
col1, col2 = st.columns([10, 1])
with col1:
    st.title("📖 Qur’anic Subjects Explorer")
with col2:
    if st.button("☰", key="hamburger"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

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
st.markdown(f"###### Showing {len(filtered_df)} Ayah(s)\n")

for i, row in filtered_df.iterrows():
    st.markdown(f"""
        <div style="border: 1px solid #ccc; border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);">
            <h4 style="color:#008000; margin-bottom: 8px;">📌 {row['Topic']}</h4>
            <span style="color: #555;"><strong>📘 Surah Name & Number:</strong> {row['SurahName:AyatNumber']}</span>
            <p style="font-size: 20px; color: #000; text-align: right; direction: rtl;"><strong>{row['Ayat in Arabic']}</strong></p>
            <p><em>Bangla:</em> {row['Bangla Translation']}</p>
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
