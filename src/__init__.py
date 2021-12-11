from flask import Response, request
from Manager import *
from flask_cors import cross_origin
from secciones_paginas.Tutores import *
from tables_managment.Table_Materias import *
from tables_managment.Table_Tutores import *
from tables_managment.Table_Carreras import *
from tables_managment.Table_Alumno_materias import *
from tables_managment.Table_Alumnos import *
from tables_managment.Table_Grupos import *