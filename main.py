"""
Sistema de Coleta de Produção Industrial
Aplicação principal para coleta e registro de dados de produção
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import warnings

warnings.filterwarnings('ignore')
os.environ['TK_SILENCE_DEPRECATION'] = '1'

print("🚀 Iniciando sistema otimizado...")

from config import CAMINHO_REDE, CAMINHO_LOCAL, VERSION
from data.manager import DataManager
from models.machine import MachineConfig
from models.batch import BatchConfig
from models.user import UserManager
from utils.logger import registrar_acao, set_log_manager
from utils.machine_id import gerar_id_computador_avancado
from utils.paths import testar_acesso_rede, garantir_arquivo_rede
import pandas as pd
import gui.auth
from gui.dev_panel_completo import abrir_painel_desenvolvedor_completo
from gui.user_manager import gerenciar_usuarios
from gui.registro_fixo import criar_janela_registro_fixa
from gui.painel_admin import abrir_painel_admin
from utils.comunicacao import sistema_comunicacao
from utils.auditoria import auditar_acesso_painel

ID_COMPUTADOR = gerar_id_computador_avancado()
print(f"🆔 ID Máquina: {ID_COMPUTADOR[:16]}...")

data_manager = DataManager()
set_log_manager(data_manager)

machine_config = MachineConfig()
batch_config = BatchConfig()
user_manager = UserManager(data_manager)

def diagnostico_inicial():
    """Diagnóstico inicial do sistema"""
    print("🔍 DIAGNÓSTICO INICIAL DO SISTEMA")
    print(f"✅ Python: {sys.version}")
    print(f"✅ Diretório atual: {os.getcwd()}")
    print(f"✅ Caminho do executável: {sys.executable if getattr(sys, 'frozen', False) else 'Rodando como .py'}")
    print(f"✅ Caminho base: {CAMINHO_LOCAL}")
    print(f"✅ Acesso à rede: {'SIM' if testar_acesso_rede() else 'NÃO'}")
    print(f"✅ Caminho rede: {CAMINHO_REDE if os.path.exists(CAMINHO_REDE) else 'Não acessível'}")
    print("🔍 Fim do diagnóstico")

def configurar_maquina_inicial():
    """Configura a máquina antes de qualquer operação"""
    maquina_configurada = machine_config.obter_configuracao_maquina()
    if maquina_configurada:
        print(f"✅ Máquina já configurada: {maquina_configurada}")
        return True
    
    print("🔄 Configurando máquina pela primeira vez...")
    
    janela_config = tk.Toplevel()
    janela_config.title("🔧 Configuração Inicial da Máquina")
    janela_config.geometry("500x400")
    janela_config.attributes('-topmost', True)
    janela_config.grab_set()
    janela_config.protocol("WM_DELETE_WINDOW", lambda: None)
    
    frame_principal = tk.Frame(janela_config)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="🔧 CONFIGURAÇÃO INICIAL DA MÁQUINA", 
             font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=10)
    
    tk.Label(frame_principal, text="Selecione qual máquina esta é:", 
             font=("Arial", 12)).pack(pady=10)
    
    from config.constants import TABELA_SIZES
    opcoes_maquina = list(TABELA_SIZES.keys()) + ["DESENVOLVEDOR", "COORDENADOR", "ENCARREGADO", "ANALISTA", "OPERADOR"]
    
    maquina_var = tk.StringVar()
    combo_maquina = ttk.Combobox(frame_principal, textvariable=maquina_var,
                                 values=opcoes_maquina, 
                                 state="readonly", 
                                 font=("Arial", 12))
    combo_maquina.pack(pady=10, fill='x')
    combo_maquina.focus()
    
    resultado = [False]
    
    def confirmar():
        maquina_selecionada = maquina_var.get().strip()
        if not maquina_selecionada:
            tk.messagebox.showwarning("Aviso", "Selecione uma máquina!")
            return
        
        if machine_config.salvar_configuracao_maquina(maquina_selecionada):
            if maquina_selecionada in TABELA_SIZES:
                size_config = {
                    'maquina': maquina_selecionada,
                    'size': TABELA_SIZES[maquina_selecionada]['size'],
                    'peso': TABELA_SIZES[maquina_selecionada]['peso']
                }
            else:
                size_config = {
                    'maquina': maquina_selecionada,
                    'size': '#0',
                    'peso': 0.000096
                }
            machine_config.salvar_configuracao_size(size_config)
            resultado[0] = True
            janela_config.destroy()
    
    tk.Button(frame_principal, text="✅ Confirmar", command=confirmar,
             bg="#28a745", fg="white", font=("Arial", 12, "bold"),
             height=2, width=25).pack(pady=20)
    
    janela_config.bind('<Return>', lambda e: confirmar())
    janela_config.update_idletasks()
    x = (janela_config.winfo_screenwidth() - janela_config.winfo_width()) // 2
    y = (janela_config.winfo_screenheight() - janela_config.winfo_height()) // 2
    janela_config.geometry(f"+{x}+{y}")
    
    janela_config.wait_window()
    return resultado[0]

def diagnostico_inicial():
    """Diagnóstico inicial do sistema"""
    print("🔍 DIAGNÓSTICO INICIAL DO SISTEMA")
    print(f"✅ Python: {sys.version}")
    print(f"✅ Diretório atual: {os.getcwd()}")
    print(f"✅ Caminho do executável: {sys.executable if getattr(sys, 'frozen', False) else 'Rodando como .py'}")
    print(f"✅ Caminho base: {CAMINHO_LOCAL}")
    print(f"✅ Acesso à rede: {'SIM' if testar_acesso_rede() else 'NÃO'}")
    print(f"✅ Caminho rede: {CAMINHO_REDE if os.path.exists(CAMINHO_REDE) else 'Não acessível'}")
    print("🔍 Fim do diagnóstico")

if __name__ == "__main__":
    try:
        print("🔧 Iniciando aplicação...")
        
        # Inicializar arquivos (tenta rede, fallback local)
        try:
            data_manager.inicializar_arquivos()
            print(f"✅ Usuários carregados: {len(data_manager.df_users)}")
        except Exception as e:
            print(f"❌ ERRO ao inicializar arquivos: {e}")
            try:
                messagebox.showerror("Erro Crítico", 
                                   f"Não foi possível inicializar o sistema!\n\n"
                                   f"Erro: {e}")
            except:
                print("❌ Não foi possível mostrar mensagem de erro")
            sys.exit(1)
        
        diagnostico_inicial()
        
        if not configurar_maquina_inicial():
            print("❌ Falha na configuração inicial. Encerrando...")
            sys.exit(1)
        
        MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
        CONFIG_SIZE = machine_config.obter_configuracao_size()
        
        print(f"✅ Máquina configurada: {MAQUINA_ATUAL}")
        print(f"📏 Size: {CONFIG_SIZE['size']} | Peso: {CONFIG_SIZE['peso']}")
        
        root = tk.Tk()
        root.title(f"Coletor de Produção v{VERSION} - Máquina {MAQUINA_ATUAL}")
        root.geometry("600x700")
        root.configure(bg='#ecf0f1')
        
        # Frame principal com scroll
        main_frame = tk.Frame(root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="COLETOR DE PRODUÇÃO", 
                 font=("Arial", 18, "bold"), fg="white", bg='#2c3e50').pack(expand=True)
        tk.Label(header_frame, text=f"v{VERSION}", 
                 font=("Arial", 9), fg="#ecf0f1", bg='#2c3e50').pack()
        
        # Informações da máquina
        info_card = tk.LabelFrame(main_frame, text="📊 Informações da Máquina", 
                                  font=("Arial", 11, "bold"), bg='white', fg='#2c3e50')
        info_card.pack(fill='x', pady=(0, 15))
        
        info_content = tk.Frame(info_card, bg='white')
        info_content.pack(fill='x', padx=15, pady=10)
        
        tk.Label(info_content, text=f"🏭 Máquina: {MAQUINA_ATUAL}", 
                 font=("Arial", 11, "bold"), bg='white', fg='#2c3e50').pack(anchor='w', pady=2)
        tk.Label(info_content, text=f"📏 Size: {CONFIG_SIZE['size']} | Peso: {CONFIG_SIZE['peso']}", 
                 font=("Arial", 10), bg='white', fg='#e74c3c').pack(anchor='w', pady=2)
        tk.Label(info_content, text=f"👥 Usuários: {len(data_manager.df_users)} cadastrados", 
                 font=("Arial", 9), bg='white', fg='#7f8c8d').pack(anchor='w', pady=2)
        tk.Label(info_content, text="🟢 Sistema Ativo", 
                 font=("Arial", 9, "bold"), bg='white', fg='#27ae60').pack(anchor='w', pady=2)
        
        # Botões principais
        botoes_card = tk.LabelFrame(main_frame, text="🎯 Ações Principais", 
                                    font=("Arial", 11, "bold"), bg='white', fg='#2c3e50')
        botoes_card.pack(fill='x', pady=(0, 15))
        
        botoes_content = tk.Frame(botoes_card, bg='white')
        botoes_content.pack(fill='x', padx=15, pady=10)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 25, "height": 2}
        
        def abrir_registro_producao():
            from gui.registro_fixo import criar_janela_registro_fixa
            criar_janela_registro_fixa(root, machine_config, batch_config, data_manager)
        
        tk.Button(botoes_content, text="📝 Registrar Produção", 
                 command=abrir_registro_producao,
                 bg="#27ae60", fg="white", **btn_style).pack(pady=5, fill='x')
        
        def configurar_lote_manual():
            from gui.registro_fixo import solicitar_novo_lote
            if solicitar_novo_lote(root, machine_config, batch_config):
                messagebox.showinfo("Sucesso", "✅ Lote configurado com sucesso!")
        
        tk.Button(botoes_content, text="📦 Configurar Lote", 
                 command=configurar_lote_manual,
                 bg="#3498db", fg="white", **btn_style).pack(pady=5, fill='x')
        
        tk.Button(botoes_content, text="📊 Dashboard", 
                 command=lambda: abrir_dashboard(),
                 bg="#9b59b6", fg="white", **btn_style).pack(pady=5, fill='x')
        
        # Painel administrativo
        admin_card = tk.LabelFrame(main_frame, text="⚙️ Administração", 
                                   font=("Arial", 11, "bold"), bg='white', fg='#2c3e50')
        admin_card.pack(fill='x', pady=(0, 15))
        
        admin_content = tk.Frame(admin_card, bg='white')
        admin_content.pack(fill='x', padx=15, pady=10)
        
        btn_admin_style = {"font": ("Arial", 10), "width": 25, "height": 1}
        
        def abrir_painel_dev():
            if gui.auth.verificar_senha_desenvolvedor(root, data_manager):
                abrir_painel_desenvolvedor_completo(root, data_manager, machine_config, batch_config)
        
        tk.Button(admin_content, text="💻 Painel Desenvolvedor", 
                 command=abrir_painel_dev,
                 bg="#e74c3c", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        def abrir_gerenciar_usuarios():
            if gui.auth.verificar_senha_desenvolvedor(root, data_manager):
                gerenciar_usuarios(root, data_manager)
        
        tk.Button(admin_content, text="👥 Gerenciar Usuários", 
                 command=abrir_gerenciar_usuarios,
                 bg="#f39c12", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        def abrir_painel_administrativo():
            # Painel admin já tem autenticação interna
            abrir_painel_admin(root, data_manager, machine_config, batch_config)
        
        tk.Button(admin_content, text="👔 Painel Administrativo", 
                 command=abrir_painel_administrativo,
                 bg="#9b59b6", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        tk.Button(admin_content, text="🔧 Configurar Máquina", 
                 command=configurar_maquina_inicial,
                 bg="#95a5a6", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        tk.Button(admin_content, text="📋 Ver Logs", 
                 command=lambda: messagebox.showinfo("Logs", f"Total: {len(data_manager.df_log)} registros"),
                 bg="#34495e", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        def abrir_ia():
            from gui.painel_ia import abrir_painel_ia
            abrir_painel_ia(root, data_manager, machine_config)
        
        tk.Button(admin_content, text="🤖 Inteligência Artificial", 
                 command=abrir_ia,
                 bg="#6f42c1", fg="white", **btn_admin_style).pack(pady=3, fill='x')
        
        # Controles do sistema
        controles_frame = tk.Frame(main_frame, bg='#ecf0f1')
        controles_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(controles_frame, text="📋 Minimizar", 
                 command=lambda: root.withdraw(),
                 bg="#95a5a6", fg="white", font=("Arial", 9), width=15).pack(side='left', padx=5)
        
        tk.Button(controles_frame, text="🔄 Atualizar", 
                 command=lambda: messagebox.showinfo("Atualizar", "Dados atualizados!"),
                 bg="#3498db", fg="white", font=("Arial", 9), width=15).pack(side='left', padx=5)
        
        tk.Button(controles_frame, text="❌ Sair", 
                 command=root.quit,
                 bg="#e74c3c", fg="white", font=("Arial", 9), width=15).pack(side='right', padx=5)
        
        def abrir_dashboard():
            """Abre o dashboard em subprocess"""
            try:
                import subprocess
                import os
                dash_path = os.path.join(os.path.dirname(__file__), "dash.py")
                if os.path.exists(dash_path):
                    subprocess.Popen(["python", dash_path])
                    messagebox.showinfo("Dashboard", "Dashboard iniciado em nova janela!")
                else:
                    messagebox.showerror("Erro", f"Arquivo dash.py não encontrado em:\n{dash_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir dashboard: {e}")
        
        # Iniciar sistema de comunicação em tempo real
        sistema_comunicacao.set_root_reference(root)
        sistema_comunicacao.set_configs(machine_config, batch_config, data_manager)
        sistema_comunicacao.iniciar_sistema_comunicacao()
        
        # Criar janela de registro FIXA (NUNCA FECHA)
        criar_janela_registro_fixa(root, machine_config, batch_config, data_manager)
        
        print("✅ Sistema carregado com sucesso!")
        print(f"👥 Usuários disponíveis: {len(data_manager.df_users)}")
        print(f"📊 Interface completa carregada")
        print(f"🔗 Sistema de comunicação ativo (verificando comandos a cada 1ms)")
        print(f"📝 Janela de registro FIXA criada (SEMPRE VISÍVEL)")
        
        root.mainloop()
        
        # Parar comunicação ao fechar
        sistema_comunicacao.parar_sistema_comunicacao()
        
    except KeyboardInterrupt:
        print("\n⚠️ Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
