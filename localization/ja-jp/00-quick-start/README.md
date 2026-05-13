![第 00 章: クイックスタート](../../../00-quick-start/images/chapter-header.png)

ようこそ！この章では、GitHub Copilot CLI（コマンドラインインターフェース）のインストール、GitHub アカウントでのサインイン、そして動作確認を行います。これはクイックセットアップの章です。準備ができたら、第 01 章から本格的なデモが始まります！

## 🎯 学習目標

この章を終えると、以下が完了しています。

- GitHub Copilot CLI のインストール
- GitHub アカウントでのサインイン
- 簡単なテストによる動作確認

> ⏱️ **目安時間**: 約 10 分（読むのに 5 分 + ハンズオンに 5 分）

---

## ✅ 前提条件

- **Copilot アクセス付きの GitHub アカウント**。[サブスクリプションオプションを確認する](https://github.com/features/copilot/plans)。学生・教員の方は [GitHub Education](https://education.github.com/pack) で Copilot Pro を無料で利用できます。
- **ターミナルの基礎**: `cd` や `ls` などのコマンドに慣れていること

### 「Copilot アクセス」とは

GitHub Copilot CLI を使用するには、有効な Copilot サブスクリプションが必要です。[github.com/settings/copilot](https://github.com/settings/copilot) でステータスを確認してください。以下のいずれかが表示されているはずです。

- **Copilot Individual** - 個人サブスクリプション
- **Copilot Business** - 組織経由
- **Copilot Enterprise** - エンタープライズ経由
- **GitHub Education** - 認定学生・教員向け無料

「You don't have access to GitHub Copilot」と表示される場合は、無料オプションを利用するか、プランに加入するか、アクセスを提供する組織に参加する必要があります。

---

## インストール

> ⏱️ **所要時間の目安**: インストールに 2〜5 分、認証に さらに 1〜2 分かかります。

### GitHub Codespaces（セットアップ不要）

前提条件のインストールを避けたい場合は、GitHub Codespaces を使用できます。Copilot CLI がすぐに使える状態で用意されており（サインインは必要）、Python と pytest も事前インストールされています。

1. [このリポジトリをフォーク](https://github.com/github/copilot-cli-for-beginners/fork)して自分の GitHub アカウントに追加する
2. **Code** > **Codespaces** > **Create codespace on main** を選択する
3. コンテナのビルドが完了するまで数分待つ
4. 準備完了！Codespace 環境でターミナルが自動的に開きます。

> 💡 **Codespace での確認**: `cd samples/book-app-project && python book_app.py help` を実行して、Python とサンプルアプリが動作していることを確認しましょう。

### ローカルインストール

ローカルマシンでコースサンプルと一緒に Copilot CLI を動かしたい場合は、以下の手順に従ってください。

1. コースサンプルをマシンに取得するため、リポジトリをクローンします。

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 以下のいずれかの方法で Copilot CLI をインストールします。

    > 💡 **どれを選べばよいか迷ったら？** Node.js がインストールされている場合は `npm` を使うのが手軽です。それ以外は自分のシステムに合った方法を選んでください。

    ### すべてのプラットフォーム（npm）

    ```bash
    # Node.js がインストールされていれば、これが最も手軽な方法です
    npm install -g @github/copilot
    ```

    ### macOS/Linux（Homebrew）

    ```bash
    brew install copilot-cli
    ```

    ### Windows（WinGet）

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux（インストールスクリプト）

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>オプション: シェルのタブ補完を有効にする</summary>

シェルのタブ補完を使うと、**Tab** キーを押して `copilot` のサブコマンド、コマンドオプション、一部のオプション値を補完できます。これはオプションですが、CLI に慣れてきたら便利です。

Copilot CLI は現在 Bash、Zsh、Fish の補完スクリプトをサポートしています。

```shell
# Bash、現在のセッションのみ
source <(copilot completion bash)

# Bash、Linux で永続化
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

永続的な補完を追加した後はシェルを再起動してください。Windows では PowerShell で Copilot CLI を実行できますが、`copilot completion` は現在 Bash、Zsh、Fish のみをサポートしています。

</details>

---

## 認証

`copilot-cli-for-beginners` リポジトリのルートでターミナルを開き、CLI を起動してフォルダへのアクセスを許可します。

```bash
copilot
```

リポジトリが含まれるフォルダを信頼するかどうか確認されます（まだ信頼していない場合）。1 回だけ信頼するか、今後のすべてのセッションで信頼するかを選べます。

<img src="../../../00-quick-start/images/copilot-trust.png" alt="Copilot CLI でフォルダ内のファイルを信頼する" width="800"/>

フォルダを信頼した後、GitHub アカウントでサインインできます。

```
> /login
```

**次に何が起こるか:**

1. Copilot CLI がワンタイムコード（例: `ABCD-1234`）を表示する
2. ブラウザが GitHub のデバイス認証ページを開く。まだ GitHub にサインインしていない場合はサインインする。
3. プロンプトが表示されたらコードを入力する
4. 「Authorize」を選択して GitHub Copilot CLI のアクセスを許可する
5. ターミナルに戻ると、サインイン完了です！

<img src="../../../00-quick-start/images/auth-device-flow.png" alt="デバイス認証フロー - ターミナルのログインからサインイン確認までの 5 ステップ" width="800"/>

*デバイス認証フロー: ターミナルでコードを生成し、ブラウザで確認すると Copilot CLI が認証されます。*

**ヒント**: サインインはセッションをまたいで持続します。トークンが期限切れになるか明示的にサインアウトするまで、1 回だけ行えば十分です。

---

## 動作確認

### ステップ 1: Copilot CLI をテストする

サインインできたので、Copilot CLI が動作しているか確認しましょう。ターミナルでまだ CLI を起動していない場合は起動します。

```bash
> Say hello and tell me what you can help with
```

レスポンスを受け取ったら、CLI を終了できます。

```bash
> /exit
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![Hello Demo](../../../00-quick-start/images/hello-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**期待される出力**: Copilot CLI の機能を説明する親しみやすいレスポンス。

### ステップ 2: サンプルブックアプリを実行する

コースには、CLI を使って探索・改善していくサンプルアプリが提供されています。*（コードは /samples/book-app-project で確認できます）*。始める前に、*Python ブックコレクションターミナルアプリ*が動作することを確認してください。システムに応じて `python` または `python3` を実行します。

> **注意:** コース全体の主な例は Python（`samples/book-app-project`）を使用しているため、ローカルオプションを選んだ場合は [Python 3.10+](https://www.python.org/downloads/) が必要です（Codespace にはすでにインストールされています）。JavaScript（`samples/book-app-project-js`）および C#（`samples/book-app-project-cs`）バージョンも用意されています。各サンプルには、その言語でアプリを実行するための README が含まれています。

```bash
cd samples/book-app-project
python book_app.py list
```

**期待される出力**: 「The Hobbit」「1984」「Dune」などを含む 5 冊の本のリスト。

### ステップ 3: ブックアプリで Copilot CLI を試す

（ステップ 2 を実行した場合は）まずリポジトリのルートに戻ります。

```bash
cd ../..   # 必要に応じてリポジトリのルートに戻る
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**期待される出力**: ブックアプリの主な関数とコマンドの概要。

エラーが表示された場合は、下記の[トラブルシューティング](#troubleshooting)セクションを確認してください。

完了したら Copilot CLI を終了できます。

```bash
> /exit
```

---

## ✅ 準備完了！

インストールはこれで完了です。第 01 章から本当の楽しみが始まります。そこでは以下を行います。

- AI がブックアプリをレビューしてコード品質の問題を即座に見つける様子を見る
- Copilot CLI を使う 3 つの方法を学ぶ
- 平易な日本語からコードを生成する

[**第 01 章: はじめの一歩に進む →**](../01-setup-and-first-steps/README.md)

---

## トラブルシューティング {#troubleshooting}

### 「copilot: command not found」

CLI がインストールされていません。別のインストール方法を試してください。

```bash
# brew が失敗した場合は npm を試す:
npm install -g @github/copilot

# またはインストールスクリプト:
curl -fsSL https://gh.io/copilot-install | bash
```

### 「You don't have access to GitHub Copilot」

1. [github.com/settings/copilot](https://github.com/settings/copilot) で Copilot サブスクリプションがあることを確認する
2. 職場のアカウントを使用している場合は、組織が CLI アクセスを許可していることを確認する

### 「Authentication failed」

再認証する:

```bash
copilot
> /login
```

### ブラウザが自動的に開かない

[github.com/login/device](https://github.com/login/device) に手動でアクセスし、ターミナルに表示されたコードを入力してください。

### トークンの有効期限切れ

`/login` を再度実行するだけです。

```bash
copilot
> /login
```

### まだ解決できない場合

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)を確認する
- [GitHub Issues](https://github.com/github/copilot-cli/issues) を検索する

---

## 🔑 重要なポイント

1. **GitHub Codespace はすぐに始める最短の方法** - Python、pytest、GitHub Copilot CLI がすべてプリインストールされており、デモにすぐ飛び込めます
2. **複数のインストール方法** - システムに合ったものを選んでください（Homebrew、WinGet、npm、またはインストールスクリプト）
3. **1 回限りの認証** - ログインはトークンが期限切れになるまで持続します
4. **ブックアプリが動作する** - コース全体を通して `samples/book-app-project` を使用します

> 📚 **公式ドキュメント**: インストールオプションと要件については [Copilot CLI のインストール](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)を参照してください。

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

[**第 01 章: はじめの一歩に進む →**](../01-setup-and-first-steps/README.md)
