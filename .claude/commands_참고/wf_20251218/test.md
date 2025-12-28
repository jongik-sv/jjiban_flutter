# /wf:test - 테스트 실행 (Lite)

> **상태 변경 없음**: 반복 실행 가능
> **적용 category**: development, defect

## 사용법

```bash
/wf:test [PROJECT/]<Task-ID> [--type tdd|e2e|all]
```

| 예시 | 설명 |
|------|------|
| `/wf:test TSK-01-01` | 자동 검색 |
| `/wf:test orchay/TSK-01-01 --type e2e` | 프로젝트 명시 + 옵션 |

---

## 테스트 유형

| 유형 | 도구 | 대상 |
|------|------|------|
| TDD | Vitest | Backend 단위/통합 |
| E2E | Playwright | Frontend 시나리오 |
| all | 모두 | TDD + E2E |

---

## 실행 과정

### 1단계: 테스트 환경 준비
- 테스트 명세 로드 (`026-test-specification.md`)
- 테스트 데이터 (Fixture) 준비
- 환경 변수 설정

### 2단계: TDD 테스트 실행
- Vitest 실행
- 커버리지 리포트 생성
- 실패 시 자동 수정 루프

### 3단계: E2E 테스트 실행
- Playwright 실행
- 스크린샷 캡처
- 실패 시 자동 수정 루프

### 4단계: 결과 문서 생성
- `070-tdd-test-results.md`
- `070-e2e-test-results.md`
- `test-results/[timestamp]/`

---

## 자동 수정 루프

| 단계 | 설명 |
|------|------|
| 1 | 테스트 실행 |
| 2 | 실패 분석 |
| 3 | 코드 수정 |
| 4 | 재실행 (최대 5회) |

---

## 품질 기준

| 항목 | 기준 |
|------|------|
| TDD 커버리지 | 80% 이상 |
| TDD 통과율 | 100% |
| E2E 통과율 | 100% |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 테스트 명세 없음 | `[ERROR] 026-test-specification.md가 없습니다` |
| TDD 5회 초과 | `[ERROR] TDD 5회 시도 후에도 실패` |
| E2E 5회 초과 | `[ERROR] E2E 5회 시도 후에도 실패` |
| 커버리지 미달 | `[WARN] 커버리지 미달: N% (목표: 80%)` |

---

## 다음 명령어

- `/wf:audit` - 코드 리뷰
- `/wf:verify` - 통합테스트

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:test lite
Version: 1.0
-->
