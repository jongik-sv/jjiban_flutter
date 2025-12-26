---
name: wf:skip
description: "infrastructure Task 설계 생략. Todo → 구현 직접 전환"
category: workflow
hierarchy-input: true
parallel-processing: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

# /wf:skip - 설계 생략 및 구현 시작

> **상태 전환**: `[ ] Todo` → `[im] 구현` (설계 단계 생략)
> **적용 category**: infrastructure only

## 사용법

```bash
/wf:skip [WP-ID | ACT-ID | Task-ID]

# 예시
/wf:skip TSK-03-01-01              # 단일 Task
/wf:skip ACT-03-01                 # Activity 내 모든 Task 병렬 처리
/wf:skip WP-03                     # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[ ]` Todo (infrastructure만) |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[ ]` + infrastructure |
| `WP-XX` | WP 내 Task 병렬 처리 | `[ ]` + infrastructure |

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 액션 |
|----------|----------|----------|------|
| infrastructure | `[ ]` Todo | `[im]` 구현 | 설계 생략, 직접 구현 |

## 설계 생략 조건

**생략 가능한 경우**:
- 단순 설정 변경
- 명확한 리팩토링 작업
- 버전 업그레이드
- 문서화 작업
- 코드 스타일 수정

**설계 필요한 경우** (생략 불가):
- 아키텍처 변경
- 성능 최적화 (복잡한 경우)
- 보안 관련 변경
- 마이그레이션 작업
- 외부 시스템 연동

## 문서 경로

@.claude/includes/wf-common.md

## 개념 충돌 해결

@.claude/includes/wf-conflict-resolution.md

**Task 폴더**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

---

## 실행 과정

### 1단계: Task 검증
1. WBS에서 Task 찾기
2. category가 `infrastructure`인지 확인
3. 현재 상태가 `[ ]` Todo인지 확인

### 2단계: 생략 타당성 확인

**생략 확인 질문**:
1. 이 작업은 아키텍처 변경을 포함하는가?
2. 복잡한 마이그레이션이 필요한가?
3. 다른 시스템에 영향을 미치는가?

→ 모두 "아니오"인 경우 생략 가능

### 3단계: 구현 문서 초기화

**030-implementation.md 초기 템플릿**:
```markdown
# 구현 문서: [Task명]

## 구현 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | infrastructure |
| 구현 일시 | [오늘 날짜] |
| 상태 | [im] 구현 |
| 설계 문서 | 생략 |

---

## 1. 작업 개요

### 1.1 목적
[작업 목적]

### 1.2 설계 생략 사유
[생략 사유 - 예: 단순 설정 변경, 명확한 작업 범위]

---

## 2. 작업 내용

### 2.1 변경 사항
| # | 파일 | 변경 내용 |
|---|------|----------|
| 1 | | |

### 2.2 상세 내용
[작업 상세 내용]

---

## 3. 테스트

### 3.1 검증 항목
- [ ] 기존 기능 정상 동작
- [ ] 테스트 통과

---

## 4. 다음 단계
- `/wf:build TSK-XX-XX-XX` - 구현 완료 후 코드리뷰
```

### 4단계: WBS 상태 업데이트
1. `[ ]` → `[im]` 상태 변경 (설계 단계 생략)
2. WBS 파일 저장

## 출력 예시

```
[wf:skip] 설계 생략 및 구현 시작

Task: TSK-03-01-01
Category: infrastructure
상태 전환: [ ] Todo → [im] 구현 (설계 생략)

생략 사유: 단순 설정 변경 작업

생성된 문서:
└── 030-implementation.md (초기화)

구현 체크리스트:
├── 설정 파일 수정
├── 테스트 확인
└── 문서화

다음 단계: 구현 완료 후 /wf:build TSK-03-01-01
```

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] infrastructure category만 지원합니다` |
| 잘못된 상태 | `[ERROR] Todo 상태가 아닙니다. 현재 상태: [상태]` |
| 이미 설계 시작 | `[ERROR] 이미 설계가 시작되었습니다. /wf:build 사용` |

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[ ]` Todo 상태인 infrastructure Task들의 설계 생략 처리를 병렬로 실행합니다.

```
[wf:skip] 워크플로우 시작 (병렬 처리)

입력: WP-03 (Work Package)
범위: Infrastructure - DevOps Setup
대상 Task: 8개 (상태 필터 적용: 5개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/5] TSK-03-01-01: CI/CD 파이프라인 설정 생략 ✅
├── [2/5] TSK-03-01-02: Docker 설정 생략 ✅
├── [3/5] TSK-03-02-01: 환경 변수 설정 생략 🔄 진행중
├── [4/5] TSK-03-02-02: 로깅 설정 생략 ⏳ 대기
└── [5/5] TSK-03-03-01: 모니터링 설정 생략 ⏳ 대기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 5개
├── 실패: 0개
└── 스킵: 3개 (Todo 상태 아님 또는 non-infrastructure)

상태 전환:
├── TSK-03-01-01: [ ] → [im] ✅
├── TSK-03-01-02: [ ] → [im] ✅
├── TSK-03-02-01: [ ] → [im] ✅
└── ...

생성된 문서:
├── TSK-03-01-01/030-implementation.md (초기화)
├── TSK-03-01-02/030-implementation.md (초기화)
└── ...

다음 단계: 개별 Task별 구현 후 /wf:build 실행
```

---

## infrastructure 워크플로우 비교

### 설계 포함 (일반)
```
[ ] Todo
  │ /wf:start
  ▼
[dd] 상세설계
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

## 다음 명령어

- `/wf:build` - 구현 완료 및 코드리뷰 시작

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
jjiban 프로젝트 - Workflow Command
author: 장종익
Command: wf:skip
Version: 1.0

Changes (v1.0):
- 초기 버전
-->
