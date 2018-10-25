from flask import Flask, jsonify, abort, request, Response
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from bson.json_util import dumps

# Maybe put this in env var? Nah... :)
MONGOHOST = "localhost"
MONGOPORT = 27017
API = "/v0"

app = Flask(__name__)

client = MongoClient(MONGOHOST, MONGOPORT)
db = client.leandro
studentCollection = db.estudantes


@app.after_request
def response_headers(response):
    response.headers["Content-Type"] = "application/json"
    return response


"""
1. Listar todos os itens de uma modalidade em um período ordenados por data
    a. Tipo da requisição: GET
    b. Parâmetros: modalidade, data de início e data de fim
    c. Retorno: lista de todos os itens com modalidade, filtrando pelo período
    passado e ordenando de forma decrescente pela data dos
    documentos.
"""


@app.route(API + "/students", methods=['GET'])
def students():
    # Retrieve the query args
    modality = get_query_arg(request, "modality")
    start_date = get_query_arg(request, "start_date")
    end_date = get_query_arg(request, "end_date")

    # Validate the dates
    try:
        start = convert_date(start_date)
        end = convert_date(end_date)
    except ValueError:
        abort(400, description="Date must be in format YYYY-MM-DD")

    # Perform the mongodb query
    matches = studentCollection\
        .find({"modalidade": modality, "data_inicio": {"$gte": start, "$lte": end}})\
        .sort("data_inicio", DESCENDING)

    # Send our response
    resp = []
    for match in matches:
        student = student_from_mongo(match)
        resp.append(student)

    return dumps(resp)


"""
2. Listar todos os cursos de um campus
    a. Tipo da requisição: GET
    b. Parâmetros: campus
    c. Retorno: lista de cursos do campus
"""


@app.route(API + "/campus-courses", methods=['GET'])
def campus_courses():
    # Retrieve the query args
    campus = get_query_arg(request, "campus")

    # Perform the mongodb query
    matches = studentCollection.find({"campus": campus}).distinct("curso")

    # Send our response
    resp = {
        "campus_courses": matches
    }
    return dumps(resp)


"""
3. Número total de alunos numa campos em um período
    a. Tipo de requisição: GET
    b. Parâmetros: campus, data de início e data de fim
    c. Retorno: Número de alunos do campus no período
"""


@app.route(API + "/students-count", methods=['GET'])
def students_acount():
    # Retrieve the query args
    campus = get_query_arg(request, "campus")
    start_date = get_query_arg(request, "start_date")
    end_date = get_query_arg(request, "end_date")

    # Validate the dates
    try:
        start = convert_date(start_date)
        end = convert_date(end_date)
    except ValueError:
        abort(400, description="Date must be in format YYYY-MM-DD")

    # Perform the mongodb query
    matches = studentCollection.find({"campus": campus, "data_inicio": {
                                     "$gte": start_date, "$lte": end_date}}).count()

    # Send our response
    resp = {
        "count": matches
    }
    return dumps(resp)


"""
1. Cadastro de alunos
    a. Tipo da requisição: POST
    b. Payload deve conter os seguintes campos:
    (nome, idade_ate_31_12_2016, ra, campus,municipio, curso
    modalidade, nivel_do_curso, data_inicio)
    c. Retorno: mesmo payload do envio com status 201
"""


@app.route(API + "/new-student", methods=['POST'])
def new_student():
    # Retrieve the payload args
    nome = get_body_arg(request, "nome")
    idade_ate_31_12_2016 = get_body_arg(request, "idade_ate_31_12_2016")
    ra = get_body_arg(request, "ra")
    campus = get_body_arg(request, "campus")
    municipio = get_body_arg(request, "municipio")
    curso = get_body_arg(request, "curso")
    modalidade = get_body_arg(request, "modalidade")
    nivel_do_curso = get_body_arg(request, "nivel_do_curso")
    data_inicio = get_body_arg(request, "data_inicio")

    student = {
        "ra": ra,
        "nivel_do_curso": nivel_do_curso,
        "modalidade": modalidade,
        "idade_ate_31_12_2016": idade_ate_31_12_2016,
        "nome": nome,
        "campus": campus,
        "curso": curso,
        "data_inicio": datetime.strptime(data_inicio, '%Y-%m-%d'),
        "municipio": municipio
    }

    # Perform the mongodb query
    result = studentCollection.insert_one(student)

    # Send our response
    return Response(dumps(student_from_mongo(student)), status=201)


"""
2. Remoção de alunos do banco pelo RA
    a. Tipo da requisição: DELETE
    b. Parâmetros: ra, campus
    c. Retorno: status 200
"""


@app.route(API + "/delete-student", methods=['DELETE'])
def delete_student():
    # Retrieve the payload args
    ra = get_body_arg(request, "ra")
    campus = get_body_arg(request, "campus")

    # Perform the mongodb deletion
    studentCollection.delete_one({"ra": ra, "campus": campus})
    return ''


@app.errorhandler(400)
def invalidQuery(error):
    response = jsonify({"message": error.description})
    return response


def convert_date(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d")


def get_query_arg(request, arg):
    receivedArg = request.args.get(arg)
    if receivedArg == None:
        abort(400, description="Missing mandatory query arg")
    return receivedArg


def get_body_arg(request, arg):
    if not request.json or not arg in request.json:
        abort(400, description="Missing mandatory field on payload")
    return request.json[arg]


def student_from_mongo(mongoObject):
    student = {
        "id": str(mongoObject["_id"]),
        "data_inicio": mongoObject["data_inicio"].strftime("%Y-%m-%d"),
        "nome": mongoObject["nome"],
        "curso": mongoObject["curso"],
        "ra": mongoObject["ra"],
        "modalidade": mongoObject["modalidade"],
        "idade_ate_31_12_2016": mongoObject["idade_ate_31_12_2016"],
        "nivel_do_curso": mongoObject["nivel_do_curso"],
        "municipio": mongoObject["municipio"],
        "campus": mongoObject["campus"]
    }
    return student
