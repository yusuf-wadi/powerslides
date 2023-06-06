import streamlit as st
import os

def more_credits():
    
    st.markdown("Pending")#"[Power your 🛝](https://buy.stripe.com/test_14k6pHgmm26z1Bm3cc)")

def sidebar():
    with st.sidebar:
        #st.markdown("<h1>🛝</h1>", unsafe_allow_html=True)

        st.markdown(f"# Welcome to 🛝PowerSlides, <span style='color: orange;'>{st.session_state['name'].split(' ')[0]}</span>", unsafe_allow_html=True)
        st.markdown(f"Remaining slides: {st.session_state['credits']}")
        st.markdown("Power your slides with AI 🧠, get more credits below 🔽")
        more_credits()    
        st.markdown(
            "## How to use\n"
            "1. Write your topic &or reference text 📜\n"   
            "2. Press generate 🔮\n"
            "3. Scroll down to download your PowerPoint presentation 💾\n"
        )
        st.markdown("## Tips:\n"
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
            "- 🛝 **PowerSlides** is a tool that generates PowerPoint slides from text.\n"
            "- It lays the groundwork for a set of slides on any topic, and all you have to do is add the finishing touches (like an art project).\n"
        )
        st.markdown(
            "This tool is a work in progress. "
            "Feel free to reach out to me through email\n"  
            "with your feedback and suggestions🏋️"
        )
        st.markdown("Made by [yusuf-wadi](https://github.com/yusuf-wadi)")
        st.markdown("# Contact")
        st.markdown("📧" + "<a href='mailto:ymw200000@utdallas.edu'><b>Email   </b></a>", unsafe_allow_html=True)  
        st.markdown("---")
        logout = st.button("Logout")
        if logout:
            st.session_state.clear()      