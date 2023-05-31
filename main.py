import langchain.chains as chains
from langchain.llms import OpenAIChat
import streamlit as st
import pandoc 
import os
import subprocess

# set OPENAI_API_KEY in your environment variables
chat = OpenAIChat(model_name='gpt-3.5-turbo', client=None)

def generate(prompt):
    response = chat.generate(prompt)
    return response.generations[0][0].text

if __name__ == '__main__':
    content = st.text_input("Enter content to generate a lesson from:")
    if content:
        prompt = [f"create a teachable lesson from this content:{content}\
            \n\n ensure the format is in this fashion, use markdown convention:\n\
                # [SLIDE TITLE]\n\
                [slide content]\n\
                ---\
                # [SLIDE TITLE]\n\
                etc..."]
        
        slides = generate(prompt)
        st.write(slides)
        slide_title = slides.split("#")[1].split("\n")[0].strip()
        
        if not os.path.exists("text/"):
            os.makedirs("text/")
        with open("text/" + "lesson.md", "w") as f:
            f.write(slides)
        if not os.path.exists("slides/"):   
            os.makedirs("slides/")
            
        # convert to pptx using pandoc
        subprocess.call(["pandoc", "text/" + "lesson.md", "-o", "slides" + "lesson.pptx"])
        st.write("Done! Check the slides folder for your lesson")
