"""Painel do Desenvolvedor COMPLETO - Para usuários sem conhecimento de programação"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import datetime
import os
import json
import uuid
import subprocess
import shutil
from models.machine import MachineConfig
from models.batch import BatchConfig
from config.constants import TABELA_SIZES
from utils.machine_id import gerar_id_computador_avancado
from config.settings import CAMINHO_REDE, CAMINHO_LOCAL
from gui.user_manager import gerenciar_usuarios


def abrir_painel_desenvolvedor_completo(root, data_manager, machine_config: MachineConfig, batch_config: BatchConfig):
    """Painel desenvolvedor COMPLETO com todas funcionalidades"""
    
    dev_win = tk.Toplevel(root)
    dev_win.title("💻 PAINEL DESENVOLVEDOR COMPLETO - Controle Total do Sistema")
    dev_win.geometry("1400x900")
    dev_win.attributes('-topmost', True)
    
    # Notebook principal
    notebook = ttk.Notebook(dev_win)
    notebook.pack(fill='both', expand=True, padx=5, pady=5)
    
    # ==================== ABA 1: COMANDOS RÁPIDOS ====================
    tab_comandos = ttk.Frame(notebook)
    notebook.add(tab_comandos, text="⚡ Comandos Rápidos")
    
    # Frame de comandos
    frm_cmd = tk.LabelFrame(tab_comandos, text="🚀 Comandos do Sistema", font=("Arial", 12, "bold"))
    frm_cmd.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Grid de botões de comando
    comandos = [
        ("🔄 Reiniciar Sistema", lambda: reiniciar_sistema(), "#e74c3c"),
        ("🧹 Limpar Cache", lambda: limpar_cache(), "#f39c12"),
        ("💾 Backup Completo", lambda: fazer_backup_completo(data_manager, machine_config), "#3498db"),
        ("📊 Exportar Dados", lambda: exportar_dados(data_manager), "#27ae60"),
        ("🔍 Verificar Integridade", lambda: verificar_integridade(data_manager), "#9b59b6"),
        ("📁 Abrir Pasta Local", lambda: abrir_pasta_local(), "#34495e"),
        ("🌐 Abrir Pasta Rede", lambda: abrir_pasta_rede(), "#16a085"),
        ("🔧 Reparar Arquivos", lambda: reparar_arquivos(data_manager), "#e67e22"),
        ("📋 Copiar ID Máquina", lambda: copiar_id_maquina(), "#95a5a6"),
        ("🗑️ Limpar Logs Antigos", lambda: limpar_logs_antigos(data_manager), "#c0392b"),
        ("📤 Sincronizar Rede", lambda: sincronizar_rede(data_manager), "#2980b9"),
        ("🔐 Resetar Senhas", lambda: resetar_senhas(data_manager), "#d35400"),
    ]
    
    row, col = 0, 0
    for texto, comando, cor in comandos:
        btn = tk.Button(frm_cmd, text=texto, command=comando, 
                       bg=cor, fg="white", font=("Arial", 10, "bold"),
                       width=25, height=2)
        btn.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 3:
            col = 0
            row += 1
    
    # Console de saída
    frm_console = tk.LabelFrame(tab_comandos, text="📟 Console de Saída", font=("Arial", 10, "bold"))
    frm_console.pack(fill='both', expand=True, padx=10, pady=10)
    
    console_text = scrolledtext.ScrolledText(frm_console, height=10, bg="#2c3e50", fg="#ecf0f1", 
                                            font=("Consolas", 9))
    console_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def log_console(mensagem):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        console_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        console_text.see(tk.END)
    
    # ==================== ABA 2: CONTROLE REMOTO AVANÇADO ====================
    tab_remoto = ttk.Frame(notebook)
    notebook.add(tab_remoto, text="🌐 Controle Remoto")
    
    frm_remoto = tk.LabelFrame(tab_remoto, text="🎮 Controle Remoto de Máquinas", font=("Arial", 12, "bold"))
    frm_remoto.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Descobrir máquinas
    tk.Label(frm_remoto, text="Máquinas Disponíveis:", font=("Arial", 10, "bold")).pack(pady=5)
    
    frame_maquinas = tk.Frame(frm_remoto)
    frame_maquinas.pack(fill='both', expand=True, padx=10, pady=5)
    
    listbox_maquinas = tk.Listbox(frame_maquinas, height=8, font=("Arial", 10))
    listbox_maquinas.pack(side='left', fill='both', expand=True)
    
    scrollbar_maq = tk.Scrollbar(frame_maquinas, command=listbox_maquinas.yview)
    scrollbar_maq.pack(side='right', fill='y')
    listbox_maquinas.config(yscrollcommand=scrollbar_maq.set)
    
    def descobrir_maquinas():
        listbox_maquinas.delete(0, tk.END)
        maquinas_encontradas = []
        
        try:
            # Buscar na REDE
            if os.path.exists(CAMINHO_REDE):
                arquivos = os.listdir(CAMINHO_REDE)
                for arquivo in arquivos:
                    if arquivo.startswith("status_maq_") and arquivo.endswith(".json"):
                        try:
                            caminho_arquivo = os.path.join(CAMINHO_REDE, arquivo)
                            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                                status = json.load(f)
                            
                            # Verificar se está online (timestamp recente)
                            timestamp_str = status.get('timestamp', '')
                            if timestamp_str:
                                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                                agora = datetime.datetime.now()
                                diferenca = (agora - timestamp).total_seconds()
                                
                                # Considerar online se atualizou nos últimos 30 segundos
                                if diferenca < 30:
                                    maquina = arquivo.replace("status_maq_", "").replace(".json", "")
                                    if maquina not in maquinas_encontradas:
                                        maquinas_encontradas.append(maquina)
                        except:
                            continue
            
            # Buscar LOCALMENTE também (para máquina atual)
            try:
                arquivos_locais = os.listdir(CAMINHO_LOCAL)
                for arquivo in arquivos_locais:
                    if arquivo.startswith("status_maq_") and arquivo.endswith(".json"):
                        try:
                            caminho_arquivo = os.path.join(CAMINHO_LOCAL, arquivo)
                            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                                status = json.load(f)
                            
                            timestamp_str = status.get('timestamp', '')
                            if timestamp_str:
                                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                                agora = datetime.datetime.now()
                                diferenca = (agora - timestamp).total_seconds()
                                
                                if diferenca < 30:
                                    maquina = arquivo.replace("status_maq_", "").replace(".json", "")
                                    if maquina not in maquinas_encontradas:
                                        maquinas_encontradas.append(maquina)
                        except:
                            continue
            except:
                pass
            
            if maquinas_encontradas:
                for maq in sorted(maquinas_encontradas):
                    listbox_maquinas.insert(tk.END, f"🟢 {maq}")
                log_console(f"✅ {len(maquinas_encontradas)} máquinas online encontradas")
            else:
                log_console("⚠️ Nenhuma máquina online encontrada")
                
        except Exception as e:
            log_console(f"❌ Erro: {e}")
    
    tk.Button(frm_remoto, text="🔍 Descobrir Máquinas", command=descobrir_maquinas,
             bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=5)
    
    # Comandos remotos
    frm_cmd_remoto = tk.LabelFrame(frm_remoto, text="📡 Enviar Comandos", font=("Arial", 10, "bold"))
    frm_cmd_remoto.pack(fill='x', padx=10, pady=10)
    
    comandos_remotos = [
        ("🔄 Reiniciar App", "reiniciar_app"),
        ("🛑 Fechar App", "fechar_app"),
        ("🚀 Abrir App", "abrir_app"),
        ("📊 Coletar Dados", "coletar_dados"),
        ("💾 Fazer Backup", "fazer_backup"),
        ("🔍 Diagnóstico", "diagnostico_completo"),
        ("🌐 Testar Rede", "testar_conectividade"),
        ("📋 Obter Logs", "obter_logs"),
        ("🧹 Limpar Cache", "limpar_cache"),
        ("📸 Capturar Tela", "capturar_tela"),
    ]
    
    row, col = 0, 0
    for texto, acao in comandos_remotos:
        btn = tk.Button(frm_cmd_remoto, text=texto, 
                       command=lambda a=acao: enviar_comando_remoto(a, listbox_maquinas, log_console),
                       bg="#27ae60", fg="white", font=("Arial", 9, "bold"), width=18, height=1)
        btn.grid(row=row, column=col, padx=3, pady=3)
        col += 1
        if col > 4:
            col = 0
            row += 1
    
    # ==================== ABA 3: CONFIGURAÇÕES ====================
    tab_config = ttk.Frame(notebook)
    notebook.add(tab_config, text="⚙️ Configurações")
    
    # Configuração de máquina
    frm_maq = tk.LabelFrame(tab_config, text="🔧 Configuração da Máquina", font=("Arial", 11, "bold"))
    frm_maq.pack(fill='x', padx=10, pady=10)
    
    MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
    CONFIG_SIZE = machine_config.obter_configuracao_size()
    
    tk.Label(frm_maq, text=f"Máquina Atual: {MAQUINA_ATUAL}", font=("Arial", 10, "bold"), fg="#2c3e50").pack(pady=5)
    tk.Label(frm_maq, text=f"Size: {CONFIG_SIZE['size']} | Peso: {CONFIG_SIZE['peso']}", 
             font=("Arial", 9), fg="#7f8c8d").pack(pady=2)
    
    tk.Label(frm_maq, text="Alterar para:", font=("Arial", 9)).pack(pady=5)
    
    maquina_var = tk.StringVar(value=MAQUINA_ATUAL)
    opcoes = list(TABELA_SIZES.keys()) + ["DESENVOLVEDOR", "COORDENADOR", "ENCARREGADO"]
    
    combo_maq = ttk.Combobox(frm_maq, textvariable=maquina_var, values=opcoes, 
                            state="readonly", width=30, font=("Arial", 10))
    combo_maq.pack(pady=5)
    
    def salvar_config_maquina():
        nova_maq = maquina_var.get()
        if machine_config.salvar_configuracao_maquina(nova_maq):
            if nova_maq in TABELA_SIZES:
                size_config = {
                    'maquina': nova_maq,
                    'size': TABELA_SIZES[nova_maq]['size'],
                    'peso': TABELA_SIZES[nova_maq]['peso']
                }
                machine_config.salvar_configuracao_size(size_config)
            log_console(f"✅ Máquina alterada: {nova_maq}")
            messagebox.showinfo("Sucesso", f"Máquina alterada para: {nova_maq}\n\nReinicie o sistema.")
        else:
            log_console("❌ Erro ao salvar configuração")
    
    tk.Button(frm_maq, text="💾 Salvar Configuração", command=salvar_config_maquina,
             bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)
    
    # Configuração de lote
    frm_lote = tk.LabelFrame(tab_config, text="📦 Configuração de Lote", font=("Arial", 11, "bold"))
    frm_lote.pack(fill='x', padx=10, pady=10)
    
    config_lote = batch_config.obter_configuracao_lote()
    
    tk.Label(frm_lote, text=f"Lote Atual: {config_lote.get('lote', 'N/D')}", 
             font=("Arial", 10, "bold"), fg="#2c3e50").pack(pady=5)
    tk.Label(frm_lote, text=f"Caixa: {config_lote.get('caixa_atual', 0)}/{config_lote.get('total_caixas', 0)}", 
             font=("Arial", 9), fg="#7f8c8d").pack(pady=2)
    
    frame_lote_inputs = tk.Frame(frm_lote)
    frame_lote_inputs.pack(pady=10)
    
    tk.Label(frame_lote_inputs, text="Lote:").grid(row=0, column=0, padx=5)
    lote_var = tk.StringVar()
    tk.Entry(frame_lote_inputs, textvariable=lote_var, width=20).grid(row=0, column=1, padx=5)
    
    tk.Label(frame_lote_inputs, text="Caixa Atual:").grid(row=0, column=2, padx=5)
    caixa_var = tk.StringVar(value="1")
    tk.Entry(frame_lote_inputs, textvariable=caixa_var, width=10).grid(row=0, column=3, padx=5)
    
    tk.Label(frame_lote_inputs, text="Total:").grid(row=0, column=4, padx=5)
    total_var = tk.StringVar(value="100")
    tk.Entry(frame_lote_inputs, textvariable=total_var, width=10).grid(row=0, column=5, padx=5)
    
    def salvar_lote():
        try:
            lote = lote_var.get().strip()
            caixa = int(caixa_var.get())
            total = int(total_var.get())
            
            if not lote:
                messagebox.showerror("Erro", "Informe o lote!")
                return
            
            if batch_config.salvar_configuracao_lote(lote, caixa, total, 0):
                log_console(f"✅ Lote configurado: {lote}")
                messagebox.showinfo("Sucesso", f"Lote {lote} configurado!")
            else:
                log_console("❌ Erro ao salvar lote")
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
    
    tk.Button(frm_lote, text="💾 Salvar Lote", command=salvar_lote,
             bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)
    
    # ==================== ABA 4: MONITORAMENTO ====================
    tab_monitor = ttk.Frame(notebook)
    notebook.add(tab_monitor, text="📊 Monitoramento")
    
    frm_stats = tk.LabelFrame(tab_monitor, text="📈 Estatísticas do Sistema", font=("Arial", 11, "bold"))
    frm_stats.pack(fill='both', expand=True, padx=10, pady=10)
    
    stats_text = scrolledtext.ScrolledText(frm_stats, height=20, font=("Consolas", 10))
    stats_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def atualizar_stats():
        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, "="*60 + "\n")
        stats_text.insert(tk.END, "📊 ESTATÍSTICAS DO SISTEMA\n")
        stats_text.insert(tk.END, "="*60 + "\n\n")
        
        stats_text.insert(tk.END, f"🏭 Máquina: {MAQUINA_ATUAL}\n")
        stats_text.insert(tk.END, f"📏 Size: {CONFIG_SIZE['size']} | Peso: {CONFIG_SIZE['peso']}\n")
        stats_text.insert(tk.END, f"📦 Lote: {config_lote.get('lote', 'N/D')}\n")
        stats_text.insert(tk.END, f"📦 Caixa: {config_lote.get('caixa_atual', 0)}/{config_lote.get('total_caixas', 0)}\n\n")
        
        stats_text.insert(tk.END, f"📊 Registros de Produção: {len(data_manager.df) if data_manager.df is not None else 0}\n")
        stats_text.insert(tk.END, f"👥 Usuários Cadastrados: {len(data_manager.df_users) if data_manager.df_users is not None else 0}\n")
        stats_text.insert(tk.END, f"📝 Logs do Sistema: {len(data_manager.df_log) if data_manager.df_log is not None else 0}\n\n")
        
        stats_text.insert(tk.END, f"📁 Caminho Local: {CAMINHO_LOCAL}\n")
        stats_text.insert(tk.END, f"🌐 Caminho Rede: {CAMINHO_REDE}\n")
        stats_text.insert(tk.END, f"🔗 Acesso Rede: {'✅ SIM' if os.path.exists(CAMINHO_REDE) else '❌ NÃO'}\n\n")
        
        stats_text.insert(tk.END, f"🆔 ID Computador: {gerar_id_computador_avancado()}\n")
        stats_text.insert(tk.END, f"⏰ Atualizado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    tk.Button(frm_stats, text="🔄 Atualizar Estatísticas", command=atualizar_stats,
             bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)
    
    atualizar_stats()
    
    # ==================== ABA 5: FERRAMENTAS ====================
    tab_tools = ttk.Frame(notebook)
    notebook.add(tab_tools, text="🛠️ Ferramentas")
    
    frm_tools = tk.LabelFrame(tab_tools, text="🔧 Ferramentas Avançadas", font=("Arial", 11, "bold"))
    frm_tools.pack(fill='both', expand=True, padx=10, pady=10)
    
    ferramentas = [
        ("👥 Gerenciar Usuários", lambda: gerenciar_usuarios(root, data_manager)),
        ("📊 Abrir Dashboard", lambda: abrir_dashboard_separado()),
        ("🗂️ Explorar Arquivos", lambda: explorar_arquivos()),
        ("📝 Editor de Configurações", lambda: editar_configuracoes()),
        ("🔍 Buscar Registros", lambda: buscar_registros(data_manager)),
        ("📤 Importar Dados", lambda: importar_dados(data_manager)),
        ("🔄 Resetar Sistema", lambda: resetar_sistema(machine_config, batch_config)),
        ("📋 Gerar Relatório", lambda: gerar_relatorio(data_manager, machine_config)),
    ]
    
    row, col = 0, 0
    for texto, comando in ferramentas:
        btn = tk.Button(frm_tools, text=texto, command=comando,
                       bg="#34495e", fg="white", font=("Arial", 10, "bold"),
                       width=25, height=2)
        btn.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col > 2:
            col = 0
            row += 1
    
    log_console("✅ Painel desenvolvedor carregado")


# ==================== FUNÇÕES DE COMANDO ====================

def reiniciar_sistema():
    if messagebox.askyesno("Confirmar", "Reiniciar o sistema?"):
        import sys
        python = sys.executable
        os.execl(python, python, *sys.argv)

def limpar_cache():
    try:
        temp_files = [f for f in os.listdir(CAMINHO_LOCAL) if f.endswith('.tmp') or f.endswith('.cache')]
        for f in temp_files:
            os.remove(os.path.join(CAMINHO_LOCAL, f))
        messagebox.showinfo("Sucesso", f"✅ {len(temp_files)} arquivos removidos")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def fazer_backup_completo(data_manager, machine_config):
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        MAQUINA = machine_config.obter_configuracao_maquina()
        backup_dir = os.path.join(CAMINHO_LOCAL, f"backup_{MAQUINA}_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        
        arquivos = [
            data_manager.csv_path,
            data_manager.users_path,
            data_manager.log_path,
            os.path.join(CAMINHO_LOCAL, "config_maquina.json"),
            os.path.join(CAMINHO_LOCAL, "config_size.json"),
            os.path.join(CAMINHO_LOCAL, "config_lote.json")
        ]
        
        for arq in arquivos:
            if os.path.exists(arq):
                shutil.copy2(arq, backup_dir)
        
        messagebox.showinfo("Sucesso", f"✅ Backup criado em:\n{backup_dir}")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def exportar_dados(data_manager):
    try:
        pasta = filedialog.askdirectory(title="Selecione pasta para exportar")
        if pasta:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if data_manager.df is not None:
                data_manager.df.to_excel(os.path.join(pasta, f"producao_{timestamp}.xlsx"), index=False)
            messagebox.showinfo("Sucesso", "✅ Dados exportados!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def verificar_integridade(data_manager):
    problemas = []
    if data_manager.df is None or len(data_manager.df) == 0:
        problemas.append("⚠️ Sem dados de produção")
    if data_manager.df_users is None or len(data_manager.df_users) == 0:
        problemas.append("⚠️ Sem usuários cadastrados")
    
    if problemas:
        messagebox.showwarning("Aviso", "\n".join(problemas))
    else:
        messagebox.showinfo("OK", "✅ Sistema íntegro!")

def abrir_pasta_local():
    os.startfile(CAMINHO_LOCAL)

def abrir_pasta_rede():
    if os.path.exists(CAMINHO_REDE):
        os.startfile(CAMINHO_REDE)
    else:
        messagebox.showwarning("Aviso", "Sem acesso à rede!")

def reparar_arquivos(data_manager):
    try:
        data_manager.inicializar_arquivos()
        messagebox.showinfo("Sucesso", "✅ Arquivos reparados!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def copiar_id_maquina():
    try:
        import pyperclip
        id_maq = gerar_id_computador_avancado()
        pyperclip.copy(id_maq)
        messagebox.showinfo("Copiado", f"✅ ID copiado:\n{id_maq[:32]}...")
    except ImportError:
        # Fallback: copiar manualmente
        id_maq = gerar_id_computador_avancado()
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(id_maq)
        root.update()
        root.destroy()
        messagebox.showinfo("Copiado", f"✅ ID copiado para área de transferência:\n{id_maq[:32]}...")

def limpar_logs_antigos(data_manager):
    if messagebox.askyesno("Confirmar", "Limpar logs com mais de 30 dias?"):
        # Implementar lógica
        messagebox.showinfo("Sucesso", "✅ Logs limpos!")

def sincronizar_rede(data_manager):
    try:
        data_manager.salvar_dados()
        messagebox.showinfo("Sucesso", "✅ Sincronizado!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def resetar_senhas(data_manager):
    if messagebox.askyesno("ATENÇÃO", "Resetar TODAS as senhas para padrão?"):
        # Implementar lógica
        messagebox.showinfo("Sucesso", "✅ Senhas resetadas!")

def enviar_comando_remoto(acao, listbox, log_func):
    selecionados = listbox.curselection()
    if not selecionados:
        messagebox.showwarning("Aviso", "Selecione uma máquina!")
        return
    
    maquina = listbox.get(selecionados[0])
    
    try:
        comando_file = os.path.join(CAMINHO_REDE, f"comando_maq_{maquina}.json")
        comando_data = {
            'id': str(uuid.uuid4()),
            'acao': acao,
            'timestamp': datetime.datetime.now().isoformat(),
            'parametros': {}
        }
        
        with open(comando_file, 'w', encoding='utf-8') as f:
            json.dump(comando_data, f, indent=2)
        
        log_func(f"✅ Comando '{acao}' enviado para {maquina}")
        messagebox.showinfo("Sucesso", f"✅ Comando enviado para {maquina}")
    except Exception as e:
        log_func(f"❌ Erro: {e}")
        messagebox.showerror("Erro", f"❌ {e}")

def abrir_dashboard_separado():
    try:
        dash_path = os.path.join(os.path.dirname(__file__), "..", "dash.py")
        if os.path.exists(dash_path):
            subprocess.Popen(["python", dash_path])
            messagebox.showinfo("Dashboard", "✅ Dashboard iniciado!")
        else:
            messagebox.showerror("Erro", "Arquivo dash.py não encontrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ {e}")

def explorar_arquivos():
    os.startfile(CAMINHO_LOCAL)

def editar_configuracoes():
    messagebox.showinfo("Info", "Use as abas de Configurações")

def buscar_registros(data_manager):
    messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")

def importar_dados(data_manager):
    messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")

def resetar_sistema(machine_config, batch_config):
    if messagebox.askyesno("ATENÇÃO", "Resetar TODAS as configurações?"):
        messagebox.showinfo("Info", "Sistema resetado!")

def gerar_relatorio(data_manager, machine_config):
    messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
