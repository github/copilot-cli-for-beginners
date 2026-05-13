![Capítulo 04: Agentes e Instruções Personalizadas](../../../04-agents-custom-instructions/images/chapter-header.png)

> **E se você pudesse contratar um revisor de código Python, um especialista em testes e um revisor de segurança... tudo em uma única ferramenta?**

No Capítulo 03, você dominou os fluxos de trabalho essenciais: revisão de código, refatoração, depuração, geração de testes e integração com git. Esses recursos tornam você altamente produtivo com o GitHub Copilot CLI. Agora, vamos ir além.

Até agora, você usou o Copilot CLI como um assistente de uso geral. Os agentes permitem que você lhe dê uma persona específica com padrões integrados, como um revisor de código que aplica dicas de tipo e PEP 8, ou um assistente de testes que escreve casos pytest. Você verá como o mesmo prompt obtém resultados visivelmente melhores quando tratado por um agente com instruções direcionadas.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Usar agentes integrados: Plan (`/plan`), Code-review (`/review`) e entender agentes automáticos (Explore, Task)
- Criar agentes especializados usando arquivos de agente (`.agent.md`)
- Usar agentes para tarefas específicas de domínio
- Alternar entre agentes usando `/agent` e `--agent`
- Escrever arquivos de instruções personalizadas para padrões específicos do projeto

> ⏱️ **Tempo estimado**: ~55 minutos (20 min de leitura + 35 min de prática)

---

## 🧩 Analogia com o Mundo Real: Contratar Especialistas

Quando você precisa de ajuda com a sua casa, você não chama um "ajudante geral". Você chama especialistas:

| Problema | Especialista | Por quê |
|----------|-------------|---------|
| Cano com vazamento | Encanador | Conhece os códigos de encanamento, tem ferramentas especializadas |
| Fiação elétrica | Eletricista | Entende os requisitos de segurança, dentro das normas |
| Telhado novo | Técnico de telhados | Conhece os materiais, considerações climáticas locais |

Os agentes funcionam da mesma forma. Em vez de uma IA genérica, use agentes que se concentram em tarefas específicas e conhecem o processo certo a seguir. Configure as instruções uma vez e reutilize sempre que precisar dessa especialidade: revisão de código, testes, segurança, documentação.

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="Analogia de Contratar Especialistas - Assim como você chama profissionais especializados para reparos domésticos, os agentes de IA são especializados para tarefas específicas como revisão de código, testes, segurança e documentação" width="800" />

---

# Usando Agentes

Comece com agentes integrados e personalizados agora mesmo.

---

## *Novo em Agentes?* Comece Aqui!
Nunca usou ou criou um agente? Aqui está tudo que você precisa saber para começar neste curso.

1. **Experimente um agente *integrado* agora:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   Isso invoca o agente Plan para criar um plano de implementação passo a passo.

2. **Veja um de nossos exemplos de agente personalizado:** É simples definir as instruções de um agente, veja nosso arquivo [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) fornecido para ver o padrão.

3. **Entenda o conceito central:** Agentes são como consultar um especialista em vez de um generalista. Um "agente frontend" se concentrará em acessibilidade e padrões de componentes automaticamente, você não precisa lembrá-lo porque já está especificado nas instruções do agente.


## Agentes Integrados

**Você já usou alguns agentes integrados no Capítulo 03: Fluxos de Trabalho de Desenvolvimento!**
<br>`/plan` e `/review` são na verdade agentes integrados. Agora você sabe o que está acontecendo por baixo dos panos. Aqui está a lista completa:

| Agente | Como Invocar | O que Faz |
|--------|-------------|-----------|
| **Plan** | `/plan` ou `Shift+Tab` (alternar modos) | Cria planos de implementação passo a passo antes de codificar |
| **Code-review** | `/review` | Revisa alterações staged/unstaged com feedback focado e acionável |
| **Init** | `/init` | Gera arquivos de configuração do projeto (instruções, agentes) |
| **Explore** | *Automático* | Usado internamente quando você pede ao Copilot para explorar ou analisar a base de código |
| **Task** | *Automático* | Executa comandos como testes, builds, lints e instalações de dependências |

<br>

**Agentes integrados em ação** - Exemplos de invocação de Plan, Code-review, Explore e Task

```bash
copilot

# Invocar o agente Plan para criar um plano de implementação
> /plan Add input validation for book year in the book app

# Invocar o agente Code-review nas suas alterações
> /review

# Os agentes Explore e Task são invocados automaticamente quando relevante:
> Run the test suite        # Usa o agente Task

> Explore how book data is loaded    # Usa o agente Explore
```

E o Agente Task? Ele funciona nos bastidores para gerenciar e rastrear o que está acontecendo e relatar de volta em um formato limpo e claro:

| Resultado | O que Você Vê |
|-----------|---------------|
| ✅ **Sucesso** | Resumo breve (ex.: "All 247 tests passed", "Build succeeded") |
| ❌ **Falha** | Saída completa com rastreamentos de pilha, erros de compilador e logs detalhados |


> 📚 **Documentação oficial**: [Agentes GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Adicionando Agentes ao Copilot CLI

Você pode simplesmente definir seus próprios agentes para fazer parte do seu fluxo de trabalho! Defina uma vez, depois dirija!

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="Quatro robôs de IA coloridos juntos, cada um com ferramentas diferentes representando capacidades especializadas de agentes" width="800"/>

## 🗂️ Adicione seus agentes

Os arquivos de agente são arquivos markdown com a extensão `.agent.md`. Eles têm duas partes: frontmatter YAML (metadados) e instruções em markdown.

> 💡 **Novo em frontmatter YAML?** É um pequeno bloco de configurações no topo do arquivo, cercado por marcadores `---`. YAML são apenas pares `chave: valor`. O resto do arquivo é markdown regular.

Aqui está um agente mínimo:

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **Obrigatório vs Opcional**: O campo `description` é obrigatório. Outros campos como `name`, `tools` e `model` são opcionais.

## Onde colocar os arquivos de agente

| Local | Escopo | Melhor Para |
|-------|--------|------------|
| `.github/agents/` | Específico do projeto | Agentes compartilhados pela equipe com convenções do projeto |
| `~/.copilot/agents/` | Global (todos os projetos) | Agentes pessoais que você usa em todo lugar |

**Este projeto inclui arquivos de agente de exemplo na pasta [.github/agents/](../../../.github/agents/)**. Você pode escrever os seus próprios ou personalizar os que já foram fornecidos.

<details>
<summary>📂 Veja os agentes de exemplo neste curso</summary>

| Arquivo | Descrição |
|---------|-----------|
| `hello-world.agent.md` | Exemplo mínimo - comece aqui |
| `python-reviewer.agent.md` | Revisor de qualidade de código Python |
| `pytest-helper.agent.md` | Especialista em testes com pytest |

```bash
# Ou copie um para a sua pasta de agentes pessoais (disponível em todos os projetos)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

Para mais agentes da comunidade, veja [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 Duas formas de usar agentes personalizados

### Modo interativo
No modo interativo, liste os agentes usando `/agent` e selecione o agente com o qual você quer trabalhar.
Selecione um agente para continuar a sua conversa.

```bash
copilot
> /agent
```

Para mudar para um agente diferente, ou para retornar ao modo padrão, use o comando `/agent` novamente.

### Modo programático

Lance diretamente para uma nova sessão com um agente.

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **Trocando agentes**: Você pode mudar para um agente diferente a qualquer momento usando `/agent` ou `--agent` novamente. Para retornar à experiência padrão do Copilot CLI, use `/agent` e selecione **sem agente**.

---

# Indo Mais Fundo com Agentes

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="Robô sendo montado numa bancada cercada de componentes e ferramentas representando a criação de agentes personalizados" width="800"/>

> 💡 **Esta seção é opcional.** Os agentes integrados (`/plan`, `/review`) são poderosos o suficiente para a maioria dos fluxos de trabalho. Crie agentes personalizados quando precisar de expertise especializada que seja consistentemente aplicada em todo o seu trabalho.

Cada tópico abaixo é independente. **Escolha o que lhe interessa - você não precisa ler todos de uma vez.**

| Quero... | Ir para |
|---|---|
| Ver por que agentes superam prompts genéricos | [Especialista vs Genérico](#specialist-vs-generic-see-the-difference) |
| Combinar agentes em uma funcionalidade | [Trabalhando com Múltiplos Agentes](#working-with-multiple-agents) |
| Organizar, nomear e compartilhar agentes | [Organizando & Compartilhando Agentes](#organizing--sharing-agents) |
| Configurar contexto sempre ativo do projeto | [Configurando Seu Projeto para o Copilot](#configuring-your-project-for-copilot) |
| Consultar propriedades YAML e ferramentas | [Referência de Arquivo de Agente](#agent-file-reference) |

Selecione um cenário abaixo para expandi-lo.

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Especialista vs Genérico: Veja a Diferença</strong> - Por que agentes produzem saída melhor do que prompts genéricos</summary>

## Especialista vs Genérico: Veja a Diferença

É aqui que os agentes provam seu valor. Veja a diferença:

### Sem um Agente (Copilot Genérico)

```bash
copilot

> Add a function to search books by year range in the book app
```

**Saída genérica**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

Básico. Funciona. Mas faltando muita coisa.

---

### Com o Agente de Revisão Python

```bash
copilot

> /agent
# Selecione "python-reviewer"

> Add a function to search books by year range in the book app
```

**Saída especializada**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**O que o agente python-reviewer inclui automaticamente**:
- ✅ Dicas de tipo em todos os parâmetros e valores de retorno
- ✅ Docstring abrangente com Args/Returns/Raises
- ✅ Validação de entrada com tratamento de erros adequado
- ✅ Compreensão de lista para melhor performance
- ✅ Tratamento de casos extremos (valores de ano ausentes/inválidos)
- ✅ Formatação conforme PEP 8
- ✅ Práticas de programação defensiva

**A diferença**: O mesmo prompt, saída dramaticamente melhor. O agente traz expertise que você esqueceria de solicitar.

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Trabalhando com Múltiplos Agentes</strong> - Combinar especialistas, alternar no meio da sessão, agentes como ferramentas</summary>

## Trabalhando com Múltiplos Agentes

O verdadeiro poder vem quando especialistas trabalham juntos em uma funcionalidade.

### Exemplo: Construindo uma Funcionalidade Simples

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Usar python-reviewer para o design
> /agent
# Selecione "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Mudar para pytest-helper para o design dos testes
> /agent
# Selecione "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Sintetizar ambos os designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**O ponto-chave**: Você é o arquiteto dirigindo os especialistas. Eles cuidam dos detalhes, você cuida da visão.

<details>
<summary>🎬 Veja em ação!</summary>

![Demo do Python Reviewer](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*A saída da demo pode variar — o seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

### Agentes como Ferramentas

Quando os agentes estão configurados, o Copilot também pode chamá-los como ferramentas durante tarefas complexas. Se você pede uma funcionalidade full-stack, o Copilot pode delegar automaticamente partes para os agentes especialistas apropriados.

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizando & Compartilhando Agentes</strong> - Nomenclatura, posicionamento de arquivos, arquivos de instruções e compartilhamento com equipe</summary>

## Organizando & Compartilhando Agentes

### Nomeando Seus Agentes

Quando você cria arquivos de agente, o nome importa. É o que você digitará após `/agent` ou `--agent`, e o que seus colegas de equipe verão na lista de agentes.

| ✅ Bons Nomes | ❌ Evite |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**Convenções de nomenclatura:**
- Use letras minúsculas com hifens: `my-agent-name.agent.md`
- Inclua o domínio: `frontend`, `backend`, `devops`, `security`
- Seja específico quando necessário: `react-typescript` vs apenas `frontend`

---

### Compartilhando com Sua Equipe

Coloque os arquivos de agente em `.github/agents/` e eles ficam com controle de versão. Faça push para o seu repositório e cada membro da equipe os obtém automaticamente. Mas os agentes são apenas um tipo de arquivo que o Copilot lê do seu projeto. Ele também suporta **arquivos de instruções** que se aplicam automaticamente a cada sessão, sem que ninguém precise executar `/agent`.

Pense desta forma: agentes são especialistas que você chama, e arquivos de instruções são regras de equipe que estão sempre ativas.

### Onde Colocar Seus Arquivos

Você já conhece os dois locais principais (veja [Onde colocar os arquivos de agente](#where-to-put-agent-files) acima). Use esta árvore de decisão para escolher:

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="Árvore de decisão para onde colocar arquivos de agente: experimentando → pasta atual, uso pela equipe → .github/agents/, em todo lugar → ~/.copilot/agents/" width="800"/>

**Comece simples:** Crie um único arquivo `*.agent.md` na sua pasta do projeto. Mova-o para um local permanente quando estiver satisfeito com ele.

Além dos arquivos de agente, o Copilot também lê **arquivos de instruções de nível de projeto** automaticamente, sem necessidade de `/agent`. Veja [Configurando Seu Projeto para o Copilot](#configuring-your-project-for-copilot) abaixo para `AGENTS.md`, `.instructions.md` e `/init`.

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configurando Seu Projeto para o Copilot</strong> - AGENTS.md, arquivos de instruções e configuração /init</summary>

## Configurando Seu Projeto para o Copilot

Agentes são especialistas que você invoca sob demanda. **Arquivos de configuração do projeto** são diferentes: o Copilot os lê automaticamente em cada sessão para entender as convenções, stack tecnológica e regras do seu projeto. Ninguém precisa executar `/agent`; o contexto está sempre ativo para todos que trabalham no repositório.

### Configuração Rápida com /init

A forma mais rápida de começar é deixar o Copilot gerar os arquivos de configuração para você:

```bash
copilot
> /init
```

O Copilot vai analisar seu projeto e criar arquivos de instruções personalizados. Você pode editá-los depois.

### Formatos de Arquivo de Instruções

| Arquivo | Escopo | Observações |
|---------|--------|-------------|
| `AGENTS.md` | Raiz do projeto ou aninhado | **Padrão entre plataformas** - funciona com Copilot e outros assistentes de IA |
| `.github/copilot-instructions.md` | Projeto | Específico do GitHub Copilot |
| `.github/instructions/*.instructions.md` | Projeto | Instruções granulares e específicas por tópico |
| `CLAUDE.md`, `GEMINI.md` | Raiz do projeto | Suportados para compatibilidade |

> 🎯 **Apenas começando?** Use `AGENTS.md` para instruções do projeto. Você pode explorar os outros formatos mais tarde conforme necessário.

### AGENTS.md

`AGENTS.md` é o formato recomendado. É um [padrão aberto](https://agents.md/) que funciona no Copilot e em outras ferramentas de codificação com IA. Coloque-o na raiz do seu repositório e o Copilot o lê automaticamente. O próprio [AGENTS.md](../../../AGENTS.md) deste projeto é um exemplo funcional.

Um `AGENTS.md` típico descreve o contexto do seu projeto, estilo de código, requisitos de segurança e padrões de teste. Escreva o seu seguindo o padrão em nosso arquivo de exemplo.

### Arquivos de Instruções Personalizadas (.instructions.md)

Para equipes que querem controle mais granular, divida as instruções em arquivos específicos por tópico. Cada arquivo cobre uma preocupação e se aplica automaticamente:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **Observação**: Arquivos de instruções funcionam com qualquer linguagem. Este exemplo usa Python para corresponder ao projeto do curso, mas você pode criar arquivos similares para TypeScript, Go, Rust ou qualquer tecnologia que sua equipe usa.

**Encontrando arquivos de instruções da comunidade**: Navegue em [github/awesome-copilot](https://github.com/github/awesome-copilot) para encontrar arquivos de instruções pré-feitos cobrindo .NET, Angular, Azure, Python, Docker e muitas outras tecnologias.

### Desabilitando Instruções Personalizadas

Se você precisar que o Copilot ignore todas as configurações específicas do projeto (útil para depuração ou comparação de comportamento):

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>Referência de Arquivo de Agente</strong> - Propriedades YAML, aliases de ferramentas e exemplos completos</summary>

## Referência de Arquivo de Agente

### Um Exemplo Mais Completo

Você já viu o [formato de agente mínimo](#-adicione-seus-agentes) acima. Aqui está um agente mais completo que usa a propriedade `tools`. Crie `~/.copilot/agents/python-reviewer.agent.md`:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### Propriedades YAML

| Propriedade | Obrigatório | Descrição |
|-------------|-------------|-----------|
| `name` | Não | Nome de exibição (padrão é o nome do arquivo) |
| `description` | **Sim** | O que o agente faz - ajuda o Copilot a entender quando sugeri-lo |
| `tools` | Não | Lista de ferramentas permitidas (omitir = todas as ferramentas disponíveis). Veja aliases de ferramentas abaixo. |
| `target` | Não | Limitar apenas a `vscode` ou `github-copilot` |

### Aliases de Ferramentas

Use esses nomes na lista `tools`:
- `read` - Ler conteúdo de arquivo
- `edit` - Editar arquivos
- `search` - Pesquisar arquivos (grep/glob)
- `execute` - Executar comandos shell (também: `shell`, `Bash`)
- `agent` - Invocar outros agentes personalizados

> 📖 **Documentação oficial**: [Configuração de agentes personalizados](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **Somente VS Code**: A propriedade `model` (para selecionar modelos de IA) funciona no VS Code mas não é suportada no GitHub Copilot CLI. Você pode incluí-la com segurança em arquivos de agente multiplataforma. O GitHub Copilot CLI a ignorará.

### Mais Templates de Agente

> 💡 **Nota para iniciantes**: Os exemplos abaixo são templates. **Substitua as tecnologias específicas pelo que seu projeto usa.** O importante é a *estrutura* do agente, não as tecnologias específicas mencionadas.

Este projeto inclui exemplos funcionais na pasta [.github/agents/](../../../.github/agents/):
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - Exemplo mínimo, comece aqui
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Revisor de qualidade de código Python
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - Especialista em testes com pytest

Para agentes da comunidade, veja [github/awesome-copilot](https://github.com/github/awesome-copilot).

</details>

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Crie seus próprios agentes e veja-os em ação.

---

## ▶️ Experimente Você Mesmo

```bash

# Criar o diretório de agentes (se não existir)
mkdir -p .github/agents

# Criar um agente revisor de código
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Criar um agente de documentação
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Agora use-os
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Ou troque de agente
copilot
> /agent
# Selecione "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 Atividade

### Desafio Principal: Construir uma Equipe de Agentes Especializados

O exemplo prático criou os agentes `reviewer` e `documentor`. Agora pratique criando e usando agentes para uma tarefa diferente - melhorar a validação de dados no aplicativo de livros:

1. Crie 3 arquivos de agente (`.agent.md`) personalizados para o aplicativo de livros, um por agente, colocados em `.github/agents/`
2. Seus agentes:
   - **data-validator**: verifica `data.json` para dados ausentes ou malformados (autores vazios, ano=0, campos ausentes)
   - **error-handler**: revisa código Python para tratamento de erros inconsistente e sugere uma abordagem unificada
   - **doc-writer**: gera ou atualiza docstrings e conteúdo README
3. Use cada agente no aplicativo de livros:
   - `data-validator` → auditar `@samples/book-app-project/data.json`
   - `error-handler` → revisar `@samples/book-app-project/books.py` e `@samples/book-app-project/utils.py`
   - `doc-writer` → adicionar docstrings a `@samples/book-app-project/books.py`
4. Colabore: use `error-handler` para identificar lacunas no tratamento de erros, depois `doc-writer` para documentar a abordagem melhorada

**Critérios de sucesso**: Você tem 3 agentes funcionando que produzem saída consistente e de alta qualidade e você pode alternar entre eles com `/agent`.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Templates iniciais**: crie um arquivo por agente em `.github/agents/`:

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**Testando seus agentes:**

> 💡 **Observação:** Você já deve ter `samples/book-app-project/data.json` na sua cópia local deste repositório. Se estiver faltando, baixe a versão original do repositório fonte:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Selecione "data-validator" da lista
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**Dica:** O campo `description` no frontmatter YAML é obrigatório para os agentes funcionarem.

</details>

### Desafio Bônus: Biblioteca de Instruções

Você construiu agentes que invoca sob demanda. Agora experimente o outro lado: **arquivos de instruções** que o Copilot lê automaticamente em cada sessão, sem necessidade de `/agent`.

Crie uma pasta `.github/instructions/` com pelo menos 3 arquivos de instruções:
- `python-style.instructions.md` para aplicar convenções PEP 8 e dicas de tipo
- `test-standards.instructions.md` para aplicar convenções pytest em arquivos de teste
- `data-quality.instructions.md` para validar entradas de dados JSON

Teste cada arquivo de instruções no código do aplicativo de livros.

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Falta `description` no frontmatter do agente | O agente não vai carregar ou não será descoberto | Sempre inclua `description:` no frontmatter YAML |
| Local errado para arquivos de agente | Agente não encontrado quando você tenta usá-lo | Coloque em `~/.copilot/agents/` (pessoal) ou `.github/agents/` (projeto) |
| Usar `.md` em vez de `.agent.md` | Arquivo pode não ser reconhecido como agente | Nomeie arquivos como `python-reviewer.agent.md` |
| Prompts de agente excessivamente longos | Pode atingir o limite de 30.000 caracteres | Mantenha as definições de agente focadas; use skills para instruções detalhadas |

### Solução de Problemas

**Agente não encontrado** - Verifique se o arquivo de agente existe em um destes locais:
- `~/.copilot/agents/`
- `.github/agents/`

Liste os agentes disponíveis:

```bash
copilot
> /agent
# Mostra todos os agentes disponíveis
```

**Agente não seguindo as instruções** - Seja explícito nos seus prompts e adicione mais detalhes às definições dos agentes:
- Frameworks/bibliotecas específicos com versões
- Convenções da equipe
- Padrões de código de exemplo

**Instruções personalizadas não carregando** - Execute `/init` no seu projeto para configurar instruções específicas do projeto:

```bash
copilot
> /init
```

Ou verifique se estão desabilitadas:
```bash
# Não use --no-custom-instructions se você quiser que sejam carregadas
copilot  # Isso carrega instruções personalizadas por padrão
```

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **Agentes integrados**: `/plan` e `/review` são invocados diretamente; Explore e Task funcionam automaticamente
2. **Agentes personalizados** são especialistas definidos em arquivos `.agent.md`
3. **Bons agentes** têm expertise clara, padrões e formatos de saída
4. **Colaboração entre múltiplos agentes** resolve problemas complexos combinando expertise
5. **Arquivos de instruções** (`.instructions.md`) codificam padrões de equipe para aplicação automática
6. **Saída consistente** vem de instruções de agente bem definidas

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ➡️ O Que Vem a Seguir

Agentes mudam *como o Copilot aborda e toma ações direcionadas* no seu código. A seguir, você aprenderá sobre **skills** - que mudam *quais etapas* ele segue. Quer saber como agentes e skills diferem? O Capítulo 05 aborda isso diretamente.

No [**Capítulo 05: Sistema de Skills**](../05-skills/README.md), você aprenderá:

- Como as skills são acionadas automaticamente pelos seus prompts (sem slash command necessário)
- Instalar skills da comunidade
- Criar skills personalizadas com arquivos SKILL.md
- A diferença entre agentes, skills e MCP
- Quando usar cada um

---

[**← Voltar ao Capítulo 03**](../03-development-workflows/README.md) | [**Continuar para o Capítulo 05 →**](../05-skills/README.md)
