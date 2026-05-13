![第 07 章: すべてをまとめる](../../../images/chapter-header.png)

> **学んだすべてがここで融合します。1 つのセッションでアイデアからマージされた PR へ。**

この章では、学んだすべてを完全なワークフローにまとめます。マルチエージェントのコラボレーションを使って機能を構築し、コミット前にセキュリティの問題を検出するプリコミットフックを設定し、Copilot を CI/CD パイプラインに統合し、1 つのターミナルセッションで機能のアイデアからマージされた PR へ進みます。これが GitHub Copilot CLI が真のフォースマルチプライヤーになる場所です。

> 💡 **注意**: この章では学んだすべてを組み合わせる方法を示します。**エージェント、スキル、MCP がなくても生産的になれます（非常に便利ですが）。** コアワークフロー — 説明、計画、実装、テスト、レビュー、リリース — は第 00〜03 章の組み込み機能だけで機能します。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- エージェント、スキル、MCP（Model Context Protocol）を統合ワークフローで組み合わせる
- マルチツールアプローチを使って完全な機能を構築する
- フックで基本的な自動化を設定する
- プロフェッショナルな開発のベストプラクティスを適用する

> ⏱️ **目安時間**: 約 75 分（15 分読む + 60 分ハンズオン）

---

## 🧩 現実世界のたとえ話: オーケストラ

<img src="../../../images/orchestra-analogy.png" alt="オーケストラのたとえ話 - 統合ワークフロー" width="800"/>

交響楽団には多くのセクションがあります:
- **弦楽器**が基礎を提供する（コアワークフローのように）
- **金管楽器**が力を加える（特化した専門知識を持つエージェントのように）
- **木管楽器**が色を加える（機能を拡張するスキルのように）
- **打楽器**がリズムを刻む（外部システムに接続する MCP のように）

個々では各セクションの音は限られています。一緒に、うまく指揮されると、素晴らしいものが生まれます。

**この章が教えることがそれです！**<br>
*指揮者がオーケストラを指揮するように、エージェント、スキル、MCP を統合ワークフローに指揮する*

コードを変更し、テストを生成し、レビューし、PR を作成するシナリオを 1 つのセッションでウォークスルーすることから始めましょう。

---

## 1 つのセッションでアイデアからマージされた PR へ

エディター、ターミナル、テストランナー、GitHub UI の間を切り替えてコンテキストを失うのではなく、1 つのターミナルセッションですべてのツールを組み合わせることができます。このパターンは以下の[統合パターン](#the-integration-pattern-for-power-users)セクションで詳しく説明します。

```bash
# インタラクティブモードで Copilot を起動する
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot が高レベルの計画を作成する...

# PYTHON-REVIEWER エージェントに切り替える
> /agent
# "python-reviewer" を選択する

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# python-reviewer エージェントが生成するもの:
# - メソッドシグネチャと戻り型
# - リスト内包表記を使ったフィルター実装
# - 空のコレクションのエッジケース処理

# PYTEST-HELPER エージェントに切り替える
> /agent
# "pytest-helper" を選択する

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# pytest-helper エージェントが生成するもの:
# - 空のコレクションのテストケース
# - 読了/未読の本が混在するテストケース
# - すべての本が読了済みのテストケース

# 実装する
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# テストする
> Generate comprehensive tests for the new feature

# 以下のようなテストが複数生成される:
# - ハッピーパス（3 テスト）— 正しくフィルタリング、読了済みを除外、未読を含む
# - エッジケース（4 テスト）— 空のコレクション、すべて読了、未読なし、1 冊
# - パラメータ化（5 ケース）— @pytest.mark.parametrize で読了/未読の比率を変える
# - 統合（4 テスト）— mark_as_read、remove_book、add_book、データ整合性との連携

# 変更をレビューする
> /review

# レビューが通ったら /pr を使って現在のブランチのプルリクエストを操作する
> /pr [view|create|fix|auto]

# または Copilot にターミナルから下書きを作成させたい場合は自然に聞く
> Create a pull request titled "Feature: Add list unread books command"
```

**従来のアプローチ**: エディター、ターミナル、テストランナー、ドキュメント、GitHub UI の間を切り替える。切り替えのたびにコンテキストの喪失と摩擦が生じる。

**重要なポイント**: あなたがアーキテクトとして専門家を指示した。彼らが詳細を処理し、あなたがビジョンを処理した。

> 💡 **さらに進めて**: このような大規模なマルチステップの計画では、`/fleet` を試して Copilot が独立したサブタスクを並行して実行できるようにしましょう。詳細は[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)を参照してください。

---

# 追加ワークフロー

<img src="../../../images/combined-workflows.png" alt="エージェント、スキル、MCP が統合ワークフローにどのように組み合わさるかを表すカラフルな巨大ジグソーパズルのピースとギアを組み立てる人々" width="800"/>

第 04〜06 章を完了したパワーユーザー向けに、これらのワークフローはエージェント、スキル、MCP が効果をどのように乗数倍するかを示します。

## 統合パターン

すべてを組み合わせるためのメンタルモデルです。

<img src="../../../images/integration-pattern.png" alt="統合パターン - 4 フェーズのワークフロー: コンテキストの収集（MCP）、分析と計画（エージェント）、実行（スキル + 手動）、完了（MCP）" width="800"/>

---

## ワークフロー 1: バグ調査と修正

完全なツール統合による実際のバグ修正:

```bash
copilot

# フェーズ 1: GitHub からバグを理解する（MCP がこれを提供する）
> Get the details of issue #1

# 学ぶ: "find_by_author は部分的な名前では機能しない"

# フェーズ 2: ベストプラクティスを調査する（Web と GitHub ソースで深く調査する）
> /research Best practices for Python case-insensitive string matching

# フェーズ 3: 関連するコードを見つける
> @samples/book-app-project/books.py Show me the find_by_author method

# フェーズ 4: 専門家の分析を取得する
> /agent
# "python-reviewer" を選択する

> Analyze this method for issues with partial name matching

# エージェントが特定する: メソッドが部分文字列マッチではなく完全一致を使っている

# フェーズ 5: エージェントのガイダンスで修正する
> Implement the fix using lowercase comparison and 'in' operator

# フェーズ 6: テストを生成する
> /agent
# "pytest-helper" を選択する

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# フェーズ 7: コミットして PR を作成する
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## ワークフロー 2: コードレビューの自動化（オプション）

> 💡 **このセクションはオプションです。** プリコミットフックはチームに便利ですが、生産性向上のために必須ではありません。始めたばかりであればスキップしてください。
>
> ⚠️ **パフォーマンスに関する注意**: このフックは各ステージされたファイルに対して `copilot -p` を呼び出し、ファイルごとに数秒かかります。大きなコミットでは、重要なファイルに制限するか、代わりに `/review` で手動でレビューを実行することを検討してください。

**git フック**は Git が特定の時点（例えばコミット直前）に自動的に実行するスクリプトです。これを使ってコードの自動チェックを実行できます。コミットで自動的な Copilot レビューを設定する方法です。

```bash
# プリコミットフックを作成する
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# ステージされたファイルを取得する（Python ファイルのみ）
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # タイムアウトを使ってハングを防ぐ（ファイルごとに 60 秒）
    # --allow-all はファイルの読み書きを自動承認するのでフックが無人で実行できる。
    # これは自動化されたスクリプトでのみ使用する。インタラクティブなセッションでは Copilot に許可を求めさせる。
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # タイムアウトが発生したか確認する
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

> ⚠️ **macOS ユーザーへ**: `timeout` コマンドは macOS にデフォルトで含まれていません。`brew install coreutils` でインストールするか、タイムアウトガードなしのシンプルな呼び出しに `timeout 60` を置き換えてください。

> 📚 **公式ドキュメント**: [フックを使う](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks)と[フック設定リファレンス](https://docs.github.com/copilot/reference/hooks-configuration) - 完全なフック API。
>
> 💡 **組み込みの代替手段**: Copilot CLI にはプリコミットなどのイベントで自動的に実行できる組み込みフックシステム（`copilot hooks`）もあります。上記の手動 git フックは完全な制御を提供し、組み込みシステムは設定が簡単です。どちらのアプローチがワークフローに合うかは上記のドキュメントを参照してください。

これですべてのコミットがクイックなセキュリティレビューを受けます。

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# 出力:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## ワークフロー 3: 新しいコードベースへのオンボーディング

新しいプロジェクトに参加するとき、コンテキスト、エージェント、MCP を組み合わせてすばやく立ち上がります。

```bash
# インタラクティブモードで Copilot を起動する
copilot

# フェーズ 1: コンテキストで全体像を把握する
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# フェーズ 2: 特定のフローを理解する
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# フェーズ 3: エージェントで専門家の分析を取得する
> /agent
# "python-reviewer" を選択する

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# フェーズ 4: 作業するものを見つける（MCP が GitHub アクセスを提供する）
> List open issues labeled "good first issue"

# フェーズ 5: コントリビューションを始める
> Pick the simplest open issue and outline a plan to fix it
```

このワークフローは `@` コンテキスト、エージェント、MCP を 1 つのオンボーディングセッションに組み合わせます。この章の前半の統合パターンそのものです。

---

# ベストプラクティスと自動化

ワークフローをより効果的にするパターンと習慣です。

---

## ベストプラクティス

### 1. 分析の前にコンテキストを収集する

分析を求める前に常にコンテキストを収集します。

```bash
# 良い例
> Get the details of issue #42
> /agent
# python-reviewer を選択する
> Analyze this issue

# 効果の低い例
> /agent
# python-reviewer を選択する
> Fix login bug
# エージェントがイシューのコンテキストを持っていない
```

### 2. エージェント、スキル、カスタム指示の違いを知る

各ツールには得意な領域があります。

```bash
# エージェント: 明示的に有効化する特化したペルソナ
> /agent
# python-reviewer を選択する
> Review this authentication code for security issues

# スキル: プロンプトがスキルの説明と一致するときに自動的に有効化されるモジュラー機能
# （使用するには事前に作成する必要がある — 第 05 章を参照）
> Generate comprehensive tests for this code
# テストスキルが設定されていれば自動的に有効化される

# カスタム指示（.github/copilot-instructions.md）: 切り替えやトリガーなしで
# すべてのセッションに適用される常時オンのガイダンス
```

> 💡 **重要なポイント**: エージェントもスキルもコードの分析と生成の両方ができます。本当の違いは**有効化の方法** — エージェントは明示的（`/agent`）、スキルは自動（プロンプトマッチ）、カスタム指示は常時オン。

### 3. セッションを集中させる

セッションにラベルを付けるために `/rename` を使い（履歴で簡単に見つけられる）、クリーンに終了するために `/exit` を使います。

```bash
# 良い例: セッションごとに 1 つの機能
> /rename list-unread-feature
# 未読リストの作業をする
> /exit

copilot
> /rename export-csv-feature
# CSV エクスポートの作業をする
> /exit

# 効果の低い例: すべてを 1 つの長いセッションで
```

### 4. Copilot でワークフローを再利用可能にする

ワークフローを Wiki に文書化するだけでなく、Copilot が使えるリポジトリに直接エンコードします。

- **カスタム指示**（`.github/copilot-instructions.md`）: コーディング標準、アーキテクチャルール、ビルド/テスト/デプロイのステップのための常時オンガイダンス。すべてのセッションが自動的に従う。
- **プロンプトファイル**（`.github/prompts/`）: チームが共有できる再利用可能でパラメータ化されたプロンプト — コードレビュー、コンポーネント生成、PR の説明のテンプレートのようなもの。
- **カスタムエージェント**（`.github/agents/`）: チームの誰もが `/agent` で有効化できる特化したペルソナ（例: セキュリティレビュアーやドキュメントライター）をエンコードする。
- **カスタムスキル**（`.github/skills/`）: 関連するときに自動有効化されるステップバイステップのワークフロー指示をパッケージ化する。

> 💡 **成果**: 新しいチームメンバーがワークフローを無料で得られます — リポジトリに組み込まれており、誰かの頭の中にロックされていません。

---

## ボーナス: プロダクションパターン

これらはオプションですが、プロフェッショナルな環境で価値があります。

### PR 説明ジェネレーター

```bash
# 包括的な PR の説明を生成する
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD 統合

既存の CI/CD パイプラインを持つチームは、GitHub Actions を使ってすべてのプルリクエストで Copilot レビューを自動化できます。これにはレビューコメントの自動投稿と重要な問題のフィルタリングが含まれます。

> 📖 **詳細**: 完全な GitHub Actions ワークフロー、設定オプション、トラブルシューティングのヒントは [CI/CD 統合](../appendices/ci-cd-integration.md)を参照してください。

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

完全なワークフローを実践しましょう。

---

## ▶️ 自分で試してみよう

デモを完了した後、これらのバリエーションを試してみましょう。

1. **エンドツーエンドチャレンジ**: 小さな機能を選んでください（例:「未読の本をリストアップ」または「CSV にエクスポート」）。完全なワークフローを使います:
   - `/plan` で計画する
   - エージェントで設計する（python-reviewer、pytest-helper）
   - 実装する
   - テストを生成する
   - PR を作成する

2. **自動化チャレンジ**: コードレビューの自動化ワークフローのプリコミットフックを設定します。意図的なファイルパスの脆弱性でコミットを作成します。ブロックされますか？

3. **自分のプロダクションワークフロー**: よく行う一般的なタスクの独自のワークフローを設計します。チェックリストとして書き留めます。どの部分をスキル、エージェント、フックで自動化できますか？

**自己確認**: エージェント、スキル、MCP がどのように連携するか、そしてそれぞれをいつ使うかを同僚に説明できれば、コースを完了しています。

---

## 📝 課題

### メインチャレンジ: エンドツーエンドの機能

ハンズオン例では「未読の本をリストアップ」機能の構築をウォークスルーしました。今度は別の機能の完全なワークフローを練習しましょう: **年の範囲で本を検索する**:

1. Copilot を起動してコンテキストを収集する: `@samples/book-app-project/books.py`
2. `/plan Add a "search by year" command that lets users find books published between two years` で計画する
3. `BookCollection` に `find_by_year_range(start_year, end_year)` メソッドを実装する
4. `book_app.py` にユーザーに開始年と終了年を入力させる `handle_search_year()` 関数を追加する
5. テストを生成する: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review` でレビューする
7. README を更新する: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. コミットメッセージを生成する

作業しながらワークフローを文書化します。

**成功基準**: 計画、実装、テスト、ドキュメント、レビューを含む Copilot CLI を使ってアイデアからコミットまでの機能を完成させました。

> 💡 **ボーナス**: 第 04 章でエージェントを設定した場合は、カスタムエージェントを作成して使ってみましょう。例えば、実装レビューのための error-handler エージェントと README 更新のための doc-writer エージェント。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**この章の上部にある[「アイデアからマージされた PR へ」](#idea-to-merged-pr-in-one-session)の例のパターンに従ってください。** 主なステップは以下です:

1. `@samples/book-app-project/books.py` でコンテキストを収集する
2. `/plan Add a "search by year" command` で計画する
3. メソッドとコマンドハンドラーを実装する
4. エッジケース（無効な入力、空の結果、逆範囲）でテストを生成する
5. `/review` でレビューする
6. `@samples/book-app-project/README.md` で README を更新する
7. `-p` でコミットメッセージを生成する

**考えるべきエッジケース:**
- ユーザーが「2000」と「1990」（逆の範囲）を入力したら？
- 範囲に一致する本がなかったら？
- ユーザーが数値以外の入力をしたら？

**重要なのは完全なワークフローを練習すること** — アイデア → コンテキスト → 計画 → 実装 → テスト → ドキュメント → コミット。

</details>

---

<details>
<summary>🔧 <strong>よくある間違い</strong>（クリックして展開）</summary>

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| 実装にすぐ飛びつく | 後で修正コストの高い設計上の問題を見逃す | まず `/plan` を使ってアプローチを考える |
| 1 つのツールだけ使う | 遅く、徹底性に欠ける | 組み合わせる: 分析にエージェント → 実行にスキル → 統合に MCP |
| コミット前にレビューしない | セキュリティの問題やバグが見過ごされる | 常に `/review` を実行するか[プリコミットフック](#workflow-2-code-review-automation-optional)を使う |
| ワークフローをチームと共有しない | 各人がゼロから発明する | 共有エージェント、スキル、指示にパターンを文書化する |

</details>

---

# まとめ

## 🔑 重要なポイント

1. **統合 > 孤立**: 最大の効果のためにツールを組み合わせる
2. **コンテキストが先**: 分析の前に必要なコンテキストを常に収集する
3. **エージェントが分析し、スキルが実行する**: 適切なジョブに適切なツールを使う
4. **繰り返しを自動化する**: フックとスクリプトが効果を乗数倍する
5. **ワークフローを文書化する**: 共有可能なパターンがチーム全体に恩恵をもたらす

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## 🎓 コース完了！

おめでとうございます！以下を学びました。

| 章 | 学んだこと |
|---------|-------------------|
| 00 | Copilot CLI のインストールとクイックスタート |
| 01 | 3 つのインタラクションモード |
| 02 | @ 構文によるコンテキスト管理 |
| 03 | 開発ワークフロー |
| 04 | 特化したエージェント |
| 05 | 拡張可能なスキル |
| 06 | MCP による外部接続 |
| 07 | 統合プロダクションワークフロー |

これで GitHub Copilot CLI を開発ワークフローの真のフォースマルチプライヤーとして使う準備が整いました。

## ➡️ 次のステップ

学習はここで止まりません:

1. **毎日練習する**: 実際の作業に Copilot CLI を使う
2. **カスタムツールを構築する**: 特定のニーズに合わせたエージェントとスキルを作成する
3. **知識を共有する**: チームがこれらのワークフローを採用するのを助ける
4. **最新情報を追う**: 新機能のために GitHub Copilot の更新情報をフォローする

### リソース

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP サーバーレジストリ](https://github.com/modelcontextprotocol/servers)
- [コミュニティスキル](https://github.com/topics/copilot-skill)

---

**素晴らしい仕事をしました！今度は素晴らしいものを作りましょう。**

**[← 第 06 章に戻る](../06-mcp-servers/README.md)** | **[コースホームに戻る →](../README.md)**
