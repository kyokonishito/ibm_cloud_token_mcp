"""IBM Cloud トークン管理モジュール"""
import httpx
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class TokenManager:
    """IBM Cloud IAM トークンを管理するクラス"""
    
    def __init__(self, iam_endpoint: str):
        """
        Args:
            iam_endpoint: IBM Cloud IAM エンドポイント
        """
        self.iam_endpoint = iam_endpoint
        self.token_url = f"{iam_endpoint}/identity/token"
    
    async def get_token(self, api_key: str) -> Dict:
        """API Key から Bearer Token を取得
        
        Args:
            api_key: IBM Cloud API Key
            
        Returns:
            トークン情報を含む辞書
            {
                "access_token": "eyJhbGc...",
                "token_type": "Bearer",
                "expires_in": 3600,
                "expiration": 1234567890,
                "scope": "ibm openid"
            }
            
        Raises:
            ValueError: API リクエストが失敗した場合
            
        Note:
            IBM Cloud API Key ベースの認証では refresh_token はサポートされていません。
            トークンの有効期限は通常3600秒（1時間）です。
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json"
                    },
                    data={
                        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                        "apikey": api_key
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code}")
            error_detail = e.response.text
            raise ValueError(f"Failed to get token (HTTP {e.response.status_code}): {error_detail}")
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise ValueError(f"Failed to connect to IBM Cloud IAM: {str(e)}")

# Made with Bob
