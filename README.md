# IBM Cloud Token MCP Server

IBM Cloud の REST API を使用する際に必要な Bearer Token を取得・管理する MCP サーバーです。

## 機能

- IBM Cloud API Key から Bearer Token を取得
- 環境変数と .env ファイルのサポート
- 包括的なエラーハンドリング
- stdio ベースの MCP プロトコル実装

## 前提条件

- Python 3.10 以上
- IBM Cloud API Key（[API Key の取得方法](https://cloud.ibm.com/iam/apikeys)）
- uv（開発用）または pipx（インストール用）

## インストール

### pipx を使用したインストール（推奨）

```bash
pipx install git+https://github.com/kyokonishito/ibm_cloud_token_mcp.git
```

### uv を使用した開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/kyokonishito/ibm-cloud-token-mcp.git
cd ibm-cloud-token-mcp

# 仮想環境を作成して依存関係をインストール
uv venv
source .venv/bin/activate  # Windows の場合: .venv\Scripts\activate
uv pip install -e "."
```

## 設定

### IBM Cloud API Key の取得

1. [IBM Cloud](https://cloud.ibm.com/) にログイン
2. [管理 > アクセス (IAM) > API キー](https://cloud.ibm.com/iam/apikeys) に移動
3. 「IBM Cloud API キーの作成」をクリック
4. 名前と説明を入力
5. API Key をコピー（再度表示できません）

### API Key の設定

IBM Cloud API Key は以下の4つの方法で設定できます（優先順位順）：

#### 方法 1: MCP 設定ファイルの env セクション（推奨）

設定ファイルに直接指定する方法です。

#### 方法 2: システム環境変数

```bash
export IBM_CLOUD_API_KEY=your_api_key_here
```

#### 方法 3: カレントディレクトリの .env ファイル

開発時に便利です。プロジェクトルートに `.env` ファイルを作成：

```
IBM_CLOUD_API_KEY=your_api_key_here
```

#### 方法 4: ホームディレクトリの .env ファイル

pipx でインストールした場合に便利です。`~/.env` ファイルを作成：

```bash
# macOS/Linux
echo "IBM_CLOUD_API_KEY=your_api_key_here" >> ~/.env

# Windows (PowerShell)
Add-Content -Path "$env:USERPROFILE\.env" -Value "IBM_CLOUD_API_KEY=your_api_key_here"
```

## 使用方法

### Claude Desktop での設定

Claude Desktop の設定ファイルに以下を追加：

**macOS の場合:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows の場合:** `%APPDATA%\Claude\claude_desktop_config.json`

#### 開発環境（uv）の場合

```json
{
  "mcpServers": {
    "ibm-cloud-token": {
      "command": "python",
      "args": ["-m", "ibm_cloud_token_mcp"],
      "env": {
        "IBM_CLOUD_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### pipx でインストールした場合

```json
{
  "mcpServers": {
    "ibm-cloud-token": {
      "command": "ibm-cloud-token-mcp",
      "env": {
        "IBM_CLOUD_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**注意:** `env` セクションを省略した場合は、システム環境変数または `.env` ファイルから API Key を読み込みます。

### IBM Bob での設定

IBM Bob の設定ファイルに以下を追加：

#### 開発環境（uv）の場合

```json
{
  "mcpServers": {
    "ibm-cloud-token": {
      "command": "python",
      "args": ["-m", "ibm_cloud_token_mcp"],
      "env": {
        "IBM_CLOUD_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### pipx でインストールした場合

```json
{
  "mcpServers": {
    "ibm-cloud-token": {
      "command": "ibm-cloud-token-mcp",
      "env": {
        "IBM_CLOUD_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**注意:** `env` セクションを省略した場合は、システム環境変数または `.env` ファイルから API Key を読み込みます。

## 利用可能なツール

### get_token

IBM Cloud API Key から Bearer Token を取得します。

**パラメータ:**
- `api_key` (オプション): IBM Cloud API Key。指定しない場合は環境変数から取得します。

**戻り値:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "expiration": 1234567890,
  "scope": "ibm openid"
}
```

**Claude/Bob での使用例:**
```
IBM Cloud のトークンを取得してください。
```

**注意:** 
- トークンの有効期限は 3600 秒（1時間）です
- トークンの有効期限が切れた場合は、`get_token` を再度呼び出して新しいトークンを取得してください
- IBM Cloud API Key 認証では refresh token はサポートされていません

## 開発

### 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/kyokonishito/ibm-cloud-token-mcp.git
cd ibm-cloud-token-mcp

# uv で仮想環境を作成
uv venv
source .venv/bin/activate  # Windows の場合: .venv\Scripts\activate

# 依存関係（開発用を含む）をインストール
uv pip install -e "."
uv pip install pytest pytest-asyncio pytest-cov respx
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジ付きで実行
pytest --cov=ibm_cloud_token_mcp --cov-report=html

#特定のテストファイルを実行
pytest tests/test_config.py
```

### サーバーをローカルで実行

```bash
# API Key を設定
export IBM_CLOUD_API_KEY=your_api_key_here

# サーバーを実行
python -m ibm_cloud_token_mcp
```

### 統合テストの実行

実際の IBM Cloud API を使用したテストを実行するには：

```bash
# 実際の API Key を .env ファイルに設定
echo "IBM_CLOUD_API_KEY=your_real_api_key" > .env

# 統合テストを実行
python test_integration.py
```

## トラブルシューティング

### API Key が見つからない

**エラー:** `IBM_CLOUD_API_KEY environment variable is not set`

**解決方法:** `IBM_CLOUD_API_KEY` 環境変数が設定されているか、`.env` ファイルに API Key が記載されているか確認してください。

### 無効な API Key

**エラー:** `Failed to get token (HTTP 401)`

**解決方法:** API Key が正しく、IBM Cloud で削除または無効化されていないことを確認してください。

### ネットワーク接続の問題

**エラー:** `Failed to connect to IBM Cloud IAM`

**解決方法:** インターネット接続を確認し、`https://iam.cloud.ibm.com` にアクセスできることを確認してください。

### トークンの有効期限切れ

トークンの有効期限が切れた場合は、`get_token` ツールを再度呼び出して新しいトークンを取得してください。

## アーキテクチャ

この MCP サーバーは以下を使用しています：
- **FastMCP**: MCP サーバー構築フレームワーク
- **httpx**: IBM Cloud API 呼び出し用の非同期 HTTP クライアント
- **python-dotenv**: 環境変数管理
- **stdio トランスポート**: MCP 通信用の標準入出力

## セキュリティに関する注意

- API Key をバージョン管理システムにコミットしないでください
- `.env` ファイルはデフォルトで `.gitignore` に含まれています
- API Key やトークンはログに出力されません
- 環境ごとに異なる API Key を使用してください

## ライセンス

Apache License 2.0 - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 参考資料

- [IBM Cloud IAM API ドキュメント](https://cloud.ibm.com/apidocs/iam-identity-token-api)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP フレームワーク](https://github.com/jlowin/fastmcp)

