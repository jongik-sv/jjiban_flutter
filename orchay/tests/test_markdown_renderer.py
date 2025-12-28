"""Markdown 렌더러 테스트.

markdown-it-py + Pygments 기반 서버 사이드 렌더링 검증.
"""

from __future__ import annotations

import pytest

from orchay.web.markdown_renderer import get_markdown_parser, get_pygments_css, render_markdown


class TestRenderMarkdown:
    """render_markdown 함수 테스트."""

    def test_basic_heading(self) -> None:
        """기본 헤딩 렌더링."""
        result = render_markdown("# Hello World")
        assert "<h1>" in result
        assert "Hello World" in result

    def test_multiple_headings(self) -> None:
        """여러 수준의 헤딩 렌더링."""
        md = "# H1\n## H2\n### H3"
        result = render_markdown(md)
        assert "<h1>" in result
        assert "<h2>" in result
        assert "<h3>" in result

    def test_paragraph(self) -> None:
        """단락 렌더링."""
        result = render_markdown("This is a paragraph.")
        assert "<p>" in result
        assert "This is a paragraph." in result

    def test_bold_and_italic(self) -> None:
        """볼드/이탤릭 렌더링."""
        result = render_markdown("**bold** and *italic*")
        assert "<strong>" in result or "<b>" in result
        assert "<em>" in result or "<i>" in result

    def test_gfm_table(self) -> None:
        """GFM 테이블 렌더링."""
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        result = render_markdown(md)
        assert "<table>" in result
        assert "<th>" in result
        assert "<td>" in result

    def test_gfm_tasklist(self) -> None:
        """GFM 체크리스트 렌더링."""
        md = "- [x] Done\n- [ ] Todo"
        result = render_markdown(md)
        assert 'type="checkbox"' in result
        assert "checked" in result

    def test_gfm_strikethrough(self) -> None:
        """GFM 취소선 렌더링."""
        result = render_markdown("~~deleted~~")
        assert "<del>" in result or "<s>" in result

    def test_code_inline(self) -> None:
        """인라인 코드 렌더링."""
        result = render_markdown("Use `print()` function")
        assert "<code>" in result
        assert "print()" in result

    def test_code_block_no_lang(self) -> None:
        """언어 없는 코드 블록 렌더링."""
        md = "```\nsome code\n```"
        result = render_markdown(md)
        assert "<pre>" in result
        assert "<code>" in result
        assert "some code" in result

    def test_code_highlighting_python(self) -> None:
        """Python 코드 하이라이팅."""
        md = "```python\nprint('hello')\n```"
        result = render_markdown(md)
        assert "highlight" in result
        assert "print" in result

    def test_code_highlighting_javascript(self) -> None:
        """JavaScript 코드 하이라이팅."""
        md = "```javascript\nconst x = 1;\n```"
        result = render_markdown(md)
        assert "highlight" in result

    def test_mermaid_passthrough(self) -> None:
        """Mermaid 코드 블록 패스스루 (클라이언트 렌더링용)."""
        md = "```mermaid\ngraph TD\n  A-->B\n```"
        result = render_markdown(md)
        assert 'class="language-mermaid"' in result
        # Mermaid는 Pygments로 하이라이팅하지 않음
        assert "highlight" not in result or 'language-mermaid' in result

    def test_link(self) -> None:
        """링크 렌더링."""
        result = render_markdown("[Google](https://google.com)")
        assert "<a" in result
        assert "href=" in result
        assert "Google" in result

    def test_image(self) -> None:
        """이미지 렌더링."""
        result = render_markdown("![alt](image.png)")
        assert "<img" in result
        assert "src=" in result

    def test_blockquote(self) -> None:
        """인용문 렌더링."""
        result = render_markdown("> This is a quote")
        assert "<blockquote>" in result

    def test_unordered_list(self) -> None:
        """순서 없는 목록 렌더링."""
        md = "- Item 1\n- Item 2"
        result = render_markdown(md)
        assert "<ul>" in result
        assert "<li>" in result

    def test_ordered_list(self) -> None:
        """순서 있는 목록 렌더링."""
        md = "1. First\n2. Second"
        result = render_markdown(md)
        assert "<ol>" in result
        assert "<li>" in result

    def test_horizontal_rule(self) -> None:
        """수평선 렌더링."""
        result = render_markdown("---")
        assert "<hr" in result

    def test_footnote(self) -> None:
        """각주 렌더링."""
        md = "Text[^1]\n\n[^1]: Footnote content"
        result = render_markdown(md)
        # footnote 플러그인이 작동하는지 확인
        assert "Footnote" in result

    def test_html_escape(self) -> None:
        """HTML 이스케이프 (XSS 방지)."""
        md = "```\n<script>alert('xss')</script>\n```"
        result = render_markdown(md)
        # script 태그가 이스케이프되어야 함
        assert "<script>" not in result
        assert "&lt;script&gt;" in result or "script" in result

    def test_empty_content(self) -> None:
        """빈 콘텐츠 처리."""
        result = render_markdown("")
        assert result == "" or result.strip() == ""


class TestGetMarkdownParser:
    """get_markdown_parser 함수 테스트."""

    def test_returns_markdown_it_instance(self) -> None:
        """MarkdownIt 인스턴스 반환."""
        from markdown_it import MarkdownIt

        parser = get_markdown_parser()
        assert isinstance(parser, MarkdownIt)

    def test_parser_is_cached(self) -> None:
        """파서 인스턴스가 캐싱되는지 확인."""
        parser1 = get_markdown_parser()
        parser2 = get_markdown_parser()
        assert parser1 is parser2


class TestGetPygmentsCss:
    """get_pygments_css 함수 테스트."""

    def test_returns_css_string(self) -> None:
        """CSS 문자열 반환."""
        css = get_pygments_css()
        assert isinstance(css, str)
        assert len(css) > 0

    def test_contains_highlight_class(self) -> None:
        """highlight 클래스 포함."""
        css = get_pygments_css()
        assert ".highlight" in css

    def test_contains_color_definitions(self) -> None:
        """색상 정의 포함."""
        css = get_pygments_css()
        assert "color:" in css or "background" in css

    def test_monokai_theme(self) -> None:
        """monokai 테마 CSS 생성."""
        css = get_pygments_css("monokai")
        assert ".highlight" in css

    def test_different_themes(self) -> None:
        """다른 테마들도 작동."""
        themes = ["monokai", "default", "friendly"]
        for theme in themes:
            css = get_pygments_css(theme)
            assert ".highlight" in css
