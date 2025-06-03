import streamlit as st
import pandas as pd
import re
from duckduckgo_search import DDGS  # ✅ Correct for version 8.0.2

# ✅ Page config
st.set_page_config(page_title="Developed by ZIYA", layout="wide")

# ✅ Load and cache data
@st.cache_data
def load_data():
    # Ensure this path is accessible or adjust for deployment
    try:
        # Removed the absolute path to make it more portable.
        # Ensure 'file_cleaned.csv' is in the same directory as this script.
        df = pd.read_csv(r"C:\ziya_workspace\ziya_data_science\Projects\file_cleaned.csv")
    except FileNotFoundError:
        st.error("Error: 'file_cleaned.csv' not found. Please ensure the CSV file is in the same directory as the script.")
        st.stop() # Stop the app if data cannot be loaded
    return df

df = load_data()

# ✅ Extract filters from query
def extract_filters(query):
    filters = {}
    price_match = re.search(r'under\s?\u20b9?(\d+)', query, re.IGNORECASE)
    if price_match:
        filters['price_max'] = int(price_match.group(1))

    ram_match = re.search(r'(\d+)\s?gb\s?ram', query, re.IGNORECASE)
    if ram_match:
        filters['ram_min'] = int(ram_match.group(1))

    return filters

# ✅ Filter dataframe
def filter_data(df, filters):
    if 'price_max' in filters:
        df = df[df['launched_price_rs'] <= filters['price_max']]
    if 'ram_min' in filters:
        df = df[df['ram_gb'] >= filters['ram_min']]
    return df

# ✅ Image search using DDGS
@st.cache_data
def fetch_image_url(name):
    try:
        with DDGS() as ddgs:
            results = ddgs.images(name, max_results=1)
            if results:
                return results[0]['image']
    except Exception as e:
        st.warning(f"Could not fetch image for {name}. Error: {e}")
    return "https://placehold.co/200x200/000000/FFFFFF?text=No+Image" # Placeholder with text

# ✅ Custom CSS for better search bar & wider layout
st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu, footer, header {visibility: hidden;}

    /* Main container padding and max width */
    .block-container {
        padding-top: 2rem; /* Reduced top padding */
        max-width: 1400px;
        margin: auto;
    }

    /* Styling for the search input and form */
    div[data-testid="stForm"] {
        display: flex;
        flex-direction: column; /* Stack input and button vertically */
        align-items: center; /* Center items horizontally within the form */
        justify-content: center; /* Center content vertically if form has a height */
        margin-top: 30px;
        margin-bottom: 100px;
    }

    div[data-testid="stForm"] > div > div[data-testid="stTextInput"] {
        width: 100%;
        max-width: 1000px; /* Increased max-width for a much longer search bar */
        margin-bottom: 15px; /* Space between input and button */
    }

    div[data-testid="stForm"] input {
        width: 100% !important;
        height: 80px !important; /* Increased height for a taller search bar */
        font-size: 28px !important; /* Adjusted font size for better fit with increased height */
        color: #00ffff !important;
        background-color: #000000 !important;
        border: 2px solid sky blue !important;
        border-radius: 10px !important;
        padding: 10px 200px !important;
        box-sizing: border-box;
        font-weight: 600;
    }

  

    /* Styling for the search button */
    div[data-testid="stForm"] button {
        background-color: #00ffff !important; /* Cyan button */
        color: #000000 !important; /* Black text */
        font-weight: bold !important;
        padding: 12px 30px !important;
        border-radius: 50px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 18px !important;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 255, 255, 0.3);
        width: auto !important; /* Allow button to size naturally */
        min-width: 180px; /* Increased minimum width for the button */
    }

    div[data-testid="stForm"] button:hover {
        background-color: #00dddd !important; /* Darker cyan on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 255, 255, 0.4);
    }

    /* Styling for the clear search button */
    .stButton > button.clear-search-button {
        background-color: #ff4444 !important; /* Red button */
        color: #ffffff !important; /* White text */
        font-weight: bold !important;
        padding: 10px 25px !important;
        border-radius: 8px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 16px !important;
        transition: all 0.2s ease-in-out;
        margin-top: 20px; /* Space above the button */
        box-shadow: 0 4px 6px rgba(255, 68, 68, 0.3);
    }

    .stButton > button.clear-search-button:hover {
        background-color: #dd3333 !important; /* Darker red on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(255, 68, 68, 0.4);
    }


    /* Result card styling */
    .result-card {
        background-color: #1e1e1e;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out;
        display: flex; /* Use flexbox for internal layout */
        flex-direction: column; /* Stack image and details vertically */
        align-items: center; /* Center content horizontally */
        text-align: center; /* Center text */
    }
    .result-card:hover {
        transform: translateY(-5px);
    }
    .result-card h4 {
        color: cyan;
        margin-bottom: 8px;
        font-size: 1.25rem;
    }
    .result-card span {
        display: block;
        margin: 5px 0;
        font-size: 0.95rem;
    }
    .stImage > img {
        border-radius: 8px;
        object-fit: contain; /* Ensure images fit well */
        max-height: 200px; /* Max height for images */
        width: 100%; /* Make image responsive within its column */
        margin-bottom: 10px; /* Space between image and text */
    }

    /* Responsive adjustments for smaller screens */
    @media (max-width: 768px) {
        div[data-testid="stForm"] {
            flex-direction: column; /* Stack input and button */
        }
        div[data-testid="stForm"] > div > div[data-testid="stTextInput"] {
            margin-bottom: 10px; /* Less space on small screens */
        }
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .result-card {
            margin: 8px 0;
            padding: 10px;
        }
        .result-card h4 {
            font-size: 1.1rem;
        }
        .result-card span {
            font-size: 0.9rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Session state initialization
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = pd.DataFrame()
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

st.title("📱 Your Phone Advisor powered by GenAi and NLP")

# ✅ Conditionally display the search form
if not st.session_state.show_results:
    with st.form(key='search_form', clear_on_submit=False):
        user_input = st.text_input(
            "🔍",
            value=st.session_state.query, # Keep previous query in the input field
            placeholder="Type your query like 'phone under ₹14000 with 16GB RAM'",
            label_visibility="collapsed",
            key="query_input_form"
        )
        submit_button = st.form_submit_button(label='Search 🚀')

    # Handle search submission when the form is visible
    if submit_button:
        st.session_state.query = user_input
        if user_input:
            filters = extract_filters(user_input)
            st.session_state.filtered_df = filter_data(df, filters)
            st.session_state.show_results = True
        else:
            st.session_state.filtered_df = pd.DataFrame() # Clear results if query is empty
            st.session_state.show_results = False
        st.rerun() # Rerun to update the display

# ✅ Display results if available
if st.session_state.show_results:
    # Display the query result prominently at the top
    st.markdown(f"### Results for your query: **{st.session_state.query}**")

    if not st.session_state.filtered_df.empty:
        st.success(f"✅ Found {len(st.session_state.filtered_df)} phone(s) matching your query!")

        # Use st.container for better visual grouping of results
        st.markdown("---") # Separator
        st.subheader("Recommended Smartphones:")

        # 4 columns for wider layout, now inside a dedicated container
        # This ensures the layout for results is distinct from the search bar
        cols = st.columns(4)
        for idx, (_, row) in enumerate(st.session_state.filtered_df.iterrows()):
            col = cols[idx % 4]
            with col:
                # Use a custom container for each phone for better styling
                with st.container(border=True): # Streamlit's built-in container with border
                    phone_name = f"{row['brand']} {row['model']}"
                    img_url = row.get('image_url')
                    if pd.isna(img_url):
                        img_url = fetch_image_url(phone_name)

                    st.image(img_url, width=200, caption=phone_name)

                    st.markdown(f"""
                        <div class='result-card-details'>
                            <h4>{phone_name}</h4>
                            <span>⚙️ <strong>Processor:</strong> {row.get('Processor', 'N/A')}</span>
                            <span>📅 <strong>Year:</strong> {row.get('launched_year', 'N/A')}</span>
                            <span>📱 <strong>RAM:</strong> {row.get('ram_gb', 'N/A')} GB</span>
                            <span>🔋 <strong>Battery:</strong> {row.get('battery_capacity_mah', 'N/A')} mAh</span>
                            <span>📷 <strong>Camera:</strong> {row.get('back_camera_mp', 'N/A')} MP</span>
                            <span>💰 <strong>Price:</strong> ₹{row.get('launched_price_rs', 'N/A')}</span>
                            <span>💾 <strong>Storage:</strong> {row.get('storage_gb', 'N/A')} GB</span>
                            <span>📐 <strong>Screen:</strong> {row.get('screen_size_inches', 'N/A')} inches</span>
                        </div>
                    """, unsafe_allow_html=True)

        with st.expander("🔍 View all results in table"):
            st.dataframe(st.session_state.filtered_df.reset_index(drop=True))
    else:
        st.warning("⚠️ No phones found matching your query.")

    # Add a "Clear Search" button below the results
    clear_col1, clear_col2, clear_col3 = st.columns([1, 1, 1])
    with clear_col2:
        if st.button("Clear Search", key="clear_search_button", help="Click to clear the current search and start a new one", type="secondary"):
            st.session_state.query = ""
            st.session_state.filtered_df = pd.DataFrame()
            st.session_state.show_results = False
            st.rerun()
