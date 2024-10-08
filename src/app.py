import streamlit as st
from utils.log import logger
from translators.llm_translator import concurent_translate
from utils.utils import validate_api_key, export_api_key, extension_to_environ, download_file, save_translated, read_file, extract_images, download_image


st.title("Dcoument Translator with Image Extraction")
logger.info("App started")


with st.sidebar:
    api_key = st.sidebar.text_input("Enter your OPENAI_API_KEY  of your GOOGLE_API_KEY", type="password")
    api_key_validation = validate_api_key(api_key)
    if not api_key_validation.get("status") == "success":
        st.text("Please enter a valid API_KEY ")
        st.stop()
    else:
        st.success("API key validated")
        export_api_key(api_key_validation.get("message"), api_key)


uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
logger.info("PDF uploaded")


if uploaded_file is not None:
    extension = extension_to_environ(uploaded_file.name)
    target_language = st.selectbox("Select target language", ['french', 'english', 'espagnol', 'italian', 'german'])
    # Step 1: Extract and translate text page by page in parallel
    with st.spinner(f'Processing PDF... in {target_language}'):
        reader_list = read_file(uploaded_file, extension)
        logger.info(f"Translating PDF to {target_language}...")

        if len(reader_list)  > 10:
            st.warning("The PDF has more than 10 pages. This may take a while.")
        
        translated_pages, iamges_pages = concurent_translate(reader_list, 
                                               target_language, 
                                               api_key_validation.get("message"))
        
        # Step 2: Save the translated pages into a new PDF
        with st.spinner('Saving translated PDF...'):
            translated = save_translated(translated_pages, reader_list, extension)
            download_file(translated, target_language, uploaded_file.name)

        # Step 3: Extract images from the original PDF
        with st.spinner('Extracting images...'):
            image_files = extract_images(iamges_pages, extension)

        with st.sidebar:
            if len(image_files) > 0:
                st.write("Images extracted")
                download_image(image_files, uploaded_file.name)

# if __name__ == "__main__":
#     import os
#     os.system("streamlit run src/app.py")