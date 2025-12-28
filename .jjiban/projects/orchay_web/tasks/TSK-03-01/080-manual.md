# Task 상세 API 및 템플릿 - 사용자 매뉴얼

> **Task ID**: TSK-03-01
> **버전**: 1.0
> **최종 수정일**: 2025-12-28

---

## 1. 개요

### 1.1 기능 소개

Task 상세 API는 WBS 트리에서 선택한 Task의 상세 정보를 표시하는 기능입니다. 웹 UI의 우측 패널에서 Task의 모든 속성과 관련 문서 목록을 확인할 수 있습니다.

### 1.2 대상 사용자

- orchay 웹 모니터링 UI 사용자
- Task 진행 상황을 확인하는 프로젝트 관리자
- 개발자 및 팀원

---

## 2. 시작하기

### 2.1 사전 요구사항

- orchay 웹 서버 실행 중
- 브라우저 (Chrome, Firefox, Edge 권장)

### 2.2 접근 방법

1. orchay 웹 서버 시작:
   ```bash
   cd orchay
   uv run orchay --web
   ```

2. 브라우저에서 `http://localhost:8080` 접속

3. 좌측 WBS 트리에서 Task 클릭

---

## 3. 사용 방법

### 3.1 기본 사용법

1. **Task 선택**: 좌측 트리에서 `TSK-XX-XX` 형식의 Task 노드 클릭
2. **상세 정보 확인**: 우측 패널에 Task 정보 표시
3. **문서 열기**: Documents 섹션에서 문서 링크 클릭

### 3.2 상세 기능

#### 3.2.1 표시되는 정보

| 필드 | 설명 |
|------|------|
| Task ID | Task 고유 식별자 (예: TSK-03-01) |
| Title | Task 제목 |
| Status | 현재 상태 (색상 배지) |
| Category | 카테고리 (development, infrastructure 등) |
| Priority | 우선순위 (critical, high, medium, low) |
| Domain | 도메인 (backend, frontend, fullstack 등) |
| Assignee | 담당자 |
| Tags | 태그 목록 |
| Dependencies | 의존하는 Task 목록 |
| Documents | 관련 문서 파일 목록 |

#### 3.2.2 상태 색상 표

| 상태 코드 | 의미 | 색상 |
|-----------|------|------|
| `[xx]` | 완료 | 🟢 녹색 |
| `[im]` | 구현 중 | 🔵 파란색 |
| `[ap]` | 승인됨 | 🟣 보라색 |
| `[dd]` | 상세설계 | 🟡 노란색 |
| `[bd]` | 기본설계 | 🟠 주황색 |
| 기타 | - | ⚪ 회색 |

#### 3.2.3 문서 목록

Documents 섹션에는 해당 Task의 산출물 목록이 표시됩니다:

- `010-design.md` - 설계 문서
- `025-traceability-matrix.md` - 추적성 매트릭스
- `026-test-specification.md` - 테스트 명세
- `030-implementation.md` - 구현 보고서
- `080-manual.md` - 사용자 매뉴얼

---

## 4. FAQ

### Q1. Task를 클릭해도 상세 정보가 표시되지 않아요.

A: 네트워크 연결을 확인하세요. 브라우저 개발자 도구(F12)의 Network 탭에서 `/api/detail/{task_id}` 요청 상태를 확인할 수 있습니다.

### Q2. 문서 링크가 비어있어요.

A: 해당 Task의 문서 디렉토리(`.orchay/projects/{project}/tasks/{task_id}/`)에 `.md` 파일이 없을 수 있습니다.

### Q3. 상태 배지 색상이 회색으로 표시돼요.

A: 알 수 없는 상태 코드입니다. WBS 파일의 status 값을 확인하세요.

---

## 5. 문제 해결

### 5.1 "Task를 찾을 수 없습니다" 에러

**원인**: 요청한 Task ID가 WBS에 존재하지 않음

**해결**:
1. WBS 파일 확인: `.orchay/projects/{project}/wbs.md`
2. Task ID 형식 확인: `TSK-XX-XX`
3. 웹 서버 재시작: WBS 변경 후 서버 재시작 필요할 수 있음

### 5.2 Documents 섹션이 표시되지 않음

**원인**: Task 문서 디렉토리가 없거나 비어있음

**해결**:
1. 디렉토리 확인: `.orchay/projects/{project}/tasks/{task_id}/`
2. `.md` 파일 존재 확인

---

## 6. 참고 자료

- [orchay 웹 모니터링 UI PRD](.orchay/projects/orchay_web/prd.md)
- [TSK-03-01 설계 문서](./010-design.md)
- [TSK-03-01 구현 보고서](./030-implementation.md)

---

## API 참조

### GET /api/detail/{task_id}

Task 상세 정보 HTML 파셜을 반환합니다.

**요청**:
```
GET /api/detail/TSK-03-01 HTTP/1.1
Host: localhost:8080
```

**응답 (200 OK)**:
```html
<div id="detail-panel" data-testid="detail-panel" class="...">
  <!-- Task 상세 정보 -->
</div>
```

**응답 (404 Not Found)**:
```html
<div class="...">
  <p>Task 'TSK-XX-XX'를 찾을 수 없습니다</p>
</div>
```

---

<!--
TSK-03-01 사용자 매뉴얼
Version: 1.0
Created: 2025-12-28
-->
