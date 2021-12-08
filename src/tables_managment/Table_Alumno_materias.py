from src.Manager import wrapper_insert
from src.config import *


@wrapper_insert(table_name='alumnos_materias')
def insert_alumno_materia(codigo_materia,nrocontrol):
    return { FIELD_VALUES: {'nrocontrol':nrocontrol,'codigo_materia': codigo_materia}}


# @wrapper_query_all("nrocontrol","codigo_materia", "calificacion","oportunidad","asesoria",table_name='alumnos_materias')
# def consulta_general_alumno_materia():
#     ...