![Capítulo 03: Fluxos de Trabalho de Desenvolvimento](../../../03-development-workflows/images/chapter-header.png)

> **E se a IA pudesse encontrar bugs que você nem sequer sabia que devia procurar?**

Neste capítulo, o GitHub Copilot CLI se torna seu companheiro diário de trabalho. Você vai usá-lo dentro dos fluxos de trabalho com os quais você já conta todos os dias: testes, refatoração, depuração e Git.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Executar revisões de código abrangentes com o Copilot CLI
- Refatorar código legado com segurança
- Depurar problemas com assistência de IA
- Gerar testes automaticamente
- Integrar o Copilot CLI ao seu fluxo de trabalho com git

> ⏱️ **Tempo estimado**: ~60 minutos (15 min de leitura + 45 min de prática)

---

## 🧩 Analogia com o Mundo Real: O Fluxo de Trabalho de um Carpinteiro

Um carpinteiro não apenas sabe usar ferramentas, ele tem *fluxos de trabalho* para diferentes trabalhos:

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="Oficina de artesão mostrando três fluxas de trabalho: Fabricar Móveis (Medir, Cortar, Montar, Acabar), Consertar Danos (Avaliar, Remover, Reparar, Igualar) e Controle de Qualidade (Inspecionar, Testar Juntas, Verificar Alinhamento)" width="800"/>

Da mesma forma, os desenvolvedores têm fluxos de trabalho para diferentes tarefas. O GitHub Copilot CLI aprimora cada um desses fluxos de trabalho, tornando você mais eficiente e eficaz nas suas tarefas diárias de codificação.

---

# Os Cinco Fluxos de Trabalho

<img src="../../../03-development-workflows/images/five-workflows.png" alt="Cinco ícones neon brilhantes representando os fluxos de trabalho de revisão de código, testes, depuração, refatoração e integração com git" width="800"/>

Cada fluxo de trabalho abaixo é independente. Escolha os que correspondem às suas necessidades atuais, ou passe por todos eles.

---

## Escolha Seu Próprio Caminho

Este capítulo cobre cinco fluxos de trabalho que os desenvolvedores normalmente usam. **No entanto, você não precisa ler todos de uma vez!** Cada fluxo de trabalho é independente em uma seção expansível abaixo. Escolha os que melhor correspondem ao que você precisa e ao seu projeto atual. Você pode sempre voltar e explorar os outros mais tarde.

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="Cinco Fluxos de Trabalho de Desenvolvimento: Revisão de Código, Refatoração, Depuração, Geração de Testes e Integração com Git mostrados como raias horizontais" width="800"/>

| Quero... | Ir para |
|---|---|
| Revisar código antes de fazer merge | [Fluxo de Trabalho 1: Revisão de Código](#workflow-1-code-review) |
| Limpar código bagunçado ou legado | [Fluxo de Trabalho 2: Refatoração](#workflow-2-refactoring) |
| Rastrear e corrigir um bug | [Fluxo de Trabalho 3: Depuração](#workflow-3-debugging) |
| Gerar testes para meu código | [Fluxo de Trabalho 4: Geração de Testes](#workflow-4-test-generation) |
| Escrever commits e PRs melhores | [Fluxo de Trabalho 5: Integração com Git](#workflow-5-git-integration) |
| Pesquisar antes de codificar | [Dica Rápida: Pesquise Antes de Planejar ou Codificar](#quick-tip-research-before-you-plan-or-code) |
| Ver um fluxo de trabalho completo de correção de bug | [Juntando Tudo](#putting-it-all-together-bug-fix-workflow) |

**Selecione um fluxo de trabalho abaixo para expandi-lo** e veja como o GitHub Copilot CLI pode aprimorar o seu processo de desenvolvimento nessa área.

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Fluxo de Trabalho 1: Revisão de Código</strong> - Revisar arquivos, usar o agente /review, criar checklists por gravidade</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="Fluxo de trabalho de revisão de código: revisar, identificar problemas, priorizar, gerar checklist." width="800"/>

### Revisão Básica

Este exemplo usa o símbolo `@` para referenciar um arquivo, dando ao Copilot CLI acesso direto ao seu conteúdo para revisão.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Revisão de Código](../../../03-development-workflows/images/code-review-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### Revisão de Validação de Entrada

Peça ao Copilot CLI para focar sua revisão em uma preocupação específica (aqui, validação de entrada) listando as categorias que você se importa no prompt.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### Revisão de Projeto com Múltiplos Arquivos

Referencie um diretório inteiro com `@` para deixar o Copilot CLI analisar cada arquivo no projeto de uma vez.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Revisão de Código Interativa

Use uma conversa com múltiplas trocas para aprofundar. Comece com uma revisão ampla, depois faça perguntas de acompanhamento sem reiniciar.

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# O Copilot CLI fornece revisão detalhada

> The user input handling - are there any edge cases I'm missing?

# O Copilot CLI mostra problemas potenciais com strings vazias e caracteres especiais

> Create a checklist of all issues found, prioritized by severity

# O Copilot CLI gera itens de ação priorizados
```

### Modelo de Checklist de Revisão

Peça ao Copilot CLI para estruturar sua saída em um formato específico (aqui, um checklist markdown categorizado por gravidade que você pode colar em uma issue).

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Entendendo as Alterações do Git (Importante para /review)

Antes de usar o comando `/review`, você precisa entender dois tipos de alterações no git:

| Tipo de Alteração | O que Significa | Como Ver |
|-------------------|-----------------|----------|
| **Alterações staged** | Arquivos que você marcou para o próximo commit com `git add` | `git diff --staged` |
| **Alterações unstaged** | Arquivos que você modificou mas ainda não adicionou | `git diff` |

```bash
# Referência rápida
git status           # Mostra tanto staged quanto unstaged
git add file.py      # Fazer stage de um arquivo para commit
git diff             # Mostra alterações unstaged
git diff --staged    # Mostra alterações staged
```

### Usando o Comando /review

O comando `/review` invoca o **agente de revisão de código** integrado, que é otimizado para analisar alterações staged e unstaged com saída de alto sinal-ruído. Use um slash command para acionar um agente integrado especializado em vez de escrever um prompt livre.

```bash
copilot

> /review
# Invoca o agente de revisão de código em alterações staged/unstaged
# Fornece feedback focado e acionável

> /review Check for security issues in authentication
# Execute a revisão com área de foco específica
```

> 💡 **Dica**: O agente de revisão de código funciona melhor quando você tem alterações pendentes. Faça stage dos seus arquivos com `git add` para revisões mais focadas.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Fluxo de Trabalho 2: Refatoração</strong> - Reestruturar código, separar responsabilidades, melhorar o tratamento de erros</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="Fluxo de trabalho de refatoração: avaliar código, planejar alterações, implementar, verificar comportamento." width="800"/>

### Refatoração Simples

> **Experimente primeiro:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

Comece com melhorias simples. Experimente no aplicativo de livros. Cada prompt usa uma referência de arquivo com `@` combinada com uma instrução de refatoração específica para que o Copilot CLI saiba exatamente o que mudar.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **Novo em refatoração?** Comece com solicitações simples como adicionar dicas de tipo ou melhorar nomes de variáveis antes de lidar com transformações complexas.

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Refatoração](../../../03-development-workflows/images/refactor-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### Separar Responsabilidades

Referencie múltiplos arquivos com `@` em um único prompt para que o Copilot CLI possa mover código entre eles como parte da refatoração.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### Melhorar o Tratamento de Erros

Forneça dois arquivos relacionados e descreva a preocupação transversal para que o Copilot CLI possa sugerir uma correção consistente em ambos.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### Adicionar Documentação

Use uma lista detalhada de bullets para especificar exatamente o que cada docstring deve conter.

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### Refatoração Segura com Testes

Encadeie dois pedidos relacionados em uma conversa com múltiplas trocas. Primeiro gere testes, depois refatore com esses testes como rede de segurança.

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Obtenha os testes primeiro

> Now refactor the BookCollection class to use a context manager for file operations

# Refatore com confiança - os testes verificam se o comportamento é preservado
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Fluxo de Trabalho 3: Depuração</strong> - Rastrear bugs, auditorias de segurança, rastrear problemas entre arquivos</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="Fluxo de trabalho de depuração: entender o erro, localizar a causa raiz, corrigir, testar." width="800"/>

### Depuração Simples

> **Experimente primeiro:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

Comece descrevendo o que está errado. Aqui estão padrões comuns de depuração que você pode experimentar com o aplicativo de livros com bugs. Cada prompt combina uma referência de arquivo com `@` e uma descrição clara do sintoma para que o Copilot CLI possa localizar e diagnosticar o bug.

```bash
copilot

# Padrão: "Esperava X mas obtive Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Padrão: "Comportamento inesperado"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Padrão: "Resultados errados"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **Dica de depuração**: Descreva o *sintoma* (o que você vê) e a *expectativa* (o que deveria acontecer). O Copilot CLI cuida do resto.

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Correção de Bug](../../../03-development-workflows/images/fix-bug-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### O "Detetive de Bugs" - A IA Encontra Bugs RELACIONADOS

É aqui que a depuração consciente do contexto brilha. Experimente este cenário com o aplicativo de livros com bugs. Forneça o arquivo inteiro via `@` e descreva apenas o sintoma reportado pelo usuário. O Copilot CLI vai rastrear a causa raiz e pode identificar bugs adicionais nas proximidades.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**O que o Copilot CLI faz**:
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**Por que isso importa**: O Copilot CLI lê o arquivo inteiro, entende o contexto do seu relatório de bug e fornece uma correção específica com uma explicação clara.

> 💡 **Bônus**: Como o Copilot CLI analisa o arquivo inteiro, ele frequentemente descobre *outros* problemas que você não perguntou. Por exemplo, enquanto corrige a busca por autor, o Copilot CLI pode também notar o bug de sensibilidade a maiúsculas e minúsculas em `find_book_by_title`!

### Exemplo Real de Segurança

Embora depurar seu próprio código seja importante, entender vulnerabilidades de segurança em aplicações de produção é crítico. Experimente este exemplo: Aponte o Copilot CLI para um arquivo desconhecido e peça para auditar por problemas de segurança.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

Este arquivo demonstra padrões reais de segurança que você encontrará em apps de produção.

> 💡 **Termos comuns de segurança que você encontrará:**
> - **SQL Injection**: Quando a entrada do usuário é colocada diretamente em uma consulta de banco de dados, permitindo que atacantes executem comandos maliciosos
> - **Parameterized queries (consultas parametrizadas)**: A alternativa segura - espaços reservados (`?`) separam os dados do usuário dos comandos SQL
> - **Race condition (condição de corrida)**: Quando duas operações acontecem ao mesmo tempo e interferem uma na outra
> - **XSS (Cross-Site Scripting)**: Quando atacantes injetam scripts maliciosos em páginas web

---

### Entendendo um Erro

Cole um rastreamento de pilha diretamente no seu prompt junto com uma referência de arquivo `@` para que o Copilot CLI possa mapear o erro para o código-fonte.

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### Depuração com Caso de Teste

Descreva a entrada exata e a saída observada para dar ao Copilot CLI um caso de teste concreto e reproduzível para raciocinar.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### Rastrear um Problema pelo Código

Referencie múltiplos arquivos e peça ao Copilot CLI para seguir o fluxo de dados entre eles para localizar onde o problema se origina.

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### Entendendo Problemas de Dados

Inclua um arquivo de dados junto com o código que o lê para que o Copilot CLI entenda o quadro completo ao sugerir melhorias no tratamento de erros.

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>Fluxo de Trabalho 4: Geração de Testes</strong> - Gerar testes abrangentes e casos extremos automaticamente</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="Fluxo de trabalho de geração de testes: analisar função, gerar testes, incluir casos extremos, executar." width="800"/>

> **Experimente primeiro:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### A "Explosão de Testes" - 2 Testes versus 15+ Testes

Ao escrever testes manualmente, os desenvolvedores tipicamente criam 2-3 testes básicos:
- Testar entrada válida
- Testar entrada inválida
- Testar um caso extremo

Veja o que acontece quando você pede ao Copilot CLI para gerar testes abrangentes! Este prompt usa uma lista de bullets estruturada com uma referência de arquivo `@` para guiar o Copilot CLI para uma cobertura de teste completa:

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Geração de Testes](../../../03-development-workflows/images/test-gen-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**O que você obtém**: 15+ testes abrangentes incluindo:

```python
class TestBookCollection:
    # Caminho feliz
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Operações de busca
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Casos extremos
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Persistência de dados
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Caracteres especiais
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**Resultado**: Em 30 segundos, você obtém testes de casos extremos que levariam uma hora para pensar e escrever.

---

### Testes Unitários

Direcione para uma única função e enumere as categorias de entrada que você quer testar para que o Copilot CLI gere testes unitários focados e completos.

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### Executando Testes

Faça ao Copilot CLI uma pergunta em linguagem natural sobre seu conjunto de ferramentas. Ele pode gerar o comando de shell correto para você.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# O Copilot CLI responde:
# cd samples/book-app-project && python -m pytest tests/
# Ou para saída detalhada: python -m pytest tests/ -v
# Para ver instruções de print: python -m pytest tests/ -s
```

### Testar Cenários Específicos

Liste cenários avançados ou complicados que você quer cobertos para que o Copilot CLI vá além do caminho feliz.

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### Adicionar Testes a um Arquivo Existente

Peça testes *adicionais* para uma única função para que o Copilot CLI gere novos casos que complementem o que você já tem.

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>Fluxo de Trabalho 5: Integração com Git</strong> - Mensagens de commit, descrições de PR, /pr, /delegate e /diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Fluxo de trabalho de integração com git: fazer stage das alterações, gerar mensagem, fazer commit, criar PR." width="800"/>

> 💡 **Este fluxo de trabalho pressupõe familiaridade básica com git** (staging, commit, branches). Se git é novo para você, experimente os outros quatro fluxos de trabalho primeiro.

### Gerar Mensagens de Commit

> **Experimente primeiro:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — faça stage de algumas alterações, depois execute isso para ver o Copilot CLI escrever sua mensagem de commit.

Este exemplo usa o flag de prompt inline `-p` com substituição de comando de shell para canalizar a saída do `git diff` diretamente para o Copilot CLI para uma mensagem de commit em uma única execução. A sintaxe `$(...)` executa o comando dentro dos parênteses e insere sua saída no comando externo.

```bash

# Veja o que mudou
git diff --staged

# Gerar mensagem de commit usando o formato de [Commit Convencional](../../../GLOSSARY.md#conventional-commit)
# (mensagens estruturadas como "feat(books): add search" ou "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Saída: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Integração com Git](../../../03-development-workflows/images/git-integration-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### Explicar Alterações

Canalize a saída do `git show` para um prompt `-p` para obter um resumo em linguagem natural do último commit.

```bash
# O que este commit mudou?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### Descrição de PR

Combine a saída do `git log` com um modelo de prompt estruturado para gerar automaticamente uma descrição completa de pull request.

```bash
# Gerar descrição de PR a partir das alterações da branch
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### Usando /pr no Modo Interativo para a Branch Atual

Se você está trabalhando com uma branch no modo interativo do Copilot CLI, pode usar o comando `/pr` para trabalhar com pull requests. Use `/pr` para ver um PR, criar um novo PR, corrigir um PR existente, ou deixar o Copilot CLI decidir automaticamente com base no estado da branch.

```bash
copilot

> /pr [view|create|fix|auto]
```

### Revisar Antes de Enviar

Use `git diff main..HEAD` dentro de um prompt `-p` para uma verificação rápida antes do envio em todas as alterações da branch.

```bash
# Última verificação antes de enviar
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Usando /delegate para Tarefas em Segundo Plano

O comando `/delegate` passa o trabalho para o agente de nuvem do GitHub Copilot. Use o slash command `/delegate` (ou o atalho `&`) para delegar uma tarefa bem definida a um agente em segundo plano.

```bash
copilot

> /delegate Add input validation to the login form

# Ou use o atalho com prefixo &:
> & Fix the typo in the README header

# O Copilot CLI:
# 1. Faz commit das suas alterações em uma nova branch
# 2. Abre um pull request rascunho
# 3. Trabalha em segundo plano no GitHub
# 4. Solicita a sua revisão quando terminar
```

Isso é ótimo para tarefas bem definidas que você quer completadas enquanto se concentra em outro trabalho.

### Usando /diff para Revisar as Alterações da Sessão

O comando `/diff` mostra todas as alterações feitas durante a sua sessão atual. Use este slash command para ver um diff visual de tudo que o Copilot CLI modificou antes de fazer commit.

```bash
copilot

# Após fazer algumas alterações...
> /diff

# Mostra um diff visual de todos os arquivos modificados nesta sessão
# Ótimo para revisar antes de fazer commit
```

</details>

---

## Dica Rápida: Pesquise Antes de Planejar ou Codificar

Quando você precisar investigar uma biblioteca, entender melhores práticas ou explorar um tópico desconhecido, use `/research` para executar uma investigação de pesquisa profunda antes de escrever qualquer código:

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

O Copilot pesquisa repositórios do GitHub e fontes da web, depois retorna um resumo com referências. Isso é útil quando você está prestes a iniciar uma nova funcionalidade e quer tomar decisões informadas primeiro. Você pode compartilhar os resultados usando `/share`.

> 💡 **Dica**: `/research` funciona bem *antes* de `/plan`. Pesquise a abordagem, depois planeje a implementação.

---

## Juntando Tudo: Fluxo de Trabalho de Correção de Bug

Aqui está um fluxo de trabalho completo para corrigir um bug reportado:

```bash

# 1. Entender o relatório de bug
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Depurar o problema e corrigir (continuando na mesma sessão)
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. Gerar testes para a correção
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Sair da sessão interativa

> /exit

# 4. Executar git add

# Fazer stage das alterações para que git diff --staged tenha algo para trabalhar
git add .

# 5. Gerar mensagem de commit
copilot -p "Generate commit message for: $(git diff --staged)"

# Exemplo de saída: "fix(books): support partial author name search"

# 6. Fazer commit das alterações (opcional)

git commit -m "<colar a mensagem gerada>"
```

### Resumo do Fluxo de Trabalho de Correção de Bug

| Etapa | Ação | Comando Copilot |
|-------|------|-----------------|
| 1 | Entender o bug | `> [descrever o bug] @arquivo-relevante.py Analyze the likely cause` |
| 2 | Análise e correção | `> Show me the function and fix the issue` |
| 3 | Gerar testes | `> Generate tests for [cenários específicos]` |
| 4 | Fazer stage das alterações | `git add .` |
| 5 | Gerar mensagem de commit | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | Fazer commit das alterações | `git commit -m "<colar a mensagem gerada>"` |

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Agora é a sua vez de aplicar esses fluxos de trabalho.

---

## ▶️ Experimente Você Mesmo

Após concluir as demos, experimente estas variações:

1. **Desafio do Detetive de Bugs**: Peça ao Copilot CLI para depurar a função `mark_as_read` em `samples/book-app-buggy/books_buggy.py`. Ele explicou por que a função marca TODOS os livros como lidos em vez de apenas um?

2. **Desafio de Testes**: Gere testes para a função `add_book` no aplicativo de livros. Conte quantos casos extremos o Copilot CLI inclui que você não teria pensado.

3. **Desafio de Mensagem de Commit**: Faça qualquer pequena alteração em um arquivo do aplicativo de livros, faça stage com (`git add .`), depois execute:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   A mensagem é melhor do que o que você teria escrito rapidamente?

**Autoavaliação**: Você entende os fluxos de trabalho de desenvolvimento quando consegue explicar por que "depurar este bug" é mais poderoso do que "encontrar bugs" (o contexto importa!).

---

## 📝 Atividade

### Desafio Principal: Refatorar, Testar e Publicar

Os exemplos práticos focaram em `find_book_by_title` e revisões de código. Agora pratique as mesmas habilidades de fluxo de trabalho em funções diferentes do `book-app-project`:

1. **Revisar**: Peça ao Copilot CLI para revisar `remove_book()` em `books.py` para casos extremos e problemas potenciais:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **Refatorar**: Peça ao Copilot CLI para melhorar `remove_book()` para lidar com casos extremos como correspondência sem distinção de maiúsculas e minúsculas e retornar feedback útil quando um livro não for encontrado
3. **Testar**: Gere testes pytest especificamente para a função `remove_book()` melhorada, cobrindo:
   - Remover um livro que existe
   - Correspondência de título sem distinção de maiúsculas e minúsculas
   - Um livro que não existe retorna feedback apropriado
   - Remover de uma coleção vazia
4. **Revisar**: Faça stage das suas alterações e execute `/review` para verificar quaisquer problemas restantes
5. **Fazer Commit**: Gere uma mensagem de commit convencional:
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Prompts de exemplo para cada etapa:**

```bash
copilot

# Etapa 1: Revisar
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# Etapa 2: Refatorar
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# Etapa 3: Testar
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# Etapa 4: Revisar
> /review

# Etapa 5: Fazer Commit
> Generate a conventional commit message for this refactor
```

**Dica:** Após melhorar `remove_book()`, tente perguntar ao Copilot CLI: "Are there any other functions in this file that could benefit from the same improvements?". Ele pode sugerir alterações semelhantes para `find_book_by_title()` ou `find_by_author()`.

</details>

### Desafio Bônus: Criar uma aplicação com o Copilot CLI

> 💡 **Observação**: Este exercício do GitHub Skills usa **Node.js** em vez de Python. As técnicas do GitHub Copilot CLI que você vai praticar — criar issues, gerar código e colaborar pelo terminal — se aplicam a qualquer linguagem.

O exercício mostra aos desenvolvedores como usar o GitHub Copilot CLI para criar issues, gerar código e colaborar pelo terminal enquanto constroem um aplicativo calculadora em Node.js. Você vai instalar o CLI, usar templates e agentes, e praticar o desenvolvimento iterativo orientado pela linha de comando.

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> [Iniciar o Exercício Skills "Criar aplicações com o Copilot CLI"](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Usar prompts vagos como "Review this code" | Feedback genérico que perde problemas específicos | Seja específico: "Review for SQL injection, XSS, and auth issues" |
| Não usar `/review` para revisões de código | Perdendo o agente de revisão de código otimizado | Use `/review` que é ajustado para saída de alto sinal-ruído |
| Pedir para "encontrar bugs" sem contexto | O Copilot CLI não sabe qual bug você está experimentando | Descreva o sintoma: "Users report X happens when Y" |
| Gerar testes sem especificar o framework | Os testes podem usar sintaxe ou biblioteca de asserção errada | Especifique: "Generate tests using Jest" ou "using pytest" |

### Solução de Problemas

**A revisão parece incompleta** - Seja mais específico sobre o que procurar:

```bash
copilot

# Em vez de:
> Review @samples/book-app-project/book_app.py

# Tente:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**Os testes não correspondem ao meu framework** - Especifique o framework:

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**A refatoração muda o comportamento** - Peça ao Copilot CLI para preservar o comportamento:

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# Resumo

## 🔑 Principais Aprendizados

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="Fluxos de Trabalho Especializados para Cada Tarefa: Revisão de Código, Refatoração, Depuração, Testes e Integração com Git" width="800"/>

1. **A revisão de código** se torna abrangente com prompts específicos
2. **A refatoração** é mais segura quando você gera testes primeiro
3. **A depuração** se beneficia de mostrar ao Copilot CLI o erro E o código
4. **A geração de testes** deve incluir casos extremos e cenários de erro
5. **A integração com Git** automatiza mensagens de commit e descrições de PR

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ✅ Ponto de Verificação: Você Dominou os Fundamentos

**Parabéns!** Agora você tem todas as habilidades essenciais para ser produtivo com o GitHub Copilot CLI:

| Habilidade | Capítulo | Você Agora Pode... |
|------------|---------|-------------------|
| Comandos Básicos | Cap 01 | Usar o modo interativo, modo plan, modo programático (-p) e slash commands |
| Contexto | Cap 02 | Referenciar arquivos com `@`, gerenciar sessões, entender janelas de contexto |
| Fluxos de Trabalho | Cap 03 | Revisar código, refatorar, depurar, gerar testes, integrar com git |

Os Capítulos 04-06 cobrem funcionalidades adicionais que adicionam ainda mais poder e valem a pena aprender.

---

## 🛠️ Construindo Seu Fluxo de Trabalho Pessoal

Não há uma única forma "certa" de usar o GitHub Copilot CLI. Aqui estão algumas dicas enquanto você desenvolve seus próprios padrões:

> 📚 **Documentação oficial**: [Melhores práticas do Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) para fluxos de trabalho recomendados e dicas do GitHub.

- **Comece com `/plan`** para qualquer coisa não trivial. Refine o plano antes da execução — um bom plano leva a melhores resultados.
- **Salve prompts que funcionam bem.** Quando o Copilot CLI cometer um erro, anote o que deu errado. Com o tempo, isso se torna o seu manual pessoal.
- **Experimente livremente.** Alguns desenvolvedores preferem prompts longos e detalhados. Outros preferem prompts curtos com acompanhamentos. Experimente diferentes abordagens e observe o que parece natural.

> 💡 **Em breve**: Nos Capítulos 04 e 05, você aprenderá como codificar suas melhores práticas em instruções personalizadas e skills que o Copilot CLI carrega automaticamente.

---

## ➡️ O Que Vem a Seguir

Os capítulos restantes cobrem funcionalidades adicionais que estendem as capacidades do Copilot CLI:

| Capítulo | O que Abrange | Quando Você vai Querer |
|----------|---------------|------------------------|
| Cap 04: Agentes | Criar personas de IA especializadas | Quando você quiser especialistas de domínio (frontend, segurança) |
| Cap 05: Skills | Carregar instruções automaticamente para tarefas | Quando você repetir os mesmos prompts com frequência |
| Cap 06: MCP | Conectar serviços externos | Quando você precisar de dados ao vivo do GitHub, bancos de dados |

**Recomendação**: Experimente os fluxos de trabalho essenciais por uma semana, depois volte aos Capítulos 04-06 quando tiver necessidades específicas.

---

## Continuar para Tópicos Adicionais

No **[Capítulo 04: Agentes e Instruções Personalizadas](../04-agents-custom-instructions/README.md)**, você aprenderá:

- Usar agentes integrados (`/plan`, `/review`)
- Criar agentes especializados (especialista em frontend, auditor de segurança) com arquivos `.agent.md`
- Padrões de colaboração entre múltiplos agentes
- Arquivos de instruções personalizadas para padrões de projeto

---

**[← Voltar ao Capítulo 02](../02-context-conversations/README.md)** | **[Continuar para o Capítulo 04 →](../04-agents-custom-instructions/README.md)**
