from src.Manager import wrapper_insert,wrapper_custom_query,wrapper_call_funcproc
from src.config import *


@wrapper_insert(table_name='tutores')
def insert_tutor(nrocontrol,nombre,apellido1,apellido2,idcarrera,password):
    cryptpass = f"crypt('{password}',gen_salt('bf'))"
    return { FIELD_VALUES: {'nrocontrol': nrocontrol,'nombre':nombre,'apellido1':apellido1,
                              'apellido2':apellido2,'idcarrera':idcarrera,"password":cryptpass}}


@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="tutores",
                      custom_select=["carreras.nombre"],innerjoin=["carreras"],on=["tutores.idcarrera","carreras.idcarrera"])
def consulta_tutores():
    return {TABLE_FIELDS:["Nro Control","Tutor","Apellido 1","Apellido 2","Carrera"]}


@wrapper_call_funcproc(func_name="get_session",error_msg="Nro de control o contrasenia incorrectos")
def session_tutor(nrocontrol,password):
    return {
        TABLE_FIELDS: ["Id grupo","Nombre","Carrera"],
        PARAMS:[nrocontrol,password,True]
    }
