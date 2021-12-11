from src import Response,request,app,cross_origin,json,consulta_general_grupos,insert_grupo


@app.route('/grupos/consulta/all', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def grupos_consulta_all():
    return Response(consulta_general_grupos())


@app.route('/grupos/registro', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def grupos_registro():
    data = request.get_json()
    nombre = data['nombre']
    nrocontrol_tutor: data['nrocontrol_tutor']
    cicloescolar: data['cicloescolar']
    idcarrera: data['idcarrera']
    return Response(insert_grupo(nombre=nombre, nrocontrol_tutor=nrocontrol_tutor, cicloescolar=cicloescolar,
                                 idcarrera=idcarrera))


@app.route('/grupos/multiregistro', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def grupos_multiregistro():
    data = request.get_json()
    promises = {"ok": [], "error": []}

    for json_row in data:
        nombre = json_row['nombre']
        nrocontrol_tutor = json_row['nrocontrol_tutor']
        cicloescolar = json_row['cicloescolar']
        idcarrera = json_row['idcarrera']

        result = insert_grupo(nombre=nombre, nrocontrol_tutor=nrocontrol_tutor, cicloescolar=cicloescolar,
                              idcarrera=idcarrera)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))
