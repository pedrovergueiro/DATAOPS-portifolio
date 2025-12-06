"""Sistema de Comunicação em Tempo Real - 1ms"""

import threading
import time
import os
import json
import datetime
import uuid
import socket
import psutil
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
            return
            
        self.executando_comandos = True
        self.thread_comandos = threading.Thread(target=self._loop_comunicacao, daemon=True)
        self.thread_comandos.start()
        print("🔗 Sistema de comunicação iniciado (1ms)")
        
    def parar_sistema_comunicacao(self):
        """Para sistema de comunicação"""
        self.executando_comandos = False
        print("🔗 Sistema de comunicação parado")
        
    def _loop_comunicacao(self):
        """Loop principal de comunicação - ENVIA STATUS E VERIFICA COMANDOS A CADA 1ms"""
        contador = 0
        while self.executando_comandos:
            try:
                # ENVIAR STATUS A CADA 1ms (1000x por segundo)
                self._enviar_status_maquina()
                
                # VERIFICAR COMANDOS A CADA 1ms
                self._verificar_comandos()
                
                time.sleep(0.001)  # 1ms
                contador += 1
                
                # Log a cada 10000 iterações (10 segundos)
                if contador % 10000 == 0:
                    print(f"🔗 Comunicação ativa - {contador} ciclos (1ms cada) - Status enviado {contador} vezes")
                
            except Exception as e:
                print(f"⚠️ Erro comunicação: {e}")
                time.sleep(0.001)
                
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
        """Verifica se há comandos para executar - A CADA 1ms"""
        if not self.machine_config:
            return
            
        try:
            MAQUINA_ATUAL = self.machine_config.obter_configuracao_maquina()
            comando_file = os.path.join(CAMINHO_REDE, f"comando_maq_{MAQUINA_ATUAL}.json")
            
            if os.path.exists(comando_file):
                time.sleep(0.001)
                
                with open(comando_file, 'r', encoding='utf-8') as f:
                    comando_data = json.load(f)
                
                comando_id = comando_data.get('id', '')
                if comando_id and comando_id not in self.comandos_ativos:
                    self.comandos_ativos[comando_id] = True
                    
                    # Executar comando
                    self._executar_comando(comando_data)
                    
                    self.comandos_executados.append({
                        'id': comando_id,
                        'acao': comando_data.get('acao', ''),
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                    
                    if len(self.comandos_executados) > 50:
                        self.comandos_executados = self.comandos_executados[-50:]
                
                # Remover arquivo de comando após execução
                try:
                    os.remove(comando_file)
                    print(f"✅ Comando executado: {comando_data.get('acao', 'N/A')}")
                except:
                    pass
                
        except:
            pass
            
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
        if parametros.get('forcar', False):
            os._exit(0)
        else:
            if self.root_ref:
                self.root_ref.quit()
    
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
        python = sys.executable
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
            screenshot_file = os.path.join(CAMINHO_REDE, f"screenshot_{MAQUINA_ATUAL}_{timestamp}.png")
            
            # Tentar com pyautogui primeiro
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_file)
                print(f"📸 Screenshot salvo: {screenshot_file}")
            except ImportError:
                # Fallback para Windows
                import subprocess
                ps_script = f"""
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Drawing
                $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
                $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
                $graphic = [System.Drawing.Graphics]::FromImage($bitmap)
                $graphic.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bitmap.Size)
                $bitmap.Save('{screenshot_file}')
                $graphic.Dispose()
                $bitmap.Dispose()
                """
                subprocess.run(["powershell", "-Command", ps_script], timeout=30)
                print(f"📸 Screenshot salvo (fallback): {screenshot_file}")
                
        except Exception as e:
            print(f"❌ Erro capturar tela: {e}")


# Instância global
sistema_comunicacao = SistemaComunicacao()
