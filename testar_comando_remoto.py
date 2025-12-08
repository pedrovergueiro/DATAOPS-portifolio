"""Script para testar comandos remotos - Envia comando para máquina específica"""

import json
import os
import uuid
import datetime
from config.settings import CAMINHO_REDE, CAMINHO_LOCAL

def enviar_comando(maquina, acao, parametros=None):
    """Envia comando para máquina específica"""
    
    if parametros is None:
        parametros = {}
    
    comando_id = str(uuid.uuid4())
    
    comando_data = {
        'id': comando_id,
        'acao': acao,
        'parametros': parametros,
        'timestamp': datetime.datetime.now().isoformat(),
        'origem': 'teste_manual'
    }
    
    # Tentar enviar para REDE primeiro
    comando_file_rede = os.path.join(CAMINHO_REDE, f"comando_maq_{maquina}.json")
    comando_file_local = os.path.join(CAMINHO_LOCAL, f"comando_maq_{maquina}.json")
    
    sucesso = False
    
    # Tentar rede
    try:
        if os.path.exists(CAMINHO_REDE):
            with open(comando_file_rede, 'w', encoding='utf-8') as f:
                json.dump(comando_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Comando enviado para REDE: {comando_file_rede}")
            sucesso = True
    except Exception as e:
        print(f"⚠️ Erro ao enviar para rede: {e}")
    
    # Tentar local também (fallback)
    try:
        with open(comando_file_local, 'w', encoding='utf-8') as f:
            json.dump(comando_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Comando enviado para LOCAL: {comando_file_local}")
        sucesso = True
    except Exception as e:
        print(f"⚠️ Erro ao enviar para local: {e}")
    
    if sucesso:
        print(f"\n📋 COMANDO ENVIADO:")
        print(f"   ID: {comando_id}")
        print(f"   Máquina: {maquina}")
        print(f"   Ação: {acao}")
        print(f"   Parâmetros: {parametros}")
        print(f"\n⏳ Aguardando execução pela máquina {maquina}...")
        print(f"   (A máquina verifica comandos a cada 1ms)")
    else:
        print(f"\n❌ FALHA ao enviar comando!")
    
    return sucesso


if __name__ == "__main__":
    print("="*60)
    print("🔧 TESTE DE COMANDOS REMOTOS")
    print("="*60)
    print()
    
    # Solicitar máquina
    print("Máquinas disponíveis: 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214")
    print("Ou: DESENVOLVEDOR, COORDENADOR, ENCARREGADO, ANALISTA, OPERADOR")
    print()
    
    maquina = input("Digite o número/nome da máquina: ").strip()
    
    if not maquina:
        print("❌ Máquina não informada!")
        exit(1)
    
    print()
    print("Comandos disponíveis:")
    print("  1. fechar_app - Fecha o aplicativo")
    print("  2. abrir_app - Abre/restaura o aplicativo")
    print("  3. reiniciar_app - Reinicia o aplicativo")
    print("  4. alterar_size - Altera o size da máquina")
    print("  5. alterar_lote - Altera o lote")
    print("  6. alterar_configuracao_maquina - Altera configuração da máquina")
    print("  7. coletar_dados - Coleta dados do sistema")
    print("  8. fazer_backup - Faz backup dos dados")
    print("  9. coletar_informacoes_sistema - Coleta informações detalhadas")
    print(" 10. testar_conectividade - Testa conectividade")
    print(" 11. obter_logs - Obtém logs do sistema")
    print(" 12. diagnostico_completo - Executa diagnóstico completo")
    print(" 13. limpar_cache - Limpa cache e arquivos temporários")
    print()
    
    acao = input("Digite o número ou nome do comando: ").strip()
    
    # Mapear número para ação
    acoes_map = {
        "1": "fechar_app",
        "2": "abrir_app",
        "3": "reiniciar_app",
        "4": "alterar_size",
        "5": "alterar_lote",
        "6": "alterar_configuracao_maquina",
        "7": "coletar_dados",
        "8": "fazer_backup",
        "9": "coletar_informacoes_sistema",
        "10": "testar_conectividade",
        "11": "obter_logs",
        "12": "diagnostico_completo",
        "13": "limpar_cache"
    }
    
    if acao in acoes_map:
        acao = acoes_map[acao]
    
    # Parâmetros específicos por ação
    parametros = {}
    
    if acao == "alterar_size":
        size = input("Digite o novo size (ex: #0, #1, #2): ").strip()
        peso = input("Digite o novo peso (ex: 0.000096): ").strip()
        parametros = {'size': size, 'peso': peso}
    
    elif acao == "alterar_lote":
        lote = input("Digite o novo lote: ").strip()
        caixa = input("Digite a caixa atual (padrão: 1): ").strip() or "1"
        total = input("Digite o total de caixas (padrão: 100): ").strip() or "100"
        parametros = {'lote': lote, 'caixa_atual': caixa, 'total_caixas': total}
    
    elif acao == "alterar_configuracao_maquina":
        nova_maquina = input("Digite o novo número da máquina: ").strip()
        parametros = {'maquina': nova_maquina}
    
    elif acao == "fechar_app":
        forcar = input("Forçar fechamento? (s/n, padrão: n): ").strip().lower() == 's'
        parametros = {'forcar': forcar}
    
    print()
    print("="*60)
    
    # Enviar comando
    enviar_comando(maquina, acao, parametros)
    
    print()
    print("="*60)
    print("✅ Teste concluído!")
    print("="*60)

