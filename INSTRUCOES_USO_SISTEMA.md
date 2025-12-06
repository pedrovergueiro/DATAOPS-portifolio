# 📖 INSTRUÇÕES DE USO DO SISTEMA

## 🚀 COMO INICIAR O SISTEMA

### 1. Executar o Sistema
```bash
python main.py
```

### 2. O que acontece ao iniciar:
- ✅ Sistema carrega configurações
- ✅ Verifica acesso à rede
- ✅ Inicia sistema de comunicação (1ms)
- ✅ Cria janela de registro FIXA (sempre visível)
- ✅ Abre janela principal do sistema

---

## 📝 JANELA DE REGISTRO FIXA

### Características:
- 🔒 **NUNCA FECHA** automaticamente
- 📌 Sempre visível sobre outras janelas
- 📍 Posicionada no canto superior direito
- 🚀 Botão "LANÇAR PRODUÇÃO" sempre acessível

### Como fechar (APENAS DESENVOLVEDOR):
1. Pressionar **ALT + F1**
2. Digitar senha de desenvolvedor: `010524Np@`
3. Janela será recriada automaticamente em 10 segundos

---

## 🌐 DESCOBERTA DE MÁQUINAS ONLINE

### Por que as máquinas não aparecem?

O sistema de comunicação precisa estar **RODANDO** para criar os arquivos de status.

### Como fazer as máquinas aparecerem:

#### PASSO 1: Verificar se o sistema está rodando
```python
# O sistema deve estar executando main.py
# Verificar no console se aparece:
# "🔗 Sistema de comunicação iniciado (1ms)"
```

#### PASSO 2: Aguardar alguns segundos
- O sistema envia status a cada 1ms
- Arquivos são criados automaticamente
- Aguarde 5-10 segundos após iniciar

#### PASSO 3: Abrir Painel Desenvolvedor
1. Janela principal → "💻 Painel Desenvolvedor"
2. Digitar senha: `010524Np@`
3. Ir para aba "🌐 Controle Remoto"
4. Clicar em "🔍 Descobrir Máquinas"

#### PASSO 4: Verificar máquinas encontradas
- Máquina atual SEMPRE deve aparecer com 🟢
- Outras máquinas aparecem se estiverem rodando o sistema
- Timestamp deve ser recente (últimos 30 segundos)

### Arquivos de Status Criados:

**Local (sempre criado):**
```
C:\Users\pedro\Documents\portifolio\DataOps\status_maq_{MAQUINA}.json
```

**Rede (se acessível):**
```
Z:\Pedro Vergueiro - melhoria continua\dataSETpfd\status_maq_{MAQUINA}.json
```

### Exemplo de arquivo de status:
```json
{
  "maquina": "201",
  "id_computador": "abc123...",
  "timestamp": "2025-12-05T22:30:00",
  "status": "online",
  "app_aberto": true,
  "ultima_acao": "22:30:00",
  "size": "#1",
  "peso": 0.000096,
  "lote": "LOTE123",
  "caixa_atual": 5,
  "total_caixas": 100,
  "recursos": {
    "cpu": 25.5,
    "memoria": 45.2,
    "disco": 60.1
  },
  "hostname": "MAQUINA-201",
  "ip": "192.168.1.100",
  "online": true
}
```

---

## 👔 PAINEL ADMINISTRATIVO

### Quem pode acessar:
- ✅ Coordenador
- ✅ Encarregado
- ✅ Desenvolvedor

### Como acessar:
1. Janela principal → "👔 Painel Administrativo"
2. Digitar usuário e senha
3. Sistema verifica permissões
4. Acesso liberado se autorizado

### 5 Abas Disponíveis:

#### ➕ ABA 1: INSERIR DADOS
- Formulário completo para inserção manual
- **Comboboxes** para seleção (evita erros de digitação):
  - Máquina (lista de máquinas disponíveis)
  - Rejeições (lista de defeitos padronizados)
  - Local (Cap/Body/Cap/Body/N/A)
- **Justificativa OBRIGATÓRIA** (mínimo 10 caracteres)
- Registro automático na auditoria

#### ✏️ ABA 2: EDITAR DADOS
- Busca por máquina e lote
- Visualização de registros existentes
- Edição com justificativa obrigatória
- Dados antes/depois salvos na auditoria

#### 🗑️ ABA 3: EXCLUIR DADOS
- Seleção de registros para exclusão
- Justificativa obrigatória
- Dados excluídos salvos na auditoria
- Confirmação dupla

#### 📋 ABA 4: AUDITORIA
- Visualização de todos os registros
- Verificação de integridade
- Exportação de relatórios
- Filtros por usuário e ação

#### 📤 ABA 5: EXPORTAR
- Exportação para Excel
- Registro na auditoria
- Seleção de período

---

## 🔐 SISTEMA DE AUDITORIA

### Características:
- 🔒 **IMUTÁVEL** - Não pode ser modificado
- 🔐 **Hash SHA-256** em cada registro
- 📝 Registra TODAS as ações
- 🛡️ Arquivo protegido (somente leitura)
- 💾 Backup automático

### Localização:
```
C:\Users\pedro\Documents\portifolio\DataOps\auditoria_producao.json
```

### Ações Auditadas:
- ✅ INSERT_PRODUCAO - Inserção de dados
- ✅ UPDATE_PRODUCAO - Edição de dados
- ✅ DELETE_PRODUCAO - Exclusão de dados
- ✅ EXPORT_DADOS - Exportação de dados
- ✅ ACESSO_PAINEL - Acesso a painéis

### Como Verificar Integridade:
1. Painel Administrativo → Aba "📋 Auditoria"
2. Clicar em "🔍 Verificar Integridade"
3. Sistema verifica hash de todos os registros
4. Resultado: ✅ Íntegro ou ❌ Comprometido

### Como Exportar Relatório:
1. Painel Administrativo → Aba "📋 Auditoria"
2. Clicar em "📄 Exportar Relatório"
3. Arquivo `.txt` é gerado com todos os registros
4. Localização: `relatorio_auditoria_{timestamp}.txt`

---

## 💻 PAINEL DESENVOLVEDOR

### Como acessar:
1. Janela principal → "💻 Painel Desenvolvedor"
2. Digitar senha: `010524Np@`
3. Painel completo é aberto

### 5 Abas Disponíveis:

#### ⚡ ABA 1: COMANDOS RÁPIDOS
12 comandos do sistema:
- 🔄 Reiniciar Sistema
- 🧹 Limpar Cache
- 💾 Backup Completo
- 📊 Exportar Dados
- 🔍 Verificar Integridade
- 📁 Abrir Pasta Local
- 🌐 Abrir Pasta Rede
- 🔧 Reparar Arquivos
- 📋 Copiar ID Máquina
- 🗑️ Limpar Logs Antigos
- 📤 Sincronizar Rede
- 🔐 Resetar Senhas

#### 🌐 ABA 2: CONTROLE REMOTO
10 comandos remotos:
- 🔄 Reiniciar App
- 🛑 Fechar App
- 🚀 Abrir App
- 📊 Coletar Dados
- 💾 Fazer Backup
- 🔍 Diagnóstico
- 🌐 Testar Rede
- 📋 Obter Logs
- 🧹 Limpar Cache
- 📸 Capturar Tela

**Como usar:**
1. Clicar em "🔍 Descobrir Máquinas"
2. Selecionar máquina na lista
3. Clicar no comando desejado
4. Comando é enviado via arquivo JSON
5. Máquina remota executa automaticamente

#### ⚙️ ABA 3: CONFIGURAÇÕES
- Alterar máquina
- Alterar size
- Configurar lote
- Salvar configurações

#### 📊 ABA 4: MONITORAMENTO
- Estatísticas do sistema
- Recursos (CPU, memória, disco)
- Total de registros
- Usuários cadastrados
- Logs do sistema

#### 🛠️ ABA 5: FERRAMENTAS
8 ferramentas avançadas:
- 👥 Gerenciar Usuários
- 📊 Abrir Dashboard
- 🗂️ Explorar Arquivos
- 📝 Editor de Configurações
- 🔍 Buscar Registros
- 📤 Importar Dados
- 🔄 Resetar Sistema
- 📋 Gerar Relatório

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### Problema 1: Máquinas não aparecem online

**Causa:** Sistema de comunicação não está rodando ou arquivos não foram criados

**Solução:**
1. Verificar se `main.py` está executando
2. Verificar no console: "🔗 Sistema de comunicação iniciado (1ms)"
3. Aguardar 5-10 segundos
4. Verificar se arquivo `status_maq_{MAQUINA}.json` existe no diretório local
5. Abrir Painel Desenvolvedor → Controle Remoto → Descobrir Máquinas

**Comando para verificar:**
```bash
dir status_maq_*.json
```

### Problema 2: Botão de registro não fecha

**Causa:** Comportamento esperado - botão NUNCA fecha

**Solução:**
- Usar atalho **ALT + F1**
- Digitar senha de desenvolvedor
- Botão será recriado em 10 segundos

### Problema 3: Justificativa não aceita

**Causa:** Justificativa muito curta ou vazia

**Solução:**
- Digitar pelo menos 10 caracteres
- Descrever claramente o motivo da ação
- Exemplo: "Correção de erro de digitação na caixa 45"

### Problema 4: Erro ao salvar auditoria

**Causa:** Arquivo protegido ou sem permissão

**Solução:**
1. Verificar permissões do arquivo
2. Executar como administrador
3. Verificar arquivo `.bak` (backup)
4. Contatar desenvolvedor

### Problema 5: Acesso negado ao painel administrativo

**Causa:** Usuário não tem permissão

**Solução:**
- Verificar tipo de usuário (deve ser Coordenador, Encarregado ou Desenvolvedor)
- Solicitar alteração de permissão ao desenvolvedor
- Verificar senha correta

---

## 📊 COMBOBOXES IMPLEMENTADOS

### Onde estão:
- ✅ Painel Administrativo → Inserir Dados
- ✅ Janela de Lançamento de Produção

### Campos com Combobox:

#### 1. Máquina
Lista de máquinas disponíveis:
- 201, 202, 203, 204, 205, 206, 207, 208, 209, 210
- 211, 212, 213, 214, 215, 216, 217, 218, 219, 220
- DESENVOLVEDOR, COORDENADOR, ENCARREGADO

#### 2. Rejeições (Defeitos)
Lista de defeitos padronizados:
- Amassada
- Apara Retida
- Barra Colada
- Cápsula Fina
- Dente
- Furo
- Rachada
- Short
- Suja
- N/A

#### 3. Local (Cap/Body)
Lista de locais:
- Cap
- Body
- Cap/Body
- N/A

### Vantagens:
- ✅ Evita erros de digitação
- ✅ Padroniza entrada de dados
- ✅ Mais rápido que digitar
- ✅ Reduz inconsistências

---

## 📈 ESTATÍSTICAS DO SISTEMA

### Performance:
- **Status:** 1000x por segundo (1ms)
- **Comandos:** 1000x por segundo (1ms)
- **Latência:** 1ms
- **Overhead:** Mínimo

### Segurança:
- **Hash SHA-256** em cada registro
- **Arquivo somente leitura**
- **Backup automático**
- **Justificativas obrigatórias**
- **Auditoria imutável**

### Código:
- **Linhas de código:** ~800 linhas novas
- **Arquivos novos:** 3
- **Arquivos modificados:** 3
- **Funcionalidades:** 15+

---

## ⚠️ AVISOS IMPORTANTES

### 1. Arquivo de Auditoria:
- ❌ **NUNCA DELETAR** `auditoria_producao.json`
- ❌ **NUNCA MODIFICAR** manualmente
- ✅ Apenas leitura via sistema
- ✅ Verificar integridade regularmente

### 2. Justificativas:
- ✅ Sempre fornecer justificativa clara
- ✅ Mínimo 10 caracteres
- ✅ Descrever motivo da ação
- ❌ Não usar justificativas genéricas

### 3. Atalho ALT+F1:
- 🔐 Apenas desenvolvedor deve saber
- 🔐 Requer senha
- 🔐 Janela recria automaticamente

### 4. Sistema de Comunicação:
- ✅ Deve estar sempre rodando
- ✅ Envia status a cada 1ms
- ✅ Verifica comandos a cada 1ms
- ❌ Não interromper o processo

---

## 📞 CONTATO

Em caso de dúvidas ou problemas:
- 📧 Contatar desenvolvedor
- 📋 Verificar logs do sistema
- 🔍 Consultar documentação

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Antes de usar o sistema, verificar:

- [ ] Sistema está executando (`python main.py`)
- [ ] Console mostra "🔗 Sistema de comunicação iniciado (1ms)"
- [ ] Janela de registro FIXA está visível
- [ ] Arquivo `status_maq_{MAQUINA}.json` existe
- [ ] Acesso à rede está funcionando
- [ ] Usuários estão cadastrados
- [ ] Arquivo de auditoria existe

---

**Versão:** 1.0 FINAL  
**Data:** Dezembro 2025  
**Status:** ✅ PRONTO PARA USO
