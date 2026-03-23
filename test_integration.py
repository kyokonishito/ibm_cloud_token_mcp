"""統合テスト - 実際の IBM Cloud API を使用してトークンを取得"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# プロジェクトのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ibm_cloud_token_mcp.config import Config
from ibm_cloud_token_mcp.token_manager import TokenManager


async def test_get_token():
    """実際の API Key を使用してトークンを取得"""
    print("=" * 60)
    print("IBM Cloud Token MCP Server - 統合テスト")
    print("=" * 60)
    
    try:
        # 設定を読み込み
        print("\n[1] 設定を読み込み中...")
        load_dotenv()
        config = Config()
        print(f"✓ API Key が設定されています（先頭5文字: {config.api_key[:5]}...）")
        print(f"✓ IAM エンドポイント: {config.iam_endpoint}")
        
        # TokenManager を作成
        print("\n[2] TokenManager を初期化中...")
        token_manager = TokenManager(config.iam_endpoint)
        print("✓ TokenManager が初期化されました")
        
        # トークンを取得
        print("\n[3] IBM Cloud からトークンを取得中...")
        result = await token_manager.get_token(config.api_key)
        
        print("✓ トークンの取得に成功しました！")
        print(f"\n--- トークン情報 ---")
        print(f"Token Type: {result.get('token_type')}")
        print(f"Expires In: {result.get('expires_in')} 秒")
        print(f"Expiration: {result.get('expiration')}")
        print(f"Access Token (先頭20文字): {result.get('access_token', '')[:20]}...")
        print(f"Scope: {result.get('scope')}")
        
        print("\n[4] トークンの有効期限について")
        print(f"   トークンは {result.get('expires_in')} 秒間有効です")
        print("   期限切れの場合は、get_token を再度呼び出してください")
        print("   (IBM Cloud API Key 認証では refresh token はサポートされていません)")
        
        print("\n" + "=" * 60)
        print("✓ すべてのテストが成功しました！")
        print("=" * 60)
        return True
        
    except ValueError as e:
        print(f"\n✗ エラーが発生しました: {e}")
        print("\n--- トラブルシューティング ---")
        print("1. IBM_CLOUD_API_KEY 環境変数が正しく設定されているか確認してください")
        print("2. API Key が有効であることを確認してください")
        print("3. インターネット接続を確認してください")
        return False
    except Exception as e:
        print(f"\n✗ 予期しないエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n注意: このテストは実際の IBM Cloud API を使用します。")
    print("有効な IBM_CLOUD_API_KEY が必要です。\n")
    
    # API Key が設定されているか確認
    load_dotenv()
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    
    if not api_key:
        print("✗ IBM_CLOUD_API_KEY が設定されていません。")
        print("\n以下のいずれかの方法で設定してください:")
        print("1. 環境変数: export IBM_CLOUD_API_KEY=your_api_key")
        print("2. .env ファイル: IBM_CLOUD_API_KEY=your_api_key")
        sys.exit(1)
    
    if api_key == "test_api_key_for_testing":
        print("✗ テスト用のダミー API Key が設定されています。")
        print("実際の IBM Cloud API Key を設定してください。")
        sys.exit(1)
    
    # テストを実行
    success = asyncio.run(test_get_token())
    sys.exit(0 if success else 1)

# Made with Bob
