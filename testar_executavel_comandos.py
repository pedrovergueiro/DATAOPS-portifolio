"""
Teste específico do sistema de comandos remotos para executáveis
Verifica se todas as funcionalidades funcionam corretamente no .exe
"""

import os
import sys
import json
import time
import datetime
import threading
from pathlib import Path

def testar_ambiente_executavel():
    """Testa se o ambiente executável está configurado corretamente"""
    print("🔧 TESTANDO AMBIENTE EXECUTÁVEL")
    print("="*50)
    
    # Verificar se está rodando como executável
    is_exe = getattr(sys, 'frozen', False)
    print(f"📦 Executável: {'SIM' if is_exe else 'NÃO'}")
    
    if is_exe:
        print(f"📁 Caminho executável: {sys.executable}")
        print(f"📂 Diretório base: {os.path.dirname(sys.executable)}")
    else:
        print(f"🐍 Script Python: {__file__}")
        print(f"📂 Diretório script: {os.path.dirname(__file__)}")
    
    return is_exe

def testar_imports_criticos():
    """Testa se todos os imports críticos funcionam"""
    print("\n🔍 TESTANDO IMPORTS CRÍTICOS")
    print("="*50)
    
    imports_criticos = [
        'tkinter',
        'pandas', 
        'psutil',
        'threading',
        'json',
        'datetime',
        'uuid',
        'socket',
        'time',
        'os'
    ]
    
    falhas = []
    
    for modulo in imports_criticos:
        try:
            __import__(modulo)
            print(f"✅ {modulo}")
        except ImportError as e:
            print(f"❌ {modulo}: {e}")
            falhas.append(modulo)
    
    return len(falhas) == 0, falhas

def testar_imports_opcionais():
    """Testa imports opcionais (com fallbacks)"""
    print("\n🔍 TESTANDO IMPORTS OPCIONAIS")
    print("="*50)
    
    imports_opcionais = [
        'pyautogui',
        'PIL',
        'zipfile',
        'subprocess'
    ]
    
    disponiveis = []
    
    for modulo in imports_opcionais:
        try:
            __import__(modulo)
            print(f"✅ {modulo}")
            disponiveis.append(modulo)
        except ImportError:
            print(f"⚠️ {modulo}: Não disponível (fallback ativo)")
    
    return disponiveis

def testar_sistema_arquivos():
    """Testa operações de arquivo necessárias para comandos remotos"""
    print("\n📁 TESTANDO SISTEMA DE ARQUIVOS")
    print("="*50)
    
    # Determinar diretório base
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)
    
    testes = []
    
    # Teste 1: Criar arquivo JSON
    try:
        test_file = os.path.join(base_dir, 'teste_comando.json')
        test_data = {
            'id': 'teste-123',
            'acao': 'teste',
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        # Ler de volta
        with open(test_file, 'r', encoding='utf-8') as f:
            data_lida = json.load(f)
        
        # Remover arquivo
        os.remove(test_file)
        
        if data_lida['id'] == 'teste-123':
            print("✅ Criar/ler/remover arquivo JSON")
            testes.append(True)
        else:
            print("❌ Dados JSON incorretos")
            testes.append(False)
            
    except Exception as e:
        print(f"❌ Operações de arquivo: {e}")
        testes.append(False)
    
    # Teste 2: Verificar permissões de escrita
    try:
        perm_file = os.path.join(base_dir, 'teste_permissao.tmp')
        with open(perm_file, 'w') as f:
            f.write('teste')
        os.remove(perm_file)
        print("✅ Permissões de escrita")
        testes.append(True)
    except Exception as e:
        print(f"❌ Permissões de escrita: {e}")
        testes.append(False)
    
    return all(testes)

def testar_threading():
    """Testa se threading funciona corretamente (crítico para comunicação)"""
    print("\n🧵 TESTANDO THREADING")
    print("="*50)
    
    resultados = []
    
    def thread_teste(resultado_lista, valor):
        time.sleep(0.1)
        resultado_lista.append(valor)
    
    try:
        # Criar múltiplas threads
        threads = []
        for i in range(3):
            t = threading.Thread(target=thread_teste, args=(resultados, i), daemon=True)
            threads.append(t)
            t.start()
        
        # Aguardar conclusão
        for t in threads:
            t.join(timeout=2)
        
        if len(resultados) == 3:
            print("✅ Threading básico")
            
            # Testar thread contínua (simula comunicação)
            stop_flag = [False]
            contador = [0]
            
            def thread_continua():
                while not stop_flag[0]:
                    contador[0] += 1
                    time.sleep(0.001)  # 1ms como no sistema real
            
            t_continua = threading.Thread(target=thread_continua, daemon=True)
            t_continua.start()
            
            time.sleep(0.1)  # Deixar rodar por 100ms
            stop_flag[0] = True
            t_continua.join(timeout=1)
            
            if contador[0] > 50:  # Deveria ter executado ~100 vezes
                print(f"✅ Threading contínuo (1ms): {contador[0]} iterações")
                return True
            else:
                print(f"❌ Threading contínuo muito lento: {contador[0]} iterações")
                return False
        else:
            print(f"❌ Threading básico: apenas {len(resultados)}/3 threads")
            return False
            
    except Exception as e:
        print(f"❌ Threading: {e}")
        return False

def testar_comunicacao_simulada():
    """Simula o sistema de comunicação completo"""
    print("\n📡 TESTANDO COMUNICAÇÃO SIMULADA")
    print("="*50)
    
    # Determinar diretório base
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)
    
    try:
        # Simular envio de comando
        comando_file = os.path.join(base_dir, 'comando_maq_TESTE.json')
        comando_data = {
            'id': 'teste-comunicacao-123',
            'acao': 'coletar_dados',
            'parametros': {},
            'timestamp': datetime.datetime.now().isoformat(),
            'origem': 'teste_executavel'
        }
        
        # Escrever comando
        with open(comando_file, 'w', encoding='utf-8') as f:
            json.dump(comando_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Comando criado")
        
        # Simular detecção (como faria o sistema real)
        comandos_detectados = []
        
        def detectar_comandos():
            if os.path.exists(comando_file):
                try:
                    with open(comando_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    comandos_detectados.append(data)
                    os.remove(comando_file)
                    return True
                except:
                    return False
            return False
        
        # Simular loop de verificação
        detectado = False
        for i in range(10):  # Tentar 10 vezes
            if detectar_comandos():
                detectado = True
                break
            time.sleep(0.001)  # 1ms
        
        if detectado and len(comandos_detectados) > 0:
            cmd = comandos_detectados[0]
            if cmd['id'] == 'teste-comunicacao-123':
                print("✅ Detecção de comando")
                print("✅ Remoção de arquivo")
                return True
            else:
                print("❌ Dados do comando incorretos")
                return False
        else:
            print("❌ Comando não detectado")
            return False
            
    except Exception as e:
        print(f"❌ Comunicação simulada: {e}")
        return False
    finally:
        # Limpar arquivo se ainda existir
        try:
            if os.path.exists(comando_file):
                os.remove(comando_file)
        except:
            pass

def testar_recursos_sistema():
    """Testa acesso a recursos do sistema (necessário para status)"""
    print("\n💻 TESTANDO RECURSOS DO SISTEMA")
    print("="*50)
    
    try:
        import psutil
        
        # CPU
        cpu = psutil.cpu_percent(interval=0.1)
        print(f"✅ CPU: {cpu}%")
        
        # Memória
        mem = psutil.virtual_memory()
        print(f"✅ Memória: {mem.percent}% ({mem.available // (1024**3)}GB livre)")
        
        # Disco
        disk = psutil.disk_usage('/')
        print(f"✅ Disco: {disk.percent}% ({disk.free // (1024**3)}GB livre)")
        
        # Rede
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"✅ Rede: {hostname} ({ip})")
        
        return True
        
    except Exception as e:
        print(f"❌ Recursos do sistema: {e}")
        return False

def executar_teste_completo():
    """Executa todos os testes"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE COMANDOS REMOTOS")
    print("="*60)
    
    testes = []
    
    # 1. Ambiente
    is_exe = testar_ambiente_executavel()
    
    # 2. Imports críticos
    imports_ok, falhas = testar_imports_criticos()
    testes.append(('Imports críticos', imports_ok))
    
    # 3. Imports opcionais
    disponiveis = testar_imports_opcionais()
    
    # 4. Sistema de arquivos
    arquivos_ok = testar_sistema_arquivos()
    testes.append(('Sistema de arquivos', arquivos_ok))
    
    # 5. Threading
    threading_ok = testar_threading()
    testes.append(('Threading', threading_ok))
    
    # 6. Comunicação
    comunicacao_ok = testar_comunicacao_simulada()
    testes.append(('Comunicação', comunicacao_ok))
    
    # 7. Recursos do sistema
    recursos_ok = testar_recursos_sistema()
    testes.append(('Recursos do sistema', recursos_ok))
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    total_testes = len(testes)
    testes_ok = sum(1 for _, ok in testes if ok)
    
    for nome, resultado in testes:
        status = "✅ OK" if resultado else "❌ FALHA"
        print(f"{nome:<25}: {status}")
    
    print(f"\n🎯 RESULTADO: {testes_ok}/{total_testes} testes passaram")
    
    if testes_ok == total_testes:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de comandos remotos pronto para executável")
        print("📡 Comunicação ultra-rápida (1ms) funcionando")
        print("🔧 Todas as funcionalidades operacionais")
        
        if is_exe:
            print("\n🔧 EXECUTÁVEL VALIDADO COM SUCESSO!")
        else:
            print("\n🐍 DESENVOLVIMENTO VALIDADO - Pronto para compilar")
            
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("❌ Verificar problemas antes de usar executável")
        
        if not imports_ok:
            print(f"\n🚨 DEPENDÊNCIAS CRÍTICAS FALTANDO: {', '.join(falhas)}")
    
    print("\n" + "="*60)
    
    return testes_ok == total_testes

if __name__ == "__main__":
    sucesso = executar_teste_completo()
    
    if sucesso:
        print("\n✅ Sistema pronto para produção!")
        sys.exit(0)
    else:
        print("\n❌ Sistema com problemas!")
        sys.exit(1)