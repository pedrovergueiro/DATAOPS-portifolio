"""Sistema de identificação de máquina"""

import uuid
import socket
import psutil
import os
import json
import datetime
from config.settings import CAMINHO_LOCAL

def gerar_id_computador_avancado():
    """Gera ID único baseado em múltiplos componentes de hardware"""
    try:
        info_parts = []
        
        mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,8*6,8)][::-1])
        info_parts.append(f"MAC:{mac_addr}")
        
        hostname = socket.gethostname()
        info_parts.append(f"HOST:{hostname}")
        
        try:
            ip_addr = socket.gethostbyname(hostname)
            info_parts.append(f"IP:{ip_addr}")
        except:
            pass
            
        try:
            cpu_info = psutil.cpu_freq()
            if cpu_info:
                info_parts.append(f"CPU:{int(cpu_info.max)}")
        except:
            pass
            
        try:
            mem_info = psutil.virtual_memory()
            info_parts.append(f"RAM:{int(mem_info.total / (1024**3))}GB")
        except:
            pass
            
        try:
            disk_info = psutil.disk_usage('/')
            info_parts.append(f"DISK:{int(disk_info.total / (1024**3))}GB")
        except:
            pass
        
        unique_string = "_".join(info_parts)
        machine_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))
        
        info_detalhada = {
            'id_maquina': machine_id,
            'hostname': hostname,
            'mac_address': mac_addr,
            'timestamp_criacao': datetime.datetime.now().isoformat(),
            'informacoes': info_parts
        }
        
        id_file = os.path.join(CAMINHO_LOCAL, "identificacao_maquina.json")
        with open(id_file, 'w', encoding='utf-8') as f:
            json.dump(info_detalhada, f, indent=2, ensure_ascii=False)
            
        return machine_id
        
    except Exception as e:
        print(f"❌ Erro ao gerar ID avançado: {e}")
        return str(uuid.uuid4())
