---
subagent:
  primary: refactoring-expert
  description: 설계 품질 분석 및 리뷰 수행
mcp-servers: [sequential-thinking, context7]
hierarchy-input: true
parallel-processing: true
---

# /wf:review - 설계 리뷰 (Lite)

> **상태 변경 없음**: 반복 실행 가능
> **적용 category**: development only
> **계층 입력**: WP/ACT/Task 단위 (하위 Task 병렬 처리)

## 사용법

```bash
/wf:review [PROJECT/]<WP-ID | ACT-ID | Task-ID> [--llm claude|gemini]
```

| 예시 | 설명 |
|------|------|
| `/wf:review TSK-01-01` | Task 단위 |
| `/wf:review ACT-01-01` | ACT 내 모든 `[dd]` Task 병렬 |
| `/wf:review TSK-01-01 --llm gemini` | 특정 LLM 리뷰 |

---

## 생성 산출물

| 파일 | 내용 |
|------|------|
| `021-design-review-{llm}-{n}.md` | 설계 리뷰 결과 |

---

## 실행 과정

### 1. 검증 대상 문서 수집

```
필수 문서 (분할 설계):
├── 020-detail-design.md (상세설계 본문)
├── 025-traceability-matrix.md (추적성 매트릭스)
├── 026-test-specification.md (테스트 명세)
└── 010-basic-design.md (기본설계)

참조 문서:
├── .jjiban/{project}/prd.md
└── .jjiban/{project}/trd.md
```

### 2. 다층 품질 검증 수행

| 검증 영역 | 관점 | 검증 항목 |
|----------|------|----------|
| 문서 완전성 | quality | 필수 섹션, 문서간 참조 일관성 |
| 요구사항 추적성 | quality | FR/BR 매핑, 누락 식별 |
| 아키텍처 | system-architect | SOLID, 컴포넌트 분할, 확장성 |
| 보안 | security | OWASP Top 10, 인증/인가, 암호화 |
| 성능 | quality | 응답시간, 캐싱, 페이지네이션 |
| 테스트 가능성 | quality | UT/E2E 시나리오, data-testid |

### 3. 리뷰 결과 작성

---

## 심각도(Severity) 분류

| 심각도 | 설명 | 예시 |
|--------|------|------|
| **Critical** | 시스템 중단, 데이터 손실, 심각한 보안 | 인증 우회, 데이터 무결성 파괴 |
| **High** | 핵심 기능 오류, 보안 취약점 | API 권한 검증 누락 |
| **Medium** | 부분적 기능 제한, 성능 저하 | 페이지네이션 미적용 |
| **Low** | 경미한 불편, 코드 품질 | 네이밍 개선 |
| **Info** | 개선 제안, 모범 사례 | 최신 패턴 적용 |

---

## 우선순위(Priority) 분류

| 우선순위 | 설명 | 조치 기한 |
|----------|------|----------|
| **P1** | 설계 결함, 심각한 보안 위험 | 구현 전 필수 수정 |
| **P2** | 아키텍처 개선, 성능 문제 | 구현 초기 수정 |
| **P3** | 코드 품질, 표준 미준수 | 구현 중 수정 |
| **P4** | 최적화 기회, 리팩토링 | 구현 후 검토 |
| **P5** | 참고 사항, 향후 고려 | 다음 iteration |

---

## 출력 예시

```
[wf:review] 설계 리뷰

Task: TSK-01-01-01 | 리뷰어: claude-1

📋 검증 대상:
├── 020-detail-design.md ✅
├── 025-traceability-matrix.md ✅
├── 026-test-specification.md ✅
└── 010-basic-design.md ✅

┌────────────────┬──────┬─────────────────────┐
│ 검증 영역      │ 평가 │ 비고                │
├────────────────┼──────┼─────────────────────┤
│ 문서 완전성    │ PASS │ 필수 섹션 모두 포함 │
│ 요구사항 추적성│ PASS │ FR 6, BR 6 매핑 완료│
│ 아키텍처       │ WARN │ 1건 개선 권장       │
│ 보안           │ PASS │                     │
│ 테스트 가능성  │ PASS │ UT 12, E2E 8 정의   │
└────────────────┴──────┴─────────────────────┘

이슈 분포: P1(0) P2(1) P3(1) P4(2) P5(1) = 5건

다음: /wf:apply 또는 /wf:build
```

---

## 에러 케이스

| 에러 | 메시지 |
|------|--------|
| 잘못된 category | `[ERROR] development만 지원합니다` |
| 잘못된 상태 | `[ERROR] 상세설계 상태가 아닙니다` |
| 상세설계 없음 | `[ERROR] 020-detail-design.md가 없습니다` |
| 추적성 매트릭스 없음 | `[ERROR] 025-traceability-matrix.md가 없습니다` |
| 테스트 명세 없음 | `[ERROR] 026-test-specification.md가 없습니다` |

---

## 다음 명령어

- `/wf:apply` - 리뷰 내용 반영
- `/wf:build` - 구현 시작 (리뷰 미반영 시)

---

## 공통 모듈 참조

@.claude/includes/wf-common-lite.md
@.claude/includes/wf-auto-commit-lite.md

---

<!--
wf:review lite
Version: 1.1
-->
