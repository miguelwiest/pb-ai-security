# Sistema Inteligente de Atendimento ao Cliente - Projeto de Bloco (TP1)

Este repositório contém a entrega do **Trabalho Prático 1 (TP1)** do Projeto de Bloco (Análise e Segurança de Agentes de IA) do **Instituto Infnet**.

---

## Objetivo do Projeto

O objetivo deste projeto é estabelecer as bases estatísticas e arquiteturais para um **Sistema de Atendimento ao Cliente com IA**:
1. **Exploração e Análise de Dados (EDA)**: Compreender o domínio de chamados de suporte técnico a partir do *Customer Support Ticket Dataset* (Kaggle), inspecionando qualidade, limpando dados e formulando hipóteses de negócio e modelagem.
2. **API Modular Segura com FastAPI**: Construir uma API RESTful escalável com autenticação JWT baseada em `OAuth2PasswordBearer`, endpoints de verificação de integridade e rota de inferência simulada.
3. **Modelagem de Segurança & DFD**: Mapear fluxos de dados, limites de confiança (*Trust Boundaries*) e aplicar a **Tríade CIA** (Confidencialidade, Integridade e Disponibilidade).

---

## Estrutura do Repositório

```text
PROJETO/
├── README.md                          # Documentação geral, guia de instalação e execução
├── requirements.txt                   # Dependências completas do projeto
├── data/
│   └── customer_support_tickets.csv   # Dataset de tickets de suporte ao cliente
├── eda/
│   └── eda.ipynb                      # Notebook Jupyter com a EDA completa e 3 hipóteses
├── fastapi/
│   ├── main.py                        # Ponto de entrada da aplicação FastAPI
│   ├── requirements.txt               # Dependências da API
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                 # Schemas Pydantic de entrada, saída e autenticação
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py                  # Endpoint GET /health
│   │   ├── auth.py                    # Endpoint POST /auth/token e GET /auth/me
│   │   └── predict.py                 # Endpoint POST /predict (protegido por JWT)
│   └── security/
│       ├── __init__.py
│       └── auth.py                    # JWT, Bcrypt, OAuth2PasswordBearer e usuário in-code
├── others/
│   ├── dfd_api.png                    # Diagrama de Fluxo de Dados (DFD) e Tríade CIA
│   └── generate_dfd.py                # Script gerador do diagrama DFD
└── tests/
    ├── __init__.py
    └── test_api.py                    # Testes automatizados (pytest) das rotas e segurança
```

---

## Instalação e Pré-requisitos

### 1. Clonar o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Criar e ativar um ambiente virtual (Opcional, mas recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

---

## Como Executar a Aplicação

### Executando a API FastAPI

Acesse o diretório `fastapi` e inicie o servidor com **Uvicorn**:

```bash
cd fastapi
uvicorn main:app --reload
```

A API estará acessível em: `http://127.0.0.1:8089`

- **Documentação Interativa (Swagger UI):** `http://127.0.0.1:8089/docs`
- **Documentação Alternativa (ReDoc):** `http://127.0.0.1:8089/redoc`

---

## Endpoints da API e Autenticação

### Credenciais do Usuário Administrador (In-Code)
Conforme requisito da entrega, a autenticação utiliza credenciais de um usuário admin in-code:
- **Username:** `admin`
- **Password:** `AdminInfnet2026!`

---

### 1. `GET /health` (Público)
Verifica o status operacional e a integridade da API.
- **Requisição:**
  ```http
  GET /health HTTP/1.1
  Host: 127.0.0.1:8089
  ```
- **Resposta (200 OK):**
  ```json
  {
    "status": "ok",
    "version": "1.0.0",
    "service": "Customer Support Ticket API - PB TP1",
    "timestamp": "2026-08-24T23:50:00Z"
  }
  ```

---

### 2. `POST /auth/token` (Público)
Autentica o usuário administrador e retorna um token de acesso JWT (form-data).
- **Requisição:**
  ```http
  POST /auth/token HTTP/1.1
  Host: 127.0.0.1:8089
  Content-Type: application/x-www-form-urlencoded

  username=admin&password=AdminInfnet2026!
  ```
- **Resposta (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

---

### 3. `POST /predict` (Protegido por JWT)
Simula a inferência do modelo de Machine Learning que classifica a intenção do ticket. Exige o cabeçalho `Authorization: Bearer <TOKEN_JWT>`.

- **Requisição:**
  ```http
  POST /predict HTTP/1.1
  Host: 127.0.0.1:8089
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json

  {
    "text": "Não consigo conectar ao servidor remoto desde hoje de manhã. Erro 504."
  }
  ```
- **Resposta (200 OK):**
  ```json
  {
    "input_text": "Não consigo conectar ao servidor remoto desde hoje de manhã. Erro 504.",
    "predicted_intent": "Technical issue",
    "confidence": 0.94,
    "simulated_model": "MockIntentClassifier-v1.0 (Simulation Phase)",
    "timestamp": "2026-08-24T23:50:05Z"
  }
  ```

---

## Execução dos Testes Automatizados

Para rodar a suíte de testes com `pytest`:

```bash
pytest tests/test_api.py -v
```

---

## Análise Exploratória de Dados (EDA)

O notebook `eda/eda.ipynb` cobre rigorosamente:
1. **Compreensão do Domínio e Fonte do Dataset**: Kaggle (*Customer Support Ticket Dataset*).
2. **Inspeção Inicial**: Tipos primitivos, contagens e estatísticas descritivas.
3. **Qualidade dos Dados**: Tratamento de nulos em tickets abertos vs fechados e verificação de integridade.
4. **Limpeza e Preparação**: Conversão de datas e criação de features textuais.
5. **Análise Univariada**: Distribuições de `Ticket Type`, `Ticket Priority`, `Ticket Channel`, `First Response Time`, `Customer Satisfaction (CSAT)` e `Customer Age`.
6. **3 Hipóteses Formuladas**:
   - **Hipótese 1:** Intenções de Cancelamento e Reembolso concentram prioridades mais altas e impactam negativamente o CSAT se não receberem triagem rápida (*Fast-Track*).
   - **Hipótese 2:** Tickets de Problemas Técnicos possuem textos mais longos e detalhados, ideais para autoatendimento automatizado via RAG (Retrieval-Augmented Generation).
   - **Hipótese 3:** Canais síncronos (Chat) possuem menor latência e textos mais objetivos do que canais assíncronos (Email), demandando estratégias de inferência diferenciadas.

---

## Modelagem de Segurança & Diagrama DFD

O diagrama completo em alta resolução está disponível em [`others/dfd_api.png`](others/dfd_api.png).

### Limites de Confiança (Trust Boundaries)
1. **Trust Boundary 1 (Zona Pública/Não Confiável):** Abrange clientes, agentes e requisições externas originadas na Internet.
2. **Trust Boundary 2 (Zona Protegida por JWT):** Abrange o núcleo da API onde a execução só ocorre após a validação criptográfica do token assinado.

### Tríade CIA
- **Confidencialidade:** Proteção de PII nos tickets via TLS/HTTPS, armazenamento de senhas com algoritmo de derivação forte (Bcrypt) e segredo JWT inviolável.
- **Integridade:** Assinatura digital HMAC-SHA256 (HS256) no JWT impedindo adulteração de payloads ou falsificação de identidade.
- **Disponibilidade:** Endpoints leves e monitoramento via `/health` para garantir operação contínua e escalabilidade.

---

## Informações de Entrega (Infnet)

- **Professor:** Tiago Xavier (`tiago.xavier@prof.infnet.edu.br`)
- **Grupo:** Miguel Andrade Wiest de São Pedro, Lorenzo Schönwald Lima, Lucas Garcia Ferro.
- **Repositório Git:** Acessível publicamente / concedido acesso ao professor.