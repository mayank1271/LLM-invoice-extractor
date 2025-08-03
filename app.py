from dotenv import load_dotenv
load_dotenv()## load all the environment variables
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## load the gemini model
model=genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## initialize the streamlit app
st.set_page_config(page_title="invoice extractor app")
st.header("Invoice Extractor App")
input=st.text_input("Enter the input")
uploaded_file=st.file_uploader("Upload an image",type=["jpg","png","jpeg"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("tell me about the invoice")

input_prompt="""
you are an expert in understaning invoices. we will upload a image as invoice
and you will have to answer any question based on the uploaded invoice image
"""

## if submit button is clicked
if submit:
    image_data= input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("the response is")
    st.write(response)




