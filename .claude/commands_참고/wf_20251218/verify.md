# /wf:verify - 통합테스트 (Lite)

> **상태 전환**: `[im] 구현` → `[ts] 테스트` (development)
> **상태 전환**: `[fx] 수정` → `[ts] 테스트` (defect)
> **적용 category**: development, defect

## 사용법

```bash
/wf:verify [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:verify TSK-01-01` | 자동 검색 |
| `/wf:verify jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 생성 산출물

| 파일 | 내용 |
|------|------|
| `070-integration-test.md` | 통합테스트 결과 |

---

## 실행 과정

1. **테스트 환경 준비**
   - 통합 테스트 환경 설정
   - 테스트 데이터 준비

2. **통합테스트 실행**
   - API 통합 테스트
   - UI-Backend 연동 테스트
   - 시나리오 기반 테스트

3. **결과 검증**
   - 기능 요구사항 충족 확인
   - 비즈니스 규칙 검증
   - 에러 핸들링 확인

4. **테스트 결과 문서 생성**
   - `070-integration-test.md`

5. **상태 업데이트**
   - `[im]` → `[ts]` (development)
   - `[fx]` → `[ts]` (defect)

---

## 테스트 범위

| 영역 | 검증 항목 |
|------|----------|
| API | 엔드포인트, 인증, 에러 |
| UI | 화면 동작, 상태 변화 |
| 연동 | Frontend ↔ Backend |
| 데이터 | CRUD, 무결성 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 상태 | `[ERROR] 구현/수정 상태가 아닙니다` |
| 구현 문서 없음 | `[ERROR] 030-implementation.md가 없습니다` |
| 테스트 실패 | `[ERROR] 통합테스트 실패: N건` |

---

## 다음 명령어

- `/wf:done` - 작업 완료

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:verify lite
Version: 1.0
-->
