from docx import Document

def read_word_file(file):
    document = Document(file)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)