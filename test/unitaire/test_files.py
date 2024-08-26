import pytest
from unittest.mock import patch, MagicMock
from app import st  # Assuming your Streamlit app code is in a function named `app` in `app.py`


def test_api_key_validation_success(mock_streamlit, mock_validate_api_key):
    st()
    mock_streamlit.success.assert_called_with("API key validated")

def test_file_upload(mock_streamlit, mock_read_file):
    uploaded_file = MagicMock()
    mock_streamlit.file_uploader.return_value = uploaded_file
    st()
    mock_read_file.assert_called_with(uploaded_file, '.pdf')

def test_language_selection(mock_streamlit):
    st()
    mock_streamlit.selectbox.assert_called_with("Select target language", ['fr', 'en', 'es', 'de', 'it'])

def test_translation_process(mock_streamlit, mock_concurent_translate, mock_read_file):
    st()
    assert mock_concurent_translate.called

def test_image_extraction(mock_streamlit, mock_extract_images):
    st()
    assert mock_extract_images.called