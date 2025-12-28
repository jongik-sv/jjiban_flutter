# /wf:done - 작업 완료 (Lite)

> **상태 전환**: `[ts] 테스트` → `[xx] 완료`
> **적용 category**: development, defect, infrastructure

## 사용법

```bash
/wf:done [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:done TSK-01-01` | 자동 검색 |
| `/wf:done orchay/TSK-01-01` | 프로젝트 명시 |

---

## 상태 전환 규칙

| category | 현재 상태 | 다음 상태 |
|----------|----------|----------|
| development | `[ts]` | `[xx]` |
| defect | `[ts]` | `[xx]` |
| infrastructure | `[im]` | `[xx]` |

---

## 생성 산출물

| 파일 | 내용 |
|------|------|
| `080-manual.md` | 사용자 매뉴얼 |

---

## 실행 과정

1. **완료 조건 검증**
   - 필수 문서 존재 확인
   - 테스트 통과 확인
   - 코드 리뷰 반영 확인

2. **매뉴얼 생성**
   - 기능 사용법 문서화
   - 화면 캡처/설명
   - 템플릿: `.orchay/templates/080-manual.md`

3. **상태 업데이트**
   - `[ts]`/`[im]` → `[xx]`

4. **상위 계층 상태 갱신**
   - ACT 내 모든 Task 완료 시 ACT 상태 업데이트
   - WP 내 모든 ACT 완료 시 WP 상태 업데이트

---

## 완료 조건

| category | 필수 조건 |
|----------|----------|
| development | 상세설계, 구현, 테스트 완료 |
| defect | 분석, 수정, 테스트 완료 |
| infrastructure | 설계, 구현 완료 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 상태 | `[ERROR] 테스트/구현 상태가 아닙니다` |
| 필수 문서 없음 | `[ERROR] 필수 문서가 없습니다: {파일명}` |
| 테스트 미완료 | `[ERROR] 테스트가 완료되지 않았습니다` |

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:done lite
Version: 1.0
-->
