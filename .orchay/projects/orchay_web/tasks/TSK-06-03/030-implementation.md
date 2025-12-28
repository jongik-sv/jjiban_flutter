# TSK-06-03 - 구현 보고서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-06-03 |
| Task명 | 문서 테이블 |
| 구현 완료일 | 2025-12-28 |
| 상태 | 구현 완료 |

---

## 1. 구현 요약

### 1.1 구현 범위

| 구현 항목 | 상태 | 비고 |
|----------|------|------|
| 문서 메타정보 API 확장 | ✅ | name, type, size, modified |
| 크기 포맷팅 함수 | ✅ | B, KB, MB 자동 변환 (BR-02) |
| 날짜 포맷팅 함수 | ✅ | YYYY-MM-DD 형식 (BR-03) |
| 문서 테이블 UI | ✅ | 4컬럼 (문서명, 타입, 크기, 수정일) |
| 반응형 테이블 | ✅ | sm: 3컬럼, md: 4컬럼 |
| 키보드 접근성 | ✅ | Enter 키로 문서 열기 |
| Document Viewer 연동 | ✅ | 기존 openDocument() 유지 |

### 1.2 변경 파일

| 파일 | 변경 내용 |
|------|----------|
| `orchay/src/orchay/web/server.py` | `format_file_size()`, `format_date()` 추가, `get_task_documents()` 메타정보 반환 확장 |
| `orchay/src/orchay/web/templates/partials/detail.html` | 문서 테이블 UI 구현 |
| `orchay/tests/test_web_server.py` | 테스트 업데이트 (메타정보 필드 검증) |

---

## 2. 설계 → 구현 매핑

### 2.1 요구사항 커버리지

| 요구사항 ID | 설계 섹션 | 구현 | 테스트 |
|------------|----------|------|--------|
| UC-01 | 3.2 문서 목록 조회 | `get_task_documents()` 메타정보 반환 | test_get_task_documents_* |
| UC-02 | 3.2 문서 상세 보기 | 테이블 행 클릭 → `openDocument()` | 기존 테스트 유지 |
| UC-03 | 3.2 접기/펼치기 | 기존 `toggleSection()` 활용 | test_document_viewer_* |

### 2.2 비즈니스 규칙 구현

| 규칙 ID | 구현 |
|---------|------|
| BR-01 | `ALLOWED_EXTENSIONS` 필터링 유지 |
| BR-02 | `format_file_size(size_bytes)` → "8.3 KB" |
| BR-03 | `format_date(timestamp)` → "2025-12-28" |

---

## 3. 코드 변경 상세

### 3.1 크기 포맷팅 함수

```python
# orchay/src/orchay/web/server.py
def format_file_size(size_bytes: int) -> str:
    """파일 크기를 사람이 읽기 쉬운 형태로 변환 (TSK-06-03 BR-02)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
```

### 3.2 날짜 포맷팅 함수

```python
def format_date(timestamp: float) -> str:
    """Unix timestamp를 YYYY-MM-DD 형식으로 변환 (TSK-06-03 BR-03)."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
```

### 3.3 get_task_documents() 확장

```python
def get_task_documents(
    task_id: str,
    base_path: Path | None = None,
    project_name: str = "",
) -> list[dict[str, str | int]]:
    """Task 관련 문서 목록 조회 (TSK-06-03: 메타정보 포함)."""
    # ...
    docs.append({
        "name": f.name,
        "type": suffix[1:].upper(),  # ".md" -> "MD"
        "size": size,
        "size_formatted": format_file_size(size),
        "modified": modified,
        "modified_formatted": format_date(modified) if modified > 0 else "-",
    })
```

### 3.4 테이블 UI (detail.html)

```html
<table class="w-full text-sm" data-testid="documents-table">
    <thead>
        <tr class="text-left text-orchay-muted border-b border-orchay-border">
            <th class="pb-2">문서명</th>
            <th class="pb-2 w-16 text-center">타입</th>
            <th class="pb-2 w-20 text-right hidden sm:table-cell">크기</th>
            <th class="pb-2 w-28 text-right hidden md:table-cell">수정일</th>
        </tr>
    </thead>
    <tbody>
        {% for doc in documents %}
        <tr class="cursor-pointer hover:bg-gray-700 ..."
            onclick="openDocument('{{ task.id }}', '{{ doc.name }}')">
            <!-- 문서명, 타입 배지, 크기, 수정일 -->
        </tr>
        {% endfor %}
    </tbody>
</table>
```

---

## 4. 테스트 결과

### 4.1 단위 테스트

| 테스트 | 결과 |
|--------|------|
| test_web_server.py (66 tests) | ✅ PASSED |
| test_get_task_documents_returns_existing_files | ✅ 메타정보 필드 검증 |
| test_get_task_documents_includes_images | ✅ 타입 필드 검증 |

### 4.2 테스트 커버리지

- 관련 테스트 66개 통과
- 새 필드 (name, type, size, size_formatted, modified, modified_formatted) 검증 추가

---

## 5. 알려진 이슈

없음

---

## 6. 다음 단계

- `/wf:audit`: 코드 리뷰
- `/wf:test`: 통합 테스트 실행
- `/wf:done`: 작업 완료

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
