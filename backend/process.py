from .ocr import extract_text_from_pdf
from .extractor import extract_data_with_langchain

def process_escritura_publica(pdf_path):
    """
    Orquestra el proceso completo de extracción, análisis y almacenamiento.
    Utiliza funciones de OCR y LangChain para extraer datos relevantes de un PDF de escritura pública.
    """
    print(f"\n--- Iniciando procesamiento de: {pdf_path} ---")

    # 1. Extraer texto del PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print("No se pudo extraer texto del PDF. Abortando.")
        return

    print("\nTexto extraído")
    
    # 2. Extraer datos relevantes con LangChain y GPT
    print("\nIniciando extracción de datos con LangChain y GPT...")
    relevant_data = extract_data_with_langchain(extracted_text)
    if not relevant_data:
        print("No se pudieron extraer datos relevantes. Abortando.")
        return

    print("\nDatos extraídos:")
    print(relevant_data.model_dump_json(indent=2))
    return relevant_data.model_dump()
