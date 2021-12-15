from src import Response,request,app,consulta_tutores,cross_origin,\
                    insert_tutor,json,consulta_pagina_tutores,session_tutor

from src.config import SECRET_JWT,TIMEOUT_JWT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@app.route('/tutores/consulta/all', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def tutores_consulta_all():
    return Response(consulta_tutores())


@app.route("/tutores/registro", methods=["POST"])
def tutores_registro():
    data = request.get_json()
    nombre = data['nombre']
    apellido1 = data['apellido1']
    apellido2 = data['apellido2']
    idcarrera = data['idcarrera']
    nrocontrol = data['nrocontrol']
    password = data['clave']

    return Response(insert_tutor(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                                 nrocontrol=nrocontrol, idcarrera=idcarrera,password=password))


@app.route("/tutores/multiregistro", methods=["POST"])
def tutores_multiregistro():
    data = request.get_json()
    promises = {"ok":[],"error":[]}

    for json_row in data:
        nombre = json_row['nombre']
        apellido1 = json_row['apellido1']
        apellido2 = json_row['apellido2']
        idcarrera = json_row['idcarrera']
        nrocontrol = json_row['nrocontrol']

        result = insert_tutor(nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                                       nrocontrol=nrocontrol, idcarrera=idcarrera)

        promises["ok" if result['status'] == 0 else "error"].append(result)

    return Response(json.dumps(promises))


@app.route("/consulta-tutor",methods=["GET","POST"])
def consulta_tutor():
    data = request.get_json()
    nrocontrol_tutor = data['nrocontrol_tutor']
    return Response(consulta_pagina_tutores(nrocontrol_tutor))


@app.route("/tutor/login",methods=["POST"])
def tutor_login():
    data = request.get_json()
    nrocontrol = data['nrocontrol']
    password = data['clave']
    data = json.loads(session_tutor(nrocontrol,password))

    if data['status'] == 0:
        s = Serializer(SECRET_JWT,TIMEOUT_JWT)
        payload = {
            'idGrupo': data['values'][0],
        }
        data['jwt'] = s.dumps(payload).decode('utf-8')

    return Response(data)


@app.route("/tutor/validar-token",methods=["POST"])
def validar_token_tutor():
    data = request.get_json()
    jwt = data['jwt']
    s = Serializer(SECRET_JWT)
    response = {}

    try:
        response['idGrupo'] = s.loads(jwt)['idGrupo']
        response['status'] = 0
        response['msg'] = "Token valido"
    except:
        response = {'status':-1,'msg':'El token no es valido. Inicie sesion nuevamente por su seguridad'}

    return Response(json.loads(response))