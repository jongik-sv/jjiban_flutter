# 테스트 명세서 (026-test-specification.md)

**Template Version:** 1.0.0 — **Last Updated:** 2025-12-28

> **목적**: 단위 테스트, E2E 테스트, 매뉴얼 테스트 시나리오 및 테스트 데이터 정의
>
> **참조**: 이 문서는 `010-design.md`와 `025-traceability-matrix.md`와 함께 사용됩니다.
>
> **활용 단계**: `/wf:build`, `/wf:test` 단계에서 테스트 코드 생성 기준으로 사용

---

## 0. 문서 메타데이터

| 항목 | 내용 |
|------|------|
| Task ID | TSK-03-01 |
| Task명 | Task 상세 API 및 템플릿 |
| 설계 참조 | `010-design.md` |
| 추적성 매트릭스 참조 | `025-traceability-matrix.md` |
| 작성일 | 2025-12-28 |
| 작성자 | Claude |

---

## 1. 테스트 전략 개요

### 1.1 테스트 범위

| 테스트 유형 | 범위 | 목표 커버리지 |
|------------|------|--------------|
| 단위 테스트 | API 라우트, 템플릿 렌더링, 유틸 함수 | 80% 이상 |
| E2E 테스트 | Task 상세 조회 시나리오 | 100% 시나리오 커버 |
| 매뉴얼 테스트 | UI/UX, 반응형, 접근성 | 전체 화면 |

### 1.2 테스트 환경

| 항목 | 내용 |
|------|------|
| 테스트 프레임워크 (단위) | pytest, pytest-asyncio |
| 테스트 프레임워크 (E2E) | pytest + httpx (FastAPI TestClient) |
| 테스트 환경 | 로컬 개발 환경 |
| 브라우저 | Chromium (E2E 확장 시) |
| 베이스 URL | `http://localhost:8080` |

---

## 2. 단위 테스트 시나리오

### 2.1 테스트 케이스 목록

| 테스트 ID | 대상 | 시나리오 | 예상 결과 | 요구사항 |
|-----------|------|----------|----------|----------|
| UT-001 | get_task_detail | 정상 조회 | 모든 속성 포함된 HTML 반환 | FR-001~FR-006 |
| UT-002 | STATUS_COLORS | 상태 색상 매핑 | 올바른 Tailwind 클래스 반환 | FR-003 |
| UT-003 | get_task_documents | 문서 목록 조회 | 존재하는 파일만 반환 | FR-007, BR-002 |
| UT-004 | get_task_detail | 미존재 Task | 에러 메시지 포함 HTML 반환 | BR-001 |

### 2.2 테스트 케이스 상세

#### UT-001: get_task_detail 정상 조회

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/web/test_server.py` |
| **테스트 블록** | `describe('get_task_detail') → it('returns task detail HTML')` |
| **Mock 의존성** | Orchestrator.get_task → Mock Task 객체 반환 |
| **입력 데이터** | `task_id: "TSK-03-01"` |
| **검증 포인트** | 응답에 task.id, task.title, task.status 포함 확인 |
| **커버리지 대상** | `get_task_detail()` 정상 분기 |
| **관련 요구사항** | FR-001~FR-006 |

```python
async def test_get_task_detail_success():
    """Task 상세 조회 성공 시 HTML 반환"""
    # Given
    mock_task = Task(
        id="TSK-03-01",
        title="Task 상세 API 및 템플릿",
        status="[dd]",
        category="development",
        priority="high",
        depends=["TSK-02-02"]
    )
    orchestrator.get_task = MagicMock(return_value=mock_task)

    # When
    response = await client.get("/api/detail/TSK-03-01")

    # Then
    assert response.status_code == 200
    assert "TSK-03-01" in response.text
    assert "Task 상세 API 및 템플릿" in response.text
    assert "[dd]" in response.text
```

#### UT-002: STATUS_COLORS 상태 색상 매핑

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/web/test_server.py` |
| **테스트 블록** | `describe('STATUS_COLORS') → it('maps status to correct color')` |
| **Mock 의존성** | - |
| **입력 데이터** | 각 상태 코드 |
| **검증 포인트** | 올바른 Tailwind 배경색 클래스 반환 |
| **커버리지 대상** | `STATUS_COLORS` 딕셔너리 |
| **관련 요구사항** | FR-003 |

```python
def test_status_colors_mapping():
    """상태 코드별 올바른 색상 클래스 반환"""
    # Given & When & Then
    assert STATUS_COLORS["[ ]"] == "bg-gray-500"
    assert STATUS_COLORS["[bd]"] == "bg-blue-500"
    assert STATUS_COLORS["[dd]"] == "bg-purple-500"
    assert STATUS_COLORS["[ap]"] == "bg-green-500"
    assert STATUS_COLORS["[im]"] == "bg-yellow-500"
    assert STATUS_COLORS["[xx]"] == "bg-emerald-500"
```

#### UT-003: get_task_documents 문서 목록 조회

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/web/test_server.py` |
| **테스트 블록** | `describe('get_task_documents') → it('returns existing files only')` |
| **Mock 의존성** | 파일시스템 모킹 |
| **입력 데이터** | `task_id: "TSK-03-01"` |
| **검증 포인트** | 존재하는 파일만 목록에 포함 |
| **커버리지 대상** | `get_task_documents()` 함수 |
| **관련 요구사항** | FR-007, BR-002 |

```python
def test_get_task_documents_returns_existing_files(tmp_path):
    """존재하는 파일만 문서 목록에 포함"""
    # Given
    task_dir = tmp_path / "TSK-03-01"
    task_dir.mkdir()
    (task_dir / "010-design.md").touch()
    (task_dir / "025-traceability-matrix.md").touch()

    # When
    docs = get_task_documents("TSK-03-01", base_path=tmp_path)

    # Then
    assert len(docs) == 2
    assert "010-design.md" in docs
    assert "025-traceability-matrix.md" in docs
```

#### UT-004: get_task_detail 미존재 Task

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/web/test_server.py` |
| **테스트 블록** | `describe('get_task_detail') → it('returns error for missing task')` |
| **Mock 의존성** | Orchestrator.get_task → None 반환 |
| **입력 데이터** | `task_id: "TSK-99-99"` |
| **검증 포인트** | 에러 메시지 포함 확인 |
| **커버리지 대상** | `get_task_detail()` 에러 분기 |
| **관련 요구사항** | BR-001 |

```python
async def test_get_task_detail_not_found():
    """미존재 Task 조회 시 에러 메시지 반환"""
    # Given
    orchestrator.get_task = MagicMock(return_value=None)

    # When
    response = await client.get("/api/detail/TSK-99-99")

    # Then
    assert response.status_code == 200  # HTML 반환
    assert "Task를 찾을 수 없습니다" in response.text
```

---

## 3. E2E 테스트 시나리오

### 3.1 테스트 케이스 목록

| 테스트 ID | 시나리오 | 사전조건 | 실행 단계 | 예상 결과 | 요구사항 |
|-----------|----------|----------|----------|----------|----------|
| E2E-001 | Task 상세 조회 | 웹서버 실행 | 1. API 호출 | 모든 속성 표시 | FR-001~FR-006 |
| E2E-002 | 문서 목록 표시 | Task 문서 존재 | 1. API 호출 | 문서 목록 표시 | FR-007, BR-002 |
| E2E-003 | 미존재 Task 오류 | - | 1. 잘못된 ID로 호출 | 에러 메시지 표시 | BR-001 |

### 3.2 테스트 케이스 상세

#### E2E-001: Task 상세 조회

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail.py` |
| **테스트명** | `test_task_detail_shows_all_properties` |
| **사전조건** | Orchestrator에 Task 존재 |
| **API 확인** | `GET /api/detail/TSK-03-01` → 200 |
| **검증 포인트** | Task ID, 제목, 상태, 카테고리, 우선순위, 의존성 표시 |
| **관련 요구사항** | FR-001~FR-006 |

```python
async def test_task_detail_shows_all_properties(client):
    """Task 상세 조회 시 모든 속성이 표시된다"""
    # When
    response = await client.get("/api/detail/TSK-03-01")

    # Then
    assert response.status_code == 200
    html = response.text

    # 필수 속성 확인
    assert "TSK-03-01" in html                    # ID
    assert "Task 상세 API 및 템플릿" in html       # 제목
    assert "[dd]" in html or "detail-design" in html  # 상태
    assert "development" in html                   # 카테고리
    assert "high" in html                          # 우선순위
    assert "TSK-02-02" in html                     # 의존성
```

#### E2E-002: 문서 목록 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail.py` |
| **테스트명** | `test_task_detail_shows_documents` |
| **사전조건** | Task 디렉토리에 문서 파일 존재 |
| **API 확인** | `GET /api/detail/TSK-03-01` → 200 |
| **검증 포인트** | Documents 섹션에 파일 목록 표시 |
| **관련 요구사항** | FR-007, BR-002 |

```python
async def test_task_detail_shows_documents(client, tmp_task_docs):
    """Task 상세에 관련 문서 목록이 표시된다"""
    # Given: tmp_task_docs fixture가 010-design.md 등 생성

    # When
    response = await client.get("/api/detail/TSK-03-01")

    # Then
    assert response.status_code == 200
    html = response.text

    assert "Documents" in html
    assert "010-design.md" in html
```

#### E2E-003: 미존재 Task 오류

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail.py` |
| **테스트명** | `test_task_detail_not_found_error` |
| **사전조건** | - |
| **API 확인** | `GET /api/detail/TSK-99-99` → 200 (에러 HTML) |
| **검증 포인트** | "Task를 찾을 수 없습니다" 메시지 |
| **관련 요구사항** | BR-001 |

```python
async def test_task_detail_not_found_error(client):
    """존재하지 않는 Task 조회 시 에러 메시지가 표시된다"""
    # When
    response = await client.get("/api/detail/TSK-99-99")

    # Then
    assert response.status_code == 200
    assert "Task를 찾을 수 없습니다" in response.text
```

---

## 4. UI 테스트케이스 (매뉴얼)

### 4.1 테스트 케이스 목록

| TC-ID | 테스트 항목 | 사전조건 | 테스트 단계 | 예상 결과 | 우선순위 | 요구사항 |
|-------|-----------|---------|-----------|----------|---------|----------|
| TC-001 | Task 상세 표시 | 웹서버 실행 | 1. 트리에서 Task 클릭 | 상세 패널에 정보 표시 | High | FR-001~FR-006 |
| TC-002 | 문서 링크 표시 | 문서 존재 | 1. 상세 패널 확인 | 문서 목록 표시 | Medium | FR-007 |
| TC-003 | 상태 색상 확인 | - | 1. 다양한 상태 Task 확인 | 상태별 색상 구분 | Medium | FR-003 |
| TC-004 | 반응형 확인 | - | 1. 브라우저 크기 조절 | 레이아웃 적응 | Medium | - |
| TC-005 | 에러 상태 확인 | - | 1. 미존재 Task 접근 | 에러 메시지 표시 | Medium | BR-001 |

### 4.2 매뉴얼 테스트 상세

#### TC-001: Task 상세 표시

**테스트 목적**: 사용자가 WBS 트리에서 Task를 클릭하면 상세 패널에 정보가 표시되는지 확인

**테스트 단계**:
1. orchay --web 실행
2. 브라우저에서 http://localhost:8080 접속
3. WBS 트리에서 Task 노드 클릭

**예상 결과**:
- 상세 패널에 Task ID 표시
- Task 제목 표시
- Status 배지 (색상 + 라벨) 표시
- Category, Domain, Priority, Depends 속성 표시

**검증 기준**:
- [ ] Task ID가 정확히 표시됨
- [ ] 제목이 정확히 표시됨
- [ ] Status 배지가 올바른 색상으로 표시됨
- [ ] 모든 속성이 누락 없이 표시됨

#### TC-003: 상태 색상 확인

**테스트 목적**: 각 상태 코드가 올바른 배경색으로 표시되는지 확인

**테스트 단계**:
1. 다양한 상태의 Task를 선택
2. 상태 배지 색상 확인

**예상 결과**:

| 상태 | 예상 색상 |
|------|----------|
| [ ] | 회색 (gray-500) |
| [bd] | 파란색 (blue-500) |
| [dd] | 보라색 (purple-500) |
| [ap] | 녹색 (green-500) |
| [im] | 노란색 (yellow-500) |
| [xx] | 에메랄드 (emerald-500) |

---

## 5. 테스트 데이터 (Fixture)

### 5.1 단위 테스트용 Mock 데이터

| 데이터 ID | 용도 | 값 |
|-----------|------|-----|
| MOCK-TASK-01 | 정상 Task | `{ id: 'TSK-03-01', title: 'Task 상세 API 및 템플릿', status: '[dd]', category: 'development', priority: 'high', depends: ['TSK-02-02'] }` |
| MOCK-TASK-02 | 의존성 없는 Task | `{ id: 'TSK-01-01', title: 'FastAPI 앱', status: '[dd]', category: 'development', priority: 'critical', depends: [] }` |
| MOCK-TASK-DONE | 완료된 Task | `{ id: 'TSK-00-00', title: '완료 Task', status: '[xx]', category: 'development', priority: 'low', depends: [] }` |

### 5.2 E2E 테스트용 시드 데이터

| 시드 ID | 용도 | 생성 방법 | 포함 데이터 |
|---------|------|----------|------------|
| SEED-E2E-BASE | 기본 E2E 환경 | 자동 시드 | Task 5개, WP 2개, ACT 3개 |
| SEED-E2E-DOCS | 문서 존재 환경 | 자동 시드 | Task + 문서 파일 3개 |

### 5.3 테스트 파일

| 파일 ID | 파일명 | 경로 | 용도 |
|---------|--------|------|------|
| DOC-001 | 010-design.md | .orchay/projects/.../tasks/TSK-03-01/ | 문서 목록 테스트 |
| DOC-002 | 025-traceability-matrix.md | .orchay/projects/.../tasks/TSK-03-01/ | 문서 목록 테스트 |
| DOC-003 | 026-test-specification.md | .orchay/projects/.../tasks/TSK-03-01/ | 문서 목록 테스트 |

---

## 6. data-testid 목록

> 프론트엔드 컴포넌트에 적용할 `data-testid` 속성 정의

### 6.1 상세 패널 셀렉터

| data-testid | 요소 | 용도 |
|-------------|------|------|
| `detail-panel` | 상세 패널 컨테이너 | 패널 로드 확인 |
| `task-id` | Task ID 표시 | ID 텍스트 확인 |
| `task-title` | Task 제목 표시 | 제목 텍스트 확인 |
| `task-status` | 상태 배지 | 상태 확인 |
| `task-category` | 카테고리 값 | 카테고리 확인 |
| `task-domain` | 도메인 값 | 도메인 확인 |
| `task-priority` | 우선순위 값 | 우선순위 확인 |
| `task-depends` | 의존성 값 | 의존성 확인 |
| `documents-list` | 문서 목록 | 문서 목록 확인 |
| `document-item` | 문서 항목 | 개별 문서 확인 |
| `error-message` | 에러 메시지 | 에러 표시 확인 |

---

## 7. 테스트 커버리지 목표

### 7.1 단위 테스트 커버리지

| 대상 | 목표 | 최소 |
|------|------|------|
| Lines | 80% | 70% |
| Branches | 75% | 65% |
| Functions | 85% | 75% |
| Statements | 80% | 70% |

### 7.2 E2E 테스트 커버리지

| 구분 | 목표 |
|------|------|
| 주요 사용자 시나리오 | 100% |
| 기능 요구사항 (FR) | 100% 커버 |
| 비즈니스 규칙 (BR) | 100% 커버 |
| 에러 케이스 | 80% 커버 |

---

## 관련 문서

- 설계: `010-design.md`
- 추적성 매트릭스: `025-traceability-matrix.md`
- PRD: `.orchay/projects/orchay_web/prd.md`

---

<!--
TSK-03-01 테스트 명세서
Version: 1.0
Created: 2025-12-28
-->
