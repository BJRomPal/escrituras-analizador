from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    """
    Extrae texto de un PDF usando Tesseract. Si el PDF no es seleccionable,
    lo convierte a imágenes y luego aplica OCR.
    """
    text = ""
    try:
        # Intenta extraer texto directamente si el PDF es seleccionable
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip(): # Si se extrajo texto seleccionable, lo retornamos
            print("Texto seleccionable extraído directamente.")
            return text
    except Exception as e:
        print(f"No se pudo extraer texto seleccionable, intentando OCR: {e}")

    # Si no se extrajo texto seleccionable, o hubo un error, se usa OCR
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            print(f"Procesando página {i+1} con Tesseract (OCR)...")
            # Usa 'spa' para español, asegúrate de que el paquete de idioma esté instalado en Tesseract
            page_text = pytesseract.image_to_string(image, lang='spa')
            text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error al convertir PDF a imagen o al aplicar OCR con Tesseract: {e}")
        return e