"""
Sistema de Prioridade de Comandos do Desenvolvedor
Garante que comandos do desenvolvedor sejam executados com prioridade máxima
"""

import os
import json
import uuid
import datetime
import threading
import time
from typing import Dict, List, Optional, Callable
from config.settings import CAMINHO_REDE, CAMINHO_LOCAL

class CommandPrioritySystem:
    """Sistema de prioridade para comandos remotos"""
    
    # Níveis de prioridade (maior número = maior prioridade)
    PRIORIDADE_SISTEMA = 1
    PRIORIDADE_USUARIO = 5
    PRIORIDADE_COORDENADOR = 10
    PRIORIDADE_DESENVOLVEDOR = 100  # MÁXIMA PRIORIDADE
    
    def __init__(self, maquina_id: str):
        self.maquina_id = str(maquina_id)
        self.comando_atual = None
        self.fila_comandos = []
        self.executando = False
        self.thread_monitor = None
        self.parar_monitor = False
        
        # Callbacks para execução
        self.callbacks = {}
        
        # Arquivos de comando
        self.arquivo_comando_rede = os.path.join(CAMINHO_REDE, f"comando_maq_{self.maquina_id}.json")
        self.arquivo_comando_local = os.path.join(CAMINHO_LOCAL, f"comando_maq_{self.maquina_id}.json")
        self.arquivo_status = os.path.join(CAMINHO_LOCAL, f"status_maq_{self.maquina_id}.json")
        
        # Log de comandos executados
        self.log_comandos = []
        
        print(f"🎯 Sistema de Prioridade iniciado para máquina {self.maquina_id}")
    
    def iniciar_monitoramento(self):
        """Inicia monitoramento contínuo de comandos"""
        if self.thread_monitor and self.thread_monitor.is_alive():
            return
        
        self.parar_monitor = False
        self.thread_monitor = threading.Thread(target=self._loop_monitoramento, daemon=True)
        self.thread_monitor.start()
        
        print(f"🔄 Monitoramento de comandos iniciado (verificação a cada 1ms)")
    
    def parar_monitoramento(self):
        """Para monitoramento de comandos"""
        self.parar_monitor = True
        if self.thread_monitor:
            self.thread_monitor.join(timeout=1)
        
        print(f"⏹️ Monitoramento de comandos parado")
    
    def _loop_monitoramento(self):
        """Loop principal de monitoramento (1ms)"""
        while not self.parar_monitor:
            try:
                # Verificar novos comandos
                self._verificar_novos_comandos()
                
                # Processar fila de comandos
                self._processar_fila_comandos()
                
                # Aguardar 1ms (1000 verificações por segundo)
                time.sleep(0.001)
                
            except Exception as e:
                print(f"❌ Erro no monitoramento: {e}")
                time.sleep(0.1)  # Aguardar mais em caso de erro
    
    def _verificar_novos_comandos(self):
        """Verifica se há novos comandos (rede e local)"""
        comandos_encontrados = []
        
        # Verificar comando na rede (prioridade)
        if os.path.exists(self.arquivo_comando_rede):
            try:
                comando = self._ler_comando(self.arquivo_comando_rede)
                if comando:
                    comandos_encontrados.append(comando)
                    os.remove(self.arquivo_comando_rede)  # Remove após ler
            except Exception as e:
                print(f"⚠️ Erro ao ler comando da rede: {e}")
        
        # Verificar comando local (fallback)
        if os.path.exists(self.arquivo_comando_local):
            try:
                comando = self._ler_comando(self.arquivo_comando_local)
                if comando:
                    comandos_encontrados.append(comando)
                    os.remove(self.arquivo_comando_local)  # Remove após ler
            except Exception as e:
                print(f"⚠️ Erro ao ler comando local: {e}")
        
        # Adicionar comandos à fila com prioridade
        for comando in comandos_encontrados:
            self._adicionar_comando_fila(comando)
    
    def _ler_comando(self, arquivo: str) -> Optional[Dict]:
        """Lê comando de arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                comando = json.load(f)
            
            # Validar estrutura básica
            if not all(key in comando for key in ['id', 'acao', 'timestamp']):
                print(f"⚠️ Comando inválido: estrutura incorreta")
                return None
            
            # Determinar prioridade baseada na origem
            origem = comando.get('origem', 'sistema')
            comando['prioridade'] = self._determinar_prioridade(origem)
            comando['recebido_em'] = datetime.datetime.now().isoformat()
            
            return comando
            
        except Exception as e:
            print(f"❌ Erro ao ler comando: {e}")
            return None
    
    def _determinar_prioridade(self, origem: str) -> int:
        """Determina prioridade baseada na origem do comando"""
        origem_lower = origem.lower()
        
        if 'desenvolvedor' in origem_lower or 'dev' in origem_lower:
            return self.PRIORIDADE_DESENVOLVEDOR
        elif 'coordenador' in origem_lower or 'coord' in origem_lower:
            return self.PRIORIDADE_COORDENADOR
        elif 'usuario' in origem_lower or 'operador' in origem_lower:
            return self.PRIORIDADE_USUARIO
        else:
            return self.PRIORIDADE_SISTEMA
    
    def _adicionar_comando_fila(self, comando: Dict):
        """Adiciona comando à fila respeitando prioridade"""
        
        # Se for comando de desenvolvedor, interromper comando atual se necessário
        if comando['prioridade'] == self.PRIORIDADE_DESENVOLVEDOR:
            if self.comando_atual and self.comando_atual['prioridade'] < self.PRIORIDADE_DESENVOLVEDOR:
                print(f"🚨 COMANDO DESENVOLVEDOR: Interrompendo comando atual para execução prioritária")
                self.comando_atual['interrompido'] = True
        
        # Inserir na fila mantendo ordem de prioridade
        inserido = False
        for i, cmd_fila in enumerate(self.fila_comandos):
            if comando['prioridade'] > cmd_fila['prioridade']:
                self.fila_comandos.insert(i, comando)
                inserido = True
                break
        
        if not inserido:
            self.fila_comandos.append(comando)
        
        print(f"📥 Comando adicionado à fila: {comando['acao']} (Prioridade: {comando['prioridade']})")
        print(f"📋 Fila atual: {len(self.fila_comandos)} comandos")
    
    def _processar_fila_comandos(self):
        """Processa comandos da fila por ordem de prioridade"""
        if self.executando or not self.fila_comandos:
            return
        
        # Pegar comando de maior prioridade
        comando = self.fila_comandos.pop(0)
        
        # Executar comando
        self._executar_comando(comando)
    
    def _executar_comando(self, comando: Dict):
        """Executa comando específico"""
        self.executando = True
        self.comando_atual = comando
        
        inicio = time.time()
        
        try:
            print(f"⚡ EXECUTANDO: {comando['acao']} (ID: {comando['id'][:8]}...)")
            
            # Buscar callback para a ação
            acao = comando['acao']
            callback = self.callbacks.get(acao)
            
            if callback:
                # Executar callback
                resultado = callback(comando)
                comando['resultado'] = resultado
                comando['status'] = 'sucesso'
                print(f"✅ Comando executado com sucesso: {acao}")
            else:
                comando['resultado'] = f"Ação '{acao}' não implementada"
                comando['status'] = 'erro'
                print(f"❌ Ação não encontrada: {acao}")
            
        except Exception as e:
            comando['resultado'] = f"Erro na execução: {str(e)}"
            comando['status'] = 'erro'
            print(f"❌ Erro ao executar comando: {e}")
        
        finally:
            # Finalizar execução
            fim = time.time()
            comando['tempo_execucao'] = fim - inicio
            comando['executado_em'] = datetime.datetime.now().isoformat()
            
            # Adicionar ao log
            self.log_comandos.append(comando)
            
            # Manter apenas últimos 100 comandos no log
            if len(self.log_comandos) > 100:
                self.log_comandos = self.log_comandos[-100:]
            
            # Atualizar status
            self._atualizar_status_sistema()
            
            self.executando = False
            self.comando_atual = None
            
            print(f"⏱️ Comando finalizado em {comando['tempo_execucao']:.3f}s")
    
    def _atualizar_status_sistema(self):
        """Atualiza status do sistema"""
        try:
            status = {
                'maquina_id': self.maquina_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'comandos_na_fila': len(self.fila_comandos),
                'executando': self.executando,
                'ultimo_comando': self.log_comandos[-1] if self.log_comandos else None,
                'total_comandos_executados': len(self.log_comandos),
                'sistema_ativo': True
            }
            
            # Salvar status local
            with open(self.arquivo_status, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            # Tentar salvar na rede também
            try:
                arquivo_status_rede = os.path.join(CAMINHO_REDE, f"status_maq_{self.maquina_id}.json")
                with open(arquivo_status_rede, 'w', encoding='utf-8') as f:
                    json.dump(status, f, indent=2, ensure_ascii=False)
            except:
                pass  # Falha silenciosa na rede
                
        except Exception as e:
            print(f"⚠️ Erro ao atualizar status: {e}")
    
    def registrar_callback(self, acao: str, callback: Callable):
        """Registra callback para uma ação específica"""
        self.callbacks[acao] = callback
        print(f"📝 Callback registrado para ação: {acao}")
    
    def enviar_comando_desenvolvedor(self, acao: str, parametros: Dict = None) -> str:
        """Envia comando com prioridade de desenvolvedor"""
        if parametros is None:
            parametros = {}
        
        comando_id = str(uuid.uuid4())
        
        comando = {
            'id': comando_id,
            'acao': acao,
            'parametros': parametros,
            'timestamp': datetime.datetime.now().isoformat(),
            'origem': 'desenvolvedor',
            'prioridade': self.PRIORIDADE_DESENVOLVEDOR
        }
        
        # Adicionar diretamente à fila (bypass do arquivo)
        self._adicionar_comando_fila(comando)
        
        print(f"🚨 COMANDO DESENVOLVEDOR ENVIADO: {acao} (ID: {comando_id[:8]}...)")
        
        return comando_id
    
    def obter_status(self) -> Dict:
        """Obtém status atual do sistema"""
        return {
            'maquina_id': self.maquina_id,
            'executando': self.executando,
            'comando_atual': self.comando_atual,
            'fila_comandos': len(self.fila_comandos),
            'total_executados': len(self.log_comandos),
            'ultimos_comandos': self.log_comandos[-5:] if self.log_comandos else []
        }
    
    def obter_log_comandos(self, limite: int = 50) -> List[Dict]:
        """Obtém log dos últimos comandos executados"""
        return self.log_comandos[-limite:] if self.log_comandos else []


# Instância global do sistema de prioridade
_sistema_prioridade = None

def inicializar_sistema_prioridade(maquina_id: str) -> CommandPrioritySystem:
    """Inicializa sistema de prioridade global"""
    global _sistema_prioridade
    
    if _sistema_prioridade:
        _sistema_prioridade.parar_monitoramento()
    
    _sistema_prioridade = CommandPrioritySystem(maquina_id)
    _sistema_prioridade.iniciar_monitoramento()
    
    return _sistema_prioridade

def obter_sistema_prioridade() -> Optional[CommandPrioritySystem]:
    """Obtém instância do sistema de prioridade"""
    return _sistema_prioridade

def finalizar_sistema_prioridade():
    """Finaliza sistema de prioridade"""
    global _sistema_prioridade
    
    if _sistema_prioridade:
        _sistema_prioridade.parar_monitoramento()
        _sistema_prioridade = None
        print("🛑 Sistema de prioridade finalizado")


if __name__ == "__main__":
    # Teste do sistema
    print("🧪 TESTE DO SISTEMA DE PRIORIDADE")
    print("="*50)
    
    # Inicializar sistema
    sistema = inicializar_sistema_prioridade("201")
    
    # Registrar alguns callbacks de teste
    def callback_teste(comando):
        print(f"  🔧 Executando: {comando['acao']}")
        time.sleep(0.1)  # Simular processamento
        return f"Ação {comando['acao']} executada com sucesso"
    
    sistema.registrar_callback("teste_acao", callback_teste)
    sistema.registrar_callback("fechar_app", callback_teste)
    sistema.registrar_callback("reiniciar_app", callback_teste)
    
    # Enviar alguns comandos de teste
    print("\n📤 Enviando comandos de teste...")
    
    # Comando normal
    sistema.enviar_comando_desenvolvedor("teste_acao", {"param": "valor1"})
    
    # Comando de alta prioridade
    sistema.enviar_comando_desenvolvedor("fechar_app", {"forcar": True})
    
    # Aguardar execução
    print("\n⏳ Aguardando execução...")
    time.sleep(2)
    
    # Mostrar status
    status = sistema.obter_status()
    print(f"\n📊 STATUS FINAL:")
    print(f"   Executados: {status['total_executados']}")
    print(f"   Na fila: {status['fila_comandos']}")
    
    # Finalizar
    finalizar_sistema_prioridade()
    print("\n✅ Teste concluído!")