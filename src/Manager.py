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


def wrapper_query_all(*args,**kwargs):

    def decorator(func):
        def wrapper():
            # data: dict = func()
            query = f'SELECT * FROM {kwargs["table_name"]}'
            print(f"Query: {query}")
            cursor.execute(query)
            record = cursor.fetchall()

            dic = {'fields':args,'values': record}

            print(f"Record dic: {dic}")
            return json.dumps(dic)

        return wrapper

    return decorator


def wrapper_insert(*args,**kwargs):

    def decorator(function):
        def wrapper(*arg2,**kwargs2):
            data: dict = function(*arg2,**kwargs2)
            print(f"Data: {data}")
            fields = str(list(data['field_values'].keys())).replace("[","(").replace("]",")").replace("'","")
            values = str(list(data['field_values'].values())).replace("[","(").replace("]",")")
            query = f'INSERT INTO {kwargs["table_name"]} {fields} VALUES {values}'

            print(f"Query: {query}")
            try:
                cursor.execute(query)
                dic = {"status": 0,"title": f"Tabla '{kwargs['table_name']}' actualizada",
                       "msg": "Registro ingresado correctamente"}

            except Exception as ex:
                dic = {"status": -1, "title": f"Error al registar en  {kwargs['table_name']}",
                        "msg": repr(ex)}

            connection.commit()
            return json.dumps(dic)

        return wrapper

    return decorator


'''Seccion Grupos'''


@wrapper_insert(table_name='grupos')
def insert_grupo(nombre):
    return { 'field_values': {'nombre': nombre} }


@wrapper_query_all("idgrupo","nombre", table_name='grupos')
def consulta_general_grupos():
    ...


'''Fin seccin grupos'''


'''Seccion alumnos'''


@wrapper_insert(table_name='alumnos')
def insert_alumno(nrocontrol,nombre,apellido1,apellido2,idgrupo):
    return { 'field_values': {'nombre':nombre,'apellido1':apellido1,'apellido2':apellido2,'idgrupo':idgrupo,
                              'nrocontrol': nrocontrol}}


@wrapper_query_all("nombre", "apellido1", "apellido2", "idgrupo", "nrocontrol", table_name='alumnos')
def consulta_general_alumnos():
    ...


'''FIn seccion alumnos'''


'''Seccion tutores'''


@wrapper_insert(table_name='tutores')
def insert_tutor(nrocontrol,nombre,apellido1,apellido2,idcarrera):
    return { 'field_values': {'nrocontrol': nrocontrol,'nombre':nombre,'apellido1':apellido1,
                              'apellido2':apellido2,'idcarrera':idcarrera}}


@wrapper_query_all("nrocontrol", "nombre", "apellido1", "apellido2", "idcarrera",table_name='tutores')
def consulta_general_tutor():
    ...


'''Fin seccion tutores'''


'''Seccion carreas'''


@wrapper_insert(table_name='carreras')
def insert_carrera(nombre,tipo,total_creditos):
    return { 'field_values': {'nombre': nombre,'tipo':tipo,'total_creditos':total_creditos}}


@wrapper_query_all("nombre", "tipo","total_creditos",table_name='carreras')
def consulta_general_carrera():
    ...


'''Fin seccion carreas'''


'''Seccion materias'''


@wrapper_insert(table_name='materias')
def insert_materia(codigo_materia,nombre,creditos):
    return { 'field_values': {'codigo_materia':codigo_materia,'nombre': nombre,'creditos':creditos}}


@wrapper_query_all("codigo_materia","nombre", "creditos",table_name='materias')
def consulta_general_materia():
    ...


'''Fin seccion materias'''


'''Seccion alumnos_materias'''


@wrapper_insert(table_name='alumnos_materias')
def insert_alumno_materia(codigo_materia,nrocontrol):
    return { 'field_values': {'nrocontrol':nrocontrol,'codigo_materia': codigo_materia}}


@wrapper_query_all("nrocontrol","codigo_materia", "calificacion","oportunidad","asesoria",table_name='alumnos_materias')
def consulta_general_alumno_materia():
    ...


'''Fin seccion alumnos_materias'''


'''Seccion grupo_tutores'''


@wrapper_insert(table_name='grupo_tutores')
def insert_grupo_docente(idgrupo,nrocontrol,cicloescolar):
    return { 'field_values': {'nrocontrol':nrocontrol,'idgrupo': idgrupo,'cicloescolar':cicloescolar}}


@wrapper_query_all("nrocontrol","idgrupo", "cicloescolar",table_name='grupo_tutores')
def consulta_general_grupo_docente():
    ...


'''Fin seccion grupo_tutores'''


def close():
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
