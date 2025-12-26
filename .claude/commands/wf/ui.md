---
subagent:
  primary: frontend-architect
  description: UI/UX 설계 및 화면 와이어프레임 생성
mcp-servers: [sequential-thinking]
hierarchy-input: true
parallel-processing: true
---

# /wf:ui - 화면설계 (Lite)

> **상태 변경 없음**: `[bd] 기본설계` 유지
> **적용 category**: development only
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)

## 사용법

```bash
/wf:ui [PROJECT/]<WP-ID | ACT-ID | Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:ui TSK-01-01` | Task 단위 |
| `/wf:ui ACT-01-01` | ACT 내 모든 `[bd]` Task 병렬 |
| `/wf:ui WP-01` | WP 내 모든 Task 병렬 |

---

## 생성 산출물

```
{TSK-ID}/
├── 011-ui-design.md        ← 화면설계 문서
└── ui-assets/              ← SVG 파일 폴더
    ├── screen-01-list.svg
    ├── screen-01-list-empty.svg
    ├── screen-02-form.svg
    └── screen-02-form-validation.svg
```

---

## 실행 과정

### 1. 입력 문서 분석

- `010-basic-design.md` 읽기
- PRD/TRD 화면 요구사항 추출
- UI 테마 가이드 참조 (`.jjiban/{project}/ui-theme-*.md`)

### 2. 화면 흐름 설계

- 화면 목록 정의 (SCR-XX)
- 화면 전환 흐름 (Mermaid stateDiagram)
- 액션-화면 매트릭스 작성

### 3. 화면별 상세 설계

| 항목 | 내용 |
|------|------|
| 레이아웃 | Grid/Flexbox 구조 |
| 컴포넌트 | 목록 + 속성 + 동작 |
| 상태 | 초기, 로딩, 성공, 에러, 빈 상태 |
| 액션 | 트리거 → 결과 → 조건 |

### 4. SVG 화면 생성

---

## SVG 파일명 규칙

```
screen-{순번}-{화면명}.svg           # 기본 상태
screen-{순번}-{화면명}-{상태}.svg    # 상태별 변화

예시:
screen-01-list.svg              # 목록 기본
screen-01-list-empty.svg        # 목록 빈 상태
screen-02-form.svg              # 입력 폼 기본
screen-02-form-validation.svg   # 유효성 에러
screen-02-form-loading.svg      # 저장 중
```

---

## SVG 스타일 가이드

### 색상 시스템

| 용도 | 색상 코드 |
|------|----------|
| 배경 | `#FFFFFF` (흰색) 또는 테마 Surface |
| 테두리 | `#E5E7EB` (gray-200) |
| 주요 요소 | `#3B82F6` (blue-500) |
| 텍스트 | `#1F2937` (gray-800) |
| 비활성 | `#9CA3AF` (gray-400) |
| 에러 | `#EF4444` (red-500) |
| 성공 | `#10B981` (green-500) |

### 폰트

| 용도 | 크기 |
|------|------|
| 제목 | 16px Bold |
| 본문 | 14px Regular |
| 캡션 | 12px Regular |

### 간격

| 항목 | 값 |
|------|---|
| 패딩 | 16px |
| 요소 간격 | 8px |

### 컴포넌트 표현

```
버튼   → 둥근 모서리 사각형 (rx=6)
입력   → 테두리 있는 사각형
카드   → 그림자 있는 사각형
테이블 → 격자 구조
아이콘 → 원 또는 심볼
링크   → 밑줄 텍스트
```

### 액션 표시

- **클릭 가능**: 파란색 테두리/배경
- **비활성**: 회색 처리
- **호버**: 점선 테두리 (선택)

---

## 011-ui-design.md 주요 섹션

| 섹션 | 내용 |
|------|------|
| 1. 화면 목록 | SCR-XX, 목적, SVG 참조 |
| 2. 화면 전환 흐름 | Mermaid stateDiagram, 액션-화면 매트릭스 |
| 3. 화면별 상세 | 레이아웃, 컴포넌트, 상태, 액션 |
| 4. 공통 컴포넌트 | 모달, 알림, 토스트 |
| 5. 반응형 설계 | Breakpoint (Desktop/Tablet/Mobile) |
| 6. 접근성 | 키보드 네비게이션, ARIA, 색상 대비 |
| 7. SVG 파일 목록 | 전체 SVG 파일 미리보기 |

---

## 출력 예시

```
[wf:ui] 화면설계

Task: TSK-01-01-01
상태: [bd] (변경 없음)

📂 기본설계 분석:
├── 화면 목록: 4개
├── 사용자 시나리오: 3개
└── 화면 흐름: 1개

🎨 화면 분석:
├── SCR-01: 목록 (기본/빈/로딩)
├── SCR-02: 생성 폼 (기본/에러/저장중)
├── SCR-03: 상세 (기본/로딩)
└── SCR-04: 수정 폼 (기본/에러/저장중)

📄 생성된 문서:
├── 011-ui-design.md
└── ui-assets/ (SVG 7개)

다음: /wf:draft
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 기본설계 상태가 아닙니다` |
| 기본설계 없음 | `[ERROR] 010-basic-design.md가 없습니다` |
| 화면 요구사항 없음 | `[WARN] 화면 요구사항이 없습니다` |
| SVG 생성 실패 | `[ERROR] SVG 생성 실패: {파일명}` |

---

## 다음 명령어

- `/wf:draft` - 상세설계 진행

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:ui lite
Version: 1.1
-->
