import configparser
import os
from cryptography.fernet import Fernet

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
chave_criptografia = config.get('criptografia', 'key')


def encriptar(dados):

    cipher = Fernet(str.encode(chave_criptografia))
    return cipher.encrypt(str.encode(dados))


def decriptar(dados):
    cipher = Fernet(str.encode(chave_criptografia))
    return cipher.decrypt(str.encode(dados))
