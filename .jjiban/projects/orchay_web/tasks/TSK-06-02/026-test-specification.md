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
| Task ID | TSK-06-02 |
| Task명 | Task Detail 패널 개선 |
| 설계 문서 참조 | `010-design.md` |
| 추적성 매트릭스 참조 | `025-traceability-matrix.md` |
| 작성일 | 2025-12-28 |
| 작성자 | Claude |

---

## 1. 테스트 전략 개요

### 1.1 테스트 범위

| 테스트 유형 | 범위 | 목표 커버리지 |
|------------|------|--------------|
| 단위 테스트 | 워크플로우 단계 계산, 진행률 계산, WBS 파싱 | 80% 이상 |
| E2E 테스트 | Detail 패널 UI, 카드 표시, 접기/펼치기 | 100% 시나리오 커버 |
| 매뉴얼 테스트 | UI/UX, 반응형, 시각적 확인 | 전체 화면 |

### 1.2 테스트 환경

| 항목 | 내용 |
|------|------|
| 테스트 프레임워크 (단위) | pytest |
| 테스트 프레임워크 (E2E) | Playwright |
| 브라우저 | Chromium (기본) |
| 베이스 URL | `http://localhost:8080` |

---

## 2. 단위 테스트 시나리오

### 2.1 테스트 케이스 목록

| 테스트 ID | 대상 | 시나리오 | 예상 결과 | 요구사항 |
|-----------|------|----------|----------|----------|
| UT-001 | get_workflow_step | status별 워크플로우 단계 반환 | 올바른 단계 반환 | FR-003, BR-001 |
| UT-002 | calculate_progress | status별 진행률 계산 | 올바른 진행률 반환 | FR-004, BR-002 |
| UT-003 | parse_requirements | WBS에서 requirements 파싱 | 요구사항 리스트 반환 | FR-005 |
| UT-004 | parse_tech_spec | WBS에서 tech-spec 파싱 | 기술스펙 딕셔너리 반환 | FR-006 |

### 2.2 테스트 케이스 상세

#### UT-001: get_workflow_step 워크플로우 단계 반환

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_server.py` |
| **테스트 블록** | `describe('get_workflow_step') → it('should return correct step for each status')` |
| **입력 데이터** | 각 status 코드: `[ ]`, `[bd]`, `[dd]`, `[ap]`, `[im]`, `[vf]`, `[xx]` |
| **검증 포인트** | status별 올바른 단계 인덱스 반환 |
| **관련 요구사항** | FR-003, BR-001 |

**테스트 데이터:**

| status | 예상 단계 | 예상 인덱스 |
|--------|----------|------------|
| `[ ]` | 시작 전 | 0 |
| `[bd]` | 설계 | 1 |
| `[dd]` | 설계 | 1 |
| `[ap]` | 승인 | 2 |
| `[im]` | 구현 | 3 |
| `[vf]` | 검증 | 4 |
| `[xx]` | 완료 | 5 |

#### UT-002: calculate_progress 진행률 계산

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_server.py` |
| **테스트 블록** | `describe('calculate_progress') → it('should return correct progress for each status')` |
| **입력 데이터** | 각 status 코드 |
| **검증 포인트** | status별 올바른 진행률(%) 반환 |
| **관련 요구사항** | FR-004, BR-002 |

**테스트 데이터:**

| status | 예상 진행률 |
|--------|------------|
| `[ ]` | 0% |
| `[bd]` | 15% |
| `[dd]` | 25% |
| `[ap]` | 40% |
| `[im]` | 60% |
| `[vf]` | 80% |
| `[xx]` | 100% |

#### UT-003: parse_requirements 요구사항 파싱

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_wbs_parser.py` |
| **테스트 블록** | `describe('parse_requirements') → it('should extract requirements from WBS')` |
| **입력 데이터** | WBS Task 항목 (requirements 포함) |
| **검증 포인트** | 요구사항 리스트 정확히 추출 |
| **관련 요구사항** | FR-005 |

#### UT-004: parse_tech_spec 기술스펙 파싱

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/test_wbs_parser.py` |
| **테스트 블록** | `describe('parse_tech_spec') → it('should extract tech-spec from WBS')` |
| **입력 데이터** | WBS Task 항목 (tech-spec, api-spec, ui-spec 포함) |
| **검증 포인트** | 각 스펙 딕셔너리 정확히 추출 |
| **관련 요구사항** | FR-006 |

---

## 3. E2E 테스트 시나리오

### 3.1 테스트 케이스 목록

| 테스트 ID | 시나리오 | 사전조건 | 실행 단계 | 예상 결과 | 요구사항 |
|-----------|----------|----------|----------|----------|----------|
| E2E-001 | 기본 정보 카드 표시 | 서버 실행 | Task 클릭 | 카드 UI에 기본 정보 표시 | FR-001, FR-002 |
| E2E-002 | 워크플로우 스테퍼 표시 | 서버 실행 | Task 클릭 | 스테퍼에 현재 단계 하이라이트 | FR-003, FR-004 |
| E2E-003 | 요구사항 섹션 표시 | 서버 실행 | 요구사항 섹션 펼치기 | PRD 참조 및 requirements 표시 | FR-005 |
| E2E-004 | 기술 스펙 섹션 표시 | 서버 실행 | 기술 스펙 섹션 펼치기 | tech-spec 내용 표시 | FR-006 |
| E2E-005 | 섹션 접기/펼치기 | 서버 실행 | 섹션 헤더 클릭 | 섹션 토글 동작 | FR-007 |

### 3.2 테스트 케이스 상세

#### E2E-001: 기본 정보 카드 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail_panel.py` |
| **테스트명** | `test_detail_panel_shows_basic_info_card` |
| **사전조건** | 웹서버 실행, WBS 로드 완료 |
| **data-testid 셀렉터** | |
| - Detail 패널 | `[data-testid="detail-panel"]` |
| - 기본 정보 카드 | `[data-testid="basic-info-card"]` |
| - 프로젝트 배지 | `[data-testid="project-badge"]` |
| - 카테고리 배지 | `[data-testid="category-badge"]` |
| - Task ID 배지 | `[data-testid="task-id-badge"]` |
| **실행 단계** | |
| 1 | 페이지 접속 (`http://localhost:8080`) |
| 2 | WBS 트리에서 Task 클릭 |
| 3 | Detail 패널 로드 확인 |
| **검증 포인트** | |
| - | 기본 정보 카드가 표시됨 |
| - | 프로젝트 배지에 "orchay_web" 표시 |
| - | 카테고리 배지에 "development" 표시 |
| - | Task ID 배지에 올바른 ID 표시 |
| **관련 요구사항** | FR-001, FR-002 |

#### E2E-002: 워크플로우 스테퍼 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail_panel.py` |
| **테스트명** | `test_detail_panel_shows_workflow_stepper` |
| **사전조건** | 웹서버 실행, Task 선택 |
| **data-testid 셀렉터** | |
| - 진행 상태 섹션 | `[data-testid="progress-section"]` |
| - 워크플로우 스테퍼 | `[data-testid="workflow-stepper"]` |
| - 스텝 아이템 | `[data-testid="step-item"]` |
| - 현재 스텝 | `[data-testid="current-step"]` |
| - 진행률 바 | `[data-testid="progress-bar"]` |
| **검증 포인트** | |
| - | 스테퍼가 표시됨 (시작 전, 설계, 구현, 완료 단계) |
| - | 현재 단계가 하이라이트됨 |
| - | 진행률 바가 올바른 퍼센트로 채워짐 |
| **관련 요구사항** | FR-003, FR-004 |

#### E2E-003: 요구사항 섹션 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail_panel.py` |
| **테스트명** | `test_detail_panel_shows_requirements_section` |
| **data-testid 셀렉터** | |
| - 요구사항 섹션 | `[data-testid="requirements-section"]` |
| - 섹션 헤더 | `[data-testid="requirements-header"]` |
| - PRD 참조 | `[data-testid="prd-ref"]` |
| - 요구사항 목록 | `[data-testid="requirements-list"]` |
| **실행 단계** | |
| 1 | Task 상세 패널 로드 |
| 2 | 요구사항 섹션 헤더 클릭 (펼치기) |
| **검증 포인트** | |
| - | 섹션이 펼쳐짐 |
| - | PRD 참조 링크 표시 |
| - | 요구사항 체크리스트 표시 |
| **관련 요구사항** | FR-005 |

#### E2E-004: 기술 스펙 섹션 표시

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail_panel.py` |
| **테스트명** | `test_detail_panel_shows_tech_spec_section` |
| **data-testid 셀렉터** | |
| - 기술 스펙 섹션 | `[data-testid="tech-spec-section"]` |
| - 기술 스펙 내용 | `[data-testid="tech-spec-content"]` |
| **실행 단계** | |
| 1 | Task 상세 패널 로드 |
| 2 | 기술 스펙 섹션 헤더 클릭 (펼치기) |
| **검증 포인트** | |
| - | tech-spec 내용 표시 |
| - | api-spec, ui-spec 등 표시 (있는 경우) |
| **관련 요구사항** | FR-006 |

#### E2E-005: 섹션 접기/펼치기

| 항목 | 내용 |
|------|------|
| **파일** | `orchay/tests/e2e/test_detail_panel.py` |
| **테스트명** | `test_section_collapse_expand` |
| **data-testid 셀렉터** | |
| - 섹션 헤더 | `[data-testid="*-header"]` |
| - 섹션 콘텐츠 | `[data-testid="*-content"]` |
| - 토글 아이콘 | `[data-testid="toggle-icon"]` |
| **실행 단계** | |
| 1 | 접힌 상태의 섹션 헤더 클릭 |
| 2 | 펼침 상태 확인 |
| 3 | 다시 헤더 클릭 |
| 4 | 접힌 상태 확인 |
| **검증 포인트** | |
| - | 클릭 시 섹션 토글 |
| - | 아이콘이 ▶ ↔ ▼ 회전 |
| - | transition 애니메이션 동작 |
| **관련 요구사항** | FR-007 |

---

## 4. UI 테스트케이스 (매뉴얼)

### 4.1 테스트 케이스 목록

| TC-ID | 테스트 항목 | 사전조건 | 테스트 단계 | 예상 결과 | 우선순위 | 요구사항 |
|-------|-----------|---------|-----------|----------|---------|----------|
| TC-001 | 기본 정보 카드 UI | 서버 실행 | Task 클릭 후 확인 | 카드 스타일 정상 | High | FR-001, FR-002 |
| TC-002 | 워크플로우 스테퍼 UI | 서버 실행 | 진행 상태 섹션 확인 | 스테퍼 및 진행률 바 정상 | High | FR-003, FR-004 |
| TC-003 | 요구사항 섹션 UI | 서버 실행 | 섹션 펼치기 | 요구사항 목록 정상 표시 | Medium | FR-005 |
| TC-004 | 기술 스펙 섹션 UI | 서버 실행 | 섹션 펼치기 | 기술 스펙 정상 표시 | Medium | FR-006 |
| TC-005 | 접기/펼치기 애니메이션 | 서버 실행 | 섹션 토글 | 부드러운 애니메이션 | Medium | FR-007 |
| TC-006 | 반응형 확인 | 서버 실행 | 브라우저 크기 조절 | 레이아웃 적응 | Low | - |
| TC-007 | 다크 테마 적용 | 서버 실행 | 전체 UI 확인 | 다크 테마 색상 일관성 | Low | - |

### 4.2 매뉴얼 테스트 상세

#### TC-001: 기본 정보 카드 UI

**테스트 목적**: Task Detail 패널의 기본 정보 카드가 올바른 스타일로 표시되는지 확인

**테스트 단계**:
1. 웹서버 접속 (`http://localhost:8080`)
2. WBS 트리에서 임의의 Task 클릭
3. Detail 패널에서 기본 정보 카드 확인

**예상 결과**:
- 카드가 `bg-gray-800 rounded-lg p-4` 스타일로 표시
- Task ID 배지가 프로젝트/카테고리/ID로 분리되어 표시
- 각 배지가 적절한 색상으로 구분됨

**검증 기준**:
- [ ] 카드 배경색이 다크 그레이
- [ ] 카드 모서리가 둥글게 처리
- [ ] 배지가 가로로 정렬되어 표시
- [ ] 제목, 우선순위, 담당자 등 기본 정보 표시

#### TC-002: 워크플로우 스테퍼 UI

**테스트 목적**: 워크플로우 스테퍼와 진행률 바가 올바르게 표시되는지 확인

**테스트 단계**:
1. 다양한 상태의 Task 선택 (`[ ]`, `[dd]`, `[im]`, `[xx]`)
2. 각각에 대해 스테퍼 표시 확인
3. 진행률 바 확인

**예상 결과**:
- 스테퍼에 4개 단계 표시 (시작 전, 설계, 구현, 완료)
- 현재 단계가 하이라이트됨
- 완료된 단계에 체크마크 또는 다른 스타일
- 진행률 바가 상태에 맞게 채워짐

**검증 기준**:
- [ ] 각 단계가 원형 아이콘으로 표시
- [ ] 단계 사이에 연결선 표시
- [ ] 현재 단계가 색상으로 구분됨
- [ ] 진행률 퍼센트가 표시됨

---

## 5. 테스트 데이터 (Fixture)

### 5.1 단위 테스트용 Mock 데이터

| 데이터 ID | 용도 | 값 |
|-----------|------|-----|
| MOCK-TASK-TODO | Todo 상태 Task | `{ id: 'TSK-01-01', status: '[ ]' }` |
| MOCK-TASK-DESIGN | 설계 중 Task | `{ id: 'TSK-01-02', status: '[dd]' }` |
| MOCK-TASK-IMPL | 구현 중 Task | `{ id: 'TSK-01-03', status: '[im]' }` |
| MOCK-TASK-DONE | 완료 Task | `{ id: 'TSK-01-04', status: '[xx]' }` |
| MOCK-WBS-REQS | 요구사항 포함 WBS | requirements 리스트 포함 |
| MOCK-WBS-SPECS | 기술스펙 포함 WBS | tech-spec, api-spec 포함 |

### 5.2 E2E 테스트용 시드 데이터

| 시드 ID | 용도 | 포함 데이터 |
|---------|------|------------|
| SEED-E2E-BASE | 기본 E2E 환경 | WP 2개, Task 6개 (다양한 상태) |
| SEED-E2E-DETAILED | 상세 정보 테스트 | 요구사항, 기술스펙 포함 Task |

---

## 6. data-testid 목록

> 프론트엔드 템플릿에 적용할 `data-testid` 속성 정의

### 6.1 Detail 패널 셀렉터

| data-testid | 요소 | 용도 |
|-------------|------|------|
| `detail-panel` | 패널 컨테이너 | 패널 로드 확인 |
| `basic-info-card` | 기본 정보 카드 | 기본 정보 표시 확인 |
| `project-badge` | 프로젝트 배지 | 프로젝트명 확인 |
| `category-badge` | 카테고리 배지 | 카테고리 확인 |
| `task-id-badge` | Task ID 배지 | Task ID 확인 |
| `progress-section` | 진행 상태 섹션 | 섹션 토글 |
| `workflow-stepper` | 워크플로우 스테퍼 | 스테퍼 확인 |
| `step-item` | 스텝 아이템 | 각 단계 확인 |
| `current-step` | 현재 스텝 | 현재 단계 확인 |
| `progress-bar` | 진행률 바 | 진행률 확인 |
| `requirements-section` | 요구사항 섹션 | 섹션 토글 |
| `requirements-header` | 요구사항 헤더 | 클릭 타겟 |
| `prd-ref` | PRD 참조 | PRD 링크 확인 |
| `requirements-list` | 요구사항 목록 | 목록 확인 |
| `tech-spec-section` | 기술 스펙 섹션 | 섹션 토글 |
| `tech-spec-content` | 기술 스펙 내용 | 내용 확인 |
| `toggle-icon` | 토글 아이콘 | 아이콘 회전 확인 |

---

## 7. 테스트 커버리지 목표

### 7.1 단위 테스트 커버리지

| 대상 | 목표 | 최소 |
|------|------|------|
| Lines | 80% | 70% |
| Branches | 75% | 65% |
| Functions | 85% | 75% |

### 7.2 E2E 테스트 커버리지

| 구분 | 목표 |
|------|------|
| 주요 사용자 시나리오 | 100% |
| 기능 요구사항 (FR) | 100% 커버 |
| 비즈니스 규칙 (BR) | 100% 커버 |

---

## 관련 문서

- 설계 문서: `010-design.md`
- 추적성 매트릭스: `025-traceability-matrix.md`
- PRD: `.jjiban/projects/orchay_web/prd.md`

---

<!--
author: Claude
Version: 1.0 (2025-12-28)
-->
