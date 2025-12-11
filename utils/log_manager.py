"""
Sistema Avançado de Gerenciamento de Logs e Prints
Permite visualizar, filtrar, excluir e gerenciar todos os logs do sistema
"""

import os
import sys
import glob
import json
import datetime
import shutil
from pathlib import Path
from typing import List, Dict, Optional

# Imports condicionais para GUI (apenas quando necessário)
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

class LogManager:
    """Gerenciador completo de logs do sistema"""
    
    def __init__(self):
        self.base_dir = self._get_base_dir()
        self.log_dir = os.path.join(self.base_dir, 'logs')
        self.backup_dir = os.path.join(self.base_dir, 'logs_backup')
        
        # Criar diretórios se não existirem
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def _get_base_dir(self) -> str:
        """Determina diretório base do sistema"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.dirname(__file__))
    
    def encontrar_logs(self, pattern: str = "*.txt") -> List[str]:
        """Encontra todos os arquivos de log"""
        pattern_path = os.path.join(self.log_dir, pattern)
        arquivos = glob.glob(pattern_path)
        
        # Incluir logs de diferentes tipos
        patterns = [
            "coletor_log_*.txt",
            "sistema_*.log",
            "debug_*.txt",
            "error_*.log",
            "comunicacao_*.log",
            "comandos_*.log"
        ]
        
        for p in patterns:
            pattern_path = os.path.join(self.log_dir, p)
            arquivos.extend(glob.glob(pattern_path))
        
        # Remover duplicatas e ordenar por data
        arquivos = list(set(arquivos))
        arquivos.sort(key=os.path.getmtime, reverse=True)
        
        return arquivos
    
    def obter_info_log(self, arquivo: str) -> Dict:
        """Obtém informações detalhadas de um log"""
        try:
            stat = os.stat(arquivo)
            
            return {
                'nome': os.path.basename(arquivo),
                'caminho': arquivo,
                'tamanho': stat.st_size,
                'tamanho_kb': stat.st_size / 1024,
                'tamanho_mb': stat.st_size / (1024 * 1024),
                'modificado': stat.st_mtime,
                'modificado_str': datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
                'criado': stat.st_ctime,
                'criado_str': datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                'linhas': self._contar_linhas(arquivo),
                'tipo': self._identificar_tipo_log(arquivo)
            }
        except Exception as e:
            return {
                'nome': os.path.basename(arquivo),
                'caminho': arquivo,
                'erro': str(e)
            }
    
    def _contar_linhas(self, arquivo: str) -> int:
        """Conta número de linhas no arquivo"""
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except:
            return 0
    
    def _identificar_tipo_log(self, arquivo: str) -> str:
        """Identifica tipo do log baseado no nome"""
        nome = os.path.basename(arquivo).lower()
        
        if 'error' in nome or 'erro' in nome:
            return 'ERROR'
        elif 'debug' in nome:
            return 'DEBUG'
        elif 'comunicacao' in nome or 'comm' in nome:
            return 'COMUNICAÇÃO'
        elif 'comando' in nome:
            return 'COMANDOS'
        elif 'sistema' in nome:
            return 'SISTEMA'
        elif 'coletor' in nome:
            return 'PRINCIPAL'
        else:
            return 'GERAL'
    
    def ler_log(self, arquivo: str, linhas: Optional[int] = None, filtro: Optional[str] = None) -> str:
        """Lê conteúdo do log com opções de filtro"""
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
            
            # Aplicar filtro se especificado
            if filtro:
                linhas_filtradas = []
                for linha in conteudo.split('\n'):
                    if filtro.lower() in linha.lower():
                        linhas_filtradas.append(linha)
                conteudo = '\n'.join(linhas_filtradas)
            
            # Limitar número de linhas se especificado
            if linhas:
                linhas_conteudo = conteudo.split('\n')
                if len(linhas_conteudo) > linhas:
                    conteudo = '\n'.join(linhas_conteudo[-linhas:])
                    conteudo = f"... (mostrando últimas {linhas} linhas) ...\n\n" + conteudo
            
            return conteudo
            
        except Exception as e:
            return f"❌ Erro ao ler arquivo: {e}"
    
    def excluir_log(self, arquivo: str, fazer_backup: bool = True) -> bool:
        """Exclui log com opção de backup"""
        try:
            if fazer_backup:
                # Fazer backup antes de excluir
                nome_backup = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(arquivo)}"
                caminho_backup = os.path.join(self.backup_dir, nome_backup)
                shutil.copy2(arquivo, caminho_backup)
            
            os.remove(arquivo)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao excluir log: {e}")
            return False
    
    def limpar_logs_antigos(self, dias: int = 30) -> int:
        """Remove logs mais antigos que X dias"""
        agora = datetime.datetime.now()
        limite = agora - datetime.timedelta(days=dias)
        
        arquivos = self.encontrar_logs()
        removidos = 0
        
        for arquivo in arquivos:
            try:
                modificado = datetime.datetime.fromtimestamp(os.path.getmtime(arquivo))
                if modificado < limite:
                    if self.excluir_log(arquivo, fazer_backup=True):
                        removidos += 1
            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")
        
        return removidos
    
    def exportar_logs(self, destino: str, filtro_tipo: Optional[str] = None) -> bool:
        """Exporta logs para um diretório"""
        try:
            os.makedirs(destino, exist_ok=True)
            
            arquivos = self.encontrar_logs()
            copiados = 0
            
            for arquivo in arquivos:
                info = self.obter_info_log(arquivo)
                
                # Aplicar filtro de tipo se especificado
                if filtro_tipo and info.get('tipo') != filtro_tipo:
                    continue
                
                nome_destino = f"export_{datetime.datetime.now().strftime('%Y%m%d')}_{info['nome']}"
                caminho_destino = os.path.join(destino, nome_destino)
                
                shutil.copy2(arquivo, caminho_destino)
                copiados += 1
            
            return copiados > 0
            
        except Exception as e:
            print(f"❌ Erro ao exportar logs: {e}")
            return False


class LogViewerGUI:
    """Interface gráfica para visualização e gerenciamento de logs"""
    
    def __init__(self, parent=None):
        if not GUI_AVAILABLE:
            raise ImportError("Tkinter não está disponível. Interface gráfica não pode ser criada.")
        
        self.log_manager = LogManager()
        self.parent = parent
        
        # Criar janela
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        
        self.root.title("📋 Gerenciador de Logs e Prints - Sistema de Produção")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.logs_atuais = []
        self.log_selecionado = None
        
        self.criar_interface()
        self.atualizar_lista_logs()
    
    def criar_interface(self):
        """Cria interface gráfica completa"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="📋 GERENCIADOR DE LOGS E PRINTS", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Frame de controles superiores
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de ação
        ttk.Button(controls_frame, text="🔄 Atualizar", 
                  command=self.atualizar_lista_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(controls_frame, text="🗑️ Excluir Selecionado", 
                  command=self.excluir_selecionado).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(controls_frame, text="🧹 Limpar Antigos", 
                  command=self.limpar_antigos).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(controls_frame, text="📤 Exportar", 
                  command=self.exportar_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(controls_frame, text="📁 Abrir Pasta", 
                  command=self.abrir_pasta_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 Filtros")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro por tipo
        ttk.Label(filter_frame, text="Tipo:").pack(side=tk.LEFT, padx=(5, 2))
        self.tipo_var = tk.StringVar(value="TODOS")
        tipo_combo = ttk.Combobox(filter_frame, textvariable=self.tipo_var, 
                                 values=["TODOS", "PRINCIPAL", "ERROR", "DEBUG", "COMUNICAÇÃO", "COMANDOS", "SISTEMA", "GERAL"],
                                 width=15)
        tipo_combo.pack(side=tk.LEFT, padx=(0, 10))
        tipo_combo.bind('<<ComboboxSelected>>', lambda e: self.filtrar_logs())
        
        # Filtro por texto
        ttk.Label(filter_frame, text="Buscar:").pack(side=tk.LEFT, padx=(5, 2))
        self.busca_var = tk.StringVar()
        busca_entry = ttk.Entry(filter_frame, textvariable=self.busca_var, width=20)
        busca_entry.pack(side=tk.LEFT, padx=(0, 5))
        busca_entry.bind('<KeyRelease>', lambda e: self.filtrar_logs())
        
        ttk.Button(filter_frame, text="🔍", command=self.filtrar_logs).pack(side=tk.LEFT)
        
        # Frame principal dividido
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Frame esquerdo - Lista de logs
        left_frame = ttk.LabelFrame(paned, text="📋 Lista de Logs")
        paned.add(left_frame, weight=1)
        
        # Treeview para logs
        columns = ('Nome', 'Tipo', 'Tamanho', 'Linhas', 'Modificado')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.tree.heading('Nome', text='📄 Nome do Arquivo')
        self.tree.heading('Tipo', text='🏷️ Tipo')
        self.tree.heading('Tamanho', text='📊 Tamanho')
        self.tree.heading('Linhas', text='📝 Linhas')
        self.tree.heading('Modificado', text='📅 Modificado')
        
        self.tree.column('Nome', width=250)
        self.tree.column('Tipo', width=100)
        self.tree.column('Tamanho', width=80)
        self.tree.column('Linhas', width=80)
        self.tree.column('Modificado', width=150)
        
        # Scrollbar para treeview
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleção
        self.tree.bind('<<TreeviewSelect>>', self.on_log_select)
        
        # Frame direito - Visualização do log
        right_frame = ttk.LabelFrame(paned, text="👁️ Conteúdo do Log")
        paned.add(right_frame, weight=2)
        
        # Controles do visualizador
        viewer_controls = ttk.Frame(right_frame)
        viewer_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(viewer_controls, text="Últimas linhas:").pack(side=tk.LEFT)
        self.linhas_var = tk.StringVar(value="1000")
        linhas_spin = ttk.Spinbox(viewer_controls, from_=100, to=10000, increment=100, 
                                 textvariable=self.linhas_var, width=10)
        linhas_spin.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(viewer_controls, text="Filtrar texto:").pack(side=tk.LEFT)
        self.filtro_texto_var = tk.StringVar()
        filtro_entry = ttk.Entry(viewer_controls, textvariable=self.filtro_texto_var, width=20)
        filtro_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        ttk.Button(viewer_controls, text="🔄 Recarregar", 
                  command=self.recarregar_conteudo).pack(side=tk.LEFT, padx=(5, 0))
        
        # Área de texto para conteúdo
        self.text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 9))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame de informações
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Informações")
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = ttk.Label(info_frame, text="Selecione um log para ver detalhes")
        self.info_label.pack(padx=10, pady=5)
    
    def atualizar_lista_logs(self):
        """Atualiza lista de logs na interface"""
        # Limpar árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obter logs
        self.logs_atuais = []
        arquivos = self.log_manager.encontrar_logs()
        
        for arquivo in arquivos:
            info = self.log_manager.obter_info_log(arquivo)
            
            if 'erro' not in info:
                self.logs_atuais.append(info)
                
                # Formatar tamanho
                if info['tamanho_mb'] > 1:
                    tamanho_str = f"{info['tamanho_mb']:.1f} MB"
                else:
                    tamanho_str = f"{info['tamanho_kb']:.1f} KB"
                
                # Inserir na árvore
                self.tree.insert('', 'end', values=(
                    info['nome'],
                    info['tipo'],
                    tamanho_str,
                    info['linhas'],
                    info['modificado_str']
                ))
        
        # Atualizar informações
        total_logs = len(self.logs_atuais)
        total_tamanho = sum(log['tamanho_mb'] for log in self.logs_atuais)
        
        self.info_label.config(text=f"📊 Total: {total_logs} logs | 💾 Tamanho total: {total_tamanho:.1f} MB")
    
    def filtrar_logs(self):
        """Aplica filtros na lista de logs"""
        tipo_filtro = self.tipo_var.get()
        busca_filtro = self.busca_var.get().lower()
        
        # Limpar árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aplicar filtros
        logs_filtrados = []
        
        for log in self.logs_atuais:
            # Filtro por tipo
            if tipo_filtro != "TODOS" and log['tipo'] != tipo_filtro:
                continue
            
            # Filtro por busca
            if busca_filtro and busca_filtro not in log['nome'].lower():
                continue
            
            logs_filtrados.append(log)
            
            # Formatar tamanho
            if log['tamanho_mb'] > 1:
                tamanho_str = f"{log['tamanho_mb']:.1f} MB"
            else:
                tamanho_str = f"{log['tamanho_kb']:.1f} KB"
            
            # Inserir na árvore
            self.tree.insert('', 'end', values=(
                log['nome'],
                log['tipo'],
                tamanho_str,
                log['linhas'],
                log['modificado_str']
            ))
        
        # Atualizar informações
        total_filtrados = len(logs_filtrados)
        total_tamanho = sum(log['tamanho_mb'] for log in logs_filtrados)
        
        self.info_label.config(text=f"📊 Filtrados: {total_filtrados} logs | 💾 Tamanho: {total_tamanho:.1f} MB")
    
    def on_log_select(self, event):
        """Evento de seleção de log"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        nome_arquivo = item['values'][0]
        
        # Encontrar log selecionado
        self.log_selecionado = None
        for log in self.logs_atuais:
            if log['nome'] == nome_arquivo:
                self.log_selecionado = log
                break
        
        if self.log_selecionado:
            self.recarregar_conteudo()
    
    def recarregar_conteudo(self):
        """Recarrega conteúdo do log selecionado"""
        if not self.log_selecionado:
            return
        
        try:
            linhas = int(self.linhas_var.get())
        except:
            linhas = 1000
        
        filtro = self.filtro_texto_var.get().strip() or None
        
        # Ler conteúdo
        conteudo = self.log_manager.ler_log(
            self.log_selecionado['caminho'], 
            linhas=linhas, 
            filtro=filtro
        )
        
        # Atualizar área de texto
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, conteudo)
        
        # Ir para o final
        self.text_area.see(tk.END)
    
    def excluir_selecionado(self):
        """Exclui log selecionado"""
        if not self.log_selecionado:
            messagebox.showwarning("Aviso", "Selecione um log para excluir")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja excluir o log '{self.log_selecionado['nome']}'?\n\n"
            f"Um backup será criado automaticamente."
        )
        
        if resposta:
            if self.log_manager.excluir_log(self.log_selecionado['caminho']):
                messagebox.showinfo("Sucesso", "Log excluído com sucesso!\nBackup criado.")
                self.atualizar_lista_logs()
                self.text_area.delete(1.0, tk.END)
            else:
                messagebox.showerror("Erro", "Falha ao excluir log")
    
    def limpar_antigos(self):
        """Limpa logs antigos"""
        dias = tk.simpledialog.askinteger(
            "Limpar Logs Antigos",
            "Excluir logs mais antigos que quantos dias?",
            initialvalue=30,
            minvalue=1,
            maxvalue=365
        )
        
        if dias:
            removidos = self.log_manager.limpar_logs_antigos(dias)
            messagebox.showinfo("Concluído", f"Removidos {removidos} logs antigos.\nBackups criados automaticamente.")
            self.atualizar_lista_logs()
    
    def exportar_logs(self):
        """Exporta logs para diretório"""
        destino = filedialog.askdirectory(title="Selecionar pasta para exportar logs")
        
        if destino:
            if self.log_manager.exportar_logs(destino):
                messagebox.showinfo("Sucesso", f"Logs exportados para:\n{destino}")
            else:
                messagebox.showerror("Erro", "Falha ao exportar logs")
    
    def abrir_pasta_logs(self):
        """Abre pasta de logs no explorador"""
        try:
            os.startfile(self.log_manager.log_dir)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir pasta:\n{e}")


def abrir_gerenciador_logs(parent=None):
    """Função para abrir o gerenciador de logs"""
    if not GUI_AVAILABLE:
        print("❌ Interface gráfica não disponível. Use LogManager diretamente.")
        return None
    
    try:
        viewer = LogViewerGUI(parent)
        if not parent:
            viewer.root.mainloop()
        return viewer
    except Exception as e:
        if parent and GUI_AVAILABLE:
            messagebox.showerror("Erro", f"Falha ao abrir gerenciador de logs:\n{e}")
        else:
            print(f"❌ Erro ao abrir gerenciador: {e}")
        return None


if __name__ == "__main__":
    # Executar como aplicativo independente
    abrir_gerenciador_logs()