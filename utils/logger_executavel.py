"""
Sistema de Logs para Executável
Permite ver prints e logs mesmo em interface gráfica
"""

import os
import sys
import datetime
import threading
from pathlib import Path

class LoggerExecutavel:
    """Logger que funciona tanto em desenvolvimento quanto em executável"""
    
    def __init__(self):
        self.log_file = None
        self.console_backup = None
        self.setup_log_file()
        self.setup_console_redirect()
        
    def setup_log_file(self):
        """Configura arquivo de log"""
        try:
            # Determinar diretório base
            if getattr(sys, 'frozen', False):
                # Executável
                base_dir = os.path.dirname(sys.executable)
            else:
                # Desenvolvimento
                base_dir = os.path.dirname(os.path.dirname(__file__))
            
            # Criar pasta de logs
            log_dir = os.path.join(base_dir, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # Nome do arquivo com timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"coletor_log_{timestamp}.txt"
            self.log_file = os.path.join(log_dir, log_filename)
            
            # Log inicial
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== LOG DO COLETOR DE PRODUÇÃO ===\n")
                f.write(f"Iniciado em: {datetime.datetime.now()}\n")
                f.write(f"Modo: {'EXECUTÁVEL' if getattr(sys, 'frozen', False) else 'DESENVOLVIMENTO'}\n")
                f.write(f"Arquivo de log: {self.log_file}\n")
                f.write("="*50 + "\n\n")
                
        except Exception as e:
            print(f"Erro ao configurar log: {e}")
    
    def setup_console_redirect(self):
        """Redireciona prints para arquivo de log"""
        if getattr(sys, 'frozen', False):
            # Apenas em executável
            try:
                self.console_backup = sys.stdout
                sys.stdout = self
                sys.stderr = self
            except:
                pass
    
    def write(self, text):
        """Escreve no log e no console original"""
        try:
            # Escrever no arquivo de log
            if self.log_file and text.strip():
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] {text}")
                    f.flush()
            
            # Escrever no console original se disponível
            if self.console_backup:
                self.console_backup.write(text)
                self.console_backup.flush()
                
        except:
            pass
    
    def flush(self):
        """Flush necessário para compatibilidade"""
        try:
            if self.console_backup:
                self.console_backup.flush()
        except:
            pass
    
    def log(self, message, level="INFO"):
        """Log com nível"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        self.write(log_line)
    
    def get_log_file_path(self):
        """Retorna caminho do arquivo de log"""
        return self.log_file
    
    def get_recent_logs(self, lines=50):
        """Retorna últimas linhas do log"""
        try:
            if self.log_file and os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    return ''.join(all_lines[-lines:])
            return "Nenhum log disponível"
        except Exception as e:
            return f"Erro ao ler logs: {e}"

# Instância global
logger_executavel = LoggerExecutavel()

def inicializar_logger():
    """Inicializa o sistema de logs"""
    return logger_executavel

def log_info(message):
    """Log de informação"""
    logger_executavel.log(message, "INFO")

def log_error(message):
    """Log de erro"""
    logger_executavel.log(message, "ERROR")

def log_warning(message):
    """Log de aviso"""
    logger_executavel.log(message, "WARNING")

def get_log_path():
    """Retorna caminho do arquivo de log"""
    return logger_executavel.get_log_file_path()

def get_recent_logs(lines=50):
    """Retorna logs recentes"""
    return logger_executavel.get_recent_logs(lines)