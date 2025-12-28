# 사용자 매뉴얼 (080-manual.md)

**Template Version:** 1.0.0 — **Last Updated:** 2025-12-28

---

## 0. 문서 메타데이터

* **문서명**: `080-manual.md`
* **Task ID**: TSK-02-02
* **Task 명**: 트리 템플릿 구현
* **작성일**: 2025-12-28
* **작성자**: Claude
* **대상 사용자**: 개발자, orchay 웹 UI 사용자

---

## 1. 개요

### 1.1 기능 소개
WBS 트리 템플릿은 orchay 웹 모니터링 UI에서 프로젝트의 Work Package(WP), Activity(ACT), Task(TSK) 계층 구조를 시각적으로 표현하는 컴포넌트입니다.

**주요 기능**:
- WP > ACT > TSK 계층 구조 시각화
- 10가지 Task 상태별 색상 코딩
- WP/ACT 확장/축소 토글
- Task 선택 시 상세 패널 로드
- WP/ACT 진행률 표시

### 1.2 대상 사용자
- **개발자**: 템플릿 커스터마이징, 스타일 수정
- **프로젝트 관리자**: WBS 트리를 통한 프로젝트 현황 모니터링

---

## 2. 시작하기

### 2.1 사전 요구사항
- orchay 서버 실행 중 (`python -m orchay --web` 또는 `--web-only`)
- `.jjiban/projects/{project}/wbs.md` 파일 존재
- 브라우저 지원: Chrome, Firefox, Edge (최신 버전)

### 2.2 접근 방법
```bash
# 웹 서버 시작
cd orchay
uv run python -m orchay orchay_web --web-only --port 8080

# 브라우저에서 접속
# http://localhost:8080
```

---

## 3. 사용 방법

### 3.1 트리 탐색

#### 확장/축소
- **WP 노드 클릭**: 하위 ACT/Task 노드 확장 또는 축소
- **토글 아이콘**: ▶ (축소됨) / ▼ (확장됨)

#### Task 선택
- **Task 노드 클릭**: 우측 상세 패널에 Task 정보 로드
- **선택 표시**: 클릭된 Task는 밝은 배경색으로 강조

### 3.2 상태 표시

| 상태 코드 | 상태명 | 색상 | 의미 |
|----------|--------|------|------|
| `[ ]` | Todo | 회색 | 미시작 |
| `[bd]` | 기본설계 | 파란색 | 기본설계 진행 중 |
| `[dd]` | 상세설계 | 보라색 | 상세설계 진행 중 |
| `[an]` | 분석 | 인디고 | 분석 진행 중 (defect) |
| `[ds]` | 설계 | 시안 | 설계 진행 중 (infrastructure) |
| `[ap]` | 승인 | 녹색 | 설계 승인 완료 |
| `[im]` | 구현 | 노란색 | 구현 진행 중 |
| `[fx]` | 수정 | 주황색 | 수정 진행 중 (defect) |
| `[vf]` | 검증 | 틸 | 테스트/검증 중 |
| `[xx]` | 완료 | 에메랄드 | 완료 |

### 3.3 진행률 표시
- **WP/ACT 노드**: 하위 Task의 완료 비율 표시
- **계산 방식**: `(완료 Task 수 / 전체 Task 수) × 100%`
- **표시 형식**: `N%` (노드 제목 우측)

---

## 4. FAQ

### Q1: 트리가 비어있어요
**A**: `.jjiban/projects/{project}/wbs.md` 파일이 존재하는지 확인하세요. wbs.md에 Task가 정의되어 있어야 합니다.

### Q2: 상태 색상이 회색으로만 표시돼요
**A**: Task의 status 필드가 올바른 형식인지 확인하세요. 예: `- status: implement [im]`

### Q3: 트리가 자동 갱신되지 않아요
**A**: 자동 갱신 기능은 TSK-02-03에서 구현됩니다. 현재 버전에서는 수동 새로고침이 필요합니다.

### Q4: 확장/축소가 작동하지 않아요
**A**: JavaScript가 활성화되어 있는지 확인하세요. 브라우저 콘솔에서 오류 메시지를 확인하세요.

---

## 5. 문제 해결

### 5.1 일반적인 문제

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 트리 로드 안됨 | 서버 연결 끊김 | 서버 재시작, 네트워크 확인 |
| 상태 색상 오류 | 잘못된 status 형식 | wbs.md의 status 필드 수정 |
| 레이아웃 깨짐 | CSS CDN 로드 실패 | 인터넷 연결 확인, 새로고침 |

### 5.2 디버깅 방법
1. 브라우저 개발자 도구 열기 (F12)
2. Console 탭에서 오류 메시지 확인
3. Network 탭에서 API 응답 확인
4. `/api/tree` 엔드포인트 직접 호출하여 데이터 확인

---

## 6. 참고 자료

### 6.1 관련 문서
- 통합설계서: `./010-design.md`
- 추적성 매트릭스: `./025-traceability-matrix.md`
- 테스트 명세서: `./026-test-specification.md`
- 구현 보고서: `./030-implementation.md`
- PRD: `.jjiban/projects/orchay_web/prd.md`

### 6.2 소스 코드 위치
- 템플릿: `orchay/src/orchay/web/templates/partials/tree.html`
- 확장 파셜: `orchay/src/orchay/web/templates/partials/wp_children.html`
- 테스트: `orchay/tests/test_tree.py`

### 6.3 관련 API
| 엔드포인트 | 설명 |
|------------|------|
| `GET /` | 메인 페이지 (트리 포함) |
| `GET /api/tree` | 전체 트리 HTML |
| `GET /api/tree/{wp_id}` | WP 하위 노드 HTML |
| `GET /api/detail/{task_id}` | Task 상세 정보 |

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0.0 | 2025-12-28 | Claude | 최초 작성 |

---

<!--
TSK-02-02 사용자 매뉴얼
Version: 1.0
-->
