"""Sistema de caminhos robusto para .exe e rede"""

import os
import sys
import time
import tempfile
from config.settings import CAMINHO_REDE, CAMINHO_LOCAL

def get_base_path():
    """Obtém o caminho base correto, funcionando tanto como .py quanto como .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__ + "/../"))

def testar_acesso_rede():
    """Testa se há acesso de escrita na rede"""
    try:
        if not os.path.exists(CAMINHO_REDE):
            return False
        
        test_file = os.path.join(CAMINHO_REDE, f"test_write_{int(time.time())}.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except Exception:
        return False

def obter_caminho_arquivo_seguro(nome_arquivo, forcar_rede=False):
    """
    Obtém caminho seguro para arquivo, priorizando rede quando disponível.
    
    Args:
        nome_arquivo: Nome do arquivo
        forcar_rede: Se True, tenta forçar uso da rede mesmo se falhar
    
    Returns:
        Caminho completo do arquivo (rede, local ou temporário)
    """
    if forcar_rede or testar_acesso_rede():
        try:
            os.makedirs(CAMINHO_REDE, exist_ok=True)
            caminho_rede = os.path.join(CAMINHO_REDE, nome_arquivo)
            print(f"✅ Usando caminho de rede: {caminho_rede}")
            return caminho_rede
        except Exception as e:
            print(f"⚠️ Erro ao acessar rede: {e}")
    
    try:
        os.makedirs(CAMINHO_LOCAL, exist_ok=True)
        caminho_local = os.path.join(CAMINHO_LOCAL, nome_arquivo)
        print(f"📁 Usando armazenamento local: {caminho_local}")
        return caminho_local
    except Exception as e:
        print(f"⚠️ Erro com caminho local: {e}")
        
        temp_dir = os.path.join(tempfile.gettempdir(), "coletor_producao")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, nome_arquivo)
        print(f"🚨 Usando diretório temporário: {temp_file}")
        return temp_file

def garantir_arquivo_rede(nome_arquivo, conteudo_padrao=None):
    """
    Garante que arquivo existe na rede, criando se necessário.
    Se não tiver acesso à rede, usa local.
    """
    caminho_rede = os.path.join(CAMINHO_REDE, nome_arquivo)
    
    try:
        # Verificar se tem acesso à rede
        if not os.path.exists(CAMINHO_REDE):
            print(f"⚠️ Sem acesso à rede, usando local para {nome_arquivo}")
            return obter_caminho_arquivo_seguro(nome_arquivo, forcar_rede=False)
        
        # Garantir que diretório de rede existe
        os.makedirs(CAMINHO_REDE, exist_ok=True)
        
        # Se arquivo não existe e tem conteúdo padrão, criar
        if not os.path.exists(caminho_rede) and conteudo_padrao is not None:
            if callable(conteudo_padrao):
                conteudo_padrao(caminho_rede)
            else:
                import pandas as pd
                if isinstance(conteudo_padrao, pd.DataFrame):
                    conteudo_padrao.to_csv(caminho_rede, index=False, encoding='utf-8')
                else:
                    with open(caminho_rede, 'w', encoding='utf-8') as f:
                        f.write(str(conteudo_padrao))
            print(f"✅ Arquivo criado na rede: {caminho_rede}")
        
        return caminho_rede
        
    except Exception as e:
        print(f"⚠️ Erro ao acessar rede para {nome_arquivo}: {e}")
        print(f"📁 Usando armazenamento local")
        return obter_caminho_arquivo_seguro(nome_arquivo, forcar_rede=False)
