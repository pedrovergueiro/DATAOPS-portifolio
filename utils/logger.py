"""Sistema de logging"""

import datetime

_log_manager = None

def set_log_manager(manager):
    """Define o gerenciador de dados para logging"""
    global _log_manager
    _log_manager = manager

def registrar_acao(acao, usuario, detalhes=""):
    """Registra ação no log"""
    try:
        registro = {
            'acao': acao,
            'usuario': usuario,
            'detalhes': str(detalhes),
            'data_hora': datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        if _log_manager:
            _log_manager.salvar_log(registro)
        return True
    except Exception as e:
        print(f"❌ Erro ao registrar ação: {e}")
        return False
