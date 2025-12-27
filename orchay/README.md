# orchay

> **orch**estration + ok**ay** - WezTerm 기반 Task 스케줄러

wbs.md를 모니터링하여 실행 가능한 Task를 추출하고, 여러 Claude Code Worker pane에 작업을 자동 분배합니다.

## 설치

```bash
cd orchay
uv venv
uv pip install -e ".[dev]"
```

## 실행

```bash
# 개발 모드
python -m orchay

# 또는
orchay
```

## 기능

- wbs.md 파일 모니터링 및 파싱
- 스케줄 큐 관리 (우선순위, 의존성)
- Worker pane 상태 감지
- 자동 작업 분배
- 실행 모드: design, quick, develop, force

## 라이선스

MIT
