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
        """Salva configuração do lote - ACEITA QUALQUER TIPO DE LOTE"""
        try:
            # Converter para string e aceitar qualquer valor
            self.lote_atual = str(lote) if lote else ''
            
            # Converter números com validação
            try:
                self.numero_caixa_atual = int(caixa_atual) if caixa_atual else 0
                self.total_caixas_lote = int(total_caixas) if total_caixas else 0
                self.caixas_registradas = int(caixas_registradas) if caixas_registradas else 0
            except (ValueError, TypeError):
                print(f"⚠️ Erro ao converter números do lote")
                return False
            
            config = {
                'lote': self.lote_atual,
                'caixa_atual': self.numero_caixa_atual,
                'total_caixas': self.total_caixas_lote,
                'caixas_registradas': self.caixas_registradas,
                'ultima_atualizacao': datetime.datetime.now().isoformat()
            }
            
            # Garantir que diretório existe
            import os
            os.makedirs(os.path.dirname(self.lote_path), exist_ok=True)
            
            with open(self.lote_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Lote salvo: {self.lote_atual} ({self.numero_caixa_atual}/{self.total_caixas_lote})")
            return True
        except Exception as e:
            print(f"❌ Erro salvar lote: {e}")
            import traceback
            traceback.print_exc()
            return False
