![Capítulo 07: Colocando Tudo Junto](../../../07-putting-it-together/images/chapter-header.png)

> **Tudo que você aprendeu se combina aqui. Vá de uma ideia a um PR mesclado em uma única sessão.**

Neste capítulo, você reunirá tudo que aprendeu em fluxos de trabalho completos. Você construirá funcionalidades usando colaboração entre múltiplos agentes, configurará hooks de pré-commit que detectam problemas de segurança antes de serem commitados, integrará o Copilot em pipelines CI/CD e irá de uma ideia de funcionalidade a um PR mesclado em uma única sessão de terminal. É aqui que o GitHub Copilot CLI se torna um verdadeiro multiplicador de força.

> 💡 **Nota**: Este capítulo mostra como combinar tudo que você aprendeu. **Você não precisa de agentes, skills ou MCP para ser produtivo (embora eles possam ser muito úteis).** O fluxo de trabalho principal — descrever, planejar, implementar, testar, revisar, publicar — funciona apenas com os recursos integrados dos Capítulos 00-03.

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Combinar agentes, skills e MCP (Model Context Protocol) em fluxos de trabalho unificados
- Construir funcionalidades completas usando abordagens com múltiplas ferramentas
- Configurar automação básica com hooks
- Aplicar melhores práticas para desenvolvimento profissional

> ⏱️ **Tempo estimado**: ~75 minutos (15 min de leitura + 60 min de prática)

---

## 🧩 Analogia com o Mundo Real: A Orquestra

<img src="../../../07-putting-it-together/images/orchestra-analogy.png" alt="Analogia da Orquestra - Fluxo de Trabalho Unificado" width="800"/>

Uma orquestra sinfônica tem muitas seções:
- **Cordas** fornecem a base (como seus fluxos de trabalho principais)
- **Metais** adicionam potência (como agentes com expertise especializada)
- **Madeiras** adicionam cor (como skills que ampliam capacidades)
- **Percussão** mantém o ritmo (como MCP conectando a sistemas externos)

Individualmente, cada seção soa limitada. Juntas, bem regidas, criam algo magnífico.

**É isso que este capítulo ensina!**<br>
*Como um regente com uma orquestra, você orquestra agentes, skills e MCP em fluxos de trabalho unificados*

Vamos começar percorrendo um cenário que modifica código, gera testes, revisa e cria um PR - tudo em uma sessão.

---

## De Ideia a PR Mesclado em Uma Sessão

Em vez de alternar entre seu editor, terminal, executor de testes e interface do GitHub perdendo contexto a cada vez, você pode combinar todas as suas ferramentas em uma única sessão de terminal. Vamos detalhar esse padrão na seção [Padrão de Integração](#the-integration-pattern-for-power-users) abaixo.

```bash
# Iniciar o Copilot no modo interativo
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# O Copilot cria um plano de alto nível...

# MUDAR PARA O AGENTE PYTHON-REVIEWER
> /agent
# Selecione "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# O agente python-reviewer produz:
# - Assinatura do método e tipo de retorno
# - Implementação de filtro usando compreensão de lista
# - Tratamento de casos extremos para coleções vazias

# MUDAR PARA O AGENTE PYTEST-HELPER
> /agent
# Selecione "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# O agente pytest-helper produz:
# - Casos de teste para coleções vazias
# - Casos de teste com livros misturados lidos/não lidos
# - Casos de teste com todos os livros lidos

# IMPLEMENTAR
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TESTAR
> Generate comprehensive tests for the new feature

# Múltiplos testes são gerados similares ao seguinte:
# - Caminho feliz (3 testes) — filtra corretamente, exclui lidos, inclui não lidos
# - Casos extremos (4 testes) — coleção vazia, todos lidos, nenhum lido, livro único
# - Parametrizado (5 casos) — variando proporções lidos/não lidos via @pytest.mark.parametrize
# - Integração (4 testes) — interação com mark_as_read, remove_book, add_book e integridade de dados

# Revisar as alterações
> /review

# Se a revisão passar, use /pr para operar no pull request da branch atual
> /pr [view|create|fix|auto]

# Ou pergunte naturalmente se quiser que o Copilot esboce pelo terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**Abordagem tradicional**: Alternando entre editor, terminal, executor de testes, documentação e interface do GitHub. Cada troca causa perda de contexto e atrito.

**O insight chave**: Você direcionou especialistas como um arquiteto. Eles cuidaram dos detalhes. Você cuidou da visão.

> 💡 **Indo além**: Para planos grandes com múltiplas etapas como este, tente `/fleet` para deixar o Copilot executar subtarefas independentes em paralelo. Veja a [documentação oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) para detalhes.

---

# Fluxos de Trabalho Adicionais

<img src="../../../07-putting-it-together/images/combined-workflows.png" alt="Pessoas montando um grande quebra-cabeça colorido com engrenagens, representando como agentes, skills e MCP se combinam em fluxos de trabalho unificados" width="800"/>

Para usuários avançados que completaram os Capítulos 04-06, esses fluxos de trabalho mostram como agentes, skills e MCP multiplicam sua eficácia.

## O Padrão de Integração

Aqui está o modelo mental para combinar tudo:

<img src="../../../07-putting-it-together/images/integration-pattern.png" alt="O Padrão de Integração - Um fluxo de trabalho de 4 fases: Reunir Contexto (MCP), Analisar e Planejar (Agentes), Executar (Skills + Manual), Concluir (MCP)" width="800"/>

---

## Fluxo de Trabalho 1: Investigação e Correção de Bug

Correção de bug do mundo real com integração completa de ferramentas:

```bash
copilot

# FASE 1: Entender o bug do GitHub (MCP fornece isso)
> Get the details of issue #1

# Descoberta: "find_by_author doesn't work with partial names"

# FASE 2: Pesquisar melhores práticas (pesquisa profunda com fontes web + GitHub)
> /research Best practices for Python case-insensitive string matching

# FASE 3: Encontrar o código relacionado
> @samples/book-app-project/books.py Show me the find_by_author method

# FASE 4: Obter análise especializada
> /agent
# Selecione "python-reviewer"

> Analyze this method for issues with partial name matching

# Agente identifica: Método usa igualdade exata em vez de correspondência de substring

# FASE 5: Corrigir com orientação do agente
> Implement the fix using lowercase comparison and 'in' operator

# FASE 6: Gerar testes
> /agent
# Selecione "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# FASE 7: Commit e PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Fluxo de Trabalho 2: Automação de Revisão de Código (Opcional)

> 💡 **Esta seção é opcional.** Hooks de pré-commit são úteis para equipes, mas não são necessários para ser produtivo. Pule isto se você está apenas começando.
>
> ⚠️ **Nota sobre performance**: Este hook chama `copilot -p` para cada arquivo staged, o que leva vários segundos por arquivo. Para commits grandes, considere limitar a arquivos críticos ou executar revisões manualmente com `/review` em vez disso.

Um **hook do git** é um script que o Git executa automaticamente em certos pontos, por exemplo, logo antes de um commit. Você pode usar isso para executar verificações automáticas no seu código. Veja como configurar uma revisão automática do Copilot nos seus commits:

```bash
# Criar um hook de pré-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Obter arquivos staged (apenas arquivos Python)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Usar timeout para evitar travamento (60 segundos por arquivo)
    # --allow-all aprova automaticamente leituras/escritas de arquivos para que o hook possa executar sem supervisão.
    # Use apenas em scripts automatizados. Em sessões interativas, deixe o Copilot pedir permissão.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Verificar se ocorreu timeout
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **Usuários macOS**: O comando `timeout` não está incluído por padrão no macOS. Instale-o com `brew install coreutils` ou substitua `timeout 60` por uma invocação simples sem guarda de timeout.

> 📚 **Documentação oficial**: [Usar hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) e [Referência de configuração de hooks](https://docs.github.com/copilot/reference/hooks-configuration) para a API completa de hooks.
>
> 💡 **Alternativa integrada**: O Copilot CLI também tem um sistema de hooks integrado (`copilot hooks`) que pode ser executado automaticamente em eventos como pré-commit. O hook manual do git acima oferece controle total, enquanto o sistema integrado é mais simples de configurar. Veja a documentação acima para decidir qual abordagem se encaixa no seu fluxo de trabalho.

Agora todo commit recebe uma revisão rápida de segurança:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Saída:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## Fluxo de Trabalho 3: Integração a uma Nova Base de Código

Ao ingressar em um novo projeto, combine contexto, agentes e MCP para se adaptar rapidamente:

```bash
# Iniciar o Copilot no modo interativo
copilot

# FASE 1: Obter a visão geral com contexto
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# FASE 2: Entender um fluxo específico
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# FASE 3: Obter análise especializada com um agente
> /agent
# Selecione "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# FASE 4: Encontrar algo para trabalhar (MCP fornece acesso ao GitHub)
> List open issues labeled "good first issue"

# FASE 5: Começar a contribuir
> Pick the simplest open issue and outline a plan to fix it
```

Este fluxo de trabalho combina contexto `@`, agentes e MCP em uma única sessão de integração — exatamente o padrão de integração do início deste capítulo.

---

# Melhores Práticas e Automação

Padrões e hábitos que tornam seus fluxos de trabalho mais eficazes.

---

## Melhores Práticas

### 1. Comece com Contexto Antes da Análise

Sempre reúna contexto antes de pedir análise:

```bash
# Bom
> Get the details of issue #42
> /agent
# Selecione python-reviewer
> Analyze this issue

# Menos eficaz
> /agent
# Selecione python-reviewer
> Fix login bug
# O agente não tem o contexto do issue
```

### 2. Conheça a Diferença: Agentes, Skills e Instruções Personalizadas

Cada ferramenta tem seu ponto forte:

```bash
# Agentes: Personas especializadas que você ativa explicitamente
> /agent
# Selecione python-reviewer
> Review this authentication code for security issues

# Skills: Capacidades modulares que se ativam automaticamente quando seu prompt
# corresponde à descrição da skill (você deve criá-las primeiro — veja o Cap. 05)
> Generate comprehensive tests for this code
# Se você tiver uma skill de teste configurada, ela se ativa automaticamente

# Instruções personalizadas (.github/copilot-instructions.md): Sempre ativas
# orientação que se aplica a cada sessão sem alternância ou acionamento
```

> 💡 **Ponto-chave**: Agentes e skills podem tanto analisar QUANTO gerar código. A diferença real é **como eles se ativam** — agentes são explícitos (`/agent`), skills são automáticas (correspondência por prompt), e instruções personalizadas estão sempre ativas.

### 3. Mantenha as Sessões Focadas

Use `/rename` para rotular sua sessão (facilita encontrar no histórico) e `/exit` para encerrá-la adequadamente:

```bash
# Bom: Uma funcionalidade por sessão
> /rename list-unread-feature
# Trabalhar em listar não lidos
> /exit

copilot
> /rename export-csv-feature
# Trabalhar na exportação CSV
> /exit

# Menos eficaz: Tudo em uma sessão longa
```

### 4. Tornar os Fluxos de Trabalho Reutilizáveis com o Copilot

Em vez de apenas documentar fluxos de trabalho em uma wiki, codifique-os diretamente no repositório onde o Copilot pode usá-los:

- **Instruções personalizadas** (`.github/copilot-instructions.md`): Orientação sempre ativa para padrões de codificação, regras de arquitetura e etapas de build/test/deploy. Cada sessão as segue automaticamente.
- **Arquivos de prompt** (`.github/prompts/`): Prompts reutilizáveis e parametrizados que sua equipe pode compartilhar — como templates para revisões de código, geração de componentes ou descrições de PR.
- **Agentes personalizados** (`.github/agents/`): Codifique personas especializadas (ex.: um revisor de segurança ou um escritor de documentação) que qualquer pessoa da equipe pode ativar com `/agent`.
- **Skills personalizadas** (`.github/skills/`): Empacote instruções de fluxo de trabalho passo a passo que se ativam automaticamente quando relevante.

> 💡 **A recompensa**: Novos membros da equipe obtêm seus fluxos de trabalho de graça — eles estão integrados ao repositório, não trancados na cabeça de alguém.

---

## Bônus: Padrões de Produção

Esses padrões são opcionais, mas valiosos para ambientes profissionais.

### Gerador de Descrição de PR

```bash
# Gerar descrições abrangentes de PR
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### Integração CI/CD

Para equipes com pipelines CI/CD existentes, você pode automatizar revisões do Copilot em cada pull request usando GitHub Actions. Isso inclui postar comentários de revisão automaticamente e filtrar por problemas críticos.

> 📖 **Saiba mais**: Veja [Integração CI/CD](../appendices/ci-cd-integration.md) para fluxos de trabalho completos do GitHub Actions, opções de configuração e dicas de solução de problemas.

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Coloque o fluxo de trabalho completo em prática.

---

## ▶️ Experimente Você Mesmo

Após completar as demos, tente estas variações:

1. **Desafio de Ponta a Ponta**: Escolha uma pequena funcionalidade (ex.: "listar livros não lidos" ou "exportar para CSV"). Use o fluxo de trabalho completo:
   - Planejar com `/plan`
   - Projetar com agentes (python-reviewer, pytest-helper)
   - Implementar
   - Gerar testes
   - Criar PR

2. **Desafio de Automação**: Configure o hook de pré-commit do fluxo de trabalho de Automação de Revisão de Código. Faça um commit com uma vulnerabilidade intencional de caminho de arquivo. Ele é bloqueado?

3. **Seu Fluxo de Trabalho de Produção**: Projete seu próprio fluxo de trabalho para uma tarefa comum que você faz. Escreva como um checklist. Que partes poderiam ser automatizadas com skills, agentes ou hooks?

**Autoavaliação**: Você completou o curso quando consegue explicar a um colega como agentes, skills e MCP funcionam juntos - e quando usar cada um.

---

## 📝 Atividade

### Desafio Principal: Funcionalidade de Ponta a Ponta

Os exemplos práticos percorreram a construção de uma funcionalidade "listar livros não lidos". Agora pratique o fluxo de trabalho completo em uma funcionalidade diferente: **pesquisar livros por faixa de ano**:

1. Inicie o Copilot e reúna contexto: `@samples/book-app-project/books.py`
2. Planeje com `/plan Add a "search by year" command that lets users find books published between two years`
3. Implemente um método `find_by_year_range(start_year, end_year)` em `BookCollection`
4. Adicione uma função `handle_search_year()` em `book_app.py` que solicita ao usuário os anos inicial e final
5. Gere testes: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Revise com `/review`
7. Atualize o README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Gere uma mensagem de commit

Documente seu fluxo de trabalho conforme avança.

**Critérios de sucesso**: Você completou a funcionalidade de ideia a commit usando o Copilot CLI, incluindo planejamento, implementação, testes, documentação e revisão.

> 💡 **Bônus**: Se você tem agentes configurados do Capítulo 04, tente criar e usar agentes personalizados. Por exemplo, um agente error-handler para revisão de implementação e um agente doc-writer para a atualização do README.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Siga o padrão do exemplo ["De Ideia a PR Mesclado"](#idea-to-merged-pr-in-one-session)** no início deste capítulo. Os passos principais são:

1. Reunir contexto com `@samples/book-app-project/books.py`
2. Planejar com `/plan Add a "search by year" command`
3. Implementar o método e o manipulador de comando
4. Gerar testes com casos extremos (entrada inválida, resultados vazios, faixa invertida)
5. Revisar com `/review`
6. Atualizar README com `@samples/book-app-project/README.md`
7. Gerar mensagem de commit com `-p`

**Casos extremos para pensar:**
- E se o usuário inserir "2000" e "1990" (faixa invertida)?
- E se nenhum livro corresponder à faixa?
- E se o usuário inserir entrada não numérica?

**O importante é praticar o fluxo de trabalho completo** de ideia → contexto → plano → implementar → testar → documentar → commit.

</details>

---

<details>
<summary>🔧 <strong>Erros Comuns</strong> (clique para expandir)</summary>

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Pular direto para a implementação | Perder problemas de design que são custosos para corrigir depois | Use `/plan` primeiro para pensar sobre a abordagem |
| Usar uma ferramenta quando múltiplas ajudariam | Resultados mais lentos e menos completos | Combine: Agente para análise → Skill para execução → MCP para integração |
| Não revisar antes de commitar | Problemas de segurança ou bugs passam despercebidos | Sempre execute `/review` ou use um [hook de pré-commit](#workflow-2-code-review-automation-optional) |
| Esquecer de compartilhar fluxos de trabalho com a equipe | Cada pessoa reinventa a roda | Documente padrões em agentes, skills e instruções compartilhadas |

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **Integração > Isolamento**: Combine ferramentas para máximo impacto
2. **Contexto primeiro**: Sempre reúna o contexto necessário antes da análise
3. **Agentes analisam, Skills executam**: Use a ferramenta certa para o trabalho
4. **Automatize a repetição**: Hooks e scripts multiplicam sua eficácia
5. **Documente fluxos de trabalho**: Padrões compartilháveis beneficiam toda a equipe

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## 🎓 Curso Concluído!

Parabéns! Você aprendeu:

| Capítulo | O que Você Aprendeu |
|----------|---------------------|
| 00 | Instalação do Copilot CLI e Início Rápido |
| 01 | Três modos de interação |
| 02 | Gerenciamento de contexto com sintaxe @ |
| 03 | Fluxos de trabalho de desenvolvimento |
| 04 | Agentes especializados |
| 05 | Skills extensíveis |
| 06 | Conexões externas com MCP |
| 07 | Fluxos de trabalho de produção unificados |

Você agora está equipado para usar o GitHub Copilot CLI como um verdadeiro multiplicador de força no seu fluxo de trabalho de desenvolvimento.

## ➡️ O Que Vem a Seguir

Seu aprendizado não para aqui:

1. **Pratique diariamente**: Use o Copilot CLI para trabalho real
2. **Construa ferramentas personalizadas**: Crie agentes e skills para suas necessidades específicas
3. **Compartilhe conhecimento**: Ajude sua equipe a adotar esses fluxos de trabalho
4. **Mantenha-se atualizado**: Acompanhe as atualizações do GitHub Copilot para novos recursos

### Recursos

- [Documentação do GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Registro de Servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Skills da Comunidade](https://github.com/topics/copilot-skill)

---

**Ótimo trabalho! Agora vá construir algo incrível.**

**[← Voltar ao Capítulo 06](../06-mcp-servers/README.md)** | **[Retornar ao Início do Curso →](../README.md)**
