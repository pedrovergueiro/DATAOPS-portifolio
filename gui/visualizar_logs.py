"""
Interface para visualizar logs do sistema
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import threading
import time

def abrir_visualizador_logs(parent):
    """Abre janela para visualizar logs do sistema"""
    
    janela = tk.Toplevel(parent)
    janela.title("📋 Visualizador de Logs")
    janela.geometry("800x600")
    janela.attributes('-topmost', True)
    
    # Frame principal
    main_frame = tk.Frame(janela)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Header
    header_frame = tk.Frame(main_frame)
    header_frame.pack(fill='x', pady=(0, 10))
    
    tk.Label(header_frame, text="📋 LOGS DO SISTEMA", 
             font=("Arial", 14, "bold")).pack(side='left')
    
    # Botões de controle
    btn_frame = tk.Frame(header_frame)
    btn_frame.pack(side='right')
    
    # Área de texto para logs
    log_text = scrolledtext.ScrolledText(
        main_frame, 
        wrap=tk.WORD, 
        font=("Consolas", 9),
        bg='#1e1e1e',
        fg='#ffffff',
        insertbackground='white'
    )
    log_text.pack(fill='both', expand=True, pady=(0, 10))
    
    # Frame de status
    status_frame = tk.Frame(main_frame)
    status_frame.pack(fill='x')
    
    status_label = tk.Label(status_frame, text="Carregando logs...", 
                           font=("Arial", 9), fg='gray')
    status_label.pack(side='left')
    
    # Variáveis de controle
    auto_refresh = tk.BooleanVar(value=True)
    refresh_thread = None
    stop_refresh = threading.Event()
    
    def carregar_logs():
        """Carrega logs do sistema"""
        try:
            from utils.logger_executavel import get_recent_logs, get_log_path
            
            # Obter logs recentes
            logs = get_recent_logs(200)  # Últimas 200 linhas
            
            # Limpar e inserir logs
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, logs)
            
            # Scroll para o final
            log_text.see(tk.END)
            
            # Atualizar status
            log_path = get_log_path()
            if log_path and os.path.exists(log_path):
                size_kb = os.path.getsize(log_path) / 1024
                status_label.config(text=f"Arquivo: {os.path.basename(log_path)} ({size_kb:.1f} KB)")
            else:
                status_label.config(text="Arquivo de log não encontrado")
                
        except Exception as e:
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, f"Erro ao carregar logs: {e}")
            status_label.config(text="Erro ao carregar logs")
    
    def refresh_automatico():
        """Thread para refresh automático"""
        while not stop_refresh.is_set():
            if auto_refresh.get():
                try:
                    janela.after(0, carregar_logs)
                except:
                    break
            
            # Aguardar 2 segundos
            for _ in range(20):
                if stop_refresh.is_set():
                    break
                time.sleep(0.1)
    
    def toggle_auto_refresh():
        """Liga/desliga refresh automático"""
        if auto_refresh.get():
            btn_auto.config(text="🔄 Auto (ON)", bg="#28a745")
        else:
            btn_auto.config(text="🔄 Auto (OFF)", bg="#6c757d")
    
    def atualizar_manual():
        """Atualização manual"""
        carregar_logs()
    
    def limpar_logs():
        """Limpa a visualização"""
        log_text.delete(1.0, tk.END)
        status_label.config(text="Logs limpos")
    
    def salvar_logs():
        """Salva logs em arquivo"""
        try:
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Logs",
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
            )
            
            if arquivo:
                conteudo = log_text.get(1.0, tk.END)
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                
                messagebox.showinfo("Sucesso", f"Logs salvos em:\n{arquivo}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar logs:\n{e}")
    
    def abrir_pasta_logs():
        """Abre pasta dos logs no explorador"""
        try:
            from utils.logger_executavel import get_log_path
            log_path = get_log_path()
            
            if log_path and os.path.exists(log_path):
                pasta = os.path.dirname(log_path)
                os.startfile(pasta)  # Windows
            else:
                messagebox.showwarning("Aviso", "Pasta de logs não encontrada")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")
    
    def filtrar_logs():
        """Filtrar logs por texto"""
        def aplicar_filtro():
            filtro = entry_filtro.get().strip().lower()
            if not filtro:
                carregar_logs()
                return
            
            try:
                from utils.logger_executavel import get_recent_logs
                logs_completos = get_recent_logs(1000)
                
                # Filtrar linhas
                linhas = logs_completos.split('\n')
                linhas_filtradas = [linha for linha in linhas if filtro in linha.lower()]
                
                # Mostrar resultado
                log_text.delete(1.0, tk.END)
                log_text.insert(tk.END, '\n'.join(linhas_filtradas))
                
                status_label.config(text=f"Filtro: '{filtro}' - {len(linhas_filtradas)} linhas")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao filtrar: {e}")
        
        # Janela de filtro
        filtro_window = tk.Toplevel(janela)
        filtro_window.title("🔍 Filtrar Logs")
        filtro_window.geometry("400x150")
        filtro_window.attributes('-topmost', True)
        
        tk.Label(filtro_window, text="Filtrar logs por texto:", 
                font=("Arial", 11)).pack(pady=10)
        
        entry_filtro = tk.Entry(filtro_window, font=("Arial", 11), width=40)
        entry_filtro.pack(pady=5)
        entry_filtro.focus()
        
        btn_filtrar = tk.Button(filtro_window, text="🔍 Filtrar", 
                               command=aplicar_filtro, bg="#007bff", fg="white",
                               font=("Arial", 10, "bold"))
        btn_filtrar.pack(pady=10)
        
        entry_filtro.bind('<Return>', lambda e: aplicar_filtro())
    
    # Criar botões
    tk.Button(btn_frame, text="🔄 Atualizar", command=atualizar_manual,
             bg="#007bff", fg="white", font=("Arial", 9)).pack(side='left', padx=2)
    
    btn_auto = tk.Button(btn_frame, text="🔄 Auto (ON)", command=toggle_auto_refresh,
                        bg="#28a745", fg="white", font=("Arial", 9))
    btn_auto.pack(side='left', padx=2)
    
    tk.Button(btn_frame, text="🔍 Filtrar", command=filtrar_logs,
             bg="#ffc107", fg="black", font=("Arial", 9)).pack(side='left', padx=2)
    
    tk.Button(btn_frame, text="🗑️ Limpar", command=limpar_logs,
             bg="#dc3545", fg="white", font=("Arial", 9)).pack(side='left', padx=2)
    
    tk.Button(btn_frame, text="💾 Salvar", command=salvar_logs,
             bg="#28a745", fg="white", font=("Arial", 9)).pack(side='left', padx=2)
    
    tk.Button(btn_frame, text="📁 Pasta", command=abrir_pasta_logs,
             bg="#6c757d", fg="white", font=("Arial", 9)).pack(side='left', padx=2)
    
    # Checkbox para auto-refresh
    tk.Checkbutton(status_frame, text="Atualização automática", 
                  variable=auto_refresh, command=toggle_auto_refresh,
                  font=("Arial", 9)).pack(side='right')
    
    # Carregar logs inicial
    carregar_logs()
    
    # Iniciar thread de refresh automático
    refresh_thread = threading.Thread(target=refresh_automatico, daemon=True)
    refresh_thread.start()
    
    # Cleanup ao fechar
    def on_closing():
        stop_refresh.set()
        janela.destroy()
    
    janela.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Centralizar janela
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() - janela.winfo_width()) // 2
    y = (janela.winfo_screenheight() - janela.winfo_height()) // 2
    janela.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    # Teste standalone
    root = tk.Tk()
    root.withdraw()
    abrir_visualizador_logs(root)
    root.mainloop()