---
name: wf:done
description: "작업 최종 완료. 매뉴얼 작성 및 마무리"
category: workflow
hierarchy-input: true
parallel-processing: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

# /wf:done - 작업 최종 완료

> **상태 전환**: `[vf] 검증` → `[xx] 완료` (development, defect)
> **상태 전환**: `[im] 구현` → `[xx] 완료` (infrastructure)
> **적용 category**: development, defect, infrastructure

## 사용법

```bash
/wf:done [WP-ID | ACT-ID | Task-ID]

# 예시
/wf:done TSK-01-01-01              # 단일 Task
/wf:done ACT-01-01                 # Activity 내 모든 Task 병렬 처리
/wf:done WP-01                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[vf]` 검증, `[im]` 구현 |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[vf]`, `[im]` 상태만 |
| `WP-XX` | WP 내 Task 병렬 처리 | `[vf]`, `[im]` 상태만 |

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 생성 문서 |
|----------|----------|----------|----------|
| development | `[vf]` 검증 | `[xx]` 완료 | `080-manual.md` |
| defect | `[vf]` 검증 | `[xx]` 완료 | - |
| infrastructure | `[im]` 구현 | `[xx]` 완료 | - |

## 문서 경로

@.claude/includes/wf-common.md

## 개념 충돌 해결

@.claude/includes/wf-conflict-resolution.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 실행 과정

### 1단계: Task 검증
1. WBS에서 Task 찾기
2. category 확인 및 현재 상태 검증:
   - development, defect: `[vf]` 검증 상태인지 확인
   - infrastructure: `[im]` 구현 상태인지 확인

### 2단계: 완료 체크리스트 검증

**development 체크리스트**:
- [ ] 기본설계 완성 (`010-basic-design.md`)
- [ ] 상세설계 완성 (분할 문서):
  - `020-detail-design.md` (상세설계 본문)
  - `025-traceability-matrix.md` (추적성 매트릭스)
  - `026-test-specification.md` (테스트 명세)
- [ ] 설계리뷰 완료 (`021-design-review-*.md`)
- [ ] 구현 완료 (`030-implementation.md`)
- [ ] 코드리뷰 완료 (`031-code-review-*.md`)
- [ ] 통합테스트 완료 (`070-integration-test.md`)

**defect 체크리스트**:
- [ ] 결함 분석 완료 (`010-analysis.md`)
- [ ] 구현 완료 (`030-implementation.md`)
- [ ] 코드리뷰 완료 (`031-code-review-*.md`)
- [ ] 테스트 완료 (`070-test-results.md`)

**infrastructure 체크리스트**:
- [ ] 설계 완료 (`010-tech-design.md`, 선택)
- [ ] 구현 완료 (`030-implementation.md`)
- [ ] 코드리뷰 완료 (`031-code-review-*.md`)

### 3단계: 매뉴얼 작성 (development만)

**080-manual.md 템플릿**:
```markdown
# 사용자 매뉴얼: [Task명]

## 문서 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| 작성일 | [오늘 날짜] |
| 버전 | 1.0 |

---

## 1. 개요

### 1.1 기능 소개
[기능에 대한 간략한 설명]

### 1.2 대상 사용자
[이 기능을 사용할 사용자 유형]

---

## 2. 시작하기

### 2.1 사전 요구사항
- 요구사항 1
- 요구사항 2

### 2.2 접근 방법
[기능에 접근하는 방법]

---

## 3. 사용 방법

### 3.1 기본 사용법
1. 단계 1
2. 단계 2
3. 단계 3

### 3.2 상세 기능

#### 기능 1: [기능명]
[기능 설명 및 사용법]

**화면 예시**:
[스크린샷 또는 설명]

#### 기능 2: [기능명]
[기능 설명 및 사용법]

---

## 4. 자주 묻는 질문 (FAQ)

### Q1: [질문]
**A**: [답변]

### Q2: [질문]
**A**: [답변]

---

## 5. 문제 해결

### 5.1 일반적인 문제

#### 문제: [문제 설명]
**원인**: [원인]
**해결 방법**: [해결 방법]

---

## 6. 참고 자료
- [관련 문서 1]
- [관련 문서 2]
```

### 4단계: 완료 보고서 생성

**Task 완료 요약** (콘솔 출력):
```
═══════════════════════════════════════════════════════
              Task 완료 보고서
═══════════════════════════════════════════════════════

Task ID: [Task-ID]
Task명: [Task명]
Category: [category]

───────────────────────────────────────────────────────
                    워크플로우 이력
───────────────────────────────────────────────────────

| 단계 | 상태 | 완료일 |
|------|------|--------|
| 시작 | [ ] → [bd] | [날짜] |
| 기본설계 | [bd] → [dd] | [날짜] |
| 상세설계 | [dd] → [dr] | [날짜] |
| 설계리뷰 | [dr] (2회) | [날짜] |
| 구현 | [im] → [cr] | [날짜] |
| 코드리뷰 | [cr] (1회) | [날짜] |
| 통합테스트 | [ts] → [xx] | [날짜] |
| 완료 | [xx] | [날짜] |

───────────────────────────────────────────────────────
                    산출물 목록
───────────────────────────────────────────────────────

| 문서 | 경로 |
|------|------|
| 기본설계 | [경로]/010-basic-design.md |
| 상세설계 본문 | [경로]/020-detail-design.md |
| 추적성 매트릭스 | [경로]/025-traceability-matrix.md |
| 테스트 명세 | [경로]/026-test-specification.md |
| 설계리뷰 | [경로]/021-design-review-*.md |
| 구현 | [경로]/030-implementation.md |
| 코드리뷰 | [경로]/031-code-review-*.md |
| 통합테스트 | [경로]/070-integration-test.md |
| 매뉴얼 | [경로]/080-manual.md |

───────────────────────────────────────────────────────
                    품질 메트릭
───────────────────────────────────────────────────────

| 항목 | 값 |
|------|-----|
| 설계리뷰 횟수 | [N]회 |
| 코드리뷰 횟수 | [N]회 |
| 테스트 커버리지 | [N]% |
| 통합테스트 통과율 | [N]% |

═══════════════════════════════════════════════════════
              Task [Task-ID] 완료
═══════════════════════════════════════════════════════
```

### 5단계: WBS 상태 전환 및 업데이트
1. 상태 전환:
   - development, defect: `[vf]` → `[xx]`
   - infrastructure: `[im]` → `[xx]`
2. 완료일 기록
3. WBS 파일 저장

## 출력 예시

```
[wf:done] 작업 최종 완료

Task: TSK-01-01-01
Task명: Project CRUD 구현
Category: development

워크플로우 완료:
✅ [ ] Todo
✅ [bd] 기본설계
✅ [dd] 상세설계
✅ [dr] 설계리뷰 (2회)
✅ [im] 구현
✅ [cr] 코드리뷰 (1회)
✅ [ts] 통합테스트
✅ [xx] 완료

생성된 문서:
└── 080-manual.md

품질 메트릭:
- 테스트 커버리지: 87%
- 통합테스트 통과율: 100%

═══════════════════════════════════════
Task TSK-01-01-01 완료
═══════════════════════════════════════
```

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 상태 (dev/defect) | `[ERROR] 검증 상태가 아닙니다. 현재 상태: [상태]` |
| 잘못된 상태 (infra) | `[ERROR] 구현 상태가 아닙니다. 현재 상태: [상태]` |
| 미완료 항목 | `[WARNING] 일부 문서가 없습니다: [문서목록]` |

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[vf]`/`[im]` 상태 Task들의 완료 처리를 병렬로 실행합니다.

```
[wf:done] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
대상 Task: 12개 (상태 필터 [vf]/[im] 적용: 10개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/10] TSK-01-01-01: Project CRUD 완료 ✅
├── [2/10] TSK-01-01-02: Project 대시보드 완료 ✅
├── [3/10] TSK-01-02-01: WP CRUD 완료 🔄 진행중
├── [4/10] TSK-01-02-02: WP 계층 구조 완료 ⏳ 대기
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 10개
├── 실패: 0개
└── 스킵: 2개 ([vf]/[im] 상태 아님)

상태 전환:
├── TSK-01-01-01: [vf] → [xx] ✅
├── TSK-01-01-02: [vf] → [xx] ✅
├── TSK-01-02-01: [im] → [xx] ✅ (infrastructure)
└── ...

생성된 문서 (development만):
├── TSK-01-01-01/080-manual.md
├── TSK-01-01-02/080-manual.md
└── ...

📈 WP-01 완료 통계:
├── 총 Task: 12개
├── 완료: 10개 (83.3%)
└── 진행중: 2개

다음 단계: WP-01 전체 완료 보고서 확인
```

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:done
Version: 1.0

Changes (v1.0):
- 생성
-->
