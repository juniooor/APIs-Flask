from typing import Optional
from itertools import count
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import Query, TinyDB


server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Aprendendo python')
spec.register(server)
database = TinyDB('database.json')
c = count()

class QueryPessoa(BaseModel):
    id: Optional[int]
    nome: Optional[str]
    idade: Optional[int]



class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory= lambda: next(c))
    nome: str
    idade: int


class Pessoas(BaseModel):

    pessoas: list[Pessoa]
    count: int


@server.get('/pessoas')
@spec.validate(query = QueryPessoa, resp=Response(HTTP_200=Pessoas))
def pegar_pessoa():
    """Retorna todas as pessoas da base de dados. informando quantidade e os dados """
    query = request.context.query.dict(exclude_none=True)
    allguys = database.search(Query().fragment(query))
    return jsonify(Pessoas(pessoas = allguys, count = len(allguys)).dict())



@server.get('/pessoas/<int:id>')
@spec.validate(resp=Response(HTTP_200=Pessoa))
def pegar_pessoas(id):
    """Retorna todas as pessoas da base de dados. informando quantidade e os dados """
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Pessoa not found! ela foi sequestrada'},404
    return jsonify(pessoa)


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_pessoa():
    """inserir Pessoa no Banco de Dados."""
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/pessoas/<int:id>')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def altera_pessoa(id):
    """Alterar os dados da Pessoa no banco de dados"""
    Pessoa = Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id == id)
    return jsonify(body)


@server.delete('/pessoas/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def delete_pessoa(id):
    """Remove pessoa pelo ID do banco de dados"""
    Pessoa = Query()
    database.remove(Pessoa.id == id)
    return jsonify({})


if __name__ == '__main__':
    server.run(debug=True)
    print('tô aqui')