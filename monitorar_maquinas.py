"""
Monitor de Máquinas - Verifica status de todas as máquinas na rede
Mostra quais estão online, offline e permite enviar comandos
"""

import os
import json
import time
import datetime
from config.settings import CAMINHO_REDE, CAMINHO_LOCAL

def listar_maquinas_ativas():
    """Lista todas as máquinas que estão enviando status"""
    maquinas = {}
    
    # Verificar arquivos de status na rede
    try:
        if os.path.exists(CAMINHO_REDE):
            for arquivo in os.listdir(CAMINHO_REDE):
                if arquivo.startswith('status_maq_') and arquivo.endswith('.json'):
                    maquina = arquivo.replace('status_maq_', '').replace('.json', '')
                    
                    try:
                        with open(os.path.join(CAMINHO_REDE, arquivo), 'r', encoding='utf-8') as f:
                            status = json.load(f)
                        
                        # Verificar se status é recente (últimos 30 segundos)
                        timestamp = datetime.datetime.fromisoformat(status['timestamp'])
                        agora = datetime.datetime.now()
                        diferenca = (agora - timestamp).total_seconds()
                        
                        maquinas[maquina] = {
                            'status': 'ONLINE' if diferenca < 30 else 'OFFLINE',
                            'ultimo_status': timestamp.strftime('%H:%M:%S'),
                            'diferenca_segundos': int(diferenca),
                            'dados': status
                        }
                        
                    except Exception as e:
                        maquinas[maquina] = {
                            'status': 'ERRO',
                            'erro': str(e)
                        }
    except Exception as e:
        print(f"❌ Erro ao acessar rede: {e}")
    
    # Verificar arquivos locais também
    try:
        if os.path.exists(CAMINHO_LOCAL):
            for arquivo in os.listdir(CAMINHO_LOCAL):
                if arquivo.startswith('status_maq_') and arquivo.endswith('.json'):
                    maquina = arquivo.replace('status_maq_', '').replace('.json', '')
                    
                    # Só adicionar se não estiver na rede
                    if maquina not in maquinas:
                        try:
                            with open(os.path.join(CAMINHO_LOCAL, arquivo), 'r', encoding='utf-8') as f:
                                status = json.load(f)
                            
                            timestamp = datetime.datetime.fromisoformat(status['timestamp'])
                            agora = datetime.datetime.now()
                            diferenca = (agora - timestamp).total_seconds()
                            
                            maquinas[maquina] = {
                                'status': 'LOCAL' if diferenca < 30 else 'OFFLINE',
                                'ultimo_status': timestamp.strftime('%H:%M:%S'),
                                'diferenca_segundos': int(diferenca),
                                'dados': status,
                                'origem': 'LOCAL'
                            }
                            
                        except Exception as e:
                            maquinas[maquina] = {
                                'status': 'ERRO',
                                'erro': str(e),
                                'origem': 'LOCAL'
                            }
    except Exception as e:
        print(f"❌ Erro ao acessar local: {e}")
    
    return maquinas

def mostrar_status_maquinas():
    """Mostra status detalhado de todas as máquinas"""
    print("="*80)
    print("📊 MONITOR DE MÁQUINAS - STATUS EM TEMPO REAL")
    print("="*80)
    print(f"🕐 Atualizado em: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print()
    
    maquinas = listar_maquinas_ativas()
    
    if not maquinas:
        print("❌ Nenhuma máquina encontrada!")
        return
    
    # Separar por status
    online = []
    offline = []
    erro = []
    
    for maquina, info in maquinas.items():
        if info['status'] == 'ONLINE':
            online.append((maquina, info))
        elif info['status'] == 'LOCAL':
            online.append((maquina, info))
        elif info['status'] == 'OFFLINE':
            offline.append((maquina, info))
        else:
            erro.append((maquina, info))
    
    # Mostrar máquinas ONLINE
    if online:
        print(f"🟢 MÁQUINAS ONLINE ({len(online)}):")
        print("-" * 60)
        for maquina, info in sorted(online):
            dados = info.get('dados', {})
            origem = info.get('origem', 'REDE')
            
            print(f"  🏭 {maquina:<15} | ⏰ {info['ultimo_status']} | 📍 {origem}")
            
            if 'dados' in info:
                size = dados.get('size', 'N/A')
                lote = dados.get('lote', 'N/A')
                cpu = dados.get('recursos', {}).get('cpu', 0)
                memoria = dados.get('recursos', {}).get('memoria', 0)
                
                print(f"      📏 Size: {size:<8} | 📦 Lote: {lote:<15}")
                print(f"      💻 CPU: {cpu:>5.1f}% | 🧠 RAM: {memoria:>5.1f}%")
                print()
    
    # Mostrar máquinas OFFLINE
    if offline:
        print(f"🔴 MÁQUINAS OFFLINE ({len(offline)}):")
        print("-" * 60)
        for maquina, info in sorted(offline):
            print(f"  🏭 {maquina:<15} | ⏰ {info['ultimo_status']} | ⏳ {info['diferenca_segundos']}s atrás")
        print()
    
    # Mostrar máquinas com ERRO
    if erro:
        print(f"❌ MÁQUINAS COM ERRO ({len(erro)}):")
        print("-" * 60)
        for maquina, info in sorted(erro):
            print(f"  🏭 {maquina:<15} | ❌ {info.get('erro', 'Erro desconhecido')}")
        print()
    
    # Resumo
    total = len(maquinas)
    print("="*80)
    print(f"📊 RESUMO: {total} máquinas | 🟢 {len(online)} online | 🔴 {len(offline)} offline | ❌ {len(erro)} erro")
    print("="*80)

def monitorar_continuo():
    """Monitora continuamente as máquinas"""
    print("🚀 INICIANDO MONITORAMENTO CONTÍNUO")
    print("   Pressione Ctrl+C para parar")
    print()
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpar tela
            mostrar_status_maquinas()
            
            print("⏳ Próxima atualização em 5 segundos...")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoramento interrompido pelo usuário")

def enviar_comando_broadcast(acao, parametros=None):
    """Envia comando para TODAS as máquinas online"""
    print(f"📡 ENVIANDO COMANDO BROADCAST: {acao}")
    
    maquinas = listar_maquinas_ativas()
    online = [m for m, info in maquinas.items() if info['status'] in ['ONLINE', 'LOCAL']]
    
    if not online:
        print("❌ Nenhuma máquina online encontrada!")
        return
    
    print(f"🎯 Enviando para {len(online)} máquinas: {', '.join(online)}")
    
    from testar_comando_remoto import enviar_comando
    
    sucessos = 0
    for maquina in online:
        try:
            if enviar_comando(maquina, acao, parametros):
                sucessos += 1
                print(f"  ✅ {maquina}")
            else:
                print(f"  ❌ {maquina}")
        except Exception as e:
            print(f"  ❌ {maquina}: {e}")
    
    print(f"\n📊 Resultado: {sucessos}/{len(online)} comandos enviados com sucesso")

if __name__ == "__main__":
    print("="*80)
    print("📊 MONITOR DE MÁQUINAS")
    print("="*80)
    print()
    print("Opções:")
    print("  1. Ver status atual")
    print("  2. Monitoramento contínuo")
    print("  3. Enviar comando broadcast")
    print("  4. Sair")
    print()
    
    while True:
        opcao = input("Digite sua opção (1-4): ").strip()
        
        if opcao == "1":
            mostrar_status_maquinas()
            input("\nPressione Enter para continuar...")
            
        elif opcao == "2":
            monitorar_continuo()
            
        elif opcao == "3":
            print("\nComandos disponíveis para broadcast:")
            print("  1. coletar_dados")
            print("  2. fazer_backup") 
            print("  3. diagnostico_completo")
            print("  4. testar_conectividade")
            print("  5. obter_logs")
            print("  6. limpar_cache")
            
            cmd = input("Digite o comando: ").strip()
            
            cmd_map = {
                "1": "coletar_dados",
                "2": "fazer_backup",
                "3": "diagnostico_completo", 
                "4": "testar_conectividade",
                "5": "obter_logs",
                "6": "limpar_cache"
            }
            
            if cmd in cmd_map:
                cmd = cmd_map[cmd]
            
            enviar_comando_broadcast(cmd)
            input("\nPressione Enter para continuar...")
            
        elif opcao == "4":
            print("👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida!")