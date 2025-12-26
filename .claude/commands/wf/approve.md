---
subagent:
  primary: refactoring-expert
  description: 설계 품질 검증 및 승인 처리
---

# /wf:approve - 설계승인 (Lite)

> **상태 전환**: `[dd] 상세설계` → `[ap] 설계승인`
> **적용 category**: development only

## 사용법

```bash
/wf:approve [PROJECT/]<Task-ID>
```

| 예시 | 설명 |
|------|------|
| `/wf:approve TSK-01-01` | 자동 검색 |
| `/wf:approve jjiban/TSK-01-01` | 프로젝트 명시 |

---

## 승인 모드

| 모드 | 동작 | 설정 |
|------|------|------|
| `manual` | 사용자 확인 후 승인 | 기본값 |
| `auto` | 조건 충족 시 자동 승인 | `project.json`에 `"approvalMode": "auto"` |

---

## 실행 과정

### Manual 모드 (기본)

1. **문서 존재 확인**
   - `010-basic-design.md` 확인
   - `020-detail-design.md` 확인

2. **리뷰 현황 표시**
   - `021-design-review-*.md` 파일 목록
   - 적용완료 여부 표시

3. **사용자 확인 프롬프트**
   ```
   [INFO] 설계 문서 준비 완료
   - 기본설계: 010-basic-design.md ✅
   - 상세설계: 020-detail-design.md ✅
   - 리뷰: 021-design-review-claude-1(적용완료).md ✅

   설계승인을 진행하시겠습니까? (y/n)
   ```

4. **상태 전환**
   ```bash
   npx tsx .jjiban/script/transition.ts {Task-ID} approve -p {project} --force
   ```
   - `--force`: manual 모드에서 확인 없이 실행

### Auto 모드

1. **자동 승인** (스크립트가 조건 검증)
   ```bash
   npx tsx .jjiban/script/transition.ts {Task-ID} approve -p {project}
   ```
   - 스크립트가 `project.json`의 `approvalMode` 확인
   - 조건 충족 시 자동 전환
   - 조건 미충족 시 실패 JSON 반환

---

## Auto 모드 승인 조건

| 조건 | 설명 |
|------|------|
| 기본설계 존재 | `010-basic-design.md` 필수 |
| 상세설계 존재 | `020-detail-design.md` 필수 |
| 리뷰 1건 이상 | `021-design-review-*.md` 존재 |
| P1 이슈 없음 | Critical/P1 미해결 이슈 0건 |

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 상세설계 상태가 아닙니다` |
| 기본설계 없음 | `[ERROR] 010-basic-design.md가 없습니다` |
| 상세설계 없음 | `[ERROR] 020-detail-design.md가 없습니다` |
| Auto 조건 미충족 | `[WARN] Auto 승인 조건 미충족. 수동 모드로 전환` |

---

## 다음 명령어

- `/wf:build` - 구현 시작

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-conflict-resolution-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:approve lite
Version: 1.0
-->
