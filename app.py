import streamlit as st
import PyPDF2
import concurrent.futures
from utils.log import logger
from config.secrets import google_api_key
from translators.llm_translator import translate_page
from utils.pdf_utils import extract_images_from_pdf, save_translated_pdf


st.title("PDF Translator with Image Extraction")
logger.info("App started")

openai_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
google_key = st.sidebar.text_input("Enter your Google API key", type="password")
if not openai_key or not google_key:
    st.warning("Please enter your OpenAI or Google API key.")
    google_key = google_api_key
    st.stop()
    
api_key = openai_key if openai_key else google_key
key = 'openai' if openai_key else 'google'

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
logger.info("PDF uploaded")

if uploaded_file is not None:
    # Step 1: Extract and translate text page by page in parallel
    with st.spinner('Processing PDF...'):
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        target_language = st.selectbox("Select target language", ['fr', 'en', 'es', 'de', 'it'])
        logger.info(f"Translating PDF to {target_language}...")
        logger.info(f"Number of pages: {pdf_reader.getNumPages()}")

        if pdf_reader.getNumPages() > 10:
            st.warning("The PDF has more than 10 pages. This may take a while.")
        
        translated_pages = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(translate_page, pdf_reader, page_num, target_language, api_key, key ='google') 
                       for page_num in range(pdf_reader.getNumPages())]
            for future in concurrent.futures.as_completed(futures):
                page_num, translated_text = future.result()
                translated_pages[page_num] = translated_text
        
        # Step 2: Save the translated pages into a new PDF
        with st.spinner('Saving translated PDF...'):
            translated_pdf = save_translated_pdf(translated_pages, pdf_reader)
            st.download_button("Download Translated PDF", translated_pdf, file_name="translated.pdf")

        # Step 3: Extract images from the original PDF
        with st.spinner('Extracting images...'):
            image_files = extract_images_from_pdf(uploaded_file)

        st.write("Images extracted:")
        for image_file in image_files:
            st.image(image_file)
            with open(image_file, "rb") as img:
                st.download_button(label=f"Download {image_file}", data=img, file_name=image_file, mime="image/png")
