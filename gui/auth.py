"""Sistema de autenticação"""

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from data.manager import DataManager
from utils.paths import garantir_arquivo_rede
from config.settings import USERS_FILE
from config.constants import USUARIOS_PADRAO, COLUNAS_USUARIOS

def verificar_senha_desenvolvedor(root, data_manager: DataManager):
    """Verifica senha do desenvolvedor - FUNCIONA REDE OU LOCAL"""
    
    def garantir_usuarios():
        """Garante que usuários existam (rede ou local)"""
        import os
        from config.settings import CAMINHO_REDE, CAMINHO_LOCAL
        
        try:
            # Verificar se precisa recarregar
            if data_manager.df_users is None or len(data_manager.df_users) == 0:
                print("🔄 Recarregando usuários...")
                data_manager.inicializar_arquivos()
            
            if data_manager.df_users is None or len(data_manager.df_users) == 0:
                print("🔄 Criando usuários padrão...")
                df_novo = pd.DataFrame(USUARIOS_PADRAO)
                data_manager.df_users = df_novo
                data_manager.salvar_usuarios()
                print("✅ Usuários criados")
                return True
            
            # Verificar se desenvolvedor existe
            dev_user = data_manager.df_users[data_manager.df_users['login'] == 'desenvolvedor']
            if dev_user.empty:
                print("➕ Adicionando usuário desenvolvedor...")
                novo_dev = pd.DataFrame([{
                    'login': 'desenvolvedor',
                    'senha': '010524Np@',
                    'tipo': 'Desenvolvedor',
                    'permissoes': True,
                    'primeiro_login': True
                }])
                data_manager.df_users = pd.concat([data_manager.df_users, novo_dev], ignore_index=True)
                data_manager.salvar_usuarios()
                print("✅ Usuário desenvolvedor criado")
            
            print(f"✅ Total de usuários: {len(data_manager.df_users)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao garantir usuários: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Garantir usuários antes de abrir janela
    if not garantir_usuarios():
        try:
            messagebox.showerror("Erro", "Não foi possível acessar o sistema de usuários!")
        except:
            print("❌ Erro ao mostrar mensagem")
        return False
    
    if data_manager.df_users is None or len(data_manager.df_users) == 0:
        messagebox.showerror("Erro", "Não foi possível carregar usuários!")
        return False
    
    janela_senha = tk.Toplevel(root)
    janela_senha.title("🔐 Acesso Desenvolvedor")
    janela_senha.geometry("350x250")
    janela_senha.attributes('-topmost', True)
    janela_senha.grab_set()
    
    frame_principal = tk.Frame(janela_senha)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="🔐 ACESSO DESENVOLVEDOR", 
             font=("Arial", 12, "bold"), fg="#2c3e50").pack(pady=10)
    
    tk.Label(frame_principal, text="Digite a senha do desenvolvedor:", 
             font=("Arial", 10)).pack(pady=5)
    
    senha_var = tk.StringVar()
    entry_senha = tk.Entry(frame_principal, textvariable=senha_var, show="*", 
                          width=25, font=("Arial", 12))
    entry_senha.pack(pady=10)
    entry_senha.focus()
    
    resultado = [False]
    
    def verificar():
        senha = senha_var.get().strip()
        
        if 'login' not in data_manager.df_users.columns or 'senha' not in data_manager.df_users.columns:
            messagebox.showerror("Erro", "Estrutura de dados corrompida!")
            return
        
        dev_user = data_manager.df_users[data_manager.df_users['login'] == 'desenvolvedor']
        
        if dev_user.empty:
            novo_dev = pd.DataFrame([{
                'login': 'desenvolvedor',
                'senha': '010524Np@',
                'tipo': 'Desenvolvedor',
                'permissoes': True,
                'primeiro_login': True
            }])
            data_manager.df_users = pd.concat([data_manager.df_users, novo_dev], ignore_index=True)
            data_manager.salvar_usuarios()
            dev_user = data_manager.df_users[data_manager.df_users['login'] == 'desenvolvedor']
        
        if not dev_user.empty:
            senha_correta = dev_user.iloc[0]['senha']
            if senha == senha_correta:
                resultado[0] = True
                janela_senha.destroy()
            else:
                messagebox.showerror("Erro", "Senha incorreta!")
                entry_senha.delete(0, tk.END)
                entry_senha.focus()
    
    tk.Button(frame_principal, text="🔓 Acessar", command=verificar,
             bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=10)
    
    janela_senha.bind('<Return>', lambda e: verificar())
    janela_senha.update_idletasks()
    x = (janela_senha.winfo_screenwidth() - janela_senha.winfo_width()) // 2
    y = (janela_senha.winfo_screenheight() - janela_senha.winfo_height()) // 2
    janela_senha.geometry(f"+{x}+{y}")
    
    janela_senha.wait_window()
    return resultado[0]
