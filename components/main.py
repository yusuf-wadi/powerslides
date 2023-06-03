import langchain.chains as chains
from langchain.llms import OpenAIChat
import streamlit as st
import pandoc 
import os
import subprocess
import sys
from openai.error import AuthenticationError
from pydantic.error_wrappers import ValidationError
import tempfile
# set OPENAI_API_KEY in your environment variables

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
    content = st.text_input("Enter content to generate a lesson from:")
    button = st.button("Generate Lesson")
    # only generate when user presses submit
    if button and content:
        prompt = [f"create a teachable lesson from this content:{content}\
            \n\n ensure the format is in this fashion, use markdown convention:\n\
                # [SLIDE1 TITLE]\n\
                [slide1 content]\n\
                ---\
                # [SLIDE2 TITLE]\n\
                etc..."]
        
        slides = generate(prompt)
        st.write(slides)
        # no spaces or colon in file names
        if "#" in slides:
            slide_title = slides.split("#")[1].split("\n")[0].replace(" ", "").replace(":", "")
            print(slide_title)
            
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
            st.write("Done! Check the slides folder for your lesson")
            with open(slides_folder + pptx_file, "rb") as f:
                file_data = f.read()
            st.download_button("Download Lesson", file_data, file_name=pptx_file)
