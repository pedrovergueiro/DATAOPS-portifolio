"""Configurações de caminhos e arquivos"""

import os
import sys

CAMINHO_REDE = r"Z:\Pedro Vergueiro - melhoria continua\dataSETpfd"

CSV_FILE = "dados_producao.csv"
USERS_FILE = "usuarios.csv"
LOG_FILE = "log_acoes.csv"

VERSION = "8.0"

def get_base_path():
    """Obtém o caminho base correto, funcionando tanto como .py quanto como .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__ + "/../"))

CAMINHO_LOCAL = get_base_path()
