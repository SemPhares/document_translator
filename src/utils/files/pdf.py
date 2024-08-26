import PyPDF2
from PIL import Image
import io
from pdf2image import convert_from_path
from src.utils.log import logger
import io
import typing as t
import PyPDF2
from reportlab.pdfgen.canvas import Canvas
from decimal import Decimal


def pdf_reader(pdf_path:str):
    """
    
    """
    reader = PyPDF2.PdfReader(pdf_path)
    logger.info(f"Number of pages: {len(reader.pages)}")
    pages = [reader.pages[i] for i in range(len(reader.pages))]
    return pages


def extract_text_from_pdf_page(pages:list[PyPDF2.PageObject],
                               page_num:int) -> str:
    """
    """
    page = pages[page_num]
    return page.extract_text()


def extract_images_from_pdf(pdf_path:str) -> list[str]:
    images = convert_from_path(pdf_path)
    image_files = []
    for i, image in enumerate(images):
        image_file = f'image_{i + 1}.png'
        image.save(image_file, 'PNG')
        image_files.append(image_file)
    return image_files


def save_translated_pdf(translated_pages: dict[int, str],
                        pages_list: list[PyPDF2.PageObject]) -> io.BytesIO:
    output_pdf = io.BytesIO()
    pdf_writer = PyPDF2.PdfWriter()

    for page_num, translated_text in sorted(translated_pages.items()):
        # Get the original page dimensions
        original_page = pages_list[page_num]
        page_width = original_page.mediabox.width
        page_height = original_page.mediabox.height
        
        # Create a temporary PDF with the translated text
        translated_pdf = io.BytesIO()
        c = Canvas(translated_pdf, pagesize=(page_width, page_height))
        
        # Add the translated text to the canvas
        c.drawString(72, float(page_height - Decimal('72')), translated_text)  # Adjust position as needed
        c.showPage()
        c.save()
        
        translated_pdf.seek(0)
        
        # Read the translated text PDF as a page
        translated_reader = PyPDF2.PdfReader(translated_pdf)
        translated_page = translated_reader.pages[0]
        
        # Add the translated page to the writer
        pdf_writer.add_page(translated_page)
    
    # Write the output PDF to a BytesIO object
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf



if __name__ == "__main__":
    pdf_path = "document_translator/test/doc/Ascension Day of Jesus Christ (Poster).pdf"
    pages = pdf_reader(pdf_path)
    print(extract_text_from_pdf_page(pages, 0))
    print(extract_images_from_pdf(pdf_path))