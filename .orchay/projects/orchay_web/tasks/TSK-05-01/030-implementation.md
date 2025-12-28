# TSK-05-01 구현 보고서

## 0. 문서 메타데이터

| 항목 | 내용 |
|------|------|
| 문서명 | `030-implementation.md` |
| Task ID | TSK-05-01 |
| Task 명 | Document Viewer 구현 |
| 작성일 | 2025-12-28 |
| 작성자 | Claude |
| 참조 설계서 | `./010-design.md` |
| 구현 상태 | ✅ 완료 |

---

## 1. 구현 개요

### 1.1 구현 목적

Task 상세 패널의 Documents 섹션에서 문서를 클릭하면 모달 팝업으로 내용을 바로 확인할 수 있는 Document Viewer 기능 구현.

### 1.2 구현 범위

**포함된 기능:**
- Document API 엔드포인트 (`GET /api/document/{task_id}/{doc_name}`)
- 모달 팝업 UI (열기/닫기)
- 마크다운 렌더링 (marked.js CDN)
- Mermaid 다이어그램 렌더링 (mermaid.js CDN)
- 이미지 파일 표시 (png, jpg, gif, webp)
- ESC 키로 모달 닫기
- Path traversal 보안 처리

**제외된 기능:**
- PDF 파일 지원 (향후 과제)
- 문서 편집 기능 (읽기 전용)

### 1.3 구현 유형

- [x] Full-stack (Backend + Frontend)

### 1.4 기술 스택

- **Backend**: Python 3.12, FastAPI, Jinja2
- **Frontend**: HTML, JavaScript, Tailwind CSS (CDN)
- **Libraries**: marked.js, mermaid.js (CDN)
- **Testing**: pytest, pytest-asyncio, httpx

---

## 2. Backend 구현 결과

### 2.1 구현된 컴포넌트

#### 2.1.1 API 엔드포인트

**파일**: `orchay/src/orchay/web/server.py:237-293`

| HTTP Method | Endpoint | 설명 |
|-------------|----------|------|
| GET | `/api/document/{task_id}/{doc_name}` | 문서/이미지 파일 조회 |

#### 2.1.2 주요 로직

**ALLOWED_EXTENSIONS** (line 28):
```python
ALLOWED_EXTENSIONS = {".md", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
```

**_get_document** 함수 (line 238-293):
1. Path traversal 검증 (`is_relative_to`)
2. 확장자 검증 (`ALLOWED_EXTENSIONS`)
3. 파일 존재 확인
4. 응답 타입 결정 (마크다운 → PlainTextResponse, 이미지 → FileResponse)

#### 2.1.3 get_task_documents 수정

**파일**: `orchay/src/orchay/web/server.py:80-110`

- 기존: `.md` 파일만 반환
- 변경: `ALLOWED_EXTENSIONS`에 포함된 모든 파일 반환 (이미지 포함)

### 2.2 단위 테스트 결과

**파일**: `orchay/tests/test_web_server.py:1418-1665`

#### 2.2.1 테스트 시나리오 매핑

| 테스트 ID | 시나리오 | 결과 |
|-----------|----------|------|
| UT-01 | 마크다운 문서 API 정상 응답 | ✅ Pass |
| UT-02 | 허용되지 않는 확장자 차단 (4건) | ✅ Pass |
| UT-03 | Path traversal 차단 (3건) | ✅ Pass |
| UT-04 | 이미지 파일 API 정상 응답 | ✅ Pass |
| UT-05 | 존재하지 않는 파일 404 | ✅ Pass |

#### 2.2.2 테스트 실행 결과

```
tests/test_web_server.py::test_get_markdown_document PASSED
tests/test_web_server.py::test_reject_disallowed_extensions[.pdf] PASSED
tests/test_web_server.py::test_reject_disallowed_extensions[.exe] PASSED
tests/test_web_server.py::test_reject_disallowed_extensions[.py] PASSED
tests/test_web_server.py::test_reject_disallowed_extensions[.html] PASSED
tests/test_web_server.py::test_block_path_traversal[../../../etc/passwd.md] PASSED
tests/test_web_server.py::test_block_path_traversal[..%2F..%2F..%2Fetc%2Fpasswd.md] PASSED
tests/test_web_server.py::test_block_path_traversal[test/../../../etc/passwd.md] PASSED
tests/test_web_server.py::test_get_image_document PASSED
tests/test_web_server.py::test_document_not_found PASSED
tests/test_web_server.py::test_get_task_documents_includes_images PASSED

11 passed
```

---

## 3. Frontend 구현 결과

### 3.1 구현된 화면

#### 3.1.1 모달 HTML

**파일**: `orchay/src/orchay/web/templates/index.html:51-80`

| 요소 | ID | 설명 |
|------|-----|------|
| 모달 컨테이너 | `document-modal` | 전체 모달 래퍼 |
| 배경 오버레이 | `document-modal-backdrop` | 클릭 시 모달 닫기 |
| 콘텐츠 영역 | `document-content` | 렌더링된 문서 표시 |
| 닫기 버튼 | `document-close-btn` | X 버튼 |

#### 3.1.2 JavaScript 함수

**파일**: `orchay/src/orchay/web/templates/index.html:268-344`

| 함수 | 설명 |
|------|------|
| `openDocument(taskId, docName)` | 문서/이미지 모달 열기 |
| `closeDocument()` | 모달 닫기 |
| ESC 키 핸들러 | 모달 열려있을 때 ESC로 닫기 |

#### 3.1.3 Documents 섹션 클릭 이벤트

**파일**: `orchay/src/orchay/web/templates/partials/detail.html:71-89`

- 문서 아이템에 `onclick="openDocument('{{ task.id }}', '{{ doc }}')"` 추가
- 호버 효과 및 커서 포인터 스타일 추가
- 파일 확장자에 따른 아이콘 분기 (📄 마크다운, 🖼️ 이미지)

### 3.2 CDN 라이브러리

**파일**: `orchay/src/orchay/web/templates/base.html:18-22`

| 라이브러리 | 용도 | 설정 |
|-----------|------|------|
| marked.js | 마크다운 렌더링 | CDN |
| mermaid.js | 다이어그램 렌더링 | startOnLoad: false, theme: 'dark' |

### 3.3 UI/모달 테스트 결과

| 테스트 ID | 시나리오 | 결과 |
|-----------|----------|------|
| test_document_viewer_modal_exists | 모달 HTML 요소 존재 확인 | ✅ Pass |
| test_document_viewer_javascript_functions | JS 함수 정의 확인 | ✅ Pass |

---

## 4. 요구사항 커버리지

### 4.1 기능 요구사항 (PRD 3.5)

| 요구사항 | 테스트 ID | 결과 |
|----------|-----------|------|
| 문서 API 엔드포인트 | UT-01, UT-04, UT-05 | ✅ |
| MD 렌더링 (marked.js) | E2E (수동) | ✅ |
| Mermaid 지원 | E2E (수동) | ✅ |
| 이미지 표시 | UT-04 | ✅ |
| 모달 팝업 UI | test_document_viewer_modal_exists | ✅ |
| ESC 키로 닫기 | test_document_viewer_javascript_functions | ✅ |
| Path traversal 차단 | UT-03 | ✅ |

### 4.2 비즈니스 규칙 (010-design.md 섹션 8)

| 규칙 ID | 설명 | 테스트 ID | 결과 |
|---------|------|-----------|------|
| BR-01 | 허용된 확장자만 제공 | UT-02 | ✅ |
| BR-02 | Path traversal 차단 | UT-03 | ✅ |
| BR-03 | 마크다운은 PlainTextResponse | UT-01 | ✅ |
| BR-04 | 이미지는 FileResponse | UT-04 | ✅ |

---

## 5. 품질 지표

| 항목 | 목표 | 결과 |
|------|------|------|
| 단위 테스트 통과 | 100% | ✅ 11/11 Pass |
| 보안 검증 (Path traversal) | 100% 차단 | ✅ Pass |
| 확장자 검증 | 허용 외 차단 | ✅ Pass |

---

## 6. 파일 변경 목록

| 파일 | 변경 유형 | 설명 |
|------|----------|------|
| `orchay/src/orchay/web/server.py` | 수정 | Document API 추가, get_task_documents 수정 |
| `orchay/src/orchay/web/templates/index.html` | 수정 | 모달 HTML + JS 추가 |
| `orchay/src/orchay/web/templates/partials/detail.html` | 수정 | 문서 클릭 이벤트 추가 |
| `orchay/tests/test_web_server.py` | 수정 | TSK-05-01 테스트 케이스 추가 |

---

## 7. 알려진 이슈

| 이슈 | 심각도 | 설명 |
|------|--------|------|
| PDF 미지원 | 🟡 Low | 향후 과제로 분류 |
| 대용량 문서 | 🟡 Low | 매우 큰 문서는 렌더링 지연 가능 |

---

## 8. 구현 완료 체크리스트

### Backend
- [x] API 엔드포인트 구현 완료
- [x] Path traversal 보안 검증
- [x] 확장자 검증
- [x] 단위 테스트 작성 및 통과

### Frontend
- [x] 모달 UI 구현 완료
- [x] 마크다운 렌더링 (marked.js)
- [x] Mermaid 다이어그램 렌더링
- [x] 이미지 표시
- [x] ESC/X/배경 클릭으로 닫기

### 통합
- [x] Backend-Frontend 연동 검증
- [x] 설계서 요구사항 충족 확인
- [x] 문서화 완료

---

## 9. 다음 단계

- `/wf:audit TSK-05-01` - 코드 리뷰 (선택)
- `/wf:done TSK-05-01` - 작업 완료

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
