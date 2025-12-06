# 💻 MANUAL DO PAINEL DESENVOLVEDOR

## 🔐 Acesso

**Senha padrão:** `010524Np@`

Para acessar: Clique em "💻 Painel Desenvolvedor" na tela principal

---

## 📑 ABAS DO PAINEL

### ⚡ 1. COMANDOS RÁPIDOS

Botões para executar ações comuns rapidamente:

#### 🔄 Reiniciar Sistema
- Reinicia completamente o aplicativo
- **Quando usar:** Após mudanças de configuração

#### 🧹 Limpar Cache
- Remove arquivos temporários (.tmp, .cache)
- **Quando usar:** Sistema lento ou erros estranhos

#### 💾 Backup Completo
- Cria backup de TODOS os dados
- Salva em: `backup_MAQUINA_DATA/`
- **Quando usar:** Antes de mudanças importantes

#### 📊 Exportar Dados
- Exporta dados de produção para Excel
- Escolha a pasta de destino
- **Quando usar:** Para análise externa

#### 🔍 Verificar Integridade
- Verifica se arquivos estão OK
- Detecta problemas nos dados
- **Quando usar:** Suspeita de corrupção

#### 📁 Abrir Pasta Local
- Abre pasta onde dados estão salvos localmente
- **Quando usar:** Verificar arquivos manualmente

#### 🌐 Abrir Pasta Rede
- Abre pasta da rede (Z:\)
- **Quando usar:** Verificar sincronização

#### 🔧 Reparar Arquivos
- Tenta corrigir arquivos corrompidos
- Recria arquivos faltantes
- **Quando usar:** Erros ao carregar dados

#### 📋 Copiar ID Máquina
- Copia ID único do computador
- **Quando usar:** Suporte técnico

#### 🗑️ Limpar Logs Antigos
- Remove logs com mais de 30 dias
- Libera espaço em disco
- **Quando usar:** Disco cheio

#### 📤 Sincronizar Rede
- Força sincronização com rede
- **Quando usar:** Dados não aparecem na rede

#### 🔐 Resetar Senhas
- ⚠️ CUIDADO: Reseta TODAS as senhas
- **Quando usar:** Emergência

---

### 🌐 2. CONTROLE REMOTO

Controle outras máquinas remotamente pela rede.

#### Como Usar:

1. **Clique em "🔍 Descobrir Máquinas"**
   - Lista todas as máquinas conectadas
   - Mostra status em tempo real

2. **Selecione uma máquina da lista**
   - Clique na máquina desejada

3. **Escolha um comando:**

   - **🔄 Reiniciar App** - Reinicia o aplicativo na máquina
   - **🛑 Fechar App** - Fecha o aplicativo
   - **🚀 Abrir App** - Abre/restaura o aplicativo
   - **📊 Coletar Dados** - Coleta informações da máquina
   - **💾 Fazer Backup** - Cria backup remoto
   - **🔍 Diagnóstico** - Diagnóstico completo do sistema
   - **🌐 Testar Rede** - Testa conectividade
   - **📋 Obter Logs** - Baixa logs da máquina
   - **🧹 Limpar Cache** - Limpa cache remoto
   - **📸 Capturar Tela** - Tira screenshot da máquina

4. **Verifique o resultado no Console de Saída**

#### ⚠️ IMPORTANTE:
- Máquina precisa estar com aplicativo aberto
- Precisa ter acesso à rede (Z:\)
- Comandos são executados em até 1 segundo

---

### ⚙️ 3. CONFIGURAÇÕES

#### 🔧 Configuração da Máquina

**Máquinas Disponíveis:**
- **201 a 214** - Máquinas de produção
- **DESENVOLVEDOR** - Modo desenvolvedor
- **COORDENADOR** - Acesso administrativo
- **ENCARREGADO** - Supervisão
- **ANALISTA** - Análise de dados
- **OPERADOR** - Operação básica

**Como Alterar:**
1. Selecione a nova máquina no dropdown
2. Clique em "💾 Salvar Configuração"
3. Reinicie o sistema

**O que muda:**
- Nome da máquina
- Size padrão
- Peso padrão
- Permissões

#### 📦 Configuração de Lote

**Campos:**
- **Lote:** Número/código do lote (aceita letras e números)
- **Caixa Atual:** Número da caixa em produção
- **Total:** Total de caixas do lote

**Como Configurar:**
1. Preencha os campos
2. Clique em "💾 Salvar Lote"
3. Janela de registro atualiza automaticamente

**Quando Configurar:**
- Início de novo lote
- Mudança de lote
- Correção de número de caixa

---

### 📊 4. MONITORAMENTO

Visualize estatísticas em tempo real do sistema.

**Informações Exibidas:**
- 🏭 Máquina atual
- 📏 Size e peso configurados
- 📦 Lote e caixa atual
- 📊 Total de registros de produção
- 👥 Usuários cadastrados
- 📝 Logs do sistema
- 📁 Caminhos de arquivos
- 🔗 Status de conexão com rede
- 🆔 ID do computador
- ⏰ Última atualização

**Botão "🔄 Atualizar Estatísticas":**
- Atualiza todas as informações
- Use após fazer mudanças

---

### 🛠️ 5. FERRAMENTAS

Ferramentas avançadas para administração.

#### 👥 Gerenciar Usuários
- Adicionar novos usuários
- Editar usuários existentes
- Remover usuários
- Alterar senhas

#### 📊 Abrir Dashboard
- Abre dashboard em janela separada
- Visualização de dados em gráficos
- Pode ser executável separado

#### 🗂️ Explorar Arquivos
- Abre pasta de dados no Windows Explorer
- Acesso rápido aos arquivos

#### 📝 Editor de Configurações
- Edita configurações avançadas
- Use com cuidado!

#### 🔍 Buscar Registros
- Busca registros específicos
- Filtros avançados

#### 📤 Importar Dados
- Importa dados de arquivos externos
- Formatos: CSV, Excel

#### 🔄 Resetar Sistema
- ⚠️ CUIDADO: Reseta TUDO
- Volta configurações ao padrão
- **Use apenas em emergência**

#### 📋 Gerar Relatório
- Gera relatório completo
- Exporta para PDF/Excel

---

## 🎯 CASOS DE USO COMUNS

### Caso 1: Máquina Nova
1. Abrir Painel Desenvolvedor
2. Ir em "Configurações"
3. Selecionar número da máquina (ex: 205)
4. Salvar e reiniciar

### Caso 2: Problema na Rede
1. Abrir Painel Desenvolvedor
2. Ir em "Comandos Rápidos"
3. Clicar em "🌐 Abrir Pasta Rede"
4. Verificar se consegue acessar
5. Se não, usar "📤 Sincronizar Rede"

### Caso 3: Controlar Máquina Remota
1. Abrir Painel Desenvolvedor
2. Ir em "Controle Remoto"
3. Clicar em "🔍 Descobrir Máquinas"
4. Selecionar máquina
5. Escolher comando (ex: "📊 Coletar Dados")
6. Verificar resultado no console

### Caso 4: Fazer Backup
1. Abrir Painel Desenvolvedor
2. Ir em "Comandos Rápidos"
3. Clicar em "💾 Backup Completo"
4. Aguardar confirmação
5. Backup salvo em pasta local

### Caso 5: Exportar Dados
1. Abrir Painel Desenvolvedor
2. Ir em "Comandos Rápidos"
3. Clicar em "📊 Exportar Dados"
4. Escolher pasta de destino
5. Arquivo Excel criado

---

## ⚠️ AVISOS IMPORTANTES

### 🔴 NÃO FAÇA:
- ❌ Não use "Resetar Sistema" sem backup
- ❌ Não altere configurações sem anotar valores anteriores
- ❌ Não envie comandos remotos sem necessidade
- ❌ Não delete arquivos manualmente da pasta

### 🟢 SEMPRE FAÇA:
- ✅ Faça backup antes de mudanças importantes
- ✅ Anote configurações antes de alterar
- ✅ Teste em uma máquina antes de aplicar em todas
- ✅ Verifique integridade após mudanças

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### Problema: "Sem acesso à rede"
**Solução:**
1. Verificar cabo de rede
2. Testar acesso ao Z:\
3. Usar modo local temporariamente

### Problema: "Erro ao salvar dados"
**Solução:**
1. Verificar espaço em disco
2. Reparar arquivos
3. Fazer backup e resetar

### Problema: "Comando remoto não funciona"
**Solução:**
1. Verificar se máquina está online
2. Verificar acesso à rede
3. Tentar descobrir máquinas novamente

### Problema: "Sistema lento"
**Solução:**
1. Limpar cache
2. Limpar logs antigos
3. Verificar espaço em disco

---

## 📞 SUPORTE

**Em caso de dúvidas:**
1. Consulte este manual
2. Verifique logs do sistema
3. Faça backup antes de tentar correções
4. Anote mensagens de erro

**Informações úteis para suporte:**
- ID da máquina (copiar do painel)
- Mensagem de erro completa
- O que estava fazendo quando ocorreu
- Última mudança feita no sistema

---

## 📝 NOTAS

- **Console de Saída:** Mostra resultado de cada ação
- **Timestamp:** Cada ação tem hora registrada
- **Logs:** Todas as ações são registradas
- **Backup:** Sempre faça backup antes de mudanças críticas

---

**Versão do Manual:** 1.0  
**Última Atualização:** Dezembro 2024  
**Sistema:** Coletor de Produção Industrial
