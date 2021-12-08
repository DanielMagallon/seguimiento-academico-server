from src.Manager import wrapper_query_all,wrapper_insert
from src.config import *


@wrapper_insert(table_name='carreras')
def insert_carrera(nombre,tipo,total_creditos):
    return { FIELD_VALUES: {'nombre': nombre,'tipo':tipo,'total_creditos':total_creditos}}


@wrapper_query_all(table_name='carreras')
def consulta_general_carrera():
    return {TABLE_FIELDS:["Carrera","Tipo","Total Creditos"]}