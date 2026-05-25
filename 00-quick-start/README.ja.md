![Chapter 00: Quick Start](images/chapter-header.png)

ようこそ！この章では、GitHub Copilot CLI（コマンドラインインターフェース）をインストールし、GitHub アカウントでサインインして、すべてが正常に動作することを確認します。これはクイックセットアップの章です。準備が整えば、第01章から本格的なデモが始まります！

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- GitHub Copilot CLI のインストール
- GitHub アカウントでのサインイン
- 簡単なテストによる動作確認

> ⏱️ **推定所要時間**: 約10分（読みもの5分 ＋ 実践5分）

---

## ✅ 前提条件

- **GitHub アカウント**: Copilot へのアクセス権が必要です。[サブスクリプションオプションはこちら](https://github.com/features/copilot/plans)。学生や教職員の方は、[GitHub Education を通じて無料で Copilot Pro を利用](https://education.github.com/pack)できる場合があります。
- **ターミナルの基本操作**: `cd` や `ls` などのコマンド操作に慣れていること。

### 「Copilot へのアクセス権」とは

GitHub Copilot CLI を使用するには、有効な Copilot サブスクリプションが必要です。ステータスは [github.com/settings/copilot](https://github.com/settings/copilot) で確認できます。以下のいずれかが表示されているはずです：

- **Copilot Individual** - 個人向けサブスクリプション
- **Copilot Business** - 組織経由
- **Copilot Enterprise** - エンタープライズ経由
- **GitHub Education** - 認証済みの学生・教職員向け（無料）

「You don't have access to GitHub Copilot」と表示される場合は、無料オプションを利用するか、プランに加入するか、アクセス権を提供している組織に参加する必要があります。

---

## インストール

> ⏱️ **時間の目安**: インストールに2〜5分。認証にさらに1〜2分かかります。

### GitHub Codespaces (セットアップ不要)

前提条件をインストールしたくない場合は、GitHub Codespaces を使用できます。これには GitHub Copilot CLI があらかじめ用意されており（サインインは必要）、Python や pytest もインストールされています。

1. [このリポジトリをフォーク](https://github.com/github/copilot-cli-for-beginners/fork)して自分の GitHub アカウントにコピーします。
2. **Code** > **Codespaces** > **Create codespace on main** を選択します。
3. コンテナが構築されるまで数分待ちます。
4. 準備完了です！ターミナルが Codespace 環境で自動的に開きます。

> 💡 **Codespace での確認**: `cd samples/book-app-project && python book_app.py help` を実行して、Python とサンプルアプリが動作することを確認してください。

### ローカルインストール

ローカルマシンで Copilot CLI を実行し、コースのサンプルを使用したい場合は、以下の手順に従ってください。

1. リポジトリをクローンして、サンプルコードを入手します：

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 以下のいずれかのオプションを使用して Copilot CLI をインストールします。

    > 💡 **どれを選べばいいかわからない場合**: Node.js がインストールされているなら `npm` を使用してください。それ以外の場合は、お使いのシステムに合ったオプションを選んでください。

    ### 全プラットフォーム (npm)

    ```bash
    # Node.js がインストールされている場合、これが最も簡単な方法です
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

    ### macOS/Linux (インストールスクリプト)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>オプション：シェルのタブ補完を有効にする</summary>

シェルのタブ補完を使用すると、**Tab** キーを押すことで `copilot` のサブコマンド、コマンドオプション、および一部のオプション値を補完できます。これは必須ではありませんが、CLI の操作に慣れてくると非常に便利です。

GitHub Copilot CLI は現在、Bash、Zsh、および Fish の補完スクリプトをサポートしています：

```shell
# Bash（現在のセッションのみ）
source <(copilot completion bash)

# Bash（Linux で永続化する場合）
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

永続的な補完を追加した後は、シェルを再起動してください。Windows 上での Copilot CLI の実行には PowerShell もサポートされていますが、`copilot completion` は現在のところ Bash、Zsh、および Fish のみをサポートしています。

</details>

---

## 認証

`copilot-cli-for-beginners` リポジトリのルートでターミナルを開き、CLI を起動してフォルダへのアクセスを許可します。

```bash
copilot
```

フォルダを信頼するかどうか尋ねられます（まだの場合）。今回のみ信頼するか、今後のすべてのセッションで信頼するかを選択できます。

<img src="images/copilot-trust.png" alt="Copilot CLI でフォルダ内のファイルを信頼する" width="800"/>

フォルダを信頼した後、GitHub アカウントでサインインできます。

```
> /login
```

**その後の流れ:**

1. Copilot CLI にワンタイムコード（例: `ABCD-1234`）が表示されます。
2. ブラウザで GitHub のデバイス認証ページが開きます。サインインしていない場合はサインインしてください。
3. プロンプトが表示されたら、コードを入力します。
4. 「Authorize」を選択して GitHub Copilot CLI にアクセス権を付与します。
5. ターミナルに戻ります。これでサインイン完了です！

<img src="images/auth-device-flow.png" alt="デバイス認証フロー - ターミナルでのログインからサインイン完了までの5ステップ" width="800"/>

*デバイス認証フロー：ターミナルでコードが生成され、ブラウザで確認し、Copilot CLI が認証されます。*

**ヒント**: サインイン状態はセッションをまたいで維持されます。トークンが期限切れになるか、明示的にサインアウトしない限り、この操作は一度だけで済みます。

---

## 動作確認

### ステップ 1: Copilot CLI のテスト

サインインが完了したので、Copilot CLI が動作するか確認しましょう。ターミナルで（まだ起動していなければ）CLI を起動します：

```bash
> Say hello and tell me what you can help with
```

（こんにちは、何を手伝ってくれるか教えて、といった意味です）

レスポンスを受け取ったら、CLI を終了できます：

```bash
> /exit
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Hello Demo](images/hello-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**期待される出力**: Copilot CLI ができることを説明する、フレンドリーな返答。

### ステップ 2: サンプル書籍アプリの実行

このコースでは、CLI を使って探索・改善していくサンプルアプリが用意されています（コードは `/samples/book-app-project` にあります）。開始する前に、この *Python 製書籍コレクション・ターミナルアプリ* が動作することを確認してください。システムに応じて `python` または `python3` を実行してください。

> **注意:** このコースの主な例では Python (`samples/book-app-project`) を使用するため、ローカルで進める場合は [Python 3.10 以上](https://www.python.org/downloads/)が必要です（Codespace にはインストール済みです）。JavaScript 版 (`samples/book-app-project-js`) や C# 版 (`samples/book-app-project-cs`) も用意されています。各サンプルには、その言語での実行方法を説明した README があります。

```bash
cd samples/book-app-project
python book_app.py list
```

**期待される出力**: "The Hobbit"、"1984"、"Dune" を含む5冊の本のリスト。

### ステップ 3: Copilot CLI で書籍アプリを試す

（ステップ 2 を実行した場合は）まずリポジトリのルートに戻ります：

```bash
cd ../..   # 必要に応じてリポジトリのルートに戻る
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**期待される出力**: 書籍アプリの主な機能とコマンドの概要。

エラーが表示される場合は、下の [トラブルシューティング](#トラブルシューティング) セクションを確認してください。

終わったら Copilot CLI を終了します：

```bash
> /exit
```

---

## ✅ 準備完了！

インストールは以上です。第01章からが本番です。次のような内容を学びます：

- AI が書籍アプリをレビューし、コード品質の問題を一瞬で見つける様子を見る
- Copilot CLI を使う3つの異なる方法を学ぶ
- 普通の英語から動作するコードを生成する

**[第01章：はじめの一歩へ続く →](../01-setup-and-first-steps/README.ja.md)**

---

## トラブルシューティング

### "copilot: command not found"

CLI がインストールされていません。別のインストール方法を試してください：

```bash
# Homebrew が失敗した場合は npm を試してください：
npm install -g @github/copilot

# またはインストールスクリプト：
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. [github.com/settings/copilot](https://github.com/settings/copilot) で Copilot のサブスクリプションがあるか確認してください。
2. 仕事用アカウントを使用している場合は、組織が CLI へのアクセスを許可しているか確認してください。

### "Authentication failed" (認証失敗)

再度認証を行ってください：

```bash
copilot
> /login
```

### ブラウザが自動的に開かない

手動で [github.com/login/device](https://github.com/login/device) にアクセスし、ターミナルに表示されたコードを入力してください。

### トークンの期限切れ

単に `/login` を再度実行してください：

```bash
copilot
> /login
```

### まだ解決しない場合

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)を確認してください。
- [GitHub Issues](https://github.com/github/copilot-cli/issues) を検索してください。

---

## 🔑 重要なポイント

1. **GitHub Codespace は手軽な開始方法です** - Python、pytest、GitHub Copilot CLI がすべてプリインストールされているため、すぐにデモに移れます。
2. **複数のインストール方法** - システムに合わせて選択できます（Homebrew、WinGet、npm、またはインストールスクリプト）。
3. **一度だけの認証** - ログイン状態はトークンが切れるまで維持されます。
4. **書籍アプリの動作確認** - コース全体を通して `samples/book-app-project` を使用します。

> 📚 **公式ドキュメント**: インストールオプションと要件については、[Install Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) を参照してください。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

**[第01章：はじめの一歩へ続く →](../01-setup-and-first-steps/README.ja.md)**
