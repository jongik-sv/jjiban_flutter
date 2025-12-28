# /wf:draft - 상세설계 (Lite)

> **상태 전환**: `[bd] 기본설계` → `[dd] 상세설계`
> **적용 category**: development only

## 사용법

```bash
/wf:draft [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:draft TSK-01-01` | 자동 검색 |
| `/wf:draft orchay/TSK-01-01` | 프로젝트 명시 |

---

## 코드 작성 금지 원칙

| 금지 | 대체 |
|------|------|
| ❌ TS/JS 코드 | ✅ 메서드 시그니처 표 |
| ❌ Vue/React 코드 | ✅ Props/Events 표 |
| ❌ SQL 쿼리 | ✅ ERD + 필드 표 |
| ❌ 테스트 코드 | ✅ 테스트 시나리오 표 |
| ✅ Prisma 스키마 | **유일한 예외** |

---

## 생성 문서

| 파일 | 내용 |
|------|------|
| `020-detail-design.md` | 상세설계 본문 |
| `025-traceability-matrix.md` | 추적성 매트릭스 |
| `026-test-specification.md` | 테스트 명세 |

---

## 실행 과정

1. **Task 검증 및 컨텍스트 수집**
   - `010-basic-design.md` 존재 확인
   - `011-ui-design.md` 참조 (선택)
   - PRD/TRD 참조 섹션 추출

2. **상위 문서 분석**
   - 기본설계: FR-XXX, BR-XXX 추출
   - 화면설계: 컴포넌트, 상태 추출
   - PRD: 원본 요구사항 확인
   - TRD: 기술 스택, 규칙 확인

3. **상세설계 문서 생성**
   - 기술 아키텍처 (ERD, 모듈 구조)
   - API 설계 (표 형식)
   - UI/UX 설계 (Text Art + 표)
   - 비즈니스 로직 (시퀀스 다이어그램)

4. **일관성 검증**
   - CHK-PRD: PRD ↔ 기본설계
   - CHK-BD: 기본설계 ↔ 상세설계
   - CHK-UI: 화면설계 ↔ 상세설계
   - CHK-TRD: TRD 준수 여부

5. **추적성 매트릭스 생성**
   - FR → PRD → 기본설계 → 상세설계 → 테스트
   - BR → 구현 위치 → 테스트

6. **Task JSON 상태 업데이트**
   - `[bd]` → `[dd]}

---

## 검증 결과 처리

| 결과 | 처리 |
|------|------|
| ❌ FAIL | 문서 생성 중단, 수정 요청 |
| ⚠️ WARN | 문서 생성 진행, 검토 항목 기록 |
| ✅ PASS | 정상 진행 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 기본설계 상태가 아닙니다` |
| 기본설계 없음 | `[ERROR] 010-basic-design.md가 없습니다` |
| 코드 블록 감지 | `[ERROR] 코드 감지. 표/다이어그램으로 변환 필요` |

---

## 다음 명령어

- `/wf:review` - LLM 설계 리뷰 (상태 변경 없음)
- `/wf:build` - 구현 시작

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:draft lite
Version: 1.0
-->
