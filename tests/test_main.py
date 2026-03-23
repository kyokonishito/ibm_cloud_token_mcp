"""__main__.py のエントリーポイントテスト"""
import subprocess
import sys
import pytest
from pathlib import Path


class TestMainEntry:
    """メインエントリーポイントのテスト"""
    
    def test_server_starts_without_banner_in_stdout(self, monkeypatch):
        """サーバーが起動時にバナーを stdout に出力しないことを確認
        
        このテストは、FastMCP のバナーが stdout に出力されると
        MCP クライアント（Bob/Claude Desktop）がエラーと解釈する問題を検出します。
        """
        # API Key を設定
        monkeypatch.setenv("IBM_CLOUD_API_KEY", "test_api_key_12345")
        
        # サーバーをサブプロセスで起動（短時間で終了させる）
        process = subprocess.Popen(
            [sys.executable, "-m", "ibm_cloud_token_mcp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        try:
            # 標準入力を閉じてサーバーを終了させる
            process.stdin.close()
            
            # プロセスが終了するまで待機（タイムアウト付き）
            stdout, stderr = process.communicate(timeout=3)
            
            # stdout にバナーの文字列が含まれていないことを確認
            assert "FastMCP" not in stdout, \
                "FastMCP banner should not appear in stdout (use show_banner=False)"
            assert "╭──" not in stdout, \
                "Banner box characters should not appear in stdout"
            assert "gofastmcp.com" not in stdout, \
                "FastMCP URL should not appear in stdout"
            
            # stderr にはログが出力されていることを確認（正常動作）
            assert len(stderr) > 0, "Logs should be written to stderr"
            
        except subprocess.TimeoutExpired:
            process.kill()
            pytest.fail("Server did not terminate within timeout")
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=2)
    


# Made with Bob