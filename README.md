#  Data Analyst AI API

API que permite fazer **perguntas em linguagem natural** sobre arquivos CSV. Envie seu dataset, faça uma pergunta em português e receba a resposta com o código Pandas gerado automaticamente por um LLM.

> Exemplo: suba o CSV abaixo, pergunte **"qual o total de vendas por região?"**.

```csv
produto,vendas,regiao
Notebook,1500,Sul
Celular,800,Norte
Notebook,2000,Sul
Tablet,600,Norte
Celular,1200,Sul
```

> Salve como `vendas.csv` (Bloco de Notas → Salvar como → Todos os arquivos) e faça o upload no `POST /uploadfile`.

**Resultado esperado:**
```json
{
  "pergunta": "qual o total de vendas por região?",
  "codigo_gerado": "result = df.groupby('regiao')['vendas'].sum()",
  "resultado": {
    "Norte": 1400,
    "Sul": 4700
  }
}
```

---

## Funcionalidades

- Upload de arquivos CSV com detecção automática de encoding e separador
- Listagem, visualização e preview de datasets enviados
-  Consultas em linguagem natural via LLM (Groq + LLaMA 3.3 70B)
-  Geração automática de código Pandas baseada nos metadados reais do CSV
- Execução segura com validação AST, namespace isolado e timeout de 5 segundos

---

## Stack

| Tecnologia | Uso |
|---|---|
| FastAPI | Framework web e definição dos endpoints |
| Pandas | Leitura e processamento dos CSVs |
| Groq API | LLM para geração de código Pandas |
| LLaMA 3.3 70B | Modelo de linguagem utilizado |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## Estrutura do Projeto

```
csv-analyst-api/
├── app/
│   ├── main.py                  # Entrada da aplicação FastAPI
│   ├── routers/
│   │   └── datasets.py          # Definição das rotas
│   └── services/
│       ├── dataService.py       # Lógica de negócio dos datasets
│       ├── groqService.py       # Integração com a API do Groq
│       └── executionService.py  # Execução segura do código gerado
├── .env                         # Variáveis de ambiente (não versionado)
├── .gitignore
└── README.md
```

---

## Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Conta gratuita no [Groq Console](https://console.groq.com) para obter a API key

### Instalação

```bash
# Clone o repositório
git clone git clone https://github.com/rafaelsodrepsc/csv-analyst-api.git
cd csv-analyst-api

# Instale as dependências
pip install fastapi uvicorn pandas groq python-dotenv

# Crie o arquivo de variáveis de ambiente
cp .env.example .env
```

### Configuração

Edite o arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_aqui
```

### Executando

```bash
cd app
python -m uvicorn main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints

### `POST /uploadfile`
Faz upload de um arquivo CSV e retorna os metadados do dataset.

**Request:** `multipart/form-data`

**Response:**
```json
{
  "id": "268d3332-7b46-420e-96f5-6b68e1a66ba0",
  "nome": "vendas.csv",
  "colunas": ["produto", "vendas", "regiao"],
  "shape": [5, 3]
}
```

---

### `GET /view_dataset`
Lista todos os datasets enviados na sessão atual.

**Response:**
```json
[
  {
    "id": "268d3332-7b46-420e-96f5-6b68e1a66ba0",
    "nome": "vendas.csv",
    "colunas": ["produto", "vendas", "regiao"],
    "shape": [5, 3]
  }
]
```

---

### `GET /datasets/{id}`
Retorna os metadados de um dataset específico.

---

### `GET /datasets/{id}/preview?rows=5`
Retorna as primeiras N linhas do dataset.

**Response:**
```json
[
  {"produto": "Notebook", "vendas": 1500, "regiao": "Sul"},
  {"produto": "Celular",  "vendas": 800,  "regiao": "Norte"}
]
```

---

### `POST /datasets/{id}/query`
Recebe uma pergunta em linguagem natural e retorna o resultado da análise.

**Request:**
```json
{
  "pergunta": "qual o total de vendas por região?"
}
```

**Response:**
```json
{
  "pergunta": "qual o total de vendas por região?",
  "codigo_gerado": "result = df.groupby('regiao')['vendas'].sum()",
  "resultado": {
    "Norte": 1400,
    "Sul": 4700
  }
}
```

---

## Segurança na Execução de Código

O código gerado pelo LLM passa por três camadas antes de ser executado:

1. **Validação AST** — bloqueia qualquer `import` ou builtin perigoso (`open`, `exec`, `eval`, etc.)
2. **Timeout** — execuções que ultrapassam 5 segundos são interrompidas
3. **Namespace isolado** — o código só enxerga o DataFrame (`df`), sem acesso ao sistema

---

##  Exemplos de Perguntas

```
"qual o produto mais vendido?"
"qual a média de vendas por região?"
"quantos registros existem por categoria?"
"qual o valor máximo de vendas?"
"mostre os 3 produtos com maior faturamento"
```
