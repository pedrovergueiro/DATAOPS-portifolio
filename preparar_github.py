"""Script para preparar o projeto para upload no GitHub"""

import os
import shutil
import json

print("="*70)
print("🚀 PREPARANDO PROJETO PARA GITHUB")
print("="*70)

# 1. Criar pasta docs e mover documentação
print("\n📁 Organizando documentação...")
if not os.path.exists("docs"):
    os.makedirs("docs")
    print("   ✅ Pasta docs/ criada")

docs_files = [
    "LEIA_ME_PRIMEIRO.txt",
    "GUIA_VISUAL_RAPIDO.txt",
    "RESPOSTAS_QUESTOES_USUARIO.md",
    "INSTRUCOES_USO_SISTEMA.md",
    "RESUMO_SISTEMA_COMPLETO.md",
    "MELHORIAS_FINAIS_IMPLEMENTADAS.md",
    "MELHORIAS_IMPLEMENTADAS.md",
    "FUNCIONALIDADES_IMPLEMENTADAS.md",
    "MANUAL_PAINEL_DESENVOLVEDOR.md",
    "INICIO_RAPIDO.md",
    "CORRECOES_FINAIS.md",
    "RESUMO_MELHORIAS_FINAIS.md",
    "COMPILAR_EXECUTAVEIS.md"
]

for doc in docs_files:
    if os.path.exists(doc):
        try:
            shutil.copy2(doc, os.path.join("docs", doc))
            print(f"   ✅ {doc} copiado para docs/")
        except Exception as e:
            print(f"   ⚠️ Erro ao copiar {doc}: {e}")

# 2. Renomear README_GITHUB.md para README.md
print("\n📄 Preparando README principal...")
if os.path.exists("README_GITHUB.md"):
    if os.path.exists("README.md"):
        shutil.copy2("README.md", "README_OLD.md")
        print("   ✅ README.md antigo salvo como README_OLD.md")
    shutil.copy2("README_GITHUB.md", "README.md")
    print("   ✅ README_GITHUB.md → README.md")

# 3. Criar arquivo de exemplo para configurações
print("\n⚙️ Criando arquivos de exemplo...")

# config_maquina.json.example
config_maquina_example = {
    "maquina": "EXEMPLO"
}
with open("config_maquina.json.example", "w", encoding="utf-8") as f:
    json.dump(config_maquina_example, f, indent=2, ensure_ascii=False)
print("   ✅ config_maquina.json.example criado")

# config_size.json.example
config_size_example = {
    "maquina": "EXEMPLO",
    "size": "#0",
    "peso": 0.000096
}
with open("config_size.json.example", "w", encoding="utf-8") as f:
    json.dump(config_size_example, f, indent=2, ensure_ascii=False)
print("   ✅ config_size.json.example criado")

# config_lote.json.example
config_lote_example = {
    "lote": "LOTE_EXEMPLO",
    "caixa_atual": 1,
    "total_caixas": 100,
    "caixas_registradas": 0
}
with open("config_lote.json.example", "w", encoding="utf-8") as f:
    json.dump(config_lote_example, f, indent=2, ensure_ascii=False)
print("   ✅ config_lote.json.example criado")

# 4. Criar arquivo de dados de exemplo
print("\n📊 Criando arquivos de dados de exemplo...")

# usuarios.csv.example
usuarios_example = """login,senha,tipo,nome_completo
admin,admin123,Desenvolvedor,Administrador do Sistema
coordenador,coord123,Coordenador,Coordenador de Produção
encarregado,enc123,Encarregado,Encarregado de Turno
operador,oper123,Operador,Operador de Máquina
"""
with open("usuarios.csv.example", "w", encoding="utf-8") as f:
    f.write(usuarios_example)
print("   ✅ usuarios.csv.example criado")

# dados_producao.csv.example
dados_example = """maquina,lote,numero_caixa,size,peso,rej1_defect,rej1_local,rej2_defect,rej2_local,rej3_defect,rej3_local,percent_cam_d,percent_cam_w,data_hora,origem,justificativa,usuario_reg
201,LOTE001,1,#1,0.000096,N/A,N/A,N/A,N/A,N/A,N/A,0.5,0.3,2024-12-05 10:00:00,coletor,,operador
"""
with open("dados_producao.csv.example", "w", encoding="utf-8") as f:
    f.write(dados_example)
print("   ✅ dados_producao.csv.example criado")

# 5. Criar INSTALL.md
print("\n📦 Criando guia de instalação...")
install_guide = """# 📦 Guia de Instalação

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/sistema-producao.git
cd sistema-producao
```

### 2. Criar Ambiente Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\\Scripts\\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Arquivos Iniciais

Copie os arquivos de exemplo:

```bash
copy config_maquina.json.example config_maquina.json
copy config_size.json.example config_size.json
copy config_lote.json.example config_lote.json
copy usuarios.csv.example usuarios.csv
copy dados_producao.csv.example dados_producao.csv
```

**Linux/Mac:**
```bash
cp config_maquina.json.example config_maquina.json
cp config_size.json.example config_size.json
cp config_lote.json.example config_lote.json
cp usuarios.csv.example usuarios.csv
cp dados_producao.csv.example dados_producao.csv
```

### 5. Executar o Sistema

```bash
python main.py
```

## Verificação

Execute o script de teste para verificar se tudo está funcionando:

```bash
python testar_sistema.py
```

## Configuração de Rede (Opcional)

Se você deseja usar o sistema em rede:

1. Edite `config/settings.py`
2. Altere `CAMINHO_REDE` para o caminho da sua rede compartilhada
3. Certifique-se de que todas as máquinas têm acesso ao caminho

## Problemas Comuns

### Erro: ModuleNotFoundError

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: Permissão negada

**Solução:** Execute como administrador (Windows) ou use sudo (Linux/Mac)

### Máquinas não aparecem online

**Solução:** 
1. Certifique-se de que o sistema está rodando
2. Aguarde 5-10 segundos
3. Execute: `python testar_sistema.py`

## Suporte

Para mais informações, consulte:
- `docs/LEIA_ME_PRIMEIRO.txt`
- `docs/GUIA_VISUAL_RAPIDO.txt`
- `docs/INSTRUCOES_USO_SISTEMA.md`

## Próximos Passos

Após a instalação:
1. Leia `docs/LEIA_ME_PRIMEIRO.txt`
2. Configure sua máquina
3. Cadastre usuários
4. Comece a usar!
"""

with open("INSTALL.md", "w", encoding="utf-8") as f:
    f.write(install_guide)
print("   ✅ INSTALL.md criado")

# 6. Verificar .gitignore
print("\n🔒 Verificando .gitignore...")
if os.path.exists(".gitignore"):
    print("   ✅ .gitignore existe")
else:
    print("   ⚠️ .gitignore não encontrado")

# 7. Listar arquivos que serão ignorados
print("\n📋 Arquivos que serão IGNORADOS pelo Git:")
ignored_patterns = [
    "*.csv (exceto .example)",
    "*.json (exceto .example)",
    "*.log",
    "*.tmp",
    "*.bak",
    "__pycache__/",
    "venv/",
    ".vscode/",
    "status_maq_*.json",
    "comando_maq_*.json",
    "auditoria_producao.json"
]
for pattern in ignored_patterns:
    print(f"   - {pattern}")

# 8. Listar arquivos que serão INCLUÍDOS
print("\n📋 Arquivos que serão INCLUÍDOS no Git:")
included_files = [
    "main.py",
    "dash.py",
    "dashboard_standalone.py",
    "testar_sistema.py",
    "preparar_github.py",
    "requirements.txt",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "INSTALL.md",
    ".gitignore",
    "*.example (arquivos de exemplo)",
    "config/*.py",
    "data/*.py",
    "gui/*.py",
    "models/*.py",
    "utils/*.py",
    "docs/*.md",
    "docs/*.txt"
]
for file in included_files:
    print(f"   ✅ {file}")

# 9. Resumo final
print("\n" + "="*70)
print("✅ PROJETO PREPARADO PARA GITHUB!")
print("="*70)

print("\n📝 PRÓXIMOS PASSOS:")
print("\n1. Inicializar repositório Git:")
print("   git init")

print("\n2. Adicionar arquivos:")
print("   git add .")

print("\n3. Fazer primeiro commit:")
print('   git commit -m "Initial commit: Sistema de Coleta de Produção v8.0"')

print("\n4. Criar repositório no GitHub:")
print("   - Acesse https://github.com/new")
print("   - Crie um novo repositório")
print("   - NÃO inicialize com README, .gitignore ou LICENSE")

print("\n5. Conectar ao repositório remoto:")
print("   git remote add origin https://github.com/seu-usuario/sistema-producao.git")

print("\n6. Enviar para o GitHub:")
print("   git branch -M main")
print("   git push -u origin main")

print("\n" + "="*70)
print("🎉 PRONTO! Seu projeto está preparado para o GitHub!")
print("="*70)

print("\n💡 DICA: Leia o README.md para mais informações sobre o projeto")
print("💡 DICA: Consulte CONTRIBUTING.md para saber como contribuir")
print("💡 DICA: Veja CHANGELOG.md para histórico de versões")

print("\n✅ Arquivos criados:")
print("   - docs/ (pasta com documentação)")
print("   - README.md (README principal)")
print("   - LICENSE (licença MIT)")
print("   - CONTRIBUTING.md (guia de contribuição)")
print("   - CHANGELOG.md (histórico de versões)")
print("   - INSTALL.md (guia de instalação)")
print("   - .gitignore (arquivos ignorados)")
print("   - *.example (arquivos de exemplo)")

print("\n" + "="*70)
