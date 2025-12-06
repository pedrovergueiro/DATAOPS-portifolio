"""Sistema de Auditoria - Registro Imutável de Ações"""

import os
import datetime
import json
import hashlib
from config.settings import CAMINHO_LOCAL

# Caminho do arquivo de auditoria (NUNCA PODE SER DELETADO)
AUDITORIA_PATH = os.path.join(CAMINHO_LOCAL, "auditoria_producao.json")

def gerar_hash_registro(registro):
    """Gera hash único para o registro (garantir integridade)"""
    registro_str = json.dumps(registro, sort_keys=True)
    return hashlib.sha256(registro_str.encode()).hexdigest()

def registrar_auditoria(acao, usuario, detalhes, dados_antes=None, dados_depois=None):
    """
    Registra ação no sistema de auditoria IMUTÁVEL
    
    Args:
        acao: Tipo de ação (INSERT, UPDATE, DELETE, EXPORT, etc.)
        usuario: Usuário que executou a ação
        detalhes: Descrição detalhada da ação
        dados_antes: Dados antes da modificação (para UPDATE/DELETE)
        dados_depois: Dados depois da modificação (para INSERT/UPDATE)
    """
    try:
        # Carregar registros existentes
        if os.path.exists(AUDITORIA_PATH):
            with open(AUDITORIA_PATH, 'r', encoding='utf-8') as f:
                auditoria = json.load(f)
        else:
            auditoria = {
                'versao': '1.0',
                'criado_em': datetime.datetime.now().isoformat(),
                'registros': []
            }
        
        # Criar novo registro
        registro = {
            'id': len(auditoria['registros']) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'data_hora_legivel': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'acao': acao,
            'usuario': usuario,
            'detalhes': detalhes,
            'dados_antes': dados_antes,
            'dados_depois': dados_depois,
            'ip': _obter_ip(),
            'hostname': _obter_hostname()
        }
        
        # Adicionar hash para garantir integridade
        registro['hash'] = gerar_hash_registro(registro)
        
        # Adicionar à lista
        auditoria['registros'].append(registro)
        auditoria['ultimo_registro'] = datetime.datetime.now().isoformat()
        auditoria['total_registros'] = len(auditoria['registros'])
        
        # Salvar (com proteção contra corrupção)
        _salvar_auditoria_seguro(auditoria)
        
        print(f"📋 Auditoria: {acao} por {usuario}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao registrar auditoria: {e}")
        # CRÍTICO: Tentar salvar em backup
        try:
            backup_path = os.path.join(CAMINHO_LOCAL, f"auditoria_backup_{int(datetime.datetime.now().timestamp())}.json")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(registro, f, indent=2, ensure_ascii=False)
            print(f"📦 Backup de auditoria salvo: {backup_path}")
        except:
            pass
        return False

def _salvar_auditoria_seguro(auditoria):
    """Salva auditoria com proteção contra corrupção"""
    try:
        # Salvar em arquivo temporário primeiro
        temp_path = AUDITORIA_PATH + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(auditoria, f, indent=2, ensure_ascii=False)
        
        # Se salvou com sucesso, substituir o original
        if os.path.exists(AUDITORIA_PATH):
            # Fazer backup do arquivo atual
            backup_path = AUDITORIA_PATH + '.bak'
            import shutil
            shutil.copy2(AUDITORIA_PATH, backup_path)
        
        # Mover temp para original
        os.replace(temp_path, AUDITORIA_PATH)
        
        # Tornar arquivo somente leitura (proteção adicional)
        try:
            os.chmod(AUDITORIA_PATH, 0o444)  # Somente leitura
        except:
            pass
            
    except Exception as e:
        print(f"❌ Erro ao salvar auditoria: {e}")
        raise

def obter_historico_auditoria(filtro_usuario=None, filtro_acao=None, limite=100):
    """Obtém histórico de auditoria com filtros"""
    try:
        if not os.path.exists(AUDITORIA_PATH):
            return []
        
        with open(AUDITORIA_PATH, 'r', encoding='utf-8') as f:
            auditoria = json.load(f)
        
        registros = auditoria.get('registros', [])
        
        # Aplicar filtros
        if filtro_usuario:
            registros = [r for r in registros if r['usuario'] == filtro_usuario]
        
        if filtro_acao:
            registros = [r for r in registros if r['acao'] == filtro_acao]
        
        # Retornar últimos N registros
        return registros[-limite:]
        
    except Exception as e:
        print(f"❌ Erro ao obter auditoria: {e}")
        return []

def verificar_integridade_auditoria():
    """Verifica se o arquivo de auditoria foi modificado"""
    try:
        if not os.path.exists(AUDITORIA_PATH):
            return True, "Arquivo de auditoria não existe ainda"
        
        with open(AUDITORIA_PATH, 'r', encoding='utf-8') as f:
            auditoria = json.load(f)
        
        registros_invalidos = []
        
        for registro in auditoria.get('registros', []):
            hash_original = registro.get('hash', '')
            registro_sem_hash = {k: v for k, v in registro.items() if k != 'hash'}
            hash_calculado = gerar_hash_registro(registro_sem_hash)
            
            if hash_original != hash_calculado:
                registros_invalidos.append(registro['id'])
        
        if registros_invalidos:
            return False, f"Registros com integridade comprometida: {registros_invalidos}"
        else:
            return True, "Todos os registros estão íntegros"
            
    except Exception as e:
        return False, f"Erro ao verificar integridade: {e}"

def exportar_auditoria_relatorio(caminho_destino=None):
    """Exporta auditoria para relatório legível"""
    try:
        if not os.path.exists(AUDITORIA_PATH):
            return False, "Arquivo de auditoria não existe"
        
        with open(AUDITORIA_PATH, 'r', encoding='utf-8') as f:
            auditoria = json.load(f)
        
        if not caminho_destino:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_destino = os.path.join(CAMINHO_LOCAL, f"relatorio_auditoria_{timestamp}.txt")
        
        with open(caminho_destino, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RELATÓRIO DE AUDITORIA - SISTEMA DE PRODUÇÃO\n")
            f.write("="*80 + "\n\n")
            f.write(f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de registros: {auditoria.get('total_registros', 0)}\n")
            f.write(f"Criado em: {auditoria.get('criado_em', 'N/A')}\n\n")
            f.write("="*80 + "\n\n")
            
            for registro in auditoria.get('registros', []):
                f.write(f"ID: {registro['id']}\n")
                f.write(f"Data/Hora: {registro['data_hora_legivel']}\n")
                f.write(f"Ação: {registro['acao']}\n")
                f.write(f"Usuário: {registro['usuario']}\n")
                f.write(f"Detalhes: {registro['detalhes']}\n")
                
                if registro.get('dados_antes'):
                    f.write(f"Dados Antes: {json.dumps(registro['dados_antes'], ensure_ascii=False)}\n")
                
                if registro.get('dados_depois'):
                    f.write(f"Dados Depois: {json.dumps(registro['dados_depois'], ensure_ascii=False)}\n")
                
                f.write(f"IP: {registro.get('ip', 'N/A')}\n")
                f.write(f"Hostname: {registro.get('hostname', 'N/A')}\n")
                f.write(f"Hash: {registro.get('hash', 'N/A')}\n")
                f.write("-"*80 + "\n\n")
        
        return True, caminho_destino
        
    except Exception as e:
        return False, f"Erro ao exportar: {e}"

def _obter_ip():
    """Obtém IP local"""
    try:
        import socket
        return socket.gethostbyname(socket.gethostname())
    except:
        return "N/A"

def _obter_hostname():
    """Obtém hostname"""
    try:
        import socket
        return socket.gethostname()
    except:
        return "N/A"

# Funções específicas para auditoria de produção

def auditar_insercao_producao(usuario, dados_producao):
    """Audita inserção de dados de produção"""
    return registrar_auditoria(
        acao="INSERT_PRODUCAO",
        usuario=usuario,
        detalhes=f"Inserção de dados de produção - Máquina: {dados_producao.get('maquina')}, Lote: {dados_producao.get('lote')}, Caixa: {dados_producao.get('numero_caixa')}",
        dados_depois=dados_producao
    )

def auditar_edicao_producao(usuario, dados_antes, dados_depois, justificativa):
    """Audita edição de dados de produção"""
    return registrar_auditoria(
        acao="UPDATE_PRODUCAO",
        usuario=usuario,
        detalhes=f"Edição de dados de produção - Justificativa: {justificativa}",
        dados_antes=dados_antes,
        dados_depois=dados_depois
    )

def auditar_exclusao_producao(usuario, dados_excluidos, justificativa):
    """Audita exclusão de dados de produção"""
    return registrar_auditoria(
        acao="DELETE_PRODUCAO",
        usuario=usuario,
        detalhes=f"Exclusão de dados de produção - Justificativa: {justificativa}",
        dados_antes=dados_excluidos
    )

def auditar_exportacao_dados(usuario, tipo_exportacao, quantidade):
    """Audita exportação de dados"""
    return registrar_auditoria(
        acao="EXPORT_DADOS",
        usuario=usuario,
        detalhes=f"Exportação de dados - Tipo: {tipo_exportacao}, Quantidade: {quantidade} registros"
    )

def auditar_acesso_painel(usuario, painel):
    """Audita acesso a painéis administrativos"""
    return registrar_auditoria(
        acao="ACESSO_PAINEL",
        usuario=usuario,
        detalhes=f"Acesso ao painel: {painel}"
    )
