"""
Tutorial para API web e Interfaz móvil
ET 29 DE 6 "Reconquista de Buenos Aires"

Copyright 2025 Alan Edmundo Etkin

Por la presente se concede permiso, libre de cargos, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados (el "Software"), a utilizar el Software[...] El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.
EL SOFTWARE SE PROPORCIONA "COMO ESTÁ", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR[...] 
"""

This file defines the database models

from pydal.validators import *

from .common import Field, db

# Tabla para alumnos (dni debe ser único)
db.define_table(
    "alumno",
    Field("dni", "string", unique=True, requires=[IS_NOT_EMPTY(), IS_LENGTH(20)]),
    Field("nombre", "string", requires=IS_NOT_EMPTY()),
    Field("apellido", "string"),
    Field("email", "string"),
)

# Confirma los cambios en el esquema
db.commit()