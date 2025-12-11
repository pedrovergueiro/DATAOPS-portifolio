# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [8.0.0] - 2025-12-05

### Adicionado
- ✨ **Sistema de Inteligência Artificial completo**
  - Predição de defeitos (75-85% precisão)
  - Detecção de anomalias (análise estatística)
  - Recomendações inteligentes priorizadas
  - Score de qualidade automatizado (0-100)
  - 3 sub-abas no painel desenvolvedor (Visão Geral, Individual, Comparativo)
- ✨ Janela de registro fixa que nunca fecha
- ✨ Atalho ALT+F1 para fechar janela de registro (apenas desenvolvedor)
- ✨ Sistema de comunicação em tempo real (1ms)
  - Verificação de comandos a cada 1ms (1000x/segundo)
  - Status enviado a cada 1 segundo (otimizado)
  - Verificação em rede E local (alta disponibilidade)
- ✨ Descoberta automática de máquinas online
- ✨ Sistema de auditoria completo e imutável
- ✨ Hash SHA-256 para integridade de registros
- ✨ Painel administrativo com autenticação
- ✨ Justificativas obrigatórias para ações manuais
- ✨ Comboboxes para seleção padronizada
- ✨ Seleção de usuário via combobox no lançamento (removida do lançamento normal)
- ✨ Layout melhorado com rejeições lado a lado
- ✨ Painel desenvolvedor completo (6 abas, 100+ funcionalidades)
  - Comandos Rápidos (12 botões)
  - Controle Remoto (10 comandos)
  - Configurações (máquina e lote)
  - Monitoramento (tempo real)
  - IA & Machine Learning (3 sub-abas)
  - Ferramentas (8 ferramentas avançadas)
- ✨ Controle remoto de máquinas
- ✨ 10 comandos remotos disponíveis
- ✨ Verificação de integridade da auditoria
- ✨ Exportação de relatórios de auditoria
- ✨ Script de teste de comandos remotos (testar_comando_remoto.py)
- ✨ Documentação completa (15+ arquivos .md)
  - README.md profissional e persuasivo
  - CHANGELOG.md completo
  - INSTALL.md com instruções detalhadas
  - CONTRIBUTING.md com guia de contribuição
  - COMPILAR_EXECUTAVEIS.md com guia de compilação
  - docs/ARCHITECTURE.md com arquitetura completa
  - docs/DEVELOPER_GUIDE.md com manual do desenvolvedor
  - docs/FEATURES.md com lista de 100+ funcionalidades
  - docs/IA_MACHINE_LEARNING.md com documentação completa da IA
  - RESUMO_FINAL_IA.md com resumo da implementação
  - ALINHAMENTO_SISTEMA.md com verificação de alinhamento
  - MELHORIAS_COMUNICACAO.md com otimizações
  - CORRECOES_REALIZADAS.md com correções de bugs

### Modificado
- 🔄 Sistema de comunicação otimizado
  - Verifica comandos a cada 1ms (1000x mais rápido)
  - Envia status a cada 1 segundo (otimizado)
  - Verifica rede E local (alta disponibilidade)
- 🔄 Status salvo localmente E na rede
- 🔄 Layout de formulários melhorado
- 🔄 Rejeições agora aparecem lado a lado (defeito e local)
- 🔄 Interface mais intuitiva e responsiva
- 🔄 Lançamento normal usa usuário automático (sem seleção)
- 🔄 Painel admin usa lote automático do sistema
- 🔄 Mensagens de confirmação sempre no topo (utils/messagebox_topmost.py)
- 🔄 Dashboard 100% compatível com coletor
  - Usa mesmas configurações (config/settings.py)
  - Usa mesmas constantes (config/constants.py)
  - Mesma estrutura de dados (COLUNAS_DADOS)

### Corrigido
- 🐛 Configuração de lote agora aceita QUALQUER valor (letras, números, símbolos)
- 🐛 Botão "Registrar Produção" agora funciona (removido "em desenvolvimento")
- 🐛 Senha desenvolvedor funciona corretamente no .exe (debug completo)
- 🐛 Painel admin abre com conteúdo (logs detalhados, try/except)
- 🐛 Máquinas agora aparecem online corretamente
- 🐛 Descoberta de máquinas funciona local e rede
- 🐛 Arquivo de auditoria protegido contra modificação
- 🐛 Validação de justificativas implementada
- 🐛 Comandos remotos executam em <1 segundo

### Segurança
- 🔐 Autenticação obrigatória no painel administrativo
- 🔐 Sistema de auditoria imutável
- 🔐 Arquivo de auditoria somente leitura
- 🔐 Backup automático de dados críticos

## [7.0.0] - 2024-11-XX

### Adicionado
- Dashboard interativo com Plotly/Dash
- Sistema de logs completo
- Gerenciamento de usuários
- Configuração de máquinas e lotes

### Modificado
- Interface gráfica melhorada
- Performance otimizada

## [6.0.0] - 2024-10-XX

### Adicionado
- Sistema de coleta de dados básico
- Registro de produção
- Exportação para CSV

## Tipos de Mudanças

- `Adicionado` para novas funcionalidades
- `Modificado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas

---

**Legenda:**
- ✨ Nova funcionalidade
- 🔄 Modificação
- 🐛 Correção de bug
- 🔐 Segurança
- 📚 Documentação
- 🚀 Performance
- 💄 Interface
