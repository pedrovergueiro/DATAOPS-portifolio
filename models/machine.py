"""Modelo de configuração de máquina"""

import os
import json
from config.settings import CAMINHO_LOCAL
from config.constants import TABELA_SIZES

class MachineConfig:
    """Gerenciador de configuração de máquina"""
    
    def __init__(self):
        self.config_path = os.path.join(CAMINHO_LOCAL, "config_maquina.json")
        self.size_path = os.path.join(CAMINHO_LOCAL, "config_size.json")
    
    def obter_configuracao_maquina(self):
        """Obtém configuração da máquina"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                return config.get('maquina', None)
            return None
        except Exception as e:
            print(f"❌ Erro configuração: {e}")
            return None
    
    def salvar_configuracao_maquina(self, maquina):
        """Salva configuração da máquina"""
        try:
            config = {'maquina': maquina}
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            print(f"❌ Erro salvar configuração: {e}")
            return False
    
    def obter_configuracao_size(self, maquina_atual=None):
        """Obtém configuração do size da máquina"""
        try:
            if os.path.exists(self.size_path):
                with open(self.size_path, 'r') as f:
                    config = json.load(f)
                return config
            elif maquina_atual and maquina_atual in TABELA_SIZES:
                return {
                    'maquina': maquina_atual,
                    'size': TABELA_SIZES[maquina_atual]['size'],
                    'peso': TABELA_SIZES[maquina_atual]['peso']
                }
            return {'maquina': maquina_atual or '', 'size': '#0', 'peso': 0.000096}
        except Exception as e:
            print(f"❌ Erro configuração size: {e}")
            return {'maquina': maquina_atual or '', 'size': '#0', 'peso': 0.000096}
    
    def salvar_configuracao_size(self, config):
        """Salva configuração do size"""
        try:
            with open(self.size_path, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            print(f"❌ Erro salvar configuração size: {e}")
            return False
