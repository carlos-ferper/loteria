from tools import *
from dbaccess import dba
from model import *


class ControlUsuario:

    @staticmethod
    def validar_credenciais(email, senha):
        resultado = list(dba.session.query(User).filter(User.email == email))
        mensagem = 'Conta não encontrada'
        if len(resultado) > 0:
            resultado = resultado[0]
            print(decriptar(resultado.password))
            if decriptar(resultado.password).decode('utf-8') == senha:
                return True, resultado
            mensagem = 'Senha inválida'

        return False, mensagem

    @staticmethod
    def login(dicionario: dict):
        email = dicionario['email']
        senha = dicionario['senha']

        resultado, dados = ControlUsuario.validar_credenciais(email, senha)

        if resultado:
            sessao = Sessao(dados, 500)
            dba.insertorm(sessao)
            dba.commit()
            return sessao.token
        return False

    @staticmethod
    def validar_token(dicionario: dict):
        token = dicionario['token']
        filtros = [
            Sessao.token == token,
            Sessao.expire_at >= datetime.now()
        ]

        resultado = list(dba.session.query(User).join(Sessao, Sessao.usuario == User.id).filter(*filtros))
        if len(resultado) > 0:
            return resultado[0].id
        return False

    @staticmethod
    def get_usuario(id: int):

        resultado = list(dba.session.query(User).filter(User.id == id))

        if len(resultado) > 0:
            return resultado[0]
        return False

    @staticmethod
    def cadastrar_cliente(dicionario: dict):
        nome = dicionario['nome']
        email = dicionario['email']
        cpf = dicionario['cpf']
        senha = dicionario['senha']
        verificar_email, _ = ControlUsuario.validar_credenciais(email, senha)

        if not verificar_email:
            usuario = User(nome, cpf, email, senha, 1)
            dba.insertorm(usuario)
            dba.commit()
            return True
        return False

    @staticmethod
    def get_usuario_by_token(token: str):
        filtros = [
            Sessao.token == token,
            Sessao.expire_at >= datetime.now()
        ]
        resultado = list(dba.session.query(User).join(Sessao, Sessao.usuario == User.id).filter(*filtros))
        if len(resultado) > 0:
            return resultado[0]
        return False

    @staticmethod
    def aumentar_saldo(dicionario: dict):
        token = dicionario['token']
        valor_adicional = float(dicionario['valor'])
        validacao_token = ControlUsuario.validar_token({'token': token})
        if validacao_token:
            usuario = ControlUsuario.get_usuario(validacao_token)
            usuario.saldo += valor_adicional
            dba.insertorm(usuario)
            dba.commit()
            return True
        return False

    @staticmethod
    def premiar_usuario(id: int, premio: float):
        usuario = ControlUsuario.get_usuario(id)
        usuario.saldo += premio
        dba.insertorm(usuario)
        dba.commit()