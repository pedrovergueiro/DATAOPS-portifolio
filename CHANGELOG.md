# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [8.0.0] - 2025-12-05

### Adicionado
- ✨ Janela de registro fixa que nunca fecha
- ✨ Atalho ALT+F1 para fechar janela de registro (apenas desenvolvedor)
- ✨ Sistema de comunicação em tempo real (1ms)
- ✨ Descoberta automática de máquinas online
- ✨ Sistema de auditoria completo e imutável
- ✨ Hash SHA-256 para integridade de registros
- ✨ Painel administrativo com autenticação
- ✨ Justificativas obrigatórias para ações manuais
- ✨ Comboboxes para seleção padronizada
- ✨ Seleção de usuário via combobox no lançamento
- ✨ Layout melhorado com rejeições lado a lado
- ✨ Painel desenvolvedor completo (30+ funcionalidades)
- ✨ Controle remoto de máquinas
- ✨ 10 comandos remotos disponíveis
- ✨ Verificação de integridade da auditoria
- ✨ Exportação de relatórios de auditoria
- ✨ Script de teste automático (testar_sistema.py)
- ✨ Documentação completa (7 arquivos)

### Modificado
- 🔄 Sistema de comunicação agora envia status a cada 1ms
- 🔄 Status salvo localmente E na rede
- 🔄 Layout de formulários melhorado
- 🔄 Rejeições agora aparecem lado a lado
- 🔄 Interface mais intuitiva e responsiva

### Corrigido
- 🐛 Máquinas agora aparecem online corretamente
- 🐛 Descoberta de máquinas funciona local e rede
- 🐛 Arquivo de auditoria protegido contra modificação
- 🐛 Validação de justificativas implementada

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
