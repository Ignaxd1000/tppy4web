# check compatibility
import py4web

assert py4web.check_compatible("1.20190709.1")

# by importing controllers you expose the actions defined in it
from . import controllers

# by importing db you expose it to the _dashboard/dbadmin
from .models import db

# import the scheduler
from .tasks import scheduler

# optional parameters
__version__ = "1.0.0"
__author__ = "Ignaxd1000"
__license__ = "Ninguna"
