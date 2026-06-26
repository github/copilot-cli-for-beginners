![GitHub Copilot CLI for Beginners](../../images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)&ensp;
[![Abrir projeto no GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Documentação oficial do Copilot CLI](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Entre na comunidade AI Foundry no Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [O que você vai aprender](#-o-que-você-vai-aprender) &ensp; ✅ [Pré-requisitos](#-pré-requisitos) &ensp; 🤖 [Família Copilot](#-entendendo-a-família-github-copilot) &ensp; 📚 [Estrutura do curso](#-estrutura-do-curso) &ensp; 📋 [Referência de comandos](#-referência-de-comandos-do-github-copilot-cli) &ensp; 🌐 [Seu idioma](#-use-seu-idioma-preferido)

# GitHub Copilot CLI para Iniciantes

> **✨ Aprenda a turbinar seu fluxo de trabalho de desenvolvimento com assistência de linha de comando movida por IA.**

O GitHub Copilot CLI traz a assistência de IA diretamente para o seu terminal. Em vez de alternar para um navegador ou editor de código, você pode fazer perguntas, gerar aplicações completas, revisar código, gerar testes e depurar problemas sem sair da linha de comando.

Pense nisso como ter um colega experiente disponível 24 horas por dia, 7 dias por semana, que pode ler o seu código, explicar padrões confusos e ajudar você a trabalhar mais rápido!

> 📘 **Prefere uma experiência web?** Você pode seguir este curso aqui mesmo no GitHub, ou visualizá-lo no [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) para uma experiência de navegação mais tradicional.

Este curso é indicado para:

- **Desenvolvedores de software** que querem usar IA a partir da linha de comando
- **Usuários de terminal** que preferem fluxos de trabalho orientados ao teclado em vez de integrações com IDEs
- **Equipes que desejam padronizar** práticas de revisão de código e desenvolvimento assistido por IA

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="../../images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - Encontre ou organize um evento" width="100%" />
  </picture>
</a>

## 🎯 O que você vai aprender

Este curso prático leva você do zero à produtividade com o GitHub Copilot CLI. Você trabalhará com um único aplicativo Python de coleção de livros ao longo de todos os capítulos, melhorando-o progressivamente com fluxos de trabalho assistidos por IA. Ao final, você usará IA com confiança para revisar código, gerar testes, depurar problemas e automatizar fluxos de trabalho — tudo pelo seu terminal.

**Nenhuma experiência com IA é necessária.** Se você sabe usar um terminal, você pode aprender isso.

**Ideal para:** Desenvolvedores, estudantes e qualquer pessoa com experiência em desenvolvimento de software.

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter:

- **Conta no GitHub**: [Crie uma gratuitamente](https://github.com/signup)<br>
- **Acesso ao GitHub Copilot**: [Plano gratuito](https://github.com/features/copilot/plans), [Assinatura mensal](https://github.com/features/copilot/plans) ou [Gratuito para estudantes/professores](https://education.github.com/pack)<br>
- **Noções básicas de terminal**: Familiaridade com `cd`, `ls` e execução de comandos

## 🤖 Entendendo a família GitHub Copilot

O GitHub Copilot evoluiu para uma família de ferramentas com IA. Veja onde cada uma delas opera:

| Produto | Onde é executado | Descrição |
|---------|-----------------|-----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>(este curso) | Seu terminal | Assistente de codificação com IA nativo do terminal |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code, Visual Studio, JetBrains, etc. | Modo agente, chat, sugestões inline |
| [**Copilot no GitHub.com**](https://github.com/copilot) | GitHub | Chat imersivo sobre seus repositórios, criação de agentes e muito mais |
| [**Agente de nuvem GitHub Copilot**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | Atribua issues a agentes e receba PRs de volta |

Este curso tem foco no **GitHub Copilot CLI**, levando a assistência de IA diretamente para o seu terminal.

## 📚 Estrutura do curso

![Trilha de aprendizado do GitHub Copilot CLI](../../images/learning-path.png)

| Capítulo | Título | O que você vai construir |
|:--------:|--------|--------------------------|
| 00 | 🚀 [Início Rápido](./00-quick-start/README.md) | Instalação e verificação |
| 01 | 👋 [Primeiros Passos](./01-setup-and-first-steps/README.md) | Demos ao vivo + três modos de interação |
| 02 | 🔍 [Contexto e Conversas](./02-context-conversations/README.md) | Análise de projetos com múltiplos arquivos |
| 03 | ⚡ [Fluxos de Trabalho de Desenvolvimento](./03-development-workflows/README.md) | Revisão de código, depuração, geração de testes |
| 04 | 🤖 [Crie Assistentes de IA Especializados](./04-agents-custom-instructions/README.md) | Agentes personalizados para o seu fluxo de trabalho |
| 05 | 🛠️ [Automatize Tarefas Repetitivas](./05-skills/README.md) | Skills que carregam automaticamente |
| 06 | 🔌 [Conecte ao GitHub, Bancos de Dados e APIs](./06-mcp-servers/README.md) | Integração com servidores MCP |
| 07 | 🎯 [Juntando Tudo](./07-putting-it-together/README.md) | Fluxos de trabalho completos de funcionalidades |

## 📖 Como este curso funciona

Cada capítulo segue o mesmo padrão:

1. **Analogia com o mundo real**: Entenda o conceito por meio de comparações familiares
2. **Conceitos fundamentais**: Aprenda o conhecimento essencial
3. **Exemplos práticos**: Execute comandos reais e veja os resultados
4. **Atividade**: Pratique o que aprendeu
5. **O que vem a seguir**: Prévia do próximo capítulo

**Os exemplos de código são executáveis.** Todos os blocos de código de copilot neste curso podem ser copiados e executados no seu terminal.

## 📋 Referência de comandos do GitHub Copilot CLI

A [**referência de comandos do GitHub Copilot CLI**](https://docs.github.com/en/copilot/reference/cli-command-reference) ajuda você a encontrar comandos e atalhos de teclado para usar o Copilot CLI com eficiência.

## 🌐 Use seu idioma preferido

Este material está disponível nos seguintes idiomas.

[English](../../README.md) | [Español](../es-es/README.md) | [日本語](../ja-jp/README.md) | [한국어](../ko-kr/README.md) | [Português](./README.md) | [中文(简体)](../zh-cn/README.md)

## 🙋 Obtendo ajuda

- 🐛 **Encontrou um bug?** [Abra uma issue](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **Documentação oficial:** [Documentação do GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## Contribuindo

> **Observação**: O código usado no curso foi projetado para gerar tipos específicos de saída durante revisões, explicações e depuração, portanto não podemos aceitar PRs que alterem o código existente.

**Como contribuir:**

1. Faça um fork deste repositório e clone-o na sua máquina
2. Crie uma branch de funcionalidade (`git checkout -b minha-melhoria`)
3. Faça suas alterações
4. Envie um pull request

## Licença

Este projeto está licenciado nos termos da licença MIT de código aberto. Consulte o arquivo [LICENSE](../../LICENSE) para ver os termos completos.
