![Capítulo 02: Contexto e Conversas](../../../02-context-conversations/images/chapter-header.png)

> **E se a IA pudesse ver toda a sua base de código, não apenas um arquivo de cada vez?**

Neste capítulo, você vai desbloquear o verdadeiro poder do GitHub Copilot CLI: o contexto. Você aprenderá a usar a sintaxe `@` para referenciar arquivos e diretórios, dando ao Copilot CLI um profundo entendimento da sua base de código. Você descobrirá como manter conversas entre sessões, retomar o trabalho dias depois exatamente onde parou, e verá como a análise entre múltiplos arquivos detecta bugs que revisões de arquivo único deixam escapar completamente.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Usar a sintaxe `@` para referenciar arquivos, diretórios e imagens
- Retomar sessões anteriores com `--resume` e `--continue`
- Entender como as [janelas de contexto](../../../GLOSSARY.md#context-window) funcionam
- Escrever conversas eficazes com múltiplas trocas
- Gerenciar permissões de diretório para fluxos de trabalho com múltiplos projetos

> ⏱️ **Tempo estimado**: ~50 minutos (20 min de leitura + 30 min de prática)

---

## 🧩 Analogia com o Mundo Real: Trabalhando com um Colega

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="O Contexto Faz a Diferença - Sem vs. Com Contexto" width="800"/>

*Assim como os seus colegas, o Copilot CLI não é um leitor de mentes. Fornecer mais informações ajuda tanto humanos quanto o Copilot a oferecerem suporte direcionado!*

Imagine explicar um bug a um colega:

> **Sem contexto**: "O aplicativo de livros não está funcionando."

> **Com contexto**: "Olha em `books.py`, especialmente na função `find_book_by_title`. Ela não está fazendo correspondência sem distinção de maiúsculas e minúsculas."

Para fornecer contexto ao Copilot CLI, use *a sintaxe `@`* para apontar o Copilot CLI para arquivos específicos.

---

# Essencial: Contexto Básico

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="Blocos de código brilhantes conectados por rastros de luz representando como o contexto flui pelas conversas do Copilot CLI" width="800"/>

Esta seção cobre tudo que você precisa para trabalhar eficientemente com contexto. Domine esses fundamentos primeiro.

---

## A Sintaxe @

O símbolo `@` referencia arquivos e diretórios nos seus prompts. É como você diz ao Copilot CLI "olhe para este arquivo."

> 💡 **Observação**: Todos os exemplos neste curso usam a pasta `samples/` incluída neste repositório, então você pode experimentar cada comando diretamente.

### Experimente Agora (Sem Configuração Necessária)

Você pode experimentar isso com qualquer arquivo no seu computador:

```bash
copilot

# Aponte para qualquer arquivo que você tenha
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **Não tem um projeto disponível?** Crie um arquivo de teste rápido:
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### Padrões Básicos do @

| Padrão | O que Faz | Exemplo de Uso |
|--------|-----------|----------------|
| `@file.py` | Referenciar um único arquivo | `Review @samples/book-app-project/books.py` |
| `@folder/` | Referenciar todos os arquivos em um diretório | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | Referenciar múltiplos arquivos | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### Referenciar um Único Arquivo

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Contexto de Arquivo](../../../02-context-conversations/images/file-context-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### Referenciar Múltiplos Arquivos

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### Referenciar um Diretório Inteiro

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## Inteligência Entre Arquivos

É aqui que o contexto se torna um superpoder. A análise de arquivo único é útil. A análise entre múltiplos arquivos é transformadora.

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="Inteligência Entre Arquivos - comparando análise de arquivo único versus análise entre múltiplos arquivos, mostrando como analisar arquivos juntos revela bugs, fluxo de dados e padrões invisíveis em isolamento" width="800"/>

### Demo: Encontrar Bugs que Abrangem Múltiplos Arquivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **Opção Avançada**: Para análise entre arquivos com foco em segurança, experimente os exemplos de Python com bugs:
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Múltiplos Arquivos](../../../02-context-conversations/images/multi-file-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**O que o Copilot CLI descobre**:

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**Por que isso importa**: Uma revisão de arquivo único perderia o quadro geral. Apenas a análise entre arquivos revela:
- **Código duplicado** que deveria ser consolidado
- **Padrões de fluxo de dados** mostrando como os componentes interagem
- **Problemas arquiteturais** que afetam a manutenibilidade

---

### Demo: Entender uma Base de Código em 60 Segundos

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="Comparação em tela dividida mostrando revisão manual de código levando 1 hora versus análise assistida por IA levando 10 segundos" width="800" />

Novo em um projeto? Aprenda sobre ele rapidamente usando o Copilot CLI.

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**O que você obtém**:
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**Resultado**: O que leva uma hora de leitura de código comprimido em 10 segundos. Você sabe exatamente onde focar.

---

## Exemplos Práticos

### Exemplo 1: Revisão de Código com Contexto

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# O Copilot CLI agora tem o conteúdo completo do arquivo e pode dar feedback específico:
# "Linha 49: Comparação com distinção de maiúsculas pode deixar livros passarem..."
# "Linha 29: Erros de decodificação JSON são capturados, mas a corrupção de dados não é registrada..."

> What about @samples/book-app-project/book_app.py?

# Agora revisando book_app.py, mas ainda ciente do contexto de books.py
```

### Exemplo 2: Entendendo uma Base de Código

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# O Copilot CLI lê books.py e entende a classe BookCollection

> @samples/book-app-project/ Give me an overview of the code structure

# O Copilot CLI analisa o diretório e resume

> How does the app save and load books?

# O Copilot CLI pode rastrear pelo código que já viu
```

<details>
<summary>🎬 Veja uma conversa com múltiplas trocas em ação!</summary>

![Demo de Múltiplas Trocas](../../../02-context-conversations/images/multi-turn-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

### Exemplo 3: Refatoração entre Múltiplos Arquivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# O Copilot CLI vê ambos os arquivos e pode sugerir como mesclar o código duplicado
```

---

## Gerenciamento de Sessões

As sessões são salvas automaticamente enquanto você trabalha. Você pode retomar sessões anteriores para continuar de onde parou.

### Sessões se Salvam Automaticamente

Cada conversa é salva automaticamente. Basta sair normalmente:

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... faça algum trabalho ...]

> /exit
```

### Retomar a Sessão Mais Recente

```bash
# Continue de onde parou
copilot --continue
```

### Retomar uma Sessão Específica

```bash
# Escolha de uma lista de sessões interativamente
copilot --resume

# Ou retome uma sessão específica por ID
copilot --resume=abc123

# Ou retome pelo nome que você deu à sessão
copilot --resume="my book app review"
```

> 💡 **Como encontro um ID de sessão?** Você não precisa memorizá-los. Executar `copilot --resume` sem um ID mostra uma lista interativa das suas sessões anteriores, seus nomes, IDs e quando foram usadas pela última vez. Basta escolher a que você quer.
>
> **E com múltiplos terminais?** Cada janela de terminal é sua própria sessão com seu próprio contexto. Se você tem o Copilot CLI aberto em três terminais, são três sessões separadas. Executar `--resume` a partir de qualquer terminal permite que você navegue por todas elas. O flag `--continue` pega a sessão do diretório de trabalho atual primeiro; se não houver nenhuma lá, ele pega a sessão mais recentemente ativa.
>
> **Posso trocar de sessões sem reiniciar?** Sim. Use o slash command `/resume` de dentro de uma sessão ativa:
> ```
> > /resume
> # Mostra uma lista de sessões para alternar
> ```

### Organize Suas Sessões

Dê nomes significativos às sessões para encontrá-las facilmente depois. Você pode nomear uma sessão quando a inicia, ou renomeá-la a qualquer momento dentro da sessão:

```bash
# Nomear uma sessão quando você a inicia
copilot --name book-app-review

# Ou renomear a sessão atual de dentro dela
copilot

> /rename book-app-review
# Sessão renomeada para identificação mais fácil
```

Uma vez que uma sessão tem um nome, você pode retomá-la diretamente pelo nome sem navegar por uma lista:

```bash
copilot --resume=book-app-review
```

Para limpar sessões que você não precisa mais, use `/session delete` de dentro de uma sessão:

```bash
copilot

> /session delete            # Exclui a sessão atual
> /session delete abc123     # Exclui uma sessão específica por ID
> /session delete-all        # Exclui todas as sessões (use com cuidado!)
```

### Verificar e Gerenciar o Contexto

À medida que você adiciona arquivos e conversa, a [janela de contexto](../../../GLOSSARY.md#context-window) do Copilot CLI vai se preenchendo. Vários comandos estão disponíveis para ajudá-lo a manter o controle:

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandona a sessão atual (sem histórico salvo) e inicia uma nova conversa

> /new
# Encerra a sessão atual (salvando-a no histórico para busca/retomada) e inicia uma nova conversa

> /rewind
# Abre um seletor de linha do tempo permitindo que você retorne a um ponto anterior da conversa
```

> 💡 **Quando usar `/clear` ou `/new`**: Se você estava revisando books.py e quer mudar para discutir utils.py, execute /new primeiro (ou /clear se não precisar do histórico da sessão). Caso contrário, o contexto obsoleto do assunto anterior pode confundir as respostas.

> 💡 **Cometeu um erro ou quer tentar uma abordagem diferente?** Use `/rewind` (ou pressione Esc duas vezes) para abrir um **seletor de linha do tempo** que permite que você volte a qualquer ponto anterior da sua conversa, não apenas ao mais recente. Isso é útil quando você tomou o caminho errado e quer voltar atrás sem começar do zero.

---

### Continue de Onde Parou

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="Linha do tempo mostrando como as sessões do GitHub Copilot CLI persistem por dias - comece na segunda-feira, retome na quarta-feira com todo o contexto restaurado" width="800"/>

*As sessões são salvas automaticamente quando você sai. Retome dias depois com contexto completo: arquivos, problemas e progresso, todos lembrados.*

Imagine este fluxo de trabalho ao longo de múltiplos dias:

```bash
# Segunda-feira: Iniciar revisão do aplicativo de livros com um nome já no início
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# Trabalhar na correção...

> /exit
```

```bash
# Quarta-feira: Retome exatamente de onde parou, pelo nome
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**O que torna isso poderoso**: Dias depois, o Copilot CLI lembra:
- O arquivo exato em que você estava trabalhando
- A lista numerada de problemas
- Quais você já resolveu
- O contexto da sua conversa

Sem precisar explicar novamente. Sem precisar reler arquivos. Apenas continue trabalhando.

---

**🎉 Agora você conhece os fundamentos!** A sintaxe `@`, o gerenciamento de sessões (`--name`/`--continue`/`--resume`/`/rename`) e os comandos de contexto (`/context`/`/clear`) são suficientes para ser altamente produtivo. Tudo abaixo é opcional. Volte a isso quando estiver pronto.

---

# Opcional: Indo Mais Fundo

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="Caverna de cristal abstrata em tons de azul e roxo representando exploração mais profunda dos conceitos de contexto" width="800"/>

Esses tópicos se baseiam nos fundamentos acima. **Escolha o que lhe interessa ou pule para [Prática](#practice).**

| Quero aprender sobre... | Ir para |
|---|---|
| Padrões de curinga e comandos avançados de sessão | [Padrões @ Adicionais & Comandos de Sessão](#additional-patterns) |
| Construir sobre contexto em múltiplos prompts | [Conversas Conscientes do Contexto](#context-aware-conversations) |
| Limites de tokens e `/compact` | [Entendendo as Janelas de Contexto](#understanding-context-windows) |
| Como escolher os arquivos certos para referenciar | [Escolhendo o que Referenciar](#choosing-what-to-reference) |
| Analisar capturas de tela e mockups | [Trabalhando com Imagens](#working-with-images) |

<details>
<summary><strong>Padrões @ Adicionais & Comandos de Sessão</strong></summary>
<a id="additional-patterns"></a>

### Padrões @ Adicionais

Para usuários avançados, o Copilot CLI suporta padrões de curinga e referências de imagens:

| Padrão | O que Faz |
|--------|-----------|
| `@folder/*.py` | Todos os arquivos .py na pasta |
| `@**/test_*.py` | Curinga recursivo: encontrar todos os arquivos de teste em qualquer lugar |
| `@image.png` | Arquivo de imagem para revisão de UI |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### Ver Informações da Sessão

```bash
copilot

> /session
# Mostra detalhes da sessão atual e resumo do espaço de trabalho

> /usage
# Mostra métricas e estatísticas da sessão
```

### Compartilhar Sua Sessão

```bash
copilot

> /share file ./my-session.md
# Exporta a sessão como um arquivo markdown

> /share gist
# Cria um GitHub gist com a sessão

> /share html
# Exporta a sessão como um arquivo HTML interativo independente
# Útil para compartilhar relatórios de sessão polidos com colegas ou salvar para referência
```

</details>

<details>
<summary><strong>Conversas Conscientes do Contexto</strong></summary>
<a id="context-aware-conversations"></a>

### Conversas Conscientes do Contexto

A mágica acontece quando você tem conversas com múltiplas trocas que se baseiam umas nas outras.

#### Exemplo: Aprimoramento Progressivo

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[Shows typed version]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[Adds validation and proper exceptions]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[Generates comprehensive tests]
```

Perceba como cada prompt se baseia no trabalho anterior. Este é o poder do contexto.

</details>

<details>
<summary><strong>Entendendo as Janelas de Contexto</strong></summary>
<a id="understanding-context-windows"></a>

### Entendendo as Janelas de Contexto

Você já conhece `/context` e `/clear` dos fundamentos. Aqui está a visão mais profunda de como as janelas de contexto funcionam.

Toda IA tem uma "janela de contexto", que é a quantidade de texto que ela pode considerar de uma vez.

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="Visualização da Janela de Contexto" width="800"/>

*A janela de contexto é como uma mesa: ela só pode conter uma quantidade limitada de coisas de uma vez. Arquivos, histórico de conversa e prompts de sistema ocupam espaço.*

#### O que Acontece no Limite

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# À medida que você adiciona mais arquivos e conversa, isso cresce

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Aviso: Aproximando-se do limite de contexto

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### O Comando `/compact`

Quando seu contexto está ficando cheio, mas você não quer perder a conversa, `/compact` resume seu histórico para liberar tokens:

```bash
copilot

> /compact
# Resume o histórico da conversa, liberando espaço de contexto
# Suas principais descobertas e decisões são preservadas
```

#### Dicas de Eficiência de Contexto

| Situação | Ação | Por quê |
|----------|------|---------|
| Começando um novo assunto | `/clear` | Remove contexto irrelevante |
| Tomou o caminho errado | `/rewind` | Voltar a qualquer ponto anterior |
| Conversa longa | `/compact` | Resume o histórico, libera tokens |
| Precisa de um arquivo específico | `@file.py` e não `@folder/` | Carrega apenas o que você precisa |
| Atingindo limites | `/new` ou `/clear` | Contexto fresco |
| Múltiplos assuntos | Use `/rename` por assunto | Fácil de retomar a sessão certa |

#### Melhores Práticas para Bases de Código Grandes

1. **Seja específico**: `@samples/book-app-project/books.py` em vez de `@samples/book-app-project/`
2. **Limpe o contexto entre assuntos**: Use `/new` ou `/clear` ao trocar de foco
3. **Use `/compact`**: Resume a conversa para liberar contexto
4. **Use múltiplas sessões**: Uma sessão por funcionalidade ou assunto

</details>

<details>
<summary><strong>Escolhendo o que Referenciar</strong></summary>
<a id="choosing-what-to-reference"></a>

### Escolhendo o que Referenciar

Nem todos os arquivos são iguais quando se trata de contexto. Veja como escolher sabiamente:

#### Considerações sobre Tamanho de Arquivo

| Tamanho do Arquivo | [Tokens](../../../GLOSSARY.md#token) Aproximados | Estratégia |
|-------------------|--------------------------------------------------|-----------|
| Pequeno (<100 linhas) | ~500-1.500 tokens | Referencie livremente |
| Médio (100-500 linhas) | ~1.500-7.500 tokens | Referencie arquivos específicos |
| Grande (500+ linhas) | 7.500+ tokens | Seja seletivo, use arquivos específicos |
| Muito Grande (1000+ linhas) | 15.000+ tokens | Considere dividir ou direcionar seções |

**Exemplos concretos:**
- Os 4 arquivos Python do aplicativo de livros combinados ≈ 2.000-3.000 tokens
- Um módulo Python típico (200 linhas) ≈ 3.000 tokens
- Um arquivo Flask API (400 linhas) ≈ 6.000 tokens
- Seu package.json ≈ 200-500 tokens
- Um prompt + resposta curtos ≈ 500-1.500 tokens

> 💡 **Estimativa rápida para código:** Multiplique as linhas de código por ~15 para obter tokens aproximados. Tenha em mente que esta é apenas uma estimativa.

#### O que Incluir vs. Excluir

**Alto valor** (inclua estes):
- Pontos de entrada (`book_app.py`, `main.py`, `app.py`)
- Os arquivos específicos sobre os quais você está perguntando
- Arquivos diretamente importados pelo seu arquivo alvo
- Arquivos de configuração (`requirements.txt`, `pyproject.toml`)
- Modelos de dados ou dataclasses

**Menor valor** (considere excluir):
- Arquivos gerados (saída compilada, assets empacotados)
- Módulos Node ou diretórios de fornecedor
- Arquivos de dados grandes ou fixtures
- Arquivos não relacionados à sua pergunta

#### O Espectro de Especificidade

```
Menos específico ────────────────────────► Mais específico
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ Analisa tudo                          └─ Apenas o que você precisa
        (usa mais contexto)                       (preserva contexto)
```

**Quando ir amplo** (`@samples/book-app-project/`):
- Exploração inicial da base de código
- Encontrar padrões em muitos arquivos
- Revisões de arquitetura

**Quando ir específico** (`@samples/book-app-project/books.py`):
- Depurar um problema específico
- Revisão de código de um arquivo específico
- Perguntar sobre uma única função

#### Exemplo Prático: Carregamento de Contexto Gradual

```bash
copilot

# Etapa 1: Começar com a estrutura
> @package.json What frameworks does this project use?

# Etapa 2: Estreitar com base na resposta
> @samples/book-app-project/ Show me the project structure

# Etapa 3: Focar no que importa
> @samples/book-app-project/books.py Review the BookCollection class

# Etapa 4: Adicionar arquivos relacionados somente quando necessário
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

Esta abordagem gradual mantém o contexto focado e eficiente.

</details>

<details>
<summary><strong>Trabalhando com Imagens</strong></summary>
<a id="working-with-images"></a>

### Trabalhando com Imagens

Você pode incluir imagens nas suas conversas usando a sintaxe `@`, ou simplesmente **colar da área de transferência** (Cmd+V / Ctrl+V). O Copilot CLI pode analisar capturas de tela, mockups e diagramas para ajudar com depuração de UI, implementação de design e análise de erros.

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **Saiba mais**: Veja [Funcionalidades Adicionais de Contexto](../appendices/additional-context.md#working-with-images) para formatos suportados, casos de uso práticos e dicas para combinar imagens com código.

</details>

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Hora de aplicar suas habilidades de contexto e gerenciamento de sessões.

---

## ▶️ Experimente Você Mesmo

### Revisão Completa do Projeto

O curso inclui arquivos de exemplo que você pode revisar diretamente. Inicie o copilot e execute o prompt mostrado a seguir:

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# O Copilot CLI identificará problemas como:
# - Funções de exibição duplicadas
# - Validação de entrada ausente
# - Tratamento de erros inconsistente
```

> 💡 **Quer tentar com seus próprios arquivos?** Crie um pequeno projeto Python (`mkdir -p my-project/src`), adicione alguns arquivos .py e depois use `@my-project/src/` para revisá-los. Você pode pedir ao copilot para criar código de exemplo se quiser!

### Fluxo de Trabalho de Sessão

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[O Copilot CLI sugere abordagem de validação]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# Mais tarde - retome de onde parou
copilot --continue

> Generate tests for the changes we made
```

---

Após concluir as demos, experimente estas variações:

1. **Desafio Entre Arquivos**: Analise como book_app.py e books.py trabalham juntos:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **Desafio de Sessão**: Inicie uma sessão, nomeie-a com `/rename my-first-session`, faça alguma coisa, saia com `/exit` e execute `copilot --continue`. Ela lembra o que você estava fazendo?

3. **Desafio de Contexto**: Execute `/context` no meio de uma sessão. Quantos tokens você está usando? Experimente `/compact` e verifique novamente. (Veja [Entendendo as Janelas de Contexto](#understanding-context-windows) em Indo Mais Fundo para mais sobre `/compact`.)

**Autoavaliação**: Você entende o contexto quando consegue explicar por que `@folder/` é mais poderoso do que abrir cada arquivo individualmente.

---

## 📝 Atividade

### Desafio Principal: Rastrear o Fluxo de Dados

Os exemplos práticos focaram em revisões de qualidade de código e validação de entrada. Agora pratique as mesmas habilidades de contexto em uma tarefa diferente, rastreando como os dados se movem pelo aplicativo:

1. Inicie uma sessão interativa: `copilot`
2. Referencie `books.py` e `book_app.py` juntos:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. Traga o arquivo de dados para contexto adicional:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. Peça uma melhoria entre arquivos:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. Renomeie a sessão: `/rename data-flow-analysis`
6. Saia com `/exit`, então retome com `copilot --continue` e faça uma pergunta de acompanhamento sobre o fluxo de dados

**Critérios de sucesso**: Você consegue rastrear dados entre múltiplos arquivos, retomar uma sessão nomeada e obter sugestões entre arquivos.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Como começar:**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

Então retome com: `copilot --continue`

**Comandos úteis:**
- `@file.py` - Referenciar um único arquivo
- `@folder/` - Referenciar todos os arquivos em uma pasta (observe a `/` no final)
- `/context` - Verificar quanto contexto você está usando
- `/rename <nome>` - Nomear sua sessão para fácil retomada

</details>

### Desafio Bônus: Limites de Contexto

1. Referencie todos os arquivos do aplicativo de livros de uma vez com `@samples/book-app-project/`
2. Faça várias perguntas detalhadas sobre arquivos diferentes (`books.py`, `utils.py`, `book_app.py`, `data.json`)
3. Execute `/context` para ver o uso. Quão rapidamente ele se preenche?
4. Pratique usar `/compact` para recuperar espaço e continue a conversa
5. Tente ser mais específico com referências de arquivo (ex.: `@samples/book-app-project/books.py` em vez de toda a pasta) e veja como afeta o uso de contexto

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Esquecer o `@` antes dos nomes de arquivo | O Copilot CLI trata "books.py" como texto simples | Use `@samples/book-app-project/books.py` para referenciar arquivos |
| Esperar que as sessões persistam automaticamente | Iniciar o `copilot` do zero perde todo o contexto anterior | Use `--continue` (última sessão) ou `--resume` (escolher uma sessão) |
| Referenciar arquivos fora do diretório atual | Erros de "Permissão negada" ou "Arquivo não encontrado" | Use `/add-dir /caminho/para/diretório` para conceder acesso |
| Não usar `/clear` ao trocar de assunto | Contexto antigo confunde respostas sobre o novo assunto | Execute `/clear` antes de iniciar uma tarefa diferente |

### Solução de Problemas

**Erros de "Arquivo não encontrado"** - Certifique-se de estar no diretório correto:

```bash
pwd  # Verificar diretório atual
ls   # Listar arquivos

# Então inicie o copilot e use caminhos relativos
copilot

> Review @samples/book-app-project/books.py
```

**"Permissão negada"** - Adicione o diretório à sua lista de permitidos:

```bash
copilot --add-dir /caminho/para/diretório

# Ou em uma sessão:
> /add-dir /caminho/para/diretório
```

**O contexto se preenche muito rápido**:
- Seja mais específico com referências de arquivo
- Use `/clear` entre diferentes assuntos
- Divida o trabalho em múltiplas sessões

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **A sintaxe `@`** fornece ao Copilot CLI contexto sobre arquivos, diretórios e imagens
2. **As conversas com múltiplas trocas** se baseiam umas nas outras à medida que o contexto se acumula
3. **As sessões são salvas automaticamente**: nomeie-as na inicialização com `--name`, retome pelo nome com `--resume=<nome>`, ou use `--continue` para pegar a sessão mais recente
4. **As janelas de contexto** têm limites: gerencie-as com `/clear`, `/compact`, `/context`, `/new` e `/rewind`
5. **Os flags de permissão** (`--add-dir`, `--allow-all`) controlam o acesso a múltiplos diretórios. Use-os sabiamente!
6. **As referências de imagem** (`@screenshot.png`) ajudam a depurar problemas de UI visualmente

> 📚 **Documentação oficial**: [Usar o Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) para a referência completa sobre contexto, sessões e trabalho com arquivos.

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ➡️ O Que Vem a Seguir

Agora que você pode fornecer contexto ao Copilot CLI, vamos colocá-lo para trabalhar em tarefas reais de desenvolvimento. As técnicas de contexto que você acabou de aprender (referências de arquivo, análise entre arquivos e gerenciamento de sessões) são a base para os fluxos de trabalho poderosos do próximo capítulo.

No **[Capítulo 03: Fluxos de Trabalho de Desenvolvimento](../03-development-workflows/README.md)**, você aprenderá:

- Fluxos de trabalho de revisão de código
- Padrões de refatoração
- Assistência na depuração
- Geração de testes
- Integração com Git

---

**[← Voltar ao Capítulo 01](../01-setup-and-first-steps/README.md)** | **[Continuar para o Capítulo 03 →](../03-development-workflows/README.md)**
