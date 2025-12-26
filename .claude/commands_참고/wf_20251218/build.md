# /wf:build - TDD 기반 구현 (Lite)

> **상태 전환**: `[ap] 설계승인` → `[im] 구현` (development)
> **상태 전환**: `[dd] 상세설계` → `[im] 구현` (infrastructure)
> **적용 category**: development, infrastructure

## 사용법

```bash
/wf:build [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:build TSK-01-01` | 자동 검색 |
| `/wf:build jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 실행 플로우

| Task 유형 | 실행 단계 |
|----------|----------|
| Backend-only | 1 → 2 → 4 → 5 |
| Frontend-only | 1 → 3 → 4 → 5 |
| Full-stack | 1 → 2 → 3 → 4 → 5 |
| infrastructure | 1 → 2(간소화) → 5 |

---

## 실행 과정

### 1단계: 설계 분석
- `020-detail-design.md` 로드
- `025-traceability-matrix.md` 로드 (테스트 매핑)
- `026-test-specification.md` 로드 (테스트 시나리오)
- `ui-assets/` 화면 이미지 분석 (Frontend)
- `ui-theme-*.md` 테마 참조 (Frontend)

### 2단계: Backend 구현
- **Red**: 테스트 시나리오 → Vitest 코드
- **Green**: Controller/Service/Repository
- **Refactor**: 코드 품질 개선

### 3단계: Frontend 구현
- UI Assets 기반 화면 구현
- API 연동 (useFetch)
- E2E 테스트 코드 작성

### 4단계: 구현 보고서
- `030-implementation.md` 생성
- 템플릿: `.jjiban/templates/030-implementation.md`

### 5단계: 상태 업데이트
- `[ap]` → `[im]` (development)
- `[dd]` → `[im]` (infrastructure)

---

## 품질 기준

| 항목 | 기준 |
|------|------|
| TDD 커버리지 | 80% 이상 |
| E2E 통과율 | 100% |
| 정적 분석 | Pass |

---

## 테스트-수정 루프

- TDD/E2E 실패 시 자동 수정 시도
- 최대 5회 재시도
- 5회 초과 시 수동 개입 요청

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development/infrastructure만 지원` |
| 잘못된 상태 (dev) | `[ERROR] 설계승인 상태가 아닙니다. /wf:approve 실행 필요` |
| 잘못된 상태 (infra) | `[ERROR] 상세설계 상태가 아닙니다` |
| 설계 문서 없음 | `[ERROR] 설계 문서가 없습니다` |
| 테스트 5회 초과 | `[ERROR] 5회 시도 후에도 실패` |

---

## 다음 명령어

| category | 다음 | 설명 |
|----------|------|------|
| development | `/wf:test` | 테스트 실행 |
| development | `/wf:audit` | 코드 리뷰 |
| infrastructure | `/wf:done` | 작업 완료 |

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:build lite
Version: 1.1
-->
