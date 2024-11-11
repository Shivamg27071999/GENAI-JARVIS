import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set page title and icon
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon=":robot_face:", layout="wide")

# Sidebar with Logo and Instructions
st.sidebar.image("https://example.com/logo.png", use_container_width=True)  # Replace with your logo URL or local path
st.sidebar.title("Generative AI Interface")
st.sidebar.write("Welcome! Enter your query below and receive an AI-generated response.")

# Main interface
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>J.A.R.V.I.S. AI-Assistant</h1>", unsafe_allow_html=True)

# Instructions
with st.expander("How to Use", expanded=False):
    st.write("1. Enter a query in the text box below.\n"
             "2. Click on **Get Response**.\n"
             "3. Wait a moment for the AI to generate a response.\n")

# Set up retry logic for handling connection errors
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))

# User input area with additional formatting
user_input = st.text_input("Enter your query:", placeholder="e.g., Explain the concept which you want to learn", max_chars=100)

# Submit button with styled output
if st.button("Get Response"):
    if user_input:
        with st.spinner("Connecting to the AI model..."):
            try:
                # Send user input to the Flask API
                response = session.post("http://127.0.0.1:5000/query", json={"query": user_input})
                if response.status_code == 200:
                    answer = response.json().get("response", "No response from API")
                    # Display the response in a styled box with black text
                    st.markdown("<h3 style='color: #333;'>Response:</h3>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background-color: #f0f0f5; padding: 15px; border-radius: 10px; color: #000;'>
                            {answer}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: Could not connect to the backend. Make sure Flask is running on http://127.0.0.1:5000.")
                st.write("Details:", e)
    else:
        st.warning("Please enter a query to get a response.")

# Additional style and footer
st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by <strong>Shivam S Garg (Data Scientist) </strong></p>", 
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Thanks to Mentor <strong>Kanav Bansal</strong> | ❤️Innomatics Research Lab❤️</p>", 
            unsafe_allow_html=True)
