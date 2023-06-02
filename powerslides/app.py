from main import main
from components.sidebar import sidebar
import streamlit as st

if __name__ == '__main__':
    sidebar()
    st.markdown("<h1>🛝 PowerSlides</h1>", unsafe_allow_html=True)
    main()