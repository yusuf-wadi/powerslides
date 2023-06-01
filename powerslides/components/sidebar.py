import streamlit as st

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) belowðŸ”‘\n"  
            "2. Write your topic and/or reference text ðŸ“„\n"
            "3. Press generate ðŸ”®\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "ðŸ› **PowerSlides** is a tool that generates PowerPoint slides from text. "
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/yusuf-wadi/powerslides) "  
            "with your feedback and suggestionsðŸ’¡"
        )
        st.markdown("Made by [yusuf-wadi](https://github.com/yusuf-wadi)")
        st.markdown("---")