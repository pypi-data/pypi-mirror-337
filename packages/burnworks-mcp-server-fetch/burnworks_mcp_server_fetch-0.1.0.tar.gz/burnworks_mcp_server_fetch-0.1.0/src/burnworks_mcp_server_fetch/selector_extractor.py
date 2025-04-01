"""
HTML要素セレクタを使用してコンテンツを抽出するための拡張モジュール
"""
from typing import Optional, Tuple
import logging

from bs4 import BeautifulSoup
import markdownify

logger = logging.getLogger(__name__)

def extract_with_selector(
    html: str, selector: str, selector_type: str
) -> Tuple[bool, str]:
    """
    セレクタを使用して特定のHTML要素を抽出し、マークダウンに変換する

    Args:
        html: 元のHTML文字列
        selector: 抽出対象の要素を指定するセレクタ
        selector_type: セレクタの種類 ('css', 'id', 'element')

    Returns:
        Tuple[bool, str]: (抽出成功したか, 抽出したコンテンツのマークダウン)
    """
    if not selector or not selector_type:
        return False, ""

    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        if selector_type == 'id':
            # ID指定の場合
            selected_content = soup.find(id=selector)
        elif selector_type == 'element':
            # 要素名指定の場合
            selected_content = soup.find(selector)
        elif selector_type == 'css':
            # CSSセレクタ指定の場合
            selected_content = soup.select_one(selector)
        else:
            # 不明なセレクタタイプの場合
            return False, f"<error>Unknown selector type: {selector_type}. Use 'id', 'element', or 'css'</error>"
        
        if selected_content:
            content = str(selected_content)
            markdown = markdownify.markdownify(
                content,
                heading_style=markdownify.ATX,
            )
            return True, markdown
        else:
            return False, f"<error>No content found matching the {selector_type} selector: {selector}</error>"
    
    except Exception as e:
        logger.exception(f"Error extracting content with selector: {str(e)}")
        return False, f"<error>Error extracting content with selector: {str(e)}</error>"


def validate_selector_params(selector: Optional[str], selector_type: Optional[str]) -> Optional[str]:
    """
    セレクタパラメータのバリデーション

    Args:
        selector: セレクタ文字列
        selector_type: セレクタタイプ

    Returns:
        Optional[str]: エラーメッセージ。問題がなければNone
    """
    if selector and not selector_type:
        return "If 'selector' is provided, 'selector_type' must also be provided (valid types: 'css', 'id', 'element')"
            
    if selector_type and selector_type not in ['css', 'id', 'element']:
        return "'selector_type' must be one of: 'css', 'id', 'element'"
    
    return None
