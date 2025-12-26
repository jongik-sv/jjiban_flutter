# /wf:start - 워크플로우 시작 (Lite)

> **상태 전환**: `[ ] Todo` → `[bd]` | `[an]` | `[dd]`

## 사용법

```bash
/wf:start [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:start TSK-01-01` | 자동 검색 (1개면 자동, 여러 개면 선택) |
| `/wf:start jjiban/TSK-01-01` | 프로젝트 명시 (바로 실행) |

---

## 상태 전환 규칙

| category | 현재 | 다음 | 생성 문서 |
|----------|------|------|----------|
| development | `[ ]` | `[bd]` | `010-basic-design.md` |
| defect | `[ ]` | `[an]` | `010-defect-analysis.md` |
| infrastructure | `[ ]` | `[dd]` | `010-tech-design.md` (선택) |

---

## 실행 과정

1. **프로젝트 해결** (wf-common-lite 참조)
   - 입력 파싱: `/` 포함 여부 확인
   - 프로젝트 수 확인 및 ID 추출
   - 경로 결정: `.jjiban/projects/{project}/`

2. **Task 정보 수집**
   - wbs.md에서 Task 찾기
   - category, 상태, PRD 참조 확인

3. **PRD/TRD 내용 추출**
   - 기본설계 PRD 참조 섹션 읽기
   - TRD 기술 요구사항 참고

4. **범위 검증**
   - WBS Task 설명 범위 내 항목만 포함
   - 누락/초과 항목 확인

5. **문서 생성**
   - Task 폴더 생성: `.jjiban/projects/{project}/tasks/{TSK-ID}/`
   - 템플릿 참조: `.jjiban/templates/010-*.md`

6. **wbs.md 상태 업데이트**
   - status 필드 변경

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| Task 없음 | `[ERROR] Task를 찾을 수 없습니다` |
| 잘못된 상태 | `[ERROR] Todo 상태가 아닙니다` |
| category 없음 | `[ERROR] Task category가 지정되지 않았습니다` |
| PRD 참조 없음 | `[WARN] PRD 참조를 찾을 수 없습니다` |

---

## 다음 명령어

| category | 다음 | 설명 |
|----------|------|------|
| development | `/wf:ui` 또는 `/wf:draft` | UI 설계 또는 상세설계 |
| defect | `/wf:fix` | 수정 단계 |
| infrastructure | `/wf:skip` 또는 `/wf:build` | 설계 생략 또는 구현 |

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:start lite
Version: 1.0
-->
