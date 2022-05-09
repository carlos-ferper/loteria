from sqlalchemy import create_engine, Column, String, Integer, Date, TIMESTAMP, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
from datetime import datetime, timedelta

Base = declarative_base()


class DefaultValues(Base):
    __tablename__ = 'default_values'

    propriedade = Column(String, primary_key=True)
    tipo_dado = Column(String)
    valor = Column(String)

    def __init__(self, propriedade: str, tipo_dado: str, valor: str):
        self.propriedade = propriedade
        self.tipo_dado = tipo_dado
        self.valor = valor


class NivelUsuario(Base):
    __tablename__ = 'nivel_usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String)

    def __init__(self, descricao: str):
        self.descricao = descricao


class User(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nivel_usuario = Column(Integer, ForeignKey('nivel_usuario.id'))
    name = Column(String)
    cpf = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    saldo = Column(Float)

    def __init__(self, name: str, cpf: int, email: str, password: str, nivel_usuario: int):
        self.nivel_usuario = nivel_usuario
        self.name = name
        self.cpf = cpf
        self.email = email
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
        self.password = hashed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.saldo = 0


class TipoSorteio(Base):
    __tablename__ = 'tipo_sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String)

    def __init__(self, descricao: str):
        self.descricao = descricao


class StatusSorteio(Base):
    __tablename__ = 'status_sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)

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

    def __init__(self, tipo_sorteio: int,  data_sorteio: datetime, inicio_vendas: datetime, fim_vendas: datetime,
                 quantidade_ingressos: int, preco_ingresso: float, status: int,
                 ingressos_por_usuario: int = 1, premio: float = None):
        self.tipo_sorteio = tipo_sorteio
        self.data_sorteio = data_sorteio
        self.inicio_vendas = inicio_vendas
        self.fim_vendas = fim_vendas
        self.quantidade_ingressos = quantidade_ingressos
        self.ingressos_por_usuario = ingressos_por_usuario
        self.preco_ingresso = preco_ingresso
        self.premio = premio
        self.status = status


class StatusIngresso(Base):
    __tablename__ = 'status_sorteio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)

    def __init__(self, status: str):
        self.status = status


class Ingresso(Base):
    __tablename__ = 'ingresso'

    id_sorteio = Column(Integer, ForeignKey('sorteio.id'))
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    status_ingresso = Column(Integer)

    def __init__(self, id_sorteio: int, id_usuario: int, status_ingresso: int):
        self.id_sorteio = id_sorteio
        self.id_usuario = id_usuario
        self.status_ingresso = status_ingresso

