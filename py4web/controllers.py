"""
Acciones del app (versión reducida: solo lo necesario para alumnos)
"""

from yatl.helpers import A

from py4web import URL, abort, action, redirect, request
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

# Página HTML para probar la búsqueda de alumno por DNI
@action("alumno")
@action.uses("alumno.html", auth, T)
def alumno_page():
    return {}

# API: comprobar si existe alumno por DNI (GET o POST)
@action("api/alumno_exist", method=["GET", "POST"])
@action.uses(auth.user)
def alumno_exist():
    """
    - GET: /api/alumno_exist?dni=1234
    - POST: JSON body { "dni": "1234" }
    Requiere usuario autenticado (sigue el estilo de las acciones en el repo).
    """
    dni = None

    if request.method == "GET":
        dni = request.query.get("dni")
    else:
        j = request.json if hasattr(request, "json") else None
        if j:
            dni = j.get("dni")

    if not dni:
        return {"error": "dni is required"}

    row = db(db.alumno.dni == dni).select().first()
    if row:
        return {
            "exists": True,
            "alumno": {
                "id": row.id,
                "dni": row.dni,
                "nombre": row.nombre,
                "apellido": row.apellido,
                "email": row.email,
            },
        }
    else:
        return {"exists": False}
