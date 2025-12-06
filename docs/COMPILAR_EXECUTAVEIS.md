# 📦 GUIA DE COMPILAÇÃO - EXECUTÁVEIS SEPARADOS

Este guia explica como compilar o sistema em executáveis separados.

## 🎯 Executáveis a Criar

1. **main.exe** - Sistema principal de coleta
2. **dashboard_standalone.exe** - Dashboard independente

---

## 📋 PRÉ-REQUISITOS

```bash
pip install pyinstaller
pip install -r requirements.txt
```

---

## 🔨 COMPILAR SISTEMA PRINCIPAL

### Comando Básico:
```bash
pyinstaller --onefile --windowed --name="ColetorProducao" main.py
```

### Comando Completo (Recomendado):
```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name="ColetorProducao" ^
  --icon=icone.ico ^
  --add-data "config;config" ^
  --add-data "data;data" ^
  --add-data "gui;gui" ^
  --add-data "models;models" ^
  --add-data "utils;utils" ^
  --hidden-import=pandas ^
  --hidden-import=openpyxl ^
  --hidden-import=psutil ^
  main.py
```

**Resultado:** `dist/ColetorProducao.exe`

---

## 📊 COMPILAR DASHBOARD

### Comando Básico:
```bash
pyinstaller --onefile --name="Dashboard" dashboard_standalone.py
```

### Comando Completo (Recomendado):
```bash
pyinstaller ^
  --onefile ^
  --name="Dashboard" ^
  --icon=icone_dash.ico ^
  --add-data "config;config" ^
  --add-data "data;data" ^
  --hidden-import=dash ^
  --hidden-import=plotly ^
  --hidden-import=pandas ^
  dashboard_standalone.py
```

**Resultado:** `dist/Dashboard.exe`

---

## 🚀 COMPILAÇÃO RÁPIDA (AMBOS)

Crie um arquivo `compilar_tudo.bat`:

```batch
@echo off
echo ========================================
echo   COMPILANDO SISTEMA DE PRODUCAO
echo ========================================
echo.

echo [1/2] Compilando Sistema Principal...
pyinstaller --onefile --windowed --name="ColetorProducao" main.py
echo.

echo [2/2] Compilando Dashboard...
pyinstaller --onefile --name="Dashboard" dashboard_standalone.py
echo.

echo ========================================
echo   COMPILACAO CONCLUIDA!
echo ========================================
echo.
echo Arquivos gerados em: dist\
echo   - ColetorProducao.exe
echo   - Dashboard.exe
echo.
pause
```

Execute: `compilar_tudo.bat`

---

## 📁 ESTRUTURA APÓS COMPILAÇÃO

```
dist/
├── ColetorProducao.exe    (Sistema principal)
└── Dashboard.exe          (Dashboard independente)

build/                     (Arquivos temporários - pode deletar)
*.spec                     (Configurações PyInstaller)
```

---

## ⚙️ OPÇÕES AVANÇADAS

### Adicionar Ícone:
```bash
--icon=caminho/para/icone.ico
```

### Incluir Arquivos Extras:
```bash
--add-data "arquivo.txt;."
--add-data "pasta;pasta"
```

### Modo Console (para debug):
```bash
# Remover --windowed para ver mensagens de erro
pyinstaller --onefile --name="ColetorProducao" main.py
```

### Otimizar Tamanho:
```bash
--exclude-module tkinter.test
--exclude-module unittest
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "ModuleNotFoundError"
**Solução:** Adicione `--hidden-import=nome_modulo`

### Erro: "FileNotFoundError"
**Solução:** Use `--add-data` para incluir arquivos necessários

### Executável muito grande
**Solução:** Use `--exclude-module` para remover módulos não usados

### Antivírus bloqueia
**Solução:** Adicione exceção ou use certificado digital

---

## 📝 NOTAS IMPORTANTES

1. **Teste sempre** os executáveis antes de distribuir
2. **Inclua requirements.txt** para referência
3. **Documente versões** das bibliotecas usadas
4. **Mantenha backups** dos arquivos .spec
5. **Teste em máquina limpa** sem Python instalado

---

## 🔄 ATUALIZAÇÃO

Para recompilar após mudanças:

```bash
# Limpar builds anteriores
rmdir /s /q build dist
del *.spec

# Recompilar
compilar_tudo.bat
```

---

## 📦 DISTRIBUIÇÃO

### Arquivos para Distribuir:

```
📦 Pacote_Sistema_Producao/
├── ColetorProducao.exe
├── Dashboard.exe
├── README.md
└── MANUAL_USUARIO.md
```

### Não Incluir:
- Arquivos .py (código fonte)
- Pasta build/
- Arquivos .spec
- __pycache__/
- .git/

---

## ✅ CHECKLIST PRÉ-DISTRIBUIÇÃO

- [ ] Testado em máquina sem Python
- [ ] Testado com e sem acesso à rede
- [ ] Verificado funcionamento de todos os botões
- [ ] Testado painel desenvolvedor
- [ ] Testado sistema de comunicação
- [ ] Verificado criação de arquivos
- [ ] Testado backup e exportação
- [ ] Dashboard abre corretamente
- [ ] Janela de registro NUNCA fecha
- [ ] Comandos remotos funcionam

---

## 📞 SUPORTE

Em caso de problemas na compilação:
1. Verifique versões das bibliotecas
2. Teste em modo console (sem --windowed)
3. Verifique logs em build/
4. Consulte documentação PyInstaller

---

**Última atualização:** Dezembro 2024
**Versão do Sistema:** 1.0
