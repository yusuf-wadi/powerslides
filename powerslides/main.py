import langchain.chains as chains
from langchain.llms import OpenAIChat
import streamlit as st
import pandoc 
import os
import subprocess
import sys
import openai.error

# set OPENAI_API_KEY in your environment variables


def generate(prompt):
    chat = OpenAIChat(model_name='gpt-3.5-turbo', client=None, openai_api_key=st.session_state.get("OPENAI_API_KEY"))
    try:
        response = chat.generate(prompt)
        return response.generations[0][0].text
    except openai.error.AuthenticationError:
        st.error("⚠️ Please set the correct key in the sidebar -> see help icon")
        return ""

def main(): 
    content = st.text_input("Enter content to generate a lesson from:")
    button = st.button("Generate Lesson")
    # only generate when user presses submit
    if button and content:
        prompt = [f"create a teachable lesson from this content:{content}\
            \n\n ensure the format is in this fashion, use markdown convention:\n\
                # [SLIDE TITLE]\n\
                [slide content]\n\
                ---\
                # [SLIDE TITLE]\n\
                etc..."]
        
        slides = generate(prompt)
        st.write(slides)
        # no spaces in file names
        if "#" in slides:
            slide_title = slides.split("#")[1].split("\n")[0].replace(" ", "_")
            print(slide_title)
            
            text_folder = "text/"
            slides_folder = "slides/"
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
