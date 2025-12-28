# /wf:apply - 설계 리뷰 반영 (Lite)

> **상태 변경 없음**: 반복 실행 가능
> **적용 category**: development only

## 사용법

```bash
/wf:apply [PROJECT/]<Task-ID> [리뷰파일번호]
```

| 예시 | 설명 |
|------|------|
| `/wf:apply TSK-01-01` | 자동 검색 |
| `/wf:apply orchay/TSK-01-01 1` | 프로젝트 명시 + 리뷰파일번호 |

---

## 실행 과정

1. **리뷰 파일 선택**
   - 최신 `021-design-review-{llm}-{n}.md` 자동 선택
   - 또는 사용자 지정 번호

2. **지적사항 분석**
   - Critical/Major 항목 우선 처리
   - 리뷰 이슈를 무조건 적용하지 않고 맥락에 따라 적용여부 판단.
   - 수정 대상 문서 식별

3. **설계 문서 수정**
   - `020-detail-design.md` 수정
   - `025-traceability-matrix.md` 수정
   - `026-test-specification.md` 수정

4. **적용 완료 표시**
   - 파일명 변경: `021-...(적용완료).md`

---

## 문서 선택 규칙

| 조건 | 선택 |
|------|------|
| 미적용 리뷰 1개 | 자동 선택 |
| 미적용 리뷰 여러개 | 사용자 확인 |
| 번호 지정 | 해당 파일 선택 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 리뷰 파일 없음 | `[ERROR] 설계 리뷰 파일이 없습니다` |
| 이미 적용됨 | `[WARN] 이미 적용 완료된 리뷰입니다` |
| 설계 문서 없음 | `[ERROR] 수정 대상 설계 문서가 없습니다` |

---

## 다음 명령어

- `/wf:review` - 추가 리뷰 (필요시)
- `/wf:build` - 구현 시작

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:apply lite
Version: 1.0
-->
