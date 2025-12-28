# TSK-01-02 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-01-02 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 관련 설계 | 010-design.md |
| 관련 추적 | 025-traceability-matrix.md |

---

## 1. 테스트 범위

### 1.1 테스트 대상

| 대상 | 설명 | 테스트 유형 |
|------|------|------------|
| base.html | 기본 레이아웃 템플릿 | 단위/E2E |
| index.html | 메인 페이지 템플릿 | 단위/E2E |
| CDN 로드 | HTMX, Tailwind CSS | E2E |
| 2열 레이아웃 | 트리/상세 패널 | E2E |

### 1.2 테스트 제외

| 제외 항목 | 사유 |
|----------|------|
| API 엔드포인트 | TSK-01-01 범위 |
| 트리 데이터 렌더링 | TSK-02-02 범위 |
| Task 상세 렌더링 | TSK-03-01 범위 |

---

## 2. 단위 테스트

### 2.1 템플릿 렌더링 테스트

#### TC-01: 다크테마 적용 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-01 |
| 테스트명 | 다크테마 클래스 적용 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. index.html 렌더링<br>2. body 요소 클래스 확인 |
| 예상 결과 | body에 `bg-gray-900 text-gray-100` 클래스 존재 |
| 우선순위 | 높음 |

```python
# test_templates.py
def test_dark_theme_applied(client):
    response = client.get("/")
    assert "bg-gray-900" in response.text
    assert "text-gray-100" in response.text
```

#### TC-02: 2열 레이아웃 구조 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-02 |
| 테스트명 | 2열 레이아웃 구조 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. index.html 렌더링<br>2. tree-panel, detail-panel 존재 확인 |
| 예상 결과 | 두 패널 모두 존재하고 w-1/2 클래스 보유 |
| 우선순위 | 높음 |

```python
def test_two_column_layout(client):
    response = client.get("/")
    assert 'id="tree-panel"' in response.text
    assert 'id="detail-panel"' in response.text
    assert "w-1/2" in response.text
```

#### TC-03: HTMX CDN 로드

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-03 |
| 테스트명 | HTMX CDN 스크립트 포함 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. base.html 렌더링<br>2. HTMX CDN URL 확인 |
| 예상 결과 | unpkg.com/htmx.org 스크립트 태그 존재 |
| 우선순위 | 높음 |

```python
def test_htmx_cdn_loaded(client):
    response = client.get("/")
    assert "unpkg.com/htmx.org" in response.text
```

#### TC-04: Tailwind CSS CDN 로드

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-04 |
| 테스트명 | Tailwind CSS CDN 스크립트 포함 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. base.html 렌더링<br>2. Tailwind CDN URL 확인 |
| 예상 결과 | cdn.tailwindcss.com 스크립트 태그 존재 |
| 우선순위 | 높음 |

```python
def test_tailwind_cdn_loaded(client):
    response = client.get("/")
    assert "cdn.tailwindcss.com" in response.text
```

#### TC-05: 헤더 프로젝트명 표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-05 |
| 테스트명 | 헤더에 프로젝트명 표시 확인 |
| 사전 조건 | project_name 컨텍스트 전달 |
| 테스트 단계 | 1. 컨텍스트와 함께 렌더링<br>2. 헤더 영역 확인 |
| 예상 결과 | 헤더에 프로젝트명 표시 |
| 우선순위 | 중간 |

```python
def test_header_project_name(client):
    response = client.get("/")
    assert "orchay - " in response.text
```

#### TC-06: 헤더 모드 표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-06 |
| 테스트명 | 헤더에 실행 모드 표시 확인 |
| 사전 조건 | mode 컨텍스트 전달 |
| 테스트 단계 | 1. 컨텍스트와 함께 렌더링<br>2. 모드 배지 확인 |
| 예상 결과 | MODE: {mode} 배지 표시 |
| 우선순위 | 중간 |

```python
def test_header_mode_badge(client):
    response = client.get("/")
    assert "MODE:" in response.text
```

#### TC-07: Worker 바 영역 존재

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-07 |
| 테스트명 | Worker 상태 바 영역 존재 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. index.html 렌더링<br>2. workers-bar 요소 확인 |
| 예상 결과 | id="workers-bar" 요소 존재 |
| 우선순위 | 높음 |

```python
def test_workers_bar_exists(client):
    response = client.get("/")
    assert 'id="workers-bar"' in response.text
```

#### TC-08: 트리 패널 HTMX 속성

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-08 |
| 테스트명 | 트리 패널에 HTMX 속성 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. index.html 렌더링<br>2. tree-panel의 hx-* 속성 확인 |
| 예상 결과 | hx-get, hx-trigger 속성 존재 |
| 우선순위 | 높음 |

```python
def test_tree_panel_htmx_attributes(client):
    response = client.get("/")
    assert 'hx-get="/api/tree"' in response.text
    assert 'hx-trigger="load, every 5s"' in response.text
```

#### TC-09: 상세 패널 기본 상태

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-09 |
| 테스트명 | 상세 패널 기본 메시지 확인 |
| 사전 조건 | 템플릿 렌더링 환경 준비 |
| 테스트 단계 | 1. index.html 렌더링<br>2. detail-panel 내용 확인 |
| 예상 결과 | "Task를 선택하세요" 메시지 표시 |
| 우선순위 | 중간 |

```python
def test_detail_panel_default_message(client):
    response = client.get("/")
    assert "Task를 선택하세요" in response.text
```

---

## 3. E2E 테스트

#### TC-10: 반응형 레이아웃

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-10 |
| 테스트명 | 반응형 레이아웃 동작 확인 |
| 사전 조건 | 브라우저 환경 준비 |
| 테스트 단계 | 1. 데스크톱 뷰포트에서 확인<br>2. 모바일 뷰포트로 변경<br>3. 레이아웃 변화 확인 |
| 예상 결과 | 뷰포트에 따라 레이아웃 변경 |
| 우선순위 | 낮음 |

```python
# test_e2e.py (Playwright)
async def test_responsive_layout(page):
    await page.goto("http://localhost:8080")

    # Desktop
    await page.set_viewport_size({"width": 1280, "height": 720})
    tree_panel = await page.query_selector("#tree-panel")
    assert await tree_panel.is_visible()

    # Mobile
    await page.set_viewport_size({"width": 375, "height": 667})
    # 모바일에서도 기본적으로 표시됨 (추후 토글 구현 시 변경)
```

---

## 4. 수동 테스트

### 4.1 시각적 확인 체크리스트

| 번호 | 확인 항목 | 합격 기준 | 결과 |
|------|----------|----------|------|
| M-01 | 다크테마 배경색 | 어두운 배경(#111827)으로 표시 | [ ] |
| M-02 | 텍스트 가독성 | 밝은 텍스트로 명확히 읽힘 | [ ] |
| M-03 | 2열 레이아웃 | 좌우 50%씩 분할 표시 | [ ] |
| M-04 | 헤더 표시 | 프로젝트명, 모드 배지 표시 | [ ] |
| M-05 | Worker 바 위치 | 헤더 아래, 메인 콘텐츠 위 | [ ] |
| M-06 | 스켈레톤 로딩 | 초기 로딩 시 애니메이션 표시 | [ ] |
| M-07 | 경계선 구분 | 영역간 border 표시 | [ ] |

### 4.2 브라우저 호환성

| 브라우저 | 버전 | 테스트 결과 |
|----------|------|------------|
| Chrome | 최신 | [ ] 통과 / [ ] 실패 |
| Firefox | 최신 | [ ] 통과 / [ ] 실패 |
| Safari | 최신 | [ ] 통과 / [ ] 실패 |
| Edge | 최신 | [ ] 통과 / [ ] 실패 |

---

## 5. 테스트 환경

### 5.1 필수 환경

```bash
# Python 테스트
pytest
pytest-asyncio
httpx  # FastAPI 테스트 클라이언트

# E2E 테스트 (선택)
playwright
```

### 5.2 테스트 실행

```bash
# 단위 테스트
cd orchay && pytest tests/test_templates.py -v

# E2E 테스트 (선택)
cd orchay && pytest tests/test_e2e.py -v
```

---

## 6. 테스트 결과 요약

| 구분 | 전체 | 통과 | 실패 | 커버리지 |
|------|------|------|------|----------|
| 단위 테스트 | 9 | - | - | - |
| E2E 테스트 | 1 | - | - | - |
| 수동 테스트 | 7 | - | - | - |
| **총계** | **17** | - | - | - |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
