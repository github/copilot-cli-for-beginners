![Capítulo 01: Primeiros Passos](../../../01-setup-and-first-steps/images/chapter-header.png)

> **Veja a IA encontrar bugs instantaneamente, explicar código confuso e gerar scripts funcionais. Depois aprenda três formas diferentes de usar o GitHub Copilot CLI.**

Este capítulo é onde a mágica começa! Você vai experimentar em primeira mão por que os desenvolvedores descrevem o GitHub Copilot CLI como ter um engenheiro sênior disponível a qualquer hora. Você verá a IA encontrar bugs de segurança em segundos, terá código complexo explicado em linguagem simples e gerará scripts funcionais instantaneamente. Em seguida, você dominará os três modos de interação (Interativo, Plan e Programático) para saber exatamente qual usar para cada tarefa.

> ⚠️ **Pré-requisitos**: Certifique-se de ter concluído o **[Capítulo 00: Início Rápido](../00-quick-start/README.md)** primeiro. Você precisará do GitHub Copilot CLI instalado e autenticado antes de executar as demos abaixo.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Experimentar o aumento de produtividade que o GitHub Copilot CLI proporciona por meio de demos práticas
- Escolher o modo certo (Interativo, Plan ou Programático) para qualquer tarefa
- Usar slash commands para controlar suas sessões

> ⏱️ **Tempo estimado**: ~45 minutos (15 min de leitura + 30 min de prática)

---

# Sua Primeira Experiência com o Copilot CLI

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="Desenvolvedor sentado em uma mesa com código no monitor e partículas brilhantes representando a assistência de IA" width="800"/>

Mergulhe de cabeça e veja o que o Copilot CLI pode fazer.

---

## Começando com Conforto: Seus Primeiros Prompts

Antes de mergulhar nas demos impressionantes, vamos começar com alguns prompts simples que você pode experimentar agora mesmo. **Nenhum repositório de código necessário**! Basta abrir um terminal e iniciar o Copilot CLI:

```bash
copilot
```

Experimente estes prompts para iniciantes:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Não usa Python? Sem problema! Basta fazer perguntas sobre a linguagem de sua preferência.

Perceba como parece natural. Basta fazer perguntas como você faria a um colega. Quando terminar de explorar, digite `/exit` para encerrar a sessão.

**O ponto-chave**: O GitHub Copilot CLI é conversacional. Você não precisa de uma sintaxe especial para começar. Apenas faça perguntas em linguagem natural.

## Veja em Ação

Agora vamos ver por que os desenvolvedores chamam isso de "ter um engenheiro sênior disponível a qualquer hora."

> 📖 **Lendo os Exemplos**: Linhas começando com `>` são prompts que você digita dentro de uma sessão interativa do Copilot CLI. Linhas sem o prefixo `>` são comandos de shell que você executa no seu terminal.

> 💡 **Sobre as Saídas de Exemplo**: As saídas de exemplo mostradas ao longo deste curso são ilustrativas. Como as respostas do Copilot CLI variam a cada vez, os seus resultados diferirão em redação, formatação e detalhes. Concentre-se no *tipo* de informação retornada, não no texto exato.

### Demo 1: Revisão de código em segundos

O curso inclui arquivos de exemplo com problemas de qualidade de código intencionais. Se você está trabalhando na sua máquina local e ainda não clonou o repositório, execute o comando `git clone` abaixo, navegue até a pasta `copilot-cli-for-beginners` e então execute o comando `copilot`.

```bash
# Clone o repositório do curso se estiver trabalhando localmente e ainda não tiver feito isso
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Inicie o Copilot
copilot
```

Dentro da sessão interativa do Copilot CLI, execute o seguinte:

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **Para que serve o símbolo `@`?** O símbolo `@` diz ao Copilot CLI para ler um arquivo. Você aprenderá tudo sobre isso no Capítulo 02. Por enquanto, apenas copie o comando exatamente como mostrado.

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Revisão de Código](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**O ponto-chave**: Uma revisão de código profissional em segundos. A revisão manual levaria... bem... mais tempo do que isso!

---

### Demo 2: Explicar código confuso

Já ficou olhando para um código sem entender o que ele faz? Experimente isso na sua sessão do Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Explicação de Código](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**O que acontece**: (a sua saída pode diferir) O Copilot CLI lê o arquivo, entende o código e o explica em linguagem simples.

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**O ponto-chave**: Código complexo explicado como um mentor paciente o explicaria.

---

### Demo 3: Gerar código funcional

Precisa de uma função para a qual normalmente gastaria 15 minutos pesquisando? Ainda na sua sessão:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Geração de Código](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**O que acontece**: Uma função completa e funcional em segundos que você pode copiar, colar e executar.

Quando terminar de explorar, saia da sessão:

```
> /exit
```

**O ponto-chave**: Gratificação instantânea, e você permaneceu em uma única sessão contínua o tempo todo.

---

# Modos e Comandos

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="Painel de controle futurista com telas brilhantes, mostradores e equalizadores representando os modos e comandos do Copilot CLI" width="800"/>

Você acabou de ver o que o Copilot CLI pode fazer. Agora vamos entender *como* usar essas capacidades com eficiência. A chave está em saber qual dos três modos de interação usar para diferentes situações.

> 💡 **Observação**: O Copilot CLI também possui um modo **Autopilot** (piloto automático) onde ele executa tarefas sem esperar pela sua entrada. É poderoso, mas requer a concessão de permissões totais e usa requisições premium de forma autônoma. Este curso se concentra nos três modos abaixo. Vamos indicar o Autopilot quando você estiver confortável com o básico.

---

## 🧩 Analogia com o Mundo Real: Jantar Fora

Pense em usar o GitHub Copilot CLI como sair para jantar. Do planejamento da viagem ao pedido, situações diferentes pedem abordagens diferentes:

| Modo | Analogia do Jantar | Quando Usar |
|------|--------------------|-------------|
| **Plan** | GPS até o restaurante | Tarefas complexas - trace o caminho, revise as paradas, concorde com o plano, depois execute |
| **Interactive** | Conversar com o garçom | Exploração e iteração - faça perguntas, personalize, receba feedback em tempo real |
| **Programmatic** | Pedido no drive-through | Tarefas rápidas e específicas - fique no seu ambiente, obtenha um resultado rápido |

Assim como sair para jantar, você vai aprender naturalmente quando cada abordagem faz sentido.

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="Três Formas de Usar o GitHub Copilot CLI - Modo Plan (GPS até o restaurante), Modo Interativo (conversar com o garçom), Modo Programático (drive-through)" width="800"/>

*Escolha o seu modo com base na tarefa: Plan para mapear primeiro, Interactive para colaboração de ida e volta, Programmatic para resultados rápidos em uma única tentativa*

### Qual Modo Devo Usar Primeiro?

**Comece com o modo Interativo.**
- Você pode experimentar e fazer perguntas de acompanhamento
- O contexto se constrói naturalmente através da conversa
- Erros são fáceis de corrigir com `/clear`

Quando estiver confortável, experimente:
- **Modo Programático** (`copilot -p "<seu prompt>"`) para perguntas rápidas e pontuais
- **Modo Plan** (`/plan`) quando precisar planejar as coisas em mais detalhes antes de codificar

---

## Os Três Modos

### Modo 1: Modo Interativo (comece aqui)

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="Modo Interativo - Como conversar com um garçom que pode responder perguntas e ajustar o pedido" width="250"/>

**Melhor para**: Exploração, iteração, conversas com múltiplas trocas. Como conversar com um garçom que pode responder perguntas, receber feedback e ajustar o pedido em tempo real.

Inicie uma sessão interativa:

```bash
copilot
```

Como você já viu até aqui, aparecerá um prompt onde você pode digitar naturalmente. Para obter ajuda sobre os comandos disponíveis, basta digitar:

```
> /help
```

**Ponto-chave**: O modo Interativo mantém o contexto. Cada mensagem se baseia nas anteriores, assim como uma conversa real.

#### Exemplo do Modo Interativo

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Perceba como cada prompt se baseia na resposta anterior. Você está tendo uma conversa, não recomeçando do zero a cada vez.

---

### Modo 2: Modo Plan

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="Modo Plan - Como planejar uma rota antes de uma viagem usando GPS" width="250"/>

**Melhor para**: Tarefas complexas onde você quer revisar a abordagem antes da execução. Similar a planejar uma rota antes de uma viagem usando GPS.

O modo Plan ajuda você a criar um plano passo a passo antes de escrever qualquer código. Use o comando `/plan` ou pressione **Shift+Tab** para alternar para o Modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Dica**: **Shift+Tab** alterna entre modos: Interativo → Plan → Autopilot. Pressione a qualquer momento durante uma sessão interativa para mudar de modo sem digitar um comando.

Você também pode lançar o Copilot CLI diretamente no modo plan usando o flag `--plan`:

```bash
copilot --plan
```

**Saída do modo plan:** (a sua saída pode diferir)

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**Ponto-chave**: O modo Plan permite revisar e modificar a abordagem antes que qualquer código seja escrito. Quando um plano estiver completo, você pode até dizer ao Copilot CLI para salvá-lo em um arquivo para referência posterior. Por exemplo, "Save this plan to `mark_as_read_plan.md`" criaria um arquivo markdown com os detalhes do plano.

> 💡 **Quer algo mais complexo?** Experimente: `/plan Add search and filter capabilities to the book app`. O modo Plan escala desde funcionalidades simples até aplicações completas.

> 📚 **Modo Autopilot**: Você pode ter notado que Shift+Tab alterna para um terceiro modo chamado **Autopilot**. No modo Autopilot, o Copilot trabalha em um plano completo sem esperar pela sua entrada a cada etapa — como delegar uma tarefa a um colega e dizer "me avise quando terminar." O fluxo de trabalho típico é plan → aceitar → autopilot, o que significa que você precisa ser bom em escrever planos primeiro. Você também pode lançar diretamente no modo autopilot com `copilot --autopilot`. Fique confortável com os modos Interativo e Plan primeiro, depois consulte a [documentação oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) quando estiver pronto.

---

### Modo 3: Modo Programático

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="Modo Programático - Como usar um drive-through para um pedido rápido" width="250"/>

**Melhor para**: Automação, scripts, CI/CD, comandos de uma única execução. Como usar um drive-through para um pedido rápido sem precisar conversar com um garçom.

Use o flag `-p` para comandos pontuais que não precisam de interação:

```bash
# Gerar código
copilot -p "Write a function that checks if a number is even or odd"

# Obter ajuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Ponto-chave**: O modo Programático fornece uma resposta rápida e sai. Sem conversa, apenas entrada → saída.

<details>
<summary>📚 <strong>Indo Além: Usando o Modo Programático em Scripts</strong> (clique para expandir)</summary>

Quando estiver confortável, você pode usar `-p` em scripts de shell:

```bash
#!/bin/bash

# Gerar mensagens de commit automaticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar um arquivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Sobre `--allow-all`**: Este flag ignora todos os prompts de permissão, permitindo que o Copilot CLI leia arquivos, execute comandos e acesse URLs sem pedir permissão primeiro. Isso é necessário para o modo programático (`-p`) pois não há sessão interativa para aprovar ações. Use `--allow-all` apenas com prompts que você mesmo escreveu e em diretórios que você confia. Nunca use com entradas não confiáveis ou em diretórios sensíveis.

</details>

---

## Slash Commands Essenciais

Estes comandos são ótimos para aprender inicialmente ao começar a usar o Copilot CLI:

| Comando | O que Faz | Quando Usar |
|---------|-----------|-------------|
| `/ask` | Fazer uma pergunta rápida sem afetar o histórico da conversa | Quando você quer uma resposta rápida sem desviar da tarefa atual |
| `/clear` | Limpar a conversa e começar do zero | Ao trocar de assunto |
| `/help` | Mostrar todos os comandos disponíveis | Quando você esquece um comando |
| `/model` | Mostrar ou trocar o modelo de IA | Quando você quer mudar o modelo de IA |
| `/plan` | Planejar seu trabalho antes de codificar | Para funcionalidades mais complexas |
| `/research` | Pesquisa profunda usando fontes do GitHub e da web | Quando você precisa investigar um assunto antes de codificar |
| `/exit` | Encerrar a sessão | Quando terminar |

> 💡 **`/ask` versus chat regular**: Normalmente cada mensagem que você envia se torna parte da conversa em andamento e afeta respostas futuras. `/ask` é um atalho "fora do registro" — perfeito para perguntas pontuais como `/ask What does YAML mean?` sem poluir o contexto da sua sessão.

> 💡 **Autocompletar com Tab**: Ao digitar um slash command, pressione **Tab** para autocompletar o nome do comando ou percorrer os subcomandos e argumentos disponíveis. Isso é especialmente útil quando você não lembra o nome exato de um comando.

É isso para começar! À medida que você se sentir confortável, pode explorar comandos adicionais.

> 📚 **Documentação oficial**: [Referência de comandos do CLI](https://docs.github.com/copilot/reference/cli-command-reference) para a lista completa de comandos e flags.

<details>
<summary>📚 <strong>Comandos Adicionais</strong> (clique para expandir)</summary>

> 💡 Os comandos essenciais acima cobrem muito do que você fará no uso diário. Esta referência está aqui para quando você estiver pronto para explorar mais.

### Ambiente do Agente

| Comando | O que Faz |
|---------|-----------|
| `/agent` | Navegar e selecionar entre os agentes disponíveis |
| `/env` | Mostrar detalhes do ambiente carregado — quais instruções, servidores MCP, skills, agentes e plugins estão ativos |
| `/init` | Inicializar instruções do Copilot para o seu repositório |
| `/mcp` | Gerenciar a configuração do servidor MCP |
| `/skills` | Gerenciar skills para capacidades aprimoradas |

> 💡 Agentes são abordados no [Capítulo 04](../04-agents-custom-instructions/README.md), skills no [Capítulo 05](../05-skills/README.md), e servidores MCP no [Capítulo 06](../06-mcp-servers/README.md).

### Modelos e Subagentes

| Comando | O que Faz |
|---------|-----------|
| `/delegate` | Delegar tarefa ao agente de nuvem do GitHub Copilot |
| `/fleet` | Dividir uma tarefa complexa em subtarefas paralelas para conclusão mais rápida |
| `/model` | Mostrar ou trocar o modelo de IA |
| `/tasks` | Ver subagentes em segundo plano e sessões de shell desanexadas |

### Código

| Comando | O que Faz |
|---------|-----------|
| `/diff` | Revisar as alterações feitas no diretório atual |
| `/pr` | Operar em pull requests para a branch atual |
| `/research` | Executar investigação de pesquisa profunda usando fontes do GitHub e da web |
| `/review` | Executar o agente de revisão de código para analisar alterações |
| `/terminal-setup` | Ativar suporte a entrada multilinha (shift+enter e ctrl+enter) |

### Permissões

| Comando | O que Faz |
|---------|-----------|
| `/add-dir <diretório>` | Adicionar um diretório à lista de permitidos |
| `/allow-all [on\|off\|show]` | Auto-aprovar todos os prompts de permissão; use `on` para ativar, `off` para desativar, `show` para verificar o status atual |
| `/yolo` | Atalho rápido para `/allow-all on` — auto-aprova todos os prompts de permissão. |
| `/cwd`, `/cd [diretório]` | Ver ou mudar o diretório de trabalho |
| `/list-dirs` | Mostrar todos os diretórios permitidos |

> ⚠️ **Use com cautela**: `/allow-all` e `/yolo` ignoram prompts de confirmação. Ótimo para projetos confiáveis, mas tenha cuidado com código não confiável.

### Sessão

| Comando | O que Faz |
|---------|-----------|
| `/clear` | Abandona a sessão atual (sem histórico salvo) e inicia uma nova conversa |
| `/compact` | Resumir a conversa para reduzir o uso de contexto |
| `/context` | Mostrar uso e visualização do token da janela de contexto |
| `/keep-alive` | Evitar que o sistema entre em suspensão enquanto o Copilot CLI está ativo — útil para tarefas longas em um laptop |
| `/new` | Encerra a sessão atual (salvando-a no histórico para busca/retomada) e inicia uma nova conversa. |
| `/resume` | Mudar para uma sessão diferente (opcionalmente especifique o ID ou nome da sessão) |
| `/rename` | Renomear a sessão atual (omita o nome para gerar um automaticamente) |
| `/rewind` | Abrir um seletor de linha do tempo para voltar a qualquer ponto anterior da conversa |
| `/usage` | Exibir métricas de uso e estatísticas da sessão |
| `/session` | Mostrar informações da sessão e resumo do espaço de trabalho; use `/session delete`, `/session delete <id>`, ou `/session delete-all` para remover sessões |
| `/share` | Exportar a sessão como um arquivo markdown, GitHub gist ou arquivo HTML independente |

### Exibição

| Comando | O que Faz |
|---------|-----------|
| `/statusline` (ou `/footer`) | Personalizar quais itens aparecem na barra de status na parte inferior da sessão (diretório, branch, esforço, janela de contexto, cota) |
| `/theme` | Ver ou definir o tema do terminal |

### Ajuda e Feedback

| Comando | O que Faz |
|---------|-----------|
| `/changelog` | Exibir o changelog para versões do CLI |
| `/feedback` | Enviar feedback ao GitHub |
| `/help` | Mostrar todos os comandos disponíveis |

### Comandos de Shell Rápidos

Execute comandos de shell diretamente sem IA prefixando com `!`:

```bash
copilot

> !git status
# Executa git status diretamente, sem passar pela IA

> !python -m pytest tests/
# Executa pytest diretamente
```

### Trocando de Modelos

O Copilot CLI suporta múltiplos modelos de IA da OpenAI, Anthropic, Google e outros. Os modelos disponíveis para você dependem do seu nível de assinatura e região. Use `/model` para ver suas opções e alternar entre eles:

```bash
copilot
> /model

# Mostra os modelos disponíveis e permite que você escolha um. Selecione Sonnet 4.5.
```

> 💡 **Dica**: Alguns modelos custam mais "requisições premium" do que outros. Modelos marcados com **1x** (como Claude Sonnet 4.5) são um ótimo padrão. São capazes e eficientes. Modelos com multiplicadores maiores consomem sua cota de requisições premium mais rápido, então guarde-os para quando realmente precisar.

> 💡 **Não sabe qual modelo escolher?** Selecione **`Auto`** no seletor de modelos para deixar o Copilot escolher automaticamente o melhor modelo disponível para cada sessão. Este é um ótimo padrão se você está apenas começando e não quer pensar sobre a seleção de modelos.

</details>

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Hora de colocar em prática o que você aprendeu.

---

## ▶️ Experimente Você Mesmo

### Exploração Interativa

Inicie o Copilot e use prompts de acompanhamento para melhorar iterativamente o aplicativo de livros:

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Planejar uma Funcionalidade

Use `/plan` para ter o Copilot CLI mapeando uma implementação antes de escrever qualquer código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revise o plano
# Aprove ou modifique
# Veja a implementação passo a passo
```

### Automatizar com o Modo Programático

O flag `-p` permite que você execute o Copilot CLI diretamente do seu terminal sem entrar no modo interativo. Copie e cole o seguinte script no seu terminal (não dentro do Copilot) a partir da raiz do repositório para revisar todos os arquivos Python no aplicativo de livros.

```bash
# Revisar todos os arquivos Python no aplicativo de livros
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Revisar todos os arquivos Python no aplicativo de livros
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

Após concluir as demos, experimente estas variações:

1. **Desafio Interativo**: Inicie o `copilot` e explore o aplicativo de livros. Pergunte sobre `@samples/book-app-project/books.py` e solicite melhorias 3 vezes seguidas.

2. **Desafio do Modo Plan**: Execute `/plan Add rating and review features to the book app`. Leia o plano com atenção. Faz sentido?

3. **Desafio Programático**: Execute `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. Funcionou na primeira tentativa?

---

## 💡 Dica: Controle Sua Sessão CLI pela Web ou Celular

O GitHub Copilot CLI suporta **sessões remotas**, permitindo que você monitore e interaja com uma sessão do CLI em execução por meio de um navegador web (no desktop ou celular) ou pelo aplicativo GitHub Mobile, sem estar fisicamente no seu terminal.

Inicie uma sessão remota com o flag `--remote`:

```bash
copilot --remote
```

O Copilot CLI exibirá um link e fornecerá acesso a um QR code. Abra o link no seu celular ou em uma aba do navegador desktop para acompanhar a sessão em tempo real, enviar prompts de acompanhamento, revisar planos e controlar o agente remotamente. As sessões são específicas do usuário, portanto você só pode acessar as suas próprias sessões do Copilot CLI.

Você também pode ativar o acesso remoto de dentro de uma sessão ativa a qualquer momento:

```
> /remote
```

Mais detalhes sobre sessões remotas podem ser encontrados na [documentação do Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Atividade

### Desafio Principal: Melhorar os Utilitários do Aplicativo de Livros

Os exemplos práticos focaram em revisar e refatorar `book_app.py`. Agora pratique as mesmas habilidades em um arquivo diferente, `utils.py`:

1. Inicie uma sessão interativa: `copilot`
2. Peça ao Copilot CLI para resumir o arquivo: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. Peça para adicionar validação de entrada: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. Peça para melhorar o tratamento de erros: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. Peça uma docstring: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. Observe como o contexto se mantém entre os prompts. Cada melhoria se baseia na última
7. Saia com `/exit`

**Critérios de sucesso**: Você deve ter um `utils.py` melhorado com validação de entrada, tratamento de erros e uma docstring, tudo construído por meio de uma conversa com múltiplas trocas.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Prompts de exemplo para tentar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comuns:**
- Se o Copilot CLI fizer perguntas de esclarecimento, basta respondê-las naturalmente
- O contexto se mantém, então cada prompt se baseia no anterior
- Use `/clear` se quiser recomeçar

</details>

### Desafio Bônus: Compare os Modos

Os exemplos usaram `/plan` para uma funcionalidade de busca e `-p` para revisões em lote. Agora experimente os três modos em uma única tarefa nova: adicionar um método `list_by_year()` à classe `BookCollection`:

1. **Interativo**: `copilot` → peça para projetar e construir o método passo a passo
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexão**: Qual modo pareceu mais natural? Quando você usaria cada um?

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Digitar `exit` em vez de `/exit` | O Copilot CLI trata "exit" como um prompt, não como um comando | Slash commands sempre começam com `/` |
| Usar `-p` para conversas com múltiplas trocas | Cada chamada com `-p` é isolada sem memória de chamadas anteriores | Use o modo interativo (`copilot`) para conversas que se baseiam em contexto |
| Esquecer as aspas em prompts com `$` ou `!` | O shell interpreta caracteres especiais antes de o Copilot CLI os ver | Envolva os prompts em aspas: `copilot -p "What does $HOME mean?"` |
| Pressionar Esc uma vez para cancelar uma tarefa em execução | Um único Esc não cancela mais trabalhos em andamento (para prevenir acidentes) | Pressione **Esc duas vezes** para cancelar enquanto o Copilot CLI está processando |

### Solução de Problemas

**"Model not available"** - Sua assinatura pode não incluir todos os modelos. Use `/model` para ver o que está disponível.

**"Context too long"** - Sua conversa usou toda a janela de contexto. Use `/clear` para reiniciar ou inicie uma nova sessão.

**"Rate limit exceeded"** - Aguarde alguns minutos e tente novamente. Considere usar o modo programático para operações em lote com intervalos.

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **O modo Interativo** é para exploração e iteração - o contexto se mantém. É como ter uma conversa com alguém que se lembra do que você disse até aquele momento.
2. **O modo Plan** é normalmente para tarefas mais complexas. Revise antes da implementação.
3. **O modo Programático** é para automação. Sem necessidade de interação.
4. **Os comandos essenciais** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) cobrem a maior parte do uso diário.

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ➡️ O Que Vem a Seguir

Agora que você entende os três modos, vamos aprender a fornecer contexto ao Copilot CLI sobre o seu código.

No **[Capítulo 02: Contexto e Conversas](../02-context-conversations/README.md)**, você aprenderá:

- A sintaxe `@` para referenciar arquivos e diretórios
- Gerenciamento de sessões com `--resume` e `--continue`
- Como o gerenciamento de contexto torna o Copilot CLI verdadeiramente poderoso

---

**[← Voltar ao Início do Curso](../README.md)** | **[Continuar para o Capítulo 02 →](../02-context-conversations/README.md)**
