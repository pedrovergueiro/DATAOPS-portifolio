# Contribuindo para o Sistema de Coleta de Produção

Obrigado por considerar contribuir para este projeto! 🎉

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor abra uma issue incluindo:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. comportamento atual
- Screenshots (se aplicável)
- Versão do Python e sistema operacional

### Sugerindo Melhorias

Para sugerir melhorias:

1. Verifique se a sugestão já não existe nas issues
2. Abra uma nova issue com a tag "enhancement"
3. Descreva claramente a melhoria proposta
4. Explique por que seria útil

### Pull Requests

1. Fork o projeto
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/MinhaFeature
   ```

3. Faça suas alterações seguindo o estilo de código do projeto

4. Teste suas alterações:
   ```bash
   python testar_sistema.py
   ```

5. Commit suas mudanças:
   ```bash
   git commit -m "Add: Descrição da feature"
   ```

6. Push para sua branch:
   ```bash
   git push origin feature/MinhaFeature
   ```

7. Abra um Pull Request

## Padrões de Código

### Python

- Siga PEP 8
- Use docstrings para funções e classes
- Comente código complexo
- Mantenha funções pequenas e focadas

### Commits

Use mensagens de commit claras:

- `Add:` para novas features
- `Fix:` para correções de bugs
- `Update:` para atualizações
- `Refactor:` para refatoração
- `Docs:` para documentação

Exemplo:
```
Add: Sistema de notificações por email
Fix: Correção no cálculo de rejeições
Update: Atualização da biblioteca pandas
```

## Estrutura de Branches

- `main` - Branch principal (produção)
- `develop` - Branch de desenvolvimento
- `feature/*` - Branches de features
- `fix/*` - Branches de correções
- `hotfix/*` - Correções urgentes

## Testes

Antes de submeter um PR:

1. Execute os testes:
   ```bash
   python testar_sistema.py
   ```

2. Verifique se não há erros no console

3. Teste manualmente as funcionalidades afetadas

## Documentação

Se sua contribuição adiciona ou modifica funcionalidades:

1. Atualize o README.md
2. Adicione/atualize docstrings
3. Atualize a documentação relevante em `docs/`

## Código de Conduta

- Seja respeitoso com outros contribuidores
- Aceite críticas construtivas
- Foque no que é melhor para o projeto
- Mantenha discussões profissionais

## Dúvidas?

Se tiver dúvidas sobre como contribuir:

1. Leia a documentação em `docs/`
2. Abra uma issue com a tag "question"
3. Entre em contato com os mantenedores

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

---

Obrigado por contribuir! 🚀
