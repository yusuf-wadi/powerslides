import streamlit as st
import os

def donate():
    
    st.markdown("If you find this app useful, please consider donating to keep it running 🙏")
    st.markdown("<form> <button formaction='https://www.buymeacoffee.com/yusufwadi0' style='color:purple;'><b><h2>Buy me a coffee ☕ :)</h2></b></button></form>", unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        #st.markdown("<h1>:racing_car:</h1>", unsafe_allow_html=True)
        # 060823 - credits currently refers to the number of slides the user has created
        st.markdown(f"# Welcome to :racing_car: PowerSlides, <span style='color: orange;'>{st.session_state['name'].split(' ')[0]}</span>", unsafe_allow_html=True)
        st.markdown(f"#### Slides Powered So Far: <span style='color: red;'>{st.session_state['credits']}</span>", unsafe_allow_html=True)
        #st.markdown("Power your slides with AI , get more credits below 👇")
        donate()
        st.markdown("---")    
        st.markdown(
            "# How to use\n"
            "1. Write your topic &or reference text 📜\n"   
            "2. Press generate 🔮\n"
            "3. Scroll down to download your PowerPoint presentation 💾\n"
        )
        st.markdown("---")  
        st.markdown("# Tips:\n"
                    "📌 Use the PowerPoint Designer tab to really make the presentation pop\n")
        # api_key_input = st.text_input(
        #     "OpenAI API Key",
        #     type="password",
        #     placeholder="Paste your OpenAI API key here (sk-...)",
        #     help="You can get your API key from https://platform.openai.com/account/api-keys.",  
        #     value=st.session_state.get("OPENAI_API_KEY", "")
        # )
        

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "- :racing_car: **PowerSlides** is a tool that generates PowerPoint slides from text.\n"
            "- It lays the groundwork for a set of slides on any topic, and all you have to do is add the finishing touches (like an art project).\n"
        )
        st.markdown(
            "This tool is a work in progress. "
            "Feel free to reach out to me through email\n"  
            "with your feedback and suggestions🏋️"
        )
        st.markdown("Made by [yusuf-wadi](https://github.com/yusuf-wadi)")
        st.markdown("---")  
        st.markdown("# Contact")
        st.markdown("📧" + "<a href='mailto:ymw200000@utdallas.edu'><b>Email   </b></a>", unsafe_allow_html=True)  
        st.markdown("---")
        logout = st.button("Logout")
        if logout:
            st.session_state.clear()      