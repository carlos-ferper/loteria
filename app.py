#!/usr/bin/env python

from flask import Flask, request, jsonify
from controls.control_usuarios import *
from controls.control_sorteio import *
from controls.control_ingresso import *

app = Flask(__name__)

if __name__ == "__main__":
    app.run(threaded=True, debug=False, use_evalex=False)


@app.route('/')
def hello_world():
    print('cheguei')
    return 'This is my first API call!'


@app.route('/criar_usuario', methods=['POST'])
def teste():
    input_json = request.get_json(force=True)
    dicionario = {
        'nome': input_json['nome'],
        'email': input_json['email'],
        'cpf': input_json['cpf'],
        'senha': input_json['senha'],
    }
    criar = ControlUsuario.cadastrar_cliente(dicionario)

    if criar:
        return "Usuario criado com sucesso!"
    return "falha ao criar o usuario!"


@app.route('/login', methods=['POST'])
def login():
    input_json = request.get_json(force=True)

    criar = ControlUsuario.login(input_json)

    if criar:
        return criar
    return "falha ao logar"


@app.route('/token', methods=['POST'])
def validar_token():
    input_json = request.get_json(force=True)

    criar = ControlUsuario.validar_token(input_json)

    if criar:
        return str(criar)
    return "falha ao logar"


@app.route('/aumentar_saldo', methods=['POST'])
def aumentar_saldo():
    input_json = request.get_json(force=True)

    criar = ControlUsuario.aumentar_saldo(input_json)

    if criar:
        return 'Saldo aumentado!'
    return "nao aumentamos o saldo"


@app.route('/criar_sorteio', methods=['POST'])
def criar_sorteio():
    input_json = request.get_json(force=True)

    status, mensagem = ControlSorteio.criar_sorteio(input_json)
    resposta = {
        'status': str(status),
        'resposta': mensagem
    }
    return resposta


@app.route('/comprar_ingresso', methods=['POST'])
def comprar_ingresso():
    input_json = request.get_json(force=True)

    status, mensagem = ControlIngresso.comprar_ingresso(input_json)
    resposta = {
        'status': str(status),
        'resposta': mensagem
    }
    return resposta


@app.route('/sortear', methods=['POST'])
def sortear():
    input_json = request.get_json(force=True)

    status, mensagem = ControlSorteio.sortear(input_json)

    resposta = {
        'status': str(status),
        'resposta': mensagem
    }
    return resposta


@app.route('/listar_sorteios', methods=['POST'])
def listar_sorteios():
    input_json = request.get_json(force=True)

    status, lista = ControlSorteio.listar_sorteios(input_json)

    if isinstance(lista, list):
        resposta = {
            'status': str(status),
            'items': lista
        }
    else:
        resposta = {
            'status': str(status),
            'mensagem': lista
        }
    return resposta


@app.route('/listar_ingressos_do_usuario', methods=['POST'])
def listar_ingressos():
    input_json = request.get_json(force=True)

    status, lista = ControlIngresso.listar_ingressos(input_json)

    if isinstance(lista, list):
        resposta = {
            'status': str(status),
            'items': lista
        }
    else:
        resposta = {
            'status': str(status),
            'mensagem': lista
        }
    return resposta
