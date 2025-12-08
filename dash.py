"""
Dashboard de Análise de Produção Industrial

ALINHAMENTO 100% COM O COLETOR (main.py):
- Usa as mesmas configurações (config/settings.py)
- Usa as mesmas constantes (config/constants.py)
- Usa as mesmas colunas de dados (COLUNAS_DADOS)
- Usa as mesmas máquinas válidas (MAQUINAS_VALIDAS)
- Lê do mesmo arquivo CSV (dados_producao.csv)
- Compatível com a estrutura de dados do coletor

Este dashboard é 100% compatível com os dados gerados pelo sistema de coleta.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import subprocess
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURAÇÕES COMPATÍVEIS COM O COLETOR
# -----------------------------

# Importar configurações do coletor para garantir alinhamento 100%
from config.settings import CAMINHO_REDE, CSV_FILE
from config.constants import MAQUINAS_VALIDAS, COLUNAS_DADOS

# Configurar estilo profissional para os gráficos
plt.style.use('seaborn-v0_8')
CORES_FABRICA = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#6B8F71', '#1C5253', '#BB4430']

def configurar_estilo_grafico():
    """Configura estilo profissional para gráficos de fábrica"""
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#f8f9fa'
    plt.rcParams['grid.color'] = '#dee2e6'
    plt.rcParams['grid.alpha'] = 0.7
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.titleweight'] = 'bold'

configurar_estilo_grafico()

# Variável global para dados
df = None

# -----------------------------
# SISTEMA DE CARREGAMENTO ROBUSTO
# -----------------------------

def carregar_dataframe_seguro(caminho, colunas_padrao=None):
    """Carrega DataFrame com tratamento robusto de erros - 100% COMPATÍVEL COM COLETOR"""
    try:
        if os.path.exists(caminho):
            print(f"📁 Carregando CSV de: {caminho}")
            df_temp = pd.read_csv(caminho, dtype=str)
            print(f"✅ CSV carregado: {len(df_temp)} registros")
            
            # Garantir que todas as colunas do coletor existem
            for col in COLUNAS_DADOS:
                if col not in df_temp.columns:
                    df_temp[col] = '' if col not in ['percent_cam_d', 'percent_cam_w'] else 0.0
            
            # Tratar colunas numéricas (mesma lógica do coletor)
            for col in ['percent_cam_d', 'percent_cam_w', 'peso']:
                if col in df_temp.columns:
                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce').fillna(0.0)
            
            # Converter data/hora (mesma lógica do coletor)
            if 'data_hora' in df_temp.columns:
                df_temp['data_hora'] = pd.to_datetime(df_temp['data_hora'], errors='coerce')
            
            df_temp = df_temp.dropna(subset=['data_hora']).copy()
            
            # Filtrar máquinas válidas (mesma lista do coletor)
            if 'maquina' in df_temp.columns:
                maquinas_atuais = df_temp['maquina'].unique()
                print(f"🏭 Máquinas encontradas: {maquinas_atuais.tolist()}")
                df_temp = df_temp[df_temp['maquina'].isin(MAQUINAS_VALIDAS)].copy()
            
            print(f"🎯 Dados finais carregados: {len(df_temp)} registros")
            return df_temp
            
        else:
            print(f"⚠️ Arquivo CSV não encontrado: {caminho}")
            return pd.DataFrame(columns=COLUNAS_DADOS)
            
    except Exception as e:
        print(f"❌ Erro ao carregar CSV: {e}")
        return pd.DataFrame(columns=COLUNAS_DADOS)

def load_data_source():
    """Carrega dados diretamente do CSV na rede - COMPATÍVEL COM COLETOR"""
    global df
    
    try:
        df = carregar_dataframe_seguro(CSV_FILE)
        
        if df is not None and not df.empty:
            atualizar_tree(df)
            atualizar_status()
            messagebox.showinfo("Sucesso", f"Dados atualizados com sucesso!\n{len(df)} registros carregados.")
        else:
            atualizar_tree(None)
            atualizar_status()
            messagebox.showinfo("Informação", "Nenhum dado encontrado. Verifique o arquivo de produção.")
            
    except Exception as e:
        print(f"❌ Erro crítico ao carregar dados: {e}")
        messagebox.showerror("Erro", f"Falha crítica ao carregar dados: {e}")

def atualizar_dados():
    """Atualiza dados globalmente - interface pública"""
    load_data_source()

# -----------------------------
# FUNÇÕES UTILITÁRIAS COMPATÍVEIS
# -----------------------------

def formatar_data_hora(dt):
    """Formata datetime para dd/mm/yyyy HH:MM (sem segundos)"""
    if pd.isna(dt):
        return ""
    return dt.strftime("%d/%m/%Y %H:%M")

def filtrar(df_total, di, df_final, hi, hf, maquina=None):
    """Filtra dados por período e máquina - SEGURO PARA DATAFRAME VAZIO"""
    if df_total is None or df_total.empty or 'data_hora' not in df_total.columns:
        return pd.DataFrame()
        
    try:
        dt_inicio = pd.Timestamp.combine(pd.to_datetime(di).date(), hi)
        dt_fim = pd.Timestamp.combine(pd.to_datetime(df_final).date(), hf)
        
        if not pd.api.types.is_datetime64_any_dtype(df_total['data_hora']):
            df_total['data_hora'] = pd.to_datetime(df_total['data_hora'], errors='coerce')
        
        mask = (df_total['data_hora'] >= dt_inicio) & (df_total['data_hora'] <= dt_fim)
        df_filtered = df_total[mask].copy()
        
        if maquina and maquina.strip() and maquina in MAQUINAS_VALIDAS:
            df_filtered = df_filtered[df_filtered['maquina'].astype(str) == maquina]
            
        return df_filtered
    except Exception as e:
        print(f"⚠️ Erro no filtro: {e}")
        return pd.DataFrame()

def get_last_24h_range():
    """Retorna data/hora inicial e final para as últimas 24h."""
    now = pd.Timestamp.now()
    start = now - pd.Timedelta(hours=24)
    return start.date(), start.time(), now.date(), now.time()

def get_last_week_range():
    """Retorna data/hora inicial e final para a última semana."""
    now = pd.Timestamp.now()
    start = now - pd.Timedelta(days=7)
    return start.date(), start.time(), now.date(), now.time()

# -----------------------------
# COMPONENTES DE INTERFACE
# -----------------------------

def criar_mensagem_sem_dados(parent):
    """Cria uma mensagem elegante para quando não há dados"""
    frame_msg = tk.Frame(parent, bg='white')
    frame_msg.pack(fill='both', expand=True)
    
    # Ícone e mensagem centralizada
    tk.Label(frame_msg, text="📭", font=("Arial", 48), bg='white', fg='#6c757d').pack(expand=True, pady=(50, 10))
    tk.Label(frame_msg, text="NENHUM DADO DISPONÍVEL", font=("Arial", 16, "bold"), 
             bg='white', fg='#6c757d').pack(pady=5)
    tk.Label(frame_msg, text="Clique em ATUALIZAR DADOS para carregar as informações mais recentes", 
             font=("Arial", 10), bg='white', fg='#6c757d', wraplength=400).pack(pady=5)
    
    # Botão para atualizar
    btn_atualizar = tk.Button(frame_msg, text="🔄 ATUALIZAR DADOS", 
                             command=atualizar_dados,
                             bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                             width=20, height=2)
    btn_atualizar.pack(pady=20)
    
    return frame_msg

# -----------------------------
# TREEVIEW PRINCIPAL
# -----------------------------

def atualizar_tree(df_filtered=None):
    """Atualiza a treeview com dados ou mensagem de sem dados"""
    for i in tree.get_children():
        tree.delete(i)
        
    if df_filtered is None:
        df_filtered = df
        
    if df_filtered is None or df_filtered.empty:
        # Mostrar mensagem elegante quando não há dados
        tree.insert('', 'end', values=(
            "---", "---", "---", "---", "---", "---", "📭 Nenhum dado disponível - Clique em ATUALIZAR DADOS"
        ))
    else:
        for _, row in df_filtered.iterrows():
            maquina = str(row.get('maquina', ''))
            rej1 = str(row.get('rej1_defect', ''))
            rej2 = str(row.get('rej2_defect', ''))
            rej3 = str(row.get('rej3_defect', ''))
            cam_d = f"{row.get('percent_cam_d',0):.2f}" if pd.notna(row.get('percent_cam_d')) else '0.00'
            cam_w = f"{row.get('percent_cam_w',0):.2f}" if pd.notna(row.get('percent_cam_w')) else '0.00'
            data_hora = formatar_data_hora(row.get('data_hora'))
            
            tree.insert('', 'end', values=(
                maquina, rej1, rej2, rej3, cam_d, cam_w, data_hora
            ))

def aplicar_filtro_principal():
    """Aplica filtro na tabela principal"""
    if df is None or df.empty:
        messagebox.showinfo("Sem Dados", "Nenhum dado disponível. Clique em ATUALIZAR DADOS primeiro.")
        return
        
    try:
        hi_str = hora_inicial.get().strip()
        hf_str = hora_final.get().strip()
        if not hi_str or not hf_str:
            messagebox.showerror("Erro", "Selecione horários válidos.")
            return
            
        hi_time = pd.to_datetime(hi_str, format="%H:%M").time()
        hf_time = pd.to_datetime(hf_str, format="%H:%M").time()
        
        df_filtrado = filtrar(df,
                             di=data_inicial.get_date(),
                             df_final=data_final.get_date(),
                             hi=hi_time,
                             hf=hf_time,
                             maquina=maquina_main.get())
        atualizar_tree(df_filtrado)
        atualizar_status()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao aplicar filtro: {e}")

def limpar_filtro_principal():
    """Limpa filtros da tabela principal"""
    dt_ini_date, dt_ini_time, dt_fim_date, dt_fim_time = get_last_24h_range()
    data_inicial.set_date(dt_ini_date)
    data_final.set_date(dt_fim_date)
    hora_inicial.set(f"{dt_ini_time.hour:02d}:{(dt_ini_time.minute // 5) * 5:02d}")
    hora_final.set(f"{dt_fim_time.hour:02d}:{(dt_fim_time.minute // 5) * 5:02d}")
    maquina_main.set('')
    atualizar_tree(df)
    atualizar_status()

# -----------------------------
# INTEGRAÇÃO COM COLETOR
# -----------------------------

def abrir_coletor():
    """Abre o aplicativo coletor - COMPATÍVEL COM SISTEMA EXISTENTE"""
    coletor_path = os.path.join(CAMINHO_REDE, "coletor_producao.py")
    
    # Tentar caminhos alternativos
    caminhos_tentativas = [
        coletor_path,
        "coletor_producao.py",
        "coletor.py",
        os.path.join(os.path.dirname(__file__), "coletor_producao.py"),
        os.path.join(os.path.dirname(__file__), "coletor.py")
    ]
    
    coletor_encontrado = None
    for caminho in caminhos_tentativas:
        if os.path.exists(caminho):
            coletor_encontrado = caminho
            break
    
    if coletor_encontrado:
        try:
            subprocess.Popen(["python", coletor_encontrado])
            messagebox.showinfo("Sucesso", "Coletor iniciado!\n\nOs dados serão salvos em:\n" + CSV_FILE)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o coletor: {e}")
    else:
        messagebox.showerror("Erro", 
                           "Coletor não encontrado!\n\n"
                           "Procure por estes arquivos:\n"
                           "- coletor_producao.py\n" 
                           "- coletor.py\n"
                           f"- {coletor_path}")

# -----------------------------
# GRÁFICOS - VERSÕES ROBUSTAS
# -----------------------------

def mostrar_grafico_top5():
    """Top 5 Defeitos - Versão robusta e compatível"""
    win = tk.Toplevel()
    win.title("📊 Top 5 Defeitos - Análise de Produção")
    win.geometry("1400x800")
    win.configure(bg='#f8f9fa')

    # Header
    header_frame = tk.Frame(win, bg='#2c3e50', height=80)
    header_frame.pack(fill='x', padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="TOP 5 DEFEITOS - ANÁLISE DE PRODUÇÃO", 
             font=("Arial", 16, "bold"), fg="white", bg='#2c3e50').pack(expand=True)

    # Frame de controle
    controle_frame = tk.Frame(win, bg='#f8f9fa')
    controle_frame.pack(fill='x', padx=20, pady=10)
    
    # Botão de atualizar
    btn_atualizar_top = tk.Button(controle_frame, text="🔄 ATUALIZAR DADOS", 
                                 command=lambda: [atualizar_dados(), atualizar_grafico()],
                                 bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                                 width=20, height=2)
    btn_atualizar_top.pack(side='left', padx=5)

    filtro_frame = tk.Frame(win, bg='#f8f9fa')
    filtro_frame.pack(fill='x', padx=20, pady=15)

    # Configurar frames de filtro
    left_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    left_frame.pack(side='left', fill='x', expand=True)
    
    right_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    right_frame.pack(side='right')

    # Labels com estilo melhorado
    tk.Label(left_frame, text="Período:", font=("Arial", 10, "bold"), bg='#f8f9fa').grid(row=0, column=0, padx=5, pady=2, sticky='w')
    tk.Label(left_frame, text="Data Inicial", bg='#f8f9fa').grid(row=1, column=0, padx=5, sticky='w')
    data_inicial_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_inicial_w.grid(row=2, column=0, padx=5)

    tk.Label(left_frame, text="Data Final", bg='#f8f9fa').grid(row=1, column=1, padx=5, sticky='w')
    data_final_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_final_w.grid(row=2, column=1, padx=5)

    horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60,5)]
    tk.Label(left_frame, text="Hora Inicial", bg='#f8f9fa').grid(row=1, column=2, padx=5, sticky='w')
    hora_inicial_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_inicial_w.grid(row=2, column=2, padx=5)

    tk.Label(left_frame, text="Hora Final", bg='#f8f9fa').grid(row=1, column=3, padx=5, sticky='w')
    hora_final_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_final_w.grid(row=2, column=3, padx=5)

    tk.Label(left_frame, text="Máquina", bg='#f8f9fa').grid(row=1, column=4, padx=5, sticky='w')
    maquina_var = ttk.Combobox(left_frame, values=MAQUINAS_VALIDAS, width=8, state="readonly")
    maquina_var.grid(row=2, column=4, padx=5)

    # Botões com cores profissionais
    btn_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 1}
    tk.Button(right_frame, text="🔍 ANALISAR", command=lambda: atualizar_grafico(), 
              bg="#28a745", fg="white", **btn_style).pack(side='left', padx=3)
    tk.Button(right_frame, text="🔄 LIMPAR", command=lambda: limpar_filtros(), 
              bg="#6c757d", fg="white", **btn_style).pack(side='left', padx=3)
    tk.Button(right_frame, text="📊 PARETO", 
              command=mostrar_grafico_pareto, 
              bg="#17a2b8", fg="white", **btn_style).pack(side='left', padx=3)

    grafico_frame = tk.Frame(win, bg='white')
    grafico_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Inicializar com mensagem de sem dados
    msg_frame = criar_mensagem_sem_dados(grafico_frame)

    def atualizar_grafico():
        nonlocal msg_frame
        
        # Remover mensagem anterior
        for widget in grafico_frame.winfo_children():
            widget.destroy()
            
        if df is None or df.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        try:
            hi_str = hora_inicial_w.get().strip()
            hf_str = hora_final_w.get().strip()
            if not hi_str or not hf_str:
                messagebox.showerror("Erro", "Selecione horários válidos.")
                return
            hi_time = pd.to_datetime(hi_str, format="%H:%M").time()
            hf_time = pd.to_datetime(hf_str, format="%H:%M").time()
        except Exception as e:
            messagebox.showerror("Erro", f"Formato de hora inválido: {e}")
            return
            
        df_filtrado = filtrar(df,
                              di=data_inicial_w.get_date(),
                              df_final=data_final_w.get_date(),
                              hi=hi_time,
                              hf=hf_time,
                              maquina=maquina_var.get())
                              
        if df_filtrado is None or df_filtrado.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Coletar defeitos válidos - VERIFICAR COLUNAS EXISTENTES
        defeitos_list = []
        colunas_defeitos = ['rej1_defect', 'rej2_defect', 'rej3_defect']
        
        for col in colunas_defeitos:
            if col in df_filtrado.columns:
                valid = df_filtrado[col].dropna().astype(str).str.strip()
                valid = valid[valid != '']
                valid = valid[valid.str.lower() != 'nan']
                defeitos_list.append(valid)
        
        if not defeitos_list:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        defeitos = pd.concat(defeitos_list, ignore_index=True)
        
        if defeitos.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return
            
        df_sorted = defeitos.value_counts().head(5)
        total = df_sorted.sum()

        # Criar gráficos
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Gráfico de barras
        axes[0].clear()
        if len(df_sorted) > 0:
            bars = axes[0].bar(range(len(df_sorted)), df_sorted.values, 
                              color=CORES_FABRICA[:len(df_sorted)], alpha=0.8, edgecolor='black', linewidth=0.5)
            axes[0].set_title("TOP 5 DEFEITOS - FREQUÊNCIA", fontsize=14, fontweight='bold', pad=20)
            axes[0].set_ylabel("QUANTIDADE DE OCORRÊNCIAS", fontweight='bold')
            axes[0].set_xlabel("TIPOS DE DEFEITOS", fontweight='bold')
            axes[0].set_xticks(range(len(df_sorted)))
            axes[0].set_xticklabels(df_sorted.index, rotation=45, ha='right')
            axes[0].grid(True, alpha=0.3, axis='y')
            
            # Adicionar valores nas barras
            for i, bar in enumerate(bars):
                height = bar.get_height()
                pct = (height/total)*100 if total>0 else 0
                axes[0].text(bar.get_x() + bar.get_width()/2, height + max(df_sorted.values)*0.01,
                            f"{int(height)}\n({pct:.1f}%)", 
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            axes[0].text(0.5, 0.5, "📭 NENHUM DADO", 
                       ha='center', va='center', transform=axes[0].transAxes, fontsize=14, color='gray')

        # Gráfico de pizza
        axes[1].clear()
        if len(df_sorted) > 0:
            wedges, texts, autotexts = axes[1].pie(df_sorted.values, 
                                                  labels=df_sorted.index, 
                                                  autopct='%1.1f%%',
                                                  colors=CORES_FABRICA[:len(df_sorted)],
                                                  startangle=90,
                                                  textprops={'fontsize': 9, 'fontweight': 'bold'})
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            axes[1].text(0.5, 0.5, "📭 NENHUM DADO", 
                       ha='center', va='center', transform=axes[1].transAxes, fontsize=14, color='gray')
                
        axes[1].set_title("DISTRIBUIÇÃO PERCENTUAL", fontsize=14, fontweight='bold', pad=20)

        # Adicionar legenda de total
        if len(df_sorted) > 0:
            fig.suptitle(f"TOTAL DE OCORRÊNCIAS: {total} | PERÍODO: {data_inicial_w.get_date().strftime('%d/%m/%Y')} a {data_final_w.get_date().strftime('%d/%m/%Y')}", 
                        fontsize=12, fontweight='bold', y=0.95)
        else:
            fig.suptitle("NENHUM DADO DISPONÍVEL", fontsize=12, fontweight='bold', y=0.95)

        fig.tight_layout(rect=[0, 0, 1, 0.95])
        canvas.draw()

    def limpar_filtros():
        dt_ini_date, dt_ini_time, dt_fim_date, dt_fim_time = get_last_week_range()
        data_inicial_w.set_date(dt_ini_date)
        data_final_w.set_date(dt_fim_date)
        hora_inicial_w.set(f"{dt_ini_time.hour:02d}:{(dt_ini_time.minute // 5) * 5:02d}")
        hora_final_w.set(f"{dt_fim_time.hour:02d}:{(dt_fim_time.minute // 5) * 5:02d}")
        maquina_var.set('')
        win.after(100, atualizar_grafico)

    # Inicializar com última semana
    limpar_filtros()

def mostrar_grafico_pareto():
    """Gráfico de Pareto - Versão robusta e compatível"""
    win = tk.Toplevel()
    win.title("📈 Gráfico de Pareto - Análise de Defeitos")
    win.geometry("1600x900")
    win.configure(bg='#f8f9fa')

    # Header
    header_frame = tk.Frame(win, bg='#2c3e50', height=80)
    header_frame.pack(fill='x', padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="GRÁFICO DE PARETO - ANÁLISE DE DEFEITOS", 
             font=("Arial", 16, "bold"), fg="white", bg='#2c3e50').pack(expand=True)

    # Frame de controle
    controle_frame = tk.Frame(win, bg='#f8f9fa')
    controle_frame.pack(fill='x', padx=20, pady=10)
    
    # Botão de atualizar
    btn_atualizar_pareto = tk.Button(controle_frame, text="🔄 ATUALIZAR DADOS", 
                                    command=lambda: [atualizar_dados(), aplicar_filtro()],
                                    bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                                    width=20, height=2)
    btn_atualizar_pareto.pack(side='left', padx=5)

    filtro_frame = tk.Frame(win, bg='#f8f9fa')
    filtro_frame.pack(fill='x', padx=20, pady=15)

    left_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    left_frame.pack(side='left', fill='x', expand=True)
    
    right_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    right_frame.pack(side='right')

    tk.Label(left_frame, text="Período:", font=("Arial", 10, "bold"), bg='#f8f9fa').grid(row=0, column=0, padx=5, pady=2, sticky='w')
    tk.Label(left_frame, text="Data Inicial", bg='#f8f9fa').grid(row=1, column=0, padx=5, sticky='w')
    data_inicial_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_inicial_w.grid(row=2, column=0, padx=5)

    tk.Label(left_frame, text="Data Final", bg='#f8f9fa').grid(row=1, column=1, padx=5, sticky='w')
    data_final_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_final_w.grid(row=2, column=1, padx=5)

    horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60,5)]
    tk.Label(left_frame, text="Hora Inicial", bg='#f8f9fa').grid(row=1, column=2, padx=5, sticky='w')
    hora_inicial_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_inicial_w.grid(row=2, column=2, padx=5)

    tk.Label(left_frame, text="Hora Final", bg='#f8f9fa').grid(row=1, column=3, padx=5, sticky='w')
    hora_final_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_final_w.grid(row=2, column=3, padx=5)

    tk.Label(left_frame, text="Máquina", bg='#f8f9fa').grid(row=1, column=4, padx=5, sticky='w')
    maquina_var = ttk.Combobox(left_frame, values=MAQUINAS_VALIDAS, width=8, state="readonly")
    maquina_var.grid(row=2, column=4, padx=5)

    btn_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 1}
    tk.Button(right_frame, text="📈 GERAR PARETO", command=lambda: aplicar_filtro(), 
              bg="#dc3545", fg="white", **btn_style).pack(side='left', padx=3)
    tk.Button(right_frame, text="🔄 LIMPAR", command=lambda: limpar_filtros(), 
              bg="#6c757d", fg="white", **btn_style).pack(side='left', padx=3)

    grafico_frame = tk.Frame(win, bg='white')
    grafico_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Inicializar com mensagem de sem dados
    msg_frame = criar_mensagem_sem_dados(grafico_frame)

    def aplicar_filtro():
        nonlocal msg_frame
        
        # Remover mensagem anterior
        for widget in grafico_frame.winfo_children():
            widget.destroy()

        if df is None or df.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        try:
            hi_str = hora_inicial_w.get().strip()
            hf_str = hora_final_w.get().strip()
            if not hi_str or not hf_str:
                messagebox.showerror("Erro", "Selecione horários válidos.")
                return
            hi_time = pd.to_datetime(hi_str, format="%H:%M").time()
            hf_time = pd.to_datetime(hf_str, format="%H:%M").time()
        except Exception as e:
            messagebox.showerror("Erro", f"Formato de hora inválido: {e}")
            return

        df_f = filtrar(df,
                       di=data_inicial_w.get_date(),
                       df_final=data_final_w.get_date(),
                       hi=hi_time,
                       hf=hf_time,
                       maquina=maquina_var.get())
        
        if df_f is None or df_f.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Coletar defeitos - VERIFICAR COLUNAS EXISTENTES
        defeitos_list = []
        colunas_defeitos = ['rej1_defect', 'rej2_defect', 'rej3_defect']
        
        for col in colunas_defeitos:
            if col in df_f.columns:
                valid = df_f[col].dropna().astype(str).str.strip()
                valid = valid[valid != '']
                valid = valid[valid.str.lower() != 'nan']
                defeitos_list.append(valid)
        
        if not defeitos_list:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        defeitos = pd.concat(defeitos_list, ignore_index=True)
        
        if defeitos.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return
            
        contagem = defeitos.value_counts()
        total = contagem.sum()
        porcentagem = (contagem / total) * 100
        porcentagem_acum = porcentagem.cumsum()

        fig, ax1 = plt.subplots(figsize=(16, 8))
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Gráfico de barras (frequência)
        if len(contagem) > 0:
            bars = ax1.bar(range(len(contagem)), contagem.values, 
                          color='#2E86AB', alpha=0.7, edgecolor='black', linewidth=0.5)
            ax1.set_xlabel('TIPOS DE DEFEITOS', fontweight='bold', fontsize=12)
            ax1.set_ylabel('FREQUÊNCIA', color='#2E86AB', fontweight='bold', fontsize=12)
            ax1.tick_params(axis='y', labelcolor='#2E86AB')
            ax1.set_xticks(range(len(contagem)))
            ax1.set_xticklabels(contagem.index, rotation=45, ha='right', fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='y')

            # Gráfico de linha (percentual acumulado)
            ax2 = ax1.twinx()
            line = ax2.plot(range(len(contagem)), porcentagem_acum.values, 
                           color='#C73E1D', marker='o', linewidth=3, markersize=8, 
                           markerfacecolor='white', markeredgecolor='#C73E1D', markeredgewidth=2)
            ax2.set_ylabel('PERCENTUAL ACUMULADO (%)', color='#C73E1D', fontweight='bold', fontsize=12)
            ax2.tick_params(axis='y', labelcolor='#C73E1D')
            ax2.set_ylim(0, 110)
            
            # Linha de 80%
            ax2.axhline(y=80, color='#F18F01', linestyle='--', linewidth=2, alpha=0.8, label='Limite 80%')
            ax2.legend(loc='upper left', fontsize=10)

            # Anotações nas barras
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2, height + max(contagem.values)*0.01,
                        f"{int(height)}\n({porcentagem.iloc[i]:.1f}%)", 
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

            # Anotações na linha
            for i, (x, y) in enumerate(zip(range(len(contagem)), porcentagem_acum.values)):
                ax2.text(x, y + 3, f"{y:.1f}%", ha='center', va='bottom', 
                        fontsize=9, color='#C73E1D', fontweight='bold', 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

            # Identificar defeitos críticos (acima de 80%)
            defeitos_criticos = contagem[porcentagem_acum <= 80]
            if not defeitos_criticos.empty:
                critico_text = "DEFEITOS CRÍTICOS (80% do total):\n" + "\n".join([
                    f"• {defeito}" for defeito in defeitos_criticos.index[:3]  # Mostrar apenas os 3 primeiros
                ])
                ax1.text(0.02, 0.98, critico_text, transform=ax1.transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle="round", facecolor='lightcoral', alpha=0.8))

            ax1.set_title("GRÁFICO DE PARETO - ANÁLISE DE DEFEITOS\n(Princípio 80/20)", 
                         fontsize=16, fontweight='bold', pad=20)
        else:
            ax1.text(0.5, 0.5, "📭 NENHUM DADO PARA ANÁLISE", 
                    ha='center', va='center', transform=ax1.transAxes, fontsize=16, color='gray')
            ax1.set_xticks([])
            ax1.set_yticks([])

        fig.tight_layout()
        canvas.draw()

    def limpar_filtros():
        dt_ini_date, dt_ini_time, dt_fim_date, dt_fim_time = get_last_week_range()
        data_inicial_w.set_date(dt_ini_date)
        data_final_w.set_date(dt_fim_date)
        hora_inicial_w.set(f"{dt_ini_time.hour:02d}:{(dt_ini_time.minute // 5) * 5:02d}")
        hora_final_w.set(f"{dt_fim_time.hour:02d}:{(dt_fim_time.minute // 5) * 5:02d}")
        maquina_var.set('')
        win.after(100, aplicar_filtro)

    limpar_filtros()

def mostrar_media_rejeicao():
    """Média de Rejeição - Versão robusta e compatível"""
    win = tk.Toplevel()
    win.title("📋 Média de Rejeição por Máquina")
    win.geometry("1600x1000")
    win.configure(bg='#f8f9fa')

    # Header
    header_frame = tk.Frame(win, bg='#2c3e50', height=80)
    header_frame.pack(fill='x', padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="MÉDIA DE REJEIÇÃO POR MÁQUINA - DESEMPENHO", 
             font=("Arial", 16, "bold"), fg="white", bg='#2c3e50').pack(expand=True)

    # Frame de controle
    controle_frame = tk.Frame(win, bg='#f8f9fa')
    controle_frame.pack(fill='x', padx=20, pady=10)
    
    # Botão de atualizar
    btn_atualizar_media = tk.Button(controle_frame, text="🔄 ATUALIZAR DADOS", 
                                   command=lambda: [atualizar_dados(), aplicar_filtro()],
                                   bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                                   width=20, height=2)
    btn_atualizar_media.pack(side='left', padx=5)

    filtro_frame = tk.Frame(win, bg='#f8f9fa')
    filtro_frame.pack(fill='x', padx=20, pady=15)

    left_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    left_frame.pack(side='left', fill='x', expand=True)
    
    right_frame = tk.Frame(filtro_frame, bg='#f8f9fa')
    right_frame.pack(side='right')

    tk.Label(left_frame, text="Período:", font=("Arial", 10, "bold"), bg='#f8f9fa').grid(row=0, column=0, padx=5, pady=2, sticky='w')
    tk.Label(left_frame, text="Data Inicial", bg='#f8f9fa').grid(row=1, column=0, padx=5, sticky='w')
    data_inicial_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_inicial_w.grid(row=2, column=0, padx=5)

    tk.Label(left_frame, text="Data Final", bg='#f8f9fa').grid(row=1, column=1, padx=5, sticky='w')
    data_final_w = DateEntry(left_frame, width=12, date_pattern='dd/mm/yyyy')
    data_final_w.grid(row=2, column=1, padx=5)

    horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60,5)]
    tk.Label(left_frame, text="Hora Inicial", bg='#f8f9fa').grid(row=1, column=2, padx=5, sticky='w')
    hora_inicial_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_inicial_w.grid(row=2, column=2, padx=5)

    tk.Label(left_frame, text="Hora Final", bg='#f8f9fa').grid(row=1, column=3, padx=5, sticky='w')
    hora_final_w = ttk.Combobox(left_frame, values=horas, width=8, state="readonly")
    hora_final_w.grid(row=2, column=3, padx=5)

    tk.Label(left_frame, text="Máquina", bg='#f8f9fa').grid(row=1, column=4, padx=5, sticky='w')
    maquina_var = ttk.Combobox(left_frame, values=MAQUINAS_VALIDAS, width=8, state="readonly")
    maquina_var.grid(row=2, column=4, padx=5)

    btn_style = {"font": ("Arial", 10, "bold"), "width": 15, "height": 1}
    tk.Button(right_frame, text="📊 CALCULAR MÉDIAS", command=lambda: aplicar_filtro(), 
              bg="#28a745", fg="white", **btn_style).pack(side='left', padx=3)
    tk.Button(right_frame, text="🔄 LIMPAR FILTROS", command=lambda: limpar_filtros(), 
              bg="#6c757d", fg="white", **btn_style).pack(side='left', padx=3)

    grafico_frame = tk.Frame(win, bg='white')
    grafico_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Inicializar com mensagem de sem dados
    msg_frame = criar_mensagem_sem_dados(grafico_frame)

    def aplicar_filtro():
        nonlocal msg_frame
        
        # Remover mensagem anterior
        for widget in grafico_frame.winfo_children():
            widget.destroy()

        if df is None or df.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        try:
            hi_str = hora_inicial_w.get().strip()
            hf_str = hora_final_w.get().strip()
            if not hi_str or not hf_str:
                messagebox.showerror("Erro", "Selecione horários válidos.")
                return
            hi_time = pd.to_datetime(hi_str, format="%H:%M").time()
            hf_time = pd.to_datetime(hf_str, format="%H:%M").time()
        except Exception as e:
            messagebox.showerror("Erro", f"Formato de hora inválido: {e}")
            return

        df_f = filtrar(df,
                       di=data_inicial_w.get_date(),
                       df_final=data_final_w.get_date(),
                       hi=hi_time,
                       hf=hf_time,
                       maquina=maquina_var.get())

        if df_f is None or df_f.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Verificar se as colunas necessárias existem
        colunas_necessarias = ['maquina', 'percent_cam_d', 'percent_cam_w']
        colunas_faltantes = [col for col in colunas_necessarias if col not in df_f.columns]
        
        if colunas_faltantes:
            label = tk.Label(grafico_frame, text=f"📭 COLUNAS FALTANTES:\n{', '.join(colunas_faltantes)}", 
                           font=("Arial", 14), fg="gray", bg='white')
            label.pack(expand=True)
            return

        # Filtrar dados válidos
        condicoes = []
        
        # Verificar colunas de percentuais
        if 'percent_cam_d' in df_f.columns:
            condicoes.append(df_f['percent_cam_d'] > 0)
        if 'percent_cam_w' in df_f.columns:
            condicoes.append(df_f['percent_cam_w'] > 0)
            
        # Verificar colunas de defeitos
        colunas_defeitos = ['rej1_defect', 'rej2_defect', 'rej3_defect']
        for col in colunas_defeitos:
            if col in df_f.columns:
                cond_defeito = (
                    (df_f[col].notna()) & 
                    (df_f[col] != '') & 
                    (df_f[col].str.lower() != 'nan')
                )
                condicoes.append(cond_defeito)

        if not condicoes:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Combinar condições
        condicao_final = condicoes[0]
        for cond in condicoes[1:]:
            condicao_final = condicao_final | cond

        df_valid = df_f[condicao_final]

        if df_valid.empty:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Calcular médias por máquina
        maquinas_com_dados = sorted(df_valid['maquina'].dropna().unique(), key=lambda x: str(x))
        media_maquinas = []
        
        for m in maquinas_com_dados:
            df_m = df_valid[df_valid['maquina'] == m]
            cam_d = df_m['percent_cam_d'].mean() if 'percent_cam_d' in df_m.columns else 0.0
            cam_w = df_m['percent_cam_w'].mean() if 'percent_cam_w' in df_m.columns else 0.0
            
            if pd.isna(cam_d): cam_d = 0.0
            if pd.isna(cam_w): cam_w = 0.0
            media_total = (cam_d + cam_w) / 2

            media_maquinas.append({
                'maquina': m,
                'CAM-D (%)': cam_d,
                'CAM-W (%)': cam_w,
                'Média (%)': media_total
            })

        if not media_maquinas:
            msg_frame = criar_mensagem_sem_dados(grafico_frame)
            return

        # Ordenar por média total
        media_maquinas.sort(key=lambda x: x['Média (%)'], reverse=True)

        # Criar gráfico
        fig, ax = plt.subplots(figsize=(16, 8))
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        x = range(len(media_maquinas))
        cam_d_means = [m['CAM-D (%)'] for m in media_maquinas]
        cam_w_means = [m['CAM-W (%)'] for m in media_maquinas]
        labels = [f"Máq. {m['maquina']}" for m in media_maquinas]
        width = 0.35

        # Função para definir cores baseadas em performance
        def cor_performance(valor, tipo):
            if valor <= 2.0:
                return '#28a745'  # Verde - Excelente
            elif valor <= 4.0:
                return '#ffc107'  # Amarelo - Bom
            elif valor <= 6.0:
                return '#fd7e14'  # Laranja - Atenção
            else:
                return '#dc3545'  # Vermelho - Crítico

        bars_d = ax.bar([i - width/2 for i in x], cam_d_means, width, 
                       color=[cor_performance(v, 'd') for v in cam_d_means],
                       label='CAM-D', edgecolor='black', linewidth=0.5)
        bars_w = ax.bar([i + width/2 for i in x], cam_w_means, width, 
                       color=[cor_performance(v, 'w') for v in cam_w_means],
                       label='CAM-W', edgecolor='black', linewidth=0.5)

        # Adicionar valores nas barras
        for bars in [bars_d, bars_w]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, height + 0.05, 
                           f"{height:.2f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontweight='bold')
        ax.set_ylabel("PERCENTUAL DE REJEIÇÃO (%)", fontweight='bold', fontsize=12)
        ax.set_xlabel("MÁQUINAS", fontweight='bold', fontsize=12)
        ax.set_title("DESEMPENHO DAS MÁQUINAS - MÉDIA DE REJEIÇÃO\n(Quanto menor, melhor)", 
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Adicionar linha de meta (3%)
        ax.axhline(y=3.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Meta (3%)')
        ax.legend(fontsize=11)

        # Adicionar estatísticas no gráfico
        total_maquinas = len(media_maquinas)
        acima_meta = sum(1 for m in media_maquinas if m['Média (%)'] <= 3.0)
        percentual_acima_meta = (acima_meta / total_maquinas) * 100

        stats_text = f"ESTATÍSTICAS:\n• Total de Máquinas: {total_maquinas}\n• Acima da Meta: {acima_meta}\n• Performance: {percentual_acima_meta:.1f}%"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle="round", facecolor='lightblue', alpha=0.8))

        fig.tight_layout()
        canvas.draw()

        # Adicionar tabela de ranking
        table_frame = tk.Frame(win, bg='white')
        table_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(table_frame, text="🏆 RANKING DE DESEMPENHO DAS MÁQUINAS", 
                font=("Arial", 12, "bold"), bg='white').pack(pady=(0, 10))
        
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='x')
        
        columns = ('Posição', 'Máquina', 'CAM-D (%)', 'CAM-W (%)', 'Média (%)', 'Status')
        tree_ranking = ttk.Treeview(tree_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            tree_ranking.heading(col, text=col)
            tree_ranking.column(col, width=120, anchor='center')
        
        # Adicionar dados à tabela
        for i, m in enumerate(media_maquinas, 1):
            status = "✅ EXCELENTE" if m['Média (%)'] <= 2.0 else \
                    "🟡 BOM" if m['Média (%)'] <= 4.0 else \
                    "🟠 ATENÇÃO" if m['Média (%)'] <= 6.0 else "🔴 CRÍTICO"
            
            tree_ranking.insert('', 'end', values=(
                f"{i}º",
                f"Máq. {m['maquina']}",
                f"{m['CAM-D (%)']:.2f}%",
                f"{m['CAM-W (%)']:.2f}%",
                f"{m['Média (%)']:.2f}%",
                status
            ))
        
        tree_ranking.pack(fill='x')

    def limpar_filtros():
        dt_ini_date, dt_ini_time, dt_fim_date, dt_fim_time = get_last_week_range()
        data_inicial_w.set_date(dt_ini_date)
        data_final_w.set_date(dt_fim_date)
        hora_inicial_w.set(f"{dt_ini_time.hour:02d}:{(dt_ini_time.minute // 5) * 5:02d}")
        hora_final_w.set(f"{dt_fim_time.hour:02d}:{(dt_fim_time.minute // 5) * 5:02d}")
        maquina_var.set('')
        win.after(100, aplicar_filtro)

    limpar_filtros()

# -----------------------------
# JANELA PRINCIPAL
# -----------------------------

def atualizar_status():
    """Atualiza a barra de status"""
    total_registros = 0 if df is None else len(df)
    status_text = f"Total de registros carregados: {total_registros} | Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    status_label.config(text=status_text)

# Criar janela principal
root = tk.Tk()
root.title("🏭 Dashboard de Produção - Controle de Qualidade")
root.geometry("1600x900")

# Header principal
header_frame = tk.Frame(root, bg='#2c3e50', height=100)
header_frame.pack(fill='x', padx=10, pady=5)
header_frame.pack_propagate(False)

tk.Label(header_frame, text="DASHBOARD DE PRODUÇÃO", 
         font=("Arial", 20, "bold"), fg="white", bg='#2c3e50').pack(expand=True)
tk.Label(header_frame, text="Controle de Qualidade e Análise de Defeitos", 
         font=("Arial", 12), fg="#ecf0f1", bg='#2c3e50').pack()

# Frame de filtros principal
filtro_frame = tk.Frame(root, bg='#ecf0f1')
filtro_frame.pack(fill='x', padx=15, pady=10)

# Filtros
filtros_left = tk.Frame(filtro_frame, bg='#ecf0f1')
filtros_left.pack(side='left', fill='x', expand=True)

tk.Label(filtros_left, text="Filtros de Período:", font=("Arial", 10, "bold"), bg='#ecf0f1').grid(row=0, column=0, padx=5, pady=2, sticky='w')

tk.Label(filtros_left, text="Data Inicial", bg='#ecf0f1').grid(row=1, column=0, padx=5, sticky='w')
data_inicial = DateEntry(filtros_left, width=12, date_pattern='dd/mm/yyyy')
data_inicial.grid(row=2, column=0, padx=5)

tk.Label(filtros_left, text="Data Final", bg='#ecf0f1').grid(row=1, column=1, padx=5, sticky='w')
data_final = DateEntry(filtros_left, width=12, date_pattern='dd/mm/yyyy')
data_final.grid(row=2, column=1, padx=5)

horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60,5)]
tk.Label(filtros_left, text="Hora Inicial", bg='#ecf0f1').grid(row=1, column=2, padx=5, sticky='w')
hora_inicial = ttk.Combobox(filtros_left, values=horas, width=8, state="readonly")
hora_inicial.grid(row=2, column=2, padx=5)
hora_inicial.set("00:00")

tk.Label(filtros_left, text="Hora Final", bg='#ecf0f1').grid(row=1, column=3, padx=5, sticky='w')
hora_final = ttk.Combobox(filtros_left, values=horas, width=8, state="readonly")
hora_final.grid(row=2, column=3, padx=5)
hora_final.set("23:55")

tk.Label(filtros_left, text="Máquina", bg='#ecf0f1').grid(row=1, column=4, padx=5, sticky='w')
maquina_main = ttk.Combobox(filtros_left, values=MAQUINAS_VALIDAS, width=8, state="readonly")
maquina_main.grid(row=2, column=4, padx=5)

# Botões de ação
botoes_frame = tk.Frame(filtro_frame, bg='#ecf0f1')
botoes_frame.pack(side='right')

btn_style = {"font": ("Arial", 10, "bold"), "width": 15, "height": 1}
tk.Button(botoes_frame, text="🔍 APLICAR FILTRO", command=aplicar_filtro_principal, 
          bg="#007bff", fg="white", **btn_style).pack(side='left', padx=2)
tk.Button(botoes_frame, text="🔄 LIMPAR FILTRO", command=limpar_filtro_principal, 
          bg="#6c757d", fg="white", **btn_style).pack(side='left', padx=2)
tk.Button(botoes_frame, text="📊 ATUALIZAR DADOS", command=atualizar_dados, 
          bg="#28a745", fg="white", **btn_style).pack(side='left', padx=2)
tk.Button(botoes_frame, text="🏭 ABRIR COLETOR", command=abrir_coletor, 
          bg="#ffc107", fg="black", **btn_style).pack(side='left', padx=2)

# Frame de gráficos rápidos
graficos_rapidos_frame = tk.Frame(root, bg='#f8f9fa')
graficos_rapidos_frame.pack(fill='x', padx=15, pady=10)

tk.Label(graficos_rapidos_frame, text="Relatórios Rápidos:", 
         font=("Arial", 12, "bold"), bg='#f8f9fa').pack(anchor='w')

botoes_graficos = tk.Frame(graficos_rapidos_frame, bg='#f8f9fa')
botoes_graficos.pack(fill='x', pady=5)

btn_graf_style = {"font": ("Arial", 10, "bold"), "width": 18, "height": 2}
tk.Button(botoes_graficos, text="📈 TOP 5 DEFEITOS", command=mostrar_grafico_top5, 
          bg="#17a2b8", fg="white", **btn_graf_style).pack(side='left', padx=5)
tk.Button(botoes_graficos, text="📊 GRÁFICO PARETO", command=mostrar_grafico_pareto, 
          bg="#6f42c1", fg="white", **btn_graf_style).pack(side='left', padx=5)
tk.Button(botoes_graficos, text="📋 MÉDIA DE REJEIÇÃO", command=mostrar_media_rejeicao, 
          bg="#e83e8c", fg="white", **btn_graf_style).pack(side='left', padx=5)

# Tabela principal
tree_frame = tk.Frame(root, bg='white')
tree_frame.pack(fill='both', expand=True, padx=15, pady=10)

# Adicionar scrollbar à tabela
scrollbar = ttk.Scrollbar(tree_frame)
scrollbar.pack(side='right', fill='y')

columns = ('Máquina', 'Rej1', 'Rej2', 'Rej3', 'CAM-D (%)', 'CAM-W (%)', 'Data/Hora')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')

tree.pack(fill='both', expand=True)

# Status bar
status_frame = tk.Frame(root, bg='#34495e', height=30)
status_frame.pack(fill='x', side='bottom')
status_frame.pack_propagate(False)

status_label = tk.Label(status_frame, text="Total de registros carregados: 0 | Última atualização: --/--/---- --:--", 
                       font=("Arial", 9), fg="white", bg='#34495e')
status_label.pack(side='left', padx=10)

# Inicializar com dados vazios
atualizar_tree(None)
atualizar_status()

# Configurar período inicial
dt_ini_date, dt_ini_time, dt_fim_date, dt_fim_time = get_last_24h_range()
data_inicial.set_date(dt_ini_date)
data_final.set_date(dt_fim_date)
hora_inicial.set(f"{dt_ini_time.hour:02d}:{(dt_ini_time.minute // 5) * 5:02d}")
hora_final.set(f"{dt_fim_time.hour:02d}:{(dt_fim_time.minute // 5) * 5:02d}")

print("✅ Dashboard inicializado com sucesso!")
print(f"📁 Caminho dos dados: {CSV_FILE}")
print("🎯 Sistema pronto para uso - Clique em ATUALIZAR DADOS para carregar informações")

# Iniciar aplicação
root.mainloop()

# =============================================================================
# Desenvolvido por: Pedro L. Vergueiro
# Sistema: Dashboard de Produção - Controle de Qualidade
# Compatível com: Coletor de Produção v8.0
# Data: Outubro 2025
# Contato: pedrolv.fsilva@gmail.com
# =============================================================================