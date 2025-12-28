# /wf:ui - 화면설계 (Lite)

> **상태 변경 없음**: `[bd] 기본설계` 유지
> **적용 category**: development only

## 사용법

```bash
/wf:ui [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:ui TSK-01-01` | 자동 검색 |
| `/wf:ui orchay/TSK-01-01` | 프로젝트 명시 |

---

## 생성 산출물

| 파일 | 내용 |
|------|------|
| `011-ui-design.md` | 화면설계 문서 |
| `ui-assets/*.svg` | 화면별 SVG 파일 |

---

## 실행 과정

1. **입력 문서 분석**
   - `010-basic-design.md` 읽기
   - PRD/TRD 화면 요구사항 추출
   - UI 테마 가이드 참조 (`.orchay/{project}/ui-theme-*.md`)

2. **화면 흐름 설계**
   - 화면 목록 정의 (SCR-XX)
   - 화면 전환 흐름 (Mermaid stateDiagram)

3. **화면별 상세 설계**
   - 레이아웃 구조 (Grid/Flexbox)
   - 컴포넌트 목록 및 속성
   - 상태별 화면 변화

4. **SVG 화면 생성** (선택)
   - `ui-assets/` 폴더에 화면별 SVG 저장
   - 와이어프레임 수준의 시각화

5. **접근성/반응형 설계**
   - ARIA 레이블, 키보드 네비게이션
   - Breakpoint별 레이아웃

---

## SVG 생성 규칙

| 항목 | 값 |
|------|---|
| 크기 | 1200x800 (기본) |
| 배경 | 투명 또는 테마 Surface 색상 |
| 폰트 | 시스템 sans-serif |
| 컴포넌트 | 사각형 + 레이블 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 기본설계 상태가 아닙니다` |
| 기본설계 없음 | `[ERROR] 010-basic-design.md가 없습니다` |
| 화면 요구사항 없음 | `[WARN] 화면 요구사항이 없습니다` |

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
Version: 1.0
-->
