import streamlit as st
st.set_page_config(page_icon="🛝", page_title='PowerSlides')
from components.main import main
from components.sidebar import sidebar
from components.app_auth import login
from components.landing import landing
import subprocess

# session state
if "authentication_status" not in st.session_state:
    st.session_state['authentication_status'] = None
if "name" not in st.session_state:
    st.session_state['name'] = None
if "username" not in st.session_state:
    st.session_state['username'] = None
if "credits" not in st.session_state:
    st.session_state['credits'] = None

# start backend for stripe
subprocess.Popen(["ruby" ,"server.rb"])

if __name__ == '__main__':
    
    st.title("🛝 PowerSlides")
    #st.markdown("<h5>Generate PowerPoint Slides from Text</h5>", unsafe_allow_html=True)
    
    if not st.session_state['authentication_status']:
        landing()
        login()
    else:
        main()
        sidebar()
        