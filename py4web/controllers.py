"""
Tutorial para API web e Interfaz móvil
ET 29 DE 6 "Reconquista de Buenos Aires"

Copyright 2025 Alan Edmundo Etkin

Por la presente se concede permiso, libre de cargos, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados (el "Software"), a utilizar el Software sin restricción, incluyendo sin limitación los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender copias del Software, y a permitir a las personas a las que se les proporcione el Software a hacer lo mismo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.
EL SOFTWARE SE PROPORCIONA "COMO ESTÁ", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR E INCUMPLIMIENTO. EN NINGÚN CASO LOS AUTORES O PROPIETARIOS DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O CUALQUIER OTRO MOTIVO, DERIVADAS DE, FUERA DE O EN CONEXIÓN CON EL SOFTWARE O SU USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.
"""

"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from yatl.helpers import A

from py4web import URL, abort, action, redirect, request

# agregar objeto HTTP
from py4web import HTTP

from .common import (
    T,
    auth,
    authenticated,
    cache,
    db,
    flash,
    logger,
    session,
    unauthenticated,
)

@action("index")
@action.uses("index.html", auth, T)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}").format(**user) if user else T("Hello")
    return dict(message=message)

# API web: acciones para consultas y modificaciones de la BDD

    
@action("recuperar")
@action.uses(auth.user)
def recuperar():
    """ Esta acción devuelve la fruta almacenada y la opción
    de cáscara. Si el registro no existe crea uno por defecto."""
    registro = db(db.fruta).select().first()
    if registro is None:
        db.fruta.insert(nombre="banana", cascara=True)
        db.commit()
        registro = db(db.fruta).select().first()
    return dict(nombre=registro.nombre, cascara=registro.cascara)

@action("cargar")
@action.uses(auth.user)
def cargar():
    """ Esta acción modifica la fruta almacenada y la opción
    de cáscara con los parámetros que recibe de la "query string"."""    
    nombre = request.query["nombre"]
    if request.query["cascara"] == "true":
        cascara = True
    else:
        cascara = False
    registro = db(db.fruta).select().first()
    if registro is None:
        db.fruta.insert(nombre=nombre, cascara=cascara)
    else:
        registro.update_record(nombre=nombre, cascara=cascara)
    db.commit()
    return dict()
