from dbaccess import dba
from model import *
from controls.control_usuarios import ControlUsuario
from controls.control_sorteio import ControlSorteio


class ControlIngresso:

    @staticmethod
    def comprar_ingresso(dicionario: dict):
        token = dicionario['token']
        sorteio = int(dicionario['sorteio'])

        usuario = ControlUsuario.get_usuario_by_token(token)

        if usuario and usuario.nivel_usuario == 2:
            sorteio = ControlSorteio.get_sorteio(sorteio)
            if not ControlSorteio.sorteio_is_full(sorteio):
                if not ControlSorteio.sorteio_cliente_full(sorteio, usuario):
                    if usuario.saldo >= sorteio.preco_ingresso:
                        loteria = ControlUsuario.get_usuario(19)
                        if sorteio.tipo_sorteio == 1:
                            sorteio.premio += sorteio.preco_ingresso
                        usuario.saldo -= sorteio.preco_ingresso
                        loteria.saldo += sorteio.preco_ingresso
                        ingresso = Ingresso(sorteio.id, usuario.id)
                        dba.insertorm(sorteio)
                        dba.insertorm(usuario)
                        dba.insertorm(ingresso)

                        dba.commit()
                    else:
                        return False, "Saldo Insuficiente para comprar o ingresso"
                    return True, 'Ingresso Comprado com Sucesso'
                return False, "Usuario já esgotou os ingressos nesse sorteio"
            return False, "Sorteio já Cheio"
        return False, 'Usuario ou tipo inválido!'

    @staticmethod
    def get_ingressos_by_sorteio(id: int):
        return list(dba.session.query(Ingresso).filter(Ingresso.id_sorteio == id))

    @staticmethod
    def listar_ingressos(dicionario: dict):
        try:
            token = dicionario['token']
            usuario = ControlUsuario.get_usuario_by_token(token)
        except:
            usuario = None
        status = int(dicionario['status'])
        if usuario is not None:
            filtros = [
                Ingresso.id_usuario == usuario.id
            ]
            if status in (1, 2, 3):
                filtros.append(Ingresso.status_ingresso == status)
            elif status != -1:
                return False, 'Status de sorteio inválido'
            resultados = list(dba.session.query(Ingresso).filter(*filtros))
            return True, [x.dicionario_resultado() for x in resultados]
