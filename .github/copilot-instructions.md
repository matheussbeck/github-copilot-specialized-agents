# Sistema de Agents para GitHub Copilot

Sistema de agents especializados para fornecer assistência técnica focada e de alta qualidade através do GitHub Copilot no VS Code.

## O Que É Isso?

Este não é um sistema de "agents autônomos". É uma técnica de **prompt engineering** que simula agents especializados através de:
- Um arquivo principal com instruções de roteamento
- Arquivos especializados para cada área técnica
- Convenções de invocação via comentários

**Como funciona**: Você indica qual "agent" quer consultar através de prefixos como `@architecture` ou `@data` em comentários, e o Copilot responde seguindo as diretrizes daquele agent específico.

## Instalação

### 1. Estrutura de Diretórios

Copie os arquivos para seu projeto:

```
seu-projeto/
├── .github/
│   └── copilot-instructions.md    # Arquivo principal (obrigatório)
└── .copilot/
    └── agents/
        ├── architecture.md
        ├── data-engineering.md
        ├── backend.md
        ├── frontend.md
        ├── database.md
        ├── security.md
        ├── bug-hunter.md
        ├── optimizer.md
        ├── documentation.md
        └── standards.md
```

### 2. Configuração do VS Code

1. Instale a extensão oficial do GitHub Copilot
2. Certifique-se de ter uma assinatura ativa do Copilot
3. Os arquivos serão automaticamente detectados pelo Copilot

### 3. Teste

Crie um arquivo Python e adicione:

```python
# @standards: este código está profissional?
def calc(x,y):
    return x+y
```

O Copilot deve responder analisando o código segundo padrões profissionais.

## Como Usar

### Invocação em Comentários

```python
# @architecture: como estruturar um sistema de notificações?
def notification_system():
    pass

# @data: qual a melhor forma de modelar este pipeline ETL?
def etl_pipeline():
    pass

# @security: esta validação está segura?
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"

# @standards: isso é gambiarra?
try:
    result = operation()
except:
    pass
```

### Invocação no Chat do Copilot

Abra o chat do Copilot (Ctrl/Cmd + I) e digite:

```
@architecture: preciso decidir entre monolito e microserviços para um sistema de vendas

@bug-hunter: por que este código está gerando memory leak?

@optimizer: como melhorar a performance desta query SQL?
```

## Agents Disponíveis

### @architecture - Arquitetura e Design de Sistemas
Decisões arquiteturais, patterns, trade-offs, escalabilidade.

**Quando usar**:
- Decisões de alto nível (monolito vs microserviços)
- Design patterns
- Estruturação de módulos
- Questões de escalabilidade

**Exemplo**:
```python
# @architecture: como estruturar autenticação em microserviços?
```

### @data - Engenharia de Dados
Pipelines ETL, modelagem, qualidade de dados, ferramentas de big data.

**Quando usar**:
- Design de pipelines
- Escolha de ferramentas (Airflow, Spark)
- Modelagem de data warehouse
- Questões de data quality

**Exemplo**:
```python
# @data: batch ou streaming para processar 500GB diários?
```

### @backend - Desenvolvimento Backend
APIs, serviços, integrações, autenticação.

**Quando usar**:
- Design de APIs REST/GraphQL
- Integrações com serviços externos
- Background jobs
- Rate limiting e caching

**Exemplo**:
```python
# @backend: como implementar retry logic com exponential backoff?
```

### @frontend - Desenvolvimento Frontend
Componentes React, state management, performance.

**Quando usar**:
- Arquitetura de componentes
- State management (Redux, Context)
- Performance optimization
- Questões de UX

**Exemplo**:
```jsx
// @frontend: este componente deveria ser memo()?
```

### @database - Banco de Dados
Modelagem, queries, índices, otimização.

**Quando usar**:
- Design de schema
- Otimização de queries
- Índices e performance
- Migrations

**Exemplo**:
```sql
-- @database: esta query está otimizada?
SELECT * FROM orders WHERE user_id = 123
```

### @security - Segurança
OWASP Top 10, vulnerabilidades, autenticação, secrets.

**Quando usar**:
- Auditoria de segurança
- Validação de inputs
- Prevenção de vulnerabilidades
- Secrets management

**Exemplo**:
```python
# @security: este endpoint está vulnerável a SQL injection?
```

### @bug-hunter - Debug e Troubleshooting
Análise de erros, stack traces, reprodução de bugs.

**Quando usar**:
- Debugging de problemas complexos
- Análise de stack traces
- Reprodução de bugs intermitentes
- Root cause analysis

**Exemplo**:
```python
# @bug-hunter: por que esta função retorna None às vezes?
```

### @optimizer - Otimização e Performance
Code refactoring, performance, complexity analysis.

**Quando usar**:
- Otimização de código lento
- Refactoring
- Análise de complexidade (Big O)
- Code quality improvement

**Exemplo**:
```python
# @optimizer: como melhorar a performance deste loop?
```

### @docs - Documentação
README, docstrings, comentários, documentação técnica.

**Quando usar**:
- Criação de README
- Docstrings efetivas
- Documentação de API
- Onboarding documentation

**Exemplo**:
```python
# @docs: preciso documentar esta função complexa
```

### @standards - Validação de Padrões (IMPORTANTE!)
Identifica gambiarras, valida convenções, compara com mercado.

**Quando usar**:
- Code review pessoal
- Verificar se está profissional
- Identificar code smells
- Aprender padrões corretos

**Exemplo**:
```python
# @standards: este código passaria em code review?
def calc(x,y):
    try:
        return x+y
    except:
        pass
```

## Fluxo de Trabalho Recomendado

### 1. Desenvolvimento

```python
# Escrevendo código novo
# @architecture: qual padrão usar para este caso?

# @backend: como estruturar esta API?
```

### 2. Revisão

```python
# Código pronto - verificar qualidade
# @standards: isso está profissional?

# @security: tem vulnerabilidades?

# @optimizer: pode ser mais performático?
```

### 3. Debug

```python
# Encontrou bug
# @bug-hunter: por que isso falha intermitentemente?

# @database: por que esta query está lenta?
```

### 4. Documentação

```python
# Finalizar feature
# @docs: ajuda a documentar este módulo
```

## Dicas de Uso

### 1. Seja Específico

```python
# RUIM - vago
# @architecture: como fazer isso?

# BOM - específico
# @architecture: sistema de notificações com 10k usuários,
# precisa ser em tempo real, como arquitetar?
```

### 2. Forneça Contexto

```python
# BOM - com contexto
# @data: pipeline processa 500GB/dia, SLA de 4h,
# batch ou streaming?

# RUIM - sem contexto
# @data: usar Spark?
```

### 3. Use Standards Frequentemente

```python
# Desenvolva o hábito de validar
# @standards: está profissional?

# Isso previne débito técnico
```

### 4. Combine Agents Quando Necessário

```python
# Questão complexa pode precisar múltiplos agents
# @architecture: estrutura geral do sistema de pagamentos
# ... obtém resposta ...

# @security: pontos de atenção de segurança nesta arquitetura
# ... obtém resposta ...

# @database: como modelar transações
```

## Limitações

### O Que NÃO É

- Não são agents autônomos que conversam entre si
- Não há delegação automática (você indica qual agent)
- Não há memória persistente entre sessões
- Contexto é compartilhado entre agents

### Escopo

- Só funciona no projeto onde os arquivos estão
- Depende do modelo do Copilot entender as instruções
- Qualidade varia com complexidade da pergunta

## Troubleshooting

### Copilot não responde seguindo os agents

1. Verifique se `.github/copilot-instructions.md` existe
2. Confirme que está usando a sintaxe correta (`@agent:`)
3. Tente reiniciar o VS Code
4. Verifique se sua assinatura do Copilot está ativa

### Respostas genéricas

1. Seja mais específico na pergunta
2. Forneça mais contexto
3. Tente reformular usando exemplos concretos

### Agent "errado" responde

1. Verifique se usou o prefixo correto
2. Confirme que o arquivo do agent existe
3. Pergunta pode ser ambígua - especifique melhor

## Personalização

### Adicionar Novo Agent

1. Crie arquivo em `.copilot/agents/novo-agent.md`
2. Siga estrutura dos agents existentes
3. Adicione entrada em `copilot-instructions.md`

### Modificar Agent Existente

1. Edite o arquivo do agent específico
2. Adicione contexto específico do seu projeto
3. Mantenha estrutura consistente

### Contexto do Projeto

Edite `.github/copilot-instructions.md` para adicionar:
- Stack específica do projeto
- Padrões internos da equipe
- Decisões arquiteturais já tomadas

## Manutenção

### Atualização

Agents podem ficar desatualizados. Revise periodicamente:
- Padrões da linguagem mudaram?
- Novas best practices disponíveis?
- Ferramentas novas no mercado?

### Feedback

Após usar um agent:
1. Resposta foi útil?
2. Instruções estão claras?
3. Falta alguma informação?

Ajuste os arquivos conforme necessário.

## Próximos Passos

1. Experimente cada agent com perguntas reais do seu dia-a-dia
2. Identifique quais agents usa mais
3. Personalize com contexto do seu projeto
4. Compartilhe com o time (se aplicável)
5. Use @standards regularmente para melhorar qualidade do código

## Recursos Adicionais

- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)

## Licença

Este sistema é open source. Use, modifique e compartilhe como preferir.

---

**Dica Final**: O agent @standards é seu melhor amigo para aprender. Use-o em TODOS os códigos que escrever. Em 3 meses você estará escrevendo código profissional naturalmente.