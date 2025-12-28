"""Markdown 렌더링 모듈 - VS Code 수준 품질.

markdown-it-py + Pygments 기반 서버 사이드 렌더링.
GFM(GitHub Flavored Markdown) 호환.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


def _highlight_code(code: str, lang: str) -> str:
    """Pygments 기반 코드 하이라이팅.

    Args:
        code: 코드 문자열
        lang: 언어 식별자 (예: python, javascript)

    Returns:
        하이라이팅된 HTML 문자열
    """
    if not lang:
        # 언어 미지정 시 일반 pre/code 블록
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code>{escaped}</code></pre>\n'

    # Mermaid는 클라이언트 사이드 렌더링을 위해 특별 처리
    if lang.lower() == "mermaid":
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code class="language-mermaid">{escaped}</code></pre>\n'

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except ClassNotFound:
        try:
            lexer = guess_lexer(code)
        except ClassNotFound:
            escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return f'<pre><code class="language-{lang}">{escaped}</code></pre>\n'

    formatter = HtmlFormatter(
        cssclass="highlight",
        linenos=False,
        nowrap=False,
    )
    return highlight(code, lexer, formatter)


def _render_fence(
    self: RendererHTML,
    tokens: list[Any],
    idx: int,
    options: dict[str, Any],
    env: dict[str, Any],
) -> str:
    """Fenced 코드 블록 렌더링 (```lang ... ```)."""
    token = tokens[idx]
    info = token.info.strip() if token.info else ""
    lang = info.split()[0] if info else ""

    return _highlight_code(token.content, lang)


def _render_code_block(
    self: RendererHTML,
    tokens: list[Any],
    idx: int,
    options: dict[str, Any],
    env: dict[str, Any],
) -> str:
    """일반 코드 블록 렌더링 (들여쓰기 기반)."""
    token = tokens[idx]
    return _highlight_code(token.content, "")


@lru_cache(maxsize=1)
def get_markdown_parser() -> MarkdownIt:
    """GFM 호환 Markdown 파서 인스턴스 반환 (캐싱).

    Returns:
        설정된 MarkdownIt 인스턴스
    """
    md = (
        MarkdownIt("gfm-like", {"linkify": True, "typographer": True})
        .use(footnote_plugin)
        .use(tasklists_plugin)
        .enable("table")
        .enable("strikethrough")
    )

    # 코드 블록 하이라이팅 룰 추가
    md.add_render_rule("fence", _render_fence)
    md.add_render_rule("code_block", _render_code_block)

    return md


def render_markdown(content: str) -> str:
    """Markdown 문자열을 HTML로 렌더링.

    Args:
        content: Markdown 원본 문자열

    Returns:
        렌더링된 HTML 문자열
    """
    md = get_markdown_parser()
    return md.render(content)


def get_pygments_css(style: str = "monokai") -> str:
    """Pygments 테마 CSS 반환.

    Args:
        style: Pygments 스타일 이름 (기본: monokai)

    Returns:
        CSS 문자열
    """
    formatter = HtmlFormatter(style=style)
    return formatter.get_style_defs(".highlight")
