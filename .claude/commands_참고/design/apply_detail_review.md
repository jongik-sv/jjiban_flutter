---
name: design:apply_detail_review
description: "상세설계 리뷰 개선사항 적용"
category: improvement
complexity: moderate
wave-enabled: false
performance-profile: optimized
auto-flags: [--seq, --token-efficient, --validate]
mcp-servers: [sequential]
personas: [system-architect, security-engineer, technical-writer]
---

# /design:apply_detail_review - 상세설계 리뷰 개선사항 적용

> 상세설계 리뷰 개선사항을 현재 시스템 맥락을 고려하여 설계 문서에 선택적으로 적용

## 🎯 목표
- 토큰 효율성 30% 절약
- 맥락 기반 선택적 적용 (무조건 적용 금지)
- P1-P2 중심 집중 적용
- 에이전트 특화 위임

## 사용법
```bash
/design:apply_detail_review Task 3.1
/design:apply_detail_review 3.1
```

## 실행 플로우

### 1단계: 리뷰 결과 분석
**Persona**: system-architect | **MCP**: sequential

1. **Task 정보 추출**: `parseTaskFromCommand(input)` → Task 번호 파싱
2. **프로젝트 맥락 분석**: `analyze_project_context(task_number)`
   - 📋 함수: `@docs/common/07.functions/analyze_project_context.md`
3. **문서 로드**:
   - 리뷰: `30.review/33.detail/{task-id}.*_*.md`
   - 상세설계: `10.design/12.detail-design/{task-id}.(상세설계).md`
   - 기본설계: `10.design/11.basic-design/{task-id}.(기본설계).md` (필요 시)
4. **맥락 기반 적용 가능성 분석**:
   - ⚠️ **중요**: 무조건 적용 금지
   - 현재 시스템 구조 & 아키텍처 호환성
   - Task 특성 & 요구사항 범위 적합성
   - 기술 스택 & 제약사항 고려
   - 구현 실현 가능성 & 효과
5. **적용 판단**:
   - ✅ 적용: 시스템&Task 적합, 실현 가능
   - ⏸️ 보류: 맥락 부적합
   - 📝 조정 적용: 현재 시스템 맞춤 조정
6. **종합 문서 작성**:
   - 리뷰 문서들을 종합하여 각 대상에 대해 적용 판단 여부 및 판단 근거를 하나의 문서로 정리
   - 적용 대상만 다음 단계에 전달
   - 종합문서 : `30.review/33.detail/{task-id}.{task명}(상세설계리뷰_종합).md`

### 2단계: 아키텍처 개선
**Persona**: system-architect (Agent) | **MCP**: sequential

- P1-P2 아키텍처 결함 수정
- 컴포넌트 구조 & 데이터 흐름 최적화
- API 인터페이스 개선
- DB 스키마 정규화 & 무결성 제약
- 외부 연동 & 트랜잭션 전략 강화

### 3단계: 보안 개선
**Persona**: security-engineer | **MCP**: sequential

- P1-P2 보안 이슈 수정
- OWASP Top 10 대응
- 인증/인가 & 암호화 강화
- RBAC 설계 & 권한 관리
- 규정 준수 (GDPR, 개인정보보호법)

### 4단계: 성능/품질 개선
**Persona**: system-architect | **MCP**: sequential

- 병목 해소 & 캐싱 전략
- SOLID, DRY, KISS, YAGNI 적용
- 디자인 패턴 & 코딩 표준
- 테스트 가능성 개선

### 5단계: 설계 문서 업데이트
**Persona**: technical-writer | **MCP**: sequential

- 상세설계서: 아키텍처/API/데이터/화면 반영
- 기본설계서: 아키텍처 변경 반영 (필요 시)
- 추적성 매트릭스 재검증
- 변경 이력 문서화

### 6단계: 적용 검증
**Persona**: system-architect + security-engineer | **MCP**: sequential

- 기본-상세설계 일관성
- 요구사항 추적성 95% 이상
- P1-P2 이슈 해결 확인
- 문서 완전성 검증

### 7단계: 리뷰 문서 업데이트
**Persona**: technical-writer | **MCP**: sequential

1. **리뷰 문서 끝에 "적용 결과" 섹션 추가**
2. **적용 결과 작성**:
   - ✅ 적용 완료: 적용 내용 & 변경 섹션
   - ⏸️ 적용 보류: 판단 사유
   - 📝 조정 적용: 조정 내용
   - 📊 개선 효과
3. **판단 근거 명시**: 적용/보류 사유 기록
4. **Task 상태 업데이트**: `update_task_status(task_number, "design_improved")`
   - 📋 함수: `@docs/common/07.functions/update_task_status.md`
   - 상태: [d→dr→di]

## 맥락 기반 판단 체크리스트

각 이슈에 대해 다음 질문:

1. **시스템 적합성**:
   - 현재 아키텍처 호환?
   - 기술 스택 충돌 없음?
   - 시스템 복잡도 적절 유지?
2. **Task 적합성**:
   - 요구사항 관련?
   - 범위 내?
   - 다른 Task 영향 없음?
3. **실현 가능성**:
   - 구현 가능?
   - 비용 대비 효과?
   - 일정 내 완료?
4. **우선순위**:
   - 🔴 P1: 필수 적용 (조정 가능)
   - 🟠 P2: 적용 권장 (체크리스트 통과 시)
   - 🟡 P3-P5: 유리한 경우만 적용

## 적용 vs 보류 판단 예시

**✅ 적용**:
- P1 보안 → 인증 강화 (시스템 적합 & 필수)
- P2 아키텍처 → API 일관성 (범위 내 & 구현 가능)
- P3 성능 → 캐싱 (기술 스택 가능 & 효과 큼)

**⏸️ 보류**:
- P2 마이크로서비스 전환 (범위 초과)
- P1 새 프레임워크 (기술 스택 충돌)
- P3 과도한 추상화 (효과 낮음)

**📝 조정**:
- 리뷰: Redis → 적용: node-cache
- 리뷰: GraphQL → 적용: REST 최적화
- 리뷰: RBAC → 적용: 단순 권한

## 리뷰 문서 "적용 결과" 템플릿

> 기존 리뷰 파일 **끝에 추가**

```markdown
---

# 📋 개선사항 적용 결과

**적용일**: {YYYY-MM-DD}
**적용자**: Claude Sonnet 4.5
**수정 설계서**: `./docs/project/maru/10.design/12.detail-design/{task-id}.{task명}(상세설계).md`

## 🧠 적용 방침
- ✅ 시스템&Task 적합 → 적용
- 📝 조정 필요 → 수정 적용
- ⏸️ 부적합 → 보류

## ✅ 적용 완료 이슈

### [ID] 제목 (P1/P2/P3)
- **원본**: {제안 내용}
- **방식**: ✅ 그대로 / 📝 조정
- **내용**: {반영 내용}
- **섹션**: {상세설계서 섹션}
- **이유**: {적용 사유}

## ⏸️ 보류 이슈

### [ID] 제목 (P1/P2/P3)
- **원본**: {제안 내용}
- **사유**: {판단 근거}
- **대안**: {대안 방안}

## 📊 적용 결과 요약

| 구분 | P1 | P2 | P3 | P4 | P5 | 합계 |
|------|----|----|----|----|----|----|
| 리뷰 이슈 | {n} | {n} | {n} | {n} | {n} | {n} |
| 적용 완료 | {n} | {n} | {n} | {n} | {n} | {n} |
| 조정 적용 | {n} | {n} | {n} | {n} | {n} | {n} |
| 보류 | {n} | {n} | {n} | {n} | {n} | {n} |

**카테고리별**:
- 🏗️ 아키텍처: {n}개 적용 / {n}개 보류
- 🛡️ 보안: {n}개 적용 / {n}개 보류
- ⚡ 성능: {n}개 적용 / {n}개 보류
- 📝 품질: {n}개 적용 / {n}개 보류

## 🔄 주요 변경 내역
1. **{섹션}**: {변경 요약}

## 🎯 개선 효과
- 설계 품질: {개선 효과}
- 리스크 해소: {해결 리스크}
- 요구사항 커버리지: {이전}% → {이후}%

## 📝 특이사항
- {특이사항}
- {향후 재검토 항목}
---
```

## 성공 기준

### 필수
1. ✅ 맥락 기반 판단: 모든 이슈 적용/보류/조정 근거 명시
2. ✅ P1 100% 처리 (조정 가능)
3. ✅ 설계 문서 업데이트
4. ✅ 리뷰 문서 적용 결과 추가
5. ✅ 일관성 검증
6. ✅ 추적성 95% 이상

### 권장
- P2 80% 이상 처리
- 실용성 기준 품질 향상
- 보류 이슈 대안 제시
- P3-P5 향후 계획

### ⚠️ 금지
1. ❌ 맹목적 전체 적용
2. ❌ 시스템 맥락 무시
3. ❌ 판단 근거 누락
4. ❌ 과도한 아키텍처 변경
5. ❌ Task 범위 초과

---

**다음**: `/dev:implement` - TDD 기반 구현
