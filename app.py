import streamlit as st
import pdfplumber
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Gemini API

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# Page Settings

st.set_page_config(
    page_title="Fact Check Agent",
    page_icon="📄",
    layout="wide"
)

# Header

col1, col2 = st.columns([5, 1])

with col1:
    st.title("📄 Fact Check Agent")
    st.write(
        "Upload a PDF document and extract factual claims using AI."
    )

with col2:
    st.write("**Prashant Singh**")
    st.write("2022UIC3516")

st.divider()

# Upload PDF

file = st.file_uploader(
    "Choose a PDF File",
    type=["pdf"]
)

if file:

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.success("PDF Uploaded Successfully")

    # Preview

    with st.expander("View PDF Content"):

        st.write(text[:5000])

    # Extract Claims

    if st.button("🔍 Extract Claims"):

        with st.spinner("Extracting Claims..."):

            prompt = f"""
            Read the following document.

            Extract only factual claims.

            Focus on:
            - Statistics
            - Dates
            - Percentages
            - Financial figures
            - Technical facts

            Return a numbered list only.

            Document:

            {text}
            """

            response = model.generate_content(prompt)

            st.subheader("Extracted Claims")

            st.write(response.text)


if st.button("Verify Claims"):

    with st.spinner("Verifying Claims..."):

        verify_prompt = f"""
        Read the document below.

        Find factual claims and verify them.

        For each claim provide:

        Claim:
        Status: Verified / Inaccurate / False
        Explanation:

        Document:
        {text}
        """

        result = model.generate_content(verify_prompt)

        st.subheader("Verification Report")

        st.write(result.text)