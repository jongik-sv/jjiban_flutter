# TSK-06-03 - 테스트 명세서

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-06-03 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |

---

## 1. 테스트 범위

### 1.1 테스트 대상

| 컴포넌트 | 테스트 유형 | 우선순위 |
|---------|------------|----------|
| `get_task_documents()` 확장 | 단위 테스트 | 높음 |
| 문서 테이블 UI | E2E 테스트 | 높음 |
| 접기/펼치기 기능 | E2E 테스트 | 중간 |
| Document Viewer 연동 | E2E 테스트 | 높음 |

### 1.2 테스트 제외 항목

- Document Viewer 모달 내부 동작 (TSK-05-01에서 테스트됨)
- Task Detail 패널 기본 레이아웃 (TSK-06-02에서 테스트)

---

## 2. 단위 테스트

### TC-001: 문서 메타정보 조회

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-001 |
| 테스트명 | get_task_documents_with_metadata |
| 대상 | `server.py::get_task_documents()` |
| 우선순위 | 높음 |

**사전 조건:**
- Task 디렉토리에 테스트 파일 존재

**테스트 데이터:**
```python
# 테스트 파일 생성
files = [
    "010-design.md",       # 8500 bytes
    "diagram.png",         # 45000 bytes
]
```

**테스트 단계:**
1. Task 디렉토리에 테스트 파일 생성
2. `get_task_documents_with_metadata(task_id)` 호출
3. 반환값 검증

**예상 결과:**
```python
[
    {
        "name": "010-design.md",
        "type": "MD",
        "size": "8.3 KB",
        "modified": "2025-12-28"
    },
    {
        "name": "diagram.png",
        "type": "PNG",
        "size": "43.9 KB",
        "modified": "2025-12-28"
    }
]
```

**판정 기준:**
- 파일명 정확
- 타입 대문자 표시
- 크기 포맷팅 정확 (KB/MB)
- 날짜 형식 YYYY-MM-DD

---

### TC-002: 빈 디렉토리 처리

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-002 |
| 테스트명 | get_task_documents_empty |
| 대상 | `server.py::get_task_documents()` |
| 우선순위 | 중간 |

**테스트 단계:**
1. 빈 Task 디렉토리 생성
2. `get_task_documents_with_metadata(task_id)` 호출
3. 빈 리스트 반환 확인

**예상 결과:**
```python
[]
```

---

### TC-003: 비허용 확장자 필터링

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-003 |
| 테스트명 | filter_disallowed_extensions |
| 대상 | `server.py::get_task_documents()` |
| 우선순위 | 높음 |

**테스트 데이터:**
```python
files = [
    "design.md",     # 허용
    "script.py",     # 비허용
    "image.png",     # 허용
    "data.json",     # 비허용
]
```

**예상 결과:**
- `design.md`와 `image.png`만 반환

---

## 3. E2E 테스트

### TC-004: 문서 테이블 표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-004 |
| 테스트명 | documents_table_display |
| 대상 | detail.html Documents 섹션 |
| 우선순위 | 높음 |

**테스트 단계:**
1. 브라우저에서 `/` 접속
2. Task 클릭하여 Detail 패널 로드
3. Documents 섹션 확인

**검증 항목:**
- [ ] 테이블 헤더 4컬럼 표시 (문서명, 타입, 크기, 수정일)
- [ ] 각 문서 행에 아이콘 표시 (📄 또는 🖼️)
- [ ] 크기가 포맷팅되어 표시 (KB/MB)
- [ ] 수정일이 YYYY-MM-DD 형식

---

### TC-005: 문서 클릭 → Document Viewer

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-005 |
| 테스트명 | document_click_opens_viewer |
| 대상 | 문서 테이블 행 클릭 |
| 우선순위 | 높음 |

**테스트 단계:**
1. Documents 테이블에서 .md 파일 행 클릭
2. Document Viewer 모달 열림 확인
3. 마크다운 렌더링 확인

**검증 항목:**
- [ ] 모달 표시됨
- [ ] 문서 내용 렌더링됨
- [ ] ESC 또는 X로 닫힘

---

### TC-006: 접기/펼치기 토글

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-006 |
| 테스트명 | documents_section_toggle |
| 대상 | Documents 섹션 헤더 |
| 우선순위 | 중간 |

**테스트 단계:**
1. Documents 섹션 헤더 클릭
2. 테이블 영역 숨김 확인
3. 아이콘 ▼ → ▶ 변경 확인
4. 다시 클릭하여 펼침 확인

**검증 항목:**
- [ ] 접힘 시 테이블 영역 hidden
- [ ] 펼침 시 테이블 영역 visible
- [ ] 아이콘 상태 변경

---

### TC-007: 문서 없음 표시

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-007 |
| 테스트명 | empty_documents_message |
| 대상 | Documents 섹션 |
| 우선순위 | 중간 |

**테스트 단계:**
1. 문서가 없는 Task 선택
2. Documents 섹션 확인

**예상 결과:**
- "문서 없음" 메시지 표시
- 테이블 미표시

---

### TC-008: hover 효과

| 항목 | 내용 |
|------|------|
| 테스트 ID | TC-008 |
| 테스트명 | document_row_hover |
| 대상 | 문서 테이블 행 |
| 우선순위 | 낮음 |

**테스트 단계:**
1. 문서 행에 마우스 올림
2. 배경색 변경 확인

**검증 항목:**
- [ ] hover 시 bg-gray-700 적용

---

## 4. 매뉴얼 테스트

### MT-001: 반응형 레이아웃

| 항목 | 내용 |
|------|------|
| 테스트 ID | MT-001 |
| 테스트명 | responsive_table_layout |
| 우선순위 | 낮음 |

**테스트 단계:**
1. 데스크톱 (1024px+): 4컬럼 테이블 확인
2. 태블릿 (768-1023px): 크기 컬럼 숨김 확인
3. 모바일 (767px-): 리스트 형태 확인

---

## 5. 테스트 환경

| 환경 | 버전/도구 |
|------|----------|
| Python | 3.10+ |
| pytest | 최신 |
| pytest-asyncio | 최신 |
| 브라우저 | Chrome, Firefox |
| E2E 도구 | httpx (TestClient) |

---

## 6. 테스트 커버리지 목표

| 유형 | 목표 | 현재 |
|------|------|------|
| 단위 테스트 | 80% | 0% |
| E2E 테스트 | 5 케이스 | 0 케이스 |

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-12-28 | 최초 작성 |
