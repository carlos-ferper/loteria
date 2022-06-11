
from sqlalchemy import create_engine, Column, String, Integer, Date, TIMESTAMP, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from tools import *
from datetime import datetime, timedelta
import secrets

Base = declarative_base()


class DefaultValues(Base):
    __tablename__ = 'default_values'

    id = Column(Integer, primary_key=True, autoincrement=True)
    propriedade = Column(String(128))
    tipo_dado = Column(String(128))
    valor = Column(String(128))

    def __init__(self, propriedade: str, tipo_dado: str, valor: str):
        self.propriedade = propriedade
        self.tipo_dado = tipo_dado
        self.valor = valor


class NivelUsuario(Base):
    __tablename__ = 'nivel_usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(128))

    def __init__(self, descricao: str):
        self.descricao = descricao


class User(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nivel_usuario = Column(Integer, ForeignKey('nivel_usuario.id'))
    name = Column(String(128))
    cpf = Column(String(128))
    email = Column(String(128))
    password = Column(String(128))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    saldo = Column(Float)

    def __init__(self, name: str, cpf: int, email: str, password: str, nivel_usuario: int):
        self.nivel_usuario = nivel_usuario
        self.name = name
        self.cpf = cpf
        self.email = email
        hashed = encriptar(password)
        self.password = hashed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.saldo = 0


class Sessao(Base):
    __tablename__ = 'sessao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(Integer, ForeignKey('usuario.id'))
    token = Column(String(128))
    created_at = Column(TIMESTAMP)
    expire_at = Column(TIMESTAMP)

    def __init__(self, usuario: User, duracao):
        self.usuario = usuario.id
        self.created_at = datetime.now()
        self.expire_at = self.created_at + timedelta(seconds=duracao)
        self.token = secrets.token_hex(20)


class TipoSorteio(Base):
    __tablename__ = 'tipo_sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(128))

    def __init__(self, descricao: str):
        self.descricao = descricao


class StatusSorteio(Base):
    __tablename__ = 'status_sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(128))

    def __init__(self, status: str):
        self.status = status


class Sorteio(Base):
    __tablename__ = 'sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_sorteio = Column(Integer, ForeignKey('tipo_sorteio.id'))
    data_sorteio = Column(TIMESTAMP)
    inicio_vendas = Column(TIMESTAMP)
    fim_vendas = Column(TIMESTAMP)
    quantidade_ingressos = Column(Integer)
    ingressos_por_usuario = Column(Integer)
    preco_ingresso = Column(Float)
    premio = Column(Float)
    status = Column(Integer)

    def __init__(self, tipo_sorteio: int, data_sorteio: datetime,
                 inicio_vendas: datetime, fim_vendas: datetime,
                 quantidade_ingressos: int, preco_ingresso: float,
                 ingressos_por_usuario: int, premio: float = 0):
        self.tipo_sorteio = tipo_sorteio
        self.data_sorteio = data_sorteio
        self.inicio_vendas = inicio_vendas
        self.fim_vendas = fim_vendas
        self.quantidade_ingressos = quantidade_ingressos
        self.ingressos_por_usuario = ingressos_por_usuario
        self.preco_ingresso = preco_ingresso
        self.premio = premio
        self.status = 1

    def dicionario_resultado(self):
        dicionario = {
            "id": self.id,
            "tipo_sorteio": self.tipo_sorteio,
            "data_sorteio": self.data_sorteio,
            "inicio_vendas": self.inicio_vendas,
            "fim_vendas": self.fim_vendas,
            "quantidade_ingressos": self.quantidade_ingressos,
            "ingressos_por_usuario": self.ingressos_por_usuario,
            "preco_ingresso": self.preco_ingresso,
            "premio": self.premio,
            "status": self.status
        }

        return dicionario


class StatusIngresso(Base):
    __tablename__ = 'status_ingresso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(128))

    def __init__(self, status: str):
        self.status = status


class Ingresso(Base):
    __tablename__ = 'ingresso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sorteio = Column(Integer, ForeignKey('sorteio.id'))
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    status_ingresso = Column(Integer, ForeignKey('status_ingresso.id'))
    token_ingresso = Column(String(128))

    def __init__(self, id_sorteio: int, id_usuario: int):
        self.id_sorteio = id_sorteio
        self.id_usuario = id_usuario
        self.status_ingresso = 1
        self.token_ingresso = secrets.token_hex(20)

    def dicionario_resultado(self):
        dicionario = {
            "id": self.id,
            "id_sorteio": self.id_sorteio,
            "status_ingresso": self.status_ingresso,
            "token_ingresso": self.token_ingresso
        }

        return dicionario
