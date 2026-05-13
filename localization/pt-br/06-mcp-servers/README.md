![Capítulo 06: Servidores MCP](../../../06-mcp-servers/images/chapter-header.png)

> **E se o Copilot pudesse ler seus issues do GitHub, verificar seu banco de dados e criar PRs... tudo pelo terminal?**

Até agora, o Copilot só pode trabalhar com o que você lhe dá diretamente: arquivos que você referencia com `@`, histórico de conversas e seus próprios dados de treinamento. Mas e se ele pudesse acessar por conta própria o seu repositório do GitHub, navegar pelos arquivos do projeto ou buscar a documentação mais recente de uma biblioteca?

É isso que o MCP (Model Context Protocol) faz. É uma forma de conectar o Copilot a serviços externos para que ele tenha acesso a dados ao vivo do mundo real. Cada serviço ao qual o Copilot se conecta é chamado de "servidor MCP". Neste capítulo, você configurará algumas dessas conexões e verá como elas tornam o Copilot dramaticamente mais útil.

> 💡 **Já familiarizado com MCP?** [Vá direto para o início rápido](#-use-the-built-in-github-mcp) para confirmar que está funcionando e comece a configurar servidores.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Entender o que é MCP e por que é importante
- Gerenciar servidores MCP usando comandos `/mcp`
- Configurar servidores MCP para GitHub, sistema de arquivos e documentação
- Usar fluxos de trabalho com MCP no projeto do aplicativo de livros
- Saber quando e como construir um servidor MCP personalizado (opcional)

> ⏱️ **Tempo estimado**: ~50 minutos (15 min de leitura + 35 min de prática)

---

## 🧩 Analogia com o Mundo Real: Extensões de Navegador

<img src="../../../06-mcp-servers/images/browser-extensions-analogy.png" alt="Servidores MCP são como Extensões de Navegador" width="800"/>

Pense nos servidores MCP como extensões de navegador. Seu navegador por si só pode exibir páginas web, mas as extensões o conectam a serviços extras:

| Extensão de Navegador | Com o que se Conecta | Equivalente MCP |
|----------------------|---------------------|-----------------|
| Gerenciador de senhas | Seu cofre de senhas | **GitHub MCP** → seus repositórios, issues, PRs |
| Grammarly | Serviço de análise de escrita | **Context7 MCP** → documentação de bibliotecas |
| Gerenciador de arquivos | Armazenamento na nuvem | **Filesystem MCP** → arquivos do projeto local |

Sem extensões, seu navegador ainda é útil, mas com elas ele se torna uma ferramenta poderosa. Os servidores MCP fazem o mesmo pelo Copilot. Eles o conectam a fontes de dados reais e ao vivo para que ele possa ler seus issues do GitHub, explorar seu sistema de arquivos, buscar documentação atualizada e muito mais.

***Servidores MCP conectam o Copilot ao mundo externo: GitHub, repositórios, documentação e mais***

> 💡 **Insight chave**: Sem MCP, o Copilot só consegue ver arquivos que você compartilha explicitamente com `@`. Com MCP, ele pode explorar proativamente seu projeto, verificar seu repositório GitHub e consultar documentação, tudo automaticamente.

---

<img src="../../../06-mcp-servers/images/quick-start-mcp.png" alt="Cabo de energia conectando com faísca elétrica brilhante cercado por ícones de tecnologia flutuantes representando conexões de servidor MCP" width="800"/>

# Início Rápido: MCP em 30 Segundos

## Comece com o servidor GitHub MCP integrado
Vamos ver o MCP em ação agora mesmo, antes de configurar qualquer coisa.
O servidor GitHub MCP está incluído por padrão. Experimente isto:

```bash
copilot
> List the recent commits in this repository
```

Se o Copilot retornar dados reais de commits, você acabou de ver o MCP em ação. É o servidor GitHub MCP acessando o GitHub em seu nome. Mas o GitHub é apenas *um* servidor. Este capítulo mostra como adicionar mais (acesso ao sistema de arquivos, documentação atualizada e outros) para que o Copilot possa fazer ainda mais.

---

## O Comando `/mcp show`

Use `/mcp show` para ver quais servidores MCP estão configurados e se estão habilitados:

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **Vendo apenas o servidor GitHub?** Isso é esperado! Se você ainda não adicionou nenhum servidor MCP adicional, o GitHub é o único listado. Você adicionará mais na próxima seção.

> 📚 **Quer ver todos os comandos de gerenciamento MCP?** Você pode gerenciar servidores com slash commands `/mcp` dentro do chat, ou com `copilot mcp` diretamente do terminal. Veja a [referência completa de comandos](#-additional-mcp-commands) no final deste capítulo.

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Status MCP](../../../06-mcp-servers/images/mcp-status-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

## O que Muda com MCP?

Aqui está a diferença que o MCP faz na prática:

**Sem MCP:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**Com MCP:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

O MCP torna o Copilot ciente do seu ambiente de desenvolvimento real.

> 📚 **Documentação oficial**: [Sobre MCP](https://docs.github.com/copilot/concepts/context/mcp) para uma visão mais profunda de como o MCP funciona com o GitHub Copilot.

---

# Configurando Servidores MCP

<img src="../../../06-mcp-servers/images/configuring-mcp-servers.png" alt="Mãos ajustando botões e deslizadores em uma mesa de mixagem profissional representando a configuração do servidor MCP" width="800"/>

Agora que você viu o MCP em ação, vamos configurar servidores adicionais. Você pode adicionar servidores de duas formas: **do registro integrado** (mais fácil — configuração guiada direto no CLI) ou **editando o arquivo de configuração** manualmente (mais flexível). Comece com a opção do registro se não tiver certeza de qual escolher.

---

## Instalando Servidores MCP do Registro

O CLI tem um registro de servidores MCP integrado que permite descobrir e instalar servidores populares com uma configuração guiada — sem necessidade de editar JSON.

```bash
copilot

> /mcp search
```

O Copilot abre um seletor interativo mostrando os servidores disponíveis. Selecione um e o CLI o guiará por qualquer configuração necessária (chaves de API, caminhos, etc.) e o adicionará à sua configuração automaticamente.

> 💡 **Por que usar o registro?** É a forma mais fácil de começar — você não precisa saber o nome do pacote npm, argumentos de comando ou estrutura JSON. O CLI cuida de tudo isso por você.

---

## Arquivo de Configuração MCP

Os servidores MCP são configurados em `~/.copilot/mcp-config.json` (nível de usuário, aplica-se a todos os projetos) ou `.mcp.json` (nível do projeto, colocado na raiz do seu projeto). Se você usou `/mcp search` acima, o CLI já criou ou atualizou este arquivo para você, mas é útil entender o formato para personalização.

> ⚠️ **Nota**: `.vscode/mcp.json` não é mais suportado como fonte de configuração MCP. Se você tiver um `.vscode/mcp.json` existente, migre-o para `.mcp.json` na raiz do projeto. O CLI mostrará uma dica de migração se detectar um arquivo de configuração antigo.

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*A maioria dos servidores MCP é distribuída como pacotes npm e executada via comando `npx`.*

<details>
<summary>💡 <strong>Novo em JSON?</strong> Clique aqui para aprender o que cada campo significa</summary>

| Campo | O que Significa |
|-------|----------------|
| `"mcpServers"` | Contêiner para todas as suas configurações de servidor MCP |
| `"server-name"` | Um nome que você escolhe (ex.: "github", "filesystem") |
| `"type": "local"` | O servidor é executado na sua máquina |
| `"command": "npx"` | O programa a executar (npx executa pacotes npm) |
| `"args": [...]` | Argumentos passados para o comando |
| `"tools": ["*"]` | Permitir todas as ferramentas deste servidor |

**Regras importantes de JSON:**
- Use aspas duplas `"` para strings (não aspas simples)
- Sem vírgulas finais após o último item
- O arquivo deve ser JSON válido (use um [validador JSON](https://jsonlint.com/) se não tiver certeza)

</details>

---

## Adicionando Servidores MCP

O servidor GitHub MCP é integrado e não requer configuração. Abaixo estão servidores adicionais que você pode adicionar. **Escolha o que lhe interessa, ou trabalhe neles em ordem.**

| Quero... | Ir para |
|---|---|
| Deixar o Copilot navegar pelos arquivos do meu projeto | [Servidor Filesystem](#filesystem-server) |
| Obter documentação atualizada de biblioteca | [Servidor Context7](#context7-server-documentation) |
| Explorar extras opcionais (servidores personalizados, web_fetch) | [Além do Básico](#beyond-the-basics) |

<details>
<summary><strong>Servidor Filesystem</strong> - Deixar o Copilot explorar os arquivos do projeto</summary>
<a id="filesystem-server"></a>

### Servidor Filesystem

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **O caminho `.`**: O `.` significa "diretório atual". O Copilot pode acessar arquivos relativos ao local de onde você o iniciou. Em um Codespace, este é a raiz do seu espaço de trabalho. Você também pode usar um caminho absoluto como `/workspaces/copilot-cli-for-beginners` se preferir.

Adicione isso ao seu `~/.copilot/mcp-config.json` e reinicie o Copilot.

</details>

<details>
<summary><strong>Servidor Context7</strong> - Obter documentação atualizada de bibliotecas</summary>
<a id="context7-server-documentation"></a>

### Servidor Context7 (Documentação)

O Context7 dá ao Copilot acesso a documentação atualizada de frameworks e bibliotecas populares. Em vez de depender de dados de treinamento que podem estar desatualizados, o Copilot busca a documentação atual real.

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **Sem chave de API necessária**
- ✅ **Sem conta necessária**
- ✅ **Seu código permanece local**

Adicione isso ao seu `~/.copilot/mcp-config.json` e reinicie o Copilot.

</details>

<details>
<summary><strong>Além do Básico</strong> - Servidores personalizados e acesso web (opcional)</summary>
<a id="beyond-the-basics"></a>

Esses são extras opcionais para quando você estiver confortável com os servidores principais acima.

### Servidor Microsoft Learn MCP

Todos os servidores MCP que você viu até agora (filesystem, Context7) são executados localmente na sua máquina. Mas os servidores MCP também podem ser executados remotamente, o que significa que você apenas aponta o Copilot CLI para uma URL e ele cuida do resto. Sem `npx` ou `python`, sem processo local, sem dependências para instalar.

O [Servidor Microsoft Learn MCP](https://github.com/microsoftdocs/mcp) é um bom exemplo. Ele dá ao Copilot CLI acesso direto à documentação oficial da Microsoft (Azure, Microsoft Foundry e outros tópicos de IA, .NET, Microsoft 365 e muito mais) para que ele possa pesquisar documentos, buscar páginas completas e encontrar amostras de código oficiais em vez de depender dos dados de treinamento do modelo.

- ✅ **Sem chave de API necessária**
- ✅ **Sem conta necessária**
- ✅ **Sem instalação local necessária**

**Instalação rápida com `/plugin install`:**

Em vez de editar seu arquivo de configuração JSON manualmente, você pode instalá-lo em um comando:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

Isso adiciona o servidor e suas skills de agente associadas automaticamente. As skills instaladas incluem:

- **microsoft-docs**: Conceitos, tutoriais e consultas factuais
- **microsoft-code-reference**: Consultas de API, amostras de código e solução de problemas
- **microsoft-skill-creator**: Uma meta-skill para gerar skills personalizadas sobre tecnologias Microsoft

**Uso:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 Saiba mais: [Visão geral do Servidor Microsoft Learn MCP](https://learn.microsoft.com/training/support/mcp-get-started)

### Acesso Web com `web_fetch`

O Copilot CLI inclui uma ferramenta `web_fetch` integrada que pode buscar conteúdo de qualquer URL. Isso é útil para trazer READMEs, documentação de API ou notas de versão sem sair do terminal. Sem necessidade de servidor MCP.

Você pode controlar quais URLs são acessíveis via `~/.copilot/config.json` (configurações gerais do Copilot), que é separado de `~/.copilot/mcp-config.json` (definições de servidor MCP).

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**Uso:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### Construindo um Servidor MCP Personalizado

Quer conectar o Copilot às suas próprias APIs, bancos de dados ou ferramentas internas? Você pode construir um servidor MCP personalizado em Python. Isso é completamente opcional, pois os servidores pré-construídos (GitHub, filesystem, Context7) cobrem a maioria dos casos de uso.

📖 Veja o [Guia de Servidor MCP Personalizado](mcp-custom-server.md) para um passo a passo completo usando o aplicativo de livros como exemplo.

📚 Para mais contexto, veja o [curso MCP para Iniciantes](https://github.com/microsoft/mcp-for-beginners).

</details>

<a id="complete-configuration-file"></a>

### Arquivo de Configuração Completo

Aqui está um `mcp-config.json` completo com servidores filesystem e Context7:

> 💡 **Nota:** O GitHub MCP é integrado. Você não precisa adicioná-lo ao seu arquivo de configuração.

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

Salve como `~/.copilot/mcp-config.json` para acesso global ou `.mcp.json` na raiz do projeto para configuração específica do projeto.

---

# Usando Servidores MCP

Agora que você tem servidores MCP configurados, vamos ver o que eles podem fazer.

<img src="../../../06-mcp-servers/images/using-mcp-servers.png" alt="Usando Servidores MCP - Diagrama hub-and-spoke mostrando um Developer CLI conectado a servidores GitHub, Filesystem, Context7 e Custom/Web Fetch" width="800" />

---

## Exemplos de Uso dos Servidores

**Escolha um servidor para explorar, ou trabalhe neles em ordem.**

| Quero experimentar... | Ir para |
|---|---|
| Repositórios, issues e PRs do GitHub | [Servidor GitHub](#github-server-built-in) |
| Navegação pelos arquivos do projeto | [Uso do Servidor Filesystem](#filesystem-server-usage) |
| Consulta de documentação de biblioteca | [Uso do Servidor Context7](#context7-server-usage) |
| Servidor personalizado, Microsoft Learn MCP e uso do web_fetch | [Uso do Além do Básico](#beyond-the-basics-usage) |

<details>
<summary><strong>Servidor GitHub (Integrado)</strong> - Acessar repositórios, issues, PRs e mais</summary>
<a id="github-server-built-in"></a>

### Servidor GitHub (Integrado)

O servidor GitHub MCP é **integrado**. Se você fez login no Copilot (o que você fez durante a configuração inicial), ele já funciona. Nenhuma configuração necessária!

> 💡 **Não está funcionando?** Execute `/login` para se autenticar novamente com o GitHub.

<details>
<summary><strong>Autenticação em Dev Containers</strong></summary>

- **GitHub Codespaces** (recomendado): A autenticação é automática. O CLI `gh` herda o token do Codespace. Nenhuma ação necessária.
- **Container de desenvolvimento local (Docker)**: Execute `gh auth login` após o container iniciar, depois reinicie o Copilot.

**Solução de problemas de autenticação:**
```bash
# Verificar se você está autenticado
gh auth status

# Se não, faça login
gh auth login

# Verificar se o GitHub MCP está conectado
copilot
> /mcp show
```

</details>

| Recurso | Exemplo |
|---------|---------|
| **Informações do repositório** | Ver commits, branches, contribuidores |
| **Issues** | Listar, criar, pesquisar e comentar em issues |
| **Pull requests** | Ver PRs, diffs, criar PRs, verificar status |
| **Pesquisa de código** | Pesquisar código em repositórios |
| **Actions** | Consultar execuções de fluxo de trabalho e status |

```bash
copilot

# Ver atividade recente neste repositório
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# Explorar a estrutura do repositório
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# Pesquisar padrões de código em todo o repositório
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **Trabalhando no seu próprio fork?** Se você fez fork deste repositório do curso, você também pode experimentar operações de escrita como criar issues e pull requests. Vamos praticar isso nos exercícios abaixo.

> ⚠️ **Não está vendo resultados?** O GitHub MCP opera no remoto do repositório (em github.com), não apenas em arquivos locais. Certifique-se de que seu repositório tem um remoto: execute `git remote -v` para verificar.

</details>

<details>
<summary><strong>Servidor Filesystem</strong> - Navegar e analisar arquivos do projeto</summary>
<a id="filesystem-server-usage"></a>

### Servidor Filesystem

Uma vez configurado, o filesystem MCP fornece ferramentas que o Copilot pode usar automaticamente:

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Servidor Context7</strong> - Consultar documentação de bibliotecas</summary>
<a id="context7-server-usage"></a>

### Servidor Context7

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# O Copilot agora conhece os padrões oficiais do pytest
# e pode aplicá-los a samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>Além do Básico</strong> - Servidor personalizado e uso do web_fetch</summary>
<a id="beyond-the-basics-usage"></a>

### Além do Básico

**Servidor MCP Personalizado**: Se você construiu o servidor book-lookup do [Guia de Servidor MCP Personalizado](mcp-custom-server.md), você pode consultar sua coleção de livros diretamente:

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**: Se você instalou o [servidor Microsoft Learn MCP](#microsoft-learn-mcp-server), você pode consultar a documentação oficial da Microsoft diretamente:

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: Use a ferramenta `web_fetch` integrada para trazer conteúdo de qualquer URL:

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## Fluxos de Trabalho com Múltiplos Servidores

Esses fluxos de trabalho mostram por que os desenvolvedores dizem "Nunca mais quero trabalhar sem isso." Cada exemplo combina múltiplos servidores MCP em uma única sessão.

<img src="../../../06-mcp-servers/images/issue-to-pr-workflow.png" alt="Fluxo de trabalho de Issue para PR usando MCP - Mostra o fluxo completo desde obter um issue do GitHub até criar um pull request" width="800"/>

*Fluxo de trabalho MCP completo: O GitHub MCP recupera dados do repositório, o Filesystem MCP encontra código, o Context7 MCP fornece melhores práticas e o Copilot cuida da análise*

Cada exemplo abaixo é independente. **Escolha um que lhe interesse, ou leia todos.**

| Quero ver... | Ir para |
|---|---|
| Múltiplos servidores trabalhando juntos | [Exploração com Múltiplos Servidores](#multi-server-exploration) |
| Indo de um issue a um PR em uma sessão | [Fluxo de Trabalho Issue-para-PR](#issue-to-pr-workflow) |
| Uma verificação rápida de saúde do projeto | [Painel de Saúde](#health-dashboard) |

<details>
<summary><strong>Exploração com Múltiplos Servidores</strong> - Combinar filesystem, GitHub e Context7 em uma sessão</summary>
<a id="multi-server-exploration"></a>

#### Explorando o Aplicativo de Livros com Múltiplos Servidores MCP

```bash
copilot

# Etapa 1: Usar filesystem MCP para explorar o aplicativo de livros
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Etapa 2: Usar GitHub MCP para verificar alterações recentes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Etapa 3: Usar Context7 MCP para melhores práticas
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Etapa 4: Sintetizar uma recomendação
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 Veja o fluxo de trabalho MCP em ação!</summary>

![Demo do Fluxo de Trabalho MCP](../../../06-mcp-servers/images/mcp-workflow-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

**O resultado**: Exploração de código → revisão do histórico → consulta de melhores práticas → plano de melhorias. **Tudo em uma única sessão de terminal, usando três servidores MCP juntos.**

</details>

<details>
<summary><strong>Fluxo de Trabalho Issue-para-PR</strong> - Ir de um issue do GitHub a um pull request sem sair do terminal</summary>
<a id="issue-to-pr-workflow"></a>

#### O Fluxo de Trabalho Issue-para-PR (No Seu Próprio Repositório)

Isso funciona melhor no seu próprio fork ou repositório onde você tem acesso de escrita:

> 💡 **Não se preocupe se não puder tentar isso agora.** Se você estiver em um clone somente leitura, você vai praticar isso na atividade. Por agora, apenas leia para entender o fluxo.

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[O Copilot implementa validação de ano em add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**Zero copiar e colar. Zero troca de contexto. Uma sessão de terminal.**

</details>

<details>
<summary><strong>Painel de Saúde</strong> - Obter uma verificação rápida de saúde do projeto usando múltiplos servidores</summary>
<a id="health-dashboard"></a>

#### Painel de Saúde do Aplicativo de Livros

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**O resultado**: Múltiplas fontes de dados agregadas em segundos. Manualmente, isso significaria executar grep, contar linhas, verificar git log e navegar por arquivos de teste. Facilmente 15+ minutos de trabalho.

</details>

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

**🎉 Agora você conhece o essencial!** Você entende MCP, viu como configurar servidores e viu fluxos de trabalho reais em ação. Agora é hora de experimentar você mesmo.

---

## ▶️ Experimente Você Mesmo

Agora é a sua vez! Complete estes exercícios para praticar o uso de servidores MCP com o projeto do aplicativo de livros.

### Exercício 1: Verificar o Status MCP

Comece vendo quais servidores MCP estão disponíveis:

```bash
copilot

> /mcp show
```

Você deve ver o servidor GitHub listado como habilitado. Se não, execute `/login` para se autenticar.

---

### Exercício 2: Explorar o Aplicativo de Livros com Filesystem MCP

Se você configurou o servidor filesystem, use-o para explorar o aplicativo de livros:

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**Resultado esperado**: O Copilot lista `book_app.py`, `books.py` e `utils.py` com suas funções.

> 💡 **Ainda não tem o filesystem MCP configurado?** Crie o arquivo de configuração da seção [Configuração Completa](#complete-configuration-file) acima. Então reinicie o Copilot.

---

### Exercício 3: Consultar o Histórico do Repositório com GitHub MCP

Use o GitHub MCP integrado para explorar este repositório do curso:

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**Resultado esperado**: O Copilot mostra mensagens de commit recentes e nomes de branches do remoto do GitHub.

> ⚠️ **Em um Codespace?** Isso funciona automaticamente. A autenticação é herdada. Se você estiver em um clone local, certifique-se de que `gh auth status` mostra que você está logado.

---

### Exercício 4: Combinar Múltiplos Servidores MCP

Agora combine filesystem e GitHub MCP em uma única sessão:

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**Resultado esperado**: O Copilot lê o arquivo JSON (filesystem MCP), lista os 5 livros incluindo "The Hobbit", "1984", "Dune", "To Kill a Mockingbird" e "Mysterious Book", então consulta o GitHub para o histórico de commits.

**Autoavaliação**: Você entende MCP quando consegue explicar por que "Check my repo's commit history" é melhor do que executar manualmente `git log` e colar a saída no seu prompt.

---

## 📝 Atividade

### Desafio Principal: Exploração MCP do Aplicativo de Livros

Pratique o uso de servidores MCP juntos no projeto do aplicativo de livros. Complete estas etapas em uma única sessão do Copilot:

1. **Verificar se o MCP está funcionando**: Execute `/mcp show` e confirme que pelo menos o servidor GitHub está habilitado
2. **Configurar o filesystem MCP** (se ainda não feito): Crie `~/.copilot/mcp-config.json` com a configuração do servidor filesystem
3. **Explorar o código**: Peça ao Copilot para usar o servidor filesystem para:
   - Listar todas as funções em `samples/book-app-project/books.py`
   - Verificar quais funções em `samples/book-app-project/utils.py` estão faltando dicas de tipo
   - Ler `samples/book-app-project/data.json` e identificar quaisquer problemas de qualidade de dados (dica: veja a última entrada)
4. **Verificar a atividade do repositório**: Peça ao Copilot para usar o GitHub MCP para:
   - Listar commits recentes que tocaram arquivos em `samples/book-app-project/`
   - Verificar se existem issues ou pull requests abertos
5. **Combinar servidores**: Em um único prompt, peça ao Copilot para:
   - Ler o arquivo de teste em `samples/book-app-project/tests/test_books.py`
   - Comparar as funções testadas com todas as funções em `books.py`
   - Resumir qual cobertura de teste está faltando

**Critérios de sucesso**: Você consegue combinar perfeitamente dados de filesystem e GitHub MCP em uma única sessão do Copilot, e consegue explicar o que cada servidor MCP contribuiu para a resposta.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Etapa 1: Verificar MCP**
```bash
copilot
> /mcp show
# Deve mostrar "github" como habilitado
# Se não, execute: /login
```

**Etapa 2: Criar o arquivo de configuração**

Use o JSON da seção [Configuração Completa](#complete-configuration-file) acima e salve como `~/.copilot/mcp-config.json`.

**Etapa 3: Problema de qualidade de dados para procurar**

O último livro em `data.json` é:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
Um autor vazio e ano igual a 0. Esse é o problema de qualidade de dados!

**Etapa 5: Comparação de cobertura de testes**

Os testes em `test_books.py` cobrem: `add_book`, `mark_as_read`, `remove_book`, `get_unread_books` e `find_book_by_title`. Funções como `load_books`, `save_books` e `list_books` não têm testes diretos. As funções CLI em `book_app.py` e os auxiliares em `utils.py` não têm testes.

**Se o MCP não estiver funcionando:** Reinicie o Copilot após editar o arquivo de configuração.

</details>

### Desafio Bônus: Construir um Servidor MCP Personalizado

Pronto para ir mais fundo? Siga o [Guia de Servidor MCP Personalizado](mcp-custom-server.md) para construir seu próprio servidor MCP em Python que se conecta a qualquer API.

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Não saber que o GitHub MCP é integrado | Tentar instalá-lo/configurá-lo manualmente | O GitHub MCP está incluído por padrão. Apenas tente: "List the recent commits in this repo" |
| Procurar a configuração no local errado | Não consegue encontrar ou editar as configurações MCP | A configuração de nível de usuário está em `~/.copilot/mcp-config.json`, o nível de projeto é `.mcp.json` na raiz do projeto |
| JSON inválido no arquivo de configuração | Servidores MCP falham ao carregar | Use `/mcp show` para verificar a configuração; valide a sintaxe JSON |
| Esquecer de autenticar servidores MCP | Erros de "Authentication failed" | Alguns MCPs precisam de autenticação separada. Verifique os requisitos de cada servidor |

### Solução de Problemas

**"Servidor MCP não encontrado"** - Verifique que:
1. O pacote npm existe: `npm view @modelcontextprotocol/server-github`
2. Sua configuração é JSON válido
3. O nome do servidor corresponde à sua configuração

Use `/mcp show` para ver a configuração atual.

**"Falha de autenticação do GitHub"** - O GitHub MCP integrado usa suas credenciais de `/login`. Tente:

```bash
copilot
> /login
```

Isso vai autenticá-lo novamente com o GitHub. Se os problemas persistirem, verifique se sua conta do GitHub tem as permissões necessárias para o repositório que você está acessando.

**"Servidor MCP falhou ao iniciar"** - Verifique os logs do servidor:
```bash
# Execute o comando do servidor manualmente para ver os erros
npx -y @modelcontextprotocol/server-github
```

**Ferramentas MCP não disponíveis** - Certifique-se de que o servidor está habilitado:
```bash
copilot

> /mcp show
# Verificar se o servidor está listado e habilitado
```

Se um servidor estiver desabilitado, veja os [comandos `/mcp` adicionais](#-additional-mcp-commands) abaixo para saber como reabilitá-lo.

</details>

---

<details>
<summary>📚 <strong>Comandos MCP Adicionais</strong> (clique para expandir)</summary>
<a id="-additional-mcp-commands"></a>

Você pode gerenciar servidores MCP de duas formas: usando **slash commands dentro de uma sessão de chat**, ou usando o **comando `copilot mcp` diretamente no seu terminal** (sem necessidade de sessão de chat).

### Opção 1: Slash commands (dentro de uma sessão de chat)

Esses funcionam quando você já está dentro do `copilot`:

| Comando | O que Faz |
|---------|-----------|
| `/mcp show` | Mostrar todos os servidores MCP configurados e seus status |
| `/mcp add` | Configuração interativa para adicionar um novo servidor |
| `/mcp edit <nome-do-servidor>` | Editar uma configuração de servidor existente |
| `/mcp enable <nome-do-servidor>` | Habilitar um servidor desabilitado (persiste entre sessões) |
| `/mcp disable <nome-do-servidor>` | Desabilitar um servidor (persiste entre sessões) |
| `/mcp delete <nome-do-servidor>` | Remover um servidor permanentemente |
| `/mcp auth <nome-do-servidor>` | Re-autenticar com um servidor MCP que usa OAuth (ex.: após trocar de conta) |

### Opção 2: Comando `copilot mcp` (do seu terminal)

Você também pode gerenciar servidores MCP diretamente do seu terminal sem iniciar uma sessão de chat primeiro:

```bash
# Listar todos os servidores MCP configurados
copilot mcp list

# Habilitar um servidor
copilot mcp enable filesystem

# Desabilitar um servidor
copilot mcp disable context7
```

> 💡 **Quando usar qual?** Use slash commands `/mcp` quando você já estiver em uma sessão de chat. Use `copilot mcp` do terminal quando quiser verificar ou alterar rapidamente suas configurações de servidor antes de iniciar uma sessão.

Para a maior parte deste curso, `/mcp show` é tudo que você precisa. Os outros comandos se tornam úteis à medida que você gerencia mais servidores ao longo do tempo.

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **MCP** conecta o Copilot a serviços externos (GitHub, sistema de arquivos, documentação)
2. **GitHub MCP é integrado** - sem necessidade de configuração, apenas `/login`
3. **Filesystem e Context7** são configurados via `~/.copilot/mcp-config.json`
4. **Fluxos de trabalho com múltiplos servidores** combinam dados de múltiplas fontes em uma única sessão
5. **Gerenciar servidores de duas formas**: use slash commands `/mcp` dentro do chat, ou `copilot mcp` do terminal
6. **Servidores personalizados** permitem conectar qualquer API (opcional, abordado no guia do apêndice)

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ➡️ O Que Vem a Seguir

Agora você tem todos os blocos de construção: modos, contexto, fluxos de trabalho, agentes, skills e MCP. Hora de colocá-los todos juntos.

No [**Capítulo 07: Colocando Tudo Junto**](../07-putting-it-together/README.md), você aprenderá:

- Combinar agentes, skills e MCP em fluxos de trabalho unificados
- Desenvolvimento completo de funcionalidades de ideia a PR mesclado
- Automação com hooks
- Melhores práticas para ambientes de equipe

---

[**← Voltar ao Capítulo 05**](../05-skills/README.md) | [**Continuar para o Capítulo 07 →**](../07-putting-it-together/README.md)
