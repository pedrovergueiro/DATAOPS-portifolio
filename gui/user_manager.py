"""Gerenciador de Usuários - Apenas Desenvolvedor"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from data.manager import DataManager


def gerenciar_usuarios(root, data_manager: DataManager):
    """Abre janela de gerenciamento de usuários - APENAS DESENVOLVEDOR"""
    
    janela_usuarios = tk.Toplevel(root)
    janela_usuarios.title("👤 Gerenciar Usuários")
    janela_usuarios.geometry("900x600")
    janela_usuarios.attributes('-topmost', True)
    
    main_frame = tk.Frame(janela_usuarios)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(main_frame, text="👤 GERENCIAMENTO DE USUÁRIOS", 
             font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=(0,10))
    
    # Treeview para usuários
    frame_tree = tk.Frame(main_frame)
    frame_tree.pack(fill='both', expand=True, pady=10)
    
    tree_usuarios = ttk.Treeview(frame_tree, columns=['Login', 'Tipo', 'Permissões'], show='headings')
    tree_usuarios.heading('Login', text='Login')
    tree_usuarios.heading('Tipo', text='Tipo')
    tree_usuarios.heading('Permissões', text='Permissões')
    
    tree_usuarios.column('Login', width=250)
    tree_usuarios.column('Tipo', width=200)
    tree_usuarios.column('Permissões', width=150)
    
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree_usuarios.yview)
    tree_usuarios.configure(yscrollcommand=scrollbar.set)
    
    tree_usuarios.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    def carregar_usuarios():
        """Carrega usuários na tabela"""
        for item in tree_usuarios.get_children():
            tree_usuarios.delete(item)
        
        if data_manager.df_users is not None:
            for _, usuario in data_manager.df_users.iterrows():
                permissoes = "Sim" if str(usuario.get('permissoes', False)).lower() in ['true', '1', 'sim'] else "Não"
                
                tree_usuarios.insert("", "end", values=[
                    usuario['login'],
                    usuario['tipo'],
                    permissoes
                ])
    
    carregar_usuarios()
    
    # Frame de botões
    frame_botoes = tk.Frame(main_frame)
    frame_botoes.pack(fill='x', pady=10)
    
    def adicionar_usuario():
        """Adiciona novo usuário"""
        janela_add = tk.Toplevel(janela_usuarios)
        janela_add.title("➕ Adicionar Usuário")
        janela_add.geometry("450x450")
        janela_add.attributes('-topmost', True)
        janela_add.grab_set()
        
        tk.Label(janela_add, text="➕ ADICIONAR NOVO USUÁRIO", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        frame_form = tk.Frame(janela_add)
        frame_form.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Campos do formulário
        tk.Label(frame_form, text="Login:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=8)
        login_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=login_var, width=30, font=("Arial", 10)).grid(row=0, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Senha:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=8)
        senha_var = tk.StringVar()
        entry_senha = tk.Entry(frame_form, textvariable=senha_var, show="*", width=30, font=("Arial", 10))
        entry_senha.grid(row=1, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Confirmar Senha:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', pady=8)
        confirmar_senha_var = tk.StringVar()
        entry_confirmar = tk.Entry(frame_form, textvariable=confirmar_senha_var, show="*", width=30, font=("Arial", 10))
        entry_confirmar.grid(row=2, column=1, pady=8, padx=5)
        
        # Botão mostrar senha
        def toggle_senha():
            if entry_senha.cget('show') == '*':
                entry_senha.config(show='')
                entry_confirmar.config(show='')
                btn_mostrar.config(text="🙈 Ocultar")
            else:
                entry_senha.config(show='*')
                entry_confirmar.config(show='*')
                btn_mostrar.config(text="👁️ Mostrar")
        
        btn_mostrar = tk.Button(frame_form, text="👁️ Mostrar", command=toggle_senha, 
                               bg="#95a5a6", fg="white", font=("Arial", 8))
        btn_mostrar.grid(row=2, column=2, pady=8, padx=5)
        
        tk.Label(frame_form, text="Tipo:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', pady=8)
        tipo_var = tk.StringVar(value="Operador")
        tipos = ["Desenvolvedor", "Coordenador", "Encarregado", "Analista", "Operador"]
        ttk.Combobox(frame_form, textvariable=tipo_var, values=tipos, state="readonly", 
                    width=27, font=("Arial", 10)).grid(row=3, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Permissões:", font=("Arial", 10)).grid(row=4, column=0, sticky='w', pady=8)
        permissoes_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_form, text="Usuário tem permissões administrativas", 
                      variable=permissoes_var, font=("Arial", 9)).grid(row=4, column=1, sticky='w', pady=8, padx=5)
        
        def salvar_usuario():
            login = login_var.get().strip()
            senha = senha_var.get()
            confirmar = confirmar_senha_var.get()
            tipo = tipo_var.get()
            permissoes = permissoes_var.get()
            
            # Validações
            if not login:
                messagebox.showerror("Erro", "Login não pode estar vazio!")
                return
            
            if not senha:
                messagebox.showerror("Erro", "Senha não pode estar vazia!")
                return
            
            if senha != confirmar:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            
            if len(senha) < 4:
                messagebox.showerror("Erro", "Senha deve ter no mínimo 4 caracteres!")
                return
            
            # Verificar se login já existe
            if login in data_manager.df_users['login'].values:
                messagebox.showerror("Erro", f"Usuário '{login}' já existe!")
                return
            
            # Adicionar usuário
            novo_usuario = pd.DataFrame([{
                'login': login,
                'senha': senha,
                'tipo': tipo,
                'permissoes': permissoes,
                'primeiro_login': True
            }])
            
            data_manager.df_users = pd.concat([data_manager.df_users, novo_usuario], ignore_index=True)
            
            if data_manager.salvar_usuarios():
                messagebox.showinfo("✅ Sucesso", f"Usuário '{login}' adicionado com sucesso!")
                carregar_usuarios()
                janela_add.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao salvar usuário!")
        
        # Botões
        frame_btns = tk.Frame(janela_add)
        frame_btns.pack(fill='x', padx=20, pady=20)
        
        tk.Button(frame_btns, text="✅ Salvar", command=salvar_usuario,
                 bg="#28a745", fg="white", font=("Arial", 11, "bold"), width=15).pack(side='left', padx=5)
        
        tk.Button(frame_btns, text="❌ Cancelar", command=janela_add.destroy,
                 bg="#dc3545", fg="white", font=("Arial", 11, "bold"), width=15).pack(side='right', padx=5)
    
    def editar_usuario():
        """Edita usuário selecionado"""
        selecionado = tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar!")
            return
        
        item = tree_usuarios.item(selecionado[0])
        login_atual = item['values'][0]
        
        # Não permitir editar desenvolvedor
        if login_atual == 'desenvolvedor':
            messagebox.showwarning("Aviso", "Não é possível editar o usuário desenvolvedor!")
            return
        
        usuario_atual = data_manager.df_users[data_manager.df_users['login'] == login_atual].iloc[0]
        
        janela_edit = tk.Toplevel(janela_usuarios)
        janela_edit.title("✏️ Editar Usuário")
        janela_edit.geometry("450x400")
        janela_edit.attributes('-topmost', True)
        janela_edit.grab_set()
        
        tk.Label(janela_edit, text=f"✏️ EDITAR USUÁRIO: {login_atual}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        frame_form = tk.Frame(janela_edit)
        frame_form.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(frame_form, text="Nova Senha:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=8)
        senha_var = tk.StringVar()
        entry_senha = tk.Entry(frame_form, textvariable=senha_var, show="*", width=30, font=("Arial", 10))
        entry_senha.grid(row=0, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Confirmar Senha:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=8)
        confirmar_senha_var = tk.StringVar()
        entry_confirmar = tk.Entry(frame_form, textvariable=confirmar_senha_var, show="*", width=30, font=("Arial", 10))
        entry_confirmar.grid(row=1, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Tipo:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', pady=8)
        tipo_var = tk.StringVar(value=usuario_atual['tipo'])
        tipos = ["Desenvolvedor", "Coordenador", "Encarregado", "Analista", "Operador"]
        ttk.Combobox(frame_form, textvariable=tipo_var, values=tipos, state="readonly", 
                    width=27, font=("Arial", 10)).grid(row=2, column=1, pady=8, padx=5)
        
        tk.Label(frame_form, text="Permissões:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', pady=8)
        permissoes_var = tk.BooleanVar(value=str(usuario_atual.get('permissoes', False)).lower() in ['true', '1', 'sim'])
        tk.Checkbutton(frame_form, text="Usuário tem permissões administrativas", 
                      variable=permissoes_var, font=("Arial", 9)).grid(row=3, column=1, sticky='w', pady=8, padx=5)
        
        tk.Label(frame_form, text="💡 Deixe a senha em branco para não alterar", 
                font=("Arial", 8), fg="#7f8c8d").grid(row=4, column=0, columnspan=2, pady=10)
        
        def salvar_edicao():
            senha = senha_var.get()
            confirmar = confirmar_senha_var.get()
            tipo = tipo_var.get()
            permissoes = permissoes_var.get()
            
            # Validar senha se foi preenchida
            if senha:
                if senha != confirmar:
                    messagebox.showerror("Erro", "As senhas não coincidem!")
                    return
                
                if len(senha) < 4:
                    messagebox.showerror("Erro", "Senha deve ter no mínimo 4 caracteres!")
                    return
                
                # Atualizar senha
                data_manager.df_users.loc[data_manager.df_users['login'] == login_atual, 'senha'] = senha
            
            # Atualizar tipo e permissões
            data_manager.df_users.loc[data_manager.df_users['login'] == login_atual, 'tipo'] = tipo
            data_manager.df_users.loc[data_manager.df_users['login'] == login_atual, 'permissoes'] = permissoes
            
            if data_manager.salvar_usuarios():
                messagebox.showinfo("✅ Sucesso", f"Usuário '{login_atual}' atualizado com sucesso!")
                carregar_usuarios()
                janela_edit.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao salvar alterações!")
        
        # Botões
        frame_btns = tk.Frame(janela_edit)
        frame_btns.pack(fill='x', padx=20, pady=20)
        
        tk.Button(frame_btns, text="✅ Salvar", command=salvar_edicao,
                 bg="#28a745", fg="white", font=("Arial", 11, "bold"), width=15).pack(side='left', padx=5)
        
        tk.Button(frame_btns, text="❌ Cancelar", command=janela_edit.destroy,
                 bg="#dc3545", fg="white", font=("Arial", 11, "bold"), width=15).pack(side='right', padx=5)
    
    def remover_usuario():
        """Remove usuário selecionado"""
        selecionado = tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para remover!")
            return
        
        item = tree_usuarios.item(selecionado[0])
        login = item['values'][0]
        
        # Não permitir remover desenvolvedor
        if login == 'desenvolvedor':
            messagebox.showwarning("Aviso", "Não é possível remover o usuário desenvolvedor!")
            return
        
        # Confirmar remoção
        resposta = messagebox.askyesno("Confirmar Remoção", 
                                       f"Tem certeza que deseja remover o usuário '{login}'?\n\n"
                                       "Esta ação não pode ser desfeita!")
        
        if resposta:
            data_manager.df_users = data_manager.df_users[data_manager.df_users['login'] != login]
            
            if data_manager.salvar_usuarios():
                messagebox.showinfo("✅ Sucesso", f"Usuário '{login}' removido com sucesso!")
                carregar_usuarios()
            else:
                messagebox.showerror("Erro", "Falha ao remover usuário!")
    
    # Botões de ação
    tk.Button(frame_botoes, text="➕ Adicionar Usuário", command=adicionar_usuario,
             bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=18).pack(side='left', padx=5)
    
    tk.Button(frame_botoes, text="✏️ Editar Usuário", command=editar_usuario,
             bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=18).pack(side='left', padx=5)
    
    tk.Button(frame_botoes, text="🗑️ Remover Usuário", command=remover_usuario,
             bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=18).pack(side='left', padx=5)
    
    tk.Button(frame_botoes, text="🔄 Atualizar", command=carregar_usuarios,
             bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=15).pack(side='right', padx=5)
    
    # Centralizar janela
    janela_usuarios.update_idletasks()
    x = (janela_usuarios.winfo_screenwidth() - janela_usuarios.winfo_width()) // 2
    y = (janela_usuarios.winfo_screenheight() - janela_usuarios.winfo_height()) // 2
    janela_usuarios.geometry(f"+{x}+{y}")
