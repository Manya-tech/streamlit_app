# Q&A Chatbot
#from langchain.llms import OpenAI

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBbEpOFAfxkZqui0O5UKHDE8aGW2P4EF6A"

genai.configure(api_key=GOOGLE_API_KEY)

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    result=response.text
    # result = result[0]['text']
    return result
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Code Generator")

st.header("Personalized Plan Generator")
deadline=st.text_input("Deadline: ")
hours = st.text_input("How many hours can you commit per day:")
marks = st.text_input("How many marks you want achieved last semester:")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
# uploaded_mark = st.file_uploader("Upload marksheet...", type=["jpg", "jpeg", "png"])
# marksheet=""   
# if uploaded_mark is not None:
#     marksheet = Image.open(uploaded_mark)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Generate plan")

input_prompt = """
               You are an expert in creating detailed plans for achieving goals on the basis of provided deadline and capabilities of the individual.
               You will receive input image of a syllabus, users capabilities in terms of text and a deadline alongwith how much time they can commit per day.
               Generate a detailed personalized plan on the basis of all this information so that the user can achieve their goal efficiently and effectively in the given time frame.
               The plan should define which topic should be done when and how much time should be spent on each topic.
               """

## If ask button is clicked
input = "Deadline is {deadline} days and user can commit {hours} hours per day. I got {marks} last semester".format(deadline=deadline,hours=hours, marks=marks)
if submit:
    image_data = input_image_setup(uploaded_file)
    # mark_data = input_image_setup(uploaded_mark)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The detailed plan is")
    st.write(response)
    