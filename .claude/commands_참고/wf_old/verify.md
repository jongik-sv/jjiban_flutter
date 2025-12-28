---
name: wf:verify
description: "통합테스트 시작. 구현 → 통합테스트 전환"
category: workflow
hierarchy-input: true
parallel-processing: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
mcp-servers: [playwright]
---

# /wf:verify - 통합테스트 시작

> **상태 전환**: `[im] 구현` → `[vf] 검증` (development)
> **상태 전환**: `[fx] 수정` → `[vf] 검증` (defect)
> **적용 category**: development, defect

## 사용법

```bash
/wf:verify [WP-ID | ACT-ID | Task-ID]

# 예시
/wf:verify TSK-01-01-01            # 단일 Task
/wf:verify ACT-01-01               # Activity 내 모든 Task 병렬 처리
/wf:verify WP-01                   # Work Package 내 모든 Task 병렬 처리
```

## 계층 입력 처리

@.claude/includes/wf-hierarchy-input.md

| 입력 타입 | 처리 방식 | 상태 필터 |
|-----------|----------|----------|
| `TSK-XX-XX-XX` | 단일 Task 처리 | `[im]` 구현, `[fx]` 수정 |
| `ACT-XX-XX` | ACT 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |
| `WP-XX` | WP 내 Task 병렬 처리 | `[im]`, `[fx]` 상태만 |

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 | 생성 문서 |
|----------|----------|----------|----------|
| development | `[im]` 구현 | `[vf]` 검증 | `070-integration-test.md` |
| defect | `[fx]` 수정 | `[vf]` 검증 | `070-test-results.md` |

## 문서 경로

@.claude/includes/wf-common.md

**Task 폴더**: `.orchay/projects/{project}/tasks/{TSK-ID}/`

---

## 실행 과정

### 1단계: Task 검증
1. Task JSON에서 Task 찾기 (`.orchay/projects/{project}/tasks/{TSK-ID}/task.json`)
2. category가 `development` 또는 `defect`인지 확인
3. 현재 상태 확인:
   - development: `[im]` 구현
   - defect: `[fx]` 수정

### 2단계: 구현 완료 검증

**development 체크리스트**:
- [ ] 구현 문서 (`030-implementation.md`) 완료
- [ ] 단위 테스트 통과
- [ ] E2E 테스트 통과
- [ ] 코드 리뷰 반영 완료 (선택)

**defect 체크리스트**:
- [ ] 구현 문서 (`030-implementation.md`) 완료
- [ ] 결함 수정 완료
- [ ] 단위 테스트 통과

### 3단계: 통합 테스트 실행 (development)

**테스트 범위**:
1. 엔드투엔드 시나리오 테스트
2. 다른 모듈과의 통합 테스트
3. API 통합 테스트
4. UI 통합 테스트

**070-integration-test.md 템플릿**:
```markdown
# 통합테스트 결과: [Task명]

## 테스트 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | development |
| 테스트 일시 | [오늘 날짜/시간] |
| 테스트 환경 | [환경 정보] |
| 상태 | [vf] 검증 |

---

## 1. 테스트 개요

### 1.1 테스트 범위
[테스트 대상 기능 및 범위]

### 1.2 테스트 환경
| 항목 | 내용 |
|------|------|
| OS | [OS] |
| Node.js | [버전] |
| Database | [DB/버전] |
| Browser | [브라우저/버전] |

---

## 2. 테스트 시나리오

### 2.1 시나리오 목록
| # | 시나리오 | 결과 | 비고 |
|---|----------|------|------|
| 1 | [시나리오1] | ✅/❌ | |
| 2 | [시나리오2] | ✅/❌ | |

### 2.2 상세 테스트 결과

#### 시나리오 1: [시나리오명]
**목적**: [테스트 목적]

**전제 조건**:
- 조건 1
- 조건 2

**테스트 단계**:
1. 단계 1 → 결과: ✅
2. 단계 2 → 결과: ✅
3. 단계 3 → 결과: ✅

**결과**: ✅ 통과

---

## 3. API 통합 테스트

### 3.1 테스트 결과
| # | API | Method | 결과 | 응답시간 |
|---|-----|--------|------|----------|
| 1 | /api/[endpoint] | GET | ✅ | [N]ms |
| 2 | /api/[endpoint] | POST | ✅ | [N]ms |

---

## 4. UI 통합 테스트

### 4.1 테스트 결과
| # | 화면 | 테스트 항목 | 결과 |
|---|------|------------|------|
| 1 | [화면명] | [항목] | ✅/❌ |

### 4.2 스크린샷
[테스트 중 캡처된 스크린샷 경로]

---

## 5. 테스트 요약

### 5.1 통계
| 항목 | 값 |
|------|-----|
| 총 테스트 케이스 | [N]건 |
| 통과 | [N]건 |
| 실패 | [N]건 |
| 통과율 | [N]% |

### 5.2 발견된 이슈
| # | 이슈 | 심각도 | 상태 |
|---|------|--------|------|
| - | 없음 | - | - |

---

## 6. 다음 단계
- `/wf:done TSK-XX-XX-XX` → 작업 완료 처리
```

### 4단계: 회귀 테스트 실행 (defect)

**070-test-results.md 템플릿**:
```markdown
# 결함 수정 테스트 결과: [Task명]

## 테스트 정보
| 항목 | 내용 |
|------|------|
| Task ID | [Task-ID] |
| Category | defect |
| 테스트 일시 | [오늘 날짜/시간] |
| 원본 결함 | [결함 설명] |
| 상태 | [vf] 검증 |

---

## 1. 결함 수정 확인

### 1.1 원본 결함 재현 테스트
| 단계 | 내용 | 결과 |
|------|------|------|
| 1 | [재현 단계 1] | ✅ 해결됨 |
| 2 | [재현 단계 2] | ✅ 해결됨 |

### 1.2 결과
- 원본 결함: ✅ 수정 확인

---

## 2. 회귀 테스트

### 2.1 영향 받는 기능 테스트
| # | 기능 | 테스트 결과 | 비고 |
|---|------|------------|------|
| 1 | [기능1] | ✅ | |
| 2 | [기능2] | ✅ | |

### 2.2 결과
- 회귀 테스트: ✅ 모든 기능 정상

---

## 3. 테스트 요약

| 항목 | 값 |
|------|-----|
| 결함 수정 확인 | ✅ |
| 회귀 테스트 통과 | ✅ |
| 새로운 이슈 | 없음 |

---

## 4. 다음 단계
- `/wf:done TSK-XX-XX-XX` → 작업 완료 처리
```

### 5단계: Task JSON 상태 업데이트
1. `[im]` → `[vf]` (development) 또는 `[fx]` → `[vf]` (defect) 상태 변경
2. updated_at 필드 업데이트
3. Task JSON 파일 저장

### 6단계: WBS 테스트 결과 업데이트 ⭐
1. **테스트 결과 판정**:
   - 모든 통합테스트 통과 → `pass`
   - 하나라도 실패 → `fail`
2. **wbs.md 업데이트**:
   - Task의 `test-result` 필드 업데이트
   - `test-result: none` → `test-result: pass` 또는 `test-result: fail`
3. **업데이트 로그**:
   - 테스트 결과 및 변경 시각 기록

---

## 출력 예시

### development
```
[wf:verify] 통합테스트 시작

Task: TSK-01-01-01
Category: development
상태 전환: [im] 구현 → [vf] 검증

구현 검증:
├── 030-implementation.md ✅
├── 단위 테스트: 15/15 통과 ✅
└── E2E 테스트: 5/5 통과 ✅

통합테스트 실행:
├── 시나리오 테스트: 5/5 통과 ✅
├── API 통합 테스트: 12/12 통과 ✅
└── UI 통합 테스트: 8/8 통과 ✅

생성된 문서:
└── 070-integration-test.md

WBS 테스트 결과 업데이트:
└── test-result: none → pass ✅

다음 단계: /wf:done TSK-01-01-01
```

### defect
```
[wf:verify] 테스트 시작

Task: TSK-02-01-01
Category: defect
상태 전환: [fx] 수정 → [vf] 검증

수정 검증:
├── 030-implementation.md ✅
└── 단위 테스트: 18/18 통과 ✅

회귀 테스트 실행:
├── 결함 수정 확인: ✅
├── 회귀 테스트: 10/10 통과 ✅
└── 새로운 이슈: 없음

생성된 문서:
└── 070-test-results.md

WBS 테스트 결과 업데이트:
└── test-result: none → pass ✅

다음 단계: /wf:done TSK-02-01-01
```

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development 또는 defect만 지원합니다` |
| 잘못된 상태 (dev) | `[ERROR] 구현 상태가 아닙니다. 현재 상태: [상태]` |
| 잘못된 상태 (defect) | `[ERROR] 수정 상태가 아닙니다. 현재 상태: [상태]` |
| 구현 문서 없음 | `[ERROR] 구현 문서가 없습니다` |
| 테스트 실패 | `[ERROR] 테스트가 통과하지 않았습니다 ([N]건 실패)` |

## WP/ACT 단위 병렬 처리

WP 또는 ACT 단위 입력 시, 해당 범위 내 `[im]`/`[fx]` 상태 Task들의 통합테스트를 병렬로 실행합니다.

```
[wf:verify] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
대상 Task: 12개 (상태 필터 적용: 8개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/8] TSK-01-01-01: Project CRUD 통합테스트 ✅
├── [2/8] TSK-01-01-02: Project 대시보드 통합테스트 ✅
├── [3/8] TSK-01-02-01: WP CRUD 통합테스트 🔄 진행중
├── [4/8] TSK-01-02-02: WP 계층 구조 통합테스트 ⏳ 대기
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 7개
├── 실패: 1개 (TSK-01-02-03: API 통합테스트 실패)
└── 스킵: 0개

상태 전환:
├── TSK-01-01-01: [im] → [vf] ✅
├── TSK-01-01-02: [im] → [vf] ✅
├── TSK-01-02-01: [im] → [vf] ✅
└── ...

생성된 문서:
├── TSK-01-01-01/070-integration-test.md
├── TSK-01-01-02/070-integration-test.md
└── ...

다음 단계: 개별 Task별 /wf:done 실행
```

---

## 다음 명령어

- `/wf:done` - 작업 최종 완료

---

## 마지막 단계: 자동 Git Commit

@.claude/includes/wf-auto-commit.md

---

<!--
orchay 프로젝트 - Workflow Command
author: 장종익
Command: wf:verify
Version: 1.0

Changes (v1.0):
- 생성
-->
