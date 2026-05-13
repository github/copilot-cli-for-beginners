![Capítulo 05: Sistema de Skills](../../../05-skills/images/chapter-header.png)

> **E se o Copilot pudesse aplicar automaticamente as melhores práticas da sua equipe sem que você precise explicá-las toda vez?**

Neste capítulo, você aprenderá sobre Skills de Agente: pastas de instruções que o Copilot carrega automaticamente quando relevantes para a sua tarefa. Enquanto os agentes mudam *como* o Copilot pensa, as skills ensinam ao Copilot *formas específicas de concluir tarefas*. Você criará uma skill de auditoria de segurança que o Copilot aplica sempre que você perguntar sobre segurança, construirá critérios de revisão padrão da equipe que garantem qualidade de código consistente e aprenderá como as skills funcionam no Copilot CLI, VS Code e no agente de nuvem do GitHub Copilot.


## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você será capaz de:

- Entender como as Skills de Agente funcionam e quando usá-las
- Criar skills personalizadas com arquivos SKILL.md
- Usar skills da comunidade de repositórios compartilhados
- Saber quando usar skills vs agentes vs MCP

> ⏱️ **Tempo estimado**: ~55 minutos (20 min de leitura + 35 min de prática)

---

## 🧩 Analogia com o Mundo Real: Ferramentas Elétricas

Uma furadeira de uso geral é útil, mas os acessórios especializados a tornam poderosa.
<img src="../../../05-skills/images/power-tools-analogy.png" alt="Ferramentas Elétricas - Skills Ampliam as Capacidades do Copilot" width="800"/>


As skills funcionam da mesma forma. Assim como você troca brocas para diferentes trabalhos, você pode adicionar skills ao Copilot para diferentes tarefas:

| Acessório de Skill | Finalidade |
|------------|---------|
| `commit` | Gerar mensagens de commit consistentes |
| `security-audit` | Verificar vulnerabilidades OWASP |
| `generate-tests` | Criar testes pytest abrangentes |
| `code-checklist` | Aplicar padrões de qualidade de código da equipe |



*Skills são acessórios especializados que ampliam o que o Copilot pode fazer*

---

# Como as Skills Funcionam

<img src="../../../05-skills/images/how-skills-work.png" alt="Ícones de skill estilo RPG brilhantes conectados por trilhas de luz em um fundo estrelado representando skills do Copilot" width="800"/>

Aprenda o que são skills, por que são importantes e como diferem de agentes e MCP.

---

## *Novo em Skills?* Comece Aqui!

1. **Veja quais skills já estão disponíveis:**
   ```bash
   copilot
   > /skills list
   ```
   Isso mostra todas as skills que o Copilot consegue encontrar, incluindo quaisquer **skills integradas** que vêm com o próprio CLI, além de skills das suas pastas do projeto e pessoais.

   > 💡 **Skills integradas**: O Copilot CLI vem com skills pré-instaladas. Por exemplo, a skill `customizing-copilot-cloud-agents-environment` fornece um guia para personalizar o ambiente do agente de nuvem do Copilot. Você não precisa criar ou instalar nada para usá-las. Execute `/skills list` para ver o que está disponível.

2. **Veja um arquivo de skill real:** Confira nosso [SKILL.md do code-checklist](../../../.github/skills/code-checklist/SKILL.md) fornecido para ver o padrão. É apenas frontmatter YAML mais instruções em markdown.

3. **Entenda o conceito central:** Skills são instruções específicas de tarefa que o Copilot carrega *automaticamente* quando o seu prompt corresponde à descrição da skill. Você não precisa ativá-las, basta perguntar naturalmente.


## Entendendo as Skills

Skills de Agente são pastas contendo instruções, scripts e recursos que o Copilot **carrega automaticamente quando relevante** para a sua tarefa. O Copilot lê o seu prompt, verifica se alguma skill corresponde e aplica as instruções relevantes automaticamente.

```bash
copilot

> Check books.py against our quality checklist
# O Copilot detecta que isso corresponde à sua skill "code-checklist"
# e aplica automaticamente o checklist de qualidade Python

> Generate tests for the BookCollection class
# O Copilot carrega a sua skill "pytest-gen"
# e aplica a estrutura de teste preferida

> What are the code quality issues in this file?
# O Copilot carrega a sua skill "code-checklist"
# e verifica de acordo com os padrões da sua equipe
```

> 💡 **Insight Chave**: As skills são **acionadas automaticamente** com base no seu prompt correspondendo à descrição da skill. Basta perguntar naturalmente e o Copilot aplica as skills relevantes nos bastidores. Você também pode invocar skills diretamente, o que você aprenderá a seguir.

> 🧰 **Templates prontos para usar**: Confira a pasta [.github/skills](../../../.github/skills/) para skills simples de copiar e colar que você pode experimentar.

### Invocação Direta por Slash Command

Embora o acionamento automático seja a forma principal como as skills funcionam, você também pode **invocar skills diretamente** usando o nome delas como um slash command:

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

Isso lhe dá controle explícito quando você quer garantir que uma skill específica seja usada.

#### Combinando Múltiplas Skills em Uma Mensagem

Você pode invocar **mais de uma skill em uma única mensagem**, e o slash command da skill pode aparecer em qualquer lugar no seu prompt — não apenas no início. Isso é útil quando você quer dois tipos diferentes de verificação em uma única vez:

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

O Copilot aplicará cada skill nomeada na mesma resposta, poupando você de enviar múltiplas mensagens separadas.

> 💡 **Dica**: Coloque os slash commands de skill onde eles se encaixarem mais naturalmente na sua frase. Você pode colocá-los no início, meio ou fim da sua mensagem.

> 📝 **Invocação de Skills vs Agentes**: Não confunda a invocação de skill com a invocação de agente:
> - **Skills**: `/nome-da-skill <prompt>`, ex.: `/code-checklist Check this file`
> - **Agentes**: `/agent` (selecionar da lista) ou `copilot --agent <nome>` (linha de comando)
>
> Se você tiver uma skill e um agente com o mesmo nome (ex.: "code-reviewer"), digitar `/code-reviewer` invoca a **skill**, não o agente.

### Como Sei que uma Skill Foi Usada?

Você pode perguntar diretamente ao Copilot:

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills vs Agentes vs MCP

Skills são apenas uma peça do modelo de extensibilidade do GitHub Copilot. Veja como elas se comparam a agentes e servidores MCP.

> *Não se preocupe com MCP ainda. Vamos abordá-lo no [Capítulo 06](../06-mcp-servers/README.md). Está incluído aqui para que você possa ver como as skills se encaixam na visão geral.*

<img src="../../../05-skills/images/skills-agents-mcp-comparison.png" alt="Diagrama de comparação mostrando as diferenças entre Agentes, Skills e Servidores MCP e como eles se combinam no seu fluxo de trabalho" width="800"/>

| Recurso | O que Faz | Quando Usar |
|---------|-----------|-------------|
| **Agentes** | Muda como a IA pensa | Precisa de expertise especializada em muitas tarefas |
| **Skills** | Fornece instruções específicas de tarefa | Tarefas específicas e repetíveis com etapas detalhadas |
| **MCP** | Conecta serviços externos | Precisa de dados ao vivo de APIs |

Use agentes para expertise ampla, skills para instruções específicas de tarefa e MCP para dados externos. Um agente pode usar uma ou mais skills durante uma conversa. Por exemplo, quando você pede a um agente para verificar o seu código, ele pode aplicar tanto uma skill `security-audit` quanto uma skill `code-checklist` automaticamente.

> 📚 **Saiba Mais**: Veja a documentação oficial [Sobre Skills de Agente](https://docs.github.com/copilot/concepts/agents/about-agent-skills) para a referência completa sobre formatos de skill e melhores práticas.

---

## De Prompts Manuais a Expertise Automática

Antes de mergulhar em como criar skills, vamos ver *por que* vale a pena aprendê-las. Uma vez que você veja os ganhos de consistência, o "como" fará mais sentido.

### Antes das Skills: Revisões Inconsistentes

Em cada revisão de código, você pode esquecer algo:

```bash
copilot

> Review this code for issues
# Revisão genérica - pode perder as preocupações específicas da sua equipe
```

Ou você escreve um prompt longo toda vez:

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

Tempo: **30+ segundos** para digitar. Consistência: **varia com a memória**.

### Depois das Skills: Melhores Práticas Automáticas

Com uma skill `code-checklist` instalada, basta perguntar naturalmente:

```bash
copilot

> Check the book collection code for quality issues
```

**O que acontece nos bastidores**:
1. O Copilot vê "qualidade de código" e "problemas" no seu prompt
2. Verifica as descrições das skills, encontra que a sua skill `code-checklist` corresponde
3. Carrega automaticamente o checklist de qualidade da sua equipe
4. Aplica todas as verificações sem você listá-las

<img src="../../../05-skills/images/skill-auto-discovery-flow.png" alt="Como as Skills São Acionadas Automaticamente - Fluxo de 4 etapas mostrando como o Copilot corresponde automaticamente o seu prompt à skill certa" width="800"/>

*Basta perguntar naturalmente. O Copilot corresponde o seu prompt à skill certa e a aplica automaticamente.*

**Saída**:
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**A diferença**: Os padrões da sua equipe são aplicados automaticamente, toda vez, sem precisar digitá-los.

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo de Acionamento de Skill](../../../05-skills/images/skill-trigger-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

## Consistência em Escala: Skill de Revisão de PR da Equipe

Imagine que a sua equipe tem um checklist de 10 pontos para PRs. Sem uma skill, cada desenvolvedor deve lembrar todos os 10 pontos, e alguém sempre esquece um deles. Com uma skill `pr-review`, toda a equipe recebe revisões consistentes:

```bash
copilot

> Can you review this PR?
```

O Copilot carrega automaticamente a skill `pr-review` da sua equipe e verifica todos os 10 pontos:

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**O poder**: Todo membro da equipe aplica os mesmos padrões automaticamente. Novos integrantes não precisam memorizar o checklist porque a skill cuida disso.

---

# Criando Skills Personalizadas

<img src="../../../05-skills/images/creating-managing-skills.png" alt="Mãos humanas e robóticas construindo uma parede de blocos LEGO brilhantes representando a criação e gerenciamento de skills" width="800"/>

Construa suas próprias skills a partir de arquivos SKILL.md.

---

## Locais das Skills

As skills são armazenadas em `.github/skills/` (específicas do projeto) ou `~/.copilot/skills/` (nível do usuário).

### Como o Copilot Encontra as Skills

O Copilot verifica automaticamente esses locais para encontrar skills:

| Local | Escopo |
|-------|--------|
| `.github/skills/` | Específico do projeto (compartilhado com a equipe via git) |
| `~/.copilot/skills/` | Específico do usuário (suas skills pessoais) |

### Estrutura da Skill

Cada skill fica em sua própria pasta com um arquivo `SKILL.md`. Você pode opcionalmente incluir scripts, exemplos ou outros recursos:

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Obrigatório: Definição e instruções da skill
    ├── examples/          # Opcional: Arquivos de exemplo que o Copilot pode referenciar
    │   └── sample.py
    └── scripts/           # Opcional: Scripts que a skill pode usar
        └── validate.sh
```

> 💡 **Dica**: O nome do diretório deve corresponder ao `name` no frontmatter do seu SKILL.md (letras minúsculas com hifens).

### Formato do SKILL.md

As skills usam um formato markdown simples com frontmatter YAML:

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**Propriedades YAML:**

| Propriedade | Obrigatório | Descrição |
|-------------|-------------|-----------|
| `name` | **Sim** | Identificador único (letras minúsculas, hifens no lugar de espaços) |
| `description` | **Sim** | O que a skill faz e quando o Copilot deve usá-la |
| `license` | Não | Licença que se aplica a esta skill |

> 📖 **Documentação oficial**: [Sobre Skills de Agente](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### Criando Sua Primeira Skill

Vamos construir uma skill de auditoria de segurança que verifica vulnerabilidades OWASP Top 10:

```bash
# Criar o diretório da skill
mkdir -p .github/skills/security-audit

# Criar o arquivo SKILL.md
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Testar a sua skill (skills carregam automaticamente com base no seu prompt)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# O Copilot detecta "vulnerabilidades de segurança" correspondendo à sua skill
# e aplica automaticamente o checklist OWASP
```

**Saída esperada** (seus resultados variarão):

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## Escrevendo Boas Descrições de Skill

O campo `description` no seu SKILL.md é crucial! É como o Copilot decide se vai carregar a sua skill:

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Dica**: Inclua palavras-chave que correspondam à forma como você faz perguntas naturalmente. Se você diz "revisão de segurança", inclua "revisão de segurança" na descrição.

### Combinando Skills com Agentes

Skills e agentes trabalham juntos. O agente fornece expertise, a skill fornece instruções específicas:

```bash
# Iniciar com um agente code-reviewer
copilot --agent code-reviewer

> Check the book app for quality issues
# a expertise do agente code-reviewer se combina
# com o checklist da sua skill code-checklist
```

---

# Gerenciando e Compartilhando Skills

Descubra skills instaladas, encontre skills da comunidade e compartilhe as suas.

<img src="../../../05-skills/images/managing-sharing-skills.png" alt="Gerenciando e Compartilhando Skills - mostrando o ciclo de descobrir, usar, criar e compartilhar skills do CLI" width="800" />

---

## Gerenciando Skills com o Comando `/skills`

Use o comando `/skills` para gerenciar as suas skills instaladas:

| Comando | O que Faz |
|---------|-----------|
| `/skills list` | Mostrar todas as skills instaladas |
| `/skills info <nome>` | Obter detalhes sobre uma skill específica |
| `/skills add <nome>` | Habilitar uma skill (de um repositório ou marketplace) |
| `/skills remove <nome>` | Desabilitar ou desinstalar uma skill |
| `/skills reload` | Recarregar skills após editar arquivos SKILL.md |

> 💡 **Lembre-se**: Você não precisa "ativar" skills para cada prompt. Uma vez instaladas, as skills são **acionadas automaticamente** quando o seu prompt corresponde à descrição delas. Esses comandos são para gerenciar quais skills estão disponíveis, não para usá-las.

### Exemplo: Ver Suas Skills

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>Veja em ação!</summary>

![Demo de Lista de Skills](../../../05-skills/images/list-skills-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

### Quando Usar `/skills reload`

Após criar ou editar o arquivo SKILL.md de uma skill, execute `/skills reload` para capturar as alterações sem reiniciar o Copilot:

```bash
# Edite o arquivo da sua skill
# Então no Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Bom saber**: As skills permanecem eficazes mesmo após usar `/compact` para resumir o histórico de conversas. Não é necessário recarregar após compactar.

---

## Encontrando e Usando Skills da Comunidade

### Usando Plugins para Instalar Skills

> 💡 **O que são plugins?** Plugins são pacotes instaláveis que podem agrupar skills, agentes e configurações de servidor MCP juntos. Pense neles como extensões de "loja de aplicativos" para o Copilot CLI.

O comando `/plugin` permite que você navegue e instale esses pacotes:

```bash
copilot

> /plugin list
# Mostra plugins instalados

> /plugin marketplace
# Navegar pelos plugins disponíveis

> /plugin install <nome-do-plugin>
# Instalar um plugin do marketplace
```

Para manter o catálogo de plugins local atualizado, atualize-o com:

```bash
copilot plugin marketplace update
```

Plugins podem agrupar múltiplas capacidades juntas. Um único plugin pode incluir skills relacionadas, agentes e configurações de servidor MCP que trabalham juntos.

### Repositórios de Skills da Comunidade

Skills pré-prontas também estão disponíveis em repositórios da comunidade:

- [**Awesome Copilot**](https://github.com/github/awesome-copilot) - Recursos oficiais do GitHub Copilot incluindo documentação e exemplos de skills

### Instalando uma Skill da Comunidade com o GitHub CLI

A forma mais fácil de instalar uma skill de um repositório GitHub é usar o comando `gh skill install` (requer [GitHub CLI v2.90.0+](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)):

```bash
# Navegar e selecionar interativamente uma skill do awesome-copilot
gh skill install github/awesome-copilot

# Ou instalar uma skill específica diretamente
gh skill install github/awesome-copilot code-checklist

# Instalar para uso pessoal em todos os projetos (escopo de usuário)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **Revise antes de instalar**: Sempre leia o `SKILL.md` de uma skill antes de instalá-la. As skills controlam o que o Copilot faz, e uma skill maliciosa poderia instruí-lo a executar comandos prejudiciais ou modificar código de formas inesperadas.

---

# Prática

<img src="../../../images/practice.png" alt="Mesa de trabalho aconchegante com monitor mostrando código, abajur, xícara de café e fones de ouvido prontos para a prática" width="800"/>

Aplique o que aprendeu construindo e testando suas próprias skills.

---

## ▶️ Experimente Você Mesmo

### Construir Mais Skills

Aqui estão duas skills mostrando padrões diferentes. Siga o mesmo fluxo de trabalho `mkdir` + `cat` de "Criando Sua Primeira Skill" acima ou copie e cole as skills no local adequado. Mais exemplos estão disponíveis em [.github/skills](../../../.github/skills).

### Skill de Geração de Testes pytest

Uma skill que garante estrutura pytest consistente em toda a sua base de código:

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### Skill de Revisão de PR da Equipe

Uma skill que aplica padrões consistentes de revisão de PR em toda a sua equipe:

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### Indo Além

1. **Desafio de Criação de Skill**: Crie uma skill `quick-review` que faz um checklist de 3 pontos:
   - Cláusulas bare except
   - Dicas de tipo ausentes
   - Nomes de variáveis pouco claros

   Teste perguntando: "Do a quick review of books.py"

2. **Comparação de Skills**: Cronômetro enquanto escreve um prompt detalhado de revisão de segurança manualmente. Depois apenas pergunte "Check for security issues in this file" e deixe a sua skill security-audit carregar automaticamente. Quanto tempo a skill economizou?

3. **Desafio de Skill da Equipe**: Pense no checklist de revisão de código da sua equipe. Você poderia codificá-lo como uma skill? Anote 3 coisas que a skill deve sempre verificar.

**Autoavaliação**: Você entende as skills quando consegue explicar por que o campo `description` é importante (é como o Copilot decide se deve carregar a sua skill).

---

## 📝 Atividade

### Desafio Principal: Construir uma Skill de Resumo de Livros

Os exemplos acima criaram skills `pytest-gen` e `pr-review`. Agora pratique criando um tipo completamente diferente de skill: uma para gerar saída formatada a partir de dados.

1. Liste suas skills atuais: Execute o Copilot e passe `/skills list`. Você também pode usar `ls .github/skills/` para ver as skills do projeto ou `ls ~/.copilot/skills/` para skills pessoais.
2. Crie uma skill `book-summary` em `.github/skills/book-summary/SKILL.md` que gera um resumo markdown formatado da coleção de livros
3. Sua skill deve ter:
   - Nome e descrição claros (a descrição é crucial para a correspondência!)
   - Regras de formatação específicas (ex.: tabela markdown com título, autor, ano, status de leitura)
   - Convenções de saída (ex.: use ✅/❌ para status de leitura, ordenar por ano)
4. Teste a skill: `@samples/book-app-project/data.json Summarize the books in this collection`
5. Verifique se a skill é acionada automaticamente verificando `/skills list`
6. Tente invocá-la diretamente com `/book-summary Summarize the books in this collection`

**Critérios de sucesso**: Você tem uma skill `book-summary` funcionando que o Copilot aplica automaticamente quando você pergunta sobre a coleção de livros.

<details>
<summary>💡 Dicas (clique para expandir)</summary>

**Template inicial**: Crie `.github/skills/book-summary/SKILL.md`:

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**Teste:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# A skill deve ser acionada automaticamente com base na correspondência da descrição
```

**Se não acionar:** Tente `/skills reload` e pergunte novamente.

</details>

### Desafio Bônus: Skill de Mensagem de Commit

1. Crie uma skill `commit-message` que gera mensagens de commit convencionais com um formato consistente
2. Teste fazendo stage de uma alteração e perguntando: "Generate a commit message for my staged changes"
3. Documente a sua skill e compartilhe-a no GitHub com o tópico `copilot-skill`

---

<details>
<summary>🔧 <strong>Erros Comuns e Solução de Problemas</strong> (clique para expandir)</summary>

### Erros Comuns

| Erro | O que Acontece | Solução |
|------|----------------|---------|
| Nomear o arquivo com algo diferente de `SKILL.md` | A skill não será reconhecida | O arquivo deve ser nomeado exatamente `SKILL.md` |
| Campo `description` vago | A skill nunca é carregada automaticamente | A descrição é o mecanismo PRINCIPAL de descoberta. Use palavras-chave específicas de gatilho |
| `name` ou `description` ausentes no frontmatter | A skill falha ao carregar | Adicione ambos os campos no frontmatter YAML |
| Local da pasta errado | Skill não encontrada | Use `.github/skills/nome-da-skill/` (projeto) ou `~/.copilot/skills/nome-da-skill/` (pessoal) |

### Solução de Problemas

**Skill não sendo usada** - Se o Copilot não está usando a sua skill quando esperado:

1. **Verifique a descrição**: Ela corresponde à forma como você está perguntando?
   ```markdown
   # Ruim: Muito vago
   description: Reviews code

   # Bom: Inclui palavras-chave de gatilho
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **Verifique o local do arquivo**:
   ```bash
   # Skills do projeto
   ls .github/skills/

   # Skills do usuário
   ls ~/.copilot/skills/
   ```

3. **Verifique o formato do SKILL.md**: O frontmatter é obrigatório:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**Skill não aparecendo** - Verifique a estrutura de pastas:
```
.github/skills/
└── my-skill/           # Nome da pasta
    └── SKILL.md        # Deve ser exatamente SKILL.md (sensível a maiúsculas)
```

Execute `/skills reload` após criar ou editar skills para garantir que as alterações sejam capturadas.

**Testando se uma skill carrega** - Pergunte diretamente ao Copilot:
```bash
> What skills do you have available for checking code quality?
# O Copilot descreverá as skills relevantes que encontrou
```

**Como sei que minha skill está realmente funcionando?**

1. **Verifique o formato de saída**: Se a sua skill especifica um formato de saída (como tags `[CRITICAL]`), procure por isso na resposta
2. **Pergunte diretamente**: Após obter uma resposta, pergunte "Did you use any skills for that?"
3. **Compare com/sem**: Tente o mesmo prompt com `--no-custom-instructions` para ver a diferença:
   ```bash
   # Com skills
   copilot --allow-all -p "Review @file.py for security issues"

   # Sem skills (comparação de referência)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **Verifique verificações específicas**: Se a sua skill inclui verificações específicas (como "funções com mais de 50 linhas"), veja se essas aparecem na saída

</details>

---

# Resumo

## 🔑 Principais Aprendizados

1. **Skills são automáticas**: O Copilot as carrega quando o seu prompt corresponde à descrição da skill
2. **Invocação direta**: Você também pode invocar skills diretamente com `/nome-da-skill` como um slash command
3. **Formato SKILL.md**: Frontmatter YAML (name, description, license opcional) mais instruções em markdown
4. **A localização importa**: `.github/skills/` para compartilhamento no projeto/equipe, `~/.copilot/skills/` para uso pessoal
5. **A descrição é fundamental**: Escreva descrições que correspondam à forma como você faz perguntas naturalmente

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

## ➡️ O Que Vem a Seguir

Skills ampliam o que o Copilot pode fazer com instruções carregadas automaticamente. Mas e quanto a se conectar a serviços externos? É aí que entra o MCP.

No [**Capítulo 06: Servidores MCP**](../06-mcp-servers/README.md), você aprenderá:

- O que é MCP (Model Context Protocol)
- Conectar ao GitHub, sistema de arquivos e serviços de documentação
- Configurar servidores MCP
- Fluxos de trabalho com múltiplos servidores

---

[**← Voltar ao Capítulo 04**](../04-agents-custom-instructions/README.md) | [**Continuar para o Capítulo 06 →**](../06-mcp-servers/README.md)
