![第00章: クイックスタート](images/chapter-header.png)

ようこそ！この章では、GitHub Copilot CLI (Command Line Interface) をインストールし、GitHub アカウントでサインインして、正しく動作することを確認します。ここは短いセットアップ章です。準備が終われば、第01章から本格的なデモに入れます。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- GitHub Copilot CLI をインストールできる
- GitHub アカウントでサインインできる
- 簡単なテストで動作確認できる

> ⏱️ **想定時間**: 約10分（読む時間 5分 + ハンズオン 5分）

---

## ✅ 前提条件

- **GitHub Account** と Copilot へのアクセス権。[プラン一覧はこちら](https://github.com/features/copilot/plans)。学生・教職員は [GitHub Education](https://education.github.com/pack) から Copilot Pro を無料で利用できます。
- **Terminal の基本操作**: `cd` や `ls` などのコマンドに慣れていること

### 「Copilot Access」とは？

GitHub Copilot CLI を使うには、有効な Copilot サブスクリプションが必要です。状態は [github.com/settings/copilot](https://github.com/settings/copilot) で確認できます。次のいずれかが表示されるはずです。

- **Copilot Individual** - 個人向けサブスクリプション
- **Copilot Business** - 組織経由で利用
- **Copilot Enterprise** - エンタープライズ経由で利用
- **GitHub Education** - 認証済みの学生・教職員向け無料利用

「You don't have access to GitHub Copilot」と表示される場合は、無料枠を使うか、プランに登録するか、利用権のある組織に参加する必要があります。

---

## Installation

> ⏱️ **時間の目安**: インストールは 2〜5 分ほど、認証はさらに 1〜2 分ほどです。

### GitHub Codespaces（セットアップ不要）

前提ツールを自分で入れたくない場合は、GitHub Codespaces を使うのが最も簡単です。GitHub Copilot CLI がすぐ使える状態で用意されており（サインインは必要です）、Python と pytest も事前にインストールされています。

1. [このリポジトリを Fork](https://github.com/github/copilot-cli-for-beginners/fork) して自分の GitHub アカウントにコピーします
2. **Code** > **Codespaces** > **Create codespace on main** を選びます
3. コンテナーのビルドが終わるまで数分待ちます
4. これで準備完了です。terminal は Codespace 環境で自動的に開きます

> 💡 **Codespace での確認**: `cd samples/book-app-project && python book_app.py help` を実行して、Python とサンプル app が動くことを確認しましょう。

### Local Installation

ローカル環境で Copilot CLI とこのコースのサンプルを使いたい場合は、次の手順に進んでください。

1. まず repo を clone して、手元にコース用サンプルを用意します。

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 次のいずれかの方法で Copilot CLI をインストールします。

    > 💡 **どれを選べばよいかわからない場合**: Node.js が入っていれば `npm` が手軽です。そうでなければ、自分の環境に合った方法を選んでください。

    ### All Platforms (npm)

    ```bash
    # If you have Node.js installed, this is a quick way to get the CLI
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

    ### macOS/Linux (Install Script)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

---

## Authentication

`copilot-cli-for-beginners` repository のルートで terminal を開き、CLI を起動してフォルダーへのアクセスを許可します。

```bash
copilot
```

まだ許可していない場合は、この repository を含むフォルダーを信頼するか尋ねられます。今回だけ許可することも、今後のセッションすべてで信頼することもできます。

<img src="images/copilot-trust.png" alt="Trusting files in a folder with the Copilot CLI" width="800"/>

フォルダーを信頼したら、GitHub アカウントでサインインします。

```
> /login
```

**次に起きること:**

1. Copilot CLI が 1 回限りのコード（例: `ABCD-1234`）を表示します
2. ブラウザーで GitHub の device authorization ページが開きます。まだサインインしていなければ、ここで GitHub にログインします
3. 表示されたコードを入力します
4. 「Authorize」を選んで GitHub Copilot CLI にアクセス権を付与します
5. terminal に戻ればサインイン完了です

<img src="images/auth-device-flow.png" alt="Device Authorization Flow - showing the 5-step process from terminal login to signed-in confirmation" width="800"/>

*device authorization の流れ: terminal がコードを発行し、ブラウザーで確認すると、Copilot CLI が認証されます。*

**Tip**: サインイン状態はセッションをまたいで保持されます。トークンの期限切れや明示的なサインアウトがない限り、毎回ログインし直す必要はありません。

---

## Verify It Works

### Step 1: Copilot CLI を試す

サインインできたら、まずは Copilot CLI が自分の環境で動いているかを確認しましょう。まだ CLI を起動していなければ、terminal で次を実行します。

```bash
> Say hello and tell me what you can help with
```

応答が返ってきたら、次で終了できます。

```bash
> /exit
```

---

<details>
<summary>🎬 動作例を見る</summary>

![Hello Demo](images/hello-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**期待される出力**: Copilot CLI ができることを案内する、フレンドリーな返答が表示されます。

### Step 2: サンプル Book App を動かす

このコースでは、CLI を使ってサンプル app を読み解き、改善していきます *(コードは /samples/book-app-project にあります)*。始める前に、*Python の book collection terminal app* が動くことを確認しましょう。環境に応じて `python` または `python3` を使ってください。

> **Note:** このコースの主な例は Python (`samples/book-app-project`) を使います。そのため、ローカルで進める場合は [Python 3.10+](https://www.python.org/downloads/) が必要です（Codespace にはすでに入っています）。必要に応じて JavaScript (`samples/book-app-project-js`) や C# (`samples/book-app-project-cs`) 版も利用できます。各サンプルには、その言語で app を動かすための README が付いています。

```bash
cd samples/book-app-project
python book_app.py list
```

**期待される出力**: 「The Hobbit」「1984」「Dune」を含む 5 冊の本の一覧が表示されます。

### Step 3: Book App で Copilot CLI を試す

Step 2 を実行した場合は、まず repository のルートに戻ります。

```bash
cd ../..   # Back to the repository root if needed
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**期待される出力**: book app の主要な機能やコマンドの概要が返ってきます。

エラーが出た場合は、下の [troubleshooting section](#troubleshooting) を確認してください。

終わったら Copilot CLI を終了します。

```bash
> /exit
```

---

## ✅ 準備完了です！

インストール作業はこれで完了です。第01章では、いよいよ本格的な活用に進みます。

- AI が book app を review して、コード品質の問題をすぐ見つける様子を見る
- Copilot CLI の 3 つの使い方を学ぶ
- 自然言語から動くコードを生成する

**[第01章へ進む: First Steps →](../01-setup-and-first-steps/README.md)**

---

## Troubleshooting

### "copilot: command not found"

CLI がインストールされていません。別の方法を試してください。

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. [github.com/settings/copilot](https://github.com/settings/copilot) で Copilot サブスクリプションを確認します
2. 仕事用アカウントなら、所属 organization が CLI 利用を許可しているか確認します

### "Authentication failed"

再認証します。

```bash
copilot
> /login
```

### Browser doesn't open automatically

手動で [github.com/login/device](https://github.com/login/device) にアクセスし、terminal に表示されたコードを入力してください。

### Token expired

もう一度 `/login` を実行するだけで大丈夫です。

```bash
copilot
> /login
```

### まだ解決しない場合

- [GitHub Copilot CLI documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) を確認する
- [GitHub Issues](https://github.com/github/copilot-cli/issues) を検索する

---

## 🔑 重要ポイント

1. **GitHub Codespace は最速のスタート方法** - Python、pytest、GitHub Copilot CLI が最初から使えるので、すぐにデモに入れます
2. **インストール方法はいくつかある** - Homebrew、WinGet、npm、install script から自分の環境に合うものを選べます
3. **認証は基本 1 回でOK** - トークンが切れるまでログイン状態は保持されます
4. **book app が今後の中心教材** - コース全体を通して `samples/book-app-project` を使います

> 📚 **Official Documentation**: インストール方法や要件は [Install Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) を参照してください。

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

**[第01章へ進む: First Steps →](../01-setup-and-first-steps/README.md)**
