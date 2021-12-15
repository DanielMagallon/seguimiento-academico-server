import psycopg2
import traceback
from flask import Flask
import json
from config import *
from psycopg2 import Error
from flask_cors import CORS
from psycopg2.extensions import cursor as cur

try:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_JWT
    CORS(app)
    connection = psycopg2.connect(user='postgres', password='psql', host='127.0.0.1',
                                  database='seguimiento_academico')

    cursor: cur = connection.cursor()
    print(f"PostgreSQL server information, cursor type: {type(cursor)}")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def wrapper_custom_query(*args, **kwargs):
    def decorator(func):
        def wrapper(*wargs, **wkwargs):
            data_func = func(*wargs, **wkwargs)
            if args:
                args2 = ['{}.{}'.format(kwargs["table_name"], a) for a in args]
                fields = str(args2).replace("[", "").replace("]", "").replace("'", "")

            if kwargs.get('custom_select'):
                select_args = str(kwargs['custom_select']).replace("[", "").replace("]", "").replace("'", "")
                if args:
                    select = f"SELECT {fields},{select_args} FROM {kwargs['table_name']}"
                else:
                    select = f"SELECT {select_args} FROM {kwargs['table_name']}"
            else:
                select = f"SELECT {fields} FROM {kwargs['table_name']}"

            if kwargs.get('innerjoin') and kwargs.get('on'):
                onq = kwargs['on']
                index = 0
                joinquery = ''
                for injoin in kwargs['innerjoin']:
                    on1 = onq[index]
                    index += 1
                    on2 = onq[index]
                    index += 1
                    joinquery += f' inner join {injoin} on {on1}={on2}'

                query = select + joinquery
            else:
                query = select

            if data_func.get('where'):
                query += " where " + data_func['where']

            cursor.execute(query)
            record = cursor.fetchall()
            if data_func.get(TABLE_FIELDS):
                dic: dict = {'fields': data_func[TABLE_FIELDS], 'values': record}
                return json.dumps(dic)
            else:
                return record

        return wrapper

    return decorator


def wrapper_query_all(*args, **kwargs):
    def decorator(func):
        def wrapper(*wargs, **wkwargs):
            data_func: dict = func(*wargs, **wkwargs)
            query = f'SELECT * FROM {kwargs["table_name"]}'
            cursor.execute(query)
            record = cursor.fetchall()

            dic = {'fields': data_func[TABLE_FIELDS], 'values': record}

            return json.dumps(dic)

        return wrapper

    return decorator


def wrapper_insert(*args, **kwargs):
    def decorator(function):
        def wrapper(*arg2, **kwargs2):
            data: dict = function(*arg2, **kwargs2)

            fields = str(list(data['field_values'].keys())).replace("[", "(").replace("]", ")").replace("'", "")
            values = str(list(data['field_values'].values())).replace("[", "(").replace("]", ")")
            query = f'INSERT INTO {kwargs["table_name"]} {fields} VALUES {values}'
            print(f"Insert into {query}")
            try:
                cursor.execute(query)
                dic = {'status': 0, 'title': f'Tabla "{kwargs["table_name"]}" actualizada',
                       'msg': 'Registro ingresado correctamente'}

            except Exception as ex:
                dic = {'status': -1, 'title': f'Error al registar en  {kwargs["table_name"]}',
                       'msg': repr(ex)}

            connection.commit()
            return json.dumps(dic)

        return wrapper

    return decorator


def wrapper_update(*args, **kwargs):
    def decorator(function):
        def wrapper(*arg2, **kwargs2):
            data: dict = function(*arg2, **kwargs2)

            query = f'UPDATE {kwargs["table_name"]} set {data["field_values"]} where {data["where"]}'
            print(f"updating {query}")
            try:
                cursor.execute(query)
                dic = {'status': 0, 'title': f'Tabla "{kwargs["table_name"]}" actualizada',
                       'msg': 'Registro actualizado correctamente'}

            except Exception as ex:
                dic = {'status': -1, 'title': f'Error al actualizar en  {kwargs["table_name"]}',
                       'msg': repr(ex)}

            connection.commit()
            return json.dumps(dic)

        return wrapper

    return decorator


def wrapper_call_funcproc(*args, **kwargs):
    def decorator(function):
        def wrapper(*args2, **kwargs2):
            try:
                data_func = function(*args2, **kwargs2)
                params: [] = data_func[PARAMS]
                if kwargs.get('type',None) == 'procedure':
                    cursor.execute(f"CALL {kwargs[FUNC_NAME]}{data_func[PROC_PARAMS]};", data_func[PROC_VALUES])
                else:
                    cursor.callproc(kwargs[FUNC_NAME], params)
                    result = cursor.fetchall()
                    print(f"Result: {result}")
                    cursor.execute(f'FETCH ALL IN "{result[0][0]}"')

                result = cursor.fetchall()
                connection.commit()

                if result:
                    dic = {'status': 0,'fields': data_func[TABLE_FIELDS], 'values': result}
                    return json.dumps(dic)
                else:
                    return json.dumps({'status': -1, 'error': kwargs[ERROR_FUN_MSG]})
            except Exception as e:
                print(f"{repr(e)} \n \t {e}")
                tb = traceback.format_exc()
                print(tb)
                connection.commit()
                return json.dumps({'status': -1, 'error': "Error en el servidor"})

        return wrapper

    return decorator


def close():
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
