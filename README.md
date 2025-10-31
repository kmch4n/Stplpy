# Stplpy 👋

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## About

StplpyはStudyPlusをPythonで操作するためのライブラリです。
このコードは学習目的で作成されたものであり、bot運用などを推奨するものではありません。

### 主な機能

- ユーザー情報の取得・管理
- フォロー・フォロワー操作
- タイムライン取得（複数種類対応）
- 学習記録の投稿・削除
- 投稿へのいいね・コメント機能
- プロフィール画像の更新
- **型ヒント完備**
- **カスタム例外クラス**
- **ユーティリティ関数**
- **テストスイート完備**

## Installation

### pipを使用したインストール（開発版）

```bash
git clone https://github.com/kmch4n/Stplpy.git
cd Stplpy
pip install -e .
```

### 開発用インストール

テストやコード品質ツールも含めてインストール：

```bash
pip install -e ".[dev]"
```

## 実行環境

このプロジェクトはPython 3.12以上で動作することを前提としています。

## Setup

### 1. tokenの取得

Charles等を使用してStudyPlusを開いた状態で適当に動かすと、Request HeaderのAuthorizationから見つけられます。
`OAuth xxxxxxxx`の`xxxxxx`部分のみを抽出してください。
**Web版StudyPlusのトークンとは異なることに注意してください。**

### 2. `.env`の作成

プロジェクトルートに`.env`ファイルを作成：

```env
TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Usage

### 基本的な使用方法

```python
from stplpy import StudyPlus
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv(".env")
client = StudyPlus(os.environ["TOKEN"])

# ユーザー情報の取得
myself = client.get_myself()
print(f"Username: {myself['username']}")

# タイムラインの取得
timeline = client.get_followee_timeline()
print(f"Posts: {len(timeline['feeds'])}")

# 学習記録の投稿
record = client.post_study_record(
    duration=3600,  # 秒単位
    comment="Pythonの学習をしました！"
)
```

### 例外処理

```python
from stplpy import StudyPlus
from stplpy.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitError,
    APIError
)

client = StudyPlus(token)

try:
    user = client.get_user("username")
except ResourceNotFoundError:
    print("ユーザーが見つかりません")
except AuthenticationError:
    print("認証に失敗しました")
except RateLimitError:
    print("レート制限に達しました")
except APIError as e:
    print(f"API エラー: {e.status_code}")
```

### ユーティリティ関数

```python
from stplpy.utils import (
    format_study_duration,
    calculate_total_study_time,
    group_by_date
)

# 学習時間のフォーマット
duration = format_study_duration(7265)  # "2h 1m 5s"

# 総学習時間の計算
records = [{"duration": 3600}, {"duration": 1800}]
total = calculate_total_study_time(records)  # 5400

# 日付でグループ化
grouped = group_by_date(records, "record_datetime")
```

## Examples

詳しい使い方は、[example.py](https://github.com/kmch4n/Stplpy/blob/main/example.py)を参考にしてください。

## Development

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付きで実行
pytest --cov=stplpy --cov-report=html
```

### コード品質チェック

```bash
# コードフォーマット
black stplpy tests

# リント
flake8 stplpy tests

# 型チェック
mypy stplpy
```

## Contributing

貢献を歓迎します！詳細は[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。

## License

MIT License

## Changelog

### v0.2.0 (Latest)

- ✨ カスタム例外クラスの追加
- ✨ 完全な型ヒントサポート
- ✨ ユーティリティ関数の追加
- ✅ pytest テストスイートの追加
- 📦 pyproject.toml によるパッケージング
- 🐛 構文エラーとバグの修正
- 📝 ドキュメントの改善

### v0.1.0

- 初期リリース
- 基本的なAPI機能