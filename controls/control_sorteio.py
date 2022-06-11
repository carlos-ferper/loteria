from tools import *
from dbaccess import dba
from model import *
from controls.control_usuarios import ControlUsuario
from true_random import get_true_random


class ControlSorteio:

    @staticmethod
    def criar_sorteio(dicionario: dict):

        token = dicionario['token']
        tipo_sorteio = int(dicionario['tipo_sorteio'])
        data_sorteio = dicionario['data_sorteio']
        inicio_vendas = dicionario['inicio_vendas']
        fim_vendas = dicionario['fim_vendas']
        quantidade_ingressos = int(dicionario['quantidade_ingressos'])
        preco_ingresso = float(dicionario['preco_ingresso'])
        ingressos_por_usuario = int(dicionario['ingressos_por_usuario'])
        try:
            premio = float(dicionario['premio'])
        except:
            premio = 0

        usuario = ControlUsuario.get_usuario_by_token(token)
        print(usuario.nivel_usuario)
        if usuario and usuario.nivel_usuario == 1:
            data_sorteio = datetime.strptime(data_sorteio, '%Y-%m-%d')
            inicio_vendas = datetime.strptime(inicio_vendas, '%Y-%m-%d')
            fim_vendas = datetime.strptime(fim_vendas, '%Y-%m-%d')
            if tipo_sorteio == 1:
                sorteio = Sorteio(tipo_sorteio, data_sorteio, inicio_vendas, fim_vendas,
                                  quantidade_ingressos, preco_ingresso, ingressos_por_usuario)
                dba.insertorm(sorteio)
            elif tipo_sorteio == 2:
                if usuario.saldo >= premio:
                    sorteio = Sorteio(tipo_sorteio, data_sorteio, inicio_vendas, fim_vendas,
                                      quantidade_ingressos, preco_ingresso, ingressos_por_usuario, premio)
                    usuario.saldo -= premio
                    dba.insertorm(sorteio)
                    dba.insertorm(usuario)
                else:
                    return False, "Saldo Insuficiente para Criar o Sorteio"
            dba.commit()
            return True, 'Sorteio Criado com Sucesso'
        return False, "Erro ao Logar"

    @staticmethod
    def get_sorteio(id: int):

        resultado = list(dba.session.query(Sorteio).filter(Sorteio.id == id))
        if len(resultado) > 0:
            return resultado[0]
        return False

    @staticmethod
    def sorteio_is_full(sorteio: Sorteio):
        ingressos_comprados = dba.session.query(Ingresso.id).filter(Ingresso.id_sorteio == sorteio.id).count()

        return ingressos_comprados == sorteio.quantidade_ingressos

    @staticmethod
    def sorteio_cliente_full(sorteio: Sorteio, usuario: User):
        filtros = [
            Ingresso.id_sorteio == sorteio.id,
            Ingresso.id_usuario == usuario.id
        ]
        ingressos_comprados = dba.session.query(Ingresso.id).filter(*filtros).count()

        return ingressos_comprados == sorteio.ingressos_por_usuario

    @staticmethod
    def sortear(dicionario: dict):
        id = dicionario['id']
        sorteio = ControlSorteio.get_sorteio(id)
        loteria = ControlUsuario.get_usuario(19)
        if isinstance(sorteio, Sorteio):
            lista_ingressos = list(dba.session.query(Ingresso).filter(Ingresso.id_sorteio == id))

            if len(lista_ingressos) > 0:
                indice_escolhido = get_true_random(len(lista_ingressos))
                ingresso_escolhido = lista_ingressos[indice_escolhido]

                for ingresso in lista_ingressos:
                    ingresso.status_ingresso = 1
                    dba.insertorm(ingresso)
                ingresso_escolhido.status_ingresso = 2
                dba.insertorm(ingresso_escolhido)
                ControlUsuario.premiar_usuario(ingresso_escolhido.id_usuario, sorteio.premio)
                loteria.saldo -= sorteio.premio
                sorteio.status = 1
                dba.insertorm(loteria)
                dba.insertorm(sorteio)
                dba.commit()
                return True, f'{ingresso_escolhido.id_usuario}'
            return False, 'Sem ingressos para sortear'
        return False, 'Sorteio Falho!'

    @staticmethod
    def listar_sorteios(dicionario: dict):
        status = int(dicionario['status'])

        if status == -1:
            resultados = dba.session.query(Sorteio).all()
        elif status in (0, 1):
            resultados = dba.session.query(Sorteio).filter(Sorteio.status == status).all()
        else:
            return False, 'Status de sorteio inválido'
        return True, [x.dicionario_resultado() for x in resultados]
