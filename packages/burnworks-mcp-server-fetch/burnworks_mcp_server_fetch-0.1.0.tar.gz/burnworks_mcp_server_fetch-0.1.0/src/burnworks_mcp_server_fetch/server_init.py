"""
セレクタ機能の初期化とパッチの適用
"""

def apply_selector_patch():
    """
    セレクタ機能のパッチを適用
    server.pyでインポートして実行する
    """
    # server_patch モジュールをインポート
    try:
        # server.pyの関数をserver_patch内の関数で置き換え
        import burnworks_mcp_server_fetch.server as server
        from burnworks_mcp_server_fetch.server_patch import (
            extract_content_from_html,
            fetch_url,
            validate_fetch_args,
            get_selector_info,
            SELECTOR_SUPPORT
        )
        
        # 元の関数を拡張版で置き換える
        server.extract_content_from_html = extract_content_from_html
        server.fetch_url = fetch_url
        
        # パッチされたことを示す属性を追加
        server.SELECTOR_SUPPORT = SELECTOR_SUPPORT
        server.validate_fetch_args = validate_fetch_args
        server.get_selector_info = get_selector_info
        
        return True
    except ImportError:
        return False
