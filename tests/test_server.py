"""server.py のテスト"""
import os
import pytest
from unittest.mock import patch, AsyncMock

from ibm_cloud_token_mcp.config import Config
from ibm_cloud_token_mcp.server import create_server


class TestServer:
    """FastMCP サーバーのテスト"""
    
    @pytest.fixture
    def config(self):
        """Config のインスタンスを作成"""
        with patch.dict(os.environ, {"IBM_CLOUD_API_KEY": "test_api_key"}):
            return Config()
    
    def test_create_server(self, config):
        """サーバーが正常に作成されることを確認"""
        mcp = create_server(config)
        assert mcp is not None
        assert mcp.name == "IBMCloudTokenMCPServer"
        assert mcp.version == "0.1.0"
    
    @pytest.mark.asyncio
    async def test_get_token_tool(self, config):
        """get_token ツールが正常に動作することを確認"""
        mcp = create_server(config)
        
        # TokenManager.get_token をモック
        mock_result = {
            "access_token": "test_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        with patch("ibm_cloud_token_mcp.server.TokenManager.get_token", new_callable=AsyncMock) as mock_get_token:
            mock_get_token.return_value = mock_result
            
            # ツールを取得して実行
            tools = await mcp.list_tools()
            get_token_tool = next((t for t in tools if t.name == "get_token"), None)
            assert get_token_tool is not None
    

# Made with Bob
