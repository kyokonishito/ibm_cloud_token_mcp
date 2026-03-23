"""config.py のテスト"""
import os
import pytest
from unittest.mock import patch

from ibm_cloud_token_mcp.config import Config


class TestConfig:
    """Config クラスのテスト"""
    
    def test_load_api_key_from_env(self):
        """環境変数から API Key を読み込めることを確認"""
        with patch.dict(os.environ, {"IBM_CLOUD_API_KEY": "test_api_key"}):
            config = Config()
            assert config.api_key == "test_api_key"
            assert config.iam_endpoint == "https://iam.cloud.ibm.com"
    
    def test_load_api_key_missing(self):
        """API Key が設定されていない場合に ValueError が発生することを確認"""
        # .env ファイルの読み込みもモックする
        with patch.dict(os.environ, {}, clear=True):
            with patch('ibm_cloud_token_mcp.config.load_dotenv'):
                with pytest.raises(ValueError) as exc_info:
                    Config()
                assert "IBM_CLOUD_API_KEY environment variable is not set" in str(exc_info.value)
    
    def test_validate_with_api_key(self):
        """API Key が設定されている場合に validate が True を返すことを確認"""
        with patch.dict(os.environ, {"IBM_CLOUD_API_KEY": "test_api_key"}):
            config = Config()
            assert config.validate() is True
    
    def test_validate_without_api_key(self):
        """API Key が空の場合に validate が False を返すことを確認"""
        with patch.dict(os.environ, {"IBM_CLOUD_API_KEY": "test_api_key"}):
            config = Config()
            config.api_key = ""
            assert config.validate() is False

# Made with Bob
