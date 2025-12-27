"""설정 로드 유틸리티."""

from __future__ import annotations

import json
from pathlib import Path

from orchay.models.config import Config


class ConfigLoadError(Exception):
    """설정 로드 오류."""


def find_jjiban_root() -> Path | None:
    """프로젝트 루트에서 .jjiban 폴더를 찾는다.

    현재 디렉토리부터 상위로 탐색합니다.

    Returns:
        .jjiban 폴더 경로 또는 None
    """
    current = Path.cwd().resolve()
    while current != current.parent:
        jjiban_path = current / ".jjiban"
        if jjiban_path.is_dir():
            return jjiban_path
        current = current.parent
    return None


def load_config() -> Config:
    """설정 파일을 로드하여 Config 객체를 반환한다.

    설정 파일 경로: .jjiban/settings/orchay.json

    Returns:
        Config 객체 (파일 없으면 기본값)

    Raises:
        ConfigLoadError: JSON 파싱 오류 또는 스키마 검증 실패
    """
    jjiban_root = find_jjiban_root()

    if jjiban_root is None:
        # .jjiban 폴더가 없으면 기본값 반환
        return Config()

    config_path = jjiban_root / "settings" / "orchay.json"

    if not config_path.exists():
        # 설정 파일이 없으면 기본값 반환
        return Config()

    try:
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigLoadError(f"JSON 파싱 오류: {e}") from e
    except OSError as e:
        raise ConfigLoadError(f"파일 읽기 오류: {e}") from e

    try:
        return Config.model_validate(data)
    except Exception as e:
        raise ConfigLoadError(f"설정 검증 오류: {e}") from e
