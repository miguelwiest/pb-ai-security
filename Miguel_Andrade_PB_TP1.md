<br><br><br><br><br><br><br><br><br>

<div style="text-align: center;">
  <h3>INSTITUTO INFNET</h3>
  <h4>ESCOLA SUPERIOR DE TECNOLOGIA</h4>
</div>

<br><br><br><br><br><br><br><br>

<div style="text-align: center;">
  <h2>Projeto de Bloco: Sistema de Atendimento com IA & Segurança</h2>
  <h3>Teste de Performance 1 (TP1)</h3>
</div>

<br><br><br><br><br><br><br><br>

<div style="text-align: right; padding-left: 50%;">
  <p>Trabalho apresentado ao Instituto Infnet como requisito parcial para obtenção de grau no Teste de Performance 1 (TP1) do Projeto de Bloco.</p>
  <p><b>Professor:</b> Tiago Xavier</p>
  <p><b>Aluno:</b> Miguel Andrade Wiest de São Pedro</p>
  <p><b>Link do Repositório Git:</b> <a href="https://github.com/miguel-pedro/miguel_pb_tp1">https://github.com/miguel/miguel_pb_tp1</a></p>
</div>

<br><br><br><br><br><br><br><br>

<div style="text-align: center;">
  <p>Rio de Janeiro - RJ</p>
  <p>2026</p>
</div>

<div style="page-break-after: always;"></div>

# Sumário Executivo e Informações de Entrega

- **Nome do Aluno:** Miguel Andrade Wiest de São Pedro
- **E-mail do Aluno:** miguela.pedro@al.infnet.edu.br
- **E-mail do Professor:** tiago.xavier@prof.infnet.edu.br
- **Repositório Git:** [https://github.com/miguel/miguel_pb_tp1](https://github.com/miguel/miguel_pb_tp1)
- **Nome do Arquivo PDF no Moodle:** `miguel_pedro_PB_TP1.PDF` (ou `miguel_saopedro_PB_TP1.PDF`)

---

# 1. Documentação Técnica do Dataset

### 1.1 Fonte (Origem do Dataset)
O dataset selecionado como base para todo o ciclo de desenvolvimento do Projeto de Bloco é o **Customer Support Ticket Dataset**, hospedado na plataforma Kaggle:
- **URL:** [https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)
- **Mantenedor:** Suraj (@suraj520)
- **Domínio:** Gestão de chamados de suporte técnico, SAC multicanal e CRM.

### 1.2 Principais Características
O conjunto de dados abrange atributos estruturados e textuais ricos:
- `Ticket ID`: Identificador único do chamado.
- `Customer Name`, `Customer Email`, `Customer Age`, `Customer Gender`: Informações cadastrais e demográficas do solicitante (dados pessoais / PII).
- `Product Purchased` & `Date of Purchase`: Contexto do produto ou serviço adquirido.
- `Ticket Type`: Categoria principal da solicitação (`Technical issue`, `Billing inquiry`, `Cancellation request`, `Product inquiry`, `Refund request`).
- `Ticket Subject` & `Ticket Description`: Título e descrição do problema em linguagem natural.
- `Ticket Status`: Estado atual do chamado (`Open`, `In Progress`, `Closed`, `Pending Customer Response`).
- `Resolution`: Descrição do procedimento adotado pelo atendente para solução do ticket.
- `Ticket Priority`: Grau de urgência do atendimento (`Low`, `Medium`, `High`, `Critical`).
- `Ticket Channel`: Canal de entrada (`Email`, `Phone`, `Chat`, `Social Media`).
- `First Response Time`: Intervalo de tempo até o primeiro retorno do time de suporte.
- `Time to Resolution`: Tempo total de resolução do chamado.
- `Customer Satisfaction Rating`: Nota de satisfação (CSAT de 1 a 5).

### 1.3 Motivo de Escolha do Dataset
1. **Atendimento aos Objetivos de IA do Bloco:** A presença de campos em texto livre (`Ticket Subject` e `Ticket Description`) combinados com rótulos de categoria (`Ticket Type`) oferece o ambiente perfeito para treinar e avaliar modelos de Processamento de Linguagem Natural (NLP) e classificação de intenções.
2. **Relevância para a Trilha de Segurança e Ataques:** A inclusão de dados pessoais identificáveis (PII) e relatórios de falhas de sistemas possibilita a modelagem rigorosa de superfícies de ataque, vazamento de dados, injeção de prompt e controle de acesso baseado em papéis.
3. **Maturidade e Realismo dos Dados:** A distribuição multicanal (chat, e-mail, telefone, redes sociais) reflete a operação real de empresas de tecnologia.

---

# 2. Resumo da Análise Exploratória de Dados (EDA)

A análise exploratória foi implementada no notebook Jupyter `eda/eda.ipynb`, estruturada nos seguintes tópicos:

1. **Compreensão do Problema:** Mapeamento das regras de negócio de helpdesk e definição do fluxo de triagem automatizada.
2. **Inspeção Inicial:** Verificação de tipos de dados (`dtypes`), dimensões e primeiras linhas do dataset.
3. **Qualidade dos Dados:** Validação de unicidade do `Ticket ID` e tratamento dos valores faltantes em chamados abertos (como `Resolution` e `Time to Resolution` ausentes em tickets não encerrados).
4. **Limpeza e Preparação:** Conversão de datas e engenharia de features auxiliares (`Description_Length`, `Subject_Word_Count`).
5. **Análise Univariada:** Geração de gráficos de distribuição para as variáveis-chave:
   - Tipos de ticket (balanceamento de classes).
   - Níveis de prioridade.
   - Canais de atendimento mais frequentes (predomínio de e-mail e chat).
   - Tempo de primeira resposta e tempo de resolução.
   - Distribuição das notas de satisfação (CSAT).

---

# 3. Hipóteses Formuladas sobre as Intenções dos Usuários

Com base na distribuição estatística observada na Análise Univariada, foram consolidadas 3 hipóteses:

### 📌 Hipótese 1: Intenções de Cancelamento e Reembolso Demandam Roteamento Rápido (*Fast-Track*)
- **Fundamentação:** Os chamados classificados como `Cancellation request` e `Refund request` concentram maior proporção de prioridades críticas e apresentam queda drástica no CSAT quando o tempo de primeira resposta ultrapassa a média.
- **Aplicação na IA:** O classificador de intenção deve atribuir prioridade máxima a essas intenções, encaminhando-as de forma imediata para retenção ou agentes seniores.

### 📌 Hipótese 2: Chamados Técnicos Apresentam Maior Extensão Textual e Alto Potencial para Resolução via RAG
- **Fundamentação:** O atributo `Description_Length` para `Technical issue` possui comprimento e vocabulário técnico superiores (erros, falhas de conectividade, códigos de status).
- **Aplicação na IA:** A riqueza contextual permite que uma IA generativa alimentada por base de conhecimento (RAG) resolva as dúvidas sem intervenção humana, reduzindo o tempo de resolução.

### 📌 Hipótese 3: Canais de Chat Concentram Interações Objetivas de Baixa Latência
- **Fundamentação:** O canal `Chat` apresenta tempos de resposta substancialmente inferiores ao `Email`, com solicitações focadas em dúvidas de faturamento ou produto.
- **Aplicação na IA:** O endpoint de inferência deve ser otimizado para latência ultrabaixa em sessões de chat em tempo real.

---

# 4. Estrutura Modular da API FastAPI & Autenticação JWT

A aplicação foi implementada de forma modular dentro do diretório `fastapi/`:

- **`fastapi/main.py`**: Ponto de entrada configurando a instância do FastAPI, middlewares de CORS, metadados OpenAPI e inclusão dos roteadores.
- **`fastapi/models/schemas.py`**: Modelos Pydantic V2 (`Token`, `TokenData`, `User`, `PredictRequest`, `PredictResponse`, `HealthResponse`) garantindo validação estrita de tipos e documentação no Swagger.
- **`fastapi/security/auth.py`**:
  - Configuração do algoritmo `HS256` com `SECRET_KEY` e tempo de expiração.
  - Hashing e verificação de senhas via biblioteca nativa `bcrypt`.
  - Configuração do `OAuth2PasswordBearer(tokenUrl="auth/token")`.
  - Usuário `admin` in-code com credenciais seguras.
  - Dependência assíncrona `get_current_user` para proteção de rotas.
- **`fastapi/routes/`**:
  - `health.py`: Rota pública `GET /health` que retorna status operacional e versão.
  - `auth.py`: Rota pública `POST /auth/token` que valida credenciais via form-data e retorna o token JWT.
  - `predict.py`: Rota protegida `POST /predict` que recebe o texto do ticket e retorna a intenção predita simulada.

### Comandos de Execução
```bash
# Executar a API localmente
cd fastapi
uvicorn main:app --reload

# Executar a suíte de testes automatizados
pytest tests/test_api.py -v
```

---

# 5. Diagrama de Fluxo de Dados (DFD) & Análise da Tríade CIA

O diagrama DFD foi gerado e salvo em `others/dfd_api.png`.

```
+-----------------------------------------------------------------------------------+
|                            TRUST BOUNDARY 1 (Pública)                            |
|  [E1: Cliente / Atendente]                 [E2: Administrador]                    |
+-----------------------------------------------------------------------------------+
           | (Texto Ticket + JWT)                      | (Credenciais)
           v                                           v
+-----------------------------------------------------------------------------------+
|                        FASTAPI GATEWAY / AUTHENTICATION                           |
|  [P1: GET /health]                         [P2: POST /auth/token]                 |
|                                                      |                            |
|                                                      v (Valida Hash Bcrypt)       |
|                                            [D1: Base Admin In-Code]               |
+-----------------------------------------------------------------------------------+
           |                                           |
           | (Token Válido)                            | (Emite JWT HS256)
           v                                           v
+-----------------------------------------------------------------------------------+
|                     TRUST BOUNDARY 2 (Zona Protegida por JWT)                     |
|  [P3: JWT Validation Middleware]  -->  [P4: POST /predict (Mock Model Inference)] |
+-----------------------------------------------------------------------------------+
```

### Matriz da Tríade CIA por Componente

| Componente / Rota | Confidencialidade (C) | Integridade (I) | Disponibilidade (A) |
| :--- | :--- | :--- | :--- |
| **Entidades Externas (E1 / E2)** | Proteção de credenciais e dados pessoais (PII) em trânsito via HTTPS/TLS. | Assegurar que os payloads não sofram ataques de Man-in-the-Middle (MitM). | Usuários e sistemas clientes devem conseguir alcançar a API sem bloqueios indevidos. |
| **GET /health (P1)** | Baixa (endpoint público sem dados sigilosos). | Alta (a resposta deve refletir o real estado de integridade do serviço). | Crítica (essencial para balanceadores de carga, health checks e Kubernetes). |
| **POST /auth/token (P2)** | Crítica (senhas tratadas com hash Bcrypt e chaves secretas nunca expostas). | Crítica (assinatura criptográfica HMAC-SHA256 impede falsificação de identidade). | Alta (sem autenticação funcional, nenhuma rota protegida é acessível). |
| **POST /predict (P3, P4)** | Alta (tickets podem conter PII; acesso restrito apenas a portadores de token válido). | Alta (garantir que a predição e o score retornados não sejam manipulados). | Alta (atendimento ao cliente requer baixa latência e alta disponibilidade). |
| **Base In-Code & Chaves (D1)** | Crítica (SECRET_KEY e credenciais nunca devem vazar em logs ou repositórios). | Crítica (constantes em memória imutáveis em tempo de execução). | Alta (armazenamento in-memory com acesso $O(1)$ sem dependência externa). |

---

# 6. Conclusão da Entrega do TP1

A entrega do TP1 cumpre com êxito todos os critérios estabelecidos pelo Instituto Infnet:
- Dataset real e explorado com rigor estatístico.
- 3 hipóteses fundamentadas sobre intenções dos usuários.
- API FastAPI modular, documentada e 100% aprovada em testes automatizados.
- Autenticação JWT in-code funcional e protegida.
- Modelagem DFD e análise da Tríade CIA detalhadas.
