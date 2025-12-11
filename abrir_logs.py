"""
Script para abrir logs do Coletor de Produção
Pode ser usado independentemente do aplicativo principal
"""

import os
import sys
import glob
import subprocess
from pathlib import Path

def encontrar_logs():
    """Encontra arquivos de log do sistema"""
    
    # Determinar diretório base
    if getattr(sys, 'frozen', False):
        # Executável
        base_dir = os.path.dirname(sys.executable)
    else:
        # Desenvolvimento
        base_dir = os.path.dirname(__file__)
    
    # Procurar pasta de logs
    log_dir = os.path.join(base_dir, 'logs')
    
    if not os.path.exists(log_dir):
        return []
    
    # Procurar arquivos de log
    pattern = os.path.join(log_dir, 'coletor_log_*.txt')
    arquivos = glob.glob(pattern)
    
    # Ordenar por data de modificação (mais recente primeiro)
    arquivos.sort(key=os.path.getmtime, reverse=True)
    
    return arquivos

def mostrar_logs_console():
    """Mostra logs no console"""
    arquivos = encontrar_logs()
    
    if not arquivos:
        print("❌ Nenhum arquivo de log encontrado")
        return
    
    print("📋 LOGS DO COLETOR DE PRODUÇÃO")
    print("="*60)
    
    # Mostrar log mais recente
    log_mais_recente = arquivos[0]
    print(f"📁 Arquivo: {os.path.basename(log_mais_recente)}")
    print(f"📅 Modificado: {os.path.getmtime(log_mais_recente)}")
    print("="*60)
    
    try:
        with open(log_mais_recente, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            print(conteudo)
    except Exception as e:
        print(f"❌ Erro ao ler log: {e}")

def abrir_log_no_notepad():
    """Abre log mais recente no Notepad"""
    arquivos = encontrar_logs()
    
    if not arquivos:
        print("❌ Nenhum arquivo de log encontrado")
        return False
    
    log_mais_recente = arquivos[0]
    
    try:
        # Tentar abrir no Notepad
        subprocess.run(['notepad.exe', log_mais_recente])
        print(f"✅ Log aberto no Notepad: {os.path.basename(log_mais_recente)}")
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir no Notepad: {e}")
        return False

def abrir_pasta_logs():
    """Abre pasta de logs no explorador"""
    # Determinar diretório base
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)
    
    log_dir = os.path.join(base_dir, 'logs')
    
    if os.path.exists(log_dir):
        try:
            os.startfile(log_dir)  # Windows
            print(f"✅ Pasta de logs aberta: {log_dir}")
            return True
        except Exception as e:
            print(f"❌ Erro ao abrir pasta: {e}")
            return False
    else:
        print(f"❌ Pasta de logs não encontrada: {log_dir}")
        return False

def listar_todos_logs():
    """Lista todos os arquivos de log disponíveis"""
    arquivos = encontrar_logs()
    
    if not arquivos:
        print("❌ Nenhum arquivo de log encontrado")
        return
    
    print("📋 ARQUIVOS DE LOG DISPONÍVEIS")
    print("="*60)
    
    for i, arquivo in enumerate(arquivos, 1):
        nome = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo) / 1024  # KB
        modificado = os.path.getmtime(arquivo)
        
        import datetime
        data_mod = datetime.datetime.fromtimestamp(modificado).strftime("%d/%m/%Y %H:%M:%S")
        
        print(f"{i:2d}. {nome}")
        print(f"    📅 {data_mod} | 📊 {tamanho:.1f} KB")
        print()

def menu_interativo():
    """Menu interativo para gerenciar logs"""
    while True:
        print("\n" + "="*60)
        print("📋 GERENCIADOR DE LOGS - COLETOR DE PRODUÇÃO")
        print("="*60)
        print("1. 👀 Mostrar log mais recente no console")
        print("2. 📝 Abrir log mais recente no Notepad")
        print("3. 📁 Abrir pasta de logs no explorador")
        print("4. 📋 Listar todos os logs disponíveis")
        print("5. 🔄 Atualizar lista")
        print("0. ❌ Sair")
        print("="*60)
        
        try:
            opcao = input("Digite sua opção (0-5): ").strip()
            
            if opcao == "0":
                print("👋 Saindo...")
                break
            elif opcao == "1":
                mostrar_logs_console()
            elif opcao == "2":
                abrir_log_no_notepad()
            elif opcao == "3":
                abrir_pasta_logs()
            elif opcao == "4":
                listar_todos_logs()
            elif opcao == "5":
                print("🔄 Lista atualizada")
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("📋 VISUALIZADOR DE LOGS - COLETOR DE PRODUÇÃO")
    print("="*60)
    
    # Verificar se há argumentos de linha de comando
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "console":
            mostrar_logs_console()
        elif comando == "notepad":
            abrir_log_no_notepad()
        elif comando == "pasta":
            abrir_pasta_logs()
        elif comando == "listar":
            listar_todos_logs()
        else:
            print(f"❌ Comando desconhecido: {comando}")
            print("Comandos disponíveis: console, notepad, pasta, listar")
    else:
        # Menu interativo
        menu_interativo()

if __name__ == "__main__":
    main()