from src.Manager import wrapper_query_all,wrapper_insert
from src.config import *


@wrapper_insert(table_name='grupos')
def insert_grupo(nombre,cicloescolar,nrocontrol_tutor,idcarrera):
    return { 'field_values': {'nombre': nombre,'nrocontrol_tutor':nrocontrol_tutor,
                              'cicloescolar':cicloescolar,'idcarrera':idcarrera} }


@wrapper_query_all(table_name='grupos')
def consulta_general_grupos():
    return {TABLE_FIELDS:["Id Grupo","Nombre","Nro Control tutor","Ciclo Escolar", "Id carrera","Activo"]}
