"""Sistema de salvamento de dados"""

import os
import pandas as pd
from config.settings import CAMINHO_LOCAL

def salvar_dataframe_seguro(dataframe, caminho):
    """Salva DataFrame com tratamento robusto de erros"""
    try:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        dataframe.to_csv(caminho, index=False, encoding='utf-8')
        print(f"💾 Dados salvos: {os.path.basename(caminho)} - {len(dataframe)} registros")
        return True
    except Exception as e:
        print(f"⚠️ Erro ao salvar {caminho}: {e}")
        
        try:
            temp_dir = os.path.join(CAMINHO_LOCAL, "backup")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, os.path.basename(caminho))
            dataframe.to_csv(temp_path, index=False, encoding='utf-8')
            print(f"📦 Backup salvo em: {temp_path}")
            return True
        except Exception as e2:
            print(f"❌ Erro crítico ao salvar backup: {e2}")
            return False
