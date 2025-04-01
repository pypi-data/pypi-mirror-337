# AgentFlowCraft

> Estrutura automatizada para criação, execução, avaliação e conformidade de múltiplos agentes de IA orientados a microtarefas, com registro e rastreamento completo.

---

## 📦 Instalação

Você pode instalar o AgentFlowCraft diretamente via pip:

```bash
# Instalar a versão mais recente do PyPI
pip install agent-flow-craft

# Ou instalar a versão de desenvolvimento diretamente do GitHub
pip install git+https://github.com/Malnati/agent-flow-craft.git
```

Para desenvolvimento local, recomendamos clonar o repositório:

```bash
# Clonar o repositório
git clone https://github.com/Malnati/agent-flow-craft.git
cd agent-flow-craft

# Instalar em modo de desenvolvimento
pip install -e .
```

Após a instalação, certifique-se de configurar as variáveis de ambiente necessárias:

```bash
# Para integração com GitHub
export GITHUB_TOKEN=seu_token_aqui
export GITHUB_OWNER=seu_usuario_github
export GITHUB_REPO=nome_do_repositorio

# Para uso da API OpenAI
export OPENAI_API_KEY=seu_token_openai
```

---

## 📋 Comandos do Makefile

O projeto disponibiliza diversos comandos através do Makefile para facilitar o uso dos agentes e a execução de tarefas comuns.

### Comandos de desenvolvimento

```bash
make create-venv              # Cria ambiente virtual Python se não existir
make install                  # Instala o projeto no ambiente virtual
make setup                    # Instala o projeto em modo de desenvolvimento
make test                     # Executa os testes do projeto
make lint                     # Executa análise de lint para verificar estilo de código
make format                   # Formata o código usando o Black
make build                    # Empacota o projeto usando python -m build
make clean                    # Remove arquivos temporários e de build
make clean-pycache            # Remove apenas os diretórios __pycache__ e arquivos .pyc
make all                      # Executa lint, test, formatação e atualização de docs
make update-docs-index        # Atualiza o índice da documentação automaticamente
```

### Agentes disponíveis

#### 1. Agente de criação de features (FeatureCoordinatorAgent)
```bash
make start-agent prompt="<descricao>" project_dir="<diretório>" [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-agent prompt="Implementar sistema de login" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_coordinator_agent.py "Implementar sistema de login" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo"
```

**Tarefas executadas:**
1. Inicializa o FeatureCoordinatorAgent com os parâmetros fornecidos
2. Configura o modelo OpenAI especificado no ConceptGenerationAgent interno
3. Configura o modelo de elevação para todos os agentes internos, se especificado
4. Em caso de falha do modelo principal, eleva automaticamente para o modelo de elevação
5. Se force=true, usa diretamente o modelo de elevação sem tentar o modelo principal
6. Cria um diretório de contexto para armazenar os resultados
7. Gera um conceito de feature a partir do prompt usando a API OpenAI
8. Processa a criação da feature com base no conceito gerado
9. Retorna o resultado em JSON com informações da feature criada

#### 2. Agente de geração de conceitos (ConceptGenerationAgent)
```bash
make start-concept-agent prompt="<descricao>" [output="<arquivo_saida>"] [context_dir="<dir_contexto>"] [project_dir="<dir_projeto>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-concept-agent prompt="Adicionar autenticação via OAuth" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" context_dir="agent_context" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_concept_agent.py "Adicionar autenticação via OAuth" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --context_dir="agent_context" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo"
```

**Tarefas executadas:**
1. Inicializa o ConceptGenerationAgent com o token OpenAI e modelo especificados
2. Configura o modelo de elevação para uso em caso de falha, se especificado
3. Se force=true, usa diretamente o modelo de elevação sem tentar o modelo principal
4. Obtém o log do Git do projeto (se disponível) para fornecer contexto
5. Envia o prompt e contexto para a API OpenAI para gerar um conceito de feature
6. Em caso de falha, tenta elevar automaticamente para o modelo de elevação
7. Estrutura a resposta em JSON com branch_type, issue_title, issue_description, etc.
8. Salva o conceito gerado no diretório de contexto com um ID único
9. Retorna o conceito completo com o context_id para uso posterior

#### 3. Agente guardrail de conceitos (ConceptGuardrailAgent)
```bash
make start-concept-guardrail-agent concept_id="<id_do_conceito>" prompt="<prompt_original>" [project_dir="<diretório>"] [output="<arquivo_saida>"] [context_dir="<dir_contexto>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-concept-guardrail-agent concept_id="concept_20240328_123456" prompt="Adicionar autenticação via OAuth" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_concept_guardrail_agent.py "concept_20240328_123456" "Adicionar autenticação via OAuth" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --elevation_model="gpt-4-turbo" --context_dir="agent_context"
```

**Tarefas executadas:**
1. Inicializa o ConceptGuardrailAgent com os tokens e modelos especificados
2. Configura o modelo de elevação para uso em caso de falha, se especificado
3. Se force=true, usa diretamente o modelo de elevação sem validação prévia
4. Carrega o conceito gerado previamente do arquivo de contexto
5. Avalia a qualidade do conceito (determinismo, clareza, detalhamento)
6. Lista arquivos de código-fonte relevantes no diretório do projeto
7. Se o conceito não for satisfatório, gera um prompt de melhoria
8. Envia o prompt de melhoria para a API OpenAI usando o modelo de elevação
9. Estrutura a resposta melhorada em JSON mantendo a compatibilidade
10. Salva o conceito melhorado no diretório de contexto com um ID único
11. Retorna a avaliação e o conceito melhorado para uso posterior

#### 4. Agente de geração de critérios TDD (TDDCriteriaAgent)
```bash
make start-tdd-criteria-agent context_id="<id_do_contexto>" project_dir="<diretório>" [output="<arquivo_saida>"] [context_dir="<dir_contexto>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-tdd-criteria-agent context_id="feature_concept_20240328_123456" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_tdd_criteria_agent.py "feature_concept_20240328_123456" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo" --context_dir="agent_context"
```

**Tarefas executadas:**
1. Inicializa o TDDCriteriaAgent com o token OpenAI e modelo especificados
2. Configura o modelo de elevação para uso em caso de falha, se especificado
3. Se force=true, usa diretamente o modelo de elevação sem tentar o modelo principal
4. Carrega o conceito da feature do arquivo de contexto especificado
5. Lista arquivos de código-fonte relevantes no diretório do projeto
6. Gera um prompt otimizado contendo o conceito e código-fonte relevante
7. Envia o prompt para a API OpenAI para gerar critérios de aceitação TDD
8. Em caso de falha, tenta elevar automaticamente para o modelo de elevação
9. Estrutura a resposta em JSON incluindo critérios, plano de testes e casos de borda
10. Salva os critérios no diretório de contexto com um ID único
11. Retorna os critérios TDD completos para uso na implementação

#### 5. Agente guardrail de critérios TDD (TDDGuardrailAgent)
```bash
make start-tdd-guardrail-agent criteria_id="<id_dos_criterios>" concept_id="<id_do_conceito>" project_dir="<diretório>" [output="<arquivo_saida>"] [context_dir="<dir_contexto>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-tdd-guardrail-agent criteria_id="tdd_criteria_20240328_123456" concept_id="feature_concept_20240328_123456" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_tdd_guardrail_agent.py "tdd_criteria_20240328_123456" "feature_concept_20240328_123456" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo" --context_dir="agent_context"
```

**Tarefas executadas:**
1. Inicializa o TDDGuardrailAgent com o token OpenAI e modelo especificados
2. Configura o modelo de elevação para uso em caso de falha, se especificado
3. Se force=true, usa diretamente o modelo de elevação sem validação prévia
4. Carrega os critérios TDD e o conceito da feature dos arquivos de contexto especificados
5. Avalia a qualidade dos critérios TDD existentes (pontuação, problemas, etc.)
6. Verifica se os critérios incluem elementos de UI (que devem ser evitados)
7. Se necessário, gera um prompt otimizado para melhorar os critérios
8. Solicita à API OpenAI critérios TDD aprimorados, usando o modelo configurado
9. Em caso de falha, tenta elevar automaticamente para o modelo de elevação
10. Salva os critérios melhorados no diretório de contexto com um ID único
11. Retorna uma avaliação completa e os critérios TDD aprimorados

#### 6. Agente de integração com GitHub (GitHubIntegrationAgent)
```bash
make start-github-agent context_id="<id>" [project_dir="<diretório>"] [context_dir="<diretório>"] [base_branch="<branch>"] [github_token="<token>"] [owner="<owner>"] [repo="<repo>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-github-agent context_id="feature_concept_20240601_123456" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" owner="Malnati" repo="agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_github_agent.py "feature_concept_20240601_123456" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --owner="Malnati" --repo="agent-flow-craft-aider" --context_dir="agent_context" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo"
```

**Tarefas executadas:**
1. Inicializa o GitHubIntegrationAgent com token, owner e repo especificados
2. Configura o modelo de elevação para uso em caso de falha, se especificado
2. Se force=true, usa diretamente o modelo de elevação sem tentar o modelo principal
3. Carrega o conceito de feature previamente gerado usando o context_id fornecido
4. Cria uma nova issue no GitHub com o título e descrição do conceito
5. Cria uma nova branch no repositório Git local baseada na issue
6. Cria um arquivo de plano de execução no repositório detalhando a feature
7. Cria um pull request no GitHub associado à issue e branch
8. Em caso de falha em qualquer etapa que use o modelo, tenta elevar automaticamente para o modelo de elevação
9. Retorna um JSON com issue_number, branch_name e status da integração

#### 7. Agente coordenador (FeatureCoordinatorAgent)
```bash
make start-coordinator-agent prompt="<descricao>" [project_dir="<diretório>"] [plan_file="<arquivo>"] [output="<arquivo>"] [context_dir="<diretório>"] [github_token="<token>"] [openai_token="<token>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-coordinator-agent prompt="Implementar sistema de notificações" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_coordinator_agent.py "Implementar sistema de notificações" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo" --context_dir="agent_context"
```

**Tarefas executadas:**
1. Inicializa o FeatureCoordinatorAgent com tokens e diretórios configurados
2. Configura todos os agentes internos com o modelo especificado
3. Configura o modelo de elevação para todos os agentes internos, se especificado
5. Obtém o log do Git para contexto da feature
6. Gera um conceito usando o ConceptGenerationAgent a partir do prompt
7. Em caso de falha em qualquer agente, tenta elevar automaticamente para o modelo de elevação
8. Salva o conceito no sistema de gerenciamento de contexto
9. Valida o plano de execução usando o PlanValidator
10. Processa o conceito no GitHub usando o GitHubIntegrationAgent
11. Orquestra todo o fluxo entre os diferentes agentes especializados
12. Retorna um resultado consolidado com todas as informações do processo

#### 8. Gerenciador de contexto (ContextManager)
```bash
make start-context-manager operation="<lista|obter|criar|atualizar|excluir>" [context_id="<id>"] [data_file="<arquivo.json>"] [limit=10] [type="<tipo>"] [context_dir="<dir_contexto>"] [output="<arquivo>"]
```
**Exemplo:** `make start-context-manager operation="listar" context_dir="agent_context" limit=5`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_context_manager.py "listar" --context_dir="agent_context" --limit=5
```

**Tarefas executadas:**
1. Inicializa o ContextManager com o diretório de contexto especificado
2. Baseado na operação solicitada, executa uma das seguintes ações:
   - lista: Lista os contextos disponíveis com limite e filtro por tipo
   - obter: Recupera um contexto específico pelo ID
   - criar: Cria um novo contexto a partir de um arquivo JSON
   - atualizar: Atualiza um contexto existente com novos dados
   - excluir: Remove um contexto pelo ID
   - limpar: Remove contextos antigos com base em dias especificados
3. Formata e exibe o resultado da operação solicitada
4. Opcionalmente salva o resultado em um arquivo de saída

#### 9. Validador de planos (PlanValidator)
```bash
make start-validator plan_file="<arquivo_plano.json>" [output="<arquivo_saida>"] [requirements="<arquivo_requisitos>"] [context_dir="<dir_contexto>"] [project_dir="<dir_projeto>"] [model="<modelo_openai>"] [elevation_model="<modelo_elevacao>"] [force=true]
```
**Exemplo:** `make start-validator plan_file="planos/feature_plan.json" project_dir="/Users/mal/GitHub/agent-flow-craft-aider" model="gpt-4-turbo" elevation_model="gpt-4-turbo"`

**Chamada direta (sem Makefile):**
```bash
python -B src/scripts/run_plan_validator.py "planos/feature_plan.json" --project_dir="/Users/mal/GitHub/agent-flow-craft-aider" --model="gpt-4-turbo" --elevation_model="gpt-4-turbo" --context_dir="agent_context"
```

**Tarefas executadas:**
1. Inicializa o PlanValidator com as configurações fornecidas
2. Configura o modelo de elevação para uso em caso de falha, se especificado
3. Se force=true, usa diretamente o modelo de elevação sem tentar o modelo principal
4. Carrega o plano de execução do arquivo JSON especificado
5. Carrega os requisitos específicos de validação (se fornecidos)
6. Usa a API OpenAI para analisar o plano contra os requisitos
7. Em caso de falha, tenta elevar automaticamente para o modelo de elevação
8. Avalia a qualidade e completude do plano de execução
9. Identifica potenciais problemas e sugestões de melhoria
10. Atribui uma pontuação de validação ao plano (de 0 a 10)
11. Retorna um relatório detalhado com o resultado da validação

### Testes

- `make test` - Executa os testes unitários do projeto
- `make test-mcp-e2e` - Executa o teste e2e do MCP
- `make test-coordinator-e2e` - Executa o teste e2e do FeatureCoordinatorAgent com o repositório de teste

---

## ✅ Status do projeto

[![Verificação de Assets](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-assets.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-assets.yml)
[![Lint Python](https://github.com/Malnati/agent-flow-craft/actions/workflows/lint-python.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/lint-python.yml)
[![Verificação de Markdown](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-markdown.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-markdown.yml)
[![Validação de YAML](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-yaml.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/check-yaml.yml)
[![Atualização do TREE.md](https://github.com/Malnati/agent-flow-craft/actions/workflows/update-tree.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/update3.yml)
[![Auto Tagging](https://github.com/Malnati/agent-flow-craft/actions/workflows/auto-tag.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/auto-tag.yml)
[![Atualizar índice da documentação](https://github.com/Malnati/agent-flow-craft/actions/workflows/update-docs-index.yml/badge.svg)](https://github.com/Malnati/agent-flow-craft/actions/workflows/update-docs-index.yml)
[![Changelog](https://img.shields.io/badge/changelog-visualizar-blue)](CHANGELOG.md)

---

## 📚 Contextualização do Projeto
Este repositório nasce de uma análise comparativa das principais ferramentas de desenvolvimento de agentes de IA (LangChain, LangFlow, AutoGen, CrewAI e Agno), avaliando popularidade, comunidade ativa e frequência de commits.

O objetivo principal é criar agentes de IA para execução autônoma de microtarefas, automatizando fluxos e utilizando inteligência artificial para replicar e acelerar o trabalho humano.

---

## 🚀 Tecnologias consideradas para o projeto
Abaixo, a lista de ferramentas consideradas durante a análise para compor o ecossistema deste projeto:

| Ferramenta      | Motivo de consideração                                     |
|-----------------|------------------------------------------------------------|
| **LangChain**   | Popularidade, comunidade ativa e frequência alta de commits. |
| **LangFlow**    | Interface visual para composição de fluxos de agentes.     |
| **AutoGen (MS)**| Robustez, confiabilidade e forte suporte institucional.    |
| **Agno (ex-Phidata)** | Flexibilidade para construção de agentes customizados.|
| **CrewAI**      | Colaboração entre múltiplos agentes com orquestração.     |
| **UV**          | Gerenciador de ambientes Python ágil e eficiente.         |
| **Cursor IDE**  | Ambiente de desenvolvimento altamente produtivo.          |
| **Aider**       | Assistente IA para desenvolvimento contextualizado.       |

### 📊 Comparativo de Popularidade e Atividade (dados coletados em 24 de março de 2025)

| Ferramenta      | Estrelas (⭐) | Contribuidores | Commits/Semana (últimos 6 meses) |
|-----------------|--------------|----------------|----------------------------------|
| **LangChain**   | ~104.000     | 3.529          | ~75                              |
| **LangFlow**    | ~52.800      | 262            | ~85                              |
| **AutoGen (MS)**| ~42.100      | 483            | ~80                              |
| **CrewAI**      | ~29.000      | 229            | ~30                              |
| **Agno**        | ~21.800      | 139            | ~40                              |

> **Conclusão**: O **LangChain** é a ferramenta mais popular e ativa, com grande comunidade. O **AutoGen** da Microsoft destaca-se pela confiabilidade e suporte contínuo. No momento, a tendência é utilizar o **AutoGen**, pela tradição da Microsoft em manter ferramentas bem documentadas e com suporte duradouro, mas o LangChain permanece como forte alternativa.

---

## 🛠 Estrutura dos agentes
Cada agente conterá:
- Registro do prompt inicial.
- Linha de raciocínio da IA (quando suportado pelo modelo).
- Log detalhado da execução.
- Arquivo `conformities.yaml` com parâmetros de conformidade.
- Avaliador automático de conformidade.
- Executor de ajustes automáticos.
- Mecanismo de fallback para intervenção manual.

---

## 📂 Estrutura planejada do repositório
```
agent-flow-craft/
│
├── docs/
├── agents/
├── templates/
├── evaluators/
├── logs/
├── examples/
├── config/
├── .github/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── roadmap.md
```
> A estrutura acima é gerada e mantida automaticamente no arquivo [TREE.md](./TREE.md).

---

## 🗺 Roadmap
Consulte o [roadmap completo](./roadmap.md) para ver as etapas em andamento, próximas metas e o ciclo de releases.

---

## 📸 Demonstrações visuais

### ✅ Ciclo de vida do agente
![Ciclo de Vida do Agente](docs/assets/ciclo-agente.png)

### ✅ Estrutura de pastas do projeto
![Estrutura de Pastas](docs/assets/estrutura-pastas.png)

### ✅ Execução simulada de um agente em terminal
![Execução do Agente](docs/assets/execucao-terminal.png)

### ✅ Ciclo de avaliação e feedback do agente
![Ciclo de Feedback do Avaliador](docs/assets/ciclo-feedback.png)

---

## 🧩 Templates disponíveis

O projeto oferece templates prontos para:
- Relato de bugs: [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Sugestões de novas funcionalidades: [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Pull Requests: [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md)

## 📂 Documentação interna

- [📚 Documentação principal (docs/README.md)](docs/README.md)
- O diretório `docs/pr/` contém os planos de execução gerados automaticamente a cada PR criado pelos agentes.
- O índice dos planos de execução é atualizado automaticamente via workflow do GitHub Actions.
- A estrutura do projeto é mantida atualizada no arquivo [TREE.md](./TREE.md).

---

## 🌐 Comunidade e Recursos

[![Contribua!](https://img.shields.io/badge/contribua-%F0%9F%91%8D-blue)](./CONTRIBUTING.md)
[![Código de Conduta](https://img.shields.io/badge/c%C3%B3digo%20de%20conduta-respeite%20as%20regras-orange)](./CODE_OF_CONDUCT.md)
[![Roadmap](https://img.shields.io/badge/roadmap-planejamento-green)](./roadmap.md)
[![Suporte](https://img.shields.io/badge/suporte-ajuda-important)](./SUPPORT.md)
[![Relatar problema](https://img.shields.io/badge/issues-reportar%20problema-lightgrey)](../../issues)

---

## 🛡 Segurança

Para detalhes sobre como relatar vulnerabilidades, consulte o nosso [SECURITY.md](./SECURITY.md).

---

## 💡 Contribua com a comunidade
Se você gosta do projeto, ⭐ favorite o repositório, compartilhe com colegas e participe das discussões e melhorias!

---

## 📣 Divulgação e engajamento

- Use a hashtag **#AgentFlowCraft** no Twitter e LinkedIn.
- Participe das discussões (em breve) na aba Discussions do GitHub.
- Acompanhe atualizações e releases pelo [roadmap](./roadmap.md).

---

## 📅 Última atualização deste README
*Última atualização: 26 de março de 2025*

---

## 🛠️ Automação da criação de features

### FeatureCreationAgent

O `FeatureCreationAgent` é um agente responsável por automatizar o fluxo de criação de novas funcionalidades no repositório. Ele realiza as seguintes etapas:

1. Recebe um prompt do usuário descrevendo a funcionalidade desejada.
2. Cria uma issue no GitHub com base no prompt.
3. Cria uma branch vinculada à issue.
4. Gera um plano de execução detalhado e salva no diretório `docs/pr/`.
5. Faz commit e push do plano de execução.
6. Abre um Pull Request vinculado à issue criada.

### Uso

Para utilizar o `FeatureCreationAgent`, siga os passos abaixo:

1. Certifique-se de que o ambiente Python está configurado e que o GitHub CLI (`gh`) está instalado e autenticado.
2. Instale a dependência `pyautogen` utilizando `uv pip install pyautogen`.
3. Adicione a dependência no arquivo de controle (`requirements.txt` ou `pyproject.toml`).
4. Crie um script CLI simples (`src/scripts/start_feature_agent.py`) para facilitar a execução do agente via terminal.

Exemplo de uso do script CLI:

```bash
python src/scripts/start_feature_agent.py "Descrição da nova funcionalidade" "Plano de execução detalhado"
```

### Publicação no PyPI

O projeto inclui um comando para publicação automatizada no Python Package Index (PyPI):

```bash
# Verificar a versão que será publicada
make version

# Configurar token do PyPI
export PyPI_TOKEN=seu_token_aqui

# Publicar no PyPI
make publish

# Para definir uma versão específica (padrão Semantic Versioning)
VERSION=1.2.3 make publish
```

Para publicar o pacote, você precisa:
1. Ter uma conta ativa no PyPI (https://pypi.org)
2. Criar uma chave de API em https://pypi.org/manage/account/token/
3. Definir a variável de ambiente `PyPI_TOKEN` com sua chave
4. Executar o comando `make publish`

#### Sistema de Versionamento

O sistema de versionamento segue o padrão PEP 440 (compatível com PyPI), com a seguinte estrutura:

```
MAJOR.MINOR.PATCH.devN
```

Onde:
- **MAJOR.MINOR**: Ano e mês (ex: 2025.03)
- **PATCH**: Dia do mês (ex: 28)
- **N**: Número único derivado do timestamp e hash do commit (ex: 10150123)

Exemplos:
- Versão automática: `2025.03.28.dev10150123`
- Versão manual: `1.2.3.dev10150123` (quando definida via `VERSION=1.2.3 make publish`)

Este formato garante que:
1. Cada publicação tem uma versão única (evitando o erro "File already exists")
2. As versões são 100% compatíveis com o PyPI (seguindo estritamente o PEP 440)
3. O sistema mantém rastreabilidade através do arquivo `version_commits.json`

#### Rastreabilidade de Versões para Commits

O projeto mantém um registro das associações entre versões publicadas e commits no arquivo `version_commits.json`. Isso permite identificar exatamente qual código-fonte corresponde a cada versão publicada.

Para consultar estas informações, use os comandos:

```bash
# Ver informações completas de uma versão
make version-info version=2025.3.28.dev10150123

# Obter apenas o hash do commit de uma versão (útil para scripts)
make find-commit version=2025.3.28.dev10150123

# Atualizar o CHANGELOG.md com informações da versão
make update-changelog version=2025.3.28.dev10150123

# Comparar mudanças entre duas versões
make compare-versions from=2025.3.28.dev1020023 to=2025.3.28.dev1020131
```

#### Integração com CHANGELOG

O sistema atualiza automaticamente o arquivo `CHANGELOG.md` após cada publicação, registrando:
- A versão publicada
- A data de publicação
- O commit exato associado à versão

Isso permite manter um histórico completo e rastreável de todas as versões publicadas. A atualização é feita automaticamente pelo comando `make publish`, mas também pode ser realizada manualmente com `make update-changelog`.

#### Ferramentas de Análise de Versões

O comando `compare-versions` permite visualizar facilmente as diferenças entre duas versões publicadas:
- Lista todos os commits entre as duas versões
- Fornece o comando git para ver as diferenças exatas de código
- Mostra informações de data e hora para cada versão

Estas ferramentas são especialmente úteis para:
- Localizar exatamente qual versão introduziu uma determinada funcionalidade ou bug
- Preparar notas de lançamento detalhadas
- Rastrear a evolução do código entre diferentes versões publicadas
- Identificar regressões entre versões

### Estrutura do diretório `docs/pr/`

O diretório `docs/pr/` contém planos de execução detalhados para as issues criadas e pull requests abertos pelo agente de criação de features. Cada arquivo neste diretório segue o formato `<issue_number>_feature_plan.md` e inclui:

- **Prompt recebido:** O prompt original fornecido pelo usuário.
- **Plano de execução gerado pela IA:** Um plano detalhado com informações estruturadas sobre a implementação da feature.

#### Estrutura do Plano de Execução

Cada plano de execução contém uma ou mais entregáveis, e para cada entregável são detalhados:

1. **Nome e Descrição:** Identificação clara e descrição detalhada do propósito do entregável.
2. **Dependências:** Lista completa de dependências técnicas (bibliotecas, serviços, etc.) necessárias.
3. **Exemplo de Uso:** Exemplo prático, geralmente com código, de como o entregável será utilizado.
4. **Critérios de Aceitação:** Lista objetiva e mensurável de critérios para validar o entregável.
5. **Resolução de Problemas:** Possíveis problemas que podem ocorrer, suas causas e resoluções.
6. **Passos de Implementação:** Lista sequencial e detalhada de passos para implementar o entregável.

Exemplo de um entregável em um plano de execução:

```markdown
### Entregável 1: Gerador de Plano de Execução

**Descrição:** Módulo responsável por gerar planos de execução detalhados a partir do prompt do usuário e do contexto do projeto.

**Dependências:**
- pyautogen>=0.2.0
- openai>=1.0.0
- gitpython>=3.1.30

**Exemplo de uso:**
```python
# Cria um gerador de plano
gerador = GeradorPlanoExecucao(openai_token="sk-xxx")

# Gera o plano a partir do prompt e contexto
plano = gerador.gerar_plano(
    prompt="Implementar sistema de autenticação",
    contexto_projeto=obter_contexto_projeto()
)

# Salva o plano em um arquivo
plano.salvar("docs/pr/42_feature_plan.md")
```

**Critérios de aceitação:**
- O plano gerado deve incluir todos os elementos obrigatórios (nome, descrição, dependências, etc.)
- O plano deve ser específico ao contexto do projeto
- O plano deve ser gerado em menos de 30 segundos
- O formato do plano deve seguir o padrão Markdown definido

**Resolução de problemas:**
- Problema: API da OpenAI retorna erro
  - Causa possível: Token inválido ou expirado
  - Resolução: Verificar e renovar o token de acesso

**Passos de implementação:**
1. Criar a classe GeradorPlanoExecucao
2. Implementar método para obter contexto do projeto (arquivos, histórico git)
3. Implementar integração com a API da OpenAI
4. Desenvolver prompt template para gerar o plano
5. Implementar parser para converter a resposta da API em estrutura de dados
6. Criar método para exportar o plano em formato Markdown
7. Implementar tratamento de erros e retentativas
```

Este formato estruturado ajuda a garantir que todos os planos de execução tenham informações completas e úteis para a implementação.

---

## 🛠️ Comandos disponíveis via Makefile

Para facilitar a execução de tarefas comuns no projeto, utilize os comandos abaixo:

| Comando                | Descrição                                                               |
|------------------------|-------------------------------------------------------------------------|
| `make install`         | Instala todas as dependências via `uv` utilizando o `pyproject.toml`.   |
| `make lint`            | Executa verificação de lint nos arquivos Python.                        |
| `make test`            | Executa todos os testes unitários.                                      |
| `make update-tree`     | Atualiza automaticamente o arquivo `TREE.md`.                           |
| `make update-docs`     | Atualiza o índice de documentação dentro da pasta `docs/`.              |
| `make tag`             | Executa o workflow de auto tagging conforme convenção semântica.        |
| `make check-assets`    | Valida a presença dos assets obrigatórios nas pastas de documentação.   |
| `make all`             | Executa lint, testes e atualizações em sequência.                       |
| `make start-agent`     | Inicia o agente de criação de features com ambiente Python configurado. |
| `make create-venv`     | Cria um ambiente virtual Python para o projeto.                         |

> Para usar, basta rodar:  
> ```bash
> # Exemplo: Inicia o agente de criação de features
> make start-agent prompt="Descrição da feature" execution_plan="Plano detalhado"
> 
> # Os comandos gerenciam automaticamente o ambiente virtual Python
> ```

# Agent Flow Craft

Agent Flow Craft é uma plataforma para orquestração de agentes especializados que trabalham juntos para criar features em projetos de software.

## Funcionalidades

- Geração de conceitos de features baseados em prompts do usuário
- Validação de planos de execução
- Criação automática de issues, branches e PRs no GitHub
- Sistema de contexto para transferência de dados entre agentes
- Agentes especializados e autônomos que podem trabalhar juntos ou separadamente

## Arquitetura

O sistema é composto por vários agentes especializados:

1. **ConceptGenerationAgent**: Gera conceitos de features a partir de prompts do usuário usando a OpenAI
2. **PlanValidator**: Valida planos de execução de features
3. **GitHubIntegrationAgent**: Integra com o GitHub para criar issues, branches e PRs
4. **ContextManager**: Gerencia a transferência de dados entre agentes
5. **FeatureCoordinatorAgent**: Coordena o fluxo de trabalho entre os agentes especializados

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/agent-flow-craft.git
cd agent-flow-craft

# Instalar o projeto
make install
```

## Configuração

Configure as variáveis de ambiente necessárias:

```bash
# Credenciais GitHub
export GITHUB_TOKEN=seu_token_github
export GITHUB_OWNER=seu_usuario_github
export GITHUB_REPO=nome_do_repositorio

# Credenciais OpenAI
export OPENAI_API_KEY=seu_token_openai
```

## Uso

### Agente Coordenador (Fluxo Completo)

Para executar o fluxo completo de criação de feature:

```bash
make start-coordinator-agent prompt="Implementar sistema de login com autenticação de dois fatores" \
  target="/caminho/para/repositorio" \
  output="resultado.json"
```

Opcionalmente, você pode fornecer um arquivo de plano:

```bash
make start-coordinator-agent prompt="Implementar sistema de login com autenticação de dois fatores" \
  plan_file="plano.json" \
  target="/caminho/para/repositorio"
```

### Agentes Individuais

Você pode executar cada agente especializado de forma autônoma:

#### Agente de Geração de Conceitos

```bash
make start-concept-agent prompt="Implementar sistema de login com autenticação de dois fatores" \
  output="conceito.json"
```

#### Agente de Integração GitHub

```bash
make start-github-agent context_id="feature_concept_20240328_123456" \
  target="/caminho/para/repositorio"
```

#### Gerenciador de Contexto

```bash
# Listar contextos
make start-context-manager operation=lista limit=5 type="feature_concept"

# Obter um contexto específico
make start-context-manager operation=obter context_id="feature_concept_20240328_123456"

# Criar um novo contexto
make start-context-manager operation=criar data_file="dados.json" type="feature_concept"

# Atualizar um contexto
make start-context-manager operation=atualizar context_id="feature_concept_20240328_123456" \
  data_file="novos_dados.json" merge=true

# Excluir um contexto
make start-context-manager operation=excluir context_id="feature_concept_20240328_123456"

# Limpar contextos antigos
make start-context-manager operation=limpar days=30
```

#### Validador de Planos

```bash
make start-validator plan_file="plano.json" output="validacao.json"
```

## Fluxo de Trabalho

O fluxo completo usando o FeatureCoordinatorAgent segue estas etapas:

1. Geração de conceito a partir do prompt do usuário (ConceptGenerationAgent)
2. Validação e correção do plano de execução (PlanValidator)
3. Criação de issue, branch e PR no GitHub (GitHubIntegrationAgent)
4. Transferência de dados entre as etapas usando contextos (ContextManager)

Os desenvolvedores podem intervir em qualquer ponto do processo, usando os agentes individuais para modificar ou complementar partes específicas do fluxo.

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/amazing-feature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Agentes Disponíveis

O projeto inclui os seguintes agentes:

- **ConceptAgent**: Gera conceitos de features com base em prompts
- **ConceptGuardrailAgent**: Valida e melhora conceitos de features gerados pelo ConceptAgent
- **FeatureConceptAgent**: Cria definição completa de features
- **GitHubIntegrationAgent**: Cria issues e branches no GitHub para features
- **FeatureCoordinatorAgent**: Orquestra todos os agentes para automatizar a geração de features completas
- **ContextManager**: Gerencia contexto para rastreio de features
- **TDDCriteriaAgent**: Gera critérios de TDD para features
- **TDDGuardrailAgent**: Valida e melhora critérios de TDD
- **RefactorAgent**: Automatiza refatoração de código usando a biblioteca Rope
- **AutoflakeAgent**: Limpa código automaticamente removendo imports não utilizados e variáveis não usadas

## Uso do AutoflakeAgent

O AutoflakeAgent permite automatizar a limpeza de código Python, removendo imports não utilizados, variáveis não usadas e expandindo imports com asterisco.

### Parâmetros

- `project_dir`: Diretório do projeto a ser analisado (obrigatório)
- `scope`: Arquivo ou diretório específico a ser limpo, relativo ao diretório do projeto (opcional)
- `aggressiveness`: Nível de agressividade - 1 (leve), 2 (moderado) ou 3 (agressivo) (padrão: 2)
- `dry_run`: Executa em modo de simulação, sem aplicar mudanças (opcional)
- `force`: Força a execução ignorando restrições de segurança (opcional)
- `output`: Arquivo de saída para o resultado da limpeza (padrão: autoflake_result.json)
- `prompt`: Descrição textual da operação (usado apenas para registro)

### Exemplo via Makefile

```bash
make start-autoflake-agent project_dir=/caminho/do/projeto scope=src/modulo aggressiveness=3 output=resultado_limpeza.json
```

### Exemplo via Linha de Comando

```bash
python src/scripts/run_autoflake_agent.py --project_dir /caminho/do/projeto --scope src/modulo --aggressiveness 3 --output resultado_limpeza.json
```

### Níveis de Agressividade

- **Leve (1)**: Remove apenas imports não utilizados
- **Moderado (2)**: Remove imports não utilizados e variáveis não usadas
- **Agressivo (3)**: Remove imports não utilizados, variáveis não usadas e expande imports com asterisco

### Modo Dry-Run

O modo dry-run permite visualizar quais mudanças seriam aplicadas sem efetivamente modificar os arquivos:

```bash
make start-autoflake-agent project_dir=/caminho/do/projeto dry_run=true
```

Para mais detalhes e exemplos, consulte a [documentação completa](docs/examples/autoflake_agent_example.md).

## Teste End-to-End do FeatureCoordinatorAgent

O comando `test-coordinator-e2e` executa um teste completo do fluxo de trabalho do FeatureCoordinatorAgent, que inclui:

1. Geração de conceito a partir de prompt
2. Transformação em feature_concept detalhado
3. Validação do plano de execução
4. Integração com GitHub (usando o repositório de teste ou mocks)

O teste utiliza o repositório https://github.com/Malnati/agent-flow-craft-e2e.git para testar a integração real com o GitHub, mas também implementa mocks para casos em que as credenciais reais não estejam disponíveis.

### Execução do Teste

```bash
make test-coordinator-e2e
```

O teste criará um ambiente temporário, clonará o repositório de teste, executará todas as etapas do fluxo e fará as verificações necessárias automaticamente.

## Licença

[Inserir informações de licença]
