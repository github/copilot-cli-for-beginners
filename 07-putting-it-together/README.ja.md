<!--
---
id: CopilotCLI-07
title: すべてを組み合わせる
description: コンテキスト、ワークフロー、エージェント、スキル、MCP を組み合わせて、アイデアからプルリクエスト作成までの完全な機能開発ワークフローを構築します。
audience: Developers / Students / Terminal users
slug: putting-it-all-together
weight: 8
---
-->

![Chapter 07: Putting It All Together](assets/chapter-header.png)

> **学んだことすべてがここに結実します。アイデア出しから PR マージまでを一つのセッションで完結させましょう。**

この章では、これまで学んだすべての知識を統合して、完全なワークフローを構築します。複数のエージェントによる共同作業での機能開発、コミット前のセキュリティチェックを行うプリコミットフックの作成、CI/CD パイプラインへの Copilot の統合、そして機能のアイデアから PR マージまでをターミナルの一つのセッションだけで進める方法を学びます。ここで GitHub Copilot CLI は、真の「生産性の倍増器」となります。

> 💡 **補足**: この章では学んだすべての組み合わせ方を紹介しますが、**生産的であるために必ずしもエージェント、スキル、MCP すべてを使う必要はありません。** コアとなるワークフロー（説明、計画、実装、テスト、レビュー、シップ）は、第00〜03章で学んだ組み込み機能だけでも十分に機能します。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- エージェント、スキル、MCP (Model Context Protocol) を統合ワークフローで組み合わせる
- 複数のツールを駆使して完全な機能を構築する
- フック（hooks）を使用した基本的な自動化をセットアップする
- プロフェッショナルな開発のためのベストプラクティスを適用する

> ⏱️ **推定所要時間**: 約75分（読みもの15分 ＋ 実践60分）

---

## 🧩 現実世界の例え：オーケストラ

<img src="assets/orchestra-analogy.png" alt="オーケストラに例えると - 統合ワークフロー" width="800"/>

交響楽団には多くのセクションがあります：
- **弦楽器**は土台を提供します（コアワークフローのように）
- **金管楽器**は力強さを加えます（専門知識を持つエージェントのように）
- **木管楽器**は彩りを添えます（能力を拡張するスキルのように）
- **打楽器**はリズムを刻みます（外部システムと繋ぐ MCP のように）

個々のセクションだけでは限界がありますが、指揮者のもとで一つになれば、壮大な芸術が生まれます。

**これこそが、この章で学ぶことです！**<br>
*オーケストラの指揮者のように、エージェント、スキル、MCP を指揮して統合ワークフローを作り上げましょう。*

まずは、コードの修正からテスト生成、レビュー、PR 作成までを一つのセッションで行うシナリオを見ていきましょう。

---

## アイデアから PR マージまでを一回のセッションで

エディタ、ターミナル、テストランナー、GitHub UI を行ったり来たりしてそのたびに文脈（コンテキスト）を失う代わりに、すべてのツールを一つのターミナルセッションに集約できます。このパターンを、後の [統合パターン](#パワーユーザーのための統合パターン) セクションで詳しく解説します。

```bash
# 対話モードで Copilot を起動
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?
（書籍アプリに、既読が False の本だけを表示する "list unread" コマンドを追加したい。どのファイルを変更すればいい？）

# Copilot がハイレベルな計画を作成……

# PYTHON-REVIEWER エージェントに切り替え
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# python-reviewer エージェントが以下を提案：
# - メソッドのシグネチャと戻り値の型
# - リスト内包表記を使ったフィルタリングの実装
# - コレクションが空の場合のエッジケース処理

# PYTEST-HELPER エージェントに切り替え
> /agent
# "pytest-helper" を選択

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# pytest-helper エージェントが以下を提案：
# - 空のコレクションでのテストケース
# - 既読・未読が混在する場合のテストケース
# - すべての本が既読の場合のテストケース

# 実装 (IMPLEMENT)
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# テスト (TEST)
> Generate comprehensive tests for the new feature

# 以下のような複数のテストが生成されます：
# - 正常系 (3テスト) — 正しくフィルタリングされるか、既読を除外し未読を含むか
# - エッジケース (4テスト) — 空のコレクション、すべて既読、未読なし、1冊のみ
# - パラメータ化テスト (5ケース) — @pytest.mark.parametrize による様々な既読比率の検証
# - 結合テスト (4テスト) — mark_as_read, remove_book, add_book との相互作用および整合性

# 変更内容をレビュー
> /review

# レビューを通過したら、/pr を使って現在のブランチのプルリクエストを操作
> /pr [view|create|fix|auto]

# あるいは自然な言葉で、ターミナルから PR を下書きさせる
> Create a pull request titled "Feature: Add list unread books command"
```

**従来のやり方**: エディタ、ターミナル、テストランナー、ドキュメント、GitHub UI を切り替える。切り替えのたびにコンテキストが失われ、摩擦が生じる。

**重要な洞察**: あなたは建築家（アーキテクト）のように専門家に指示を出しました。彼らが詳細を詰め、あなたはビジョンを担当しました。

> 💡 **さらに先へ**: このような大規模な複数ステップの計画には、`/fleet` を使って独立したサブタスクを並列実行させることも検討してください。詳細は [公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)（英語）を参照してください。

---

# 追加のワークフロー

<img src="assets/combined-workflows.png" alt="歯車が付いた巨大なカラフルなジグソーパズルを組み立てる人々。エージェント、スキル、MCPが統合ワークフローとして組み合わさる様子を表現している" width="800"/>

第04〜06章を完了したパワーユーザー向けに、エージェント、スキル、MCP が生産性をいかに倍増させるかを示すワークフローを紹介します。

## 統合パターン

すべてを組み合わせるためのメンタルモデルは以下の通りです：

<img src="assets/integration-pattern.png" alt="統合パターン - 4つのフェーズ：コンテキスト収集 (MCP)、分析と計画 (エージェント)、実行 (スキル + 手動)、完了 (MCP)" width="800"/>

---

## ワークフロー 1：バグの調査と修正

すべてのツールを統合した、現実的なバグ修正の流れ：

```bash
copilot

# フェーズ 1：GitHub からバグの内容を把握 (MCP を使用)
> Get the details of issue #1

# 把握：「find_by_author が部分一致で動作しない」

# フェーズ 2：ベストプラクティスを調査 (ウェブと GitHub ソースでの詳細調査)
> /research Best practices for Python case-insensitive string matching

# フェーズ 3：関連コードを見つける
> @samples/book-app-project/books.py Show me the find_by_author method

# フェーズ 4：専門家による分析を受ける
> /agent
# "python-reviewer" を選択

> Analyze this method for issues with partial name matching

# エージェントが特定：部分一致ではなく完全一致 (==) が使われている

# フェーズ 5：エージェントのガイドに従って修正
> Implement the fix using lowercase comparison and 'in' operator

# フェーズ 6：テストを生成
> /agent
# "pytest-helper" を選択

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# フェーズ 7：コミットと PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## ワークフロー 2：コードレビューの自動化（オプション）

> 💡 **このセクションはオプションです。** プリコミットフックはチーム開発に有用ですが、必須ではありません。始めたばかりの方はスキップして構いません。
>
> ⚠️ **パフォーマンスに関する注意**: このフックはステージングされたファイルごとに `copilot -p` を呼び出すため、ファイルあたり数秒かかります。大量のコミットを行う場合は、重要なファイルに限定するか、代わりに `/review` を手動で実行することを検討してください。

**Git フック（hook）** とは、Git が特定のポイント（例：コミットの直前）で自動的に実行するスクリプトです。これを使って、コードの自動チェックを実行できます。コミット時に自動で Copilot レビューを走らせる設定方法は以下の通りです：

```bash
# プリコミットフックを作成
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# ステージングされたファイルを取得（Pythonファイルのみ）
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # ハングアップを防ぐためにタイムアウトを設定（1ファイルあたり60秒）
    # --allow-all はファイル読み書きを自動承認し、フックが無人実行できるようにします。
    # 自動化スクリプトでのみ使用してください。対話型セッションでは Copilot に許可を求めさせてください。
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # タイムアウトが発生したかチェック
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS ユーザーの方へ**: macOS にはデフォルトで `timeout` コマンドが含まれていません。`brew install coreutils` でインストールするか、タイムアウト保護なしの単純な呼び出しに書き換えてください。

> 📚 **公式ドキュメント**: フックの完全な API については、[Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) および [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration)（英語）を参照してください。
>
> 💡 **組み込みの代替案**: Copilot CLI には、プリコミットなどのイベントで自動実行できる組み込みのフックシステム (`copilot hooks`) もあります。上記の手動 Git フックは完全な制御が可能ですが、組み込みシステムの方が設定は簡単です。ご自身のワークフローに合う方を選んでください。

これで、すべてのコミットでクイックセキュリティレビューが行われるようになります：

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# 出力例:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# 問題を修正して再試行してください。
```

---

## ワークフロー 3：新しいコードベースへのオンボーディング

新しいプロジェクトに参加した際、コンテキスト、エージェント、MCP を組み合わせて素早く立ち上がりましょう：

```bash
# 対話モードで Copilot を起動
copilot

# フェーズ 1：コンテキストを使って全体像を把握
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# フェーズ 2：特定のフローを理解
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# フェーズ 3：エージェントを使って専門的な分析を得る
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# フェーズ 4：着手すべきタスクを探す (MCP で GitHub にアクセス)
> List open issues labeled "good first issue"

# フェーズ 5：貢献を始める
> Pick the simplest open issue and outline a plan to fix it
```

このワークフローは、`@` コンテキスト、エージェント、MCP を一つのオンボーディングセッションに統合しており、まさにこの章の前半で紹介した統合パターンそのものです。

---

# ベストプラクティスと自動化

ワークフローをより効果的にするためのパターンと習慣を紹介します。

---

## ベストプラクティス

### 1. 分析の前にまずコンテキストを

分析を依頼する前に、必ず必要なコンテキストを収集してください：

```bash
# 良い例
> Get the details of issue #42
> /agent
# python-reviewer を選択
> Analyze this issue

# あまり効果的でない例
> /agent
# python-reviewer を選択
> Fix login bug
# エージェントが Issue のコンテキストを持っていません
```

### 2. エージェント、スキル、カスタム指示の違いを知る

各ツールにはそれぞれの得意分野があります：

```bash
# エージェント：明示的に有効化する特化型ペルソナ
> /agent
# python-reviewer を選択
> Review this authentication code for security issues

# スキル：プロンプトが説明と一致したときに自動で有効化されるモジュール機能
# (第05章に従って、あらかじめ作成しておく必要があります)
> Generate comprehensive tests for this code
# テスト用スキルが設定されていれば、自動的に有効になります

# カスタム指示 (.github/copilot-instructions.md)：
# 切り替えやトリガーなしで、すべてのセッションに適用される常時オンのガイド
```

> 💡 **重要なポイント**: エージェントもスキルも、コードの分析と生成の両方が可能です。本当の違いは **「どのように有効になるか」** です。エージェントは明示的 (`/agent`)、スキルは自動的（プロンプト一致）、カスタム指示は常時オンです。

### 3. セッションの焦点を絞る

`/rename` を使ってセッションにラベルを付け（履歴で見つけやすくなります）、`/exit` で綺麗に終了しましょう：

```bash
# 良い例：一つの機能につき一つのセッション
> /rename list-unread-feature
# list unread 機能に取り組む
> /exit

copilot
> /rename export-csv-feature
# CSV エクスポート機能に取り組む
> /exit

# あまり良くない例：一つの長いセッションですべてを行う
```

### 4. ワークフローを Copilot で再利用可能にする

ワークフローを単に Wiki にドキュメント化するだけでなく、リポジトリに直接組み込んで Copilot が使えるようにしましょう：

- **カスタム指示** (`.github/copilot-instructions.md`): コーディング標準、アーキテクチャ規則、ビルド/テスト/デプロイ手順などの常時オンのガイド。すべてのセッションで自動的に遵守されます。
- **プロンプトファイル** (`.github/prompts/`): コードレビュー、コンポーネント生成、PR の説明文などのテンプレートとしてチームで共有できる、パラメータ化された再利用可能なプロンプト。
- **カスタムエージェント** (`.github/agents/`): セキュリティレビュアーやドキュメントライターなど、チームの誰もが `/agent` で呼び出せる専門ペルソナを定義します。
- **カスタムスキル** (`.github/skills/`): 関連する場面で自動トリガーされる、ステップバイステップのワークフロー指示をパッケージ化します。

> 💡 **得られるメリット**: 新しいチームメンバーは、ワークフローを最初から「無料」で手に入れることができます。誰かの頭の中ではなく、リポジトリに組み込まれているからです。

---

## おまけ：プロダクションパターン

これらはオプションですが、プロフェッショナルな環境では価値の高いパターンです。

### PR 説明文ジェネレータ

```bash
# 包括的な PR 説明文を生成
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD 連携

既存の CI/CD パイプラインがあるチームでは、GitHub Actions を使ってすべてのプルリクエストに対して Copilot レビューを自動化できます。これには、レビューコメントの自動投稿や致命的な問題のフィルタリングが含まれます。

> 📖 **さらに詳しく**: 完全な GitHub Actions ワークフロー、設定オプション、およびトラブルシューティングのヒントについては、[CI/CD 連携](../appendices/ci-cd-integration.md)（英語）を参照してください。

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

統合ワークフローを実際に試してみましょう。

---

## ▶️ 自分で試してみる

デモを終えたら、以下のバリエーションに挑戦してみてください：

1. **エンドツーエンド・チャレンジ**: 小さな機能（例：「未読本のリスト表示」や「CSV エクスポート」）を選び、フルワークフローで進めてください：
   - `/plan` で計画を立てる
   - エージェント（python-reviewer, pytest-helper）で設計する
   - 実装する
   - テストを生成する
   - PR を作成する

2. **自動化チャレンジ**: 「コードレビューの自動化」ワークフローに従ってプリコミットフックをセットアップしてください。わざとファイルパスの脆弱性を含んだコミットをしようとしてみてください。ブロックされますか？

3. **あなた自身のプロダクションワークフロー**: あなたが普段行う一般的なタスクのためのワークフローを設計してください。それをチェックリストとして書き出してみましょう。どの部分をスキル、エージェント、あるいはフックで自動化できそうですか？

**自己チェック**: エージェント、スキル、MCP がどのように連携するか、そしてそれぞれをいつ使うべきかを同僚に説明できれば、このコースを修了したと言えます。

---

## 📝 課題

### メインチャレンジ：エンドツーエンドの機能開発

ハンズオンの例では「未読本のリスト表示」機能を作りました。今度は別の機能、**「出版年の範囲による本の検索」**でフルワークフローを練習しましょう：

1. Copilot を起動し、コンテキストを収集する：`@samples/book-app-project/books.py`
2. 計画を立てる：`/plan Add a "search by year" command that lets users find books published between two years`
3. `BookCollection` に `find_by_year_range(start_year, end_year)` メソッドを実装する
4. `book_app.py` に、ユーザーに開始年と終了年を促す `handle_search_year()` 関数を追加する
5. テストを生成する：`@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review` でレビューを行う
7. README を更新する：`@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. コミットメッセージを生成する

作業を進めながら、自分のワークフローを記録してください。

**成功基準**: 計画、実装、テスト、ドキュメント作成、レビューを含め、アイデアからコミットまでを Copilot CLI を使って完結させていること。

> 💡 **おまけ**: 第04章でエージェントをセットアップ済みなら、カスタムエージェントを作成して使ってみてください。例えば、実装レビュー用の error-handler エージェントや、README 更新用の doc-writer エージェントなどです。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**この章の冒頭にある [「アイデアから PR マージまで」](#アイデアから-pr-マージまでを一回のセッションで) の例のパターンに従ってください。** 主要なステップは以下の通りです：

1. `@samples/book-app-project/books.py` でコンテキストを収集
2. `/plan Add a "search by year" command` で計画を立てる
3. メソッドとコマンドハンドラーを実装
4. エッジケース（無効な入力、結果なし、範囲の逆転）を含めたテストを生成
5. `/review` でレビュー
6. `@samples/book-app-project/README.md` で README を更新
7. `-p` でコミットメッセージを生成

**考慮すべきエッジケース：**
- ユーザーが "2000" と "1990" を入力した場合は？（範囲の逆転）
- 範囲に一致する本が一冊もない場合は？
- 数値以外の入力がされた場合は？

**鍵となるのは、アイデア → コンテキスト → 計画 → 実装 → テスト → ドキュメント → コミットというフルワークフローを練習することです。**

</details>

---

<details>
<summary>🔧 <strong>よくある間違い</strong> (クリックして展開)</summary>

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| すぐに実装に取り掛かってしまう | 設計上の問題を見逃し、後で修正コストが高くなります | まず `/plan` を使ってアプローチをよく考えましょう |
| 一つのツールだけで済ませようとする | 結果が出るのが遅くなり、網羅性も下がります | 組み合わせましょう：エージェントで分析 → スキルで実行 → MCP で統合 |
| コミット前にレビューを忘れる | セキュリティ問題やバグが紛れ込みます | 常に `/review` を実行するか、[プリコミットフック](#ワークフロー-2：コードレビューの自動化オプション) を使いましょう |
| ワークフローをチームと共有しない | 各自がバラバラに同じ苦労をすることになります | 共有のエージェント、スキル、指示としてパターンをドキュメント化しましょう |

</details>

---

# まとめ

## 🔑 重要なポイント

1. **統合は分離に勝る**: 最大の効果を得るためにツールを組み合わせましょう
2. **コンテキストが先**: 分析を依頼する前に、必ず必要な背景情報を揃えましょう
3. **エージェントが分析し、スキルが実行する**: 役割に合わせて適切なツールを選びましょう
4. **反復作業を自動化する**: フックやスクリプトが生産性を何倍にも高めます
5. **ワークフローをドキュメント化する**: 共有可能なパターンはチーム全体の利益になります

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## 🎓 コース修了！

おめでとうございます！以下の内容をすべて習得しました：

| 章 | 学習内容 |
|---------|-------------------|
| 00 | Copilot CLI のインストールとクイックスタート |
| 01 | 3つのインタラクションモード |
| 02 | @ 構文によるコンテキスト管理 |
| 03 | 開発ワークフロー |
| 04 | 特化型エージェント |
| 05 | 拡張可能なスキル |
| 06 | MCP による外部接続 |
| 07 | 統合されたプロダクション・ワークフロー |

これであなたは、開発ワークフローにおいて GitHub Copilot CLI を真の生産性倍増器として使いこなす準備が整いました。

## ➡️ 次は？

学習に終わりはありません：

1. **毎日実践する**: 実際の仕事で Copilot CLI を使ってみましょう
2. **独自のツールを作る**: あなたのニーズに合わせたエージェントやスキルを作成しましょう
3. **知識を共有する**: チームがこれらのワークフローを導入するのを手助けしましょう
4. **最新情報を追う**: 新機能については GitHub Copilot のアップデートを確認しましょう

### リソース

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP サーバーレジストリ](https://github.com/modelcontextprotocol/servers)
- [コミュニティ製スキル](https://github.com/topics/copilot-skill)

---

**素晴らしい成果です！さあ、素晴らしいものを作り上げましょう。**

**[← 第06章に戻る](../06-mcp-servers/README.ja.md)** | **[コースのホームに戻る →](../README.ja.md)**
