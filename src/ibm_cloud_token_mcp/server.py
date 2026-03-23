"""FastMCP サーバー定義"""
import fastmcp
from typing import Optional
import logging

from .config import Config
from .token_manager import TokenManager

logger = logging.getLogger(__name__)


def create_server(config: Config) -> fastmcp.FastMCP:
    """FastMCP サーバーを作成して設定する
    
    Args:
        config: アプリケーション設定
        
    Returns:
        設定済みの FastMCP サーバーインスタンス
    """
    # FastMCP サーバーを作成
    mcp = fastmcp.FastMCP(
        name="IBMCloudTokenMCPServer",
        version="0.1.0",
    )
    
    # TokenManager のインスタンスを作成
    token_manager = TokenManager(config.iam_endpoint)
    
    @mcp.tool()
    async def get_token(api_key: Optional[str] = None) -> dict:
        """IBM Cloud API Key から Bearer Token を取得します。
        
        Args:
            api_key: IBM Cloud API Key（省略時は環境変数から取得）
            
        Returns:
            トークン情報を含む辞書
            {
                "access_token": "eyJhbGc...",
                "token_type": "Bearer",
                "expires_in": 3600,
                "expiration": 1234567890,
                "scope": "ibm openid"
            }
            
        Note:
            IBM Cloud API Key ベースの認証では、トークンは3600秒（1時間）有効です。
            期限切れの場合は、このツールを再度呼び出して新しいトークンを取得してください。
        """
        try:
            # API Key が指定されていない場合は設定から取得
            key = api_key if api_key else config.api_key
            
            logger.info("Requesting token from IBM Cloud IAM")
            result = await token_manager.get_token(key)
            logger.info("Token retrieved successfully")
            
            return result
        except Exception as e:
            logger.error(f"Error getting token: {str(e)}")
            raise
    
    return mcp

# Made with Bob
