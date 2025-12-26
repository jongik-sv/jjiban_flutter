# 공통 모듈: 계층 입력 처리 (WP/ACT/TSK)

> 이 파일은 모든 `/wf:*` 명령어에서 Work Package, Activity, Task 단위 입력을 처리하는 공통 모듈입니다.

---

## 1. 지원 입력 형식

| 입력 형식 | 설명 | 예시 |
|-----------|------|------|
| `WP-XX` | Work Package 단위 | `WP-01`, `WP-08` |
| `ACT-XX-XX` | Activity 단위 | `ACT-01-01`, `ACT-02-03` |
| `TSK-XX-XX-XX` | Task 단위 (4단계 구조) | `TSK-01-01-01`, `TSK-02-01-02` |
| `TSK-XX-XX` | Task 단위 (3단계 구조, ACT 없음) | `TSK-01-01`, `TSK-02-03` |

---

## 2. 입력 ID 파싱 규칙

### 2.1 ID 패턴 정규식

```javascript
// ID 타입 식별
const patterns = {
    workPackage: /^WP-(\d{2})$/i,                    // WP-01, WP-08
    activity:    /^ACT-(\d{2})-(\d{2})$/i,           // ACT-01-01
    task4Level:  /^TSK-(\d{2})-(\d{2})-(\d{2})$/i,   // TSK-01-01-01 (4단계: WP/ACT/TSK)
    task3Level:  /^TSK-(\d{2})-(\d{2})$/i            // TSK-01-01 (3단계: WP/TSK, ACT 없음)
};

function parseInputId(input) {
    if (patterns.workPackage.test(input)) return { type: 'WP', id: input };
    if (patterns.activity.test(input)) return { type: 'ACT', id: input };
    if (patterns.task4Level.test(input)) return { type: 'TSK', id: input, level: 4 };
    if (patterns.task3Level.test(input)) return { type: 'TSK', id: input, level: 3 };
    return null;
}
```

### 2.2 입력 타입 판별

| 패턴 | 타입 | 처리 방식 |
|------|------|----------|
| `WP-XX` | Work Package | 해당 WP 내 모든 Task 병렬 처리 |
| `ACT-XX-XX` | Activity | 해당 ACT 내 모든 Task 병렬 처리 |
| `TSK-XX-XX-XX` | Task (4단계) | 단일 Task 처리 (WP/ACT/TSK 구조) |
| `TSK-XX-XX` | Task (3단계) | 단일 Task 처리 (WP/TSK 구조, ACT 없음) |

---

## 3. wbs.md 기반 Task 조회 방법

### 3.1 디렉토리 구조

> **PRD 5.1 구조**: Task 메타데이터는 `wbs.md`에서 관리, 문서는 `tasks/` 폴더에 저장

```
.jjiban/
├── settings/                          # 전역 설정
├── templates/                         # 문서 템플릿
└── projects/
    └── {project}/                     # 프로젝트 폴더
        ├── project.json               # 프로젝트 메타데이터
        ├── team.json                  # 팀원 목록
        ├── wbs.md                     # WBS 통합 파일 (메타데이터)
        └── tasks/                     # Task 문서 폴더
            ├── TSK-01-01/             # 3단계 구조 Task
            │   ├── 010-basic-design.md
            │   └── ...
            └── TSK-01-01-01/          # 4단계 구조 Task
                ├── 010-basic-design.md
                └── ...
```

### 3.2 wbs.md 구조

**경로**: `.jjiban/projects/{project}/wbs.md`

```markdown
# WBS - {Project Name}

> version: 1.0
> depth: 4
> updated: 2026-12-13

---

## WP-01: 플랫폼 기반 구축
- status: in_progress
- priority: high
- schedule: 2026-01-15 ~ 2026-02-14

### ACT-01-01: 프로젝트 관리
- status: in_progress
- schedule: 2026-01-15 ~ 2026-01-22

#### TSK-01-01-01: 프로젝트 CRUD API 구현
- category: development
- status: implement [im]
- priority: high
- assignee: hong

#### TSK-01-01-02: 프로젝트 목록 UI 구현
- category: development
- status: todo [ ]
- priority: high
- assignee: hong
- depends: TSK-01-01-01

---

## WP-02: 칸반 보드
- status: planned
- priority: high

### TSK-02-01: 칸반 컴포넌트 구현
- category: development
- status: todo [ ]
- note: 3단계 구조 예시 (ACT 없이 WP 아래 직접 TSK)
```

### 3.3 wbs.md에서 Task 조회 절차

**WP 입력 시 (예: `WP-01`)**:
1. wbs.md 파일 읽기
2. `## WP-01:` 섹션 찾기
3. 해당 WP 아래의 모든 `TSK-*` 항목 수집
4. 결과: `[TSK-01-01-01, TSK-01-01-02, ...]`

```javascript
function getTasksInWP(project, wpId) {
    const wbsPath = `.jjiban/projects/${project}/wbs.md`;
    const wbsContent = readFile(wbsPath);

    // WP 섹션에서 모든 TSK-* 찾기
    const wpPattern = new RegExp(`## ${wpId}:[\\s\\S]*?(?=## WP-|$)`, 'i');
    const wpSection = wbsContent.match(wpPattern)?.[0];

    const taskPattern = /^#{3,4} (TSK-\d{2}-\d{2}(?:-\d{2})?):.*$/gim;
    const tasks = [...wpSection.matchAll(taskPattern)].map(m => m[1]);
    return tasks;
}
```

**ACT 입력 시 (예: `ACT-01-01`)**:
1. wbs.md 파일 읽기
2. `### ACT-01-01:` 섹션 찾기
3. 해당 ACT 아래의 모든 `TSK-*` 항목 수집
4. 결과: `[TSK-01-01-01, TSK-01-01-02, ...]`

```javascript
function getTasksInACT(project, actId) {
    const wbsPath = `.jjiban/projects/${project}/wbs.md`;
    const wbsContent = readFile(wbsPath);

    // ACT 섹션에서 모든 TSK-* 찾기
    const actPattern = new RegExp(`### ${actId}:[\\s\\S]*?(?=### ACT-|## WP-|$)`, 'i');
    const actSection = wbsContent.match(actPattern)?.[0];

    const taskPattern = /^#### (TSK-\d{2}-\d{2}-\d{2}):.*$/gim;
    const tasks = [...actSection.matchAll(taskPattern)].map(m => m[1]);
    return tasks;
}
```

**TSK 입력 시 (예: `TSK-01-01-01`)**:
1. wbs.md에서 Task 메타데이터 조회
2. Task 문서 폴더 경로: `.jjiban/projects/{project}/tasks/TSK-01-01-01/`
3. 결과: `[TSK-01-01-01]`

```javascript
// Task 문서 폴더 경로
function getTaskFolderPath(project, taskId) {
    return `.jjiban/projects/${project}/tasks/${taskId}/`;
}

// Task 문서 경로
function getTaskDocPath(project, taskId, docName) {
    return `.jjiban/projects/${project}/tasks/${taskId}/${docName}`;
}
```

---

## 4. wbs.md에서 상태 조회/업데이트

### 4.1 Task 상태 조회

```javascript
function getTaskStatus(project, taskId) {
    const wbsPath = `.jjiban/projects/${project}/wbs.md`;
    const wbsContent = readFile(wbsPath);

    // Task 섹션 찾기
    const taskPattern = new RegExp(`^#{2,4} ${taskId}:[\\s\\S]*?(?=^#{2,4} |$)`, 'im');
    const taskSection = wbsContent.match(taskPattern)?.[0];

    if (!taskSection) return null;

    // status 필드에서 상태 코드 추출
    // - status: implement [im]
    const statusMatch = taskSection.match(/- status:\s*\w+\s*\[(\w+)\]/i);
    return statusMatch ? `[${statusMatch[1]}]` : '[ ]';
}
```

### 4.2 Task 상태 업데이트

```javascript
function updateTaskStatus(project, taskId, newStatusText, newStatusCode) {
    const wbsPath = `.jjiban/projects/${project}/wbs.md`;
    let wbsContent = readFile(wbsPath);

    // Task 섹션에서 status 필드 찾아 변경
    // 예: "- status: todo [ ]" → "- status: implement [im]"
    const oldPattern = new RegExp(
        `(^#{2,4} ${taskId}:[\\s\\S]*?- status:\\s*)\\w+\\s*\\[\\w*\\]`,
        'im'
    );
    wbsContent = wbsContent.replace(oldPattern, `$1${newStatusText} [${newStatusCode}]`);

    writeFile(wbsPath, wbsContent);
}
```

### 4.3 Task 상태 코드

| 상태 코드 | 의미 | 상태 텍스트 |
|----------|------|------------|
| `[ ]` | Todo (미시작) | `todo` |
| `[bd]` | 기본설계 | `basic-design` |
| `[dd]` | 상세설계 | `detail-design` |
| `[an]` | 분석 (defect) | `analysis` |
| `[ds]` | 설계 (infrastructure) | `design` |
| `[im]` | 구현 | `implement` |
| `[fx]` | 수정 (defect) | `fix` |
| `[ts]` | 통합테스트 | `test` |
| `[xx]` | 완료 | `done` |

---

## 5. 상태 필터링

명령어별로 특정 상태의 Task만 처리하도록 필터링합니다.

### 5.1 상태 기반 필터 규칙

| 명령어 | 처리 대상 상태 | 필터 조건 |
|--------|---------------|-----------|
| `/wf:start` | `[ ]` Todo | 미시작 Task만 |
| `/wf:draft` | `[bd]` 기본설계 | 기본설계 완료 Task만 |
| `/wf:build` | `[dd]` 상세설계, `[ds]` 설계 | 설계 완료 Task만 |
| `/wf:review` | `[dd]` 상세설계 | 상세설계 완료 Task만 |
| `/wf:audit` | `[im]` 구현, `[fx]` 수정 | 구현/수정 완료 Task만 |
| `/wf:verify` | `[im]` 구현, `[fx]` 수정 | 구현/수정 완료 Task만 |
| `/wf:done` | `[ts]` 테스트 | 테스트 완료 Task만 |

### 5.2 상태 필터링 함수

```javascript
function filterTasksByStatus(project, taskIds, targetStatuses) {
    return taskIds.filter(taskId => {
        const status = getTaskStatus(project, taskId);
        return targetStatuses.includes(status);
    });
}
```

---

## 6. 병렬 처리 구현

### 6.1 병렬 실행 원칙

WP 또는 ACT 단위 입력 시, 해당 범위 내 Task들을 **병렬**로 처리합니다.

```
/wf:start WP-01

실행 흐름:
┌─────────────────────────────────────────────────────────┐
│ wbs.md에서 WP-01 내 Task 목록 수집                       │
│ └── TSK-01-01-01, TSK-01-01-02, TSK-01-02-01, ...       │
├─────────────────────────────────────────────────────────┤
│ 상태 필터링 ([ ] Todo 상태만)                           │
│ └── TSK-01-01-02, TSK-01-02-01                         │
├─────────────────────────────────────────────────────────┤
│ 병렬 처리 (Task Agent 위임)                             │
│ ├── Task Agent → TSK-01-01-02                          │
│ └── Task Agent → TSK-01-02-01                          │
├─────────────────────────────────────────────────────────┤
│ 결과 수집 및 통합 보고                                  │
└─────────────────────────────────────────────────────────┘
```

### 6.2 병렬 처리 도구

```markdown
병렬 처리 시 Task 도구 활용:

1. **Task 도구 병렬 호출**:
   - 각 Task에 대해 Task 도구를 병렬로 호출
   - subagent_type: 해당 명령어에 맞는 에이전트 타입
   - run_in_background: true (선택적)

2. **결과 수집**:
   - TaskOutput으로 각 Task 결과 수집
   - 통합 결과 보고서 생성
```

### 6.3 동시 실행 제한

| 설정 | 기본값 | 설명 |
|------|--------|------|
| 최대 병렬 수 | 5 | 동시 실행 Task 수 제한 |
| 배치 크기 | 5 | 한 번에 처리할 Task 그룹 크기 |

---

## 7. 출력 형식

### 7.1 단일 Task 처리 (기존)

```
[wf:start] 워크플로우 시작

Task: TSK-01-01-01
Category: development
상태 전환: [ ] Todo → [bd] 기본설계
...
```

### 7.2 WP/ACT 단위 병렬 처리

```
[wf:start] 워크플로우 시작 (병렬 처리)

입력: WP-01 (Work Package)
범위: Core - Issue Management
데이터 경로: .jjiban/projects/{project}/wbs.md
대상 Task: 12개 (상태 필터 적용: 8개)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 병렬 처리 진행 상황:
├── [1/8] TSK-01-01-01: Project CRUD 구현 ✅
├── [2/8] TSK-01-01-02: Project 대시보드 구현 ✅
├── [3/8] TSK-01-02-01: WP CRUD 구현 🔄 진행중
├── [4/8] TSK-01-02-02: WP 계층 구조 관리 ⏳ 대기
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 처리 결과 요약:
├── 성공: 6개
├── 실패: 1개 (TSK-01-02-03: 상세설계 문서 없음)
└── 스킵: 1개 (TSK-01-02-04: 이미 진행 중)

다음 단계: 개별 Task별 다음 명령어 실행
```

---

## 8. 사용 예시

### 8.1 명령어별 예시

```bash
# Work Package 단위 실행
/wf:start WP-01           # WP-01 내 모든 Todo Task 시작
/wf:draft WP-01           # WP-01 내 모든 기본설계 완료 Task 상세설계
/wf:build WP-01           # WP-01 내 모든 상세설계 완료 Task 구현

# Activity 단위 실행
/wf:start ACT-01-01       # ACT-01-01 내 모든 Todo Task 시작
/wf:review ACT-01-01      # ACT-01-01 내 모든 상세설계 Task 리뷰

# Task 단위 실행 (기존)
/wf:start TSK-01-01-01    # 단일 Task 시작
```

### 8.2 옵션 조합

```bash
# 특정 상태 Task만 처리 (선택적 옵션)
/wf:build WP-01 --status dd    # 상세설계 상태만
/wf:audit ACT-01-01 --llm gemini  # 특정 LLM으로 리뷰

# 병렬 처리 제어 (선택적 옵션)
/wf:start WP-01 --parallel 3   # 최대 3개 병렬
/wf:draft ACT-01-01 --sequential  # 순차 처리
```

---

## 9. 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 ID 형식 | `[ERROR] 잘못된 ID 형식입니다. WP-XX, ACT-XX-XX, TSK-XX-XX-XX 형식을 사용하세요` |
| wbs.md 없음 | `[ERROR] WBS 파일을 찾을 수 없습니다: .jjiban/projects/{project}/wbs.md` |
| WP 섹션 없음 | `[ERROR] WBS에서 Work Package를 찾을 수 없습니다: WP-XX` |
| ACT 섹션 없음 | `[ERROR] WBS에서 Activity를 찾을 수 없습니다: ACT-XX-XX` |
| Task 없음 | `[ERROR] WBS에서 Task를 찾을 수 없습니다: TSK-XX-XX-XX` |
| Task 폴더 없음 | `[ERROR] Task 문서 폴더를 찾을 수 없습니다: .jjiban/projects/{project}/tasks/{TSK-ID}/` |
| 대상 Task 없음 | `[WARN] 처리 대상 Task가 없습니다. (상태 필터: [상태])` |
| 모두 스킵 | `[WARN] 모든 Task가 스킵되었습니다. (이미 처리됨 또는 조건 미충족)` |

---

<!--
jjiban 프로젝트 - Workflow Common Module
Module: wf-hierarchy-input
Version: 4.0
author: 장종익

Changes (v4.0):
- PRD 5.1 디렉토리 구조에 맞게 전면 개편
- .jjiban/projects/{project}/ 경로로 변경
- wbs.md 기반 Task 메타데이터 조회로 변경
- task.json 제거 → wbs.md에서 상태 관리
- tasks/ 폴더에는 문서만 저장
- wbs.md 파싱 로직 추가 (getTasksInWP, getTasksInACT)
- 상태 조회/업데이트 함수 추가

Previous (v3.0):
- .jjiban/{project}/ 구조
- task.json 개별 파일 사용
-->
