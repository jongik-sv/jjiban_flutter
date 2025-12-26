# /wf:fix - 결함 수정 (Lite)

> **상태 전환**: `[an] 분석` → `[fx] 수정`
> **적용 category**: defect only

## 사용법

```bash
/wf:fix [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:fix TSK-01-01` | 자동 검색 |
| `/wf:fix jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 실행 과정

1. **분석 문서 로드**
   - `010-defect-analysis.md` 읽기
   - 영향 범위 확인
   - 수정 방안 확인

2. **결함 수정**
   - 근본 원인 해결
   - 관련 코드 수정
   - 회귀 방지 코드 추가

3. **테스트 작성/실행**
   - 결함 재현 테스트 추가
   - 기존 테스트 실행
   - 회귀 테스트 확인

4. **구현 보고서 작성**
   - `030-implementation.md` 생성
   - 수정 내역 기록

5. **상태 업데이트**
   - `[an]` → `[fx]`

---

## 수정 원칙

| 원칙 | 설명 |
|------|------|
| 근본 원인 | 증상이 아닌 원인 해결 |
| 최소 변경 | 필요한 부분만 수정 |
| 테스트 추가 | 재발 방지 테스트 필수 |
| 회귀 방지 | 기존 기능 영향 없음 확인 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] defect만 지원합니다` |
| 잘못된 상태 | `[ERROR] 분석 상태가 아닙니다` |
| 분석 문서 없음 | `[ERROR] 010-defect-analysis.md가 없습니다` |
| 테스트 실패 | `[ERROR] 회귀 테스트 실패: N건` |

---

## 다음 명령어

- `/wf:test` - 테스트 실행
- `/wf:audit` - 코드 리뷰
- `/wf:verify` - 통합테스트

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:fix lite
Version: 1.0
-->
