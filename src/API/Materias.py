from src import app,json,cross_origin,Response,request,insert_materia,consulta_general_materia,\
    consulta_materia_xnombre


@app.route('/materias/consulta/all', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def materias_consulta_all():
    return Response(consulta_general_materia())


@app.route('/materias/registro', methods=['POST'])
def materias_registro():
    data = request.get_json()
    codigo_materia = data['codigo_materia']
    nombre = data['nombre']
    creditos = data['creditos']
    return Response(insert_materia(nombre=nombre, codigo_materia=codigo_materia, creditos=creditos))


@app.route('/materias/multiregistro', methods=['POST'])
def materias_multiregistro():
    data = request.get_json()
    promises = {"ok":[],"error":[]}

    for json_row in data:
        codigo_materia = json_row['codigo_materia']
        nombre = json_row['nombre']
        creditos = json_row['creditos']

        result = insert_materia(nombre=nombre, codigo_materia=codigo_materia, creditos=creditos)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))


@app.route('/materias/consulta/bynombre', methods=['POST'])
def codigo_materia():
    data = request.get_json()
    nombre = data['nombre']
    res = consulta_materia_xnombre(nombre)
    print(res)
    return Response(res)