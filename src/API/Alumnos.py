from src import Response,request,app,session_alumno,json,\
                consulta_general_alumnos,cross_origin,insert_alumno,update_data_alumno,consulta_pagina_tutores


@app.route('/alumnos/consulta/bygrupo', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def alumnos_consulta_all():
    data = request.get_json()
    idgrupo = data['idgrupo']
    return Response(consulta_general_alumnos(idgrupo))


@app.route('/alumnos/registro', methods=['POST'])
def alumnos_registro():
    data = request.get_json()
    nombre = data['nombre']
    apellido1 = data['apellido1']
    apellido2 = data['apellido2']
    idgrupo = data['idgrupo']
    nrocontrol = data['nrocontrol']
    return Response(insert_alumno(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                                  idgrupo=idgrupo, nrocontrol=nrocontrol))


@app.route('/alumnos/multiregistro', methods=['POST'])
def alumnos_multiregistro():
    data = request.get_json()
    promises = {"ok":[],"error":[]}

    for json_row in data:
        nombre = json_row['nombre']
        apellido1 = json_row['apellido1']
        apellido2 = json_row['apellido2']
        idgrupo = json_row['idgrupo']
        nrocontrol = json_row['nrocontrol']

        result = insert_alumno(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                                        idgrupo=idgrupo, nrocontrol=nrocontrol)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))


@app.route("/alumnos/login",methods=["POST"])
def alumnos_login():
    data = request.get_json()
    nrocontrol = data['nrocontrol']
    clave = data['clave']
    return Response(session_alumno(nrocontrol,clave))


@app.route("/alumno/update",methods=["GET","POST"])
def update_alumno():
    data = request.get_json()
    nrocontrol_al = data['nrocontrol_alumno']
    nrocontrol_tu = data['nrocontrol_tutor']
    codigo_materia = data['codigo_materia']
    calif = float(data['calificacion'])
    data = json.loads(update_data_alumno(nrocontrol_al,codigo_materia,calif))
    if data['status'] == 0:
        return Response(consulta_pagina_tutores(nrocontrol_tu,True,nrocontrol_al))
    else:
        return Response(data)