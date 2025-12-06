# 📦 Guia de Instalação

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
venv\Scripts\activate
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
