import json

from src import *
from flask_cors import cross_origin
from flask import Response,request
'''
Seccion Grupos
'''


@app.route('/grupos/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def grupos_consulta_all():
    return Response(consulta_general_grupos())


@app.route('/grupos/registro', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def grupos_registro():
    data = request.get_json()
    nombre = data['nombre']
    return Response(insert_grupo(nombre))


@app.route('/grupos/multiregistro', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def grupos_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        nombre = json_row['nombre']
        promises[index]=insert_grupo(nombre)
        index+=1

    return Response(json.dumps(promises))

'''
Fin Seccion Grupos
'''


'''
Seccion Tutores
'''


@app.route('/tutores/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def tutores_consulta_all():
    return Response(consulta_general_tutor())


@app.route("/tutores/registro", methods=["POST"])
def tutores_registro():
    data = request.get_json()
    nombre = data['nombre']
    apellido1 = data['apellido1']
    apellido2 = data['apellido2']
    idcarrera = data['idcarrera']
    nrocontrol = data['nrocontrol']
    return Response(insert_tutor(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                        nrocontrol=nrocontrol,idcarrera=idcarrera))


@app.route("/tutores/multiregistro", methods=["POST"])
def tutores_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        nombre = json_row['nombre']
        apellido1 = json_row['apellido1']
        apellido2 = json_row['apellido2']
        idcarrera = json_row['idcarrera']
        nrocontrol = json_row['nrocontrol']
        promises[index]=insert_tutor(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                        nrocontrol=nrocontrol,idcarrera=idcarrera)
        index+=1

    return Response(json.dumps(promises))

'''
Fin Seccion Tutores
'''

'''
Seccion alumnos
'''


@app.route('/alumnos/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def alumnos_consulta_all():
    return Response(consulta_general_alumnos())


@app.route('/alumnos/registro', methods=['POST'])
def alumnos_registro():
    data = request.get_json()
    nombre = data['nombre']
    apellido1 = data['apellido1']
    apellido2 = data['apellido2']
    idgrupo = data['idgrupo']
    nrocontrol = data['nrocontrol']
    return Response(insert_alumno(nombre=nombre, apellido1=apellido1,apellido2=apellido2,
                         idgrupo=idgrupo, nrocontrol=nrocontrol))


@app.route('/alumnos/multiregistro', methods=['POST'])
def alumnos_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        nombre = json_row['nombre']
        apellido1 = json_row['apellido1']
        apellido2 = json_row['apellido2']
        idgrupo = json_row['idgrupo']
        nrocontrol = json_row['nrocontrol']
        promises[index]=insert_alumno(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                      idgrupo=idgrupo, nrocontrol=nrocontrol)
        index+=1

    return Response(json.dumps(promises))


'''
Fin Seccion alumnos
'''


'''
Seccion carreras
'''

@app.route('/carreras/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def carreras_consulta_all():
    return Response(consulta_general_carrera())


@app.route('/carreras/registro', methods=['POST'])
def carreras_registro():
    data = request.get_json()
    nombre = data['nombre']
    tipo = data['tipo']
    return Response(insert_carrera(nombre=nombre,tipo=tipo))


@app.route('/carreras/multiregistro', methods=['POST'])
def carreras_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        nombre = json_row['nombre']
        tipo = json_row['tipo']
        total_creditos = json_row['total_creditos']
        promises[index]=insert_carrera(nombre=nombre, tipo=tipo,total_creditos=total_creditos)
        index+=1

    return Response(json.dumps(promises))


'''
Fin seccion carreas
'''


'''
Seccion materias
'''


@app.route('/materias/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def materias_consulta_all():
    return Response(consulta_general_materia())


@app.route('/materias/registro', methods=['POST'])
def materias_registro():
    data = request.get_json()
    codigo_materia = data['codigo_materia']
    nombre = data['nombre']
    creditos = data['creditos']
    return Response(insert_materia(nombre=nombre,codigo_materia=codigo_materia,creditos=creditos))


@app.route('/materias/multiregistro', methods=['POST'])
def materias_multiregistro():
    data = request.get_json()
    promises = {}
    index=0
    for json_row in data:
        codigo_materia = json_row['codigo_materia']
        nombre = json_row['nombre']
        creditos = json_row['creditos']
        promises[index] = insert_materia(nombre=nombre,codigo_materia=codigo_materia,creditos=creditos)
        index+=1

    return Response(json.dumps(promises))

'''
Fin seccion materias
'''


'''
Seccion alumno-materias
'''


@app.route('/alumno-materias/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def materia_alumnos_consulta_all():
    return Response(consulta_general_alumno_materia())


@app.route('/alumno-materias/registro', methods=['POST'])
def materias_alumnos_registro():
    data = request.get_json()
    codigo_materia = data['codigo_materia']
    nrocontrol = data['nrocontrol']
    return Response(insert_alumno_materia(codigo_materia=codigo_materia,nrocontrol=nrocontrol))


@app.route('/alumno-materias/multiregistro', methods=['POST'])
def materias_alumnos_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        codigo_materia = json_row['codigo_materia']
        nrocontrol = json_row['nrocontrol']
        promises[index]=insert_alumno_materia(codigo_materia=codigo_materia, nrocontrol=nrocontrol)
        index+=1

    return Response(json.dumps(promises))


'''
Fin seccion alumno-materias
'''


'''
Seccion grupo_tutores
'''


@app.route('/grupo-tutores/consulta/all', methods=['POST','GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def grupo_tutores_consulta_all():
    return Response(consulta_general_grupo_docente())


@app.route('/grupo-tutores/registro', methods=['POST'])
def grupo_tutores_registro():
    data = request.get_json()
    idgrupo = data['idgrupo']
    nrocontrol = data['nrocontrol']
    cicloescolar = data['cicloescolar']
    return Response(insert_grupo_docente(idgrupo=idgrupo,nrocontrol=nrocontrol,cicloescolar=cicloescolar))


@app.route('/grupo-tutores/multiregistro', methods=['POST'])
def grupo_tutores_multiregistro():
    data = request.get_json()
    promises = {}
    index = 0
    for json_row in data:
        idgrupo = json_row['idgrupo']
        nrocontrol = json_row['nrocontrol']
        cicloescolar = json_row['cicloescolar']
        promises[index] = insert_grupo_docente(idgrupo=idgrupo, nrocontrol=nrocontrol, cicloescolar=cicloescolar)
        index+=1

    return Response(json.dumps(promises))


'''
Fin seccion grupo-tutores
'''

if __name__ == '__main__':
    print("Running flask server")
    # host_vb='192.168.122.1'
    # host_wl = '192.168.1.71'
    global_host = '0.0.0.0'
    app.run(debug=True, port='5800', host=global_host)
