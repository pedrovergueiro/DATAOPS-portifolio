"""Janela de Registro Sempre Visível - NUNCA FECHA"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from models.batch import BatchConfig
from models.machine import MachineConfig
from data.manager import DataManager
import pandas as pd


# Variável global para a janela
janela_registro_global = None


def criar_janela_registro_fixa(root, machine_config: MachineConfig, batch_config: BatchConfig, data_manager: DataManager):
    """Cria janela que NUNCA fecha e fica SEMPRE sobre outros apps - ATALHO ALT+F1 PARA FECHAR"""
    global janela_registro_global
    
    if janela_registro_global and janela_registro_global.winfo_exists():
        janela_registro_global.lift()
        return janela_registro_global
    
    # Criar janela INDEPENDENTE que não fecha quando root fecha
    janela_independente = tk.Tk()
    janela_independente.withdraw()  # Esconder temporariamente
    
    try:
        # Usar Tk() ao invés de Toplevel para ser TOTALMENTE INDEPENDENTE
        janela_registro_global = tk.Toplevel(janela_independente)
        janela_registro_global.title("📝 Registrar Produção - FIXA")
        janela_registro_global.geometry("350x150")
        
        # CONFIGURAÇÕES DE SEGURANÇA MÁXIMA - NUNCA FECHA
        janela_registro_global.attributes('-topmost', True)
        janela_registro_global.attributes('-alpha', 0.95)
        janela_registro_global.resizable(False, False)
        janela_registro_global.overrideredirect(True)
        janela_registro_global.protocol("WM_DELETE_WINDOW", lambda: None)  # Bloqueia fechar
        
        # ATALHO SECRETO ALT+F1 PARA FECHAR (APENAS DESENVOLVEDOR SABE)
        def fechar_com_senha(event=None):
            import gui.auth
            if gui.auth.verificar_senha_desenvolvedor(root, data_manager):
                janela_registro_global.destroy()
                messagebox.showinfo("Janela Fechada", "Janela de registro fechada.\nSerá recriada em 10 segundos.")
                root.after(10000, lambda: criar_janela_registro_fixa(root, machine_config, batch_config, data_manager))
        
        janela_registro_global.bind('<Alt-F1>', fechar_com_senha)
        
        # Impedir que feche quando outras janelas fecharem
        def manter_viva():
            if janela_registro_global.winfo_exists():
                janela_registro_global.lift()
                janela_registro_global.after(100, manter_viva)
        manter_viva()
        
        # Barra de título personalizada
        title_bar = tk.Frame(janela_registro_global, bg='#2c3e50', height=25)
        title_bar.pack(fill='x', side='top')
        
        title_label = tk.Label(title_bar, text="📝 Registrar Produção - SEMPRE VISÍVEL", 
                               bg='#2c3e50', fg='white', font=('Arial', 10, 'bold'))
        title_label.pack(side='left', padx=5)
        
        # Posicionar no canto superior direito
        janela_registro_global.update_idletasks()
        screen_width = janela_registro_global.winfo_screenwidth()
        x = screen_width - 370
        y = 50
        janela_registro_global.geometry(f"+{x}+{y}")
        
        # Conteúdo principal
        content_frame = tk.Frame(janela_registro_global, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Informações de lote e size
        info_frame = tk.Frame(content_frame, bg='white')
        info_frame.pack(fill='x', pady=(0, 5))
        
        config_lote = batch_config.obter_configuracao_lote()
        CONFIG_SIZE = machine_config.obter_configuracao_size()
        
        lbl_lote = tk.Label(info_frame, 
                           text=f"Lote: {config_lote.get('lote', 'N/D')} | Caixa: {config_lote.get('caixa_atual', 0)}/{config_lote.get('total_caixas', 0)}", 
                           font=("Arial", 8), fg="#2c3e50", bg='white')
        lbl_lote.pack(side='left')
        
        lbl_size = tk.Label(info_frame, text=f"Size: {CONFIG_SIZE['size']}", 
                           font=("Arial", 8), fg="#e74c3c", bg='white')
        lbl_size.pack(side='right')
        
        # Botão principal - ABRE JANELA DE LANÇAMENTO
        def abrir_lancamento():
            # Verificar se lote está configurado
            config_lote = batch_config.obter_configuracao_lote()
            
            if not config_lote.get('lote') or config_lote.get('caixa_atual', 0) >= config_lote.get('total_caixas', 0):
                # Solicitar novo lote
                if solicitar_novo_lote(root, machine_config, batch_config):
                    # Atualizar labels
                    config_lote = batch_config.obter_configuracao_lote()
                    lbl_lote.config(text=f"Lote: {config_lote.get('lote', 'N/D')} | Caixa: {config_lote.get('caixa_atual', 0)}/{config_lote.get('total_caixas', 0)}")
                    # Abrir janela de lançamento
                    abrir_janela_lancamento_completo(root, machine_config, batch_config, data_manager, lbl_lote)
                else:
                    return
            else:
                # Abrir janela de lançamento
                abrir_janela_lancamento_completo(root, machine_config, batch_config, data_manager, lbl_lote)
        
        btn_registrar = tk.Button(content_frame, 
                                 text="🚀 LANÇAR PRODUÇÃO", 
                                 command=abrir_lancamento,
                                 bg="#28a745", fg="white", 
                                 font=("Arial", 12, "bold"),
                                 height=2, width=25)
        btn_registrar.pack(fill='both', expand=True)
        
        # Informação de máquina
        MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
        lbl_maquina = tk.Label(content_frame, text=f"Máquina: {MAQUINA_ATUAL}", 
                              font=("Arial", 8), fg="#7f8c8d", bg='white')
        lbl_maquina.pack(side='bottom')
        
        print("✅ Janela registro FIXA criada (NUNCA FECHA)")
        return janela_registro_global
        
    except Exception as e:
        print(f"❌ Erro ao criar janela de registro fixa: {e}")
        return None


def solicitar_novo_lote(root, machine_config: MachineConfig, batch_config: BatchConfig):
    """Solicita novo lote ao usuário"""
    
    janela_lote = tk.Toplevel(root)
    janela_lote.title("📦 Configuração de Lote")
    janela_lote.geometry("500x400")
    janela_lote.attributes('-topmost', True)
    janela_lote.grab_set()
    
    frame_principal = tk.Frame(janela_lote)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=10)
    
    tk.Label(frame_principal, text="📦 CONFIGURAÇÃO DE LOTE", 
             font=("Arial", 14, "bold")).pack(pady=10)
    
    # Informação da máquina
    MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
    CONFIG_SIZE = machine_config.obter_configuracao_size()
    
    tk.Label(frame_principal, text=f"Máquina: {MAQUINA_ATUAL} | Size: {CONFIG_SIZE['size']}", 
             font=("Arial", 10), fg="#7f8c8d").pack(pady=5)
    
    # Frame para os campos de entrada
    frame_campos = tk.Frame(frame_principal)
    frame_campos.pack(fill='x', pady=10)
    
    # Lote
    frame_lote = tk.Frame(frame_campos)
    frame_lote.pack(fill='x', pady=8)
    
    tk.Label(frame_lote, text="Número do Lote:", font=("Arial", 10)).pack(side='left', padx=(0, 10))
    lote_var = tk.StringVar()
    entry_lote = tk.Entry(frame_lote, textvariable=lote_var, width=30, font=("Arial", 10))
    entry_lote.pack(side='left', fill='x', expand=True)
    
    # Total de caixas
    frame_total = tk.Frame(frame_campos)
    frame_total.pack(fill='x', pady=8)
    
    tk.Label(frame_total, text="Número Total de Caixas:", font=("Arial", 10)).pack(side='left', padx=(0, 10))
    total_var = tk.StringVar()
    entry_total = tk.Entry(frame_total, textvariable=total_var, width=30, font=("Arial", 10))
    entry_total.pack(side='left', fill='x', expand=True)
    
    # Caixa atual
    frame_caixa = tk.Frame(frame_campos)
    frame_caixa.pack(fill='x', pady=8)
    
    tk.Label(frame_caixa, text="Número da Caixa Atual:", font=("Arial", 10)).pack(side='left', padx=(0, 10))
    caixa_var = tk.StringVar(value="1")
    entry_caixa = tk.Entry(frame_caixa, textvariable=caixa_var, width=30, font=("Arial", 10))
    entry_caixa.pack(side='left', fill='x', expand=True)
    
    # Informações
    info_frame = tk.Frame(frame_principal)
    info_frame.pack(fill='x', pady=15)
    
    tk.Label(info_frame, text="💡 Informações:", font=("Arial", 9, "bold"), fg="blue").pack(anchor='w')
    tk.Label(info_frame, text="• Lote: Aceita qualquer caractere (letras, números, símbolos)", 
             font=("Arial", 8), fg="#666").pack(anchor='w')
    tk.Label(info_frame, text="• Caixas: Apenas números inteiros positivos", 
             font=("Arial", 8), fg="#666").pack(anchor='w')
    
    resultado = [False]
    
    def confirmar_lote():
        try:
            lote = lote_var.get().strip()
            
            if not lote:
                messagebox.showerror("Erro", "O número do lote não pode estar vazio!")
                return
            
            try:
                total_caixas = int(total_var.get()) if total_var.get() else 0
                caixa_atual = int(caixa_var.get()) if caixa_var.get() else 0
            except ValueError:
                messagebox.showerror("Erro", "Número de caixas deve ser um valor inteiro!")
                return
            
            if total_caixas <= 0 or caixa_atual <= 0:
                messagebox.showerror("Erro", "Números de caixas devem ser maiores que zero!")
                return
            
            if caixa_atual > total_caixas:
                messagebox.showerror("Erro", "Caixa atual não pode ser maior que o total!")
                return
            
            # Salvar configuração
            if batch_config.salvar_configuracao_lote(lote, caixa_atual, total_caixas, 0):
                resultado[0] = True
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
    
    janela_lote.bind('<Return>', lambda e: confirmar_lote())
    
    # Centralizar
    janela_lote.update_idletasks()
    x = (janela_lote.winfo_screenwidth() - janela_lote.winfo_width()) // 2
    y = (janela_lote.winfo_screenheight() - janela_lote.winfo_height()) // 2
    janela_lote.geometry(f"+{x}+{y}")
    
    entry_lote.focus()
    
    janela_lote.wait_window()
    return resultado[0]


def abrir_janela_lancamento_completo(root, machine_config: MachineConfig, batch_config: BatchConfig, 
                                     data_manager: DataManager, lbl_lote_ref):
    """Abre janela completa para lançamento de produção"""
    
    config_lote = batch_config.obter_configuracao_lote()
    
    janela_lancamento = tk.Toplevel(root)
    janela_lancamento.title("📊 Lançamento de Produção")
    janela_lancamento.geometry("500x600")
    janela_lancamento.attributes('-topmost', True)
    janela_lancamento.grab_set()
    
    main_frame = tk.Frame(janela_lancamento)
    main_frame.pack(fill='both', expand=True, padx=15, pady=15)
    
    MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
    CONFIG_SIZE = machine_config.obter_configuracao_size()
    
    tk.Label(main_frame, text="LANÇAMENTO DE PRODUÇÃO", 
             font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=(0,10))
    
    # Informações atuais
    info_frame = tk.Frame(main_frame)
    info_frame.pack(fill='x', pady=(0,10))
    
    tk.Label(info_frame, text=f"Máquina: {MAQUINA_ATUAL}", 
             font=("Arial", 10), fg="#7f8c8d").pack(side='left')
    tk.Label(info_frame, text=f"Size: {CONFIG_SIZE['size']} (Peso: {CONFIG_SIZE['peso']})", 
             font=("Arial", 10), fg="#e74c3c").pack(side='right')
    
    tk.Label(main_frame, text=f"Lote: {config_lote.get('lote')} | Caixa: {config_lote.get('caixa_atual')}/{config_lote.get('total_caixas')}", 
             font=("Arial", 10, "bold"), fg="#27ae60").pack(pady=5)
    
    # USUÁRIO AUTOMÁTICO (não precisa selecionar no lançamento normal)
    # Usa "operador" como padrão ou primeiro usuário disponível
    usuario_automatico = "operador"
    if data_manager.df_users is not None and len(data_manager.df_users) > 0:
        # Tentar usar "operador" primeiro
        if "operador" not in data_manager.df_users['login'].values:
            # Se não existir, usar primeiro usuário
            usuario_automatico = data_manager.df_users['login'].iloc[0]
    
    # Dados de produção
    frm_dados = tk.LabelFrame(main_frame, text="📝 Dados de Produção", font=("Arial", 10, "bold"))
    frm_dados.pack(fill='x', pady=10)
    
    # Variáveis
    rej1_var, loc1_var = tk.StringVar(), tk.StringVar()
    rej2_var, loc2_var = tk.StringVar(), tk.StringVar()
    rej3_var, loc3_var = tk.StringVar(), tk.StringVar()
    camd_var, camw_var = tk.StringVar(), tk.StringVar()
    
    # Listas de opções
    lista_defeitos = ["Amassada", "Apara Retida", "Barra Colada", "Cápsula Fina", "Dente", 
                     "Furo", "Rachada", "Short", "Suja", "N/A"]
    cap_body = ["Cap", "Body", "Cap/Body", "N/A"]
    
    # Campos de rejeição - LADO A LADO
    for i, (rej, loc) in enumerate([(rej1_var, loc1_var), (rej2_var, loc2_var), (rej3_var, loc3_var)], start=1):
        tk.Label(frm_dados, text=f"Rej {i}:").grid(row=i, column=0, padx=4, pady=2, sticky='e')
        ttk.Combobox(frm_dados, textvariable=rej, values=lista_defeitos, width=15).grid(row=i, column=1, padx=2)
        tk.Label(frm_dados, text="Local:").grid(row=i, column=2, padx=2)
        ttk.Combobox(frm_dados, textvariable=loc, values=cap_body, width=10).grid(row=i, column=3, padx=2)
    
    # Percentuais
    tk.Label(frm_dados, text="CAM-D (%)").grid(row=4, column=0)
    tk.Entry(frm_dados, textvariable=camd_var, width=8).grid(row=4, column=1)
    tk.Label(frm_dados, text="CAM-W (%)").grid(row=4, column=2)
    tk.Entry(frm_dados, textvariable=camw_var, width=8).grid(row=4, column=3)
    
    def lancar_dados():
        """Lança dados de produção - USUÁRIO AUTOMÁTICO"""
        
        try:
            pctd = float(camd_var.get().replace(',','.')) if camd_var.get() else None
            pctw = float(camw_var.get().replace(',','.')) if camw_var.get() else None
        except:
            messagebox.showerror("Erro", "Percentual inválido.")
            return
        
        # Criar registro
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        novo_registro = {
            'maquina': MAQUINA_ATUAL,
            'rej1_defect': rej1_var.get(),
            'rej1_local': loc1_var.get(),
            'rej2_defect': rej2_var.get(),
            'rej2_local': loc2_var.get(),
            'rej3_defect': rej3_var.get(),
            'rej3_local': loc3_var.get(),
            'percent_cam_d': pctd,
            'percent_cam_w': pctw,
            'data_hora': data_hora,
            'origem': 'coletor',
            'justificativa': '',
            'usuario_reg': usuario_automatico,  # USUÁRIO AUTOMÁTICO
            'lote': config_lote.get('lote'),
            'numero_caixa': config_lote.get('caixa_atual'),
            'size': CONFIG_SIZE['size'],
            'peso': CONFIG_SIZE['peso']
        }
        
        if data_manager.df is None:
            data_manager.df = pd.DataFrame([novo_registro])
        else:
            data_manager.df = pd.concat([data_manager.df, pd.DataFrame([novo_registro])], ignore_index=True)
        
        # Salvar
        if data_manager.salvar_dados():
            messagebox.showinfo("Sucesso", "✅ Lançamento registrado!")
        else:
            messagebox.showwarning("Aviso", "Dados salvos apenas localmente")
        
        # Incrementar caixa
        caixa_atual = config_lote.get('caixa_atual', 0) + 1
        total_caixas = config_lote.get('total_caixas', 0)
        caixas_reg = config_lote.get('caixas_registradas', 0) + 1
        
        batch_config.salvar_configuracao_lote(config_lote.get('lote'), caixa_atual, total_caixas, caixas_reg)
        
        # Atualizar label na janela fixa
        config_lote_novo = batch_config.obter_configuracao_lote()
        lbl_lote_ref.config(text=f"Lote: {config_lote_novo.get('lote', 'N/D')} | Caixa: {config_lote_novo.get('caixa_atual', 0)}/{config_lote_novo.get('total_caixas', 0)}")
        
        # Verificar se precisa de novo lote
        if caixa_atual >= total_caixas:
            janela_lancamento.destroy()
            messagebox.showinfo("📦 Lote Completo", 
                           f"Lote {config_lote.get('lote')} atingiu {total_caixas} caixas!\n\n"
                           "Configure um novo lote.")
            solicitar_novo_lote(root, machine_config, batch_config)
            lbl_lote_ref.config(text=f"Lote: {batch_config.obter_configuracao_lote().get('lote', 'N/D')} | Caixa: {batch_config.obter_configuracao_lote().get('caixa_atual', 0)}/{batch_config.obter_configuracao_lote().get('total_caixas', 0)}")
        else:
            janela_lancamento.destroy()
    
    tk.Button(main_frame, text="🚀 Registrar Produção", command=lancar_dados,
             bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2).pack(fill='x', pady=15)
    
    # Centralizar
    janela_lancamento.update_idletasks()
    x = (janela_lancamento.winfo_screenwidth() - janela_lancamento.winfo_width()) // 2
    y = (janela_lancamento.winfo_screenheight() - janela_lancamento.winfo_height()) // 2
    janela_lancamento.geometry(f"+{x}+{y}")
