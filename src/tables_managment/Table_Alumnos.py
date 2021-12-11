from src.Manager import wrapper_custom_query,wrapper_insert,wrapper_call_funcproc
from src.config import *


@wrapper_insert(table_name='alumnos')
def insert_alumno(nrocontrol,nombre,apellido1,apellido2,idgrupo):
    return { 'field_values': {'nombre':nombre,'apellido1':apellido1,'apellido2':apellido2,'idgrupo':idgrupo,
                              'nrocontrol': nrocontrol}}


@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="alumnos",
                      custom_select=["grupos.nombre"],innerjoin=["grupos"],
                      on=["grupos.idgrupo","alumnos.idgrupo"])
def consulta_general_alumnos(idgrupo):
    return {TABLE_FIELDS:["Nro Control","Nombre","Apellido 1","Apellido 2","Grupo"],
            'where': f"alumnos.idgrupo={idgrupo}"}


@wrapper_call_funcproc(func_name="get_session",error_msg="Nro de control o contrasenia incorrectos")
def session_alumno(nrocontrol,password):
    return { PARAMS:[nrocontrol,password,False] }