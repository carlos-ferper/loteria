from dbaccess import DBAccess


class Controller:
    def __init__(self):
        print('inicio')
        self.dba = DBAccess()
        self.criar_banco()

        self.encerrar_dba()
        print('fim')

    def criar_banco(self):
        print('criando bd')
        self.dba.createbase()

    def encerrar_dba(self):
        self.dba.commit()
        self.dba.close()


def ajustar_propriedade(valor_default):
    if valor_default.tipo_dado == 'float':
        prop = float(valor_default.valor)
    elif valor_default.tipo_dado == 'int':
        prop = int(valor_default.valor)
    elif valor_default.tipo_dado == 'bool':
        prop = bool(valor_default.valor)
    else:
        prop = valor_default.valor

    return prop
