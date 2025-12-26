---
subagent:
  primary: devops-architect
  description: 인프라 설계 생략 처리
hierarchy-input: true
parallel-processing: true
---

# /wf:skip - 설계 생략 (Lite)

> **상태 전환**: `[ ] Todo` → `[im] 구현`
> **적용 category**: infrastructure only
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)

## 사용법

```bash
/wf:skip [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:skip TSK-01-01` | Task 단위 |
| `/wf:skip ACT-01-01` | ACT 내 모든 `[ ]` infrastructure Task 병렬 |
| `/wf:skip WP-01` | WP 내 모든 Task 병렬 |

---

## 생략 타당성 기준 ⭐

### 생략 가능한 경우

| 조건 | 예시 |
|------|------|
| 단순 설정 변경 | 환경 변수 수정, 설정 파일 변경 |
| 명확한 리팩토링 | 코드 스타일, 린트 수정 |
| 버전 업그레이드 | 패키지 업데이트 |
| 문서화 작업 | README, 주석 추가 |

### 설계 필요 (생략 불가)

| 조건 | 예시 |
|------|------|
| 아키텍처 변경 | 서비스 구조 변경 |
| 복잡한 최적화 | 성능 튜닝, 캐싱 전략 |
| 보안 관련 변경 | 인증/인가 수정 |
| 마이그레이션 | DB 스키마 변경, 데이터 이관 |
| 외부 연동 | 새 API, 서드파티 통합 |

---

## 생략 확인 질문

```
생략 결정 체크리스트:
1. 이 작업은 아키텍처 변경을 포함하는가? → No
2. 복잡한 마이그레이션이 필요한가? → No
3. 다른 시스템에 영향을 미치는가? → No

→ 모두 "No"인 경우 생략 가능
```

---

## 실행 과정

### 1단계: Task 검증

- category가 `infrastructure`인지 확인
- 현재 상태가 `[ ]` Todo인지 확인

### 2단계: 생략 타당성 확인

- 상기 생략 조건 충족 여부 판단
- 생략 사유 기록

### 3단계: 구현 문서 초기화

```markdown
# 구현 문서: [Task명]

## 구현 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | infrastructure |
| 상태 | [im] 구현 |
| 설계 문서 | 생략 |

## 1. 설계 생략 사유
[생략 사유 - 예: 단순 설정 변경]

## 2. 작업 내용
| # | 파일 | 변경 내용 |
|---|------|----------|
| 1 | | |
```

### 4단계: 상태 전환

```bash
npx tsx .jjiban/script/transition.ts {Task-ID} skip -p {project}
```
- 성공: `{ "success": true, "newStatus": "im" }`

---

## 워크플로우 비교

### 설계 포함 (일반)

```
[ ] Todo
  │ /wf:start
  ▼
[ds] 설계
  │ /wf:build
  ▼
[im] 구현 → ...
```

### 설계 생략 (단순 작업)

```
[ ] Todo
  │ /wf:skip ← 현재
  ▼
[im] 구현 → ...
```

---

## 출력 예시

```
[wf:skip] 설계 생략

Task: TSK-03-01-01
Category: infrastructure
상태 전환: [ ] → [im] (설계 생략)

📋 생략 검증:
├── 아키텍처 변경: No ✅
├── 마이그레이션: No ✅
└── 외부 영향: No ✅

생략 사유: 단순 설정 변경 작업

📄 생성: 030-implementation.md (초기화)

구현 체크리스트:
├── 설정 파일 수정
├── 테스트 확인
└── 문서화

다음: /wf:build TSK-03-01-01
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] infrastructure만 지원합니다` |
| 잘못된 상태 | `[ERROR] Todo 상태가 아닙니다` |
| 이미 설계 시작 | `[ERROR] 이미 설계가 시작되었습니다` |

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
Version: 1.1
-->
