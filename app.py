import json
from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import Query, TinyDB



server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Aprendendo python')
spec.register(server)
database = TinyDB('database.json')


class Pessoa(BaseModel):
    id: Optional[int]
    nome: str
    idade: int


class Pessoas(BaseModel):

    pessoas: list[Pessoa]
    count: int



@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas))
def pegar_pessoas():
    """Retorna todas as pessoas da base de dados. informando quantidade e os dados """
    return jsonify(
        Pessoas(
            pessoas=database.all(),
            count=len(database.all())
        ).dict()
    )



@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_pessoa():
    """inserir Pessoa no Banco de Dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body


if __name__ == '__main__':
    server.run(debug=True)
    print('tô aqui')