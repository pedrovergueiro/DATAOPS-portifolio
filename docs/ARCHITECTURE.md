# 🏗️ Arquitetura do Sistema

## Visão Geral

O sistema é composto por **dois aplicativos principais** que trabalham de forma integrada:

1. **Sistema de Coleta** (`main.py`) - Coleta dados de produção em tempo real
2. **Dashboard de Análise** (`dash.py`) - Visualiza e analisa os dados coletados

## 🔄 Alinhamento de Dados

### Garantia de Compatibilidade 100%

Ambos os aplicativos compartilham as mesmas configurações e estruturas de dados:

```python
# Configurações compartilhadas
from config.settings import CAMINHO_REDE, CSV_FILE
from config.constants import MAQUINAS_VALIDAS, COLUNAS_DADOS
```

### Estrutura de Dados Unificada

**Colunas de Dados (COLUNAS_DADOS):**
```python
[
    'maquina',          # Identificação da máquina (201-214)
    'rej1_defect',      # Defeito da rejeição 1
    'rej1_local',       # Local da rejeição 1 (Cap/Body)
    'rej2_defect',      # Defeito da rejeição 2
    'rej2_local',       # Local da rejeição 2
    'rej3_defect',      # Defeito da rejeição 3
    'rej3_local',       # Local da rejeição 3
    'percent_cam_d',    # Percentual CAM-D
    'percent_cam_w',    # Percentual CAM-W
    'data_hora',        # Timestamp do registro
    'origem',           # Origem do dado (coletor/manual)
    'justificativa',    # Justificativa (se manual)
    'usuario_reg',      # Usuário que registrou
    'lote',             # Número do lote
    'numero_caixa',     # Número da caixa
    'size',             # Tamanho do produto
    'peso'              # Peso do produto
]
```

**Máquinas Válidas (MAQUINAS_VALIDAS):**
```python
['201', '202', '203', '204', '205', '206', '207', 
 '208', '209', '210', '211', '212', '213', '214']
```

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA DE COLETA                        │
│                      (main.py)                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Operador registra produção                             │
│  2. Dados validados e formatados                           │
│  3. Salvos em CSV (dados_producao.csv)                     │
│  4. Auditoria registrada (SHA-256)                         │
│                                                             │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ CSV compartilhado
                   │ (dados_producao.csv)
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  DASHBOARD DE ANÁLISE                       │
│                      (dash.py)                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Lê dados do CSV                                        │
│  2. Valida estrutura (mesmas colunas)                      │
│  3. Filtra máquinas válidas                                │
│  4. Gera gráficos e análises                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Componentes Compartilhados

### 1. Configurações (`config/`)

**settings.py:**
- `CAMINHO_REDE` - Caminho da rede compartilhada
- `CAMINHO_LOCAL` - Caminho local de fallback
- `CSV_FILE` - Nome do arquivo de dados
- `VERSION` - Versão do sistema

**constants.py:**
- `TABELA_SIZES` - Configuração de máquinas
- `MAQUINAS_VALIDAS` - Lista de máquinas válidas
- `COLUNAS_DADOS` - Estrutura de dados
- `COLUNAS_USUARIOS` - Estrutura de usuários

### 2. Modelos (`models/`)

**machine.py:**
- Gerenciamento de configuração de máquinas
- Persistência de configurações

**batch.py:**
- Gerenciamento de lotes
- Controle de caixas

**user.py:**
- Gerenciamento de usuários
- Autenticação e autorização

### 3. Camada de Dados (`data/`)

**manager.py:**
- Gerenciamento centralizado de dados
- Carregamento e salvamento
- Validação de estrutura

**loader.py:**
- Carregamento seguro de CSV
- Tratamento de erros
- Fallback local/rede

**saver.py:**
- Salvamento atômico
- Backup automático
- Sincronização rede

## 🔐 Sistema de Auditoria

### Registro Imutável

Todas as ações são registradas com:
- **Hash SHA-256** - Garantia de integridade
- **Timestamp** - Data e hora exata
- **Usuário** - Quem executou a ação
- **Dados antes/depois** - Diff completo
- **IP e Hostname** - Rastreabilidade

### Arquivo de Auditoria

```json
{
  "versao": "1.0",
  "criado_em": "2025-12-05T10:00:00",
  "registros": [
    {
      "id": 1,
      "timestamp": "2025-12-05T10:30:00",
      "acao": "INSERT_PRODUCAO",
      "usuario": "operador1",
      "detalhes": "Inserção de dados de produção",
      "dados_depois": {...},
      "hash": "abc123..."
    }
  ]
}
```

## 🌐 Comunicação em Tempo Real

### Sistema de Status (1ms)

```python
# Loop de comunicação - 1000x por segundo
while executando:
    enviar_status_maquina()    # Status atual
    verificar_comandos()        # Comandos pendentes
    time.sleep(0.001)          # 1ms
```

### Arquivos de Status

**status_maq_{MAQUINA}.json:**
```json
{
  "maquina": "201",
  "timestamp": "2025-12-05T10:30:00",
  "status": "online",
  "recursos": {
    "cpu": 25.5,
    "memoria": 45.2,
    "disco": 60.1
  },
  "online": true
}
```

## 📈 Escalabilidade

### Suporte a Múltiplas Máquinas

- ✅ Cada máquina executa o coletor independentemente
- ✅ Dados salvos em arquivo CSV compartilhado
- ✅ Dashboard lê dados de todas as máquinas
- ✅ Sincronização automática via rede

### Alta Disponibilidade

- ✅ Fallback local se rede indisponível
- ✅ Salvamento dual (local + rede)
- ✅ Recuperação automática de erros
- ✅ Backup automático de dados

## 🔄 Sincronização

### Estratégia de Sincronização

1. **Escrita:**
   - Salva localmente primeiro (rápido)
   - Tenta salvar na rede (se disponível)
   - Mantém ambas as cópias atualizadas

2. **Leitura:**
   - Tenta ler da rede primeiro
   - Fallback para local se rede indisponível
   - Valida estrutura de dados

3. **Conflitos:**
   - Timestamp mais recente prevalece
   - Auditoria registra todas as mudanças
   - Backup automático antes de sobrescrever

## 🎯 Garantias de Integridade

### Validações Implementadas

1. **Estrutura de Dados:**
   - Todas as colunas obrigatórias presentes
   - Tipos de dados corretos
   - Valores dentro dos limites

2. **Máquinas:**
   - Apenas máquinas válidas (201-214)
   - Configuração correta de size/peso
   - ID único por máquina

3. **Auditoria:**
   - Hash SHA-256 em cada registro
   - Verificação de integridade
   - Arquivo somente leitura

4. **Usuários:**
   - Autenticação obrigatória
   - Autorização por perfil
   - Logs de acesso

## 📊 Performance

### Métricas

| Componente | Métrica | Valor |
|------------|---------|-------|
| Comunicação | Latência | 1ms |
| Comunicação | Throughput | 1000 req/s |
| Salvamento | Tempo médio | <100ms |
| Carregamento | Tempo médio | <500ms |
| Dashboard | Atualização | <2s |

### Otimizações

- ✅ Threading para operações paralelas
- ✅ Caching de dados frequentes
- ✅ Lazy loading de componentes
- ✅ Batch processing quando possível

## 🔍 Monitoramento

### Logs do Sistema

- ✅ Todas as ações registradas
- ✅ Erros capturados e logados
- ✅ Performance monitorada
- ✅ Recursos do sistema rastreados

### Diagnóstico

```python
# Diagnóstico automático na inicialização
diagnostico_inicial()
# - Verifica Python
# - Verifica diretórios
# - Testa acesso à rede
# - Valida arquivos
```

## 🚀 Deployment

### Requisitos

- Python 3.8+
- Acesso à rede compartilhada
- Permissões de leitura/escrita
- Bibliotecas listadas em requirements.txt

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/pedrovergueiro/DATAOPS-portifolio.git

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure arquivos iniciais
cp config_maquina.json.example config_maquina.json
cp usuarios.csv.example usuarios.csv

# 4. Execute o coletor
python main.py

# 5. Execute o dashboard (em outra máquina/terminal)
python dash.py
```

## 📝 Manutenção

### Backup

- ✅ Backup automático antes de modificações
- ✅ Arquivos .bak mantidos
- ✅ Auditoria nunca deletada

### Atualização

- ✅ Versionamento semântico
- ✅ Changelog mantido
- ✅ Migração de dados quando necessário

---

**Versão:** 8.0  
**Data:** 05/12/2025  
**Status:** ✅ Produção
