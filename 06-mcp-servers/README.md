![第06章: MCP Servers](images/chapter-header.png)

> **Copilot が GitHub issues を読んだり、database を確認したり、PR を作ったりできるとしたらどうでしょうか？ しかも terminal からそのまま。**

これまでの Copilot は、`@` で渡した files、会話履歴、学習済み知識をもとに動いていました。では、GitHub repository を自分で見に行ったり、project files を調べたり、最新の library documentation を取得したりできたらどうでしょうか。

それを可能にするのが MCP（Model Context Protocol）です。Copilot を外部 service に接続し、live data を扱えるようにする仕組みです。Copilot が接続する各 service を「MCP server」と呼びます。この章では、その接続を設定し、Copilot がさらに実用的になる様子を見ていきます。

> 💡 **すでに MCP を知っている場合**: [quick start](#-use-the-built-in-github-mcp) から始めて、動作確認と設定を進めてください。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- MCP が何か、なぜ重要かを理解する
- `/mcp` commands で MCP servers を管理する
- GitHub、filesystem、documentation 用の MCP servers を設定する
- book app project で MCP-powered workflow を試す
- 必要に応じて custom MCP server を作る考え方を知る

> ⏱️ **想定時間**: 約50分（読む時間 15分 + ハンズオン 35分）

---

## 🧩 現実世界のたとえ: Browser Extensions

<img src="images/browser-extensions-analogy.png" alt="MCP Servers are like Browser Extensions" width="800"/>

MCP servers は browser extensions に少し似ています。browser 単体でも web page は見られますが、extension を入れると外部 service とつながって一気に便利になります。

| Browser Extension | つながるもの | MCP の例 |
|-------------------|---------------------|----------------|
| Password manager | password vault | **GitHub MCP** → repos、issues、PRs |
| Grammarly | writing analysis service | **Context7 MCP** → library docs |
| File manager | cloud storage | **Filesystem MCP** → local project files |

extensions なしでも browser は使えますが、extensions があると一気に強力になります。MCP servers も同じで、Copilot を GitHub、documentation、filesystem などの live data source とつなぎます。

***MCP servers は Copilot を GitHub、repos、documentation などの「外の世界」と接続します***

> 💡 **Key insight**: MCP がない場合、Copilot は `@` で明示的に共有された files しか見られません。MCP があると、project を自分で探索したり、GitHub repo を確認したり、docs を調べたりできます。

---

<img src="images/quick-start-mcp.png" alt="Power cable connecting with bright electrical spark surrounded by floating tech icons representing MCP server connections" width="800"/>

# Quick Start: MCP を 30 秒で試す

## built-in GitHub MCP server を試す

設定前に、まず MCP が動く感覚を見てみましょう。GitHub MCP server は built-in です。次を試してください。

```bash
copilot
> List the recent commits in this repository
```

実際の commit data が返ってきたら、すでに MCP を体験できています。GitHub は built-in の 1 例にすぎません。この章では、filesystem や最新 documentation を引く server も追加していきます。

---

## `/mcp show` Command

`/mcp show` を使うと、どの MCP server が設定されていて、enabled かどうかを確認できます。

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub server しか見えなくても大丈夫**: 追加 server をまだ入れていなければ、それが normal です。次の section で増やします。

> 📚 **`/mcp` の全 command を見たい場合**: chat 内の `/mcp` slash commands や terminal の `copilot mcp` が使えます。

<details>
<summary>🎬 動作例を見る</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

## MCP があると何が変わる？

実際の違いを比べると分かりやすいです。

**Without MCP:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**With MCP:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP があると、Copilot は実際の開発環境に即した data を使って答えられるようになります。

> 📚 **Official Documentation**: [About MCP](https://docs.github.com/copilot/concepts/context/mcp)

---

# Configuring MCP Servers

<img src="images/configuring-mcp-servers.png" alt="Hands adjusting knobs and sliders on a professional audio mixing board representing MCP server configuration" width="800"/>

MCP の雰囲気が分かったところで、追加 server を設定していきましょう。方法は 2 つあります。

- **built-in registry から入れる** - もっとも簡単。CLI が対話的に案内してくれます
- **config file を手で編集する** - 柔軟性が高い方法です

迷ったらまずは registry 方式がおすすめです。

---

## Registry から MCP Servers を入れる

CLI には MCP server registry が built-in であり、popular server を検索して guided setup できます。

```bash
copilot

> /mcp search
```

interactive picker が開き、必要な API key や path の設定もガイドしてくれます。

> 💡 **なぜ registry が便利なの？** npm package 名や JSON format を覚えなくても、CLI が設定を作ってくれるからです。

---

## MCP Configuration File

MCP server の設定は `~/.copilot/mcp-config.json`（user-level）または `.mcp.json`（project root）に保存します。

> ⚠️ **Note**: `.vscode/mcp.json` は現在サポート対象外です。古い config がある場合は `.mcp.json` に移してください。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*多くの MCP server は npm package として配布され、`npx` で実行されます。*

<details>
<summary>💡 <strong>JSON が初めてなら</strong> クリックして展開</summary>

| Field | 意味 |
|-------|---------------|
| `"mcpServers"` | すべての MCP server 設定を入れる container |
| `"server-name"` | 自分で付ける名前（例: github, filesystem） |
| `"type": "local"` | server は自分の machine 上で動く |
| `"command": "npx"` | 実行する program |
| `"args": [...]` | command に渡す引数 |
| `"tools": ["*"]` | その server の tool をすべて許可 |

**JSON で気を付けること:**
- string には double quotes `"` を使う
- 最後の要素に trailing comma を付けない
- valid な JSON にする

</details>

---

## MCP Servers を追加する

GitHub MCP server は built-in で追加設定不要です。それ以外の server は、興味のあるものから試せます。

| やりたいこと | 該当セクション |
|---|---|
| Copilot に project files を見せたい | [Filesystem Server](#filesystem-server) |
| 最新の library documentation を引きたい | [Context7 Server](#context7-server-documentation) |
| custom server や web access も見たい | [Beyond the Basics](#beyond-the-basics) |

<details>
<summary><strong>Filesystem Server</strong> - Copilot に project files を探索させる</summary>
<a id="filesystem-server"></a>

### Filesystem Server

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` path の意味**: `.` は current directory です。Copilot を起動した位置から相対的に file access できます。

</details>

<details>
<summary><strong>Context7 Server</strong> - 最新 documentation を引く</summary>
<a id="context7-server-documentation"></a>

### Context7 Server (Documentation)

Context7 を使うと、popular framework や library の最新 docs を引けます。training data だけに頼らず、現在の documentation を参照できるのが強みです。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **API key 不要**
- ✅ **account 不要**
- ✅ **自分の code は local のまま**

</details>

<details>
<summary><strong>Beyond the Basics</strong> - custom servers と web access（optional）</summary>
<a id="beyond-the-basics"></a>

ここは optional です。基本 server に慣れてからで十分です。

### Microsoft Learn MCP Server

Microsoft Learn MCP server を使うと、Azure や .NET、Microsoft 365 などの official docs に直接アクセスできます。

```bash
copilot

> /plugin install microsoftdocs/mcp
```

**使用例:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

### `web_fetch` による Web Access

Copilot CLI には built-in の `web_fetch` tool もあり、任意 URL の README や docs を取得できます。MCP server がなくても使える場面があります。

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### Custom MCP Server を作る

自分の API や internal tool とつなぎたい場合は、Python などで custom MCP server を作ることもできます。詳細は [Custom MCP Server Guide](mcp-custom-server.md) を参照してください。

</details>

<a id="complete-configuration-file"></a>

### Complete Configuration File

filesystem と Context7 を両方入れた full config の例です。

> 💡 **Note:** GitHub MCP は built-in なので、config file に書く必要はありません。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

---

# Using MCP Servers

設定できたら、次は実際に何ができるかを見ていきましょう。

<img src="images/using-mcp-servers.png" alt="Using MCP Servers - Hub-and-spoke diagram showing a Developer CLI connected to GitHub, Filesystem, Context7, and Custom/Web Fetch servers" width="800" />

---

## Server Usage Examples

| 試したいこと | 該当セクション |
|---|---|
| GitHub repos、issues、PRs | [GitHub Server](#github-server-built-in) |
| project files の閲覧 | [Filesystem Server Usage](#filesystem-server-usage) |
| library documentation lookup | [Context7 Server Usage](#context7-server-usage) |
| custom server や web_fetch | [Beyond the Basics Usage](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub Server (Built-in)</strong> - repos、issues、PRs などにアクセスする</summary>
<a id="github-server-built-in"></a>

### GitHub Server (Built-in)

GitHub MCP server は **built-in** です。初期 setup で `/login` していれば、そのまま使えます。

| Feature | Example |
|---------|----------|
| **Repository info** | commits、branches、contributors を見る |
| **Issues** | issue の一覧、作成、検索、comment |
| **Pull requests** | PR、diff、status の確認 |
| **Code search** | repository 横断で code を検索 |
| **Actions** | workflow run と status の確認 |

```bash
copilot

> List the last 5 commits in this repository
> What branches exist in this repository?
> Search this repository for files that import pytest
```

> 💡 **自分の fork で試す場合**: write access があれば issue 作成や PR 作成も試せます。

</details>

<details>
<summary><strong>Filesystem Server</strong> - project files を閲覧・分析する</summary>
<a id="filesystem-server-usage"></a>

### Filesystem Server

設定後は、filesystem MCP を使って files を探索できます。

```bash
copilot

> How many Python files are in the book-app-project directory?

> What's the total size of the data.json file?

> Find all functions that don't have type hints in the book app
```

</details>

<details>
<summary><strong>Context7 Server</strong> - library documentation を調べる</summary>
<a id="context7-server-usage"></a>

### Context7 Server

```bash
copilot

> What are the best practices for using pytest fixtures?

> How can I apply this to the book app's test file?
```

official docs の情報をもとに、project に即した advice が返ってきます。

</details>

<details>
<summary><strong>Beyond the Basics</strong> - custom server と web_fetch の利用</summary>
<a id="beyond-the-basics-usage"></a>

### Beyond the Basics

**Custom MCP Server**: [Custom MCP Server Guide](mcp-custom-server.md) で作った server に対して query を投げられます。

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP** も使えば、official Microsoft docs を直接引けます。

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch** では任意 URL の content を取得できます。

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## Multi-Server Workflows

複数 MCP server を組み合わせると、「もうこれなしでは戻れない」と感じる理由が分かってきます。

<img src="images/issue-to-pr-workflow.png" alt="Issue to PR Workflow using MCP - Shows the complete flow from getting a GitHub issue through creating a pull request" width="800"/>

*GitHub MCP で repo data、Filesystem MCP で files、Context7 MCP で best practices を取得し、Copilot がまとめて分析します。*

| 見たいこと | 該当セクション |
|---|---|
| 複数 server の連携 | [Multi-Server Exploration](#multi-server-exploration) |
| issue から PR までを 1 session で進める | [Issue-to-PR Workflow](#issue-to-pr-workflow) |
| project の health check | [Health Dashboard](#health-dashboard) |

<details>
<summary><strong>Multi-Server Exploration</strong> - filesystem、GitHub、Context7 を 1 session で組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数 MCP Servers で Book App を探索する

```bash
copilot

# Step 1: Use filesystem MCP to explore the book app
> List all Python files in samples/book-app-project/ and summarize
> what each file does

# Step 2: Use GitHub MCP to check recent changes
> What were the last 3 commits that touched files in samples/book-app-project/?

# Step 3: Use Context7 MCP for best practices
> What are Python best practices for JSON data persistence?

# Step 4: Synthesize a recommendation
> Based on the book app code and these best practices,
> what improvements would you suggest?
```

<details>
<summary>🎬 MCP workflow の動作例を見る</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

**結果**: code exploration → history review → best practices lookup → improvement plan を、1 つの terminal session のまま進められます。

</details>

<details>
<summary><strong>Issue-to-PR Workflow</strong> - GitHub issue から pull request まで terminal を離れずに進める</summary>
<a id="issue-to-pr-workflow"></a>

#### The Issue-to-PR Workflow

```bash
copilot

> Get the details of GitHub issue #1

> @samples/book-app-project/books.py Fix the issue described in issue #1

> Run the tests to make sure the fix works

> Create a pull request titled "Add year validation to book app"
```

**copy-paste なし、context switching なし、1 つの terminal session だけで進められます。**

</details>

<details>
<summary><strong>Health Dashboard</strong> - 複数 server を使って project の health check をする</summary>
<a id="health-dashboard"></a>

#### Book App Health Dashboard

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory
```

**結果**: 複数 data source の情報をまとめて数秒で把握できます。手作業なら grep や git log、test file の確認などで 15 分以上かかることもあります。

</details>

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

**🎉 ここまでで essentials は理解できました。** では、実際に自分で試してみましょう。

---

## ▶️ Try It Yourself

### Exercise 1: MCP Status を確認する

```bash
copilot

> /mcp show
```

GitHub server が enabled と表示されれば OK です。表示されない場合は `/login` してください。

---

### Exercise 2: Filesystem MCP で Book App を探る

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**: `book_app.py`、`books.py`、`utils.py` とその functions が表示されます。

---

### Exercise 3: GitHub MCP で Repository History を見る

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**: GitHub remote の recent commits や branch names が表示されます。

---

### Exercise 4: 複数 MCP Servers を組み合わせる

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**Self-Check**: 「repo の commit history を見て」と頼む方が、`git log` を手で実行して貼り付けるよりなぜ便利か説明できれば、MCP の価値を理解できています。

---

## 📝 Assignment

### Main Challenge: Book App MCP Exploration

book app project で MCP servers を組み合わせて使う練習です。1 つの Copilot session の中で次を進めてください。

1. **MCP が動いているか確認**: `/mcp show` を実行し、少なくとも GitHub server が enabled であることを確認する
2. **filesystem MCP を設定**（まだなら）: `~/.copilot/mcp-config.json` に filesystem config を追加する
3. **code を探索**: filesystem server を使って次を確認する
   - `samples/book-app-project/books.py` の functions 一覧
   - `samples/book-app-project/utils.py` で type hints がない functions
   - `samples/book-app-project/data.json` の data quality issue
4. **repository activity を確認**: GitHub MCP を使って次を見る
   - `samples/book-app-project/` に関連する recent commits
   - open issues や pull requests があるか
5. **servers を組み合わせる**: test file を読み、`books.py` の functions と比較し、足りない test coverage をまとめる

**成功条件**: filesystem と GitHub MCP の data を 1 つの session で自然に組み合わせられることです。

<details>
<summary>💡 Hints（クリックして展開）</summary>

**Step 1: Verify MCP**
```bash
copilot
> /mcp show
```

**Step 2: config file を作る**

この章の [Complete Configuration](#complete-configuration-file) を `~/.copilot/mcp-config.json` に保存します。

**Step 3: data quality issue のヒント**

`data.json` の最後の book には、author が空、year が 0 という問題があります。

**Step 5: test coverage comparison**

`test_books.py` は一部 functions をカバーしていますが、`load_books`、`save_books`、`list_books` などには direct test が不足しています。

</details>

### Bonus Challenge: Custom MCP Server を作る

さらに深く学びたい場合は、[Custom MCP Server Guide](mcp-custom-server.md) を使って、自分の API につながる MCP server を作ってみてください。

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong>（クリックして展開）</summary>

### Common Mistakes

| Mistake | 起きること | Fix |
|---------|--------------|-----|
| GitHub MCP が built-in だと知らない | 手動インストールしようとしてしまう | まずは「List the recent commits in this repo」を試す |
| config file の場所を間違える | MCP settings を見つけられない | user-level は `~/.copilot/mcp-config.json`、project-level は `.mcp.json` |
| JSON が無効 | MCP server が読み込まれない | `/mcp show` で確認し、JSON syntax を見直す |
| 認証を忘れる | authentication failed が出る | 必要に応じて `/login` を実行する |

### Troubleshooting

**"MCP server not found"** - npm package、config の JSON、server 名を確認します。

**"GitHub authentication failed"** - built-in GitHub MCP は `/login` credentials を使います。再認証してください。

```bash
copilot
> /login
```

**"MCP tools not available"** - `/mcp show` で enabled か確認します。

</details>

---

# Summary

## 🔑 Key Takeaways

1. **MCP** は Copilot を外部 service（GitHub、filesystem、documentation）に接続する
2. **GitHub MCP は built-in** - 追加設定なしで使える
3. **Filesystem と Context7** は `~/.copilot/mcp-config.json` などで設定する
4. **複数 server を組み合わせる** と、1 session で investigation や planning ができる
5. **管理方法は 2 通り**: chat 内の `/mcp` slash commands と、terminal の `copilot mcp`
6. **custom server** を使えば、任意の API にもつなげられる

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次は？

これで、modes、context、workflows、agents、skills、MCP という building blocks がそろいました。最後の Chapter 07 では、それらを 1 つの実践 workflow にまとめます。

**[Chapter 07: Putting It All Together](../07-putting-it-together/README.md)** では、次のことを学びます。

- agents、skills、MCP を組み合わせた unified workflow
- idea から merged PR までの流れ
- hooks を使った automation
- team development での best practices

---

**[← Chapter 05 に戻る](../05-skills/README.md)** | **[Chapter 07 へ進む →](../07-putting-it-together/README.md)**
