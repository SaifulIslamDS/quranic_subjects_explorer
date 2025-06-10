import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Qur’anic Subjects Explorer",
    page_icon="📖",
    layout="wide"
)

# Custom CSS and responsive layout
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Noto Sans Bengali', sans-serif;
        background-color: #f5f7fa;
        color: #222;
    }

    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #003366;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
    }

    .stApp {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    @media (max-width: 768px) {
        .stApp {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hamburger {
            display: block !important;
        }
    }

    .ayat-box {
        background-color: #ffc6fcff;
        border-left: 6px solid #2c3e50;
        border-radius: 12px;
        padding: 15px 20px;
        margin: 15px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }

    .arabic {
        direction: rtl;
        text-align: right;
        font-size: 22px;
        font-family: 'Amiri', serif;
        color: #1c2331;
        margin-bottom: 10px;
    }

    .translation {
        font-size: 16px;
        line-height: 1.6;
    }

    .bangla {
        font-family: 'Noto Sans Bengali', sans-serif;
        color: #444;
    }

    .english {
        font-style: italic;
        color: #555;
    }

    .hamburger {
        display: none;
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 26px;
        cursor: pointer;
        color: #003366;
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Amiri&family=Noto+Sans+Bengali&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("quran_subjects.csv")
    df.columns = df.columns.str.strip()  # Clean whitespace
    return df

df = load_data()

# Reset callback function
def reset_filters():
    st.session_state.main_category = "All"
    st.session_state.selected_topics = []

# Sidebar
st.sidebar.header("🔍 Filter Options")

# Create widgets first so Streamlit registers their keys
main_categories = ["All"] + sorted(df['Main Category'].dropna().unique().tolist())
selected_main_cat = st.sidebar.selectbox("Select Main Category", main_categories, key="main_category")

# Filter based on current main category selection
filtered_df = df.copy()
if selected_main_cat != "All":
    filtered_df = filtered_df[filtered_df['Main Category'] == selected_main_cat]

topics = sorted(filtered_df['Topic'].dropna().unique().tolist())
selected_topics = st.sidebar.multiselect("Select Topic(s)", topics, key="selected_topics")

# 🔄 Reset Button now uses a callback safely
st.sidebar.button("🔄 Reset Filters", on_click=reset_filters)

# Apply topic filtering
if selected_topics:
    filtered_df = filtered_df[filtered_df['Topic'].isin(selected_topics)]

# Title and hamburger
st.markdown('<div class="hamburger">☰</div>', unsafe_allow_html=True)
st.title("📖 Qur’anic Subjects Explorer")
st.markdown("Explore the Qur'an by **Main Category**, **Topic**, **Sub-Topic**, and view sample verses with translations.")

# Result count
st.markdown(f"📚 **{len(filtered_df)} result(s)** found")

# Display results
for _, row in filtered_df.iterrows():
    st.markdown(f"### ➡️ {row['Topic']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Main Category:**  \n{row['Main Category']}")
    with col2:
        st.markdown(f"**Surah:Ayat**  \n{row['Surah:Ayat']}")
    with col3:
        st.markdown(f"**Surah Name:Ayat**  \n{row['SurahName:AyatNumber']}")

    st.markdown(f"""
    <div class="ayat-box">
        <div class="arabic">{row['Ayat in Arabic']}</div>
        <div class="translation bangla"><strong>বাংলা অনুবাদ:</strong><br>{row['Bangla Translation']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

# Footer
st.markdown("---")
st.markdown("📘 Built with ❤️ for knowledge seekers | © 2025 [Saiful Islam](https://saifulshuvo.com)")
