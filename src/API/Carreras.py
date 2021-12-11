from src import app,cross_origin,json,Response,request,insert_carrera,consulta_general_carrera


@app.route('/carreras/consulta/all', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def carreras_consulta_all():
    return Response(consulta_general_carrera())


@app.route('/carreras/registro', methods=['POST'])
def carreras_registro():
    data = request.get_json()
    nombre = data['nombre']
    tipo = data['tipo']
    return Response(insert_carrera(nombre=nombre, tipo=tipo))


@app.route('/carreras/multiregistro', methods=['POST'])
def carreras_multiregistro():
    data = request.get_json()
    promises = {"ok":[],"error":[]}

    for json_row in data:
        nombre = json_row['nombre']
        tipo = json_row['tipo']
        total_creditos = json_row['total_creditos']

        result = insert_carrera(nombre=nombre, tipo=tipo, total_creditos=total_creditos)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))
