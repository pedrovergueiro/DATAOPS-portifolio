"""Modelo de configuração de lote"""

import os
import json
import datetime
from config.settings import CAMINHO_LOCAL

class BatchConfig:
    """Gerenciador de configuração de lote"""
    
    def __init__(self):
        self.lote_path = os.path.join(CAMINHO_LOCAL, "config_lote.json")
        self.lote_atual = None
        self.numero_caixa_atual = 0
        self.total_caixas_lote = 0
        self.caixas_registradas = 0
        self._carregar()
    
    def _carregar(self):
        """Carrega configuração do lote"""
        try:
            if os.path.exists(self.lote_path):
                with open(self.lote_path, 'r') as f:
                    config = json.load(f)
                self.lote_atual = config.get('lote', None)
                self.numero_caixa_atual = config.get('caixa_atual', 0)
                self.total_caixas_lote = config.get('total_caixas', 0)
                self.caixas_registradas = config.get('caixas_registradas', 0)
        except Exception as e:
            print(f"❌ Erro carregar lote: {e}")
    
    def obter_configuracao_lote(self):
        """Obtém configuração atual do lote"""
        return {
            'lote': self.lote_atual or '',
            'caixa_atual': self.numero_caixa_atual,
            'total_caixas': self.total_caixas_lote,
            'caixas_registradas': self.caixas_registradas
        }
    
    def salvar_configuracao_lote(self, lote, caixa_atual, total_caixas, caixas_registradas):
        """Salva configuração do lote"""
        try:
            self.lote_atual = lote
            self.numero_caixa_atual = caixa_atual
            self.total_caixas_lote = total_caixas
            self.caixas_registradas = caixas_registradas
            
            config = {
                'lote': lote,
                'caixa_atual': caixa_atual,
                'total_caixas': total_caixas,
                'caixas_registradas': caixas_registradas,
                'ultima_atualizacao': datetime.datetime.now().isoformat()
            }
            with open(self.lote_path, 'w') as f:
                json.dump(config, f)
            return True
        except Exception as e:
            print(f"❌ Erro salvar lote: {e}")
            return False
