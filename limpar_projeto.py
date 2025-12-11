#!/usr/bin/env python3
"""
Script de Limpeza Automática do Projeto
Remove arquivos temporários, cache e mantém o projeto organizado
"""

import os
import shutil
import glob
from pathlib import Path

def limpar_cache():
    """Remove todos os arquivos de cache Python"""
    print("🧹 Limpando cache Python...")
    
    # Remover __pycache__ recursivamente
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_path)
                print(f"  ✅ Removido: {cache_path}")
            except Exception as e:
                print(f"  ❌ Erro ao remover {cache_path}: {e}")
    
    # Remover arquivos .pyc
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"  ✅ Removido: {pyc_file}")
        except Exception as e:
            print(f"  ❌ Erro ao remover {pyc_file}: {e}")

def limpar_logs_antigos():
    """Remove logs antigos (mais de 7 dias)"""
    print("📋 Limpando logs antigos...")
    
    if os.path.exists('logs'):
        import time
        agora = time.time()
        sete_dias = 7 * 24 * 60 * 60  # 7 dias em segundos
        
        for arquivo in os.listdir('logs'):
            caminho = os.path.join('logs', arquivo)
            if os.path.isfile(caminho):
                idade = agora - os.path.getmtime(caminho)
                if idade > sete_dias:
                    try:
                        os.remove(caminho)
                        print(f"  ✅ Log antigo removido: {arquivo}")
                    except Exception as e:
                        print(f"  ❌ Erro ao remover {arquivo}: {e}")

def limpar_arquivos_temporarios():
    """Remove arquivos temporários"""
    print("🗑️ Limpando arquivos temporários...")
    
    # Padrões de arquivos temporários
    padroes = [
        '*.tmp',
        '*.bak',
        '*.temp',
        'temp_*',
        'status_maq_*.json',
        'comando_maq_*.json',
        'teste_*',
        'debug_*'
    ]
    
    for padrao in padroes:
        arquivos = glob.glob(padrao)
        for arquivo in arquivos:
            try:
                os.remove(arquivo)
                print(f"  ✅ Removido: {arquivo}")
            except Exception as e:
                print(f"  ❌ Erro ao remover {arquivo}: {e}")

def limpar_builds():
    """Remove diretórios de build"""
    print("🔨 Limpando builds...")
    
    diretorios = ['build', 'dist']
    
    for diretorio in diretorios:
        if os.path.exists(diretorio):
            try:
                shutil.rmtree(diretorio)
                print(f"  ✅ Removido: {diretorio}/")
            except Exception as e:
                print(f"  ❌ Erro ao remover {diretorio}: {e}")

def verificar_estrutura():
    """Verifica se a estrutura do projeto está correta"""
    print("🔍 Verificando estrutura do projeto...")
    
    diretorios_essenciais = [
        'config',
        'data', 
        'gui',
        'models',
        'utils',
        'docs'
    ]
    
    arquivos_essenciais = [
        'main.py',
        'README.md',
        'requirements.txt',
        '.gitignore'
    ]
    
    # Verificar diretórios
    for diretorio in diretorios_essenciais:
        if os.path.exists(diretorio):
            print(f"  ✅ Diretório: {diretorio}/")
        else:
            print(f"  ❌ FALTANDO: {diretorio}/")
    
    # Verificar arquivos
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"  ✅ Arquivo: {arquivo}")
        else:
            print(f"  ❌ FALTANDO: {arquivo}")

def mostrar_estatisticas():
    """Mostra estatísticas do projeto"""
    print("📊 Estatísticas do projeto...")
    
    # Contar arquivos Python
    py_files = glob.glob('**/*.py', recursive=True)
    print(f"  📄 Arquivos Python: {len(py_files)}")
    
    # Contar linhas de código
    total_linhas = 0
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                linhas = len(f.readlines())
                total_linhas += linhas
        except:
            pass
    
    print(f"  📝 Total de linhas: {total_linhas}")
    
    # Tamanho do projeto
    tamanho_total = 0
    for root, dirs, files in os.walk('.'):
        # Ignorar .git
        if '.git' in root:
            continue
        for file in files:
            try:
                tamanho_total += os.path.getsize(os.path.join(root, file))
            except:
                pass
    
    tamanho_mb = tamanho_total / (1024 * 1024)
    print(f"  💾 Tamanho total: {tamanho_mb:.1f} MB")

def main():
    """Função principal"""
    print("🧹 LIMPEZA AUTOMÁTICA DO PROJETO")
    print("="*50)
    
    # Executar limpezas
    limpar_cache()
    limpar_logs_antigos()
    limpar_arquivos_temporarios()
    limpar_builds()
    
    print("\n" + "="*50)
    
    # Verificações
    verificar_estrutura()
    mostrar_estatisticas()
    
    print("\n" + "="*50)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("="*50)
    
    print("\n📋 PROJETO LIMPO E ORGANIZADO:")
    print("✅ Cache removido")
    print("✅ Logs antigos limpos")
    print("✅ Arquivos temporários removidos")
    print("✅ Builds limpos")
    print("✅ Estrutura verificada")
    
    print("\n🚀 PROJETO PRONTO PARA:")
    print("• Desenvolvimento")
    print("• Compilação")
    print("• Commit no Git")
    print("• Deploy em produção")

if __name__ == "__main__":
    main()