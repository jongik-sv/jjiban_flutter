---
subagent:
  primary: refactoring-expert
  description: 코드 리뷰 지적사항 반영
mcp-servers: [sequential-thinking, context7]
hierarchy-input: true
parallel-processing: true
---

# /wf:patch - 코드 리뷰 반영 (Lite)

> **상태 변경 없음**: 반복 실행 가능
> **적용 category**: development, infrastructure
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)

## 사용법

```bash
/wf:patch [PROJECT/]<WP-ID | ACT-ID | Task-ID> [--review N] [--priority must,should]
```

| 예시 | 설명 |
|------|------|
| `/wf:patch TSK-01-01` | 최신 미적용 리뷰 자동 선택 |
| `/wf:patch TSK-01-01 --review 2` | 특정 리뷰 회차 지정 |
| `/wf:patch ACT-01-01` | ACT 내 모든 `[im]` Task 병렬 |
| `/wf:patch TSK-01-01 --priority must,should` | 우선순위 필터 |

---

## 우선순위별 적용 원칙 ⭐

| 우선순위 | 분류 | 적용 원칙 | 예시 |
|---------|------|----------|------|
| **P1** | Must Fix | 반드시 적용, 즉시 수정 | 보안 취약점, 치명적 버그 |
| **P2** | Should Fix | 적용 권장, 릴리즈 전 수정 | 성능 이슈, 코드 품질 |
| **P3** | Nice to Have | 선택적 적용, 리소스 여유 시 | 코딩 스타일, 문서화 |

---

## 실행 과정

### 1. 리뷰 파일 선택

```
탐색 우선순위:
1. "(적용완료)" 표시 없는 최신 리뷰 문서 (기본)
2. --review N 옵션 지정 시 해당 회차
3. "(적용완료)" 파일은 탐색에서 제외

파일 패턴:
├── 031-code-review-claude-1(적용완료).md  ← 제외
├── 031-code-review-claude-2.md           ← 최신 (대상)
└── 031-code-review-gemini-1(적용완료).md ← 제외
```

### 2. 지적사항 분석

```
📋 우선순위별 분류:
├── 3.1 필수 (Must Fix)      ← P1: 즉시 적용
├── 3.2 권장 (Should Fix)    ← P2: 권장 적용
└── 3.3 선택 (Nice to Have)  ← P3: 검토 후 적용

적용 범위 결정:
├── 코드 수정 필요 → 소스 파일 목록
├── 문서 수정 필요 → 설계/구현 문서
└── 테스트 추가 필요 → 테스트 파일
```

### 3. 코드 수정

- P1 보안 이슈 수정 우선
- 성능 최적화 코드 적용
- 코딩 표준 준수 리팩토링
- 누락 테스트 케이스 추가

### 4. 테스트 재실행 및 검증 ⭐

**테스트-수정 루프** (최대 5회):

```
🔄 테스트-수정 루프:
├── 1️⃣ 단위 테스트 실행
├── 2️⃣ 실패 분석
│   ├── 기존 테스트 실패 → 회귀 수정
│   └── 새 테스트 실패 → 추가 수정
├── 3️⃣ 코드 수정
├── 4️⃣ 타입 체크 확인
└── 5️⃣ 재실행 (최대 5회)
```

### 5. 구현 문서 업데이트 ⭐

```markdown
## X. 코드 리뷰 반영 이력

### 반영 일시: 2026-12-08
### 기준 리뷰: 031-code-review-claude-1.md

| # | 항목 | 유형 | 파일 | 상태 |
|---|------|------|------|------|
| 1 | [항목1] | Must | [파일] | ✅ 반영 |
| 2 | [항목2] | Should | [파일] | ✅ 반영 |
| 3 | [항목3] | Nice | [파일] | ⏭️ 스킵 |

### 미반영 사항 (사유 포함)
| # | 항목 | 유형 | 사유 |
|---|------|------|------|
| 1 | [항목3] | Nice | 현재 범위 외 |
```

### 6. 적용완료 처리

```
변경 전: 031-code-review-claude-1.md
변경 후: 031-code-review-claude-1(적용완료).md
```

---

## 출력 예시

```
[wf:patch] 코드 리뷰 내용 반영

Task: TSK-01-01-01

📋 기준 리뷰: 031-code-review-claude-1.md

✅ 개선 사항 반영:
├── [Must]   1/1 반영 완료
├── [Should] 2/2 반영 완료
└── [Nice]   0/1 스킵 (사유: 현재 범위 외)

🔄 테스트-수정 루프: 2회 시도
├── 1차: 2/18 실패 → 회귀 수정
└── 2차: 18/18 ✅

📁 수정된 파일:
├── api/src/modules/project/project.service.ts
├── api/src/modules/project/project.controller.ts
└── api/src/modules/project/__tests__/project.service.spec.ts

📄 업데이트된 문서:
├── 030-implementation.md (리뷰 반영 이력 추가)
└── 031-...(적용완료).md

다음: /wf:audit (재리뷰) 또는 /wf:verify
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 상태 | `[ERROR] 구현/수정 상태가 아닙니다` |
| 리뷰 문서 없음 | `[ERROR] 코드 리뷰 파일이 없습니다` |
| 이미 적용됨 | `[WARN] 이미 적용 완료된 리뷰입니다` |
| 미적용 리뷰 없음 | `[WARN] 적용 가능한 리뷰가 없습니다` |
| 테스트 5회 초과 | `[ERROR] 테스트 5회 시도 후 실패. 수동 개입 필요` |

---

## 반복 리뷰-패치 사이클

```
[im] 구현 (development/infrastructure)
[fx] 수정 (defect)
      │
      ├── /wf:audit ───→ 031-code-review-{llm}-{n}.md
      │                          │
      │                          ▼
      ├── /wf:patch ────→ 소스 코드 수정
      │                          │
      │                          ▼
      │                  리뷰 문서 "(적용완료)" 처리
      │                          │
      ├── /wf:audit ───→ 031-code-review-{llm}-{n+1}.md
      │                          │
      └── (품질 만족까지 반복) ───┘
```

---

## 다음 명령어

- `/wf:audit` - 재리뷰 (필요시)
- `/wf:verify` - 통합테스트

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:patch lite
Version: 1.1
-->
