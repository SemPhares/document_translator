import PyPDF2
from PIL import Image
import io
from pdf2image import convert_from_path



def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    image_files = []
    for i, image in enumerate(images):
        image_file = f'image_{i + 1}.png'
        image.save(image_file, 'PNG')
        image_files.append(image_file)
    return image_files


def extract_text_from_page(pdf_reader, page_num):
    page = pdf_reader.getPage(page_num)
    return page.extract_text()


def save_translated_pdf(translated_pages, original_pdf):
    output_pdf = io.BytesIO()
    pdf_writer = PyPDF2.PdfFileWriter()
    
    for page_num, translated_text in sorted(translated_pages.items()):
        page = original_pdf.getPage(page_num)
        pdf_writer.addBlankPage(width=page.mediaBox.getWidth(),
                                height=page.mediaBox.getHeight())
        # Ajouter le texte traduit à la page PDF
        pdf_writer.getPage(page_num).merge_text(translated_text)

    pdf_writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf
