"""設定管理モジュール"""
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """アプリケーション設定を管理するクラス"""
    
    def __init__(self):
        # .env ファイルを読み込み（複数の場所を試す）
        self._load_env_files()
        self.api_key = self._load_api_key()
        self.iam_endpoint = os.getenv("IBM_CLOUD_IAM_ENDPOINT", "https://iam.cloud.ibm.com")
    
    def _load_env_files(self) -> None:
        """複数の場所から .env ファイルを読み込む
        
        以下の順序で .env ファイルを探します：
        1. カレントディレクトリの .env
        2. ホームディレクトリの .env
        """
        # カレントディレクトリの .env を読み込み
        load_dotenv()
        
        # ホームディレクトリの .env も読み込み（既存の環境変数は上書きしない）
        home_env = Path.home() / ".env"
        if home_env.exists():
            load_dotenv(home_env, override=False)
    
    def _load_api_key(self) -> str:
        """環境変数から API Key を読み込む
        
        Returns:
            IBM Cloud API Key
            
        Raises:
            ValueError: API Key が設定されていない場合
        """
        api_key = os.getenv("IBM_CLOUD_API_KEY")
        if not api_key:
            raise ValueError(
                "IBM_CLOUD_API_KEY environment variable is not set. "
                "Please set it in one of the following ways:\n"
                "1. Environment variable: export IBM_CLOUD_API_KEY=your_api_key\n"
                "2. .env file in current directory\n"
                "3. ~/.env file in home directory\n"
                "4. MCP server config file env section"
            )
        return api_key
    
    def validate(self) -> bool:
        """設定の妥当性を検証
        
        Returns:
            設定が有効な場合は True
        """
        return bool(self.api_key)

# Made with Bob
