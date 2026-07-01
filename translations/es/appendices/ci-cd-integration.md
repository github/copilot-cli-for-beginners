<!--
---
id: CopilotCLI-Appendix-CI-CD-Integration
title: !translate CI/CD Integration
description: !translate Integrate GitHub Copilot CLI into GitHub Actions workflows for automated pull request reviews.
audience: Developers / Students / Terminal users
slug: ci-cd-integration
weight: 91
---
-->

# Integración CI/CD

> 📖 **Requisito previo**: Completa el [Capítulo 07: Uniéndolo todo](../07-putting-it-together/README.md) antes de leer este apéndice.
>
> ⚠️ **Este apéndice es para equipos con pipelines CI/CD existentes.** Si eres nuevo en GitHub Actions o en los conceptos de CI/CD, comienza con el enfoque más sencillo de hook de pre-commit en la sección [Automatización de revisión de código](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) del Capítulo 07.

Este apéndice muestra cómo integrar GitHub Copilot CLI en tus pipelines de CI/CD para revisiones de código automatizadas en pull requests.

---

## Flujo de trabajo de GitHub Actions

Este flujo de trabajo revisa automáticamente los archivos modificados cuando se abre o actualiza un pull request:

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
          fetch-depth: 0  # Needed to compare with main branch

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get list of changed JS/TS files
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
            
            # Use --silent to suppress progress output
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // Only post if there's meaningful content
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

## Opciones de configuración

### Limitar el alcance de la revisión

Puedes centrar la revisión en tipos específicos de problemas:

```yaml
# Security-only review
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Performance-only review
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### Gestionar PRs grandes

Para PRs con muchos archivos, considera agruparlos o limitarlos:

```yaml
# Limit to first 10 files
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Or set a timeout per file
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### Configuración del equipo

Para revisiones consistentes en todo tu equipo, crea una configuración compartida:

```json
// .copilot/config.json (committed to repo)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## Alternativa: Bot de revisión de PR

Para flujos de revisión más sofisticados, considera usar el agente en la nube de GitHub Copilot:

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

## Buenas prácticas para la integración CI/CD

1. **Usa la bandera `--silent`** - Suprime la salida de progreso para logs más limpios
2. **Establece tiempos de espera** - Evita que revisiones bloqueadas interrumpan tu pipeline
3. **Filtra tipos de archivos** - Revisa solo los archivos relevantes (omite código generado y dependencias)
4. **Conciencia de límite de tasa** - Distribuye las revisiones para PRs grandes
5. **Falla de forma controlada** - No bloquees las fusiones por fallos en las revisiones; regístralos y continúa

---

## Solución de problemas

### "Autenticación fallida" en CI

Asegúrate de que tu flujo de trabajo tenga los permisos correctos:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### Revisiones que agotan el tiempo de espera

Aumenta el tiempo de espera o reduce el alcance:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### Límites de tokens en archivos grandes

Omite los archivos muy grandes:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← Volver al Capítulo 07](../07-putting-it-together/README.md)** | **[Volver a los apéndices](README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->