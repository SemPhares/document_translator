import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_streamlit():
    with patch('app.st') as mock:
        yield mock

@pytest.fixture
def mock_logger():
    with patch('app.logger') as mock:
        yield mock

@pytest.fixture
def mock_validate_api_key():
    with patch('app.validate_api_key') as mock:
        mock.return_value = {"status": "success", "message": "Valid API Key"}
        yield mock

@pytest.fixture
def mock_concurent_translate():
    with patch('app.concurent_translate') as mock:
        mock.return_value = ["Translated page 1", "Translated page 2"]
        yield mock

@pytest.fixture
def mock_read_file():
    with patch('app.read_file') as mock:
        mock.return_value = ["Page 1 content", "Page 2 content"]
        yield mock

@pytest.fixture
def mock_save_translated():
    with patch('app.save_translated') as mock:
        mock.return_value = MagicMock()
        yield mock

@pytest.fixture
def mock_extract_images():
    with patch('app.extract_images') as mock:
        mock.return_value = ["image_1.png", "image_2.png"]
        yield mock