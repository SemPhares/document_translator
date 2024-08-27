import PyPDF2
import io
from pdf2image import convert_from_path
# from utils.log import logger
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import utils



def pdf_reader(pdf_path:str) -> list[PyPDF2.PageObject]:
    """
    
    """
    reader = PyPDF2.PdfReader(pdf_path)
    # logger.info(f"Number of pages: {len(reader.pages)}")
    return reader.pages


def extract_text_from_pdf_page(pages:list[PyPDF2.PageObject],
                               page_num:int) -> str:
    """
    """
    page = pages[page_num]
    return page.extract_text()


def extract_image_from_pdf_page(pages:list[PyPDF2.PageObject],
                                page_num:int) -> list:
    """
    """
    page = pages[page_num]
    return page.images


def images_to_dict_bytes(images_pages:dict[int, list]) -> dict[str, bytes]:
    image_files = {}
    for page_idx, images_list in images_pages.items():
        for image_idx, image in enumerate(images_list):
            image_file = f"image_{page_idx}_{image_idx}.png"
            image_files[image_file] = image.data
    return image_files


def save_translated_pdf(translated_pages: dict[int, str]) -> io.BytesIO:
    output_pdf = io.BytesIO()
    
    # Dimensions de la page A4
    page_width, page_height = A4
    
    # Marges en millimètres, converties en points
    left_margin = 20 * mm
    right_margin = 20 * mm
    top_margin = 20 * mm
    bottom_margin = 20 * mm
    
    # Calcul de la largeur et de la hauteur utilisables
    usable_width = page_width - left_margin - right_margin

    # Créer le canvas ReportLab
    c = Canvas(output_pdf, pagesize=A4)

    # Paramètres de police
    c.setFont("Helvetica", 12)
    line_height = 14  # Hauteur de ligne en points

    for page_num, translated_text in sorted(translated_pages.items()):
        # Diviser le texte en lignes pour s'assurer qu'il s'adapte à la largeur de la page
        lines = utils.simpleSplit(translated_text, 'Helvetica', 12, usable_width)

        # Initialiser les positions de départ pour écrire
        current_y = page_height - top_margin
        
        for line in lines:
            # Vérifier si la page a encore assez d'espace pour écrire une ligne
            if current_y - line_height < bottom_margin:
                c.showPage()  # Créer une nouvelle page
                current_y = page_height - top_margin  # Réinitialiser la position en haut de la nouvelle page

            # Écrire la ligne et passer à la suivante
            c.drawString(left_margin, current_y, line)
            current_y -= line_height

        # Passer à une nouvelle page après avoir écrit le texte traduit d'une page originale
        c.showPage()

    c.save()
    output_pdf.seek(0)
    return output_pdf



if __name__ == "__main__":
    pdf_path = "/Users/elsem/Documents/code/document_translator/test/doc/Ascension Day of Jesus Christ (Poster).pdf"
    list_pages = pdf_reader(pdf_path)
    # translated_pages = {0: "lorem ipsum \n"*260, 1: "ceci est un test "*10000}
    pages = extract_text_from_pdf_page(list_pages, 0)+"\n"*50
    translated_pages = {i: pages for i in range(10)}
    out_pdf = save_translated_pdf(translated_pages).read()
    with open("/Users/elsem/Documents/code/document_translator/test/doc/test-translated.pdf", "wb") as f:
        f.write(out_pdf)

    # print(extract_images_from_pdf(pdf_path))