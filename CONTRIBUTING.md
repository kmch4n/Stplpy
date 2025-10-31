# Contributing to Stplpy

Stplpyへの貢献に興味を持っていただきありがとうございます！このドキュメントでは、プロジェクトへの貢献方法について説明します。

## 開発環境のセットアップ

### 必要な環境

- Python 3.12以上
- Git

### セットアップ手順

1. リポジトリをフォーク・クローン

```bash
git clone https://github.com/yourusername/Stplpy.git
cd Stplpy
```

2. 仮想環境を作成

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. 開発用依存関係をインストール

```bash
pip install -e ".[dev]"
```

## 開発ワークフロー

### 1. ブランチの作成

新機能やバグ修正のために、新しいブランチを作成します：

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. コードの変更

- コードを変更する前に、既存のコードスタイルを確認してください
- 型ヒントを必ず追加してください
- docstringを追加して、関数やクラスの動作を文書化してください

### 3. コードスタイル

このプロジェクトでは以下のツールを使用しています：

#### Black (コードフォーマッター)

```bash
black stplpy tests
```

#### Flake8 (リンター)

```bash
flake8 stplpy tests
```

#### Mypy (型チェック)

```bash
mypy stplpy
```

### 4. テストの実行

変更後、必ずテストを実行してください：

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付きで実行
pytest --cov=stplpy --cov-report=html

# 特定のテストファイルを実行
pytest tests/test_user.py
```

### 5. 新しいテストの追加

新機能を追加する場合は、必ずテストも追加してください：

- `tests/`ディレクトリに対応するテストファイルを作成
- 各関数に対して少なくとも1つのテストを作成
- エッジケースやエラーケースもテスト

例：

```python
def test_new_feature():
    """Test description."""
    # Arrange
    expected = "expected result"

    # Act
    result = your_function()

    # Assert
    assert result == expected
```

## コミットメッセージ

コミットメッセージは以下の形式に従ってください：

```
[絵文字] 短い説明

詳細な説明（必要に応じて）

- 変更点1
- 変更点2
```

### 使用する絵文字：

- 🐛 `:bug:` - バグ修正
- ✨ `:sparkles:` - 新機能
- 📝 `:memo:` - ドキュメント
- 🎨 `:art:` - コードスタイル/構造の改善
- ♻️ `:recycle:` - リファクタリング
- ✅ `:white_check_mark:` - テストの追加/更新
- 🔧 `:wrench:` - 設定ファイルの変更
- ⬆️ `:arrow_up:` - 依存関係の更新
- 🔒 `:lock:` - セキュリティ修正

例：

```
[✨] Add user statistics feature

ユーザーの学習統計を取得する新機能を追加

- get_user_statistics()メソッドを実装
- 総学習時間と記録数を計算
- テストケースを追加
```

## プルリクエスト

### PRを作成する前に

- [ ] すべてのテストがパスすることを確認
- [ ] コードスタイルチェックがパスすることを確認
- [ ] 新機能にはテストが含まれている
- [ ] ドキュメントを更新（必要な場合）

### PRの説明

PRには以下を含めてください：

1. **変更内容の要約**
2. **変更の理由**
3. **関連するIssue番号**（ある場合）
4. **スクリーンショットやログ**（該当する場合）

### PRテンプレート

```markdown
## 変更内容

<!-- 何を変更したか簡潔に説明 -->

## 変更の理由

<!-- なぜこの変更が必要か -->

## 関連Issue

Closes #issue_number

## チェックリスト

- [ ] テストを追加/更新した
- [ ] ドキュメントを更新した
- [ ] コードスタイルチェックに合格
- [ ] すべてのテストに合格
```

## Issue報告

バグを発見した場合や新機能を提案する場合は、Issueを作成してください。

### バグ報告

```markdown
## バグの説明

<!-- バグの明確な説明 -->

## 再現手順

1.
2.
3.

## 期待される動作

<!-- 何が起こるべきか -->

## 実際の動作

<!-- 実際に何が起こったか -->

## 環境

- OS:
- Python version:
- Stplpy version:
```

### 機能要望

```markdown
## 機能の説明

<!-- 追加したい機能の説明 -->

## ユースケース

<!-- この機能が必要な理由と使用例 -->

## 実装案

<!-- 実装のアイデア（あれば） -->
```

## コードレビュー

すべてのPRはレビューされます。レビュアーからのフィードバックに建設的に対応してください。

## 質問

質問がある場合は、Issueを作成するか、既存のディスカッションに参加してください。

## ライセンス

貢献されたコードは、プロジェクトのライセンス（MIT）の下で公開されます。

---

貢献いただきありがとうございます！ 🎉
