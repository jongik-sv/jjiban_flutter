# /wf:skip - 설계 생략 (Lite)

> **상태 전환**: `[ ] Todo` → `[im] 구현`
> **적용 category**: infrastructure only

## 사용법

```bash
/wf:skip [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:skip TSK-01-01` | 자동 검색 |
| `/wf:skip jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 용도

- 설계 문서 없이 바로 구현하는 간단한 인프라 Task
- 스크립트, 설정 파일 등 단순 작업

---

## 실행 과정

1. **Task 검증**
   - category가 `infrastructure`인지 확인
   - 현재 상태가 `[ ]` Todo인지 확인

2. **설계 생략 기록**
   - Task에 설계 생략 사유 기록

3. **상태 업데이트**
   - `[ ]` → `[im]`

---

## 사용 조건

| 조건 | 설명 |
|------|------|
| 단순 작업 | 설정 변경, 스크립트 작성 |
| 명확한 요구사항 | WBS 설명만으로 충분 |
| 낮은 복잡도 | 설계 문서 불필요 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] infrastructure만 지원합니다` |
| 잘못된 상태 | `[ERROR] Todo 상태가 아닙니다` |

---

## 다음 명령어

- `/wf:build` - 구현 시작

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:skip lite
Version: 1.0
-->
