"""token_manager.py のテスト"""
import pytest
import respx
import httpx

from ibm_cloud_token_mcp.token_manager import TokenManager


class TestTokenManager:
    """TokenManager クラスのテスト"""
    
    @pytest.fixture
    def token_manager(self):
        """TokenManager のインスタンスを作成"""
        return TokenManager("https://iam.cloud.ibm.com")
    
    @pytest.mark.asyncio
    @respx.mock
    async def test_get_token_success(self, token_manager):
        """トークン取得が成功することを確認"""
        # モックレスポンスを設定
        mock_response = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "J1vABcD3fGhI5kLmN7pQrS9tUvW1xYz...",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": 1234567890,
            "scope": "ibm openid"
        }
        
        respx.post("https://iam.cloud.ibm.com/identity/token").mock(
            return_value=httpx.Response(200, json=mock_response)
        )
        
        # トークンを取得
        result = await token_manager.get_token("test_api_key")
        
        # 結果を検証
        assert result["access_token"] == mock_response["access_token"]
        assert result["token_type"] == "Bearer"
        assert result["expires_in"] == 3600
    
    @pytest.mark.asyncio
    @respx.mock
    async def test_get_token_invalid_api_key(self, token_manager):
        """無効な API Key でエラーが発生することを確認"""
        # 401 エラーをモック
        respx.post("https://iam.cloud.ibm.com/identity/token").mock(
            return_value=httpx.Response(401, json={"error": "invalid_apikey"})
        )
        
        # エラーが発生することを確認
        with pytest.raises(ValueError) as exc_info:
            await token_manager.get_token("invalid_api_key")
        
        assert "Failed to get token" in str(exc_info.value)
        assert "401" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @respx.mock
    async def test_get_token_network_error(self, token_manager):
        """ネットワークエラーが発生することを確認"""
        # ネットワークエラーをモック
        respx.post("https://iam.cloud.ibm.com/identity/token").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )
        
        # エラーが発生することを確認
        with pytest.raises(ValueError) as exc_info:
            await token_manager.get_token("test_api_key")
        
        assert "Failed to connect to IBM Cloud IAM" in str(exc_info.value)
    

# Made with Bob
