from dotenv import load_dotenv 

load_dotenv() 

import streamlit as st
import os 

# from pdf2image import convert_from_bytes

from PIL import Image 
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("Invoice Extractor using Google Gemini Pro")

## Function to load gemini pro vision 
# model=genai.GenerativeModel("gemini-pro-vision")
model = genai.GenerativeModel("gemini-2.5-flash")


def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image, prompt])
    return response.text

## this will take the uploaded file and convert it into bytes and will image format which can be fed to the gemini pro vision model
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        ## Read the file as bytes
        bytes_image_data = uploaded_file.getvalue()

        image_parts =  {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": bytes_image_data
            }
        
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded. Please upload an image file to proceed.")
    


## Initialize our streamlit app 
st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt : ", key="input")

uploaded_file=st.file_uploader("Upload Invoice Image", type=["jpg", "jpeg", "png", "pdf"], key="file")  
image=""

if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice Image", use_column_width=True)


submit=st.button("Tell me about the invoice")


## how I want gemeini model to behave  -- its important to give clear instructions to the model
input_prompt="""
You are an export in understanding invoice. We will upload a image as invoice and you will have to answer any question based on the uploaded invoice image 
"""

## if submit button is clicked 

if submit:
    image_data=input_image_details(uploaded_file) ## this will convert the uploaded image into bytes and image format which can be fed to the gemini pro vision model
    response=get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is ")
    st.write(response)


