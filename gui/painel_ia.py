"""Painel de Inteligência Artificial e Machine Learning"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from ml.predictor import PredicaoInteligente


def abrir_painel_ia(root, data_manager, machine_config):
    """Abre painel de IA com análises e predições"""
    
    # Inicializar IA
    ia = PredicaoInteligente(data_manager)
    
    janela_ia = tk.Toplevel(root)
    janela_ia.title("🤖 Painel de Inteligência Artificial")
    janela_ia.geometry("1600x900")
    janela_ia.attributes('-topmost', True)
    
    # Header
    header_frame = tk.Frame(janela_ia, bg='#6f42c1', height=100)
    header_frame.pack(fill='x', padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🤖 INTELIGÊNCIA ARTIFICIAL", 
             font=("Arial", 20, "bold"), fg="white", bg='#6f42c1').pack(expand=True)
    tk.Label(header_frame, text="Análise Preditiva e Recomendações Inteligentes", 
             font=("Arial", 11), fg="white", bg='#6f42c1').pack()
    
    # Notebook
    notebook = ttk.Notebook(janela_ia)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # ABA 1: Predição de Defeitos
    tab_predicao = ttk.Frame(notebook)
    notebook.add(tab_predicao, text="🔮 Predição de Defeitos")
    criar_aba_predicao(tab_predicao, ia, machine_config)
    
    # ABA 2: Detecção de Anomalias
    tab_anomalias = ttk.Frame(notebook)
    notebook.add(tab_anomalias, text="⚠️ Detecção de Anomalias")
    criar_aba_anomalias(tab_anomalias, ia, machine_config)
    
    # ABA 3: Recomendações Inteligentes
    tab_recomendacoes = ttk.Frame(notebook)
    notebook.add(tab_recomendacoes, text="💡 Recomendações")
    criar_aba_recomendacoes(tab_recomendacoes, ia, machine_config)
    
    # ABA 4: Relatório Completo
    tab_relatorio = ttk.Frame(notebook)
    notebook.add(tab_relatorio, text="📊 Relatório IA")
    criar_aba_relatorio(tab_relatorio, ia, machine_config)


def criar_aba_predicao(parent, ia, machine_config):
    """Cria aba de predição de defeitos"""
    
    frame_principal = tk.Frame(parent)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="🔮 PREDIÇÃO DE DEFEITOS", 
             font=("Arial", 16, "bold"), fg="#6f42c1").pack(pady=10)
    
    tk.Label(frame_principal, text="IA analisa padrões históricos para prever próximos defeitos", 
             font=("Arial", 10), fg="#666").pack(pady=5)
    
    # Seleção de máquina
    frame_selecao = tk.Frame(frame_principal)
    frame_selecao.pack(fill='x', pady=15)
    
    tk.Label(frame_selecao, text="Selecione a máquina:", 
             font=("Arial", 11, "bold")).pack(side='left', padx=10)
    
    maquina_var = tk.StringVar()
    MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
    maquina_var.set(MAQUINA_ATUAL)
    
    from config.constants import TABELA_SIZES
    maquinas = list(TABELA_SIZES.keys())
    
    combo_maquina = ttk.Combobox(frame_selecao, textvariable=maquina_var, 
                                 values=maquinas, state="readonly", 
                                 width=15, font=("Arial", 11))
    combo_maquina.pack(side='left', padx=10)
    
    # Frame de resultados
    frame_resultados = tk.LabelFrame(frame_principal, text="Resultados da Predição", 
                                     font=("Arial", 11, "bold"))
    frame_resultados.pack(fill='both', expand=True, pady=10)
    
    # Text widget para mostrar resultados
    text_resultados = scrolledtext.ScrolledText(frame_resultados, 
                                                font=("Consolas", 10), 
                                                height=25, wrap=tk.WORD)
    text_resultados.pack(fill='both', expand=True, padx=10, pady=10)
    
    def executar_predicao():
        maquina = maquina_var.get()
        if not maquina:
            messagebox.showwarning("Aviso", "Selecione uma máquina!")
            return
        
        text_resultados.delete(1.0, tk.END)
        text_resultados.insert(tk.END, f"🔄 Analisando dados da máquina {maquina}...\n\n")
        text_resultados.update()
        
        # Executar predição
        resultado = ia.prever_proximo_defeito(maquina)
        
        if not resultado:
            text_resultados.insert(tk.END, "❌ Nenhum dado disponível para esta máquina\n")
            return
        
        if 'erro' in resultado:
            text_resultados.insert(tk.END, f"⚠️ {resultado['erro']}\n")
            return
        
        # Mostrar resultados
        text_resultados.insert(tk.END, "="*80 + "\n")
        text_resultados.insert(tk.END, f"🤖 PREDIÇÃO DE DEFEITOS - MÁQUINA {maquina}\n")
        text_resultados.insert(tk.END, "="*80 + "\n\n")
        
        # Defeito mais provável
        if resultado.get('defeito_mais_provavel'):
            defeito = resultado['defeito_mais_provavel']
            text_resultados.insert(tk.END, "🎯 DEFEITO MAIS PROVÁVEL:\n")
            text_resultados.insert(tk.END, f"   Defeito: {defeito['defeito']}\n")
            text_resultados.insert(tk.END, f"   Probabilidade: {defeito['probabilidade']}%\n")
            text_resultados.insert(tk.END, f"   Nível de Risco: {defeito['nivel_risco']}\n")
            text_resultados.insert(tk.END, f"   Ocorrências: {defeito['ocorrencias']}x\n\n")
        
        # Top 5 predições
        text_resultados.insert(tk.END, "📊 TOP 5 DEFEITOS PREVISTOS:\n\n")
        for i, pred in enumerate(resultado.get('predicoes', []), 1):
            text_resultados.insert(tk.END, f"{i}. {pred['defeito']}\n")
            text_resultados.insert(tk.END, f"   Probabilidade: {pred['probabilidade']}%\n")
            text_resultados.insert(tk.END, f"   Risco: {pred['nivel_risco']}\n")
            text_resultados.insert(tk.END, f"   Ocorrências: {pred['ocorrencias']}x\n\n")
        
        # Tendência
        text_resultados.insert(tk.END, f"📈 TENDÊNCIA: {resultado.get('tendencia', 'N/D')}\n\n")
        
        # Confiança
        text_resultados.insert(tk.END, f"🎯 CONFIANÇA DA PREDIÇÃO: {resultado.get('confianca', 'N/D')}\n\n")
        
        # Recomendação
        text_resultados.insert(tk.END, "💡 RECOMENDAÇÃO:\n")
        text_resultados.insert(tk.END, f"{resultado.get('recomendacao', 'N/D')}\n\n")
        
        text_resultados.insert(tk.END, "="*80 + "\n")
    
    # Botão de executar
    tk.Button(frame_selecao, text="🔮 PREVER DEFEITOS", 
             command=executar_predicao,
             bg="#6f42c1", fg="white", font=("Arial", 11, "bold"),
             width=20, height=2).pack(side='left', padx=10)


def criar_aba_anomalias(parent, ia, machine_config):
    """Cria aba de detecção de anomalias"""
    
    frame_principal = tk.Frame(parent)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="⚠️ DETECÇÃO DE ANOMALIAS", 
             font=("Arial", 16, "bold"), fg="#dc3545").pack(pady=10)
    
    tk.Label(frame_principal, text="IA identifica padrões anormais e comportamentos suspeitos", 
             font=("Arial", 10), fg="#666").pack(pady=5)
    
    # Seleção de máquina
    frame_selecao = tk.Frame(frame_principal)
    frame_selecao.pack(fill='x', pady=15)
    
    tk.Label(frame_selecao, text="Máquina:", 
             font=("Arial", 11, "bold")).pack(side='left', padx=10)
    
    maquina_var = tk.StringVar()
    
    from config.constants import TABELA_SIZES
    maquinas = ['TODAS'] + list(TABELA_SIZES.keys())
    
    combo_maquina = ttk.Combobox(frame_selecao, textvariable=maquina_var, 
                                 values=maquinas, state="readonly", 
                                 width=15, font=("Arial", 11))
    combo_maquina.pack(side='left', padx=10)
    combo_maquina.current(0)
    
    # Frame de resultados
    frame_resultados = tk.LabelFrame(frame_principal, text="Anomalias Detectadas", 
                                     font=("Arial", 11, "bold"))
    frame_resultados.pack(fill='both', expand=True, pady=10)
    
    # Treeview para anomalias
    colunas = ('Tipo', 'Máquina', 'Detalhes', 'Severidade')
    tree = ttk.Treeview(frame_resultados, columns=colunas, show='headings', height=20)
    
    for col in colunas:
        tree.heading(col, text=col)
    
    tree.column('Tipo', width=150)
    tree.column('Máquina', width=100)
    tree.column('Detalhes', width=600)
    tree.column('Severidade', width=100)
    
    scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    scrollbar.pack(side='right', fill='y', pady=10)
    
    def detectar_anomalias():
        # Limpar tree
        for item in tree.get_children():
            tree.delete(item)
        
        maquina = maquina_var.get()
        maquina_filtro = None if maquina == 'TODAS' else maquina
        
        # Detectar anomalias
        anomalias = ia.detectar_anomalias(maquina_filtro)
        
        if not anomalias:
            tree.insert('', 'end', values=('---', '---', '✅ Nenhuma anomalia detectada', '---'))
            return
        
        # Mostrar anomalias
        for anomalia in anomalias:
            tipo = anomalia.get('tipo', 'N/D')
            maq = anomalia.get('maquina', 'N/D')
            severidade = anomalia.get('severidade', 'N/D')
            
            # Montar detalhes
            if tipo == 'pico_rejeicao':
                detalhes = f"{anomalia.get('metrica', 'N/D')}: {anomalia.get('valor', 0)}% (limite: {anomalia.get('limite_esperado', 0)}%)"
            elif tipo == 'mudanca_padrao':
                detalhes = f"{anomalia.get('metrica', 'N/D')}: Variação de {anomalia.get('variacao_percentual', 0)}%"
            elif tipo == 'defeito_repetitivo':
                detalhes = f"Defeito '{anomalia.get('defeito', 'N/D')}' repetido {anomalia.get('frequencia', 0)}x ({anomalia.get('percentual', 0)}%)"
            else:
                detalhes = str(anomalia)
            
            # Cor por severidade
            tag = 'alta' if severidade == 'ALTA' else 'media'
            tree.insert('', 'end', values=(tipo, maq, detalhes, severidade), tags=(tag,))
        
        # Configurar cores
        tree.tag_configure('alta', background='#ffcccc')
        tree.tag_configure('media', background='#fff3cd')
    
    # Botão de detectar
    tk.Button(frame_selecao, text="⚠️ DETECTAR ANOMALIAS", 
             command=detectar_anomalias,
             bg="#dc3545", fg="white", font=("Arial", 11, "bold"),
             width=20, height=2).pack(side='left', padx=10)


def criar_aba_recomendacoes(parent, ia, machine_config):
    """Cria aba de recomendações inteligentes"""
    
    frame_principal = tk.Frame(parent)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="💡 RECOMENDAÇÕES INTELIGENTES", 
             font=("Arial", 16, "bold"), fg="#28a745").pack(pady=10)
    
    tk.Label(frame_principal, text="IA sugere ações baseadas em análise de dados históricos", 
             font=("Arial", 10), fg="#666").pack(pady=5)
    
    # Seleção de máquina
    frame_selecao = tk.Frame(frame_principal)
    frame_selecao.pack(fill='x', pady=15)
    
    tk.Label(frame_selecao, text="Máquina:", 
             font=("Arial", 11, "bold")).pack(side='left', padx=10)
    
    maquina_var = tk.StringVar()
    MAQUINA_ATUAL = machine_config.obter_configuracao_maquina()
    maquina_var.set(MAQUINA_ATUAL)
    
    from config.constants import TABELA_SIZES
    maquinas = list(TABELA_SIZES.keys())
    
    combo_maquina = ttk.Combobox(frame_selecao, textvariable=maquina_var, 
                                 values=maquinas, state="readonly", 
                                 width=15, font=("Arial", 11))
    combo_maquina.pack(side='left', padx=10)
    
    # Frame de resultados
    frame_resultados = tk.LabelFrame(frame_principal, text="Recomendações", 
                                     font=("Arial", 11, "bold"))
    frame_resultados.pack(fill='both', expand=True, pady=10)
    
    # Treeview para recomendações
    colunas = ('Prioridade', 'Tipo', 'Ação', 'Impacto')
    tree = ttk.Treeview(frame_resultados, columns=colunas, show='headings', height=20)
    
    for col in colunas:
        tree.heading(col, text=col)
    
    tree.column('Prioridade', width=120)
    tree.column('Tipo', width=150)
    tree.column('Ação', width=600)
    tree.column('Impacto', width=300)
    
    scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    scrollbar.pack(side='right', fill='y', pady=10)
    
    def gerar_recomendacoes():
        # Limpar tree
        for item in tree.get_children():
            tree.delete(item)
        
        maquina = maquina_var.get()
        if not maquina:
            messagebox.showwarning("Aviso", "Selecione uma máquina!")
            return
        
        # Gerar recomendações
        recomendacoes = ia.recomendar_acoes(maquina)
        
        if not recomendacoes:
            tree.insert('', 'end', values=('---', '---', '✅ Nenhuma recomendação no momento', '---'))
            return
        
        # Mostrar recomendações
        for rec in recomendacoes:
            prioridade = rec.get('prioridade', 'N/D')
            tipo = rec.get('tipo', 'N/D')
            acao = rec.get('acao', 'N/D')
            impacto = rec.get('impacto', 'N/D')
            
            # Cor por prioridade
            if prioridade == 'URGENTE':
                tag = 'urgente'
            elif prioridade == 'ALTA':
                tag = 'alta'
            elif prioridade == 'MÉDIA':
                tag = 'media'
            else:
                tag = 'baixa'
            
            tree.insert('', 'end', values=(prioridade, tipo, acao, impacto), tags=(tag,))
        
        # Configurar cores
        tree.tag_configure('urgente', background='#ff0000', foreground='white')
        tree.tag_configure('alta', background='#ffcccc')
        tree.tag_configure('media', background='#fff3cd')
        tree.tag_configure('baixa', background='#d4edda')
    
    # Botão de gerar
    tk.Button(frame_selecao, text="💡 GERAR RECOMENDAÇÕES", 
             command=gerar_recomendacoes,
             bg="#28a745", fg="white", font=("Arial", 11, "bold"),
             width=22, height=2).pack(side='left', padx=10)


def criar_aba_relatorio(parent, ia, machine_config):
    """Cria aba de relatório completo de IA"""
    
    frame_principal = tk.Frame(parent)
    frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame_principal, text="📊 RELATÓRIO COMPLETO DE IA", 
             font=("Arial", 16, "bold"), fg="#17a2b8").pack(pady=10)
    
    tk.Label(frame_principal, text="Análise completa com todos os insights de IA", 
             font=("Arial", 10), fg="#666").pack(pady=5)
    
    # Botões
    frame_botoes = tk.Frame(frame_principal)
    frame_botoes.pack(fill='x', pady=15)
    
    # Text widget para relatório
    text_relatorio = scrolledtext.ScrolledText(frame_principal, 
                                               font=("Consolas", 9), 
                                               height=30, wrap=tk.WORD)
    text_relatorio.pack(fill='both', expand=True, pady=10)
    
    def gerar_relatorio_completo():
        text_relatorio.delete(1.0, tk.END)
        text_relatorio.insert(tk.END, "🔄 Gerando relatório completo de IA...\n\n")
        text_relatorio.update()
        
        # Gerar relatório
        relatorio = ia.gerar_relatorio_ia()
        
        if not relatorio:
            text_relatorio.insert(tk.END, "❌ Nenhum dado disponível\n")
            return
        
        # Mostrar relatório
        text_relatorio.delete(1.0, tk.END)
        text_relatorio.insert(tk.END, json.dumps(relatorio, indent=2, ensure_ascii=False))
    
    tk.Button(frame_botoes, text="📊 GERAR RELATÓRIO COMPLETO", 
             command=gerar_relatorio_completo,
             bg="#17a2b8", fg="white", font=("Arial", 12, "bold"),
             width=30, height=2).pack(pady=10)

