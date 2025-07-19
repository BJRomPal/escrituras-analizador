# Import necessary libraries
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
import os

# Buscamos los modelos Pydantic necesarios para la extracción de datos
from .models import EscrituraPublicaData

load_dotenv()

# Buscamos la clave de OpenAI está configurada en las variables de entorno
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Configura el parser de salida Pydantic
parser = PydanticOutputParser(pydantic_object=EscrituraPublicaData)

# Creamos el prompt para GPT
prompt_template = PromptTemplate(
    template="""Debes Extraer la siguiente información exclusivamente de la **escritura pública actual** proporcionada.

    INSTRUCCIONES IMPORTANTES:

    1. **Escribano firmante (otorgante):**
      - La escritura puede mencionar varios escribanos. Identificá **únicamente** al **escribano firmante**, que siempre está mencionado al final del documento (en la fórmula de cierre o en la firma o después de la palabra Ante mí y antes de la palabra **CONCUERDA**).
      - No uses escribanos citados como antecedentes, autorizantes de documentos previos, ni reemplazantes.
      - Si aparecen folio y registro, también deben corresponder al escribano firmante, que están al **final del documento**.

    2. **Partes intervinientes:**
      - Identificá correctamente a los **comparecientes verdaderos**.
      - Si una persona actúa **en representación de otra persona física o jurídica (ej: sociedad)**, el **interviniente es el representado**, no el representante.
        - Ejemplo correcto: `"Juan Perez o el primero o el segundo interviene en nombre y representación de Constructora Class SA)"`
        - Ejemplo incorrecto: `"Juan Pérez"`
      - Si hay más de una parte representada, listalas por separado.
      - Si la persona es física debes poner su rol en la escritura (vendedor o comprador) y todos los datos personales: nombre, apellido, nacionalidad, fecha de nacimiento, documento de identidad, estado civil, domicilio
      - Si es una persona jurídica poner su rol en la escritura (vendedor o comprador) y el nombre y el domicilio.
      - Recuerda poner el **rol en la escritura** (Vendedor o Comprador).

    3. **Número de escritura:**
      - Devuélvelo en número arábigo (ej: `435`) aunque esté en letras en el texto.

    4. **Datos faltantes:**
      - Si un campo no aparece en el texto, devuélvelo como campo vacío (`""` o lista vacía).

    -----

    **Formato de Salida:**
    Formatea tu respuesta estrictamente como un objeto JSON siguiendo este esquema:
    {format_instructions}

    **Texto de la escritura pública:**
    {escritura_text}

    """
    ,
    input_variables=["escritura_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def extract_data_with_langchain(text_from_pdf):
    """
    Utiliza LangChain y GPT para extraer datos relevantes del texto.
    """
    if not text_from_pdf:
        return None
    try:
    # Verifica si la clave de OpenAI está configurada
        if not os.getenv("OPENAI_API_KEY"):
            print("Por favor, configura la variable de entorno OPENAI_API_KEY con tu clave de OpenAI.")
            return None
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)

        # Crea la cadena de LangChain
        extraction_chain = prompt_template | llm | parser
        # Invoca la cadena con el texto del PDF
        extracted_data = extraction_chain.invoke({"escritura_text": text_from_pdf})
        return extracted_data
    except Exception as e:
        print(f"Error al extraer datos con LangChain: {e}")
        import traceback
        traceback.print_exc()
        return None