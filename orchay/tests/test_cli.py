"""CLI 파싱 테스트."""

from __future__ import annotations

import pytest


class TestParseArgsDefault:
    """TC-06: parse_args() 기본 실행 테스트."""

    def test_parse_args_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """기본 인자로 파싱."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(sys, "argv", ["orchay"])
        args = parse_args()

        assert args.project == "orchay"
        assert args.dry_run is False
        assert args.workers == 3
        assert args.mode == "quick"

    def test_parse_args_with_project(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """프로젝트명 지정."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(sys, "argv", ["orchay", "my-project"])
        args = parse_args()

        assert args.project == "my-project"


class TestParseArgsOptions:
    """TC-07: parse_args() 옵션 파싱 테스트."""

    def test_parse_args_with_workers(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Worker 수 옵션."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(sys, "argv", ["orchay", "-w", "2"])
        args = parse_args()

        assert args.workers == 2

    def test_parse_args_with_mode(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """모드 옵션."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(sys, "argv", ["orchay", "-m", "develop"])
        args = parse_args()

        assert args.mode == "develop"

    def test_parse_args_with_dry_run(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """dry-run 옵션."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(sys, "argv", ["orchay", "--dry-run"])
        args = parse_args()

        assert args.dry_run is True

    def test_parse_args_all_options(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """모든 옵션 조합."""
        import sys
        from orchay.main import parse_args

        monkeypatch.setattr(
            sys, "argv", ["orchay", "my-project", "-w", "2", "-m", "develop", "--dry-run", "-i", "10"]
        )
        args = parse_args()

        assert args.project == "my-project"
        assert args.workers == 2
        assert args.mode == "develop"
        assert args.dry_run is True
        assert args.interval == 10


class TestParseArgsHistorySubcommand:
    """TC-08: parse_args() history 서브커맨드 테스트."""

    def test_parse_args_history_list(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """history 목록 조회."""
        import sys
        from orchay.cli import create_parser

        monkeypatch.setattr(sys, "argv", ["orchay", "history"])
        parser = create_parser()
        args = parser.parse_args()

        assert args.command == "history"

    def test_parse_args_history_with_task_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """history 특정 Task 조회."""
        import sys
        from orchay.cli import create_parser

        monkeypatch.setattr(sys, "argv", ["orchay", "history", "TSK-01-01"])
        parser = create_parser()
        args = parser.parse_args()

        assert args.command == "history"
        assert args.task_id == "TSK-01-01"

    def test_parse_args_history_with_limit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """history limit 옵션."""
        import sys
        from orchay.cli import create_parser

        monkeypatch.setattr(sys, "argv", ["orchay", "history", "--limit", "20"])
        parser = create_parser()
        args = parser.parse_args()

        assert args.command == "history"
        assert args.limit == 20

    def test_parse_args_history_clear(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """history clear 옵션."""
        import sys
        from orchay.cli import create_parser

        monkeypatch.setattr(sys, "argv", ["orchay", "history", "--clear"])
        parser = create_parser()
        args = parser.parse_args()

        assert args.command == "history"
        assert args.clear is True
