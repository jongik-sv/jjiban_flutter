# 공통 모듈: Task 데이터 및 문서 경로

> 이 파일은 모든 `/wf:*` 명령어에서 참조하는 공통 모듈입니다.

---

## 파일 기반 아키텍처 경로 규칙

### 1. 디렉토리 구조

JJIBAN은 `.jjiban/` 폴더에 모든 데이터와 문서를 관리합니다.

> **중요**: PRD 5.1 디렉토리 구조를 따릅니다.

```
.jjiban/
├── settings/                      # 전역 설정 (모든 프로젝트 공통)
│   ├── projects.json              # 프로젝트 목록
│   ├── columns.json               # 칸반 컬럼 정의
│   ├── categories.json            # 카테고리 정의
│   ├── workflows.json             # 워크플로우 규칙
│   └── actions.json               # 상태 내 액션 정의
│
├── templates/                     # 문서 템플릿
│   ├── 010-basic-design.md
│   ├── 011-ui-design.md
│   ├── 020-detail-design.md
│   ├── 030-implementation.md
│   ├── 070-integration-test.md
│   └── 080-manual.md
│
└── projects/                      # 프로젝트 폴더
    └── {project-id}/              # 개별 프로젝트
        ├── project.json           # 프로젝트 메타데이터
        ├── team.json              # 팀원 목록
        ├── wbs.md                 # WBS 통합 파일 (유일한 소스)
        │
        └── tasks/                 # Task 문서 폴더
            ├── TSK-01-01/         # 3단계: WP-ACT 없이 직접
            │   ├── 010-basic-design.md
            │   └── 020-detail-design.md
            └── TSK-01-01-01/      # 4단계: WP-ACT-TSK
                ├── 010-basic-design.md
                └── 020-detail-design.md
```

> **wbs.md**: WP, ACT, TSK의 모든 메타데이터를 단일 마크다운 파일로 관리. LLM이 한 번에 전체 구조를 파악 가능
> **3단계 구조**: Project → WP → TSK (소규모 프로젝트)
> **4단계 구조**: Project → WP → ACT → TSK (대규모 프로젝트)
> **settings 폴더**: 전역 설정. 없으면 기본 설정을 메모리에서 생성

### 2. 주요 파일 경로

| 용도 | 경로 | 설명 |
|------|------|------|
| 프로젝트 목록 | `.jjiban/settings/projects.json` | 전역 프로젝트 목록 |
| 프로젝트 정보 | `.jjiban/projects/{project}/project.json` | 프로젝트 메타데이터 |
| WBS 통합 파일 | `.jjiban/projects/{project}/wbs.md` | WP/ACT/TSK 메타데이터 |
| 팀 정보 | `.jjiban/projects/{project}/team.json` | 팀 멤버 목록 |
| Task 문서 폴더 | `.jjiban/projects/{project}/tasks/{TSK-ID}/` | Task 관련 문서 |
| 문서 템플릿 | `.jjiban/templates/` | 전역 문서 템플릿 |

### 3. wbs.md 구조 (Task 메타데이터 관리)

**파일 경로**: `.jjiban/projects/{project}/wbs.md`

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
- progress: 25%

### ACT-01-01: 프로젝트 관리
- status: in_progress
- schedule: 2026-01-15 ~ 2026-01-22

#### TSK-01-01-01: 프로젝트 CRUD API 구현
- category: development
- status: implement [im]
- priority: high
- assignee: hong
- schedule: 2026-01-15 ~ 2026-01-21
- tags: api, backend, crud
- depends: -
- blocked-by: -
```

### 4. Task 상태 코드 (wbs.md에서 관리)

| 상태 코드 | 의미 | Category | 칸반 컬럼 |
|----------|------|----------|----------|
| `[ ]` | Todo (미시작) | 공통 | Todo |
| `[bd]` | 기본설계 | development | Design |
| `[dd]` | 상세설계 | development | Detail |
| `[an]` | 분석 | defect | Detail |
| `[ds]` | 설계 | infrastructure | Detail |
| `[im]` | 구현 | development, infrastructure | Implement |
| `[fx]` | 수정 | defect | Implement |
| `[ts]` | 테스트/통합테스트 | development, defect | Verify |
| `[xx]` | 완료 | 공통 | Done |

---

## Task 문서 폴더 경로 규칙

### 1. Task 폴더 구조

모든 Task 관련 문서는 Task 폴더 내에 저장됩니다.

> **Task 문서 경로**: `.jjiban/projects/{project}/tasks/{TSK-ID}/`

```
{TSK-ID}/                              # Task 폴더
├── 010-basic-design.md                # 기본설계 (development)
├── 010-tech-design.md                 # 기술설계 (infrastructure)
├── 010-defect-analysis.md             # 결함분석 (defect)
├── 011-ui-design.md                   # 화면설계 (development, 선택)
├── ui-assets/                         # SVG 화면 파일 (선택)
│   └── screen-*.svg
├── 020-detail-design.md               # 상세설계 (development)
├── 021-design-review-{llm}-{n}.md     # 설계리뷰
├── 025-traceability-matrix.md         # 추적성 매트릭스
├── 026-test-specification.md          # 테스트 명세
├── 030-implementation.md              # 구현 문서
├── 031-code-review-{llm}-{n}.md       # 코드리뷰
├── 070-integration-test.md            # 통합테스트 (development)
├── 070-test-results.md                # 테스트 결과 (defect)
├── 080-manual.md                      # 사용자 매뉴얼 (development)
└── test-results/                      # 테스트 결과 아티팩트
    └── {timestamp}/
        ├── tdd/
        └── e2e/
```

### 2. 문서 파일 명명 규칙

| 번호 | 파일명 | 용도 | Category |
|------|--------|------|----------|
| 010 | `010-basic-design.md` | 기본설계 | development |
| 011 | `011-ui-design.md` | 화면설계 | development |
| 020 | `020-detail-design.md` | 상세설계 | development |
| 021 | `021-design-review-{llm}-{n}.md` | 설계리뷰 (N차) | development |
| 025 | `025-traceability-matrix.md` | 추적성 매트릭스 | development |
| 026 | `026-test-specification.md` | 테스트 명세 | development |
| 010 | `010-tech-design.md` | 기술설계 | infrastructure |
| 010 | `010-defect-analysis.md` | 결함분석 | defect |
| 030 | `030-implementation.md` | 구현 문서 | 공통 |
| 031 | `031-code-review-{llm}-{n}.md` | 코드리뷰 (N차) | 공통 |
| 070 | `070-integration-test.md` | 통합테스트 | development |
| 070 | `070-test-results.md` | 테스트 결과 | defect |
| 080 | `080-manual.md` | 사용자 매뉴얼 | development |

### 3. 전체 경로 예시

| Task ID | Task 폴더 경로 | 구조 |
|---------|----------------|------|
| TSK-01-01-01 | `.jjiban/projects/{project}/tasks/TSK-01-01-01/` | 4단계 |
| TSK-01-02-01 | `.jjiban/projects/{project}/tasks/TSK-01-02-01/` | 4단계 |
| TSK-02-01 | `.jjiban/projects/{project}/tasks/TSK-02-01/` | 3단계 |

---

## Task 조회 절차

### 1. wbs.md에서 Task 정보 조회

```javascript
// wbs.md 파일 경로
function getWbsPath(project) {
    return `.jjiban/projects/${project}/wbs.md`;
}

// Task 문서 폴더 경로
function getTaskFolderPath(project, taskId) {
    return `.jjiban/projects/${project}/tasks/${taskId}/`;
}

// Task 문서 경로
function getTaskDocPath(project, taskId, docName) {
    return `.jjiban/projects/${project}/tasks/${taskId}/${docName}`;
}
```

### 2. wbs.md에서 Task 상태 확인

wbs.md 파일을 파싱하여 Task 상태를 확인합니다.

```javascript
function getTaskFromWbs(wbsContent, taskId) {
    // TSK-ID 패턴으로 Task 섹션 찾기
    const taskPattern = new RegExp(`^#{2,4} ${taskId}:`, 'im');
    const taskMatch = wbsContent.match(taskPattern);

    if (!taskMatch) return null;

    // status 필드에서 상태 추출
    // - status: implement [im]
    const statusPattern = /- status:\s*\w+\s*\[(\w+)\]/;
    // 파싱 로직...
}
```

### 3. Task 상태 업데이트

wbs.md 파일에서 해당 Task의 status 필드를 수정합니다.

```javascript
function updateTaskStatus(project, taskId, newStatus) {
    const wbsPath = getWbsPath(project);
    let wbsContent = readFile(wbsPath);

    // Task 섹션에서 status 필드 찾아 변경
    // 예: "- status: todo [ ]" → "- status: implement [im]"

    writeFile(wbsPath, wbsContent);
}
```

---

## 프로젝트 설정 파일

### settings/projects.json 스키마

**경로**: `.jjiban/settings/projects.json`

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "jjiban",
      "name": "JJIBAN Project Manager",
      "path": "jjiban",
      "status": "active",
      "wbsDepth": 4,
      "createdAt": "2026-01-15"
    }
  ],
  "defaultProject": "jjiban"
}
```

### project.json 스키마

**경로**: `.jjiban/projects/{project}/project.json`

```json
{
  "id": "jjiban",
  "name": "JJIBAN Project Manager",
  "description": "AI 기반 프로젝트 관리 도구",
  "version": "0.1.0",
  "status": "active",
  "createdAt": "2026-01-15T00:00:00Z",
  "updatedAt": "2026-12-12T10:00:00Z",
  "scheduledStart": "2026-01-15",
  "scheduledEnd": "2026-06-30"
}
```

---

<!--
jjiban 프로젝트 - Workflow Common Module
Version: 4.0
author: 장종익

Changes (v4.0):
- PRD 5.1 디렉토리 구조에 맞게 전면 개편
- .jjiban/projects/{project}/ 경로로 변경
- .jjiban/settings/ 전역 설정 폴더 추가
- .jjiban/templates/ 문서 템플릿 폴더 추가
- task.json 제거 → wbs.md에서 메타데이터 통합 관리
- tasks/ 폴더에는 문서만 저장 (TSK-ID 폴더)
- wbs.md 구조 및 파싱 방법 설명 추가
- 상태 코드에 칸반 컬럼 매핑 추가

Previous (v3.0):
- .jjiban/{project}/ 구조
- task.json 개별 파일 사용
-->
