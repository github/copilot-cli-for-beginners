# Recursos Adicionais de Contexto

> 📖 **Pré-requisito**: Complete o [Capítulo 02: Contexto e Conversas](../02-context-conversations/README.md) antes de ler este apêndice.

Este apêndice cobre dois recursos adicionais de contexto: trabalho com imagens e gerenciamento de permissões em múltiplos diretórios.

---

## Trabalhando com Imagens

Você pode incluir imagens nas suas conversas usando a sintaxe `@`. O Copilot pode analisar capturas de tela, mockups, diagramas e outros conteúdos visuais.

### Referência Básica de Imagem

```bash
copilot

> @screenshot.png What's happening in this UI?

# O Copilot analisa a imagem e responde

> @mockup.png @current-design.png Compare these two designs

# Você também pode arrastar e soltar imagens ou colar da área de transferência
```

### Formatos de Imagem Suportados

| Formato | Melhor Para |
|---------|------------|
| PNG | Capturas de tela, mockups de UI, diagramas |
| JPG/JPEG | Fotos, imagens complexas |
| GIF | Diagramas simples (apenas primeiro quadro) |
| WebP | Capturas de tela web |

### Casos de Uso Práticos de Imagem

**1. Depuração de UI**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. Implementação de Design**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. Análise de Erros**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. Revisão de Arquitetura**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. Comparação Antes/Depois**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### Combinando Imagens com Código

As imagens se tornam ainda mais poderosas quando combinadas com contexto de código:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### Dicas para Imagens

- **Recorte capturas de tela** para mostrar apenas as partes relevantes (economiza tokens de contexto)
- **Use alto contraste** para elementos de UI que você deseja analisar
- **Anote se necessário** - circule ou destaque áreas problemáticas antes de fazer upload
- **Uma imagem por conceito** - múltiplas imagens funcionam, mas seja focado

---

## Padrões de Permissão

Por padrão, o Copilot pode acessar arquivos no seu diretório atual. Para arquivos em outros locais, você precisa conceder acesso.

### Adicionar Diretórios

```bash
# Adicionar um diretório à lista permitida
copilot --add-dir /path/to/other/project

# Adicionar múltiplos diretórios
copilot --add-dir ~/workspace --add-dir /tmp
```

### Permitir Todos os Caminhos

```bash
# Desabilitar restrições de caminho completamente (use com cautela)
copilot --allow-all-paths
```

### Dentro de uma Sessão

```bash
copilot

> /add-dir /path/to/other/project
# Agora você pode referenciar arquivos desse diretório

> /list-dirs
# Ver todos os diretórios permitidos

> /yolo
# Alias rápido para /allow-all ativado — aprova automaticamente todos os prompts de permissão
```

### Para Automação

```bash
# Permitir todas as permissões para scripts não interativos
copilot -p "Review @src/" --allow-all

# Ou use o alias memorável
copilot -p "Review @src/" --yolo
```

### Quando Você Precisa de Acesso a Múltiplos Diretórios

Cenários comuns onde você precisará dessas permissões:

1. **Trabalho em monorepo** - Comparar código entre pacotes
2. **Refatoração entre projetos** - Atualizar bibliotecas compartilhadas
3. **Projetos de documentação** - Referenciar múltiplas bases de código
4. **Trabalho de migração** - Comparar implementações antigas e novas

---

**[← Voltar ao Capítulo 02](../02-context-conversations/README.md)** | **[Retornar aos Apêndices](README.md)**
