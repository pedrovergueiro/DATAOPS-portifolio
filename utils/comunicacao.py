"""Sistema de Comunicação em Tempo Real - 1ms"""

import threading
import time
import os
import json
import datetime
import uuid
import socket
import psutil
import tkinter as tk
from tkinter import messagebox
from config.settings import CAMINHO_REDE
from utils.machine_id import gerar_id_computador_avancado


class SistemaComunicacao:
    """Sistema de comunicação em tempo real entre máquinas"""
    
    def __init__(self):
        self.comandos_ativos = {}
        self.thread_comandos = None
        self.executando_comandos = False
        self.ultimo_status = {}
        self.root_ref = None
        self.comandos_executados = []
        self.machine_config = None
        self.batch_config = None
        self.data_manager = None
        
    def set_root_reference(self, root):
        """Define referência para a janela principal"""
        self.root_ref = root
    
    def set_configs(self, machine_config, batch_config, data_manager):
        """Define configurações do sistema"""
        self.machine_config = machine_config
        self.batch_config = batch_config
        self.data_manager = data_manager
        
    def iniciar_sistema_comunicacao(self):
        """Inicia sistema de envio de status e recebimento de comandos"""
        if self.executando_comandos:
            print("⚠️ Sistema de comunicação já está ativo")
            return
            
        print("🚀 INICIANDO SISTEMA DE COMUNICAÇÃO ULTRA-RÁPIDO...")
        
        # Limpar comandos ativos antigos
        self.comandos_ativos.clear()
        
        # Verificar se diretórios existem
        from config.settings import CAMINHO_LOCAL
        
        if os.path.exists(CAMINHO_REDE):
            print(f"✅ Acesso à REDE: {CAMINHO_REDE}")
        else:
            print(f"⚠️ SEM acesso à rede: {CAMINHO_REDE}")
            
        if os.path.exists(CAMINHO_LOCAL):
            print(f"✅ Acesso LOCAL: {CAMINHO_LOCAL}")
        else:
            print(f"❌ SEM acesso local: {CAMINHO_LOCAL}")
            
        self.executando_comandos = True
        self.thread_comandos = threading.Thread(target=self._loop_comunicacao, daemon=True)
        self.thread_comandos.start()
        
        print("🔗 Sistema de comunicação INICIADO!")
        print("⚡ Verificação de comandos: CADA 1ms (1000x por segundo)")
        print("📊 Envio de status: CADA 1 segundo")
        print("🎯 PRONTO para receber e executar comandos remotos!")
        
    def parar_sistema_comunicacao(self):
        """Para sistema de comunicação"""
        print("🛑 PARANDO sistema de comunicação...")
        self.executando_comandos = False
        
        # Aguardar thread terminar
        if self.thread_comandos and self.thread_comandos.is_alive():
            self.thread_comandos.join(timeout=2)
            
        print("🔗 Sistema de comunicação PARADO")
        
    def verificar_status_comunicacao(self):
        """Verifica se o sistema de comunicação está ativo"""
        return {
            'ativo': self.executando_comandos,
            'thread_viva': self.thread_comandos.is_alive() if self.thread_comandos else False,
            'comandos_executados': len(self.comandos_executados),
            'ultimo_status': self.ultimo_status.get('timestamp', 'Nunca') if self.ultimo_status else 'Nunca'
        }
        
    def _loop_comunicacao(self):
        """Loop principal de comunicação - VERIFICA COMANDOS A CADA 1ms (1000x/segundo)"""
        contador = 0
        contador_status = 0
        contador_comandos_verificados = 0
        contador_comandos_executados = 0
        
        print("🚀 INICIANDO LOOP DE COMUNICAÇÃO ULTRA-RÁPIDO (1ms)")
        print("📡 Verificando comandos a cada 1 milissegundo")
        print("📊 Enviando status a cada 1 segundo")
        
        # Log para arquivo também
        try:
            from utils.logger_executavel import log_info
            log_info("Sistema de comunicação iniciado - Loop ultra-rápido (1ms)")
        except:
            pass
        
        while self.executando_comandos:
            try:
                # VERIFICAR COMANDOS A CADA 1ms (PRIORIDADE MÁXIMA)
                comando_executado = self._verificar_comandos()
                contador_comandos_verificados += 1
                
                if comando_executado:
                    contador_comandos_executados += 1
                    print(f"⚡ COMANDO EXECUTADO! Total executados: {contador_comandos_executados}")
                
                # ENVIAR STATUS A CADA 1000ms (1 segundo) para não sobrecarregar
                if contador % 1000 == 0:
                    self._enviar_status_maquina()
                    contador_status += 1
                
                # Sleep mínimo para verificação ultra-rápida
                time.sleep(0.001)  # 1ms - VERIFICAÇÃO ULTRA RÁPIDA
                contador += 1
                
                # Log detalhado a cada 30000 iterações (30 segundos)
                if contador % 30000 == 0:
                    print(f"🔗 COMUNICAÇÃO ATIVA:")
                    print(f"   ⏱️  {contador} verificações (1ms cada) = {contador/1000:.1f}s ativo")
                    print(f"   📊 Status enviado {contador_status}x")
                    print(f"   🔍 Comandos verificados: {contador_comandos_verificados}")
                    print(f"   ⚡ Comandos executados: {contador_comandos_executados}")
                    print(f"   🎯 Taxa execução: {(contador_comandos_executados/contador_comandos_verificados*100):.4f}%")
                
            except Exception as e:
                print(f"⚠️ Erro no loop comunicação: {e}")
                # Continuar mesmo com erro, mas com delay maior
                time.sleep(0.005)  # 5ms em caso de erro
                
    def _enviar_status_maquina(self):
        """Envia status da máquina para rede E local"""
        if not self.machine_config or not self.batch_config or not self.data_manager:
            return
            
        try:
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            CONFIG_SIZE = self.machine_config.obter_configuracao_size()
            config_lote = self.batch_config.obter_configuracao_lote()
            
            from utils.machine_id import gerar_id_computador_avancado
            from config.settings import CAMINHO_LOCAL
            ID_COMPUTADOR = gerar_id_computador_avancado()
            
            # Arquivos de status (rede E local)
            status_file_rede = os.path.join(CAMINHO_REDE, f"status_maq_{MAQUINA_ATUAL}.json")
            status_file_local = os.path.join(CAMINHO_LOCAL, f"status_maq_{MAQUINA_ATUAL}.json")
            
            # Verificar recursos do sistema
            cpu_percent = psutil.cpu_percent()
            mem_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            status_data = {
                'maquina': MAQUINA_ATUAL,
                'id_computador': ID_COMPUTADOR,
                'timestamp': datetime.datetime.now().isoformat(),
                'status': 'online',
                'app_aberto': True,
                'ultima_acao': datetime.datetime.now().strftime("%H:%M:%S"),
                'size': CONFIG_SIZE['size'],
                'peso': CONFIG_SIZE['peso'],
                'lote': config_lote.get('lote', ''),
                'caixa_atual': config_lote.get('caixa_atual', 0),
                'total_caixas': config_lote.get('total_caixas', 0),
                'caixas_registradas': config_lote.get('caixas_registradas', 0),
                'recursos': {
                    'cpu': cpu_percent,
                    'memoria': mem_percent,
                    'disco': disk_percent
                },
                'comandos_executados': self.comandos_executados[-10:],
                'hostname': socket.gethostname(),
                'ip': self._obter_ip_local(),
                'versao': '1.0',
                'online': True
            }
            
            # Salvar SEMPRE localmente (para descoberta de máquinas)
            try:
                with open(status_file_local, 'w', encoding='utf-8') as f:
                    json.dump(status_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"⚠️ Erro salvar status local: {e}")
            
            # Tentar enviar para rede também
            try:
                if os.path.exists(CAMINHO_REDE):
                    with open(status_file_rede, 'w', encoding='utf-8') as f:
                        json.dump(status_data, f, indent=2, ensure_ascii=False)
            except:
                pass
                
            self.ultimo_status = status_data
            
        except Exception as e:
            print(f"⚠️ Erro enviar status: {e}")
            
    def _obter_ip_local(self):
        """Obtém IP local da máquina"""
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"
            
    def _verificar_comandos(self):
        """Verifica se há comandos para executar - A CADA 1ms (ULTRA RÁPIDO)"""
        if not self.machine_config:
            return False
            
        try:
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            
            # Verificar REDE primeiro (prioridade)
            comando_file_rede = os.path.join(CAMINHO_REDE, f"comando_maq_{MAQUINA_ATUAL}.json")
            
            # Verificar LOCAL também (fallback)
            from config.settings import CAMINHO_LOCAL
            comando_file_local = os.path.join(CAMINHO_LOCAL, f"comando_maq_{MAQUINA_ATUAL}.json")
            
            # Lista de arquivos para verificar (ordem de prioridade)
            arquivos_comando = []
            if os.path.exists(comando_file_rede):
                arquivos_comando.append(('REDE', comando_file_rede))
            if os.path.exists(comando_file_local):
                arquivos_comando.append(('LOCAL', comando_file_local))
            
            # Processar todos os comandos encontrados
            comando_executado = False
            
            for origem, comando_file in arquivos_comando:
                try:
                    # Verificar se arquivo não está vazio e foi escrito completamente
                    if os.path.getsize(comando_file) == 0:
                        continue
                        
                    # Pequeno delay para garantir escrita completa
                    time.sleep(0.002)
                    
                    with open(comando_file, 'r', encoding='utf-8') as f:
                        comando_data = json.load(f)
                    
                    comando_id = comando_data.get('id', '')
                    acao = comando_data.get('acao', 'N/A')
                    
                    # Verificar se comando já foi executado
                    if comando_id and comando_id not in self.comandos_ativos:
                        self.comandos_ativos[comando_id] = True
                        
                        print(f"🔔 COMANDO RECEBIDO ({origem}): {acao} (ID: {comando_id[:8]}...)")
                        print(f"📁 Arquivo: {comando_file}")
                        
                        # Log detalhado
                        try:
                            from utils.logger_executavel import log_info
                            log_info(f"COMANDO RECEBIDO: {acao} de {origem} (ID: {comando_id})")
                        except:
                            pass
                        
                        # Executar comando IMEDIATAMENTE
                        try:
                            self._executar_comando(comando_data)
                            print(f"✅ COMANDO EXECUTADO COM SUCESSO: {acao}")
                            
                            # Log sucesso
                            try:
                                from utils.logger_executavel import log_info
                                log_info(f"COMANDO EXECUTADO COM SUCESSO: {acao}")
                            except:
                                pass
                            
                            comando_executado = True
                        except Exception as e:
                            print(f"❌ ERRO AO EXECUTAR COMANDO {acao}: {e}")
                            
                            # Log erro
                            try:
                                from utils.logger_executavel import log_error
                                log_error(f"ERRO AO EXECUTAR COMANDO {acao}: {e}")
                            except:
                                pass
                        
                        # Registrar comando executado
                        self.comandos_executados.append({
                            'id': comando_id,
                            'acao': acao,
                            'origem': origem,
                            'timestamp': datetime.datetime.now().isoformat(),
                            'arquivo': comando_file
                        })
                        
                        # Manter apenas últimos 100 comandos
                        if len(self.comandos_executados) > 100:
                            self.comandos_executados = self.comandos_executados[-100:]
                    
                    # Remover arquivo de comando após execução (SEMPRE)
                    try:
                        os.remove(comando_file)
                        print(f"🗑️ Arquivo de comando removido: {os.path.basename(comando_file)}")
                    except Exception as e:
                        print(f"⚠️ Erro ao remover arquivo de comando: {e}")
                        
                except json.JSONDecodeError as e:
                    print(f"⚠️ Arquivo de comando com JSON inválido ({origem}): {e}")
                    # Remover arquivo corrompido
                    try:
                        os.remove(comando_file)
                        print(f"🗑️ Arquivo corrompido removido: {comando_file}")
                    except:
                        pass
                except Exception as e:
                    print(f"⚠️ Erro ao processar comando ({origem}): {e}")
            
            return comando_executado
                
        except Exception as e:
            # Log apenas erros críticos
            if "No such file" not in str(e):
                print(f"⚠️ Erro crítico verificar comandos: {e}")
            return False
            
    def _executar_comando(self, comando_data):
        """Executa comando recebido"""
        try:
            acao = comando_data.get('acao', '')
            parametros = comando_data.get('parametros', {})
            
            print(f"🔧 Executando comando: {acao}")
            
            if self.root_ref:
                if acao == 'fechar_app':
                    self.root_ref.after(0, lambda: self._comando_fechar_app(parametros))
                elif acao == 'abrir_app':
                    self.root_ref.after(0, lambda: self._comando_abrir_app(parametros))
                elif acao == 'reiniciar_app':
                    self.root_ref.after(0, lambda: self._comando_reiniciar_app(parametros))
                elif acao == 'alterar_size':
                    self.root_ref.after(0, lambda: self._comando_alterar_size(parametros))
                elif acao == 'alterar_lote':
                    self.root_ref.after(0, lambda: self._comando_alterar_lote(parametros))
                elif acao == 'alterar_configuracao_maquina':
                    self.root_ref.after(0, lambda: self._comando_alterar_configuracao_maquina(parametros))
                elif acao == 'coletar_dados':
                    self._comando_coletar_dados(parametros)
                elif acao == 'fazer_backup':
                    self._comando_fazer_backup(parametros)
                elif acao == 'coletar_informacoes_sistema':
                    self._comando_coletar_informacoes_sistema(parametros)
                elif acao == 'executar_comando_sistema':
                    self._comando_executar_comando_sistema(parametros)
                elif acao == 'testar_conectividade':
                    self._comando_testar_conectividade(parametros)
                elif acao == 'obter_logs':
                    self._comando_obter_logs(parametros)
                elif acao == 'diagnostico_completo':
                    self._comando_diagnostico_completo(parametros)
                elif acao == 'limpar_cache':
                    self._comando_limpar_cache(parametros)
                elif acao == 'capturar_tela':
                    self._comando_capturar_tela(parametros)
                else:
                    print(f"❌ Comando desconhecido: {acao}")
                
        except Exception as e:
            print(f"❌ Erro executar comando: {e}")
    
    def _comando_fechar_app(self, parametros):
        """Fecha aplicação"""
        print("🛑 Recebido comando: FECHAR APP")
        
        from tkinter import messagebox
        
        # Mostrar confirmação SEMPRE NO TOPO
        if self.root_ref:
            # Criar janela de confirmação
            janela_confirmacao = tk.Toplevel(self.root_ref)
            janela_confirmacao.title("⚠️ Confirmação")
            janela_confirmacao.geometry("400x200")
            janela_confirmacao.attributes('-topmost', True)
            janela_confirmacao.grab_set()
            
            frame = tk.Frame(janela_confirmacao)
            frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            tk.Label(frame, text="⚠️ COMANDO REMOTO RECEBIDO", 
                    font=("Arial", 14, "bold"), fg="red").pack(pady=10)
            
            tk.Label(frame, text="Deseja FECHAR o aplicativo?", 
                    font=("Arial", 11)).pack(pady=10)
            
            resultado = [False]
            
            def confirmar():
                resultado[0] = True
                janela_confirmacao.destroy()
                if parametros.get('forcar', False):
                    os._exit(0)
                else:
                    if self.root_ref:
                        self.root_ref.quit()
            
            def cancelar():
                janela_confirmacao.destroy()
            
            btn_frame = tk.Frame(frame)
            btn_frame.pack(pady=20)
            
            tk.Button(btn_frame, text="✅ SIM, FECHAR", command=confirmar,
                     bg="#dc3545", fg="white", font=("Arial", 11, "bold"), 
                     width=15, height=2).pack(side='left', padx=5)
            
            tk.Button(btn_frame, text="❌ CANCELAR", command=cancelar,
                     bg="#6c757d", fg="white", font=("Arial", 11, "bold"), 
                     width=15, height=2).pack(side='left', padx=5)
            
            # Centralizar
            janela_confirmacao.update_idletasks()
            x = (janela_confirmacao.winfo_screenwidth() - janela_confirmacao.winfo_width()) // 2
            y = (janela_confirmacao.winfo_screenheight() - janela_confirmacao.winfo_height()) // 2
            janela_confirmacao.geometry(f"+{x}+{y}")
    
    def _comando_abrir_app(self, parametros):
        """Abre/restaura aplicação"""
        print("🚀 Recebido comando: ABRIR APP")
        if self.root_ref and self.root_ref.winfo_exists():
            self.root_ref.deiconify()
            self.root_ref.lift()
            self.root_ref.focus_force()
    
    def _comando_reiniciar_app(self, parametros):
        """Reinicia aplicação"""
        print("🔄 Recebido comando: REINICIAR APP")
        import sys
        
        # Verificar se está rodando como executável
        if getattr(sys, 'frozen', False):
            # Executável PyInstaller
            executable_path = sys.executable
            print(f"🔄 Reiniciando executável: {executable_path}")
            os.execl(executable_path, executable_path)
        else:
            # Script Python
            python = sys.executable
            print(f"🔄 Reiniciando script Python: {python} {' '.join(sys.argv)}")
            os.execl(python, python, *sys.argv)
    
    def _comando_alterar_size(self, parametros):
        """Altera size da máquina"""
        print("📏 Recebido comando: ALTERAR SIZE")
        size_novo = parametros.get('size')
        peso_novo = parametros.get('peso')
        
        if size_novo and peso_novo and self.machine_config:
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            CONFIG_SIZE = {
                'maquina': MAQUINA_ATUAL,
                'size': size_novo,
                'peso': float(peso_novo)
            }
            self.machine_config.salvar_configuracao_size(CONFIG_SIZE)
            print(f"✅ Size alterado: {size_novo} (Peso: {peso_novo})")
    
    def _comando_alterar_lote(self, parametros):
        """Altera lote"""
        print("📦 Recebido comando: ALTERAR LOTE")
        lote_novo = parametros.get('lote')
        caixa_nova = parametros.get('caixa_atual', 1)
        total_novo = parametros.get('total_caixas', 100)
        
        if lote_novo and self.batch_config:
            self.batch_config.salvar_configuracao_lote(lote_novo, int(caixa_nova), int(total_novo), 0)
            print(f"✅ Lote alterado: {lote_novo}")
    
    def _comando_alterar_configuracao_maquina(self, parametros):
        """Altera configuração da máquina"""
        print("⚙️ Recebido comando: ALTERAR CONFIGURAÇÃO MÁQUINA")
        nova_maquina = parametros.get('maquina')
        
        if nova_maquina and self.machine_config:
            self.machine_config.salvar_configuracao_maquina(nova_maquina)
            print(f"✅ Máquina alterada: {nova_maquina}")
    
    def _comando_coletar_dados(self, parametros):
        """Coleta dados do sistema"""
        print("📊 Recebido comando: COLETAR DADOS")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            
            info_sistema = {
                'timestamp': datetime.datetime.now().isoformat(),
                'maquina': MAQUINA_ATUAL,
                'hostname': socket.gethostname(),
                'ip': self._obter_ip_local(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'total_registros': len(self.data_manager.df) if self.data_manager.df is not None else 0,
                'total_usuarios': len(self.data_manager.df_users) if self.data_manager.df_users is not None else 0
            }
            
            dados_file = os.path.join(CAMINHO_REDE, f"dados_coletados_{MAQUINA_ATUAL}_{int(time.time())}.json")
            with open(dados_file, 'w', encoding='utf-8') as f:
                json.dump(info_sistema, f, indent=2, ensure_ascii=False)
                
            print(f"📊 Dados coletados salvos em: {dados_file}")
        except Exception as e:
            print(f"❌ Erro coletar dados: {e}")
    
    def _comando_fazer_backup(self, parametros):
        """Faz backup dos dados"""
        print("💾 Recebido comando: FAZER BACKUP")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(CAMINHO_REDE, f"backup_{MAQUINA_ATUAL}_{timestamp}.zip")
            
            import zipfile
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                arquivos = [
                    self.data_manager.csv_path,
                    self.data_manager.users_path,
                    self.data_manager.log_path
                ]
                for arquivo in arquivos:
                    if os.path.exists(arquivo):
                        zipf.write(arquivo, os.path.basename(arquivo))
                        
            print(f"💾 Backup criado: {backup_file}")
        except Exception as e:
            print(f"❌ Erro criar backup: {e}")
    
    def _comando_coletar_informacoes_sistema(self, parametros):
        """Coleta informações detalhadas do sistema"""
        print("🔍 Recebido comando: COLETAR INFORMAÇÕES SISTEMA")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            CONFIG_SIZE = self.machine_config.obter_configuracao_size()
            config_lote = self.batch_config.obter_configuracao_lote()
            
            info_detalhada = {
                'maquina': MAQUINA_ATUAL,
                'id_computador': gerar_id_computador_avancado(),
                'hostname': socket.gethostname(),
                'ip': self._obter_ip_local(),
                'sistema_operacional': os.name,
                'timestamp': datetime.datetime.now().isoformat(),
                'recursos': {
                    'cpu_cores': psutil.cpu_count(),
                    'cpu_usage': psutil.cpu_percent(interval=1),
                    'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                    'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_total_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                    'disk_used_gb': round(psutil.disk_usage('/').used / (1024**3), 2),
                    'disk_free_gb': round(psutil.disk_usage('/').free / (1024**3), 2),
                    'disk_percent': psutil.disk_usage('/').percent
                },
                'configuracoes': {
                    'size': CONFIG_SIZE,
                    'lote_atual': config_lote.get('lote', ''),
                    'caixa_atual': config_lote.get('caixa_atual', 0),
                    'total_caixas': config_lote.get('total_caixas', 0)
                },
                'estatisticas': {
                    'total_registros': len(self.data_manager.df) if self.data_manager.df is not None else 0,
                    'total_usuarios': len(self.data_manager.df_users) if self.data_manager.df_users is not None else 0,
                    'total_logs': len(self.data_manager.df_log) if self.data_manager.df_log is not None else 0
                },
                'rede': {
                    'conectado_rede': os.path.exists(CAMINHO_REDE),
                    'caminho_rede': CAMINHO_REDE
                }
            }
            
            info_file = os.path.join(CAMINHO_REDE, f"info_sistema_{MAQUINA_ATUAL}_{int(time.time())}.json")
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(info_detalhada, f, indent=2, ensure_ascii=False)
                
            print(f"🔍 Informações salvas em: {info_file}")
        except Exception as e:
            print(f"❌ Erro coletar informações: {e}")
    
    def _comando_executar_comando_sistema(self, parametros):
        """Executa comando do sistema operacional"""
        comando = parametros.get('comando', '')
        print(f"⚙️ Recebido comando: EXECUTAR COMANDO SISTEMA - {comando}")
        
        if not comando:
            return
            
        try:
            import subprocess
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=60)
            
            if self.machine_config:
                MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
                resultado_file = os.path.join(CAMINHO_REDE, f"resultado_comando_{MAQUINA_ATUAL}_{int(time.time())}.txt")
                with open(resultado_file, 'w', encoding='utf-8') as f:
                    f.write(f"Comando: {comando}\n")
                    f.write(f"Return code: {resultado.returncode}\n")
                    f.write(f"Saída:\n{resultado.stdout}\n")
                    if resultado.stderr:
                        f.write(f"Erros:\n{resultado.stderr}\n")
                        
                print(f"⚙️ Resultado salvo em: {resultado_file}")
        except Exception as e:
            print(f"❌ Erro executar comando: {e}")
    
    def _comando_testar_conectividade(self, parametros):
        """Testa conectividade com rede e serviços"""
        print("🌐 Recebido comando: TESTAR CONECTIVIDADE")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            resultados = []
            
            if os.path.exists(CAMINHO_REDE):
                resultados.append("✅ Acesso à rede: OK")
            else:
                resultados.append("❌ Acesso à rede: FALHA")
            
            try:
                test_file = os.path.join(CAMINHO_REDE, f"test_{int(time.time())}.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                resultados.append("✅ Escrita na rede: OK")
            except:
                resultados.append("❌ Escrita na rede: FALHA")
            
            arquivos_locais = [
                self.data_manager.csv_path,
                self.data_manager.users_path,
                self.data_manager.log_path
            ]
            for arquivo in arquivos_locais:
                if os.path.exists(arquivo):
                    resultados.append(f"✅ {os.path.basename(arquivo)}: OK")
                else:
                    resultados.append(f"❌ {os.path.basename(arquivo)}: FALHA")
            
            resultado_file = os.path.join(CAMINHO_REDE, f"teste_conectividade_{MAQUINA_ATUAL}_{int(time.time())}.txt")
            with open(resultado_file, 'w', encoding='utf-8') as f:
                f.write("TESTE DE CONECTIVIDADE\n")
                f.write(f"Máquina: {MAQUINA_ATUAL}\n")
                f.write(f"Data: {datetime.datetime.now()}\n\n")
                f.write("\n".join(resultados))
            
            print(f"🌐 Resultados salvos em: {resultado_file}")
        except Exception as e:
            print(f"❌ Erro testar conectividade: {e}")
    
    def _comando_obter_logs(self, parametros):
        """Obtém e envia logs do sistema"""
        print("📋 Recebido comando: OBTER LOGS")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            logs_file = os.path.join(CAMINHO_REDE, f"logs_{MAQUINA_ATUAL}_{int(time.time())}.txt")
            
            with open(logs_file, 'w', encoding='utf-8') as f:
                f.write("LOGS DO SISTEMA\n")
                f.write(f"Máquina: {MAQUINA_ATUAL}\n")
                f.write(f"Data: {datetime.datetime.now()}\n")
                f.write("="*50 + "\n\n")
                
                if self.data_manager.df_log is not None and len(self.data_manager.df_log) > 0:
                    f.write("ÚLTIMAS AÇÕES:\n")
                    for _, log in self.data_manager.df_log.tail(100).iterrows():
                        f.write(f"{log['data_hora']} | {log['usuario']} | {log['acao']} | {log['detalhes']}\n")
                else:
                    f.write("Nenhum log disponível\n")
                
                f.write("\n" + "="*50 + "\n")
                f.write("COMANDOS EXECUTADOS:\n")
                for cmd in self.comandos_executados[-20:]:
                    f.write(f"{cmd['timestamp']} | {cmd['acao']} (ID: {cmd['id']})\n")
            
            print(f"📋 Logs salvos em: {logs_file}")
        except Exception as e:
            print(f"❌ Erro obter logs: {e}")
    
    def _comando_diagnostico_completo(self, parametros):
        """Executa diagnóstico completo do sistema"""
        print("🔧 Recebido comando: DIAGNÓSTICO COMPLETO")
        try:
            if not self.machine_config or not self.data_manager:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            CONFIG_SIZE = self.machine_config.obter_configuracao_size()
            config_lote = self.batch_config.obter_configuracao_lote()
            
            diagnostico = {
                'timestamp': datetime.datetime.now().isoformat(),
                'maquina': MAQUINA_ATUAL,
                'sistema': {
                    'cpu_usage': psutil.cpu_percent(interval=1),
                    'memory_usage': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent,
                    'processos_ativos': len(psutil.pids())
                },
                'rede': {
                    'hostname': socket.gethostname(),
                    'ip': self._obter_ip_local(),
                    'conectado_rede': os.path.exists(CAMINHO_REDE)
                },
                'aplicacao': {
                    'maquina_configurada': MAQUINA_ATUAL,
                    'size_configurado': CONFIG_SIZE['size'],
                    'lote_ativo': config_lote.get('lote', ''),
                    'caixa_atual': config_lote.get('caixa_atual', 0),
                    'total_caixas': config_lote.get('total_caixas', 0),
                    'comunicacao_ativa': self.executando_comandos,
                    'comandos_executados': len(self.comandos_executados)
                },
                'dados': {
                    'registros_producao': len(self.data_manager.df) if self.data_manager.df is not None else 0,
                    'usuarios_cadastrados': len(self.data_manager.df_users) if self.data_manager.df_users is not None else 0,
                    'logs_sistema': len(self.data_manager.df_log) if self.data_manager.df_log is not None else 0
                }
            }
            
            diag_file = os.path.join(CAMINHO_REDE, f"diagnostico_{MAQUINA_ATUAL}_{int(time.time())}.json")
            with open(diag_file, 'w', encoding='utf-8') as f:
                json.dump(diagnostico, f, indent=2, ensure_ascii=False)
            
            print(f"🔧 Diagnóstico salvo em: {diag_file}")
        except Exception as e:
            print(f"❌ Erro diagnóstico: {e}")
    
    def _comando_limpar_cache(self, parametros):
        """Limpa cache e arquivos temporários"""
        print("🧹 Recebido comando: LIMPAR CACHE")
        try:
            from config.settings import CAMINHO_LOCAL
            temp_dir = CAMINHO_LOCAL
            arquivos_removidos = 0
            
            for file in os.listdir(temp_dir):
                if file.endswith('.tmp') or file.endswith('.log'):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                        arquivos_removidos += 1
                    except:
                        pass
            
            print(f"🧹 Cache limpo: {arquivos_removidos} arquivos removidos")
        except Exception as e:
            print(f"❌ Erro limpar cache: {e}")
    
    def _comando_capturar_tela(self, parametros):
        """Captura a tela da máquina remota"""
        print("📸 Recebido comando: CAPTURAR TELA")
        try:
            if not self.machine_config:
                return
                
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Tentar salvar na rede primeiro, depois local
            screenshot_file_rede = os.path.join(CAMINHO_REDE, f"screenshot_{MAQUINA_ATUAL}_{timestamp}.png")
            from config.settings import CAMINHO_LOCAL
            screenshot_file_local = os.path.join(CAMINHO_LOCAL, f"screenshot_{MAQUINA_ATUAL}_{timestamp}.png")
            
            screenshot_file = screenshot_file_rede if os.path.exists(CAMINHO_REDE) else screenshot_file_local
            
            # Método 1: Tentar com pyautogui (mais confiável)
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_file)
                print(f"📸 Screenshot salvo (pyautogui): {screenshot_file}")
                return
            except ImportError:
                print("⚠️ pyautogui não disponível, tentando método alternativo...")
            except Exception as e:
                print(f"⚠️ Erro com pyautogui: {e}")
            
            # Método 2: Fallback para Windows usando PIL + win32gui
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save(screenshot_file)
                print(f"📸 Screenshot salvo (PIL): {screenshot_file}")
                return
            except ImportError:
                print("⚠️ PIL não disponível, tentando PowerShell...")
            except Exception as e:
                print(f"⚠️ Erro com PIL: {e}")
            
            # Método 3: Fallback para PowerShell (Windows)
            try:
                import subprocess
                # Usar caminho absoluto para evitar problemas com executável
                screenshot_file_abs = os.path.abspath(screenshot_file)
                
                ps_script = f"""
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Drawing
                $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
                $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
                $graphic = [System.Drawing.Graphics]::FromImage($bitmap)
                $graphic.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bitmap.Size)
                $bitmap.Save('{screenshot_file_abs}')
                $graphic.Dispose()
                $bitmap.Dispose()
                Write-Host 'Screenshot capturado com sucesso'
                """
                
                resultado = subprocess.run(
                    ["powershell", "-Command", ps_script], 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
                
                if resultado.returncode == 0 and os.path.exists(screenshot_file):
                    print(f"📸 Screenshot salvo (PowerShell): {screenshot_file}")
                else:
                    print(f"❌ Erro PowerShell: {resultado.stderr}")
                    
            except Exception as e:
                print(f"❌ Erro PowerShell: {e}")
                
            # Método 4: Último recurso - criar arquivo de texto indicando tentativa
            try:
                info_file = screenshot_file.replace('.png', '_info.txt')
                with open(info_file, 'w', encoding='utf-8') as f:
                    f.write(f"Tentativa de captura de tela\n")
                    f.write(f"Máquina: {MAQUINA_ATUAL}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Status: Métodos de captura não disponíveis\n")
                print(f"📝 Arquivo de informação criado: {info_file}")
            except Exception as e:
                print(f"❌ Erro criar arquivo info: {e}")
                
        except Exception as e:
            print(f"❌ Erro geral capturar tela: {e}")


# Instância global
sistema_comunicacao = SistemaComunicacao()
