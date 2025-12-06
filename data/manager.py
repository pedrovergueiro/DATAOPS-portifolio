"""Gerenciador central de dados"""

import pandas as pd
from .loader import carregar_dataframe_seguro
from .saver import salvar_dataframe_seguro
from utils.paths import obter_caminho_arquivo_seguro, garantir_arquivo_rede
from config.settings import CSV_FILE, USERS_FILE, LOG_FILE
from config.constants import COLUNAS_DADOS, COLUNAS_USUARIOS, COLUNAS_LOG, USUARIOS_PADRAO


class DataManager:
    """Gerenciador central de dados com suporte a rede"""

    def __init__(self):
        self.csv_path = None
        self.users_path = None
        self.log_path = None
        self.df = None
        self.df_users = None
        self.df_log = None
        self._inicializar_caminhos()

    def _inicializar_caminhos(self):
        """Inicializa caminhos dos arquivos - TENTA REDE, FALLBACK LOCAL"""
        import os
        from config.settings import CAMINHO_REDE, CAMINHO_LOCAL
        
        self.csv_path = obter_caminho_arquivo_seguro(CSV_FILE)
        
        # Tentar usar rede para usuários, fallback para local
        if os.path.exists(CAMINHO_REDE):
            self.users_path = os.path.join(CAMINHO_REDE, USERS_FILE)
            print(f"✅ Usando REDE para usuários: {self.users_path}")
        else:
            self.users_path = os.path.join(CAMINHO_LOCAL, USERS_FILE)
            print(f"📁 Usando LOCAL para usuários: {self.users_path}")
        
        self.log_path = obter_caminho_arquivo_seguro(LOG_FILE)

    def inicializar_arquivos(self):
        """Inicializa todos os arquivos necessários - TENTA REDE, FALLBACK LOCAL"""
        import os
        from config.settings import CAMINHO_REDE, CAMINHO_LOCAL
        
        print(f"📂 Caminho base: {self.csv_path}")
        print(f"📁 Caminho usuários: {self.users_path}")
        print(f"🌐 Caminho rede: {CAMINHO_REDE}")
        
        # Verificar acesso à rede
        tem_acesso_rede = os.path.exists(CAMINHO_REDE)
        
        if not tem_acesso_rede:
            print(f"⚠️ Sem acesso à rede! Usando modo LOCAL")
            print(f"📁 Usuários serão salvos localmente em: {CAMINHO_LOCAL}")
            # Usar caminho local para usuários
            self.users_path = os.path.join(CAMINHO_LOCAL, "usuarios.csv")
        else:
            print(f"✅ Acesso à rede confirmado")
            # Garantir que diretório de rede existe
            os.makedirs(CAMINHO_REDE, exist_ok=True)
        
        df_log_temp = carregar_dataframe_seguro(self.log_path, COLUNAS_LOG)
        df_temp = carregar_dataframe_seguro(self.csv_path, COLUNAS_DADOS)
        
        # CARREGAR USUÁRIOS DA REDE
        df_users_temp = carregar_dataframe_seguro(self.users_path, COLUNAS_USUARIOS)

        # Garante todas as colunas do arquivo de usuários
        for col in COLUNAS_USUARIOS:
            if col not in df_users_temp.columns:
                if col in ["permissoes", "primeiro_login"]:
                    df_users_temp[col] = True
                else:
                    df_users_temp[col] = ""

        # Se o arquivo estiver vazio ou sem coluna login → cria padrões
        if len(df_users_temp) == 0 or "login" not in df_users_temp.columns:
            print("🔄 Criando usuários padrão na REDE")
            df_users_temp = pd.DataFrame(columns=COLUNAS_USUARIOS)

        # Garante usuários padrão
        usuarios_adicionados = False
        for usuario in USUARIOS_PADRAO:
            if len(df_users_temp) == 0 or usuario["login"] not in df_users_temp["login"].values:
                df_users_temp = pd.concat(
                    [df_users_temp, pd.DataFrame([usuario])],
                    ignore_index=True
                )
                print(f"➕ Usuário padrão adicionado: {usuario['login']}")
                usuarios_adicionados = True

        # SALVAR USUÁRIOS (REDE OU LOCAL)
        if usuarios_adicionados or len(df_users_temp) > 0:
            try:
                # Garantir que diretório existe
                os.makedirs(os.path.dirname(self.users_path), exist_ok=True)
                df_users_temp.to_csv(self.users_path, index=False, encoding='utf-8')
                local_ou_rede = "REDE" if tem_acesso_rede else "LOCAL"
                print(f"✅ Usuários salvos ({local_ou_rede}): {self.users_path}")
            except Exception as e:
                print(f"❌ ERRO ao salvar usuários: {e}")
                # Tentar salvar em local como último recurso
                try:
                    local_backup = os.path.join(CAMINHO_LOCAL, "usuarios.csv")
                    os.makedirs(CAMINHO_LOCAL, exist_ok=True)
                    df_users_temp.to_csv(local_backup, index=False, encoding='utf-8')
                    self.users_path = local_backup
                    print(f"✅ Usuários salvos em backup local: {local_backup}")
                except Exception as e2:
                    print(f"❌ ERRO CRÍTICO ao salvar backup: {e2}")

        print(f"📊 Dados produção: {len(df_temp)} registros")
        print(f"👥 Usuários: {len(df_users_temp)} cadastrados")
        print(f"📝 Logs: {len(df_log_temp)} registros")

        # Atualiza atributos
        self.df = df_temp
        self.df_users = df_users_temp
        self.df_log = df_log_temp

        return self.df, self.df_users, self.df_log

    def salvar_dados(self):
        """Salva dados de produção"""
        return salvar_dataframe_seguro(self.df, self.csv_path)

    def salvar_usuarios(self):
        """Salva usuários"""
        return salvar_dataframe_seguro(self.df_users, self.users_path)

    def salvar_log(self, registro):
        """Salva registro de log"""
        if self.df_log is None:
            self.df_log = pd.DataFrame(columns=COLUNAS_LOG)

        novo_registro = pd.DataFrame([registro])
        self.df_log = pd.concat([self.df_log, novo_registro], ignore_index=True)
        return salvar_dataframe_seguro(self.df_log, self.log_path)
