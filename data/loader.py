"""Sistema de carregamento de dados"""

import pandas as pd
import shutil
import time
import os

def carregar_dataframe_seguro(caminho, colunas_padrao):
    """Carrega DataFrame com tratamento robusto de erros"""
    try:
        if os.path.exists(caminho):
            try:
                df = pd.read_csv(caminho, dtype=str)
                print(f"✅ Arquivo carregado: {os.path.basename(caminho)} - {len(df)} registros")
                return df
            except pd.errors.EmptyDataError:
                print(f"⚠️ Arquivo vazio: {caminho}")
                return pd.DataFrame(columns=colunas_padrao)
            except Exception as e:
                print(f"⚠️ Erro ao ler {caminho}: {e}")
                try:
                    backup_path = caminho + f".corrupt.{int(time.time())}.bak"
                    shutil.copy2(caminho, backup_path)
                    print(f"📦 Backup do arquivo corrompido salvo em: {backup_path}")
                except:
                    pass
                return pd.DataFrame(columns=colunas_padrao)
        else:
            print(f"📄 Criando novo arquivo: {os.path.basename(caminho)}")
            return pd.DataFrame(columns=colunas_padrao)
    except Exception as e:
        print(f"❌ Erro crítico ao carregar {caminho}: {e}")
        return pd.DataFrame(columns=colunas_padrao)
