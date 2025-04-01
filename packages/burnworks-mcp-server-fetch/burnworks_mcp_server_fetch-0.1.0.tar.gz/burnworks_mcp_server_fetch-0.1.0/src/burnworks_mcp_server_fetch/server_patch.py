"""
元のMCPサーバーを拡張して、セレクタ機能を追加するためのパッチモジュール
"""
import logging
from typing import Optional, Tuple, Any

from pydantic import Field
from mcp.types import ErrorData, INVALID_PARAMS
from mcp.shared.exceptions import McpError

from burnworks_mcp_server_fetch.server import (
    extract_content_from_html as original_extract_content_from_html,
    fetch_url as original_fetch_url,
    Fetch,
)

# セレクタ機能のインポート
try:
    from burnworks_mcp_server_fetch.selector_extractor import extract_with_selector, validate_selector_params
    SELECTOR_SUPPORT = True
    logging.info("Selector support is enabled")
except ImportError:
    SELECTOR_SUPPORT = False
    logging.warning("Selector support is disabled. Install beautifulsoup4 to enable it.")

# Fetchモデルの拡張
if SELECTOR_SUPPORT:
    # selectorとselector_typeフィールドを追加
    Fetch.model_fields["selector"] = Field(
        default=None,
        description="CSS selector, ID, or element name to extract specific content",
    )
    Fetch.model_fields["selector_type"] = Field(
        default=None,
        description="Type of selector: 'css', 'id', or 'element'",
    )


# 拡張版のextract_content_from_html関数
def enhanced_extract_content_from_html(html: str, selector: Optional[str] = None, selector_type: Optional[str] = None) -> str:
    """拡張版: HTML内容を抽出してマークダウン形式に変換"""
    # セレクタ機能が利用可能でセレクタが指定されている場合
    if SELECTOR_SUPPORT and selector and selector_type:
        success, content = extract_with_selector(html, selector, selector_type)
        if success:
            return content
        # 失敗した場合は元の方法にフォールバック
    
    # 元の関数の処理を利用
    return original_extract_content_from_html(html)


# 拡張版のfetch_url関数
async def enhanced_fetch_url(
    url: str, user_agent: str, force_raw: bool = False, proxy_url: Optional[str] = None,
    selector: Optional[str] = None, selector_type: Optional[str] = None
) -> Tuple[str, str]:
    """拡張版: URLを取得して内容を返す"""
    # 元の関数を呼び出して基本的な内容を取得
    content, prefix = await original_fetch_url(url, user_agent, force_raw, proxy_url)
    
    # HTMLコンテンツでraw出力が要求されていない場合のみセレクタ処理を適用
    is_page_html = not prefix  # prefixが空なら、HTMLとして処理された
    
    if SELECTOR_SUPPORT and is_page_html and not force_raw and selector and selector_type:
        # セレクタを使用して内容を抽出
        success, selected_content = extract_with_selector(content, selector, selector_type)
        if success:
            return selected_content, prefix
    
    return content, prefix


# 元の関数をパッチ関数に置き換える
extract_content_from_html = enhanced_extract_content_from_html
fetch_url = enhanced_fetch_url


# call_tool関数でセレクタパラメータの検証を行うヘルパー関数
def validate_fetch_args(args: Any) -> None:
    """Fetch引数のバリデーション"""
    if SELECTOR_SUPPORT:
        selector = getattr(args, "selector", None)
        selector_type = getattr(args, "selector_type", None)
        
        error_msg = validate_selector_params(selector, selector_type)
        if error_msg:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))


# セレクタ情報を取得するヘルパー関数
def get_selector_info(args: Any) -> str:
    """セレクタ情報の文字列を作成"""
    if not SELECTOR_SUPPORT:
        return ""
    
    selector = getattr(args, "selector", None)
    selector_type = getattr(args, "selector_type", None)
    
    if selector and selector_type:
        return f" (extracted using {selector_type} selector: {selector})"
    return ""
