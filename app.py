import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Smart ATS",
    page_icon= "🤖",
    layout="centered",
)


API_KEY = "YOUR_API_KEY"

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Configure Gemini AI model with the provided API key
configure_gemini_api(API_KEY)

# Function to get response from Gemini AI
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt 
input_prompt = """
You are an expert in resume evaluation and job matching. I need you to analyze an input resume against a given job description and provide the following outputs:
ATS Score: Calculate the ATS (Applicant Tracking System) score for the resume based on the job description. The score should be provided as a percentage.
Missing Words: Identify and list the important keywords or phrases that are present in the job description but missing in the resume. These should 
be words or phrases that are highly relevant to the job role and necessary for matching the resume with the job description.
Resume Summary: Provide a brief summary of the resume, highlighting the key skills, experiences, and qualifications of the candidate.
Recommendations for Improvement: Based on the job description, suggest specific improvements to enhance the quality of the resume. 
This can include adding missing keywords, rephrasing certain sections, emphasizing relevant experiences, and any other changes that would increase the resume's 
relevance to the job description.
Inputs:
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":"", "Recommendations":""}}
"""

st.title("Resume Matcher ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader("Response:")
        parsed_response = json.loads(response)
        percent = parsed_response['JD Match']
        percent = percent.replace("%", "")
        progress_text = "Your score"
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(int(percent)):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        for key, value in parsed_response.items():
            st.write(f"**{key}:** {value}")

