![Capítulo 00: Início Rápido](../../../00-quick-start/images/chapter-header.png)

Bem-vindo! Neste capítulo, você irá instalar o GitHub Copilot CLI (Interface de Linha de Comando), fazer login com a sua conta do GitHub e verificar que tudo está funcionando. Este é um capítulo de configuração rápida. Assim que estiver pronto, as demos de verdade começam no Capítulo 01!

## 🎯 Objetivos de aprendizado

Ao final deste capítulo, você terá:

- Instalado o GitHub Copilot CLI
- Feito login com a sua conta do GitHub
- Verificado que funciona com um teste simples

> ⏱️ **Tempo estimado**: ~10 minutos (5 min de leitura + 5 min de prática)

---

## ✅ Pré-requisitos

- **Conta no GitHub** com acesso ao Copilot. [Veja as opções de assinatura](https://github.com/features/copilot/plans). Estudantes e professores podem acessar o Copilot Pro [gratuitamente pelo GitHub Education](https://education.github.com/pack).
- **Noções básicas de terminal**: Familiaridade com comandos como `cd` e `ls`

### O que significa "Acesso ao Copilot"

O GitHub Copilot CLI requer uma assinatura ativa do Copilot. Você pode verificar o seu status em [github.com/settings/copilot](https://github.com/settings/copilot). Você verá uma das seguintes opções:

- **Copilot Individual** - Assinatura pessoal
- **Copilot Business** - Pela sua organização
- **Copilot Enterprise** - Pela sua empresa
- **GitHub Education** - Gratuito para estudantes/professores verificados

Se você vir "Você não tem acesso ao GitHub Copilot", será necessário usar a opção gratuita, assinar um plano ou ingressar em uma organização que ofereça acesso.

---

## Instalação

> ⏱️ **Estimativa de tempo**: A instalação leva de 2 a 5 minutos. A autenticação adiciona mais 1 a 2 minutos.

### GitHub Codespaces (Sem configuração)

Se você não quiser instalar os pré-requisitos, pode usar o GitHub Codespaces, que já vem com o GitHub Copilot CLI pronto para uso (você precisará fazer login), além de Python e pytest pré-instalados.

1. [Faça um fork deste repositório](https://github.com/github/copilot-cli-for-beginners/fork) para a sua conta no GitHub
2. Selecione **Code** > **Codespaces** > **Create codespace on main**
3. Aguarde alguns minutos para o contêiner ser construído
4. Você está pronto! O terminal será aberto automaticamente no ambiente do Codespace.

> 💡 **Verifique no Codespace**: Execute `cd samples/book-app-project && python book_app.py help` para confirmar que Python e o aplicativo de exemplo estão funcionando.

### Instalação Local

Siga estes passos se quiser executar o Copilot CLI na sua máquina local com os exemplos do curso.

1. Clone o repositório para ter os exemplos do curso na sua máquina:

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. Instale o Copilot CLI usando uma das opções a seguir.

    > 💡 **Não sabe qual escolher?** Use `npm` se você tiver Node.js instalado. Caso contrário, escolha a opção que corresponde ao seu sistema.

    ### Todas as plataformas (npm)

    ```bash
    # Se você tem Node.js instalado, esta é uma forma rápida de obter o CLI
    npm install -g @github/copilot
    ```

    ### macOS/Linux (Homebrew)

    ```bash
    brew install copilot-cli
    ```

    ### Windows (WinGet)

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux (Script de instalação)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>Opcional: Ativar o autocompletar no shell</summary>

O autocompletar no shell permite que você pressione **Tab** para completar subcomandos do `copilot`, opções de comandos e alguns valores de opções. Isso é opcional, mas pode ser útil quando você já estiver confortável usando o CLI.

O Copilot CLI atualmente suporta scripts de autocompletar para Bash, Zsh e Fish:

```shell
# Bash, somente a sessão atual
source <(copilot completion bash)

# Bash, persistente no Linux
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

Reinicie seu shell após adicionar o autocompletar persistente. O PowerShell é suportado para executar o Copilot CLI no Windows, mas `copilot completion` atualmente suporta apenas Bash, Zsh e Fish.

</details>

---

## Autenticação

Abra uma janela de terminal na raiz do repositório `copilot-cli-for-beginners`, inicie o CLI e permita o acesso à pasta.

```bash
copilot
```

Você será solicitado a confiar na pasta que contém o repositório (caso ainda não tenha feito isso). Você pode confiar apenas uma vez ou para todas as sessões futuras.

<img src="../../../00-quick-start/images/copilot-trust.png" alt="Confiando em arquivos de uma pasta com o Copilot CLI" width="800"/>

Após confiar na pasta, você pode fazer login com a sua conta do GitHub.

```
> /login
```

**O que acontece a seguir:**

1. O Copilot CLI exibe um código único (como `ABCD-1234`)
2. Seu navegador abre a página de autorização de dispositivo do GitHub. Faça login no GitHub caso ainda não tenha feito.
3. Insira o código quando solicitado
4. Selecione "Autorizar" para conceder acesso ao GitHub Copilot CLI
5. Retorne ao seu terminal — agora você está conectado!

<img src="../../../00-quick-start/images/auth-device-flow.png" alt="Fluxo de Autorização de Dispositivo - mostrando o processo de 5 etapas do login no terminal até a confirmação de login" width="800"/>

*O fluxo de autorização de dispositivo: o seu terminal gera um código, você o verifica no navegador e o Copilot CLI é autenticado.*

**Dica**: O login persiste entre sessões. Você só precisa fazer isso uma vez, a menos que o seu token expire ou você saia explicitamente.

---

## Verificar se funciona

### Etapa 1: Testar o Copilot CLI

Agora que você está conectado, vamos verificar se o Copilot CLI está funcionando. No terminal, inicie o CLI se ainda não tiver feito isso:

```bash
> Say hello and tell me what you can help with
```

Após receber uma resposta, você pode sair do CLI:

```bash
> /exit
```

---

<details>
<summary>🎬 Veja em ação!</summary>

![Demo Olá](../../../00-quick-start/images/hello-demo.gif)

*A saída da demo pode variar. O seu modelo, ferramentas e respostas serão diferentes do que está mostrado aqui.*

</details>

---

**Saída esperada**: Uma resposta amigável listando as capacidades do Copilot CLI.

### Etapa 2: Executar o aplicativo de livros de exemplo

O curso fornece um aplicativo de exemplo que você irá explorar e melhorar ao longo do curso usando o CLI *(Você pode ver o código em /samples/book-app-project)*. Verifique se o *aplicativo de coleção de livros em Python* funciona antes de começar. Execute `python` ou `python3` dependendo do seu sistema.

> **Observação:** Os exemplos principais mostrados ao longo do curso usam Python (`samples/book-app-project`), portanto você precisará ter [Python 3.10+](https://www.python.org/downloads/) disponível na sua máquina local se escolheu essa opção (o Codespace já o tem instalado). Versões em JavaScript (`samples/book-app-project-js`) e C# (`samples/book-app-project-cs`) também estão disponíveis se preferir trabalhar com essas linguagens. Cada exemplo tem um README com instruções para executar o aplicativo nessa linguagem.

```bash
cd samples/book-app-project
python book_app.py list
```

**Saída esperada**: Uma lista de 5 livros incluindo "The Hobbit", "1984" e "Dune".

### Etapa 3: Experimentar o Copilot CLI com o aplicativo de livros

Volte primeiro para a raiz do repositório (se executou a Etapa 2):

```bash
cd ../..   # Voltar para a raiz do repositório, se necessário
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**Saída esperada**: Um resumo das principais funções e comandos do aplicativo de livros.

Se você vir um erro, verifique a [seção de solução de problemas](#troubleshooting) abaixo.

Quando terminar, você pode sair do Copilot CLI:

```bash
> /exit
```

---

## ✅ Você está pronto!

É isso para a instalação. A diversão de verdade começa no Capítulo 01, onde você irá:

- Ver a IA revisar o aplicativo de livros e encontrar problemas de qualidade de código instantaneamente
- Aprender três formas diferentes de usar o Copilot CLI
- Gerar código funcional a partir de linguagem natural

[**Continuar para o Capítulo 01: Primeiros Passos →**](../01-setup-and-first-steps/README.md)

---

## Solução de problemas

### "copilot: command not found"

O CLI não está instalado. Tente um método de instalação diferente:

```bash
# Se o brew falhou, tente npm:
npm install -g @github/copilot

# Ou o script de instalação:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. Verifique se você tem uma assinatura do Copilot em [github.com/settings/copilot](https://github.com/settings/copilot)
2. Verifique se a sua organização permite acesso ao CLI se estiver usando uma conta de trabalho

### "Authentication failed"

Faça a autenticação novamente:

```bash
copilot
> /login
```

### O navegador não abre automaticamente

Visite manualmente [github.com/login/device](https://github.com/login/device) e insira o código exibido no seu terminal.

### Token expirado

Simplesmente execute `/login` novamente:

```bash
copilot
> /login
```

### Ainda com problemas?

- Consulte a [documentação do GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- Pesquise nas [Issues do GitHub](https://github.com/github/copilot-cli/issues)

---

## 🔑 Principais aprendizados

1. **Um GitHub Codespace é uma forma rápida de começar** - Python, pytest e o GitHub Copilot CLI já vêm pré-instalados para que você pule direto para as demos
2. **Múltiplos métodos de instalação** - Escolha o que funciona para o seu sistema (Homebrew, WinGet, npm ou script de instalação)
3. **Autenticação única** - O login persiste até o token expirar
4. **O aplicativo de livros funciona** - Você usará `samples/book-app-project` ao longo de todo o curso

> 📚 **Documentação oficial**: [Instalar o Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) para opções e requisitos de instalação.

> 📋 **Referência rápida**: Veja a [referência de comandos do GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para uma lista completa de comandos e atalhos.

---

[**Continuar para o Capítulo 01: Primeiros Passos →**](../01-setup-and-first-steps/README.md)
