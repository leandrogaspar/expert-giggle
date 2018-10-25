from flask import Flask
from pymongo import MongoClient
from pymongo import DESCENDING
from datetime import datetime
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient('localhost', 27017)

db = client.leandro
estudantes = db.estudantes

"""
1. Listar todos os itens de uma modalidade em um período ordenados por data
    a. Tipo da requisição: GET
    b. Parâmetros: modalidade, data de início e data de fim
    c. Retorno: lista de todos os itens com modalidade, filtrando pelo período
    passado e ordenando de forma decrescente pela data dos
    documentos.
"""
@app.route("/1")
def modalidade():
    modalidade = 'PRESENCIAL'
    data_inicio = convertDate('2014-05-02')
    data_fim = convertDate('2015-05-02')

    match = estudantes.find({"modalidade": modalidade, "data_inicio": { "$gte": data_inicio, "$lte": data_fim }}).sort('data_inicio', DESCENDING)

    return dumps(match)

"""
2. Listar todos os cursos de um campus
    a. Tipo da requisição: GET
    b. Parâmetros: campus
    c. Retorno: lista de cursos do campus
"""
@app.route("/2")
def cursos():
    campus = 'AQ'

    match = estudantes.find({"campus": campus}).distinct("curso")
    print(match)

    return dumps(match)

"""
3. Número total de alunos numa campos em um período
    a. Tipo de requisição: GET
    b. Parâmetros: campus, data de início e data de fim
    c. Retorno: Número de alunos do campus no período
"""
@app.route("/3")
def alunos():
    campus = 'AQ'
    data_inicio = convertDate('2014-05-02')
    data_fim = convertDate('2015-05-02')

    match = estudantes.find({"campus": campus , "data_inicio": { "$gte": data_inicio, "$lte": data_fim }}).count()
    print(match)

    return dumps(match)

def convertDate(dateString):
    return datetime.strptime(dateString, '%Y-%m-%d')