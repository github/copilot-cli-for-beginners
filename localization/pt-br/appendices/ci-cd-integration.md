# Integração CI/CD

> 📖 **Pré-requisito**: Complete o [Capítulo 07: Colocando Tudo Junto](../07-putting-it-together/README.md) antes de ler este apêndice.
>
> ⚠️ **Este apêndice é para equipes com pipelines CI/CD existentes.** Se você é novo em GitHub Actions ou conceitos de CI/CD, comece com a abordagem mais simples de hook de pré-commit na seção [Automação de Revisão de Código](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) do Capítulo 07.

Este apêndice mostra como integrar o GitHub Copilot CLI em seus pipelines CI/CD para revisão automatizada de código em pull requests.

---

## Fluxo de Trabalho do GitHub Actions

Este fluxo de trabalho revisa automaticamente os arquivos alterados quando um pull request é aberto ou atualizado:

```yaml
# .github/workflows/copilot-review.yml
name: Copilot Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Necessário para comparar com a branch main

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Obter lista de arquivos JS/TS alterados
          FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts|jsx|tsx)$' || true)
          
          if [ -z "$FILES" ]; then
            echo "No JavaScript/TypeScript files changed"
            exit 0
          fi
          
          echo "# Copilot Code Review" > review.md
          echo "" >> review.md
          
          for file in $FILES; do
            echo "Reviewing $file..."
            echo "## $file" >> review.md
            echo "" >> review.md
            
            # Usar --silent para suprimir saída de progresso
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // Só publicar se houver conteúdo significativo
            if (review.includes('CRITICAL') || review.includes('HIGH')) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: review
              });
            } else {
              console.log('No critical issues found, skipping comment');
            }
```

---

## Opções de Configuração

### Limitando o Escopo da Revisão

Você pode focar a revisão em tipos específicos de problemas:

```yaml
# Revisão apenas de segurança
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Revisão apenas de performance
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### Tratando PRs Grandes

Para PRs com muitos arquivos, considere agrupar ou limitar:

```yaml
# Limitar aos primeiros 10 arquivos
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Ou definir um timeout por arquivo
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### Configuração da Equipe

Para revisões consistentes em toda a equipe, crie uma configuração compartilhada:

```json
// .copilot/config.json (commitado no repositório)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## Alternativa: Bot de Revisão de PR

Para fluxos de trabalho de revisão mais sofisticados, considere usar o agente de nuvem do GitHub Copilot:

```yaml
# .github/workflows/copilot-agent-review.yml
name: Request Copilot Review

on:
  pull_request:
    types: [opened, ready_for_review]

jobs:
  request-review:
    runs-on: ubuntu-latest
    steps:
      - name: Request Copilot Review
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              reviewers: ['copilot[bot]']
            });
```

---

## Melhores Práticas para Integração CI/CD

1. **Use a flag `--silent`** - Suprime a saída de progresso para logs mais limpos
2. **Defina timeouts** - Evite que revisões travadas bloqueiem seu pipeline
3. **Filtre tipos de arquivo** - Revise apenas arquivos relevantes (ignore código gerado, dependências)
4. **Consciência sobre limites de taxa** - Espaçe as revisões para PRs grandes
5. **Falhe graciosamente** - Não bloqueie merges em falhas de revisão; registre e continue

---

## Solução de Problemas

### "Authentication failed" no CI

Certifique-se de que seu fluxo de trabalho tem as permissões corretas:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### Revisões com timeout

Aumente o timeout ou reduza o escopo:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### Limites de token em arquivos grandes

Ignore arquivos muito grandes:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← Voltar ao Capítulo 07](../07-putting-it-together/README.md)** | **[Retornar aos Apêndices](README.md)**
