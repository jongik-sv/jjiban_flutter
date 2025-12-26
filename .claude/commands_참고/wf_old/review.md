---
name: wf:review
description: "development Task 설계 리뷰 실행. 상태 변경 없음, 반복 가능"
category: workflow
hierarchy-input: true
parallel-processing: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
---

# /wf:review - LLM 설계 리뷰

> **상태 내 액션**: 상태 변경 없음, 반복 가능
> **사용 가능 상태**: `[dd]` 상세설계
> **적용 category**: development only

## 사용법

```bash
/wf:review [WP-ID | ACT-ID | Task-ID] [--llm claude|gemini|codex]

# 예시
/wf:review TSK-01-01-01              # 단일 Task
/wf:review TSK-01-01-01 --llm gemini # 특정 LLM으로 리뷰
/wf:review ACT-01-01                 # Activity 내 모든 Task 병렬 처리
/wf:review WP-01                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[dd]` 상세설계 |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[dd]` 상태만 |
| `WP-XX` | WP 내 Task 병렬 처리 | `[dd]` 상태만 |

## 동작 규칙

| category | 사용 가능 상태 | 상태 변경 | 생성 문서 |
|----------|--------------|----------|----------|
| development | `[dd]` 상세설계 | 없음 (반복 가능) | `021-design-review-{llm}-{n}.md` |

## 문서 경로

@.claude/includes/wf-common.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 실행 과정

### 1단계: Task 검증
1. WBS에서 Task 찾기
2. category가 `development`인지 확인
3. 현재 상태가 `[dd]` 상세설계인지 확인
4. `020-detail-design.md` 존재 확인

### 2단계: 검증 대상 문서 수집
**필수 문서** (분할된 상세설계 문서):
- **상세설계서**: `[Task폴더]/020-detail-design.md`
- **추적성 매트릭스**: `[Task폴더]/025-traceability-matrix.md`
- **테스트 명세**: `[Task폴더]/026-test-specification.md`
- **기본설계서**: `[Task폴더]/010-basic-design.md`

**참조 문서**:
- **PRD**: `.jjiban/{project}/prd.md`
- **TRD**: `.jjiban/{project}/trd.md`
- **프로젝트 메타**: `.jjiban/{project}/project.json`

### 3단계: 다층 품질 검증 수행

#### 3.1 문서 구조 및 완전성 검증
1. **상세설계서 구조 분석** (분할된 3개 문서 검증):
   - `020-detail-design.md`: 상세설계 템플릿(`@.jjiban/templates/020-detail-design.md`) 준수 여부
   - `025-traceability-matrix.md`: 추적성 매트릭스 템플릿(`@.jjiban/templates/025-traceability-matrix.md`) 준수 여부
   - `026-test-specification.md`: 테스트 명세 템플릿(`@.jjiban/templates/026-test-specification.md`) 준수 여부
   - 각 문서의 필수 섹션 포함 여부
   - 문서 간 상호 참조 일관성

2. **요구사항 추적성 검증**:
   - 기본설계의 모든 요구사항(FR)이 상세설계에 반영되었는지 확인
   - 비즈니스 규칙(BR)과 설계 요소 간 매핑 검증
   - 누락된 요구사항 식별

3. **상위 문서 일관성 확인**:
   - PRD ↔ 기본설계 ↔ 상세설계 일관성 검증
   - TRD 기술 스택 준수 여부 확인
   - 용어 및 명명 규칙 일관성 검증

#### 3.2 아키텍처 검증 (system-architect 관점)
1. **시스템 구조 분석**:
   - 아키텍처 패턴 적절성 평가 (NestJS 모듈 구조, Vue 컴포넌트 구조)
   - 컴포넌트 분할 및 책임 분리 검증 (SRP, OCP, LSP, ISP, DIP)
   - 확장성 및 유지보수성 평가

2. **데이터 흐름 검증**:
   - 데이터 인터페이스 설계 적절성
   - API 설계 일관성 및 REST 원칙 준수
   - 데이터 모델 정규화 및 무결성

3. **통합 전략 평가**:
   - 외부 시스템/모듈 연동 설계 적절성
   - 에러 처리 및 트랜잭션 관리
   - 의존성 관리 전략

#### 3.3 보안 검증 (security-engineer 관점)
1. **보안 위협 분석**:
   - OWASP Top 10 대응 여부 확인
   - 인증/인가 메커니즘 적절성
   - 데이터 암호화 및 보호 전략

2. **취약점 식별**:
   - SQL Injection, XSS, CSRF 등 취약점 가능성
   - 민감 데이터 노출 위험
   - 접근 제어 및 권한 관리

3. **보안 정책 준수**:
   - 입력 유효성 검증 전략
   - 에러 메시지 노출 수준
   - 보안 로깅 전략

#### 3.4 성능 및 품질 검증 (quality-engineer 관점)
1. **성능 요구사항 검증**:
   - 응답 시간 및 처리량 목표 달성 가능성
   - 병목 지점 식별 및 최적화 방안
   - 캐싱 전략 및 리소스 관리
   - 페이지네이션/가상 스크롤 적용 여부

2. **테스트 가능성 평가** (`026-test-specification.md` 검증):
   - 단위 테스트 시나리오 완전성 (섹션 2)
   - E2E 테스트 시나리오 완전성 (섹션 3)
   - 테스트 데이터(Fixture) 충분성 (섹션 5)
   - data-testid 정의 여부 (섹션 6)
   - `025-traceability-matrix.md`와의 테스트 ID 매핑 일관성

3. **코드 품질 기준**:
   - SOLID 원칙 준수 여부
   - DRY, KISS, YAGNI 원칙 적용
   - TRD 코딩 표준 및 네이밍 컨벤션 준수

### 4단계: 기존 리뷰 문서 확인 (반복 실행 시)

```
리뷰 문서 넘버링:
├── 021-design-review-claude-1.md (1차 리뷰)
├── 021-design-review-claude-2.md (2차 리뷰)
├── 021-design-review-gemini-1.md (다른 LLM 1차)
└── ...
```

### 5단계: 리뷰 문서 생성

템플릿 참조: `@.jjiban/templates/021-design-review.md`

---

## 이슈 분류 기준

### 심각도(Severity) 분류
| 기호 | 심각도 | 설명 | 예시 |
|------|--------|------|------|
| **Critical** | 시스템 중단, 데이터 손실, 심각한 보안 이슈 | 인증 우회 가능, 데이터 무결성 파괴 |
| **High** | 핵심 기능 오류, 다수 사용자 영향, 보안 취약점 | API 권한 검증 누락, 중요 비즈니스 규칙 미구현 |
| **Medium** | 부분적 기능 제한, 성능 저하, 사용성 문제 | 페이지네이션 미적용, 에러 메시지 불명확 |
| **Low** | 경미한 불편, UI/문구 개선, 코드 품질 | 코드 중복, 네이밍 개선 필요 |
| **Info** | 개선 제안, 모범 사례 권장 | 최신 패턴 적용 제안, 문서화 보완 |

### 우선순위(Priority) 할당
| 기호 | 우선순위 | 설명 | 조치 기한 |
|------|----------|------|----------|
| **P1** | 즉시 해결 | 설계 결함, 심각한 보안 위험, 구현 불가능 | 구현 전 필수 수정 |
| **P2** | 빠른 해결 | 아키텍처 개선, 성능 문제, 테스트 불가능 | 구현 초기 수정 |
| **P3** | 보통 해결 | 코드 품질, 표준 미준수, 문서화 부족 | 구현 중 수정 |
| **P4** | 개선 항목 | 최적화 기회, 모범 사례 적용, 리팩토링 | 구현 후 검토 |
| **P5** | 참고 사항 | 참고용 정보, 향후 고려 사항 | 다음 iteration |

---

## 출력 예시

```
[wf:review] LLM 설계 리뷰 실행

Task: TSK-01-01-01
Category: development
현재 상태: [dd] 상세설계 (변경 없음)
리뷰어: claude
리뷰 회차: 1차

검증 대상:
├── 020-detail-design.md (상세설계 본문)
├── 025-traceability-matrix.md (추적성 매트릭스)
├── 026-test-specification.md (테스트 명세)
├── 010-basic-design.md
├── .jjiban/jjiban/prd.md
└── .jjiban/jjiban/trd.md

생성된 문서:
└── 021-design-review-claude-1.md

리뷰 요약:
┌──────────────────┬──────┬──────────────────────────────────┐
│ 검증 영역        │ 평가 │ 비고                             │
├──────────────────┼──────┼──────────────────────────────────┤
│ 문서 완전성      │ PASS │ 필수 섹션 모두 포함              │
│ 요구사항 추적성  │ PASS │ 6 FR, 6 BR 모두 매핑             │
│ 아키텍처         │ WARN │ 1건 개선 권장                    │
│ 보안             │ PASS │                                  │
│ 성능             │ PASS │                                  │
│ 테스트 가능성    │ PASS │ 26개 테스트케이스 정의           │
└──────────────────┴──────┴──────────────────────────────────┘

이슈 분포:
| 우선순위 | Critical | High | Medium | Low | Info | 합계 |
|----------|----------|------|--------|-----|------|------|
| P1       | 0        | 0    | 0      | 0   | 0    | 0    |
| P2       | 0        | 1    | 0      | 0   | 0    | 1    |
| P3       | 0        | 0    | 1      | 0   | 0    | 1    |
| P4       | 0        | 0    | 0      | 2   | 0    | 2    |
| P5       | 0        | 0    | 0      | 0   | 1    | 1    |
| 합계     | 0        | 1    | 1      | 2   | 1    | 5    |

강점:
- 요구사항 추적성 매트릭스가 상세하게 작성됨
- 테스트 계획이 구체적이고 실행 가능함
- API 계약이 명확하게 정의됨

개선 사항:
- [P2/High] 아키텍처: 외부 모듈 의존성 주입 전략 보완 필요
- [P3/Medium] 성능: 대량 데이터 조회 시 가상 스크롤 고려
- [P4/Low] 품질: 일부 컴포넌트 SRP 원칙 개선 여지
- [P4/Low] 품질: 에러 메시지 사용자 친화적 개선
- [P5/Info] 참고: 향후 캐싱 전략 적용 고려

다음 단계:
- 개선 반영: /wf:apply TSK-01-01-01
- 추가 리뷰: /wf:review TSK-01-01-01 --llm gemini
- 구현 진행: /wf:build TSK-01-01-01
```

## 반복 리뷰 사이클

```
[dd] 상세설계
      │
      ├── /wf:review ──┐
      │                │ (상태 변경 없음)
      │                │
      ├── /wf:apply ───┤ (설계서 수정)
      │                │
      └── /wf:review ──┘ (반복 가능)
      │
      └── /wf:build → [im] 구현
```

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development category만 지원합니다` |
| 잘못된 상태 | `[ERROR] 상세설계 상태가 아닙니다. 현재 상태: [상태]` |
| 상세설계 없음 | `[ERROR] 020-detail-design.md 파일이 없습니다` |
| 추적성 매트릭스 없음 | `[ERROR] 025-traceability-matrix.md 파일이 없습니다` |
| 테스트 명세 없음 | `[ERROR] 026-test-specification.md 파일이 없습니다` |
| 기본설계 없음 | `[WARN] 010-basic-design.md 파일이 없습니다. 리뷰 범위가 제한됩니다` |

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[dd]` 상태 Task들을 병렬로 리뷰합니다.

```
[wf:review] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
대상 Task: 12개 (상태 필터 적용: 5개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/5] TSK-01-01-01: Project CRUD 리뷰 ✅
├── [2/5] TSK-01-01-02: Project 대시보드 리뷰 ✅
├── [3/5] TSK-01-02-01: WP CRUD 리뷰 🔄 진행중
├── [4/5] TSK-01-02-02: WP 계층 구조 리뷰 ⏳ 대기
└── [5/5] TSK-01-03-01: Activity CRUD 리뷰 ⏳ 대기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 4개
├── 실패: 1개 (TSK-01-02-02: 상세설계 문서 없음)
└── 스킵: 0개

생성된 문서:
├── TSK-01-01-01/021-design-review-claude-1.md
├── TSK-01-01-02/021-design-review-claude-1.md
├── TSK-01-02-01/021-design-review-claude-1.md
└── TSK-01-03-01/021-design-review-claude-1.md

다음 단계: 개별 Task별 /wf:apply 또는 /wf:build 실행
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/wf:apply` | 리뷰 내용을 설계서에 반영 |
| `/wf:build` | 구현 시작 |

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:review
Version: 1.0

Changes (v1.0):
- 생성
-->
