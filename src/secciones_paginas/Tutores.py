from src.Manager import wrapper_custom_query
from src.config import *
import json

@wrapper_custom_query("idgrupo","nombre","cicloescolar","idcarrera",table_name="grupos",
                      custom_select=["carreras.nombre","carreras.total_creditos"],
                      innerjoin=["carreras"],on=["carreras.idcarrera","grupos.idcarrera"])
def __extraer_grupo_tutor(nrocontrol_tutor):
    return {'where': f"nrocontrol_tutor='{nrocontrol_tutor}' and activo",
            TABLE_FIELDS:["Id grupo","Nombre","Ciclo escolar","Id carrera","Carrera","Creditos"]}




@wrapper_custom_query("nrocontrol","nombre","apellido1","apellido2",table_name="alumnos")
def __extraer_alumnos_grupo_tutor(idgrupo):
    return {'where': f"idgrupo={idgrupo}",
            TABLE_FIELDS: ["Nro Control", "Nombre", "Apellido 1","Apellido 2"]}


@wrapper_custom_query("calificacion","oportunidad","asesoria",
                      custom_select="materias.nombre",
                      table_name="alumnos_materias",innerjoin=["materias"],
                      on=["materias.codigo_materia","alumnos_materias.codigo_materia"])
def __extraer_info_alumno(nrocontrol_alumno):
    return {'where': f"nrocontrol='{nrocontrol_alumno}' and activo",
            TABLE_FIELDS: ["Calificacion", "Oportunidad", "Asesoria","Materia"]}


@wrapper_custom_query(table_name="alumnos",custom_select="count(1)")
def __count_alumnos_grupo(idgrupo):
    return {'where': f"idgrupo={idgrupo}"}


#  Puedria ser eliminado
# @wrapper_custom_query(table_name="alumnos_materias",custom_select="count(1)")
# def __count_materias_semestre(nrocontrol):
#     return {'where': f"nrocontrol='{nrocontrol}' adn activo"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="count(1)")
def __materias_escecial_sem(nrocontrol_alumno):
    return {'where': f"nrocontrol='{nrocontrol_alumno}' and oportunidad=3 and activo"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="count(1)")
def __total_materias_aprobadas(nrocontrol_alumno):
    return {'where': f"nrocontrol='{nrocontrol_alumno}' and calificacion>={CALIFICACION_APROBATORIA}"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="count(1)")
def __total_materias_aprobadas_semestre(nrocontrol_alumno,aprobadas):
    if aprobadas:
        return {'where': f"nrocontrol='{nrocontrol_alumno}' and calificacion>={CALIFICACION_APROBATORIA} and activo"}

    return {'where': f"nrocontrol='{nrocontrol_alumno}' and calificacion<{CALIFICACION_APROBATORIA} and activo"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="avg(calificacion)")
def __promedio_sem_actual(nrocontrol_alumno):
    return {'where': f"nrocontrol='{nrocontrol_alumno}' and activo"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="sum(materias.creditos)",
                      innerjoin=["materias"],on=["materias.codigo_materia","alumnos_materias.codigo_materia"])
def __creditos_aprobados_semestre(nrocontrol_alumno,aprobados=True):
    if aprobados:
        return {'where': f"nrocontrol='{nrocontrol_alumno}' and activo and calificacion>={CALIFICACION_APROBATORIA}"}

    return {'where': f"nrocontrol='{nrocontrol_alumno}' and activo and calificacion<{CALIFICACION_APROBATORIA}"}


@wrapper_custom_query(table_name="alumnos_materias",custom_select="sum(materias.creditos)",
                      innerjoin=["materias"],on=["materias.codigo_materia","alumnos_materias.codigo_materia"])
def __creditos_acumulados(nrocontrol_alumno):
    return {'where': f"nrocontrol='{nrocontrol_alumno}' and calificacion>={CALIFICACION_APROBATORIA}"}


@wrapper_custom_query(table_name="alumnos_materias",
                      custom_select="alumnos_materias.codigo_materia,materias.nombre,avg(calificacion)",
                      innerjoin=["alumnos","materias"],
                      on=["alumnos.nrocontrol","alumnos_materias.nrocontrol",
                          "materias.codigo_materia","alumnos_materias.codigo_materia"])
def __promedio_grupal_materias(idgrupo):
    return {TABLE_FIELDS: ["Codigo Materia","Materia","Promedio"],
        'where': f"alumnos.idgrupo={idgrupo} group by alumnos_materias.codigo_materia, materias.nombre"}


def consulta_pagina_tutores(nrocontrol_tutor):
    data = {}
    grupo_tutor = json.loads(__extraer_grupo_tutor(nrocontrol_tutor))
    data['Grupo Activo'] = grupo_tutor
    current_idgrupo = grupo_tutor['values'][0][0]
    cantidad_alumnos = __count_alumnos_grupo(current_idgrupo)[0][0]
    alumnos_grupo = json.loads(__extraer_alumnos_grupo_tutor(current_idgrupo))

    data['Alumnos Grupo'] = alumnos_grupo

    prom_grup_mat = json.loads(__promedio_grupal_materias(current_idgrupo))
    data['Promedios Materias Grupal'] = prom_grup_mat if prom_grup_mat is not None else 0

    # print(f"Paso 1: Grupo = {grupo_tutor}")
    # print(f"Paso 2: Grupo = {alumnos_grupo}")
    # print("Paso 3: Alumnos Info")

    alumnos_info = []
    alumnos_total_materias_reporte = {'Todas aprobadas':0}

    for alumno in alumnos_grupo['values']:

        #Extrae info del alumno dado (alumno[0]=nrocontrol)

        alinfo: dict = json.loads(__extraer_info_alumno(alumno[0]))
        alinfo['Nro Control'] = alumno[0]
        alinfo['Alumno'] = " ".join(alumno[1:])

        total_mat_apr = __total_materias_aprobadas(alumno[0])[0][0]
        alinfo['Total Materias Aprobadas']=total_mat_apr

        # Calcular la cantidad de materias tomadas por dicho alumno
        total_mat_apr = __total_materias_aprobadas_semestre(alumno[0],True)[0][0]
        alinfo['Total Mat. Aprobadas Semestre'] = total_mat_apr
        total_mat_repr = __total_materias_aprobadas_semestre(alumno[0], False)[0][0]
        alinfo['Total Mat. Reprobadas Semestre'] = total_mat_repr

        int_tmrep = int(total_mat_repr)
        if int_tmrep == 0:
            alumnos_total_materias_reporte['Todas aprobadas']+=1
        else:
            string = f"Alumnos con {int_tmrep} materia(s) en repetecion"
            if alumnos_total_materias_reporte.get(string):
                alumnos_total_materias_reporte[string]+=1
            else:
                alumnos_total_materias_reporte[string]=1

        alinfo['Situacion'] = "Irregular" if total_mat_repr else "Regular"

        prom_seme_actual = __promedio_sem_actual(alumno[0])[0][0]
        alinfo['Promedio Sem.'] = prom_seme_actual

        creditos_apr_sem = __creditos_aprobados_semestre(alumno[0])[0][0]
        creditos_repr_sem = __creditos_aprobados_semestre(alumno[0],False)[0][0]
        creditos_acumulados = __creditos_acumulados(alumno[0])[0][0]
        materias_especial_sem = __materias_escecial_sem(alumno[0])[0][0]

        alinfo['Creditos Acum.'] = creditos_acumulados if creditos_acumulados is not None  else 0
        alinfo['Creditos Apr. Semestre'] = creditos_apr_sem if creditos_apr_sem is not None  else 0
        alinfo['Creditos Repr. Semestre'] = creditos_repr_sem if creditos_repr_sem is not None  else 0
        alinfo['Especial'] = materias_especial_sem if materias_especial_sem is not None else 0
        alumnos_info.append(alinfo)

    data['Alumnos info'] =  alumnos_info

    data['Seguimiento Academico'] = {}
    data['Seguimiento Academico']['Cantidad Alumnos'] = cantidad_alumnos
    data['Seguimiento Academico']['Reporte']=alumnos_total_materias_reporte
    return json.dumps(data)