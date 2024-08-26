import os
import io
import tempfile
import streamlit as st
import typing as t
from src.utils.log import logger

def validate_api_key(api_key:str):
    """
    """

    if not api_key:
        return {"status": "fail", "message": "Enmpty API key"}
    try:
        from google import generativeai as genai
        genai.configure(api_key= api_key)        
        model = genai.GenerativeModel(model_name = "gemini-1.0-pro-latest")
        return {"status": "success", "message": "google"}
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        #  validate openaa api key
        try:
            from openai import OpenAI
            OpenAI.api_key = api_key
            response = OpenAI.completions.create(
                engine="text-davinci-002",
                prompt="Translate the following text to French: 'Hello, how are you?'")
            return {"status": "success", "message": "openai"}
        
        except Exception as e:
            st.error(f"{e.__class__.__name__}: {e}")
            logger.error(f"{e.__class__.__name__}: {e}")
            return {"status": "fail", "message": "Invalid API key"}


def export_api_key(google_or_openai:str,
                   api_key:str):
    """
    """
    if google_or_openai == "google":
        os.environ["GOOGLE_API_KEY"] = api_key
    else:
        os.environ["OPENAI_API_KEY"] = api_key

    return st.success(f"{google_or_openai} API key exported")


def extension_to_environ(file_name:str):
    """
    """
    extension = file_name.split('.')[-1]
    logger.info(f"File extension: {extension}")
    os.environ['CUURENT_EXTENSION'] = extension
    return extension


def validate_extension(extension:str):
    """
    """
    if extension is None:
            extension = os.environ.get("CUURENT_EXTENSION")
    if extension is None:
        raise NameError(
            "No CUURENT_EXTENSION environment variable"
        )
    
    return extension


def read_file(file_path:str,
              extension:str) -> list:
    """
    """
    extension = validate_extension(extension)
    if extension == 'pdf':
        from src.utils.files.pdf import pdf_reader
        return pdf_reader(file_path)
    


def extract_text_from_page(pages:list,
                           page_num:int,
                           extension:str=None) -> str:
    """
    """
        
    extension = validate_extension(extension)
    if extension == 'pdf':
        from src.utils.files.pdf import extract_text_from_pdf_page
        return extract_text_from_pdf_page(pages, page_num)


def download_file(file:io.BytesIO,
                  target_language:str,
                  file_name:str):
    """
    """
    file_name = file_name.split('.')[0]
    return st.download_button("Download Translated PDF", file, 
                              file_name=f"trans_{target_language}_{file_name}.pdf")


def save_translated(translated_pages:t.Dict[int, str],
                    original_file,
                    extension:str=None,
                    ) -> io.BytesIO:
    """
    """
    translated = io.BytesIO()
    extension = validate_extension(extension)

    if extension == 'pdf':
        from src.utils.files.pdf import save_translated_pdf
        translated = save_translated_pdf(translated_pages, original_file)
    

    return translated

def file_to_tempfile(uploaded_file):
    """
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write the uploaded file to the temporary file
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
        logger.info(f"Temporary file path: {temp_file_path}")
    return temp_file_path


def extract_images(uploaded_file:str,
                   extension:str=None) -> list:
    """
    """
    extension = validate_extension(extension)
    temp_file_path = file_to_tempfile(uploaded_file)
    if extension == 'pdf':
        from src.utils.files.pdf import extract_images_from_pdf
        return extract_images_from_pdf(temp_file_path)
    