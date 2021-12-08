from src.Manager import wrapper_insert,wrapper_custom_query,session,cursor
from src.config import *

@wrapper_insert(table_name='tutores')
def insert_tutor(nrocontrol,nombre,apellido1,apellido2,idcarrera):
    return { FIELD_VALUES: {'nrocontrol': nrocontrol,'nombre':nombre,'apellido1':apellido1,
                              'apellido2':apellido2,'idcarrera':idcarrera}}


# @wrapper_query_all("nrocontrol", "nombre", "apellido1", "apellido2", "idcarrera",table_name='tutores')
# def consulta_general_tutor():
#     ...


@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="tutores",
                      custom_select=["carreras.nombre"],innerjoin=["carreras"],on=["tutores.idcarrera","carreras.idcarrera"])
def consulta_tutores():
    return {TABLE_FIELDS:["Nro Control","Tutor","Apellido 1","Apellido 2","Carrera"]}



def session_tutor(nrocontrol,password):
    