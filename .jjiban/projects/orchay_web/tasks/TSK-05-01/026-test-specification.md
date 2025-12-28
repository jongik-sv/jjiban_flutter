# TSK-05-01 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-05-01 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 단위 테스트

### UT-01: 마크다운 문서 API 정상 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | UT-01 |
| 대상 | `GET /api/document/{task_id}/{doc_name}` |
| 목적 | 마크다운 파일 요청 시 PlainTextResponse 반환 확인 |

**사전 조건:**
- `.jjiban/projects/{project}/tasks/TSK-TEST/test.md` 파일 존재

**테스트 단계:**
1. `GET /api/document/TSK-TEST/test.md` 요청
2. 응답 상태 코드 확인
3. Content-Type 확인
4. 응답 본문 확인

**기대 결과:**
- 상태 코드: 200
- Content-Type: `text/plain; charset=utf-8`
- 본문: 마크다운 텍스트 원본

**테스트 코드:**
```python
async def test_get_markdown_document(client: AsyncClient):
    # Arrange
    task_id = "TSK-TEST"
    doc_name = "test.md"

    # Act
    response = await client.get(f"/api/document/{task_id}/{doc_name}")

    # Assert
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "# Test" in response.text
```

---

### UT-02: 허용되지 않는 확장자 차단

| 항목 | 내용 |
|------|------|
| 테스트 ID | UT-02 |
| 대상 | `GET /api/document/{task_id}/{doc_name}` |
| 목적 | .pdf, .exe 등 허용되지 않는 확장자 요청 시 400 반환 |

**테스트 단계:**
1. `GET /api/document/TSK-TEST/file.pdf` 요청
2. 응답 상태 코드 확인

**기대 결과:**
- 상태 코드: 400
- 메시지: "Unsupported file type"

**테스트 코드:**
```python
@pytest.mark.parametrize("ext", [".pdf", ".exe", ".py", ".html"])
async def test_reject_disallowed_extensions(client: AsyncClient, ext: str):
    response = await client.get(f"/api/document/TSK-TEST/file{ext}")
    assert response.status_code == 400
    assert "Unsupported file type" in response.text
```

---

### UT-03: Path Traversal 차단

| 항목 | 내용 |
|------|------|
| 테스트 ID | UT-03 |
| 대상 | `GET /api/document/{task_id}/{doc_name}` |
| 목적 | `../` 포함 경로 요청 시 403 반환 |

**테스트 단계:**
1. `GET /api/document/TSK-TEST/../../../etc/passwd` 요청
2. 응답 상태 코드 확인

**기대 결과:**
- 상태 코드: 403
- 메시지: "Access denied"

**테스트 코드:**
```python
@pytest.mark.parametrize("malicious_path", [
    "../../../etc/passwd",
    "..\\..\\windows\\system32\\config\\sam",
    "test/../../../etc/passwd",
])
async def test_block_path_traversal(client: AsyncClient, malicious_path: str):
    response = await client.get(f"/api/document/TSK-TEST/{malicious_path}")
    assert response.status_code == 403
    assert "Access denied" in response.text
```

---

### UT-04: 이미지 파일 API 정상 응답

| 항목 | 내용 |
|------|------|
| 테스트 ID | UT-04 |
| 대상 | `GET /api/document/{task_id}/{doc_name}` |
| 목적 | 이미지 파일 요청 시 FileResponse 반환 확인 |

**사전 조건:**
- `.jjiban/projects/{project}/tasks/TSK-TEST/image.png` 파일 존재

**테스트 단계:**
1. `GET /api/document/TSK-TEST/image.png` 요청
2. 응답 상태 코드 확인
3. Content-Type 확인

**기대 결과:**
- 상태 코드: 200
- Content-Type: `image/png`

**테스트 코드:**
```python
@pytest.mark.parametrize("ext,mime", [
    (".png", "image/png"),
    (".jpg", "image/jpeg"),
    (".gif", "image/gif"),
    (".webp", "image/webp"),
])
async def test_get_image_document(client: AsyncClient, ext: str, mime: str):
    response = await client.get(f"/api/document/TSK-TEST/image{ext}")
    assert response.status_code == 200
    assert mime in response.headers["content-type"]
```

---

### UT-05: 존재하지 않는 파일 404

| 항목 | 내용 |
|------|------|
| 테스트 ID | UT-05 |
| 대상 | `GET /api/document/{task_id}/{doc_name}` |
| 목적 | 존재하지 않는 파일 요청 시 404 반환 |

**테스트 코드:**
```python
async def test_document_not_found(client: AsyncClient):
    response = await client.get("/api/document/TSK-TEST/nonexistent.md")
    assert response.status_code == 404
    assert "not found" in response.text.lower()
```

---

## 2. E2E 테스트

### E2E-01: 마크다운 렌더링 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | E2E-01 |
| 대상 | Document Viewer 모달 |
| 목적 | 마크다운이 HTML로 렌더링되는지 확인 |

**사전 조건:**
- 웹서버 실행 중
- Task 상세 패널에 .md 문서 존재

**테스트 단계:**
1. Task 상세 패널 열기
2. .md 문서 클릭
3. 모달 열림 확인
4. 마크다운 렌더링 확인 (h1, p, code 등)

**기대 결과:**
- 모달에 렌더링된 HTML 표시
- `# Title` → `<h1>Title</h1>`
- 코드블록 → `<pre><code>`

**Playwright 테스트:**
```python
async def test_markdown_rendering(page: Page):
    await page.goto("http://localhost:8080")
    await page.click("[data-testid='document-item']")
    await page.wait_for_selector("#document-modal")

    content = await page.locator("#document-content").inner_html()
    assert "<h1>" in content or "<h2>" in content
```

---

### E2E-02: Mermaid 다이어그램 렌더링

| 항목 | 내용 |
|------|------|
| 테스트 ID | E2E-02 |
| 대상 | Document Viewer 모달 |
| 목적 | Mermaid 코드블록이 SVG로 렌더링되는지 확인 |

**사전 조건:**
- Mermaid 코드블록이 포함된 .md 파일 존재

**테스트 단계:**
1. Mermaid 포함 문서 클릭
2. 모달 열림 확인
3. SVG 요소 존재 확인

**기대 결과:**
- `.mermaid` 클래스 또는 `<svg>` 요소 존재

**Playwright 테스트:**
```python
async def test_mermaid_rendering(page: Page):
    await page.goto("http://localhost:8080")
    await page.click("[data-testid='document-with-mermaid']")
    await page.wait_for_selector("#document-modal")

    # Mermaid 렌더링 대기
    await page.wait_for_selector("svg", timeout=5000)

    svg_count = await page.locator("svg").count()
    assert svg_count > 0
```

---

### E2E-03: 이미지 표시 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | E2E-03 |
| 대상 | Document Viewer 모달 |
| 목적 | 이미지 파일이 모달에 표시되는지 확인 |

**테스트 단계:**
1. 이미지 파일 클릭
2. 모달 열림 확인
3. `<img>` 요소 존재 확인

**Playwright 테스트:**
```python
async def test_image_display(page: Page):
    await page.goto("http://localhost:8080")
    await page.click("[data-testid='image-item']")
    await page.wait_for_selector("#document-modal")

    img = page.locator("#document-content img")
    assert await img.count() == 1
    assert await img.get_attribute("src") is not None
```

---

### E2E-04: 모달 열기/닫기

| 항목 | 내용 |
|------|------|
| 테스트 ID | E2E-04 |
| 대상 | Document Viewer 모달 |
| 목적 | 모달 열기 및 X 버튼/배경 클릭으로 닫기 확인 |

**테스트 단계:**
1. 문서 클릭 → 모달 열림 확인
2. X 버튼 클릭 → 모달 닫힘 확인
3. 문서 재클릭 → 모달 열림 확인
4. 배경 클릭 → 모달 닫힘 확인

**Playwright 테스트:**
```python
async def test_modal_open_close(page: Page):
    await page.goto("http://localhost:8080")

    # 열기
    await page.click("[data-testid='document-item']")
    await page.wait_for_selector("#document-modal:not(.hidden)")

    # X 버튼으로 닫기
    await page.click("#document-close-btn")
    await page.wait_for_selector("#document-modal.hidden")

    # 다시 열기
    await page.click("[data-testid='document-item']")
    await page.wait_for_selector("#document-modal:not(.hidden)")

    # 배경 클릭으로 닫기
    await page.click("#document-modal-backdrop")
    await page.wait_for_selector("#document-modal.hidden")
```

---

### E2E-05: ESC 키로 모달 닫기

| 항목 | 내용 |
|------|------|
| 테스트 ID | E2E-05 |
| 대상 | Document Viewer 모달 |
| 목적 | ESC 키로 모달이 닫히는지 확인 |

**테스트 단계:**
1. 문서 클릭 → 모달 열림 확인
2. ESC 키 누름
3. 모달 닫힘 확인

**Playwright 테스트:**
```python
async def test_esc_closes_modal(page: Page):
    await page.goto("http://localhost:8080")

    await page.click("[data-testid='document-item']")
    await page.wait_for_selector("#document-modal:not(.hidden)")

    await page.keyboard.press("Escape")
    await page.wait_for_selector("#document-modal.hidden")
```

---

## 3. 수동 테스트

### MT-01: 반응형 모달 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | MT-01 |
| 대상 | Document Viewer 모달 |
| 목적 | 다양한 화면 크기에서 모달이 적절히 표시되는지 확인 |

**테스트 단계:**
1. 데스크톱 (1920x1080)에서 모달 열기 → 너비 확인
2. 태블릿 (768x1024)에서 모달 열기 → 너비 확인
3. 모바일 (375x667)에서 모달 열기 → 너비 확인

**확인 항목:**
- 데스크톱: max-width 900px, 중앙 정렬
- 태블릿: 너비 90%
- 모바일: 너비 95%

---

### MT-02: 다크 테마 Mermaid 확인

| 항목 | 내용 |
|------|------|
| 테스트 ID | MT-02 |
| 대상 | Mermaid 다이어그램 |
| 목적 | 다크 테마에서 다이어그램이 잘 보이는지 확인 |

**확인 항목:**
- 배경색과 대비되는 색상
- 텍스트 가독성

---

## 4. 테스트 커버리지 요약

| 카테고리 | 테스트 수 | 자동화 | 수동 |
|---------|---------|--------|------|
| 단위 테스트 | 5 | 5 | 0 |
| E2E 테스트 | 5 | 5 | 0 |
| 수동 테스트 | 2 | 0 | 2 |
| **합계** | **12** | **10** | **2** |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
