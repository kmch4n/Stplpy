# Hi there👋
## About
StplpyはStudyPlusをPythonで操作するためのライブラリです。
このコードは学習目的で作成されたものであり、bot運用などを推奨するものではありません。

## Usage
### ライブラリのダウンロード
このプロジェクトを使用するには、いくつかの外部ライブラリが必要です。これらのライブラリはrequirements.txtファイルにリストされており、次のコマンドを実行することで簡単にインストールできます。

ターミナルまたはコマンドプロンプトを開き、プロジェクトのルートディレクトリ（requirements.txtファイルが存在するディレクトリ）に移動してください。次に、以下のコマンドを実行します：

``pip install -r requirements.txt``

### tokenの取得
Charles等を使用してStudyPlusを開いた状態で適当に動かすと、Request HeaderのAuthorizationから見つけられます。
``OAuth xxxxxxxx``の``xxxxxx``部分のみを抽出してください。
**Web版StudyPlusのトークンとは異なることに注意してください。**

### `.env`の作成
```config
TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Feature
```python
from  stplpy  import  StudyPlus
from  dotenv  import  load_dotenv
import  os

load_dotenv(".env")
cl  =  StudyPlus(os.environ["TOKEN"])

myself  =  cl.get_myself()
print(myself)
```
詳しい使い方は、[example.py](https://github.com/kmch4n/Stplpy/blob/main/example.py)を参考にしてください。