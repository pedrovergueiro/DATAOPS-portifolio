"""Script de Teste do Sistema de Comunicação"""

import os
import time
import json
from config.settings import CAMINHO_LOCAL, CAMINHO_REDE

print("="*60)
print("🔍 TESTE DO SISTEMA DE COMUNICAÇÃO")
print("="*60)

# Teste 1: Verificar diretórios
print("\n📁 Teste 1: Verificando diretórios...")
print(f"   Local: {CAMINHO_LOCAL}")
print(f"   Existe: {'✅ SIM' if os.path.exists(CAMINHO_LOCAL) else '❌ NÃO'}")
print(f"   Rede: {CAMINHO_REDE}")
print(f"   Existe: {'✅ SIM' if os.path.exists(CAMINHO_REDE) else '❌ NÃO'}")

# Teste 2: Verificar arquivos de status
print("\n📊 Teste 2: Verificando arquivos de status...")
arquivos_status_local = [f for f in os.listdir(CAMINHO_LOCAL) if f.startswith('status_maq_') and f.endswith('.json')]
print(f"   Arquivos locais: {len(arquivos_status_local)}")
for arquivo in arquivos_status_local:
    print(f"      - {arquivo}")

if os.path.exists(CAMINHO_REDE):
    arquivos_status_rede = [f for f in os.listdir(CAMINHO_REDE) if f.startswith('status_maq_') and f.endswith('.json')]
    print(f"   Arquivos na rede: {len(arquivos_status_rede)}")
    for arquivo in arquivos_status_rede:
        print(f"      - {arquivo}")
else:
    print("   ⚠️ Rede não acessível")

# Teste 3: Verificar conteúdo dos arquivos
print("\n📄 Teste 3: Verificando conteúdo dos arquivos...")
if arquivos_status_local:
    for arquivo in arquivos_status_local:
        caminho = os.path.join(CAMINHO_LOCAL, arquivo)
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            print(f"\n   Arquivo: {arquivo}")
            print(f"      Máquina: {status.get('maquina', 'N/A')}")
            print(f"      Status: {status.get('status', 'N/A')}")
            print(f"      Timestamp: {status.get('timestamp', 'N/A')}")
            print(f"      Online: {status.get('online', False)}")
            print(f"      Hostname: {status.get('hostname', 'N/A')}")
            print(f"      IP: {status.get('ip', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Erro ao ler {arquivo}: {e}")
else:
    print("   ⚠️ Nenhum arquivo de status encontrado")
    print("   💡 Dica: Execute main.py e aguarde alguns segundos")

# Teste 4: Verificar arquivo de auditoria
print("\n📋 Teste 4: Verificando arquivo de auditoria...")
auditoria_path = os.path.join(CAMINHO_LOCAL, "auditoria_producao.json")
if os.path.exists(auditoria_path):
    print(f"   ✅ Arquivo existe: {auditoria_path}")
    try:
        with open(auditoria_path, 'r', encoding='utf-8') as f:
            auditoria = json.load(f)
        print(f"   Total de registros: {auditoria.get('total_registros', 0)}")
        print(f"   Último registro: {auditoria.get('ultimo_registro', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erro ao ler auditoria: {e}")
else:
    print(f"   ⚠️ Arquivo não existe: {auditoria_path}")

# Teste 5: Verificar configurações
print("\n⚙️ Teste 5: Verificando configurações...")
config_maquina = os.path.join(CAMINHO_LOCAL, "config_maquina.json")
config_size = os.path.join(CAMINHO_LOCAL, "config_size.json")
config_lote = os.path.join(CAMINHO_LOCAL, "config_lote.json")

for config_file in [config_maquina, config_size, config_lote]:
    if os.path.exists(config_file):
        print(f"   ✅ {os.path.basename(config_file)}")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"      {json.dumps(config, indent=6, ensure_ascii=False)}")
        except Exception as e:
            print(f"      ❌ Erro ao ler: {e}")
    else:
        print(f"   ⚠️ {os.path.basename(config_file)} não existe")

# Teste 6: Simular criação de arquivo de status
print("\n🧪 Teste 6: Simulando criação de arquivo de status...")
try:
    import datetime
    import socket
    
    teste_status = {
        'maquina': 'TESTE',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'online',
        'online': True,
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname())
    }
    
    teste_path = os.path.join(CAMINHO_LOCAL, "status_maq_TESTE.json")
    with open(teste_path, 'w', encoding='utf-8') as f:
        json.dump(teste_status, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Arquivo de teste criado: {teste_path}")
    print(f"   Conteúdo:")
    print(f"      {json.dumps(teste_status, indent=6, ensure_ascii=False)}")
    
    # Remover arquivo de teste
    time.sleep(1)
    os.remove(teste_path)
    print(f"   🗑️ Arquivo de teste removido")
    
except Exception as e:
    print(f"   ❌ Erro ao criar arquivo de teste: {e}")

# Resumo
print("\n" + "="*60)
print("📊 RESUMO DO TESTE")
print("="*60)

problemas = []

if not os.path.exists(CAMINHO_LOCAL):
    problemas.append("❌ Diretório local não existe")

if not arquivos_status_local:
    problemas.append("⚠️ Nenhum arquivo de status encontrado (execute main.py)")

if not os.path.exists(auditoria_path):
    problemas.append("⚠️ Arquivo de auditoria não existe")

if not os.path.exists(config_maquina):
    problemas.append("⚠️ Configuração de máquina não existe")

if problemas:
    print("\n🔴 PROBLEMAS ENCONTRADOS:")
    for problema in problemas:
        print(f"   {problema}")
    print("\n💡 SOLUÇÃO:")
    print("   1. Execute: python main.py")
    print("   2. Aguarde 5-10 segundos")
    print("   3. Execute este teste novamente")
else:
    print("\n✅ TODOS OS TESTES PASSARAM!")
    print("   Sistema está funcionando corretamente")

print("\n" + "="*60)
print("🏁 FIM DO TESTE")
print("="*60)
