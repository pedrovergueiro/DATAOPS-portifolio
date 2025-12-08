"""MessageBox sempre no topo - Sobrepõe todas as janelas"""

import tkinter as tk
from tkinter import messagebox as mb


def showinfo(title, message, parent=None):
    """Mostra mensagem de informação SEMPRE NO TOPO"""
    return _show_message(title, message, "info", parent)


def showwarning(title, message, parent=None):
    """Mostra mensagem de aviso SEMPRE NO TOPO"""
    return _show_message(title, message, "warning", parent)


def showerror(title, message, parent=None):
    """Mostra mensagem de erro SEMPRE NO TOPO"""
    return _show_message(title, message, "error", parent)


def askyesno(title, message, parent=None):
    """Pergunta Sim/Não SEMPRE NO TOPO"""
    return _show_question(title, message, "yesno", parent)


def askokcancel(title, message, parent=None):
    """Pergunta OK/Cancelar SEMPRE NO TOPO"""
    return _show_question(title, message, "okcancel", parent)


def askretrycancel(title, message, parent=None):
    """Pergunta Tentar Novamente/Cancelar SEMPRE NO TOPO"""
    return _show_question(title, message, "retrycancel", parent)


def _show_message(title, message, tipo, parent):
    """Mostra mensagem customizada SEMPRE NO TOPO"""
    # Criar janela temporária se não houver parent
    if parent is None:
        temp_root = tk.Tk()
        temp_root.withdraw()
        parent = temp_root
    
    # Criar janela de mensagem
    janela = tk.Toplevel(parent)
    janela.title(title)
    janela.attributes('-topmost', True)
    janela.grab_set()
    janela.resizable(False, False)
    
    # Ícones por tipo
    icones = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌"
    }
    
    cores = {
        "info": "#3498db",
        "warning": "#f39c12",
        "error": "#e74c3c"
    }
    
    # Frame principal
    frame = tk.Frame(janela, bg='white')
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Ícone e título
    tk.Label(frame, text=icones.get(tipo, "ℹ️"), 
             font=("Arial", 32), bg='white').pack(pady=(0, 10))
    
    tk.Label(frame, text=title, 
             font=("Arial", 12, "bold"), 
             fg=cores.get(tipo, "#3498db"), 
             bg='white').pack(pady=5)
    
    # Mensagem
    tk.Label(frame, text=message, 
             font=("Arial", 10), 
             bg='white', 
             wraplength=350, 
             justify='center').pack(pady=10)
    
    # Botão OK
    tk.Button(frame, text="OK", 
             command=janela.destroy,
             bg=cores.get(tipo, "#3498db"), 
             fg="white", 
             font=("Arial", 10, "bold"),
             width=15, 
             height=2).pack(pady=10)
    
    # Centralizar
    janela.update_idletasks()
    width = janela.winfo_width()
    height = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (width // 2)
    y = (janela.winfo_screenheight() // 2) - (height // 2)
    janela.geometry(f"+{x}+{y}")
    
    # Bind Enter para fechar
    janela.bind('<Return>', lambda e: janela.destroy())
    
    # Aguardar fechamento
    janela.wait_window()
    
    # Limpar janela temporária
    if isinstance(parent, tk.Tk) and parent.winfo_exists():
        try:
            parent.destroy()
        except:
            pass


def _show_question(title, message, tipo, parent):
    """Mostra pergunta customizada SEMPRE NO TOPO"""
    # Criar janela temporária se não houver parent
    if parent is None:
        temp_root = tk.Tk()
        temp_root.withdraw()
        parent = temp_root
    
    # Criar janela de pergunta
    janela = tk.Toplevel(parent)
    janela.title(title)
    janela.attributes('-topmost', True)
    janela.grab_set()
    janela.resizable(False, False)
    
    resultado = [False]
    
    # Frame principal
    frame = tk.Frame(janela, bg='white')
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Ícone
    tk.Label(frame, text="❓", 
             font=("Arial", 32), bg='white').pack(pady=(0, 10))
    
    # Título
    tk.Label(frame, text=title, 
             font=("Arial", 12, "bold"), 
             fg="#3498db", 
             bg='white').pack(pady=5)
    
    # Mensagem
    tk.Label(frame, text=message, 
             font=("Arial", 10), 
             bg='white', 
             wraplength=350, 
             justify='center').pack(pady=10)
    
    # Botões
    btn_frame = tk.Frame(frame, bg='white')
    btn_frame.pack(pady=10)
    
    def sim():
        resultado[0] = True
        janela.destroy()
    
    def nao():
        resultado[0] = False
        janela.destroy()
    
    if tipo == "yesno":
        tk.Button(btn_frame, text="✅ SIM", 
                 command=sim,
                 bg="#28a745", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=12, 
                 height=2).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="❌ NÃO", 
                 command=nao,
                 bg="#dc3545", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=12, 
                 height=2).pack(side='left', padx=5)
    
    elif tipo == "okcancel":
        tk.Button(btn_frame, text="✅ OK", 
                 command=sim,
                 bg="#28a745", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=12, 
                 height=2).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="❌ CANCELAR", 
                 command=nao,
                 bg="#6c757d", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=12, 
                 height=2).pack(side='left', padx=5)
    
    elif tipo == "retrycancel":
        tk.Button(btn_frame, text="🔄 TENTAR NOVAMENTE", 
                 command=sim,
                 bg="#3498db", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=15, 
                 height=2).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="❌ CANCELAR", 
                 command=nao,
                 bg="#6c757d", 
                 fg="white", 
                 font=("Arial", 10, "bold"),
                 width=12, 
                 height=2).pack(side='left', padx=5)
    
    # Centralizar
    janela.update_idletasks()
    width = janela.winfo_width()
    height = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (width // 2)
    y = (janela.winfo_screenheight() // 2) - (height // 2)
    janela.geometry(f"+{x}+{y}")
    
    # Aguardar fechamento
    janela.wait_window()
    
    # Limpar janela temporária
    if isinstance(parent, tk.Tk) and parent.winfo_exists():
        try:
            parent.destroy()
        except:
            pass
    
    return resultado[0]

