---
subagent:
  primary: system-architect
  description: 아키텍처 설계 및 상세설계 문서 생성
mcp-servers: [sequential-thinking, context7]
hierarchy-input: true
parallel-processing: true
---

# /wf:draft - 상세설계 (Lite)

> ⚠️ **DEPRECATED**: 이 명령어는 더 이상 사용되지 않습니다.
> development 카테고리는 `/wf:design` 명령어를 사용하세요.
> (4단계 워크플로우: `[ ]` → `[dd]` → `[ap]` → `[im]` → `[xx]`)

---

> **상태 전환**: `[bd] 기본설계` → `[dd] 상세설계`
> **적용 category**: development only (레거시)
> **계층 입력**: WP/ACT/Task 단위 (WP/ACT 입력 시 하위 Task 병렬 처리)

## 사용법

```bash
/wf:draft [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:draft TSK-01-01` | Task 단위 처리 |
| `/wf:draft ACT-01-01` | ACT 내 모든 `[bd]` Task 병렬 |
| `/wf:draft WP-01` | WP 내 모든 `[bd]` Task 병렬 |

---

## ⛔ 코드 작성 금지 원칙 (최우선)

| 금지 | 대체 | 감지 패턴 |
|------|------|----------|
| ❌ TS/JS 코드 | ✅ 메서드 시그니처 표 | `function`, `const`, `let`, `var` |
| ❌ Vue/React 코드 | ✅ Props/Events 표 | `<template>`, `<script>`, `defineComponent` |
| ❌ 테스트 코드 | ✅ 테스트 시나리오 표 | `describe(`, `it(`, `test(`, `expect(` |
| ❌ SQL 쿼리 | ✅ ERD + 필드 표 | `SELECT`, `INSERT`, `UPDATE` |
| ❌ 타입 정의 | ✅ 필드 정의 표 | `interface`, `type`, `export` |
| ✅ **Prisma 스키마** | **유일한 예외** | `model`, `@@`, `@relation` |

**설계 표현 원칙**:
```
├── 📊 표 (Table) - 필드 정의, 메서드 목록, API 명세
├── 📐 다이어그램 (Mermaid) - ERD, 시퀀스, 상태 전환
├── 🌳 트리 구조 (Text) - 디렉토리, 컴포넌트 계층
└── 🎨 Text Art - 화면 레이아웃 와이어프레임
```

---

## 생성 문서 (3개 분할)

| 파일 | 내용 |
|------|------|
| `020-detail-design.md` | 상세설계 본문 (아키텍처, API, UI, 비즈니스로직) |
| `025-traceability-matrix.md` | 추적성 매트릭스 (FR/BR → 설계 → 테스트) |
| `026-test-specification.md` | 테스트 명세 (UT, E2E, TC, Fixture) |

---

## 실행 과정

### 1. Task 검증 및 컨텍스트 수집

```
탐색 경로:
├── Task: {TSK-ID}/
│   ├── 010-basic-design.md ✅ (필수)
│   ├── 011-ui-design.md (선택)
│   └── ui-assets/*.svg (선택)
├── Project:
│   ├── prd.md → PRD 참조 섹션 추출
│   └── trd.md → 기술 스택/규칙 확인
```

### 2. 상위 문서 분석

| 문서 | 추출 항목 |
|------|----------|
| 기본설계 | FR-XXX, BR-XXX, 데이터/화면/인터페이스 요구 |
| 화면설계 | SCR-XX, 컴포넌트, 상태, SVG 참조 |
| PRD | 원본 요구사항, 비즈니스 규칙 |
| TRD | 기술 스택, API 규칙, 네이밍 컨벤션 |

### 3. 상세설계 문서 생성

| 설계 항목 | 표현 방식 |
|----------|----------|
| 데이터베이스 ERD | Mermaid erDiagram |
| **Prisma 스키마** | ✅ 코드 블록 (유일한 예외) |
| 백엔드 모듈 구조 | 트리 + 역할 표 |
| API 명세 | 엔드포인트/Request/Response 표 |
| UI 컴포넌트 | Props/Events/상태 표 |
| 비즈니스 로직 | 시퀀스 다이어그램 + 서비스 메서드 표 |
| 테스트 시나리오 | UT/E2E 시나리오 표 (코드 아님) |

### 4. 일관성 검증 (CHK-*)

#### PRD ↔ 기본설계
| ID | 검증 항목 |
|----|----------|
| CHK-PRD-01 | 기능 요구사항 완전성 |
| CHK-PRD-02 | 비즈니스 규칙 일치성 |
| CHK-PRD-03 | 용어 일관성 |
| CHK-PRD-04 | 범위 일치성 |

#### 기본설계 ↔ 상세설계
| ID | 검증 항목 |
|----|----------|
| CHK-BD-01 | FR 구현 방법 명시 |
| CHK-BD-02 | BR 구현 위치/방식 정의 |
| CHK-BD-03 | 데이터 모델 → Prisma 매핑 |
| CHK-BD-04 | 인터페이스 → API 매핑 |
| CHK-BD-05 | 화면 → 컴포넌트 매핑 |
| CHK-BD-06 | 수용기준 → 테스트케이스 변환 |

#### 화면설계 ↔ 상세설계 (선택)
| ID | 검증 항목 |
|----|----------|
| CHK-UI-01 | 화면 목록 완전성 |
| CHK-UI-02 | 화면 흐름 일치성 |
| CHK-UI-03 | 컴포넌트 커버리지 |
| CHK-UI-04 | 상태 정의 완전성 |
| CHK-UI-05 | 화면설계 ↔ 상세설계 동기화 |

#### TRD ↔ 상세설계
| ID | 검증 항목 |
|----|----------|
| CHK-TRD-01 | 기술 스택 준수 |
| CHK-TRD-02 | 아키텍처 패턴 준수 |
| CHK-TRD-03 | API 설계 규칙 준수 |
| CHK-TRD-04 | DB 스키마 규칙 준수 |
| CHK-TRD-05 | 에러 핸들링 표준 준수 |

### 5. 검증 결과 출력

```
┌─────────────────────────────────────────────┐
│ 📋 일관성 검증 결과                          │
├─────────────────────────────────────────────┤
│ ✅ PASS: 17 | ⚠️ WARN: 1 | ❌ FAIL: 0        │
├─────────────────────────────────────────────┤
│ [PASS] CHK-PRD-01: 기능 요구사항 완전성      │
│ [WARN] CHK-PRD-03: 용어 혼용 (통일 권장)     │
└─────────────────────────────────────────────┘
```

### 6. 추적성 매트릭스 생성

- FR → PRD → 기본설계 → 상세설계 → 테스트
- BR → 구현 위치 → 테스트
- 데이터 모델 → Prisma → API DTO

### 7. 상태 전환 (자동)

```bash
npx tsx .jjiban/script/transition.ts {Task-ID} draft -p {project}
```
- 성공: `{ "success": true, "newStatus": "dd" }`

---

## 검증 결과 처리

| 결과 | 처리 |
|------|------|
| ❌ FAIL | 문서 생성 중단, 상위 문서 수정 요청 |
| ⚠️ WARN | 문서 생성 진행, 검토 항목 기록 |
| ✅ PASS | 정상 진행 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 기본설계 상태가 아닙니다` |
| 기본설계 없음 | `[ERROR] 010-basic-design.md가 없습니다` |
| 코드 블록 감지 | `[ERROR] 코드 감지. 표/다이어그램으로 변환 필요` |
| 일관성 검증 실패 | `[FAIL] CHK-TRD-01: 기술 스택 불일치` |
| 화면설계 미발견 | `[INFO] 011-ui-design.md 없음 (화면 없는 기능)` |

---

## 다음 명령어

- `/wf:review` - LLM 설계 리뷰 (상태 변경 없음)
- `/wf:build` - 구현 시작

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:draft lite
Version: 1.1
-->
