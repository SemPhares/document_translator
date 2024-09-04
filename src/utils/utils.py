import os
import io
import zipfile
import tempfile
import streamlit as st
import typing as t
from utils.log import logger


def validate_api_key(api_key:str):
    """
    """

    if not api_key:
        return {"status": "fail", "message": "Enmpty API key"}
    try:
        from google import generativeai as genai
        genai.configure(api_key= api_key)        
        model = genai.GenerativeModel(model_name = "gemini-1.0-pro-latest")
        response = model.generate_content("Translate the following text to French: 'Hello, how are you?'").text
        return {"status": "success", "message": "google"}
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        #  validate openAI api key
        try:
            from openai import OpenAI
            client=OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="text-davinci-002",
                messages=[
                {"role": "system", "content": "You are an expert in translations"},
                {"role": "user", "content": "Translate the following text to French: 'Hello, how are you?"}
                    ]
            )
            return {"status": "success", "message": "openai"}
        
        except Exception as e:
            st.error("Invalid API key")
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
        from utils.files.pdf import pdf_reader
        return pdf_reader(file_path)
    

def extract_text_from_page(pages:list,
                           page_num:int,
                           extension:str=None) -> str:
    """
    """  
    extension = validate_extension(extension)
    if extension == 'pdf':
        from utils.files.pdf import extract_text_from_pdf_page
        return extract_text_from_pdf_page(pages, page_num)
    

def extract_images_from_page(pages:list,
                             page_num:int,
                             extension:str=None) -> list:
    """
    """
    extension = validate_extension(extension)
    if extension == 'pdf':
        from utils.files.pdf import extract_image_from_pdf_page
        return extract_image_from_pdf_page(pages, page_num)


def download_file(file:io.BytesIO,
                  target_language:str,
                  file_name:str):
    """
    """
    file_name = file_name.split('.')[0]
    return st.download_button("Download Translated PDF", file, 
                              file_name=f"trans_{target_language}_{file_name}.pdf")


def download_image(image_files:dict[str, bytes],
                   file_name:str):
    """
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for image_name, image_bytes in image_files.items():
            zip_file.writestr(image_name, image_bytes)

    zip_buffer.seek(0)

    # Provide the zip file download button
    st.download_button(
        label="Download Zip",
        data=zip_buffer,
        file_name=f"{file_name}-images.zip",
        mime="application/zip"
    )
                   

def save_translated(translated_pages:t.Dict[int, str],
                    original_pages:list,
                    extension:str=None,
                    ) -> io.BytesIO:
    """
    """
    translated = io.BytesIO()
    extension = validate_extension(extension)

    if extension == 'pdf':
        from utils.files.pdf import save_translated_pdf
        translated = save_translated_pdf(translated_pages)

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


def extract_images(images_pages:dict[int, list],
                   extension:str=None) -> dict[str, bytes]:
    """
    """
    extension = validate_extension(extension)
    # temp_file_path = file_to_tempfile(uploaded_file)
    if extension == 'pdf':
        from utils.files.pdf import images_to_dict_bytes
        return images_to_dict_bytes(images_pages)
    

