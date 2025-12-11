"""
Configurações específicas para executáveis (.exe)
Garante compatibilidade e funcionalidade completa
"""

import os
import sys
import json
from pathlib import Path

def detectar_ambiente():
    """Detecta se está rodando como executável ou script"""
    return {
        'is_executable': getattr(sys, 'frozen', False),
        'executable_path': sys.executable if getattr(sys, 'frozen', False) else None,
        'script_path': __file__ if not getattr(sys, 'frozen', False) else None,
        'base_dir': os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    }

def configurar_paths_executavel():
    """Configura paths para funcionamento em executável"""
    env = detectar_ambiente()
    
    if env['is_executable']:
        print("🔧 CONFIGURANDO PARA EXECUTÁVEL (.exe)")
        
        # Diretório base do executável
        base_dir = env['base_dir']
        
        # Paths relativos ao executável
        paths = {
            'base': base_dir,
            'config': os.path.join(base_dir, 'config'),
            'data': os.path.join(base_dir, 'data'),
            'logs': os.path.join(base_dir, 'logs'),
            'temp': os.path.join(base_dir, 'temp'),
            'backup': os.path.join(base_dir, 'backup')
        }
        
        # Criar diretórios se não existirem
        for nome, path in paths.items():
            try:
                os.makedirs(path, exist_ok=True)
                print(f"✅ Diretório {nome}: {path}")
            except Exception as e:
                print(f"⚠️ Erro criar diretório {nome}: {e}")
        
        return paths
    else:
        print("🐍 CONFIGURANDO PARA DESENVOLVIMENTO (.py)")
        return None

def verificar_dependencias_executavel():
    """Verifica se todas as dependências estão disponíveis no executável"""
    dependencias = {
        'criticas': [
            'tkinter',
            'pandas', 
            'psutil',
            'json',
            'threading',
            'datetime',
            'uuid',
            'socket'
        ],
        'opcionais': [
            'pyautogui',
            'PIL',
            'zipfile',
            'subprocess'
        ]
    }
    
    resultado = {
        'criticas_ok': True,
        'opcionais_disponiveis': [],
        'criticas_faltando': [],
        'opcionais_faltando': []
    }
    
    # Verificar dependências críticas
    for dep in dependencias['criticas']:
        try:
            __import__(dep)
            print(f"✅ {dep}: OK")
        except ImportError:
            print(f"❌ {dep}: FALTANDO")
            resultado['criticas_faltando'].append(dep)
            resultado['criticas_ok'] = False
    
    # Verificar dependências opcionais
    for dep in dependencias['opcionais']:
        try:
            __import__(dep)
            print(f"✅ {dep}: OK (opcional)")
            resultado['opcionais_disponiveis'].append(dep)
        except ImportError:
            print(f"⚠️ {dep}: Não disponível (opcional)")
            resultado['opcionais_faltando'].append(dep)
    
    return resultado

def configurar_sistema_comunicacao_executavel():
    """Configura sistema de comunicação para executáveis"""
    env = detectar_ambiente()
    
    config = {
        'verificacao_intervalo_ms': 1,  # 1ms
        'status_intervalo_ms': 1000,    # 1 segundo
        'timeout_comando': 60,          # 60 segundos
        'max_comandos_historico': 100,
        'auto_restart': True,
        'fallback_local': True,
        'log_detalhado': env['is_executable']  # Mais logs em executável
    }
    
    if env['is_executable']:
        print("🔧 Configuração otimizada para EXECUTÁVEL:")
        print(f"   ⚡ Verificação: {config['verificacao_intervalo_ms']}ms")
        print(f"   📊 Status: {config['status_intervalo_ms']}ms") 
        print(f"   🔄 Auto-restart: {config['auto_restart']}")
        print(f"   📁 Fallback local: {config['fallback_local']}")
    
    return config

def criar_arquivo_info_executavel():
    """Cria arquivo com informações do executável"""
    env = detectar_ambiente()
    
    if env['is_executable']:
        info = {
            'tipo': 'executavel',
            'versao': '1.0',
            'timestamp_criacao': str(datetime.datetime.now()),
            'executable_path': env['executable_path'],
            'base_dir': env['base_dir'],
            'sistema_comunicacao': {
                'ativo': True,
                'verificacao_ms': 1,
                'comandos_suportados': [
                    'fechar_app', 'abrir_app', 'reiniciar_app',
                    'alterar_size', 'alterar_lote', 'alterar_configuracao_maquina',
                    'coletar_dados', 'fazer_backup', 'coletar_informacoes_sistema',
                    'executar_comando_sistema', 'testar_conectividade', 'obter_logs',
                    'diagnostico_completo', 'limpar_cache', 'capturar_tela'
                ]
            },
            'dependencias': verificar_dependencias_executavel()
        }
        
        try:
            info_file = os.path.join(env['base_dir'], 'info_executavel.json')
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2, ensure_ascii=False)
            print(f"📄 Arquivo de informações criado: {info_file}")
        except Exception as e:
            print(f"⚠️ Erro criar arquivo info: {e}")
        
        return info
    
    return None

def testar_funcionalidades_executavel():
    """Testa todas as funcionalidades críticas no executável"""
    print("🧪 TESTANDO FUNCIONALIDADES DO EXECUTÁVEL")
    
    testes = {
        'paths': False,
        'comunicacao': False,
        'arquivos': False,
        'threads': False,
        'json': False,
        'rede': False
    }
    
    # Teste 1: Paths e diretórios
    try:
        env = detectar_ambiente()
        if env['base_dir'] and os.path.exists(env['base_dir']):
            testes['paths'] = True
            print("✅ Teste paths: OK")
        else:
            print("❌ Teste paths: FALHA")
    except Exception as e:
        print(f"❌ Teste paths: {e}")
    
    # Teste 2: Threading
    try:
        import threading
        import time
        
        def test_thread():
            time.sleep(0.1)
        
        t = threading.Thread(target=test_thread, daemon=True)
        t.start()
        t.join(timeout=1)
        testes['threads'] = True
        print("✅ Teste threading: OK")
    except Exception as e:
        print(f"❌ Teste threading: {e}")
    
    # Teste 3: JSON
    try:
        import json
        test_data = {'teste': 'ok', 'timestamp': str(datetime.datetime.now())}
        json_str = json.dumps(test_data)
        json.loads(json_str)
        testes['json'] = True
        print("✅ Teste JSON: OK")
    except Exception as e:
        print(f"❌ Teste JSON: {e}")
    
    # Teste 4: Arquivos
    try:
        env = detectar_ambiente()
        test_file = os.path.join(env['base_dir'], 'test_executavel.tmp')
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('teste executável')
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        os.remove(test_file)
        
        if content == 'teste executável':
            testes['arquivos'] = True
            print("✅ Teste arquivos: OK")
        else:
            print("❌ Teste arquivos: Conteúdo incorreto")
    except Exception as e:
        print(f"❌ Teste arquivos: {e}")
    
    # Teste 5: Rede (básico)
    try:
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if hostname and ip:
            testes['rede'] = True
            print(f"✅ Teste rede: OK ({hostname} - {ip})")
        else:
            print("❌ Teste rede: Sem hostname/IP")
    except Exception as e:
        print(f"❌ Teste rede: {e}")
    
    # Resumo
    total_testes = len(testes)
    testes_ok = sum(testes.values())
    
    print(f"\n📊 RESULTADO DOS TESTES: {testes_ok}/{total_testes} OK")
    
    if testes_ok == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM - Executável pronto!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM - Verificar problemas")
        for teste, resultado in testes.items():
            if not resultado:
                print(f"   ❌ {teste}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🔧 CONFIGURAÇÃO PARA EXECUTÁVEL")
    print("="*60)
    
    # Detectar ambiente
    env = detectar_ambiente()
    print(f"🎯 Ambiente: {'EXECUTÁVEL' if env['is_executable'] else 'DESENVOLVIMENTO'}")
    
    if env['is_executable']:
        print(f"📁 Diretório base: {env['base_dir']}")
        
        # Configurar paths
        configurar_paths_executavel()
        
        # Verificar dependências
        print("\n🔍 VERIFICANDO DEPENDÊNCIAS:")
        deps = verificar_dependencias_executavel()
        
        # Configurar comunicação
        print("\n📡 CONFIGURANDO COMUNICAÇÃO:")
        config_com = configurar_sistema_comunicacao_executavel()
        
        # Criar arquivo info
        print("\n📄 CRIANDO ARQUIVO DE INFORMAÇÕES:")
        criar_arquivo_info_executavel()
        
        # Testar funcionalidades
        print("\n🧪 TESTANDO FUNCIONALIDADES:")
        sucesso = testar_funcionalidades_executavel()
        
        print("\n" + "="*60)
        if sucesso and deps['criticas_ok']:
            print("🎉 EXECUTÁVEL CONFIGURADO COM SUCESSO!")
            print("✅ Todas as funcionalidades estão operacionais")
            print("📡 Sistema de comunicação pronto (1ms)")
        else:
            print("⚠️ CONFIGURAÇÃO COM PROBLEMAS")
            if not deps['criticas_ok']:
                print("❌ Dependências críticas faltando")
            if not sucesso:
                print("❌ Testes de funcionalidade falharam")
        print("="*60)
    else:
        print("🐍 Rodando em modo desenvolvimento - configuração não necessária")