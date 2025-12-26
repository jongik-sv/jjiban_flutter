---
name: wf:patch
description: "코드 리뷰 내용 반영 (최적화 버전)"
category: workflow
complexity: moderate
wave-enabled: false
performance-profile: optimized
hierarchy-input: true
parallel-processing: true
auto-flags:
  - --seq
  - --token-efficient
  - --validate
allowed-tools: [Read, Write, Edit, MultiEdit, Glob, Grep, Bash, Task]
mcp-servers: [sequential-thinking, context7]
personas: [refactoring-expert, backend-architect, quality-engineer]
---

# /wf:patch - 코드 리뷰 내용 반영 (v2)

> **최적화된 개선사항 적용**: Code Review에서 도출된 개선사항을 소스 코드 및 구현 문서에 체계적으로 적용하고 검증합니다.

> **상태 내 액션**: 상태 변경 없음, 반복 가능
> **사용 가능 상태**: `[im]` 구현 (development, infrastructure), `[fx]` 수정 (defect)
> **적용 category**: development, defect, infrastructure

## 최적화 목표

- **토큰 효율성**: 30% 토큰 절약
- **우선순위 기반**: Must → Should → Nice 순서의 선택적 적용
- **검증 중심**: 변경 사항의 회귀 테스트 자동화
- **에이전트 특화**: 도메인별 전문 에이전트 활용

## 사용법

```bash
# 기본 사용법 (최신 리뷰 문서 기준)
/wf:patch TSK-01-01-01              # 단일 Task

# 특정 리뷰 회차 지정
/wf:patch TSK-01-01-01 --review 2

# 우선순위 필터링
/wf:patch TSK-01-01-01 --priority must,should

# WP/ACT 단위 병렬 처리
/wf:patch ACT-01-01                 # Activity 내 모든 Task 병렬 처리
/wf:patch WP-01                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[im]` 구현, `[fx]` 수정 |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |
| `WP-XX` | WP 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |

## 동작 규칙

| category | 사용 가능 상태 | 상태 변경 | 수정 대상 |
|----------|--------------|----------|----------|
| development | `[im]` 구현 | 없음 (반복 가능) | 소스 코드, `030-implementation.md` |
| defect | `[fx]` 수정 | 없음 (반복 가능) | 소스 코드, `030-implementation.md` |
| infrastructure | `[im]` 구현 | 없음 (반복 가능) | 소스 코드, `030-implementation.md` |

## 문서 경로

@.claude/includes/wf-common.md

## 개념 충돌 해결

@.claude/includes/wf-conflict-resolution.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 자동 실행 플로우

### 1단계: Task 검증 및 컨텍스트 로드
**Auto-Persona**: refactoring-expert
**MCP**: sequential-thinking

**자동 실행 단계**:
1. **Task 정보 추출 및 파싱**:
   ```javascript
   // "/wf:patch TSK-01-01-01" 에서 Task ID 추출
   function parseTaskFromCommand(input) {
       const taskPattern = /TSK-(\d{2})-(\d{2})-(\d{2})/i;
       return input.match(taskPattern)?.[0]; // "TSK-01-01-01" 추출
   }
   ```

2. **WBS에서 Task 정보 조회**:
   - `.jjiban/projects/{project}/tasks/{TSK-ID}/task.json` 에서 Task 정보 조회
   - category 확인 (development | defect | infrastructure)
   - 현재 상태 확인: `[im]` 또는 `[fx]`

3. **Task 디렉토리 구조 확인**:
   ```
   .jjiban/projects/{project}/tasks/{TSK-ID}/
   ├── 010-basic-design.md (development만)
   ├── 020-detail-design.md
   ├── 030-implementation.md
   ├── 031-code-review-{llm}-{n}.md  ← 리뷰 문서
   └── test-results/
   ```

### 2단계: 코드 리뷰 문서 분석
**Auto-Persona**: quality-engineer
**MCP**: sequential-thinking

**자동 실행 단계**:
1. **리뷰 문서 탐색**:
   ```
   탐색 우선순위:
   1. "(적용완료)" 표시가 없는 리뷰 문서 중 최신 찾기 (기본)
   2. --review N 옵션 지정 시 해당 회차 문서 사용
   3. "(적용완료)" 파일은 탐색에서 제외

   파일 패턴 예시:
   ├── 031-code-review-claude-1(적용완료).md  ← 제외
   ├── 031-code-review-claude-2.md           ← 최신 (대상)
   └── 031-code-review-gemini-1(적용완료).md ← 제외
   ```

2. **우선순위별 이슈 분류**:
   ```markdown
   ## 3. 개선 사항 목록

   ### 3.1 필수 (Must Fix)      ← P1: 즉시 적용
   ### 3.2 권장 (Should Fix)    ← P2: 권장 적용
   ### 3.3 선택 (Nice to Have)  ← P3: 검토 후 적용
   ```

3. **적용 범위 결정**:
   - 코드 수정이 필요한 이슈 → 소스 파일 목록
   - 문서 수정이 필요한 이슈 → 설계/구현 문서
   - 테스트 추가가 필요한 이슈 → 테스트 파일

### 3단계: 코드 개선사항 적용 (Agent 위임)
**Auto-Persona**: backend-architect (API) / frontend-developer (UI)
**MCP**: context7, sequential-thinking

**자동 실행 단계**:
1. **Backend 코드 개선** (backend-architect 위임):
   - P1 보안 이슈 수정 (SQL injection, XSS 등)
   - 성능 최적화 코드 적용
   - 코딩 표준 준수 리팩토링
   - API 인터페이스 개선

2. **Frontend 코드 개선** (필요시):
   - UI/UX 개선사항 적용
   - 컴포넌트 구조 개선
   - 타입 정의 보완

3. **테스트 코드 개선** (quality-engineer):
   - 누락된 테스트 케이스 추가
   - 예외 상황 테스트 강화
   - 테스트 커버리지 향상

**수정 체크리스트**:
- [ ] 필수(Must Fix) 항목 전부 반영
- [ ] 권장(Should Fix) 항목 검토 및 반영
- [ ] 선택(Nice to Have) 항목 검토
- [ ] 기존 테스트 통과 확인

### 4단계: 테스트 재실행 및 검증
**Auto-Persona**: quality-engineer
**MCP**: sequential-thinking

**자동 실행 단계**:
1. **단위 테스트 실행**:
   ```bash
   # API 테스트
   cd api && npm run test -- --run

   # Web 테스트 (해당 시)
   cd web && npm run test -- --run
   ```

2. **회귀 테스트 확인**:
   - 수정된 코드에 대한 기존 테스트 통과 확인
   - 새 테스트 추가 (필요시)

3. **코드 품질 검증**:
   - 정적 분석 통과 확인
   - 타입 체크 통과 확인

### 5단계: 구현 문서 업데이트
**Auto-Persona**: technical-writer
**MCP**: sequential-thinking

**자동 실행 단계**:
1. **구현 문서에 리뷰 반영 이력 추가**:
   ```markdown
   ## X. 코드 리뷰 반영 이력

   ### 반영 일시: 2026-12-08
   ### 기준 리뷰: 031-code-review-claude-1.md

   | # | 항목 | 유형 | 파일 | 상태 |
   |---|------|------|------|------|
   | 1 | [항목1] | Must | [파일] | ✅ 반영 |
   | 2 | [항목2] | Should | [파일] | ✅ 반영 |
   | 3 | [항목3] | Nice | [파일] | ⏭️ 스킵 |

   ### 미반영 사항 (사유 포함)
   | # | 항목 | 유형 | 사유 |
   |---|------|------|------|
   | 1 | [항목3] | Nice | 현재 범위 외 |
   ```

2. **변경 사항 요약 업데이트**:
   - 수정된 파일 목록
   - 주요 변경 내용
   - 테스트 결과

### 6단계: 리뷰 문서 적용완료 처리
**Auto-Persona**: technical-writer

**자동 실행 단계**:
1. **리뷰 문서에 "(적용완료)" 표시 추가**:
   ```
   변경 전: 031-code-review-claude-1.md
   변경 후: 031-code-review-claude-1(적용완료).md
   ```

2. **파일 이름 변경 수행**:
   ```bash
   # 예시
   mv "031-code-review-claude-1.md" "031-code-review-claude-1(적용완료).md"
   ```

3. **적용완료 처리 목적**:
   - 동일 리뷰 문서 재적용 방지
   - 다음 /wf:patch 실행 시 자동 제외
   - 리뷰-패치 이력 추적 용이

### 7단계: 적용 결과 보고
**Auto-Persona**: technical-writer

**출력 형식**:
```
[wf:patch] 코드 리뷰 내용 반영 완료

Task: TSK-01-01-01
Category: development
현재 상태: [im] 구현 (변경 없음)

📋 기준 리뷰 문서: 031-code-review-claude-1.md

✅ 개선 사항 반영:
├── [Must]   1/1 반영 완료
├── [Should] 2/2 반영 완료
└── [Nice]   0/1 스킵 (사유: 현재 범위 외)

📁 수정된 파일:
├── api/src/modules/project/project.service.ts
├── api/src/modules/project/project.controller.ts
└── api/src/modules/project/__tests__/project.service.spec.ts

🧪 테스트 결과:
├── 단위 테스트: 18/18 통과 ✅
└── 타입 체크: 통과 ✅

📄 업데이트된 문서:
└── 030-implementation.md (코드 리뷰 반영 이력 추가)

🔄 다음 단계:
├── 재리뷰: /wf:audit TSK-01-01-01
└── 통합테스트: /wf:verify TSK-01-01-01
```

---

## 적용 기준 가이드

### 우선순위별 적용 원칙

| 우선순위 | 분류 | 적용 원칙 | 예시 |
|---------|------|----------|------|
| **P1** | Must Fix | 반드시 적용, 즉시 수정 | 보안 취약점, 치명적 버그 |
| **P2** | Should Fix | 적용 권장, 릴리즈 전 수정 | 성능 이슈, 코드 품질 |
| **P3** | Nice to Have | 선택적 적용, 리소스 여유 시 | 코딩 스타일, 문서화 |

### 변경 영향도 평가

| 영향도 | 설명 | 검증 수준 |
|-------|------|----------|
| **High** | 아키텍처/핵심 로직 변경 | 전체 테스트 + 수동 검증 |
| **Medium** | 기능 수정/인터페이스 변경 | 관련 테스트 실행 |
| **Low** | 코딩 스타일/주석 수정 | 기본 테스트만 |

---

## 반복 리뷰-패치 사이클

```
[im] 구현 (development/infrastructure)
[fx] 수정 (defect)
      │
      ├── /wf:audit ───→ {nn}-code-review-{llm}-{n}.md
      │                          │
      │                          ▼
      ├── /wf:patch ────→ 소스 코드 수정
      │                          │
      │                          ▼
      │                  리뷰 문서 "(적용완료)" 처리
      │                          │
      │                          ▼
      ├── /wf:audit ───→ {nn}-code-review-{llm}-{n+1}.md
      │                          │
      └── (품질 만족까지 반복) ───┘
      │
      ├── /wf:verify → [ts] 통합테스트 (development, defect)
      └── /wf:done → [xx] 완료 (infrastructure)
```

---

## 에러 케이스

| 에러 | 메시지 | 해결 방법 |
|------|--------|----------|
| 잘못된 상태 (dev) | `[ERROR] 구현 상태가 아닙니다. 현재 상태: [상태]` | /wf:build 먼저 실행 |
| 잘못된 상태 (defect) | `[ERROR] 수정 상태가 아닙니다. 현재 상태: [상태]` | /wf:analyze 먼저 실행 |
| 리뷰 문서 없음 | `[ERROR] 코드 리뷰 문서가 없습니다` | /wf:audit 먼저 실행 |
| 미적용 리뷰 없음 | `[ERROR] 적용 가능한 리뷰 문서가 없습니다 (모두 적용완료)` | /wf:audit로 새 리뷰 생성 |
| 이미 적용된 리뷰 | `[ERROR] 지정된 리뷰([N])는 이미 적용완료된 문서입니다` | 다른 리뷰 회차 지정 또는 새 리뷰 생성 |
| 리뷰 회차 없음 | `[ERROR] 지정된 리뷰 회차([N])가 존재하지 않습니다` | 올바른 회차 지정 |
| 테스트 실패 | `[ERROR] 테스트가 통과하지 않았습니다 ([N]건 실패)` | 테스트 실패 원인 수정 |

---

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[im]`/`[fx]` 상태 Task들에 코드 리뷰 내용을 병렬로 반영합니다.

```
[wf:patch] 워크플로우 시작 (병렬 처리)

입력: ACT-01-02 (Activity)
범위: Work Package 관리 기능
대상 Task: 4개 (상태 필터 적용: 3개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/3] TSK-01-02-01: WP CRUD 패치 ✅
├── [2/3] TSK-01-02-02: WP 계층 구조 패치 ✅
└── [3/3] TSK-01-02-03: WP 상태 관리 패치 🔄 진행중

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 3개
├── 실패: 0개
└── 스킵: 1개 (TSK-01-02-04: 리뷰 문서 없음)

수정된 파일:
├── api/src/modules/work-package/...
├── web/components/work-package/...
└── 각 Task의 030-implementation.md

다음 단계: 개별 Task별 /wf:verify 실행
```

---

## 관련 명령어

| 명령어 | 설명 | 사용 시점 |
|--------|------|----------|
| `/wf:audit` | LLM 코드 리뷰 실행 | 리뷰 문서 생성 필요 시 |
| `/wf:patch` | 리뷰 내용 반영 (현재) | 리뷰 후 수정 적용 시 |
| `/wf:verify` | 통합테스트 시작 | 리뷰-패치 사이클 완료 후 |
| `/wf:done` | 작업 완료 | infrastructure 완료 시 |

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:patch
Version: 1.0

Changes (v1.0):
- 생성
-->
