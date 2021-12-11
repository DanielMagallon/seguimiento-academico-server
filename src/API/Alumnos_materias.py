from src import app,cross_origin,Response,request,json,insert_alumno_materia


@app.route('/alumno-materias/consulta/all', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def materia_alumnos_consulta_all():
    return Response("")


@app.route('/alumno-materias/registro', methods=['POST'])
def materias_alumnos_registro():
    data = request.get_json()
    codigo_materia = data['codigo_materia']
    nrocontrol = data['nrocontrol']
    return Response(insert_alumno_materia(codigo_materia=codigo_materia, nrocontrol=nrocontrol))


@app.route('/alumnos_materias/multiregistro', methods=['POST'])
def materias_alumnos_multiregistro():
    data = request.get_json()
    promises = {"ok": [], "error": []}

    for json_row in data:
        codigo_materia = json_row['codigo_materia']
        nrocontrol = json_row['nrocontrol']

        result = insert_alumno_materia(codigo_materia=codigo_materia, nrocontrol=nrocontrol)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))