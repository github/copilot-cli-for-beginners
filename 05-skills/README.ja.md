<!--
---
id: CopilotCLI-05
title: スキル
description: カスタムで再利用可能な CLI コマンド、パラメータ、連携を作成し、一般的なタスクを自動化します。
audience: Developers / Students / Terminal users
slug: skills
weight: 6
---
-->

![Chapter 05: Skills System](assets/chapter-header.png)

[English Version](./README.md)

> **もし Copilot が、あなたのチームのベストプラクティスを毎回説明しなくても自動的に適用してくれたらどうでしょうか？**

この章では、「Agent Skills（エージェント・スキル）」について学びます。これは、あなたのタスクに関連がある場合に Copilot が自動的に読み込む指示のフォルダです。エージェントが Copilot の *考え方* を変えるのに対し、スキルは *タスクを完了させるための具体的な方法* を教えるものです。セキュリティについて質問したときに常に適用されるセキュリティ監査スキルを作成したり、チーム標準のレビュー基準を構築して一貫したコード品質を確保したりする方法を学びます。また、スキルが Copilot CLI、VS Code、および GitHub Copilot クラウドエージェント間でどのように機能するかも確認します。


## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- Agent Skills の仕組みと使い所を理解する
- `SKILL.md` ファイルを使用してカスタムスキルを作成する
- 共有リポジトリのコミュニティ製スキルを使用する
- スキル、エージェント、MCP の使い分けを理解する

> ⏱️ **推定所要時間**: 約55分（読みもの20分 ＋ 実践35分）

---

## 🧩 現実世界の例え：電動工具

汎用的なドリルは便利ですが、専用のアタッチメントを付けることでさらに強力になります。
<img src="assets/power-tools-analogy.png" alt="電動工具 - スキルは Copilot の能力を拡張する" width="800"/>


スキルも同じように機能します。仕事に合わせてドリルの刃を交換するように、異なるタスクに合わせて Copilot にスキルを追加できます：

| スキル・アタッチメント | 目的 |
|------------|---------|
| `commit` | 一貫性のあるコミットメッセージを生成する |
| `security-audit` | OWASP の脆弱性をチェックする |
| `generate-tests` | 包括的な pytest テストを作成する |
| `code-checklist` | チームのコード品質基準を適用する |



*スキルは、Copilot ができることを拡張する専門のアタッチメントのようなものです*

---

# スキルの仕組み

<img src="assets/how-skills-work.png" alt="星空を背景に光の軌跡でつながれた、RPG風の光るスキルアイコン。Copilot のスキルを表現している" width="800"/>

スキルとは何か、なぜ重要なのか、そしてエージェントや MCP とどう違うのかを学びましょう。

---

## *スキル初心者の方へ* まずはこちらから！

1. **利用可能なスキルを確認する：**
   ```bash
   copilot
   > /skills list
   ```
   これにより、Copilot が見つけたすべてのスキルが表示されます。CLI 自体に組み込まれている **組み込みスキル**、プロジェクト内のスキル、および個人用フォルダのスキルが含まれます。

   > 💡 **組み込みスキル**: Copilot CLI には最初からインストールされているスキルがあります。例えば、`customizing-copilot-cloud-agents-environment` スキルは、Copilot クラウドエージェントの環境をカスタマイズするためのガイドを提供します。これらを使うために何かを作成したりインストールしたりする必要はありません。`/skills list` を実行して、何があるか見てみましょう。

2. **実際のスキルファイルを見る：** 用意されている [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) をチェックしてパターンを確認してください。YAML フロントマターと Markdown 形式の指示だけで構成されています。

3. **核心となる概念を理解する：** スキルは、あなたのプロンプトがスキルの「説明（description）」と一致したときに、Copilot が *自動的に* 読み込むタスク固有の指示です。有効化の手間は不要で、自然に質問するだけで適用されます。


## スキルを理解する

Agent Skills は、タスクに関連がある場合に Copilot が **自動的に読み込む** 指示、スクリプト、リソースが含まれたフォルダです。Copilot はあなたのプロンプトを読み、一致するスキルがあるかを確認し、関連する指示を自動的に適用します。

```bash
copilot

> Check books.py against our quality checklist
# Copilot はこれが "code-checklist" スキルに一致することを検知し、
# Python 品質チェックリストを自動的に適用します。

> Generate tests for the BookCollection class
# Copilot は "pytest-gen" スキルを読み込み、
# 推奨されるテスト構造を適用します。

> What are the code quality issues in this file?
# Copilot は "code-checklist" スキルを読み込み、
# チームの標準に照らしてチェックします。
```

> 💡 **重要な洞察**: スキルは、プロンプトがスキルの説明と一致したときに **自動的にトリガー** されます。自然に問いかけるだけで、舞台裏で Copilot が関連するスキルを適用してくれます。もちろん、次に説明するように直接呼び出すことも可能です。

> 🧰 **すぐに使えるテンプレート**: [ .github/skills](../.github/skills/) フォルダには、簡単にコピーして試せるシンプルなスキルが含まれています。

### スラッシュコマンドによる直接呼び出し

自動トリガーが主な仕組みですが、スキル名をスラッシュコマンドとして使用して **直接呼び出す** こともできます：

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

これにより、特定のスキルを確実に使用させたい場合に明示的なコントロールが可能になります。

#### 1つのメッセージで複数のスキルを組み合わせる

**1つのメッセージで複数のスキルを呼び出す**ことができます。また、スキルのスラッシュコマンドはプロンプトの先頭だけでなく、文章のどこに置いても構いません。これは、1回で2つの異なるチェックを行いたい場合に便利です：

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot は同じ回答の中でそれぞれの指定されたスキルを適用するため、個別に複数のメッセージを送信する手間が省けます。

> 💡 **ヒント**: スキルのスラッシュコマンドは、文章の中で最も自然に感じられる場所に配置できます。メッセージの先頭、途中、または末尾のどこに置いても機能します。

> 📝 **スキル vs エージェントの呼び出し**: スキルの呼び出しとエージェントの呼び出しを混同しないでください：
> - **スキル**: `/スキル名 <プロンプト>` 例：`/code-checklist Check this file`
> - **エージェント**: `/agent` (リストから選択) または `copilot --agent <名前>` (コマンドライン)
>
> もし同じ名前（例：「code-reviewer」）のスキルとエージェントの両方がある場合、`/code-reviewer` と入力するとエージェントではなく **スキル** が呼び出されます。

### スキルが使われたかどうかを知るには？

Copilot に直接聞くことができます：

```bash
> What skills did you use for that response?
（今の回答にはどのスキルを使った？）

> What skills do you have available for security reviews?
（セキュリティレビューに使えるスキルは何がある？）
```

### スキル vs エージェント vs MCP

スキルは、GitHub Copilot の拡張性モデルの一要素に過ぎません。エージェントや MCP サーバーとの比較は以下の通りです。

> *MCP についてはまだ心配しなくて大丈夫です。[第06章](../06-mcp-servers/)で詳しく扱います。ここでは全体像におけるスキルの位置付けを確認するために掲載しています。*

<img src="assets/skills-agents-mcp-comparison.png" alt="エージェント、スキル、MCP サーバーの違いと、それらがどのようにワークフローに組み合わさるかを示す比較図" width="800"/>

| 機能 | 何をするか | いつ使うか |
|---------|--------------|-------------|
| **エージェント** | AI の考え方を変える | 多くのタスクにわたって専門知識が必要なとき |
| **スキル** | タスク固有の指示を与える | 手順が決まっている特定の反復タスクのとき |
| **MCP** | 外部サービスに接続する | API からのライブデータが必要なとき |

幅広い専門知識にはエージェントを、特定のタスク指示にはスキルを、外部データには MCP を使用します。会話の中で、一つのエージェントが一つ以上のスキルを使用することもあります。例えば、エージェントにコードのチェックを依頼すると、`security-audit` スキルと `code-checklist` スキルの両方が自動的に適用されるといった具合です。

> 📚 **さらに詳しく**: スキルの形式やベストプラクティスに関する完全なリファレンスについては、公式ドキュメントの [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)（英語）を参照してください。

---

## 手動プロンプトから自動化された専門知識へ

スキルの作り方に飛び込む前に、なぜスキルを学ぶ価値があるのかを見てみましょう。一貫性の向上というメリットを理解すれば、「どうやって」作るのかがより腑に落ちるはずです。

### スキル導入前：不揃いなレビュー

コードレビューのたびに、何かを忘れてしまうかもしれません：

```bash
copilot

> Review this code for issues
# 一般的なレビューになり、チーム固有の懸念事項を見逃す可能性があります
```

あるいは、毎回長いプロンプトを書くことになります：

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

入力時間：**30秒以上**。一貫性：**その時の記憶力次第**。

### スキル導入後：自動化されたベストプラクティス

`code-checklist` スキルがインストールされていれば、自然に聞くだけで済みます：

```bash
copilot

> Check the book collection code for quality issues
```

**舞台裏で起きていること**:
1. Copilot がプロンプト内の「code quality（コード品質）」や「issues（問題）」という言葉に注目します。
2. スキルの説明を確認し、`code-checklist` スキルが一致することを発見します。
3. チームの品質チェックリストを自動的に読み込みます。
4. あなたがいちいち列挙しなくても、すべてのチェック項目を適用します。

<img src="assets/skill-auto-discovery-flow.png" alt="スキルの自動トリガーの仕組み - プロンプトを適切なスキルに自動的にマッチングさせる4ステップのフロー" width="800"/>

*自然に問いかけるだけ。Copilot がプロンプトを適切なスキルにマッチさせ、自動的に適用します。*

**出力例**:
```
## Code Checklist: books.py

### コード品質
- [合格] すべての関数に型ヒントがある
- [合格] bare except 句がない
- [合格] ミュータブルなデフォルト引数がない
- [合格] ファイル入出力にコンテキストマネージャが使われている
- [合格] 関数が50行以内である
- [合格] 変数名と関数名が PEP 8 に従っている

### 入力バリデーション
- [不合格] ユーザー入力がバリデーションされていない - add_book() があらゆる年の値を受け付けてしまう
- [不合格] エッジケースが完全に処理されていない - タイトルや著者に空文字列を受け付けてしまう
- [合格] エラーメッセージが明確で役立つ

### テスト
- [不合格] 対応する pytest テストが見つからない

### まとめ
マージ前に 3 項目の修正が必要です
```

**違い**: あなたが入力しなくても、チームの標準が毎回自動的に適用されます。

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Skill Trigger Demo](assets/skill-trigger-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

## 規模に応じた一貫性：チーム PR レビュー・スキル

チームに 10 項目の PR チェックリストがあると想像してください。スキルがなければ、すべての開発者がその 10 項目を覚えておく必要があり、誰かが必ず一つは忘れてしまいます。`pr-review` スキルがあれば、チーム全体で一貫したレビューを受けることができます：

```bash
copilot

> Can you review this PR?
```

Copilot は自動的にチームの `pr-review` スキルを読み込み、10 項目すべてをチェックします：

```
PR Review: feature/user-auth

## セキュリティ ✅
- ハードコードされたシークレットなし
- 入力バリデーションあり
- bare except 句なし

## コード品質 ⚠️
- [警告] 45行目に print 文あり - マージ前に削除してください
- [警告] 78行目の TODO に Issue 参照がない
- [警告] 公開関数に型ヒントがない

## テスト ✅
- 新しいテストが追加されている
- エッジケースがカバーされている

## ドキュメント ❌
- [不合格] 破壊的変更が CHANGELOG に記載されていない
- [不合格] API の変更に伴う OpenAPI スペックの更新が必要
```

**その威力**: チームメンバー全員が同じ基準を自動的に適用できます。新人はチェックリストを暗記する必要はなく、スキルがそれを処理してくれます。

---

# カスタムスキルの作成

<img src="assets/creating-managing-skills.png" alt="光るレゴのようなブロックの壁を構築する人間とロボットの手。スキルの作成と管理を表現している" width="800"/>

`SKILL.md` ファイルから独自のスキルを構築しましょう。

---

## スキルの置き場所

スキルは `.github/skills/`（プロジェクト固有）または `~/.copilot/skills/`（ユーザーレベル）に保存されます。

### Copilot がスキルを見つける仕組み

Copilot は以下の場所を自動的にスキャンしてスキルを探します：

| 場所 | 範囲 |
|----------|-------|
| `.github/skills/` | プロジェクト固有（git 経由でチームと共有） |
| `~/.copilot/skills/` | ユーザー固有（あなた個人のスキル） |

### スキルの構造

各スキルは、`SKILL.md` ファイルを含む独自のフォルダに配置します。オプションでスクリプト、例、その他のリソースを含めることもできます：

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # 必須：スキルの定義と指示
    ├── examples/          # オプション：Copilot が参照できる例のファイル
    │   └── sample.py
    └── scripts/           # オプション：スキルが使用できるスクリプト
        └── validate.sh
```

> 💡 **ヒント**: ディレクトリ名は、`SKILL.md` のフロントマターにある `name` と一致させるべきです（小文字とハイフンを使用）。

### SKILL.md の形式

スキルは、YAML フロントマターを備えたシンプルな Markdown 形式を使用します：

```markdown
---
name: code-checklist
description: セキュリティ、パフォーマンス、保守性のチェックを含む包括的なコード品質チェックリスト
license: MIT
---

# コードチェックリスト

コードをチェックする際は、以下の点を確認してください：

## セキュリティ
- SQL インジェクションの脆弱性
- XSS 脆弱性
- 認証/認可の問題
- 機密データの露出

## パフォーマンス
- N+1 クエリ問題（すべての項目に対して1つのクエリではなく、項目ごとにクエリを実行している）
- 不要なループや計算
- メモリリーク
- ブロッキング操作

## 保守性
- 関数の長さ（50行を超える関数にフラグを立てる）
- コードの重複
- エラーハンドリングの欠如
- 不明瞭な命名

## 出力形式
問題を重要度付きの番号付きリストで提供してください：
- [CRITICAL] - マージ前に修正必須
- [HIGH] - マージ前に修正すべき
- [MEDIUM] - 近いうちに対処すべき
- [LOW] - あれば望ましい
```

**YAML プロパティ:**

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | **はい** | 一意の識別子（小文字、スペースはハイフンに） |
| `description` | **はい** | スキルが何をするか、および Copilot がいつ使用すべきか |
| `license` | いいえ | このスキルに適用されるライセンス |

> 📖 **公式ドキュメント**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)（英語）

### 最初のスキルを作成する

OWASP Top 10 の脆弱性をチェックするセキュリティ監査スキルを作成してみましょう：

```bash
# スキル用ディレクトリの作成
mkdir -p .github/skills/security-audit

# SKILL.md ファイルの作成
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: OWASP (Open Web Application Security Project) Top 10 脆弱性をチェックするセキュリティに特化したコードレビュー
---

# セキュリティ監査

以下の項目をチェックするセキュリティ監査を実行してください：

## インジェクションの脆弱性
- SQL インジェクション（クエリ内での文字列結合）
- コマンドインジェクション（サニタイズされていないシェルコマンド）
- LDAP インジェクション
- XPath インジェクション

## 認証の問題
- ハードコードされた認証情報
- 脆弱なパスワード要件
- レート制限の欠如
- セッション管理の不備

## 機密データ
- 平文のパスワード
- コード内の API キー
- 機密情報のログ出力
- 暗号化の欠如

## アクセス制御
- 認可チェックの欠如
- 安全でない直接オブジェクト参照
- パストラバーサルの脆弱性

## 出力
見つかった各問題について以下を提供してください：
1. ファイル名と行番号
2. 脆弱性の種類
3. 重要度 (CRITICAL/HIGH/MEDIUM/LOW)
4. 推奨される修正案
EOF

# スキルをテストする（プロンプトに基づいて自動的にロードされます）
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot は「security vulnerabilities（セキュリティ脆弱性）」がスキルに一致することを検知し、
# 自動的に OWASP チェックリストを適用します。
```

**期待される出力例**（結果は異なります）：

```
セキュリティ監査: book-app-project

[HIGH] ハードコードされたファイルパス (book_app.py, 12行目)
  ファイルパスが設定可能ではなくハードコードされています
  修正案：環境変数または設定ファイルを使用してください

[MEDIUM] 入力バリデーションの欠如 (book_app.py, 34行目)
  ユーザー入力がサニタイズされずに直接関数に渡されています
  修正案：処理前に入力バリデーションを追加してください

✅ SQL インジェクションは見つかりませんでした
✅ ハードコードされた認証情報は見つかりませんでした
```

---

## 優れたスキルの説明（Description）を書く

`SKILL.md` の `description` フィールドは非常に重要です！これによって Copilot がスキルを読み込むかどうかが決まります：

```markdown
---
name: security-audit
description: セキュリティレビュー、脆弱性スキャン、SQLインジェクション、XSS、
  認証の問題、OWASP Top 10 脆弱性、およびセキュリティベストプラクティスの確認に使用します
---
```

> 💡 **ヒント**: 自然に質問するときに使うキーワードを含めましょう。「セキュリティレビュー」と聞くことが多いなら、説明にも「セキュリティレビュー」を含めます。

### スキルとエージェントの組み合わせ

スキルとエージェントは連携して動作します。エージェントが専門知識を提供し、スキルが具体的な指示を提供します：

```bash
# code-reviewer エージェントで開始
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer エージェントの専門知識と、
# code-checklist スキルのチェックリストが組み合わされます
```

---

# スキルの管理と共有

インストールされたスキルの確認、コミュニティ製スキルの検索、独自のスキルの共有方法について説明します。

<img src="assets/managing-sharing-skills.png" alt="スキルの管理と共有 - CLIスキルの発見、使用、作成、共有のサイクルを示している" width="800" />

---

## `/skills` コマンドによるスキルの管理

`/skills` コマンドを使用して、インストールされているスキルを管理します：

| コマンド | 何をするか |
|---------|--------------|
| `/skills list` | インストールされている全スキルを表示 |
| `/skills info <name>` | 特定のスキルの詳細を取得 |
| `/skills add <name>` | スキルを有効化する（リポジトリやマーケットプレイスから） |
| `/skills remove <name>` | スキルを無効化またはアンインストールする |
| `/skills reload` | `SKILL.md` ファイルを編集した後、スキルを再読み込みする |

> 💡 **覚えておいてください**: プロンプトごとにスキルを「有効化」する必要はありません。一度インストールされれば、プロンプトが説明と一致したときにスキルは **自動的にトリガー** されます。これらのコマンドは、どのスキルを利用可能にするかを管理するためのものであり、使うためのものではありません。

### 例：スキルの表示

```bash
copilot

> /skills list

利用可能なスキル：
- security-audit: OWASP Top 10 をチェックするセキュリティに特化したコードレビュー
- generate-tests: エッジケースを含む包括的なユニットテストを生成
- code-checklist: チームのコード品質チェックリスト
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: OWASP Top 10 の脆弱性をチェックするセキュリティに特化したコードレビュー
```

---

<details>
<summary>実際の動きを見てみよう！</summary>

![List Skills Demo](assets/list-skills-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

### `/skills reload` を使うタイミング

スキルの `SKILL.md` ファイルを作成または編集した後は、`/skills reload` を実行して、Copilot を再起動せずに変更を反映させます：

```bash
# スキルファイルを編集
# その後 Copilot 内で：
> /skills reload
Skills reloaded successfully.
```

> 💡 **補足**: `/compact` で会話履歴を要約した後でも、スキルの効果は維持されます。要約後に再読み込みする必要はありません。

---

## コミュニティ製スキルの検索と利用

### プラグイン（Plugins）を使用したスキルのインストール

> 💡 **プラグインとは？** プラグインは、スキル、エージェント、および MCP サーバーの設定を一つにまとめたインストール可能なパッケージです。Copilot CLI 用の「アプリストア」の拡張機能のようなものだと考えてください。

`/plugin` コマンドを使用して、これらのパッケージをブラウズおよびインストールできます：

```bash
copilot

> /plugin list
# インストール済みプラグインを表示

> /plugin marketplace
# 利用可能なプラグインをブラウズ

> /plugin install <plugin-name>
# マーケットプレイスからプラグインをインストール
```

ローカルのプラグインカタログを最新の状態に保つには、以下を実行して更新します：

```bash
copilot plugin marketplace update
```

プラグインは複数の機能を一括で提供できます。一つのプラグインに、互いに連携する関連スキル、エージェント、MCP サーバー設定が含まれている場合があります。

### コミュニティ製スキルリポジトリ

コミュニティリポジトリからも既成のスキルを入手できます：

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - スキルのドキュメントや例を含む、GitHub Copilot の公式リソース

### GitHub CLI を使用したコミュニティ製スキルのインストール

GitHub リポジトリからスキルをインストールする最も簡単な方法は、`gh skill install` コマンドを使用することです（[GitHub CLI v2.90.0 以上](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)（英語）が必要です）：

```bash
# awesome-copilot からスキルをブラウズして対話的に選択する
gh skill install github/awesome-copilot

# または、特定のスキルを直接インストールする
gh skill install github/awesome-copilot ai-ready

# すべてのプロジェクトで個人利用するためにインストールする（ユーザー共通スコープ）
gh skill install github/awesome-copilot ai-ready --scope user
```

> ⚠️ **インストール前の確認**: インストールする前に、必ずスキルの `SKILL.md` を読んでください。スキルは Copilot の動作を制御するため、悪意のあるスキルが有害なコマンドを実行させたり、予期しない方法でコードを修正させたりする可能性があります。

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

独自のスキルを構築し、テストすることで学んだことを応用してみましょう。

---

## ▶️ 自分で試してみる

### さらなるスキルを構築する

異なるパターンを示す2つのスキルを紹介します。前述の「最初のスキルを作成する」と同様の `mkdir` + `cat` ワークフローに従うか、適切な場所にコピー＆ペーストしてください。その他の例は [.github/skills](../.github/skills) にあります。

### pytest テスト生成スキル

コードベース全体で一貫した pytest の構造を保証するスキル：

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: フィクスチャやエッジケースを含む包括的な pytest テストを生成
---

# pytest テスト生成

以下の項目を含む pytest テストを生成してください：

## テスト構造
- pytest の規約（test_ プリフィックス）を使用する
- 可能な限り、一つのテストにつき一つのアサーションにする
- 期待される動作を説明する明確なテスト名にする
- setup/teardown にはフィクスチャを使用する

## カバレッジ
- 正常系（Happy path）のシナリオ
- エッジケース：None、空文字列、空のリスト
- 境界値
- pytest.raises() を使用したエラーシナリオ

## フィクスチャ
- 再利用可能なテストデータには @pytest.fixture を使用する
- ファイル操作には tmpdir/tmp_path を使用する
- 外部依存関係は pytest-mock でモックする

## 出力
適切なインポート文を含んだ、そのまま実行可能な完全なテストファイルを提供してください。
EOF
```

### チーム PR レビュー・スキル

チーム全体で一貫した PR レビュー基準を遵守させるスキル：

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: チーム標準の PR レビューチェックリスト
---

# PR レビュー

チームの標準に照らしてコードの変更をレビューしてください：

## セキュリティ・チェックリスト
- [ ] ハードコードされたシークレットや API キーがない
- [ ] すべてのユーザーデータに対して入力バリデーションがある
- [ ] bare except 句がない
- [ ] ログに機密データが含まれていない

## コード品質
- [ ] 関数が50行以内である
- [ ] 本番コードに print 文がない
- [ ] 公開関数に型ヒントがある
- [ ] ファイル入出力にコンテキストマネージャが使われている
- [ ] Issue 参照のない TODO がない

## テスト
- [ ] 新しいコードにテストがある
- [ ] エッジケースがカバーされている
- [ ] 説明なしにスキップされたテストがない

## ドキュメント
- [ ] API の変更がドキュメント化されている
- [ ] 破壊的変更が記されている
- [ ] 必要に応じて README が更新されている

## 出力形式
結果を以下のように提供してください：
- ✅ PASS: 問題ない項目
- ⚠️ WARN: 改善の余地がある項目
- ❌ FAIL: マージ前に修正が必須の項目
EOF
```

### さらに先へ

1. **スキル作成チャレンジ**: 以下の3点をチェックする `quick-review` スキルを作成してください：
   - bare except 句
   - 型ヒントの欠如
   - 不明瞭な変数名

   「Do a quick review of books.py」と聞いてテストしてみてください。

2. **スキルの比較**: 詳細なセキュリティレビューのプロンプトを手動で書くのにかかる時間を計ってみてください。次に、「Check for security issues in this file」とだけ聞いて、`security-audit` スキルを自動で読み込ませてみてください。スキルによってどれくらいの時間が節約できましたか？

3. **チームスキル・チャレンジ**: あなたのチームのコードレビュー・チェックリストを考えてみてください。それをスキルとして体系化できますか？そのスキルが常にチェックすべき3つの項目を書き出してみてください。

**自己チェック**: `description` フィールドがなぜ重要なのか（Copilot がスキルを読み込むかどうかを判断する基準だから！）を説明できれば、スキルを理解したと言えます。

---

## 📝 課題

### メインチャレンジ：書籍サマリスキルの構築

これまでは `pytest-gen` や `pr-review` スキルを作成しました。今度は、データからフォーマットされた出力を生成するという、全く異なる種類のスキルを練習しましょう。

1. 現在のスキルを一覧表示する：Copilot を起動し、`/skills list` を渡します。`ls .github/skills/` でプロジェクトのスキルを、`ls ~/.copilot/skills/` で個人のスキルを確認することもできます。
2. `.github/skills/book-summary/SKILL.md` に、書籍コレクションのフォーマットされた Markdown サマリを生成する `book-summary` スキルを作成してください。
3. スキルには以下の内容を含めてください：
   - 明確な名前と説明（マッチングには説明が不可欠です！）
   - 具体的なフォーマット規則（例：タイトル、著者、年、既読状態の Markdown テーブル）
   - 出力規約（例：既読状態に ✅/❌ を使う、出版年順にソートする）
4. スキルをテストする：`@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list` を確認して、スキルが自動的にトリガーされるか検証する。
6. `/book-summary Summarize the books in this collection` のように直接呼び出してみる。

**成功基準**: 書籍コレクションについて尋ねたときに、Copilot が自動的に適用する動作する `book-summary` スキルが作成されていること。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**テンプレート**: `.github/skills/book-summary/SKILL.md` を作成します：

```markdown
---
name: book-summary
description: 書籍コレクションのフォーマットされた Markdown サマリを生成
---

# 書籍サマリ・ジェネレータ

以下の規則に従って書籍コレクションのサマリを生成してください：

1. 「タイトル、著者、年、状態」の列を持つ Markdown テーブルを出力する
2. 既読の本には ✅、未読の本には ❌ を使用する
3. 出版年順（古い順）にソートする
4. 最後に合計冊数を含める
5. データの問題（著者の欠落、無効な年など）があればフラグを立てる

例：
| タイトル | 著者 | 年 | 状態 |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**合計: 2 冊 (既読 1, 未読 1)**
```

**テスト：**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# 説明が一致すれば、スキルが自動的にトリガーされるはずです
```

**トリガーされない場合：** `/skills reload` を実行してから再度試してください。

</details>

### ボーナスチャレンジ：コミットメッセージ・スキル

1. 一貫した形式でコンベンショナルコミットメッセージを生成する `commit-message` スキルを作成してください。
2. 変更をステージングし、「Generate a commit message for my staged changes」と聞いてテストしてください。
3. 作成したスキルをドキュメント化し、GitHub で `copilot-skill` トピックを付けて共有してみてください。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| ファイル名を `SKILL.md` 以外にする | スキルとして認識されません | 必ず `SKILL.md` という名前にしてください |
| `description` フィールドが曖昧 | スキルが自動的にロードされません | 説明は主要な発見メカニズムです。具体的なトリガーワードを使ってください |
| フロントマターに `name` または `description` がない | スキルの読み込みに失敗します | YAML フロントマターに両方のフィールドを追加してください |
| フォルダの場所が間違っている | スキルが見つかりません | `.github/skills/スキル名/` (プロジェクト) または `~/.copilot/skills/スキル名/` (個人) を使ってください |

### トラブルシューティング

**スキルが使われない** - 期待通りに Copilot がスキルを使ってくれない場合：

1. **説明（description）を確認する**: あなたの問いかけと一致していますか？
   ```markdown
   # 悪い例：曖昧すぎる
   description: Reviews code

   # 良い例：トリガーワードを含んでいる
   description: コードレビュー、コード品質のチェック、バグの発見、
     セキュリティ問題、ベストプラクティス違反の確認に使用します
   ```

2. **ファイルの場所を検証する**:
   ```bash
   # プロジェクトのスキル
   ls .github/skills/

   # 個人のスキル
   ls ~/.copilot/skills/
   ```

3. **SKILL.md の形式を確認する**: フロントマターは必須です：
   ```markdown
   ---
   name: skill-name
   description: スキルが何をするか、いつ使うか
   ---

   # ここに指示を書く
   ```

**スキルが表示されない** - フォルダ構造を確認してください：
```
.github/skills/
└── my-skill/           # フォルダ名
    └── SKILL.md        # 正確に SKILL.md である必要があります（大文字小文字を区別）
```

スキルを作成または編集した後は `/skills reload` を実行して、変更が反映されるようにしてください。

**スキルがロードされるかテストする** - Copilot に直接聞いてみてください：
```bash
> What skills do you have available for checking code quality?
# Copilot は見つけた関連スキルを説明してくれます
```

**自分のスキルが実際に動いているか知るには？**

1. **出力形式を確認する**: スキルで出力形式（`[CRITICAL]` タグなど）を指定している場合、回答にそれがあるか探してください。
2. **直接聞く**: 回答を得た後、「Did you use any skills for that?（今の回答にスキルを使った？）」と聞いてください。
3. **あり・なしを比較する**: `--no-custom-instructions` を付けて同じプロンプトを試し、違いを見てください：
   ```bash
   # スキルあり
   copilot --allow-all -p "Review @file.py for security issues"

   # スキルなし（ベースライン比較）
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **特定のチェック項目を確認する**: スキルに特定のチェック（「50行を超える関数」など）が含まれている場合、それが出力に現れているか確認してください。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **スキルは自動的**: プロンプトがスキルの説明と一致すると、Copilot は自動的に読み込みます。
2. **直接呼び出し**: `/スキル名` というスラッシュコマンドで直接呼び出すこともできます。
3. **SKILL.md の形式**: YAML フロントマター（name, description, オプションで license）と Markdown の指示で構成されます。
4. **場所が重要**: プロジェクト/チーム共有には `.github/skills/`、個人利用には `~/.copilot/skills/` を使います。
5. **説明が鍵**: 自然に質問する際の内容に合わせた説明を書きましょう。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ➡️ 次は？

スキルは、自動ロードされる指示によって Copilot ができることを拡張しました。では、外部サービスに接続したい場合はどうすればいいでしょうか？そこで登場するのが MCP です。

**[第06章：MCP サーバー](../06-mcp-servers/README.ja.md)** では以下を学びます：

- MCP (Model Context Protocol) とは何か
- GitHub、ファイルシステム、ドキュメントサービスへの接続
- MCP サーバーの設定
- 複数サーバーのワークフロー

---

**[← 第04章に戻る](../04-agents-custom-instructions/README.ja.md)** | **[第06章へ進む →](../06-mcp-servers/README.ja.md)**
