#import langchain.chains as chains
from langchain.llms import OpenAIChat
import streamlit as st
import os
import subprocess
from openai.error import AuthenticationError
from pydantic.error_wrappers import ValidationError
import tempfile
from decouple import config as cfg
import deta
from decouple import config as cfg
# set OPENAI_API_KEY in env

db = deta.Deta(cfg('DETA_KEY')).Base('users')
st.session_state["OPENAI_API_KEY"] = cfg("OPENAI_API_KEY")

def generate(prompt):
    try:
        chat = OpenAIChat(model_name='gpt-3.5-turbo', client=None, openai_api_key=st.session_state.get("OPENAI_API_KEY"))
        response = chat.generate(prompt)
        return response.generations[0][0].text
    except AuthenticationError:
        st.error("⚠️ Please set the correct key in the sidebar -> see help icon")
        return ""
    except ValidationError:
        st.error("⚠️ Please set the correct key in the sidebar -> see help icon")
        return ""

def main(): 
    content = st.text_area("Enter content or topic to generate a presentation:")
    button = st.button("Generate Lesson") 
    # only generate when user presses submit
    if button and content and st.session_state['credits'] > 0:
        prompt = [f"create a teachable lesson from this content:{content}\
            \n\n IMPORTANT-> ensure the format is in this fashion, use markdown convention:\n\n\
                # [SLIDE1 TITLE]\n\
                [slide1 content]\n\
                ---\
                # [SLIDE2 TITLE]\n\
                [slide2 content]\n\
                ---\n\
                etc..."]
        with st.spinner("Generating slides...\n Once done, you can download the slides below"):
            slides = generate(prompt)
        
        st.write(slides)
        db.update({"credits": st.session_state['credits'] - 1}, key=st.session_state['username'])
        st.session_state['credits'] = db.get(key=st.session_state['username'])['credits']
        # no spaces or colon in file names
        if "#" in slides:
            slide_title = slides.split("#")[1].split("\n")[0].replace(" ", "").replace(":", "")  
            text_folder_dir = tempfile.TemporaryDirectory()#"/text/"
            slides_folder_dir = tempfile.TemporaryDirectory()#"/slides/"
            text_folder = text_folder_dir.name
            slides_folder = slides_folder_dir.name
            
            md_file = f"{slide_title}_lesson.md"
            pptx_file = f"{slide_title}_lesson.pptx"
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            with open(text_folder + md_file, "w", encoding="utf-8") as f:
                f.write(slides)
            if not os.path.exists(slides_folder):   
                os.makedirs(slides_folder)
                
            # convert to pptx using pandoc
            subprocess.call(["pandoc", text_folder + md_file, "-o", slides_folder + pptx_file])
            st.markdown("---")
            st.success("🎉 Done!")
            with open(slides_folder + pptx_file, "rb") as f:
                file_data = f.read()
                st.download_button("Download Lesson", file_data, file_name=pptx_file)
            
