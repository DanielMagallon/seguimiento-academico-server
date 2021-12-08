from src.Manager import wrapper_query_all,wrapper_insert
from src.config import *


@wrapper_insert(table_name='materias')
def insert_materia(codigo_materia,nombre,creditos):
    return { FIELD_VALUES: {'codigo_materia':codigo_materia,'nombre': nombre,'creditos':creditos}}


@wrapper_query_all(table_name='materias')
def consulta_general_materia():
    return {TABLE_FIELDS:["Codigo ","Materia","Creditos"]}