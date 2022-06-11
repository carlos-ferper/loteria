import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import *

# PARAMETERS
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))


class DBAccess(object):
    # Construtor - abertura da conexao
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://" +
            config.get('db', 'local_user') + ":" +
            config.get('db', 'local_pass') + "@" +
            config.get('db', 'local_host') + ":3306/" +
            config.get('db', 'local_db_name'), pool_timeout=1000, encoding='latin1', echo=False)

        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        session = sessionmaker()
        session.configure(bind=self.engine, autoflush=False, autocommit=False)
        self.session = session()

    def createbase(self):
        Base.metadata.create_all(self.engine)

    def insertorm(self, obj):
        self.session.add(obj)

    def getsession(self):
        return self.session

    def getengine(self):
        return self.engine

    def commit(self):
        self.trans.commit()
        self.session.commit()
        self.trans = self.conn.begin()

    def rollback(self):
        self.session.rollback()
        self.trans.rollback()
        self.trans.rollback()
        self.trans = self.conn.begin()

    def close(self):
        self.trans.commit()
        self.session.commit()
        self.conn.close()
        self.session.close()

    def login(self, email, senha):
        resultado = self.session.query(User).filter(User.email == email).one()

        mensagem = 'Conta não encontrada'
        if resultado:
            hashed = bcrypt.hashpw(senha, bcrypt.gensalt(10))
            password = hashed
            if resultado.password == password:
                return True, resultado
            mensagem = 'Senha inválida'

        return False, mensagem

    def listar_sorteios(self, status: int = -1) -> list:
        if status != -1:
            filtros = [

                Sorteio.status == status

            ]

            return self.session.query(Sorteio).filter(filtros).all()
        return self.session.query(Sorteio).all()

    def usuario_by_token(self, token: str):

        filtros = [
            Sessao.token == token,
            Sessao.expire_at >= datetime.now()
        ]

        return self.session.query(User).join(Sessao, Sessao.usuario == User.id).filter(*filtros).one()

    def email_cadastrado(self, email: str):

        resultado = self.session.query(User).filter(User.email == email).one()

        return resultado is not None

    def listar_ingressos_usuario(self, usuario: User, status: int = -1):
        filtros = [

            Ingresso.id_usuario == usuario.id

        ]

        if status != -1:
            filtros.append(Ingresso.status_ingresso == status)

        return self.session.query(Ingresso).filter(filtros).all()

    def listar_ingressos_sorteio(self, sorteio: Sorteio, status: int = -1):
        filtros = [

            Ingresso.id_sorteio == sorteio.id

        ]

        if status != -1:
            filtros.append(Ingresso.status_ingresso == status)

        return self.session.query(Ingresso).filter(filtros).all()

    def achar_propriedade(self, propriedade: str):
        return self.session.query(DefaultValues).filter(DefaultValues.propriedade == propriedade).one()

dba = DBAccess()