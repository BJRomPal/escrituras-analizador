from pydantic import BaseModel, Field
from typing import List, Optional

class ParteInterviniente(BaseModel):
    rol: str = Field(description="Rol de la parte en la escritura (ej. Vendedor, Comprador, Apoderado, Donante, Donatario, etc.)")
    nombre: str = Field(description="Nombre o razón social de la parte")
    apellido: Optional[str] = Field(None, description="Apellido de la parte, si aplica para personas físicas")
    nacionalidad: Optional[str] = Field(None, description="Nacionalidad de la parte")
    fecha_nacimiento: Optional[str] = Field(None, description="Fecha de nacimiento de la parte (formato DD-MM-AAAA), si aplica")
    tipo_documento: Optional[str] = Field(None, description="Tipo de documento de identidad (ej. DNI, Cedula de Identidad, Pasaporte)")
    numero_documento: Optional[str] = Field(None, description="Número del documento de identidad")
    tipo_CUIL: Optional[str] = Field(None, description="Tipo de CUIL (ej. CUIL, CUIT)")
    numero_CUIL: Optional[str] = Field(None, description="Número del CUIL o CUIT")
    estado_civil: Optional[str] = Field(None, description="Estado civil de la parte (ej. casado/a, soltero/a, divorciado/a), si aplica")
    nombre_apellido_conyuge: Optional[str] = Field(None, description="Nombre y apellido del cónyuge del interviniente")
    domicilio: Optional[str] = Field(None, description="Domicilio completo de la parte")
    representacion: Optional[str] = Field(None, description="Si actúa en representación de alguien o una entidad, describir a quién o qué representa")

class NomenclaturaCatastralData(BaseModel):
    circunscripcion: str = Field(description="La circunscripción del inmueble")
    seccion: str = Field(description="la seccción del inmueble")
    quinta: Optional[str] = Field(None, description="la quinta del inmueble")
    fraccion: Optional[str] = Field(None, description="la fracción del inmueble")
    manzana: Optional[str] = Field(None, description="la manzana del inmueble")
    parcela: Optional[str] = Field(None, description="la parcela del inmueble")
    subparcela: Optional[str] = Field(None, description="la subparcela del inmueble")

class DescripcionPropiedadData(BaseModel):
    direccion: str = Field(description="Dirección de la propiedad")
    Partida: str = Field(description="Partida de la propiedad")
    nomenclatura_catastral: List[NomenclaturaCatastralData] = Field(description="Nomenclatura catastral de la propiedad")
    superficie: Optional[str] = Field(description="Superficie de la propiedad")
    medidas: Optional[str] = Field(description="Medidas y Linderos de la propiedad")
    matricula: Optional[str] = Field(description="Matrícula de la propiedad")

class EscrituraPublicaData(BaseModel):
    fecha_otorgamiento: str = Field(description="Fecha en que se otorgó la escritura")
    lugar_escritura: str = Field(description="Lugar celebración de la escritura pública")
    numero_escritura: str = Field(description="Número de la escritura pública")
    folio_escritura: str = Field(description="Folio de la escritura pública que se encuentra al final del documento (ej. que pasó ante mí al folio 784)")
    escribano: str = Field(description="Nombre completo del escribano que autorizó la escritura. Se encuentra al final del documento (ej. Ante mí: Juan Pérez)")
    registro_escribano: str = Field(description="Registro del escribano. Se encuentra al final del documento (Ej. del Registro 765)")
    partes_intervinientes: List[ParteInterviniente] = Field(description="Lista de los datos estructurados de las partes intervinientes, incluyendo su rol y datos personales.")
    descripcion_propiedad: DescripcionPropiedadData = Field(description="Descripción detallada de la propiedad, incluyendo dirección, matrícula, nomenclatura catastral, superficies.")
    valor_transaccion: str = Field(description="Valor monetario de la transacción si aplica, con moneda")
    observaciones: str = Field(description="Cualquier otra observación relevante no clasificada")