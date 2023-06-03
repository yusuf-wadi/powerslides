import streamlit as st



def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

def sidebar():
    with st.sidebar:
        #st.markdown("<h1>🛝</h1>", unsafe_allow_html=True)
        st.markdown("# Welcome to 🛝PowerSlides")
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below 🔽\n"  
            "2. Write your topic &or reference text 📜\n"
            "3. Press generate 🔮\n"
        )
        st.markdown("## Tips:\n"
                    "📌 Use the PowerPoint Designer tab to really make the presentation pop\n")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  
            value=st.session_state.get("OPENAI_API_KEY", "")
        )
        
        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "- 🛝 **PowerSlides** is a tool that generates PowerPoint slides from text.\n"
            "- It lays the groundwork and all you have to do is add the finishing touches (like an art project).\n"
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/yusuf-wadi/powerslides) "  
            "with your feedback and suggestions🏋️"
        )
        st.markdown("Made by [yusuf-wadi](https://github.com/yusuf-wadi)")
        st.markdown("---")
        st.markdown("# Contact")
        st.markdown("📧" + "<a href='mailto:ymw200000@utdallas.edu'><b>Email   </b></a>", unsafe_allow_html=True)