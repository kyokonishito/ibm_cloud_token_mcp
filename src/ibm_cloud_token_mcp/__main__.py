"""IBM Cloud Token MCP Server のエントリーポイント

このモジュールは stdio トランスポートで MCP サーバーを起動します。

Usage:
    python -m ibm_cloud_token_mcp [--transport stdio]
    OR
    ibm-cloud-token-mcp [--transport stdio] (if installed via pipx)
"""
import sys
import argparse
import logging

from .config import Config
from .server import create_server

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr  # ログは stderr に出力
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析
    
    Returns:
        解析された引数
    """
    parser = argparse.ArgumentParser(
        description="IBM Cloud Token MCP Server - Provides IBM Cloud Bearer Token management"
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio"],
        default="stdio",
        help="Transport type (default: stdio)"
    )
    return parser.parse_args()


def main() -> None:
    """MCP サーバーを起動"""
    try:
        # コマンドライン引数を解析
        args = parse_args()
        
        # 設定を読み込み
        logger.info("Loading configuration")
        config = Config()
        
        # 設定を検証
        if not config.validate():
            logger.error("Configuration validation failed")
            sys.exit(1)
        
        logger.info("Configuration loaded successfully")
        
        # FastMCP サーバーを作成
        logger.info("Creating MCP server")
        mcp = create_server(config)
        
        # 指定されたトランスポートでサーバーを起動（バナーを無効化）
        logger.info(f"Starting MCP server with {args.transport} transport")
        mcp.run(transport=args.transport, show_banner=False)
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
