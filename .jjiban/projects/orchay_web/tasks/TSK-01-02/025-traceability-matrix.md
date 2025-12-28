# TSK-01-02 - 요구사항 추적 매트릭스

## 문서 정보

| 항목 | 내용 |
|------|------|
| Task ID | TSK-01-02 |
| 문서 버전 | 1.0 |
| 작성일 | 2025-12-28 |
| 관련 설계 | 010-design.md |

---

## 1. PRD → 설계 추적

| PRD 섹션 | 요구사항 | 설계 반영 | 설계 위치 |
|----------|----------|----------|----------|
| 2.1 레이아웃 | 2열 레이아웃 (트리 \| 상세) | base.html, index.html 2열 구조 | 5.2 화면별 상세 |
| 2.1 레이아웃 | 헤더, 메인, 푸터 구조 | base.html 레이아웃 정의 | 5.2 base.html |
| 2.2 주요 컴포넌트 | Header (프로젝트명, 모드) | index.html 헤더 영역 | 11.5 index.html |
| 2.2 주요 컴포넌트 | Worker Bar | workers-bar div | 11.5 index.html |
| 2.2 주요 컴포넌트 | WBS Tree 영역 | tree-panel div | 11.5 index.html |
| 2.2 주요 컴포넌트 | Task Detail 영역 | detail-panel div | 11.5 index.html |
| 2.3 실시간 갱신 | HTMX hx-trigger="every 5s" | 템플릿 HTMX 속성 | 11.5 index.html |

---

## 2. TRD → 설계 추적

| TRD 섹션 | 기술 스펙 | 설계 반영 | 설계 위치 |
|----------|----------|----------|----------|
| 기술 스택 | Jinja2 ^3.0 | base.html extends/block | 11.5 base.html |
| 기술 스택 | HTMX 2.0 CDN | unpkg.com/htmx.org@2.0.0 | 11.5 base.html |
| 기술 스택 | Tailwind CSS 3.x CDN | cdn.tailwindcss.com | 11.5 base.html |
| 파일 구조 | templates/base.html | 생성 예정 | 11.4 파일 구조 |
| 파일 구조 | templates/index.html | 생성 예정 | 11.4 파일 구조 |
| 파일 구조 | templates/partials/ | 디렉터리 구조 정의 | 11.4 파일 구조 |
| UI 스타일링 | bg-gray-900 다크테마 | body 클래스 적용 | 8.1 BR-01 |
| UI 스타일링 | flex h-screen | 레이아웃 구조 | 5.2 index.html |

---

## 3. 설계 → 테스트 추적

| 설계 항목 | 설계 위치 | 테스트 케이스 | 테스트 위치 |
|----------|----------|-------------|-------------|
| 다크테마 적용 | 8.1 BR-01 | TC-01 | 026-test-specification.md |
| 2열 레이아웃 | 5.2 index.html | TC-02 | 026-test-specification.md |
| HTMX CDN 로드 | 11.5 base.html | TC-03 | 026-test-specification.md |
| Tailwind CSS CDN 로드 | 11.5 base.html | TC-04 | 026-test-specification.md |
| 헤더 프로젝트명 표시 | 11.5 index.html | TC-05 | 026-test-specification.md |
| 헤더 모드 표시 | 11.5 index.html | TC-06 | 026-test-specification.md |
| Worker 바 영역 | 11.5 index.html | TC-07 | 026-test-specification.md |
| 트리 패널 HTMX 속성 | 11.5 index.html | TC-08 | 026-test-specification.md |
| 상세 패널 기본 상태 | 11.5 index.html | TC-09 | 026-test-specification.md |
| 반응형 레이아웃 | 5.3 반응형 동작 | TC-10 | 026-test-specification.md |

---

## 4. 요구사항 커버리지 요약

| 구분 | 전체 | 반영됨 | 커버리지 |
|------|------|--------|----------|
| PRD 요구사항 | 7 | 7 | 100% |
| TRD 기술 스펙 | 8 | 8 | 100% |
| 설계 → 테스트 | 10 | 10 | 100% |

---

## 5. 미반영 사항

> 현재 미반영 사항 없음

| PRD/TRD 항목 | 미반영 사유 | 대응 계획 |
|-------------|------------|----------|
| - | - | - |

---

## 변경 이력

| 버전 | 일자 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-12-28 | Claude | 최초 작성 |
