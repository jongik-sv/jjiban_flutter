---
name: wf:audit
description: "LLM 코드 리뷰 실행. 상태 변경 없음, 반복 가능"
category: workflow
complexity: enhanced
performance-profile: optimized
hierarchy-input: true
parallel-processing: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
auto-flags:
  - --token-efficient
mcp-servers: [context7]
personas: [system-architect, security-engineer, quality-engineer]
---

# /wf:audit - LLM 코드 리뷰 (v2.1)

> **최적화된 코드 리뷰**: 다중 LLM을 활용한 설계-구현 일관성 검증을 통해 불일치성을 분석하고 개선 제안을 제공합니다.

## 🎯 최적화 목표

- **토큰 효율성**: 30% 토큰 절약
- **다중 LLM 활용**: 다른 LLM 결과와 분리 유지 (Claude, Gemini, Codex)
- **체계적 검증**: 우선순위 기반 이슈 분류
- **실행 가능성**: 구체적이고 실행 가능한 개선 제안

## 워크플로우 위치

> **상태 내 액션**: 상태 변경 없음, 반복 가능
> **사용 가능 상태**: `[im]` 구현 (development, infrastructure), `[fx]` 수정 (defect)
> **적용 category**: development, defect, infrastructure

## 사용법

```bash
/wf:audit [WP-ID | ACT-ID | Task-ID] [--llm claude|gemini|codex]

# 예시
/wf:audit TSK-01-01-01              # 단일 Task
/wf:audit TSK-01-01-01 --llm gemini # 특정 LLM으로 코드 리뷰
/wf:audit ACT-01-01                 # Activity 내 모든 Task 병렬 처리
/wf:audit WP-01                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[im]` 구현, `[fx]` 수정 |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |
| `WP-XX` | WP 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |

## 동작 규칙

| category | 사용 가능 상태 | 상태 변경 | 생성 문서 |
|----------|--------------|----------|----------|
| development | `[im]` 구현 | 없음 (반복 가능) | `031-code-review-{llm}-{n}.md` |
| defect | `[fx]` 수정 | 없음 (반복 가능) | `031-code-review-{llm}-{n}.md` |
| infrastructure | `[im]` 구현 | 없음 (반복 가능) | `031-code-review-{llm}-{n}.md` |

## 문서 경로

@.claude/includes/wf-common.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 자동 실행 플로우

### 1단계: Task 검증 및 문서 수집
**Auto-Persona**: system-architect

**자동 실행 단계**:
1. **Task 정보 추출 및 파싱**:
   ```javascript
   // "/wf:audit TSK-01-01-01"에서 Task ID 추출
   function parseTaskFromCommand(input) {
       const taskPattern = /TSK-(\d{2})-(\d{2})-(\d{2})/i;
       return input.match(taskPattern)?.[0];
   }
   ```

2. **WBS에서 Task 조회**:
   - `.jjiban/projects/{project}/tasks/{TSK-ID}/task.json`에서 Task 정보 조회
   - category 확인: development | defect | infrastructure
   - 현재 상태 확인:
     - development: `[im]` 구현
     - defect: `[fx]` 수정
     - infrastructure: `[im]` 구현

3. **관련 문서 자동 수집**:
   - 상세설계 문서 (development, 분할 문서):
     - `020-detail-design.md` (상세설계 본문)
     - `025-traceability-matrix.md` (추적성 매트릭스)
     - `026-test-specification.md` (테스트 명세)
   - 분석 문서: `010-analysis.md` (defect)
   - 구현 문서: `030-implementation.md` (development/infrastructure)
   - 테스트 결과 (있는 경우)
   - 소스 코드 분석

### 2단계: 소스 코드 분석 및 매핑
**Auto-Persona**: system-architect
**MCP**: context7

**자동 실행 단계**:
1. **구현된 소스 코드 분석**:
   - Backend API 구조 및 로직 분석
   - Frontend 화면 구성 및 연동 분석
   - 데이터베이스 스키마 및 관계 분석

2. **설계 대비 구현 매핑**:
   - 상세설계서의 요구사항 vs 실제 구현
   - API 명세 vs 구현된 엔드포인트
   - 화면 설계 vs 구현된 UI
   - 데이터 모델 vs 데이터베이스 스키마

3. **Context7 활용** (선택):
   - 사용된 라이브러리/프레임워크 문서 조회
   - 최신 베스트 프랙티스 확인

### 3단계: 일관성 검증 및 이슈 도출
**Auto-Persona**: system-architect + security-engineer + quality-engineer
**권장 LLM**: Claude 대신 Gemini, GPT 등 다른 LLM 활용

**자동 실행 단계**:

#### 3.1 설계-구현 일관성 검증
- 기능적 요구사항 충족도 검증
- 비기능적 요구사항 (성능, 보안) 검증
- 인터페이스 설계 일관성 검증

#### 3.2 코드 품질 및 보안 검증
- 코딩 표준 및 패턴 준수 검증
- 보안 취약점 및 리스크 분석 (XSS, SQL Injection, CSRF 등)
- 성능 최적화 가능성 분석 (N+1 쿼리, 불필요한 렌더링 등)

#### 3.3 테스트 커버리지 및 품질 검증
- 테스트 케이스 완전성 검증
- 예외 처리 및 경계 조건 검증
- 사용성 및 접근성 검증

#### 3.4 심각도(Severity) 분류
| 심각도 | 아이콘 | 설명 |
|--------|--------|------|
| Critical | ⚠️ | 시스템 전체 중단, 데이터 손실, 보안 이슈 |
| High | ❗ | 핵심 기능 오류, 다수 사용자 영향 |
| Medium | 🔧 | 부분적 기능 제한, 사용성 저하 |
| Low | 📝 | 경미한 불편, UI/문구/미관 문제 |
| Info | ℹ️ | 기타 문제, 경고 수준 |

#### 3.5 우선순위(Priority) 할당
| 우선순위 | 아이콘 | 설명 |
|----------|--------|------|
| P1 | 🔴 | 즉시 해결: 운영 차질, 고객 불만 폭주, 보안 위협 |
| P2 | 🟠 | 빠른 해결: 주요 기능 저하, 다수 사용자 영향 |
| P3 | 🟡 | 보통 해결: 단기적 우회 가능, 영향 제한적 |
| P4 | 🟢 | 개선 항목: 장기 개선, 경미한 사항 |
| P5 | 🔵 | 보류 항목: 보류 항목 |

#### 3.6 매트릭스 기반 분류
심각도와 우선순위를 조합한 종합 평가 수행

### 4단계: 기존 리뷰 문서 확인 (반복 실행 시)

```
리뷰 문서 넘버링:
├── 031-code-review-claude-1(적용완료).md  ← 적용 완료 (넘버링 제외)
├── 031-code-review-claude-2.md           ← 2차 리뷰 (현재 최신)
├── 031-code-review-gemini-1(적용완료).md ← 적용 완료 (넘버링 제외)
└── 031-code-review-gemini-2.md           ← 다른 LLM 2차

넘버링 규칙:
- "(적용완료)" 파일은 넘버링 계산에서 제외
- 새 리뷰 생성 시 해당 LLM의 미적용 리뷰 수 + 1
```

### 5단계: 코드 리뷰 보고서 생성
**Auto-Persona**: technical-writer

**자동 실행 단계**:
1. **검증 결과 종합**:
   - 발견된 이슈 목록 정리
   - 우선순위 분류 (P1: 치명적 → P5: 개선)
   - 영향도 및 해결 난이도 평가

2. **개선사항 제안**:
   - 구체적이고 실행 가능한 해결 방안
   - 코드 예시 또는 설계 변경사항 포함
   - 비용-효과 분석

3. **보고서 작성**: 아래 템플릿에 따라 작성

---

## 코드 리뷰 보고서 템플릿

**파일명**: `{nn}-code-review-{llm}-{n}.md`

```markdown
# 코드 리뷰: [Task명]

## 리뷰 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | [category] |
| 리뷰 일시 | [YYYY-MM-DD HH:mm] |
| 리뷰어 | [LLM명] |
| 리뷰 회차 | [N]차 |

---

## 1. 리뷰 요약

### 1.1 전체 평가
| 항목 | 평가 | 심각도 | 우선순위 | 비고 |
|------|------|--------|---------|------|
| 설계 일치성 | ✅/⚠️/❌ | - | - | |
| 코드 품질 | ✅/⚠️/❌ | - | - | |
| 보안 | ✅/⚠️/❌ | - | - | |
| 성능 | ✅/⚠️/❌ | - | - | |
| 테스트 | ✅/⚠️/❌ | - | - | |

### 1.2 이슈 통계
| 심각도 | 개수 |
|--------|------|
| ⚠️ Critical | 0 |
| ❗ High | 0 |
| 🔧 Medium | 0 |
| 📝 Low | 0 |
| ℹ️ Info | 0 |

### 1.3 종합 의견
[전반적인 구현 품질 평가]

---

## 2. 상세 리뷰

### 2.1 설계-구현 일치성
**검증 범위**: [검증 대상 문서 및 코드]

| 설계 항목 | 구현 상태 | 일치 여부 | 비고 |
|-----------|----------|----------|------|
| | | ✅/❌ | |

**분석 결과**:
[설계와 구현의 일치 여부 분석]

### 2.2 코드 품질
**검토 기준**: SOLID, Clean Code, 프로젝트 코딩 표준

| 원칙 | 준수 여부 | 위반 사례 |
|------|----------|----------|
| SRP (단일 책임) | ✅/❌ | |
| OCP (개방-폐쇄) | ✅/❌ | |
| DRY (중복 제거) | ✅/❌ | |
| 네이밍 규칙 | ✅/❌ | |

**분석 결과**:
[코드 품질 분석: 가독성, 유지보수성, SOLID 원칙 등]

### 2.3 보안 검토
**검토 항목**: OWASP Top 10 기준

| 취약점 유형 | 검토 결과 | 발견 위치 |
|-------------|----------|----------|
| XSS | ✅/❌ | |
| SQL Injection | ✅/❌ | |
| CSRF | ✅/❌ | |
| 인증/인가 | ✅/❌ | |
| 민감정보 노출 | ✅/❌ | |

**분석 결과**:
[보안 취약점 분석]

### 2.4 성능 검토
**검토 항목**: 쿼리 최적화, 렌더링 성능, 리소스 사용

| 성능 항목 | 검토 결과 | 개선 필요 |
|-----------|----------|----------|
| N+1 쿼리 | ✅/❌ | |
| 불필요한 렌더링 | ✅/❌ | |
| 메모리 누수 | ✅/❌ | |
| API 응답 시간 | ✅/❌ | |

**분석 결과**:
[성능 이슈 분석]

### 2.5 테스트 검토
**검토 항목**: 테스트 커버리지, 테스트 품질

| 테스트 항목 | 상태 | 커버리지 |
|-------------|------|---------|
| 단위 테스트 | ✅/❌ | % |
| 통합 테스트 | ✅/❌ | % |
| E2E 테스트 | ✅/❌ | % |

**분석 결과**:
[테스트 커버리지 및 품질 분석]

---

## 3. 개선 사항 목록

### 3.1 🔴 P1 - 즉시 해결 (Must Fix)
| # | 심각도 | 파일 | 라인 | 설명 | 해결 방안 |
|---|--------|------|------|------|----------|
| 1 | ⚠️ | | | | |

### 3.2 🟠 P2 - 빠른 해결 (Should Fix)
| # | 심각도 | 파일 | 라인 | 설명 | 해결 방안 |
|---|--------|------|------|------|----------|
| 1 | ❗ | | | | |

### 3.3 🟡 P3 - 보통 해결 (Could Fix)
| # | 심각도 | 파일 | 라인 | 설명 | 해결 방안 |
|---|--------|------|------|------|----------|
| 1 | 🔧 | | | | |

### 3.4 🟢 P4 - 개선 항목 (Nice to Have)
| # | 심각도 | 파일 | 라인 | 설명 | 해결 방안 |
|---|--------|------|------|------|----------|
| 1 | 📝 | | | | |

### 3.5 🔵 P5 - 보류 항목 (Backlog)
| # | 심각도 | 파일 | 라인 | 설명 | 비고 |
|---|--------|------|------|------|------|
| 1 | ℹ️ | | | | |

---

## 4. 코드 개선 예시

### 4.1 [이슈 제목]
**현재 코드**:
```[language]
// 문제가 있는 코드
```

**개선 코드**:
```[language]
// 개선된 코드
```

**개선 이유**: [설명]

---

## 5. 다음 단계

- 개선 사항 반영: `/wf:patch [Task-ID]` → 코드 수정
- 추가 리뷰: `/wf:audit [Task-ID]` → 재리뷰
- 다음 워크플로우:
  - development: `/wf:verify [Task-ID]` → 통합테스트
  - defect: `/wf:verify [Task-ID]` → 테스트
  - infrastructure: `/wf:done [Task-ID]` → 완료


---

## 🎯 최적화 특징

### 🔍 다중 LLM 교차 검증
- Claude 외 Gemini, Codex 등 다른 LLM 활용 권장
- 각 LLM의 강점을 활용한 검증 관점 다양화
- 편향 방지 및 객관성 확보

### 📊 체계적 이슈 분류
- P1-P5 우선순위 기반 이슈 관리
- 심각도(Severity)와 우선순위(Priority) 매트릭스 적용
- 실행 가능성 중심의 개선안 제시

### ⚡ 토큰 효율성
- Context7 MCP로 최신 라이브러리 문서 참조
- 구조화된 분석 템플릿 활용
- 중요 이슈 중심의 집중 분석

---

## 출력 예시

```
[wf:audit] LLM 코드 리뷰 실행

Task: TSK-01-01-01
Category: development
현재 상태: [im] 구현 (변경 없음)
리뷰어: claude

생성된 문서:
└── 031-code-review-claude-1.md

리뷰 요약:
┌─────────────┬────────┬──────────┬──────────┐
│ 항목        │ 평가   │ 심각도   │ 우선순위 │
├─────────────┼────────┼──────────┼──────────┤
│ 설계 일치성 │ ✅     │ -        │ -        │
│ 코드 품질   │ ⚠️     │ Medium   │ P3       │
│ 보안        │ ✅     │ -        │ -        │
│ 성능        │ ⚠️     │ High     │ P2       │
│ 테스트      │ ✅     │ -        │ -        │
└─────────────┴────────┴──────────┴──────────┘

이슈 통계:
- ⚠️ Critical: 0건
- ❗ High: 1건
- 🔧 Medium: 2건
- 📝 Low: 1건

다음 단계:
- 개선 반영: /wf:patch TSK-01-01-01
- 통합테스트: /wf:verify TSK-01-01-01
```

---

## 반복 리뷰-패치 사이클

```
[im] 구현 (development/infrastructure)
[fx] 수정 (defect)
      │
      ├── /wf:audit ──┐
      │               │ (상태 변경 없음)
      │               │
      ├── /wf:patch ──┤ (코드 수정)
      │               │
      └── /wf:audit ──┘ (반복 가능)
      │
      ├── /wf:verify → [ts] 통합테스트 (development, defect)
      └── /wf:done → [xx] 완료 (infrastructure)
```

---

## 코드 리뷰 품질 기준

| 기준 | 목표 | 설명 |
|------|------|------|
| 커버리지 | 90%+ | 설계서 요구사항 검증 비율 |
| 정확성 | 100% | 실제 소스 코드 기반 분석 |
| 실행 가능성 | 100% | 구체적 개선 방안 포함 |
| 우선순위 | P1-P2 필수 | P1-P2 이슈는 반드시 해결 권장 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 상태 (dev) | `[ERROR] 구현 상태가 아닙니다. 현재 상태: [상태]` |
| 잘못된 상태 (defect) | `[ERROR] 수정 상태가 아닙니다. 현재 상태: [상태]` |
| 구현 문서 없음 | `[ERROR] 구현 문서가 없습니다` |
| Task 미발견 | `[ERROR] WBS에서 Task를 찾을 수 없습니다: [Task-ID]` |

---

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[im]`/`[fx]` 상태 Task들을 병렬로 코드 리뷰합니다.

```
[wf:audit] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
대상 Task: 12개 (상태 필터 적용: 6개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/6] TSK-01-01-01: Project CRUD 코드리뷰 ✅
├── [2/6] TSK-01-01-02: Project 대시보드 코드리뷰 ✅
├── [3/6] TSK-01-02-01: WP CRUD 코드리뷰 🔄 진행중
├── [4/6] TSK-01-02-02: WP 계층 구조 코드리뷰 ⏳ 대기
├── [5/6] TSK-01-03-01: Activity CRUD 코드리뷰 ⏳ 대기
└── [6/6] TSK-01-03-02: Activity 관계 관리 코드리뷰 ⏳ 대기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 5개
├── 실패: 1개 (TSK-01-02-02: 구현 문서 없음)
└── 스킵: 0개

생성된 문서:
├── TSK-01-01-01/031-code-review-claude-1.md
├── TSK-01-01-02/031-code-review-claude-1.md
├── TSK-01-02-01/031-code-review-claude-1.md
├── TSK-01-03-01/031-code-review-claude-1.md
└── TSK-01-03-02/031-code-review-claude-1.md

다음 단계: 개별 Task별 /wf:patch 또는 /wf:verify 실행
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/wf:patch` | 코드 리뷰 내용 반영 |
| `/wf:verify` | 통합테스트 시작 (development, defect) |
| `/wf:done` | 작업 완료 (infrastructure) |

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:audit
Version: 1.0

Changes (v1.0):
- 생성
-->
