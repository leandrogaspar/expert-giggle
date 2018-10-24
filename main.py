from flask import Flask
app = Flask(__name__)

"""
1. Listar todos os itens de uma modalidade em um período ordenados por data
a. Tipo da requisição: GET
b. Parâmetros: modalidade, data de início e data de fim
c. Retorno: lista de todos os itens com modalidade, filtrando pelo período
passado e ordenando de forma decrescente pela data dos
documentos.
"""
@app.route("/")
def hello():
    return "Hello World!"

"""
2. Listar todos os cursos de um campus
a. Tipo da requisição: GET
  b. Parâmetros: campus
  c. Retorno: lista de cursos do campus
"""

"""
3. Número total de alunos numa campos em um período
  a. Tipo de requisição: GET
  b. Parâmetros: campus, data de início e data de fim
  c. Retorno: Número de alunos do campus no período
"""