import psycopg2
from flask import Flask
import json
from psycopg2 import Error
from flask_cors import CORS

try:
    app = Flask(__name__)
    CORS(app)
    connection = psycopg2.connect(user='postgres',password='psql',host='127.0.0.1',
                          database='seguimiento_academico')

    cursor = connection.cursor()
    print(f"PostgreSQL server information, cursor type: {type(cursor)}")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)



def wrapper_custom_query(*args,**kwargs):

    def decorator(func):
        def wrapper(*wargs,**wkwargs):
            data_func = func(*wargs,**wkwargs)
            args2 = ['{}.{}'.format(kwargs["table_name"],a) for a in args]
            fields = str(args2).replace("[","").replace("]","").replace("'","")

            if kwargs.get('selectjoin'):
                select_args = str(kwargs['selectjoin']).replace("[","").replace("]","").replace("'","")
                select = f"SELECT {fields},{select_args} FROM {kwargs['table_name']}"
            else:
                select = f"SELECT {fields} FROM {kwargs['table_name']}"

            if kwargs.get('innerjoin') and kwargs.get('on'):
                onq = kwargs['on']
                index=0
                joinquery=''
                for injoin in kwargs['innerjoin']:
                    on1 = onq[index]
                    index+=1
                    on2 = onq[index]
                    index+=1
                    joinquery+=f' inner join {injoin} on {on1}={on2}'

                query = select + joinquery
            else:
                query = select

            if data_func.get('where'):
                query += data_func['where']

            print(f'Custo query: {query}')
            cursor.execute(query)
            record = cursor.fetchall()

            return json.dumps({'fields': data_func['tables_fields'], 'values': record})


        return wrapper

    return decorator


def wrapper_query_all(*args,**kwargs):

    def decorator(func):
        def wrapper(*wargs,**wkwargs):
            data_func: dict = func(*wargs,**wkwargs)
            query = f'SELECT * FROM {kwargs["table_name"]}'
            print(f"Query: {query}")
            cursor.execute(query)
            record = cursor.fetchall()

            dic = {'fields':data_func['tables_fields'],'values': record}

            return dic

        return wrapper

    return decorator


def wrapper_insert(*args,**kwargs):

    def decorator(function):
        def wrapper(*arg2,**kwargs2):
            data: dict = function(*arg2,**kwargs2)

            fields = str(list(data['field_values'].keys())).replace("[","(").replace("]",")").replace("'","")
            values = str(list(data['field_values'].values())).replace("[","(").replace("]",")")
            query = f'INSERT INTO {kwargs["table_name"]} {fields} VALUES {values}'

            try:
                cursor.execute(query)
                dic = {'status': 0,'title': f'Tabla "{kwargs["table_name"]}" actualizada',
                       'msg': 'Registro ingresado correctamente'}

            except Exception as ex:
                dic = {'status': -1, 'title': f'Error al registar en  {kwargs["table_name"]}',
                        'msg': repr(ex)}

            connection.commit()
            return dic

        return wrapper

    return decorator


'''Seccion Grupos'''


@wrapper_insert(table_name='grupos')
def insert_grupo(nombre,cicloescolar,nrocontrol_tutor,idcarrera):
    return { 'field_values': {'nombre': nombre,'nrocontrol_tutor':nrocontrol_tutor,
                              'cicloescolar':cicloescolar,'idcarrera':idcarrera} }


@wrapper_query_all(table_name='grupos')
def consulta_general_grupos():
    return {'tables_fields':["Id Grupo","Nombre","Nro Control tutor","Ciclo Escolar", "Id carrera","Activo"]}


'''Fin seccin grupos'''


'''Seccion alumnos'''


@wrapper_insert(table_name='alumnos')
def insert_alumno(nrocontrol,nombre,apellido1,apellido2,idgrupo):
    return { 'field_values': {'nombre':nombre,'apellido1':apellido1,'apellido2':apellido2,'idgrupo':idgrupo,
                              'nrocontrol': nrocontrol}}


@wrapper_query_all(table_name='alumnos')
def consulta_general_alumnos():
    return {'tables_fields':["Alumno","Apellido 1","Apellido 2","Nro Control"]}


'''FIn seccion alumnos'''


'''Seccion tutores'''


@wrapper_insert(table_name='tutores')
def insert_tutor(nrocontrol,nombre,apellido1,apellido2,idcarrera):
    return { 'field_values': {'nrocontrol': nrocontrol,'nombre':nombre,'apellido1':apellido1,
                              'apellido2':apellido2,'idcarrera':idcarrera}}


# @wrapper_query_all("nrocontrol", "nombre", "apellido1", "apellido2", "idcarrera",table_name='tutores')
# def consulta_general_tutor():
#     ...


@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="tutores",
                      selectjoin=["carreras.nombre"],innerjoin=["carreras"],on=["tutores.idcarrera","carreras.idcarrera"])
def consulta_tutores():
    return {'tables_fields':["Nro Control","Tutor","Apellido 1","Apellido 2","Carrera"]}

'''Fin seccion tutores'''


'''Seccion carreas'''


@wrapper_insert(table_name='carreras')
def insert_carrera(nombre,tipo,total_creditos):
    return { 'field_values': {'nombre': nombre,'tipo':tipo,'total_creditos':total_creditos}}


@wrapper_query_all(table_name='carreras')
def consulta_general_carrera():
    return {'tables_fields':["Carrera","Tipo","Total Creditos"]}


'''Fin seccion carreas'''


'''Seccion materias'''


@wrapper_insert(table_name='materias')
def insert_materia(codigo_materia,nombre,creditos):
    return { 'field_values': {'codigo_materia':codigo_materia,'nombre': nombre,'creditos':creditos}}


@wrapper_query_all(table_name='materias')
def consulta_general_materia():
    return {'tables_fields':["Codigo ","Materia","Creditos"]}


'''Fin seccion materias'''


'''Seccion alumnos_materias'''


@wrapper_insert(table_name='alumnos_materias')
def insert_alumno_materia(codigo_materia,nrocontrol):
    return { 'field_values': {'nrocontrol':nrocontrol,'codigo_materia': codigo_materia}}


# @wrapper_query_all("nrocontrol","codigo_materia", "calificacion","oportunidad","asesoria",table_name='alumnos_materias')
# def consulta_general_alumno_materia():
#     ...


'''Fin seccion alumnos_materias'''


'''Seccion Pagina Consulta/Altas Tutores'''


@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="tutores",
                      selectjoin=["carreras.nombre"],innerjoin=["carreras"],on=["tutores.idcarrera","carreras.idcarrera"])
def consulta_tutores():
    return {'tables_fields':["Nro Control","Tutor","Apellido 1","Apellido 2","Carrera"]}


@wrapper_custom_query("idgrupo","nombre","cicloescolar","idcarrera",table_name="grupos")
def __extraer_grupo_tutor(nrocontrol_tutor):
    return {'where': f"nrocontrol_tutor='{nrocontrol_tutor}' and activo",
            'table_fields':["Id grupo","Nombre","Ciclo escolar","Id carrera"]}


def consulta_pagina_tutores(nrocontrol_tutor):
    paso1 = __extraer_grupo_tutor(nrocontrol_tutor)
    print(f"Paso 1: Grupo = {paso1}")
    return "Ok"


'''Fin Seccion'''

def close():
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
