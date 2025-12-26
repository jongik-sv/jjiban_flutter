# /wf:review - 설계 리뷰 (Lite)

> **상태 변경 없음**: 반복 실행 가능
> **적용 category**: development only

## 사용법

```bash
/wf:review [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:review TSK-01-01` | 자동 검색 |
| `/wf:review jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 생성 산출물

| 파일 | 내용 |
|------|------|
| `021-design-review-{llm}-{n}.md` | 설계 리뷰 결과 |

---

## 실행 과정

1. **설계 문서 로드**
   - `020-detail-design.md`
   - `025-traceability-matrix.md`
   - `026-test-specification.md`
   - `011-ui-design.md` (선택)

2. **리뷰 수행**
   - 설계 완전성 검토
   - 일관성 검증
   - 기술적 타당성 평가
   - 테스트 커버리지 검토

3. **리뷰 결과 작성**
   - 지적사항 (심각도/우선순위)
   - 개선 제안
   - 승인/조건부승인/재검토 판정

---

## 심각도/우선순위

| 심각도 | 설명 |
|--------|------|
| Critical | 기능 장애, 보안 취약점 |
| Major | 주요 기능 누락, 성능 이슈 |
| Minor | 품질 개선, 코드 스타일 |
| Info | 참고 사항 |

| 우선순위 | 설명 |
|---------|------|
| P1 | 즉시 수정 필수 |
| P2 | 구현 전 수정 |
| P3 | 구현 중 수정 가능 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 상세설계 없음 | `[ERROR] 020-detail-design.md가 없습니다` |

---

## 다음 명령어

- `/wf:apply` - 리뷰 내용 반영
- `/wf:build` - 구현 시작 (리뷰 미반영 시)

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md

---

<!--
wf:review lite
Version: 1.0
-->
