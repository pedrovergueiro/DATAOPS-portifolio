"""Painel do Desenvolvedor"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import json
import uuid
from models.machine import MachineConfig
from models.batch import BatchConfig
from config.constants import TABELA_SIZES
from utils.machine_id import gerar_id_computador_avancado
from config.settings import CAMINHO_REDE
from gui.user_manager import gerenciar_usuarios
from utils.log_manager import abrir_gerenciador_logs
from utils.command_priority_system import inicializar_sistema_prioridade, obter_sistema_prioridade


def abrir_painel_desenvolvedor(root, data_manager, machine_config: MachineConfig, batch_config: BatchConfig):
    """Abre painel exclusivo do desenvolvedor"""
    
    try:
        dev_win = tk.Toplevel(root)
        dev_win.title("💻 Painel do Desenvolvedor - Sistema Completo")
        dev_win.geometry("1200x800")
        dev_win.attributes('-topmost', True)
        
        # Notebook para abas
        notebook_dev = ttk.Notebook(dev_win)
        notebook_dev.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ABA 1: CONFIGURAÇÕES AVANÇADAS
        frame_config_avancada = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_config_avancada, text="⚙️ Configurações Avançadas")
        
        # Configuração de máquina
        frm_config_maquina = tk.LabelFrame(frame_config_avancada, text="🔧 Configuração da Máquina Atual")
        frm_config_maquina.pack(fill='x', padx=20, pady=10)
        
        MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
        ID_COMPUTADOR = gerar_id_computador_avancado()
        
        tk.Label(frm_config_maquina, text="Máquina Atual:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Informações atuais
        info_atual = tk.Label(frm_config_maquina, text=f"Atual: {MAQUINA_ATUAL} | ID: {ID_COMPUTADOR[:8]}...", 
                             font=("Arial", 9), fg="#7f8c8d")
        info_atual.grid(row=1, column=0, columnspan=3, padx=5, pady=2, sticky='w')
        
        tk.Label(frm_config_maquina, text="Nova Configuração:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        maquina_var = tk.StringVar(value=MAQUINA_ATUAL)
        
        # Opções de máquina disponíveis
        opcoes_maquina = [
            "DESENVOLVEDOR", "COORDENADOR", "ENCARREGADO", "ANALISTA", "OPERADOR",
            "201", "202", "203", "204", "205", "206", "207", "208", 
            "209", "210", "211", "212", "213", "214"
        ]
        
        combo_maquina = ttk.Combobox(frm_config_maquina, textvariable=maquina_var,
                                    values=opcoes_maquina, 
                                    state="readonly", width=20)
        combo_maquina.grid(row=2, column=1, padx=5, pady=5)
        
        def salvar_config_desenvolvedor():
            nova_maquina = maquina_var.get()
            
            if not nova_maquina:
                messagebox.showerror("Erro", "Selecione uma configuração para a máquina!")
                return
            
            if machine_config.salvar_configuracao_maquina(nova_maquina):
                # Atualizar configuração de size baseada na máquina
                if nova_maquina in TABELA_SIZES:
                    CONFIG_SIZE = {
                        'maquina': nova_maquina,
                        'size': TABELA_SIZES[nova_maquina]['size'],
                        'peso': TABELA_SIZES[nova_maquina]['peso']
                    }
                    machine_config.salvar_configuracao_size(CONFIG_SIZE)
                
                # Atualizar interface
                root.title(f"Coletor de Produção - Máquina {nova_maquina}")
                info_atual.config(text=f"Atual: {nova_maquina} | ID: {ID_COMPUTADOR[:8]}...")
                
                messagebox.showinfo("✅ Sucesso", 
                               f"Configuração salva com sucesso!\n\n"
                               f"Máquina: {nova_maquina}\n"
                               f"Reinicie o sistema para aplicar todas as mudanças.")
            else:
                messagebox.showerror("❌ Erro", "Erro ao salvar configuração!")
        
        tk.Button(frm_config_maquina, text="💾 Salvar Configuração", 
                  command=salvar_config_desenvolvedor, 
                  bg="#28a745", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=5, pady=5)
        
        # CONFIGURAÇÃO DE SIZE
        frm_config_size = tk.LabelFrame(frame_config_avancada, text="📏 Configuração de Size")
        frm_config_size.pack(fill='x', padx=20, pady=10)
        
        CONFIG_SIZE = machine_config.obter_configuracao_size()
        
        tk.Label(frm_config_size, text="Size Atual:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Label(frm_config_size, text=f"{CONFIG_SIZE['size']} (Peso: {CONFIG_SIZE['peso']})", 
                 font=("Arial", 10), fg="#e74c3c").grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(frm_config_size, text="Novo Size:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        size_var = tk.StringVar(value=CONFIG_SIZE['size'])
        
        # Opções de size
        sizes_disponiveis = list(set([f"{v['size']} (Peso: {v['peso']})" for k, v in TABELA_SIZES.items()]))
        combo_size = ttk.Combobox(frm_config_size, textvariable=size_var,
                                 values=sizes_disponiveis, 
                                 state="readonly", width=25)
        combo_size.grid(row=1, column=1, padx=5, pady=5)
        
        def salvar_config_size():
            novo_size_str = size_var.get()
            
            if not novo_size_str:
                messagebox.showerror("Erro", "Selecione um size!")
                return
            
            # Extrair size e peso da string
            try:
                size_parte = novo_size_str.split(' (Peso: ')[0]
                peso_parte = novo_size_str.split(' (Peso: ')[1].replace(')', '')
                peso = float(peso_parte)
                
                CONFIG_SIZE_NOVO = {
                    'maquina': MAQUINA_ATUAL,
                    'size': size_parte,
                    'peso': peso
                }
                
                if machine_config.salvar_configuracao_size(CONFIG_SIZE_NOVO):
                    messagebox.showinfo("✅ Sucesso", 
                                   f"Size atualizado!\n\n"
                                   f"Novo Size: {size_parte}\n"
                                   f"Peso: {peso}")
                else:
                    messagebox.showerror("❌ Erro", "Erro ao salvar configuração do size!")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar size: {e}")
        
        tk.Button(frm_config_size, text="💾 Salvar Size", 
                  command=salvar_config_size, 
                  bg="#3498db", fg="white", font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=5)
        
        # CONFIGURAÇÃO DE LOTE
        frm_config_lote = tk.LabelFrame(frame_config_avancada, text="📦 Configuração de Lote")
        frm_config_lote.pack(fill='x', padx=20, pady=10)
        
        config_lote = batch_config.obter_configuracao_lote()
        
        tk.Label(frm_config_lote, text="Lote Atual:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        lbl_lote_info = tk.Label(frm_config_lote, text=f"{config_lote.get('lote', 'Nenhum')} | Caixa: {config_lote.get('caixa_atual', 0)}/{config_lote.get('total_caixas', 0)}", 
                 font=("Arial", 10), fg="#27ae60")
        lbl_lote_info.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        def alterar_lote_desenvolvedor():
            # Abrir janela de configuração de lote
            janela_lote = tk.Toplevel(dev_win)
            janela_lote.title("📦 Configuração de Lote")
            janela_lote.geometry("500x400")
            janela_lote.attributes('-topmost', True)
            janela_lote.grab_set()
            
            frame_principal = tk.Frame(janela_lote)
            frame_principal.pack(fill='both', expand=True, padx=20, pady=10)
            
            tk.Label(frame_principal, text="📦 CONFIGURAÇÃO DE LOTE", 
                     font=("Arial", 14, "bold")).pack(pady=10)
            
            # Campos
            frame_campos = tk.Frame(frame_principal)
            frame_campos.pack(fill='x', pady=10)
            
            tk.Label(frame_campos, text="Número do Lote:", font=("Arial", 10)).pack(anchor='w', pady=5)
            lote_var = tk.StringVar()
            tk.Entry(frame_campos, textvariable=lote_var, width=30, font=("Arial", 10)).pack(fill='x', pady=5)
            
            tk.Label(frame_campos, text="Número Total de Caixas:", font=("Arial", 10)).pack(anchor='w', pady=5)
            total_var = tk.StringVar()
            tk.Entry(frame_campos, textvariable=total_var, width=30, font=("Arial", 10)).pack(fill='x', pady=5)
            
            tk.Label(frame_campos, text="Número da Caixa Atual:", font=("Arial", 10)).pack(anchor='w', pady=5)
            caixa_var = tk.StringVar(value="1")
            tk.Entry(frame_campos, textvariable=caixa_var, width=30, font=("Arial", 10)).pack(fill='x', pady=5)
            
            def confirmar_lote():
                try:
                    lote = lote_var.get().strip()
                    if not lote:
                        messagebox.showerror("Erro", "O número do lote não pode estar vazio!")
                        return
                    
                    total_caixas = int(total_var.get()) if total_var.get() else 0
                    caixa_atual = int(caixa_var.get()) if caixa_var.get() else 0
                    
                    if total_caixas <= 0 or caixa_atual <= 0:
                        messagebox.showerror("Erro", "Números de caixas devem ser maiores que zero!")
                        return
                    
                    if caixa_atual > total_caixas:
                        messagebox.showerror("Erro", "Caixa atual não pode ser maior que o total!")
                        return
                    
                    if batch_config.salvar_configuracao_lote(lote, caixa_atual, total_caixas, 0):
                        lbl_lote_info.config(text=f"{lote} | Caixa: {caixa_atual}/{total_caixas}")
                        janela_lote.destroy()
                        messagebox.showinfo("✅ Sucesso", 
                                       f"Lote configurado!\n\n"
                                       f"Lote: {lote}\n"
                                       f"Caixa atual: {caixa_atual}\n"
                                       f"Total de caixas: {total_caixas}")
                    else:
                        messagebox.showerror("Erro", "Erro ao salvar configuração do lote!")
                        
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro inesperado: {e}")
            
            tk.Button(frame_principal, text="✅ Confirmar Lote", command=confirmar_lote,
                     bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=20)
        
        tk.Button(frm_config_lote, text="📦 Alterar Lote", 
                  command=alterar_lote_desenvolvedor, 
                  bg="#f39c12", fg="white", font=("Arial", 10)).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # ABA 2: INFORMAÇÕES DO SISTEMA
        frame_info_sistema = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_info_sistema, text="ℹ️ Informações do Sistema")
        
        info_text = tk.Text(frame_info_sistema, wrap='word', font=("Courier", 9))
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Coletar informações
        info_sistema = f"""
╔══════════════════════════════════════════════════════════════╗
║           INFORMAÇÕES DO SISTEMA - PAINEL DEV                ║
╚══════════════════════════════════════════════════════════════╝

📊 CONFIGURAÇÃO ATUAL:
   • Máquina: {MAQUINA_ATUAL}
   • ID Computador: {ID_COMPUTADOR}
   • Size: {CONFIG_SIZE['size']}
   • Peso: {CONFIG_SIZE['peso']}

📦 LOTE ATUAL:
   • Lote: {config_lote.get('lote', 'N/D')}
   • Caixa Atual: {config_lote.get('caixa_atual', 0)}
   • Total de Caixas: {config_lote.get('total_caixas', 0)}
   • Caixas Registradas: {config_lote.get('caixas_registradas', 0)}

👥 USUÁRIOS:
   • Total de usuários: {len(data_manager.df_users)}
   • Usuários cadastrados: {', '.join(data_manager.df_users['login'].tolist())}

📊 DADOS:
   • Total de registros: {len(data_manager.df)}
   • Total de logs: {len(data_manager.df_log)}

📁 CAMINHOS:
   • Dados: {data_manager.csv_path}
   • Usuários: {data_manager.users_path}
   • Logs: {data_manager.log_path}

⏰ TIMESTAMP: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
        
        info_text.insert('1.0', info_sistema)
        info_text.config(state='disabled')
        
        # ABA 3: GERENCIAMENTO DE USUÁRIOS
        frame_usuarios = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_usuarios, text="👥 Usuários")
        
        tk.Label(frame_usuarios, text="👥 GERENCIAMENTO DE USUÁRIOS", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(frame_usuarios, text="Gerencie todos os usuários do sistema", 
                 font=("Arial", 10), fg="#7f8c8d").pack(pady=5)
        
        # Informações
        info_usuarios_frame = tk.LabelFrame(frame_usuarios, text="📊 Estatísticas", font=("Arial", 10, "bold"))
        info_usuarios_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(info_usuarios_frame, text=f"Total de usuários cadastrados: {len(data_manager.df_users)}", 
                 font=("Arial", 10)).pack(anchor='w', padx=10, pady=5)
        
        tipos_count = data_manager.df_users['tipo'].value_counts().to_dict()
        for tipo, count in tipos_count.items():
            tk.Label(info_usuarios_frame, text=f"  • {tipo}: {count}", 
                     font=("Arial", 9), fg="#666").pack(anchor='w', padx=20, pady=2)
        
        # Botão para abrir gerenciador completo
        btn_gerenciar = tk.Button(frame_usuarios, text="🔧 Abrir Gerenciador Completo de Usuários", 
                                 command=lambda: gerenciar_usuarios(root, data_manager),
                                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), 
                                 height=2, width=40)
        btn_gerenciar.pack(pady=20)
        
        # Tabela de visualização rápida
        tk.Label(frame_usuarios, text="Visualização Rápida:", 
                 font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=(20, 5))
        
        tree_frame = tk.Frame(frame_usuarios)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        tree_usuarios = ttk.Treeview(tree_frame, columns=('Login', 'Tipo', 'Permissões'), 
                                     show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree_usuarios.yview)
        
        tree_usuarios.heading('Login', text='Login')
        tree_usuarios.heading('Tipo', text='Tipo')
        tree_usuarios.heading('Permissões', text='Permissões')
        
        tree_usuarios.column('Login', width=250)
        tree_usuarios.column('Tipo', width=200)
        tree_usuarios.column('Permissões', width=150)
        
        # Preencher tabela
        for _, usuario in data_manager.df_users.iterrows():
            tree_usuarios.insert('', 'end', values=(
                usuario['login'],
                usuario['tipo'],
                'Sim' if str(usuario.get('permissoes', False)).lower() in ['true', '1', 'sim'] else 'Não'
            ))
        
        tree_usuarios.pack(fill='both', expand=True)
        
        # ABA 4: CONTROLE REMOTO
        frame_controle = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_controle, text="🌐 Controle Remoto")
        
        tk.Label(frame_controle, text="🌐 CONTROLE REMOTO DE MÁQUINAS", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(frame_controle, text="Envie comandos para outras máquinas na rede", 
                 font=("Arial", 10), fg="#7f8c8d").pack(pady=5)
        
        # Frame para descobrir máquinas
        frm_descobrir = tk.LabelFrame(frame_controle, text="🔍 Máquinas Online", font=("Arial", 10, "bold"))
        frm_descobrir.pack(fill='x', padx=20, pady=10)
        
        maquinas_online_var = tk.StringVar(value="Clique em 'Descobrir' para buscar máquinas...")
        lbl_maquinas = tk.Label(frm_descobrir, textvariable=maquinas_online_var, 
                               font=("Arial", 9), fg="#666", justify='left')
        lbl_maquinas.pack(anchor='w', padx=10, pady=10)
        
        def descobrir_maquinas():
            """Descobre máquinas online na rede"""
            try:
                maquinas = []
                if os.path.exists(CAMINHO_REDE):
                    for arquivo in os.listdir(CAMINHO_REDE):
                        if arquivo.startswith('status_maq_') and arquivo.endswith('.json'):
                            try:
                                caminho_arquivo = os.path.join(CAMINHO_REDE, arquivo)
                                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                                    status = json.load(f)
                                
                                timestamp_str = status.get('timestamp', '')
                                if timestamp_str:
                                    timestamp = datetime.datetime.fromisoformat(timestamp_str)
                                    agora = datetime.datetime.now()
                                    diferenca = (agora - timestamp).total_seconds()
                                    
                                    if diferenca < 60:  # Online se atualizou nos últimos 60s
                                        maquina_id = arquivo.replace('status_maq_', '').replace('.json', '')
                                        maquinas.append(f"✅ {maquina_id} - {status.get('hostname', 'N/A')} - IP: {status.get('ip', 'N/A')}")
                            except:
                                continue
                
                if maquinas:
                    maquinas_online_var.set("\n".join(maquinas))
                else:
                    maquinas_online_var.set("❌ Nenhuma máquina online encontrada")
            except Exception as e:
                maquinas_online_var.set(f"❌ Erro ao descobrir máquinas: {e}")
        
        tk.Button(frm_descobrir, text="🔍 Descobrir Máquinas", command=descobrir_maquinas,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Frame para enviar comandos
        frm_comandos = tk.LabelFrame(frame_controle, text="📤 Enviar Comando", font=("Arial", 10, "bold"))
        frm_comandos.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Seleção de máquina
        tk.Label(frm_comandos, text="Máquina Destino:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        maquina_destino_var = tk.StringVar()
        entry_maquina = tk.Entry(frm_comandos, textvariable=maquina_destino_var, width=20, font=("Arial", 10))
        entry_maquina.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        tk.Label(frm_comandos, text="(ex: 201, 202, DESENVOLVEDOR)", 
                font=("Arial", 8), fg="#999").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        
        # Seleção de comando
        tk.Label(frm_comandos, text="Comando:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        comando_var = tk.StringVar()
        comandos_disponiveis = [
            "fechar_app",
            "abrir_app",
            "reiniciar_app",
            "alterar_size",
            "alterar_lote",
            "alterar_configuracao_maquina",
            "coletar_dados",
            "fazer_backup",
            "coletar_informacoes_sistema",
            "executar_comando_sistema",
            "testar_conectividade",
            "obter_logs",
            "diagnostico_completo",
            "limpar_cache",
            "capturar_tela"
        ]
        combo_comando = ttk.Combobox(frm_comandos, textvariable=comando_var, 
                                    values=comandos_disponiveis, state="readonly", width=30)
        combo_comando.grid(row=1, column=1, columnspan=2, sticky='w', padx=10, pady=5)
        
        # Parâmetros
        tk.Label(frm_comandos, text="Parâmetros (JSON):", font=("Arial", 10)).grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        text_parametros = tk.Text(frm_comandos, width=50, height=6, font=("Courier", 9))
        text_parametros.grid(row=2, column=1, columnspan=2, sticky='w', padx=10, pady=5)
        text_parametros.insert('1.0', '{}')
        
        def enviar_comando():
            """Envia comando para máquina"""
            maquina = maquina_destino_var.get().strip()
            comando = comando_var.get()
            
            if not maquina:
                messagebox.showerror("Erro", "Selecione uma máquina destino!")
                return
            
            if not comando:
                messagebox.showerror("Erro", "Selecione um comando!")
                return
            
            try:
                parametros_str = text_parametros.get('1.0', 'end').strip()
                parametros = json.loads(parametros_str) if parametros_str else {}
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Parâmetros JSON inválidos!")
                return
            
            try:
                maquina_remetente = machine_config.obter_configuracao_maquina()
                
                comando_data = {
                    'acao': comando,
                    'parametros': parametros,
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.datetime.now().isoformat(),
                    'remetente': maquina_remetente
                }
                
                comando_file = os.path.join(CAMINHO_REDE, f"comando_maq_{maquina}.json")
                
                # Garantir que diretório existe
                os.makedirs(CAMINHO_REDE, exist_ok=True)
                
                with open(comando_file, 'w', encoding='utf-8') as f:
                    json.dump(comando_data, f, indent=2, ensure_ascii=False)
                
                print(f"📤 Comando enviado: {comando} -> {maquina}")
                
                messagebox.showinfo("✅ Sucesso", 
                                  f"Comando '{comando}' enviado para máquina '{maquina}'!\n\n"
                                  f"ID: {comando_data['id']}\n\n"
                                  f"O comando será executado em até 1 segundo.")
            except Exception as e:
                print(f"❌ Erro ao enviar comando: {e}")
                messagebox.showerror("Erro", f"Falha ao enviar comando: {e}")
        
        tk.Button(frm_comandos, text="📤 Enviar Comando", command=enviar_comando,
                 bg="#28a745", fg="white", font=("Arial", 11, "bold"), 
                 height=2, width=20).grid(row=3, column=1, pady=15)
        
        # Exemplos de comandos
        frm_exemplos = tk.LabelFrame(frame_controle, text="💡 Exemplos de Parâmetros", font=("Arial", 9, "bold"))
        frm_exemplos.pack(fill='x', padx=20, pady=10)
        
        exemplos_text = """
• alterar_size: {"size": "#1", "peso": 0.000076}
• alterar_lote: {"lote": "LOTE123", "caixa_atual": 1, "total_caixas": 100}
• alterar_configuracao_maquina: {"maquina": "201"}
• executar_comando_sistema: {"comando": "dir"}
• fechar_app: {"forcar": false}
• Sem parâmetros: {}
        """
        tk.Label(frm_exemplos, text=exemplos_text, font=("Courier", 8), 
                justify='left', fg="#666").pack(anchor='w', padx=10, pady=5)
        
        # Botão para enviar para todas as máquinas
        def enviar_para_todas():
            """Envia comando para todas as máquinas online"""
            comando = comando_var.get()
            
            if not comando:
                messagebox.showerror("Erro", "Selecione um comando!")
                return
            
            try:
                parametros_str = text_parametros.get('1.0', 'end').strip()
                parametros = json.loads(parametros_str) if parametros_str else {}
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Parâmetros JSON inválidos!")
                return
            
            # Descobrir máquinas
            maquinas = []
            if os.path.exists(CAMINHO_REDE):
                for arquivo in os.listdir(CAMINHO_REDE):
                    if arquivo.startswith('status_maq_') and arquivo.endswith('.json'):
                        try:
                            caminho_arquivo = os.path.join(CAMINHO_REDE, arquivo)
                            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                                status = json.load(f)
                            
                            timestamp_str = status.get('timestamp', '')
                            if timestamp_str:
                                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                                agora = datetime.datetime.now()
                                diferenca = (agora - timestamp).total_seconds()
                                
                                if diferenca < 60:
                                    maquina_id = arquivo.replace('status_maq_', '').replace('.json', '')
                                    maquinas.append(maquina_id)
                        except:
                            continue
            
            if not maquinas:
                messagebox.showwarning("Aviso", "Nenhuma máquina online encontrada!")
                return
            
            # Enviar para todas
            maquina_remetente = machine_config.obter_configuracao_maquina()
            enviados = 0
            
            for maquina in maquinas:
                if maquina != maquina_remetente:  # Não enviar para si mesmo
                    try:
                        comando_data = {
                            'acao': comando,
                            'parametros': parametros,
                            'id': str(uuid.uuid4()),
                            'timestamp': datetime.datetime.now().isoformat(),
                            'remetente': maquina_remetente
                        }
                        
                        comando_file = os.path.join(CAMINHO_REDE, f"comando_maq_{maquina}.json")
                        with open(comando_file, 'w', encoding='utf-8') as f:
                            json.dump(comando_data, f, indent=2, ensure_ascii=False)
                        
                        enviados += 1
                        print(f"📤 Comando enviado para: {maquina}")
                    except Exception as e:
                        print(f"❌ Erro ao enviar para {maquina}: {e}")
            
            messagebox.showinfo("✅ Sucesso", 
                              f"Comando '{comando}' enviado para {enviados} máquina(s)!")
        
        tk.Button(frm_comandos, text="📢 Enviar para TODAS as Máquinas", command=enviar_para_todas,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                 height=2, width=30).grid(row=4, column=1, pady=15)
        
        # ABA 5: GERENCIADOR DE LOGS E PRINTS
        frame_logs = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_logs, text="📋 Logs & Prints")
        
        tk.Label(frame_logs, text="📋 GERENCIADOR DE LOGS E PRINTS", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(frame_logs, text="Visualize, filtre e gerencie todos os logs do sistema", 
                 font=("Arial", 10), fg="#7f8c8d").pack(pady=5)
        
        # Informações sobre logs
        info_logs_frame = tk.LabelFrame(frame_logs, text="ℹ️ Informações dos Logs", font=("Arial", 10, "bold"))
        info_logs_frame.pack(fill='x', padx=20, pady=10)
        
        # Verificar logs existentes
        from utils.log_manager import LogManager
        log_manager = LogManager()
        logs_encontrados = log_manager.encontrar_logs()
        
        total_logs = len(logs_encontrados)
        total_tamanho = 0
        tipos_logs = {}
        
        for log_path in logs_encontrados:
            info_log = log_manager.obter_info_log(log_path)
            if 'erro' not in info_log:
                total_tamanho += info_log.get('tamanho_mb', 0)
                tipo = info_log.get('tipo', 'GERAL')
                tipos_logs[tipo] = tipos_logs.get(tipo, 0) + 1
        
        tk.Label(info_logs_frame, text=f"📊 Total de arquivos de log: {total_logs}", 
                 font=("Arial", 10)).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(info_logs_frame, text=f"💾 Tamanho total: {total_tamanho:.1f} MB", 
                 font=("Arial", 10)).pack(anchor='w', padx=10, pady=2)
        
        if tipos_logs:
            tk.Label(info_logs_frame, text="📂 Tipos de logs encontrados:", 
                     font=("Arial", 10, "bold")).pack(anchor='w', padx=10, pady=(10, 2))
            
            for tipo, count in tipos_logs.items():
                tk.Label(info_logs_frame, text=f"  • {tipo}: {count} arquivo(s)", 
                         font=("Arial", 9), fg="#666").pack(anchor='w', padx=20, pady=1)
        
        # Botões de ação
        buttons_frame = tk.Frame(frame_logs)
        buttons_frame.pack(pady=20)
        
        def abrir_gerenciador_completo():
            """Abre o gerenciador completo de logs"""
            try:
                abrir_gerenciador_logs(dev_win)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir gerenciador de logs:\n{e}")
        
        def abrir_pasta_logs():
            """Abre pasta de logs no explorador"""
            try:
                import os
                os.startfile(log_manager.log_dir)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir pasta de logs:\n{e}")
        
        def limpar_logs_antigos():
            """Limpa logs antigos"""
            try:
                import tkinter.simpledialog as simpledialog
                dias = simpledialog.askinteger(
                    "Limpar Logs Antigos",
                    "Excluir logs mais antigos que quantos dias?",
                    initialvalue=30,
                    minvalue=1,
                    maxvalue=365
                )
                
                if dias:
                    removidos = log_manager.limpar_logs_antigos(dias)
                    messagebox.showinfo("Concluído", 
                                      f"Removidos {removidos} logs antigos.\n"
                                      f"Backups criados automaticamente.")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao limpar logs:\n{e}")
        
        # Botões principais
        tk.Button(buttons_frame, text="🔧 Abrir Gerenciador Completo", 
                  command=abrir_gerenciador_completo,
                  bg="#3498db", fg="white", font=("Arial", 12, "bold"), 
                  height=2, width=25).pack(pady=5)
        
        tk.Button(buttons_frame, text="📁 Abrir Pasta de Logs", 
                  command=abrir_pasta_logs,
                  bg="#f39c12", fg="white", font=("Arial", 11, "bold"), 
                  height=2, width=25).pack(pady=5)
        
        tk.Button(buttons_frame, text="🧹 Limpar Logs Antigos", 
                  command=limpar_logs_antigos,
                  bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), 
                  height=2, width=25).pack(pady=5)
        
        # Visualização rápida dos últimos logs
        preview_frame = tk.LabelFrame(frame_logs, text="👁️ Visualização Rápida - Últimos Logs", 
                                     font=("Arial", 10, "bold"))
        preview_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Lista dos últimos logs
        logs_listbox = tk.Listbox(preview_frame, height=8, font=("Courier", 9))
        logs_scroll = tk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=logs_listbox.yview)
        logs_listbox.configure(yscrollcommand=logs_scroll.set)
        
        logs_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        logs_scroll.pack(side=tk.RIGHT, fill='y', pady=5)
        
        # Preencher lista com logs recentes
        for i, log_path in enumerate(logs_encontrados[:10]):  # Mostrar apenas os 10 mais recentes
            info_log = log_manager.obter_info_log(log_path)
            if 'erro' not in info_log:
                nome = info_log['nome']
                tipo = info_log['tipo']
                tamanho = f"{info_log['tamanho_kb']:.1f}KB"
                modificado = info_log['modificado_str']
                
                linha = f"{nome:<30} | {tipo:<10} | {tamanho:<8} | {modificado}"
                logs_listbox.insert(tk.END, linha)
        
        # ABA 6: COMANDOS PRIORITÁRIOS
        frame_priority = ttk.Frame(notebook_dev)
        notebook_dev.add(frame_priority, text="🚨 Comandos Prioritários")
        
        tk.Label(frame_priority, text="🚨 SISTEMA DE COMANDOS PRIORITÁRIOS", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(frame_priority, text="Comandos do desenvolvedor têm prioridade MÁXIMA e são executados imediatamente", 
                 font=("Arial", 10), fg="#e74c3c").pack(pady=5)
        
        # Inicializar sistema de prioridade se não estiver ativo
        maquina_atual = machine_config.obter_configuracao_maquina()
        sistema_prioridade = obter_sistema_prioridade()
        
        if not sistema_prioridade:
            try:
                sistema_prioridade = inicializar_sistema_prioridade(maquina_atual)
                print(f"🎯 Sistema de prioridade inicializado para máquina {maquina_atual}")
            except Exception as e:
                print(f"❌ Erro ao inicializar sistema de prioridade: {e}")
        
        # Status do sistema
        status_frame = tk.LabelFrame(frame_priority, text="📊 Status do Sistema de Prioridade", 
                                   font=("Arial", 10, "bold"))
        status_frame.pack(fill='x', padx=20, pady=10)
        
        def atualizar_status_prioridade():
            """Atualiza informações do sistema de prioridade"""
            if sistema_prioridade:
                status = sistema_prioridade.obter_status()
                
                status_text = f"""
🎯 Máquina: {status['maquina_id']}
⚡ Sistema Ativo: {'Sim' if sistema_prioridade.thread_monitor and sistema_prioridade.thread_monitor.is_alive() else 'Não'}
🔄 Executando: {'Sim' if status['executando'] else 'Não'}
📋 Comandos na Fila: {status['fila_comandos']}
📊 Total Executados: {status['total_executados']}
"""
                
                if 'comando_atual' in status and status['comando_atual']:
                    cmd_atual = status['comando_atual']
                    status_text += f"⚡ Comando Atual: {cmd_atual.get('acao', 'N/D')}\n"
                
                status_label.config(text=status_text)
            else:
                status_label.config(text="❌ Sistema de prioridade não inicializado")
        
        status_label = tk.Label(status_frame, text="Carregando...", font=("Courier", 9), 
                               justify='left', anchor='w')
        status_label.pack(anchor='w', padx=10, pady=5)
        
        # Botão para atualizar status
        tk.Button(status_frame, text="🔄 Atualizar Status", 
                  command=atualizar_status_prioridade,
                  bg="#17a2b8", fg="white", font=("Arial", 9)).pack(anchor='e', padx=10, pady=5)
        
        # Envio de comandos prioritários
        cmd_priority_frame = tk.LabelFrame(frame_priority, text="🚨 Enviar Comando Prioritário", 
                                         font=("Arial", 10, "bold"))
        cmd_priority_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(cmd_priority_frame, text="⚠️ ATENÇÃO: Comandos enviados aqui têm PRIORIDADE MÁXIMA", 
                 font=("Arial", 9, "bold"), fg="#e74c3c").pack(pady=5)
        
        # Seleção de comando prioritário
        cmd_frame = tk.Frame(cmd_priority_frame)
        cmd_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(cmd_frame, text="Comando:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=5)
        
        priority_cmd_var = tk.StringVar()
        priority_commands = [
            "fechar_app",
            "reiniciar_app", 
            "parar_sistema",
            "emergencia_parar",
            "diagnostico_completo",
            "obter_logs",
            "capturar_tela",
            "coletar_informacoes_sistema"
        ]
        
        priority_combo = ttk.Combobox(cmd_frame, textvariable=priority_cmd_var, 
                                    values=priority_commands, state="readonly", width=25)
        priority_combo.grid(row=0, column=1, padx=5)
        
        tk.Label(cmd_frame, text="Parâmetros:", font=("Arial", 10)).grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        
        priority_params_text = tk.Text(cmd_frame, width=40, height=4, font=("Courier", 9))
        priority_params_text.grid(row=1, column=1, padx=5, pady=5)
        priority_params_text.insert('1.0', '{}')
        
        def enviar_comando_prioritario():
            """Envia comando com prioridade máxima"""
            if not sistema_prioridade:
                messagebox.showerror("Erro", "Sistema de prioridade não está ativo!")
                return
            
            comando = priority_cmd_var.get()
            if not comando:
                messagebox.showerror("Erro", "Selecione um comando!")
                return
            
            try:
                params_str = priority_params_text.get('1.0', 'end').strip()
                parametros = json.loads(params_str) if params_str else {}
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Parâmetros JSON inválidos!")
                return
            
            try:
                comando_id = sistema_prioridade.enviar_comando_desenvolvedor(comando, parametros)
                
                messagebox.showinfo("✅ Comando Enviado", 
                                  f"Comando prioritário enviado!\n\n"
                                  f"🚨 Comando: {comando}\n"
                                  f"🆔 ID: {comando_id[:8]}...\n"
                                  f"⚡ Prioridade: MÁXIMA\n\n"
                                  f"O comando será executado IMEDIATAMENTE!")
                
                # Atualizar status
                atualizar_status_prioridade()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao enviar comando:\n{e}")
        
        tk.Button(cmd_priority_frame, text="🚨 ENVIAR COMANDO PRIORITÁRIO", 
                  command=enviar_comando_prioritario,
                  bg="#dc3545", fg="white", font=("Arial", 12, "bold"), 
                  height=2, width=30).pack(pady=15)
        
        # Log de comandos executados
        log_frame = tk.LabelFrame(frame_priority, text="📜 Log de Comandos Executados", 
                                font=("Arial", 10, "bold"))
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Lista de comandos
        cmd_log_listbox = tk.Listbox(log_frame, height=8, font=("Courier", 8))
        cmd_log_scroll = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=cmd_log_listbox.yview)
        cmd_log_listbox.configure(yscrollcommand=cmd_log_scroll.set)
        
        cmd_log_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        cmd_log_scroll.pack(side=tk.RIGHT, fill='y', pady=5)
        
        def atualizar_log_comandos():
            """Atualiza log de comandos executados"""
            cmd_log_listbox.delete(0, tk.END)
            
            if sistema_prioridade:
                comandos = sistema_prioridade.obter_log_comandos(20)  # Últimos 20
                
                for cmd in reversed(comandos):  # Mais recentes primeiro
                    acao = cmd.get('acao', 'N/D')
                    status = cmd.get('status', 'N/D')
                    tempo = cmd.get('tempo_execucao', 0)
                    prioridade = cmd.get('prioridade', 0)
                    
                    # Emoji baseado no status
                    emoji = "✅" if status == "sucesso" else "❌"
                    
                    # Emoji baseado na prioridade
                    if prioridade >= 100:
                        priority_emoji = "🚨"
                    elif prioridade >= 10:
                        priority_emoji = "⚡"
                    else:
                        priority_emoji = "📝"
                    
                    linha = f"{emoji} {priority_emoji} {acao:<20} | {status:<8} | {tempo:.3f}s"
                    cmd_log_listbox.insert(tk.END, linha)
        
        # Botão para atualizar log
        tk.Button(log_frame, text="🔄 Atualizar Log", 
                  command=atualizar_log_comandos,
                  bg="#28a745", fg="white", font=("Arial", 9)).pack(anchor='e', padx=5, pady=2)
        
        # Atualizar status inicial
        atualizar_status_prioridade()
        atualizar_log_comandos()
        
        # Centralizar janela
        dev_win.update_idletasks()
        x = (dev_win.winfo_screenwidth() - dev_win.winfo_width()) // 2
        y = (dev_win.winfo_screenheight() - dev_win.winfo_height()) // 2
        dev_win.geometry(f"+{x}+{y}")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir painel do desenvolvedor: {e}")
        import traceback
        traceback.print_exc()
